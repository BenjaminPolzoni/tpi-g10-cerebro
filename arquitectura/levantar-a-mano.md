---
tags: [tpi, g10, runbook, frontend, docker, tailscale, edge]
actualizado: 2026-11-05
---

# Levantar el Frontend Local a Mano (Edge + Mesh + Webapp)

> [!info] Resumen
> Guía paso a paso para compilar y desplegar manualmente el frontend en contenedores locales, conectarlo a la **Tailnet compartida** mediante el sidecar de Tailscale y rutear llamadas al backend remoto (`tpi-plataforma`).

---

## 🗺️ Modelo Mental y Arquitectura

El entorno frontend local se orquesta mediante Docker Compose en tres contenedores que comparten el mismo espacio de red (`network_mode: "service:mesh"`):

```mermaid
flowchart TD
    subgraph Host ["Tu Mac / PC (127.0.0.1:8000)"]
        Browser["Navegador / Curl"]
        subgraph DockerMesh ["Red del Sidecar (front-local)"]
            Mesh["mesh (Tailscale)<br/>ts.net IP: 100.x.y.z<br/>Puerto: 8000"]
            Edge["edge (Nginx Proxy)<br/>Puerto: 8000"]
            Webapp["webapp (Frontend)<br/>Nginx serviendo Angular :4200"]
        end
    end

    subgraph Tailnet ["Malla Tailscale Compartida"]
        Platform["tpi-plataforma.tail767776.ts.net<br/>100.92.236.38 :80 (API Gateway)"]
    end

    Browser -->|http://localhost:8000/| Edge
    Edge -->|/ (rutas web, assets, JS, CSS)| Webapp
    Edge -->|/api/* (llamadas backend)| Platform
```

* **`front-local-mesh-1`:** Sidecar de Tailscale. Conecta el entorno local a la Tailnet privada y expone `127.0.0.1:8000` en tu máquina.
* **`front-local-webapp-1`:** Contenedor Nginx ligero que sirve los assets y bundles estáticos de Angular en el puerto interno `4200`.
* **`front-local-edge-1`:** Proxy inverso local. Rutea el frontend desde `webapp` y redirige el tráfico de API hacia la plataforma compartida.

---

## 📋 Paso a Paso

### Paso 1: Actualizar rama y obtener el commit

📍 **Dónde pararse:** En la raíz del repositorio de código del frontend:
```bash
cd /Users/benjaminpolzoni/dev/TPI_2026/Frontend/2026-PIV-TPI-FE
```

```bash
# 1. Pararse en develop y sincronizar con el remoto
git checkout develop
git pull --ff-only origin develop

# 2. Guardar el hash corto del commit en una variable de entorno
H=$(git rev-parse --short HEAD)
echo "Commit a compilar: $H"
```

#### ¿Qué significa cada parámetro?
* `git pull --ff-only origin develop`:
  * `--ff-only`: Fast-forward only. Se niega a fusionar si hay commits locales divergentes, garantizando que el árbol sea idéntico al remoto.
* `H=$(git rev-parse --short HEAD)`:
  * `git rev-parse --short HEAD`: Extrae el SHA corto de 7 a 10 caracteres del commit actual (ej. `3d063e37b6`).
  * `H=...`: Variable de shell reutilizada para etiquetar la imagen Docker.

---

### Paso 2: Exportar el código al directorio de build y aplicar parche de budgets

Para que Docker no procese archivos innecesarios (`node_modules`, `.git`, etc.), se genera un export limpio del repositorio y se incrementan los límites de tamaño en `angular.json` para evitar que la compilación de producción falle por presupuestos estrictos de CSS.

📍 **Dónde pararse:** En la carpeta de build del entorno:
```bash
cd /Users/benjaminpolzoni/dev/TPI_2026/Frontend/local-edge/build
```

```bash
# 1. Limpiar export previo y recrear la carpeta de código fe/
rm -rf fe && mkdir fe

# 2. Exportar el árbol del commit $H directamente a fe/
(cd /Users/benjaminpolzoni/dev/TPI_2026/Frontend/2026-PIV-TPI-FE && git archive $H) | tar -x -C fe

# 3. Elevar los límites de budgets de estilos en angular.json
sed -i '' 's/"maximumWarning": "8kB"/"maximumWarning": "60kB"/; s/"maximumError": "10kB"/"maximumError": "100kB"/; s/"maximumError": "3MB"/"maximumError": "6MB"/' fe/angular.json
```

#### ¿Qué significa cada parámetro?
* `git archive $H`: Genera un stream tar en memoria con los archivos tracked del commit `$H`.
* `tar -x -C fe`:
  * `-x`: Extrae el contenido del tar.
  * `-C fe`: Especifica el directorio de destino.
* `sed -i '' 's/.../.../' fe/angular.json`:
  * `-i ''`: Modificación in-place compatible con macOS (BSD sed).
  * Eleva el error máximo de estilos por componente a `100kB` y del bundle inicial a `6MB` (necesario por componentes arcade/3D).

---

### Paso 3: Compilar la imagen Docker del frontend

📍 **Dónde pararse:** `local-edge/build`:
```bash
cd /Users/benjaminpolzoni/dev/TPI_2026/Frontend/local-edge/build
```

```bash
docker build -f ../Dockerfile.front-no-token -t tpi-front-webapp:develop-$H .
```

#### ¿Qué significa cada parámetro?
* `docker build`: Comando de construcción de imágenes Docker.
* `-f ../Dockerfile.front-no-token`: Apunta al Dockerfile especial que utiliza el paquete empaquetado `ui-kit.tgz`, evitando pedir token de GitHub Packages durante el build.
* `-t tpi-front-webapp:develop-$H`: Etiqueta (`tag`) la imagen con el identificador del commit.
* `.`: Directorio de contexto actual (contiene `fe/` y `ui-kit.tgz`).

> [!tip] Tiempo de compilación
> Este paso ejecuta `npm install` y `npm run build:prod` de Angular dentro del contenedor; demora entre 2 y 3 minutos habitualmente.

---

### Paso 4: Levantar o recrear el contenedor en Docker Compose

📍 **Dónde pararse:** En la carpeta `local-edge`:
```bash
cd /Users/benjaminpolzoni/dev/TPI_2026/Frontend/local-edge
```

```bash
WEBAPP_IMAGE=tpi-front-webapp:develop-$H docker compose -f docker-compose.yml up -d --no-deps webapp
```

#### ¿Qué significa cada parámetro?
* `WEBAPP_IMAGE=tpi-front-webapp:develop-$H`: Sobrescribe la variable del `docker-compose.yml` para usar la imagen que acabamos de compilar.
* `-f docker-compose.yml`: Especifica el archivo compose principal.
* `up -d`: Levanta en segundo plano (*detached mode*).
* `--no-deps`: No reinicia los contenedores dependientes (`mesh` y `edge`), solo recrea `webapp`.
* `webapp`: Nombre del servicio que se actualizará.

---

### Paso 5: Verificación y Pruebas

#### 1. Validar que los 3 contenedores estén arriba:
```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
```
Debes ver:
* `front-local-mesh-1` en estado `healthy`.
* `front-local-webapp-1` en estado `Up`.
* `front-local-edge-1` en estado `Up`.

#### 2. Validar visibilidad de Tailscale hacia el backend:
```bash
docker exec front-local-mesh-1 tailscale status
```
* Debe figurar el nodo `100.92.236.38  tpi-plataforma` activo en la lista.

#### 3. Probar la API del backend desde el host:
```bash
curl -i http://127.0.0.1:8000/api/users/public/organizations/tup
```
* Debe retornar `HTTP/1.1 200 OK` junto al JSON de la organización TUP.

#### 4. Probar la aplicación en el navegador:
Abrir: **[http://localhost:8000/o/tup/login](http://localhost:8000/o/tup/login)**

---

## 🚨 Troubleshooting (Problemas Frecuentes)

### Error 504 Gateway Timeout o pantalla en blanco al cargar datos
* **Causa:** La sesión efímera de Tailscale del sidecar (`front-local-mesh-1`) caducó o perdió sincronización con los servidores de coordinación tras muchas horas encendido.
* **Solución (Reset limpio de Tailscale):**

```bash
cd /Users/benjaminpolzoni/dev/TPI_2026/Frontend/local-edge

# 1. Bajar el compose y destruir el volumen de estado de Tailscale
WEBAPP_IMAGE=tpi-front-webapp:develop-$H docker compose down -v

# 2. Levantar el stack completo (crea una nueva sesión en Tailscale usando TS_AUTHKEY de .env)
WEBAPP_IMAGE=tpi-front-webapp:develop-$H docker compose up -d

# 3. Esperar 15 segundos al healthcheck y reintentar
curl -i http://127.0.0.1:8000/api/users/public/organizations/tup
```
