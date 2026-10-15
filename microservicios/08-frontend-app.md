# Aplicación Frontend: Angular SPA (`2026-PIV-TPI-FE`)

> **Ficha Técnica Canónica y Guía de Integración**  
> Tema: **Frontend Unificado de la Plataforma**  
> Equipo Responsable: **Equipo de Frontend (P4)**  
> Repositorio: `2026-P4-FE/2026-PIV-TPI-FE` (Local: `D:\Dev\IdeaProjects\Progra4\2026-PIV-TPI-FE`)  
> Estado: **Vigente (v2.0.0)**

---

## 1. Identidad y Arquitectura de Ejecución

| Parámetro | Valor |
|---|---|
| **Tecnología Base** | Angular 18+ (Standalone Components, Signals, RxJS) |
| **Librería de Componentes** | UI Kit Oficial `@2026-p4-fe/ui` (mandatorio) |
| **Render 3D y Canvas** | Three.js / WebGL (visor de grafos, biomas y avatares 3D) |
| **Puerto Dev Local (Angular CLI)** | `http://localhost:4200` |
| **Puerto Mesh con Nginx Edge** | `http://localhost:8000` (puerto loopback recomendado) |
| **Almacenamiento de Objetos 3D** | Garage S3 Object Storage (`/_s3/`, puerto 3900) |

---

## 2. Modos de Ejecución

### Modo A: Dev Server Local (Hot Reload)
- Configura `proxy.conf.json` apuntando hacia el API Gateway local (`http://localhost:8080`) o directamente hacia `roadmap-service` (`http://localhost:8010`).
- Comando: `npm run start`

### Modo B: Tailnet Mesh con Sidecar Nginx (Convención Organizacional)
El frontend corre contenido en tres contenedores coordinados:
1. `mesh`: Sidecar Tailscale con tag `tag:frontend-edge` y hostname `group-10-frontend-<apellido>`.
2. `edge`: Nginx que sirve la app en `/`, redirige `/api/` y `/.well-known/` a `http://tpi-plataforma.tail767776.ts.net:80`, y reescribe Garage S3 a `/_s3/`.
3. `webapp`: Bundle compilado de Angular o servidor Vite/Angular con live reload.
- **Acceso:** Se accede **exclusivamente por loopback:** `http://localhost:8000` (nunca por `:4200` directo en este modo).

---

## 3. Módulos y Pantallas del Dominio Roadmap

### 3.1 Grafo y Visor 3D del Roadmap (`/courses/{courseId}/roadmap`)
- Consume `GET /api/roadmap/courses/{courseId}/graph`.
- Renderiza nodos en un espacio interactivo tridimensional:
  - Metadatos visuales: `biome_key` (`FOREST`, `DESERT`, `CYBER`, etc. según V22), `icon_key` (V20) y posiciones espaciales `(x, y, z)` del editor gráfico (V23).
  - Estado visual del nodo: `LOCKED`, `UNLOCKED`, `COMPLETED`, `IN_PROGRESS`.

### 3.2 Gate de Elegibilidad Previo al Desafío
- Al hacer clic en un nodo de desafío, la UI consulta el Gate:  
  `GET /api/roadmap/courses/{courseId}/students/{studentId}/nodes/{nodeId}/eligibility`
- Si `eligible=false`, muestra un modal explicativo con los motivos (falta de vidas, prerequisitos incompletos, lecturas previas obligatorias).
- Si `eligible=true`, habilita el botón para iniciar el intento en el Motor.

### 3.3 Personalizador del Avatar 3D (`/courses/{courseId}/avatar`)
- Permite al estudiante seleccionar y previsualizar su modelo 3D GLB, accesorios, colores y animaciones.
- Guarda la personalización en `PUT /api/roadmap/courses/{courseId}/students/{studentId}/avatar`.

### 3.4 Pantalla de Inventario del Alumno (HU-35, `/courses/{courseId}/inventory`)
- Consume `GET /api/roadmap/courses/{courseId}/inventory`.
- Muestra el saldo de vidas, tope máximo, saldo de monedas e ítems cosméticos equipados.
- Si el backend responde con `stale: true`, despliega un badge amarillo informando que los datos son temporales debido a intermitencias de red.

### 3.5 Ranking Dinámico y Zonas Percentiles (`/courses/{courseId}/leaderboard`)
- Consume `GET /api/roadmap/courses/{courseId}/rankings`.
- Muestra el podio, posición del alumno y su zona de rendimiento (P90 oro, MIDDLE azul, P10 naranja), activas dinámicamente si la cohorte posee $\ge 10$ participantes.

---

## 4. Convenciones de Consumo HTTP y Seguridad
- **Cookie de Sesión `fu_at`:** La autenticación se propaga mediante cookie HTTP-only con `withCredentials: true`.
- **Formato de Payloads:** Todos los contratos se comunican en `snake_case`. El interceptor de Angular o los modelos TypeScript tipan los campos respetando la convención de backend.
- **Manejo de Errores Problem Details:** Los fallos `4xx` y `5xx` se parsean extrayendo `title`, `detail`, `instance` y `trace_id` para feedback al usuario.
