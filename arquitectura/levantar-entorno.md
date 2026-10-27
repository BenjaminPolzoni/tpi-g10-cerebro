---
tags: [tpi, g10, runbook, entorno, tailscale, skills]
actualizado: 2026-10-26
---

# Levantar el entorno: front + back (estable o de prueba)

> [!info] Resumen en una línea
> No corremos la plataforma completa en la PC. Nos conectamos por **Tailscale** a la plataforma compartida (`tpi-plataforma.tail767776.ts.net`). El **back estable** ya está ahí; el **back de prueba** es una *variante* de nuestro micro (`roadmap-service`) que se registra en la misma malla y a la que solo llegan los pedidos que llevan nuestro nombre. El **front** corre local (nginx de borde + sidecar de Tailscale) y le pega a la API compartida.

Runbook paso a paso de la variante del roadmap: [[microservicios/11-levantar-variante-roadmap]]. Contexto del micro: [[microservicios/10-roadmap-service]].

## Cómo funciona (modelo mental)

```mermaid
flowchart LR
  B[Navegador<br/>localhost:8000] --> E[edge nginx local]
  E -->|/api, /.well-known<br/>+ X-Tpi-Variant: polzoni| P[Edge de la plataforma<br/>tailscale serve :80]
  E -->|/_s3/| G[Garage :3900]
  P --> GW[API Gateway]
  GW -->|sin header| S[roadmap-service ESTABLE<br/>de un compañero]
  GW -->|con header polzoni| V[roadmap-service:polzoni<br/>nuestra PC]
  GW --> O[Otros micros<br/>Courses, Users, Accounting...]
```

- **Front local** = 3 contenedores: `mesh` (sidecar Tailscale, nodo `group-10-frontend-polzoni-2`), `webapp` (build o dev server) y `edge` (nginx). Solo sale a TCP 80 y 3900 de la plataforma; publica el puerto **solo en loopback** (`127.0.0.1:8000`).
- **Back** = el micro + su sidecar Tailscale + su base Postgres propia + (por defecto) su Kafka propio. Entra a la malla con una clave `tag:microservicio` y se registra en Eureka.
- **Variante** = el gateway elige instancia por el header `X-Tpi-Variant` (o cookie). El front local lo inyecta en todo `/api/` cuando se activa con `front-variant.sh on`. Sin header → instancia estable.
- Identidad: el login lo resuelve users-service; el gateway propaga la identidad. El micro no valida JWT, solo `GatewayIdentityFilter`.

## Back estable vs. back de prueba

| | Estable | De prueba (variante) |
|---|---|---|
| Quién la corre | **Un compañero** (no esta PC) | Esta PC |
| `APP_VARIANT` | vacío | `polzoni` (rama de trabajo, `Backend/tpi-roadmap`) o `polzoni-develop` (contingencia, worktree `Backend/tpi-roadmap-stable` en `origin/develop`) |
| Qué hacemos nosotros | Nada: usamos la plataforma tal cual (front sin variante) | `up.sh mesh` + `front-variant.sh on` |
| Datos / Kafka | Reales | Base propia **vacía**; Kafka aislado (sin eventos reales) salvo `KAFKA_MODE=routed` |

> [!danger] NUNCA levantar el roadmap estable desde esta PC
> Con `APP_VARIANT` vacío pisamos la instancia del compañero (mismo id de Eureka `roadmap-service:8010` y mismo nodo en la tailnet). Antes de cualquier `up.sh mesh`, **verificar que `.tpi/platform/.env` tenga `APP_VARIANT`**. Esta PC es la secundaria.

**Usar el back estable desde el front** = levantar el front local *sin* overlay de variante (`front-variant.sh off`): todo va a la estable.
**Usar el back de prueba** = variante levantada + `front-variant.sh on --name polzoni`.

## Skills (en `~/.claude/skills/`)

| Skill | Cuándo |
|---|---|
| `own-variant-of-a-micro-beside-the-stable` | **La principal para el back de prueba.** Elige el nombre, instala la plantilla, pide Kafka, levanta, verifica y (opcional) apunta el front. |
| `local-front-through-tailscale-mesh` | Arma el front local (compose + nginx + sidecar), build o dev server con hot reload, y `/_s3/` para Garage. |
| `levantar-micro` | Levantar un micro **sin** variante (`APP_VARIANT` vacío). **No usar para roadmap** (ver aviso). |
| `integrate-micro-gateway` | Integrar un micro Spring MVC con el gateway; genera `tpi-integration.yml`. Roadmap ya lo tiene. |

Plantilla del equipo de plataforma: repo `2026-P4-BE/tpi-system-compose` (carpeta `team/`), docs `docs/variants.md` y `docs/mesh.md`. Se instala en `Backend/<micro>/.tpi/platform/` (`up.sh`, `verify.sh`, `front-variant.sh`).

## Claves y secretos

| Variable | Dónde va | Qué es / de dónde sale |
|---|---|---|
| `TS_AUTHKEY` (back) | `Backend/tpi-roadmap/.tpi/platform/.env` | Clave Tailscale reutilizable con tag `tag:microservicio` |
| `DB_PASSWORD` | ídem | Contraseña de la base del micro (la elige el equipo) |
| `APP_CLIENT_SECRET` | ídem | Secreto **propio** del roadmap para pedir service-token a otros micros. Sin él, el micro arranca pero las llamadas micro→micro dan 401. No reusar el de otro micro |
| `TS_AUTHKEY` (front) | `Frontend/local-edge/.env` | Clave **distinta**, efímera, tag `tag:frontend-edge` (solo TCP 80 y 3900 de la plataforma). No pedir `tag:microservicio` para el front |
| `S3_ACCESS_KEY` / `S3_SECRET_KEY` | `.env` del micro | Solo si el micro guarda archivos en Garage (las da quien administra Garage) |
| `NODE_AUTH_TOKEN` | `.env` del front | Solo para el dev server con hot reload: PAT `read:packages` para el UI kit privado. Sin token se instala desde el tarball de `Frontend/local-edge/build/ui-kit.tgz` |

Variables no secretas del `.env` del back: `SERVICE_ID=roadmap-service`, `SEGMENT=roadmap`, `PORT=8010`, `DATABASE=postgres`, `BUILD_CONTEXT=../..`, `APP_VARIANT=polzoni`, `KAFKA_MODE` (vacío = aislado; `routed` = Kafka real con grupo propio; `shared` solo si el micro soporta `APP_VARIANT_GROUP_SUFFIX`). Del front: `LOCAL_PORT=8000`, `TS_HOSTNAME=group-10-frontend-polzoni-2`, `WEBAPP_IMAGE=tpi-front-webapp:<commit>`.

- Las claves las dan **Rami Ibazeta** o **Santiago Moya** por canal privado.
- Van **solo** en esos `.env` (ignorados por git). Nunca en chat, log, commit ni en este vault.
- Convención de ubicación de la clave recibida: `~/.config/tpi-plataforma-unificada/front/`.

## Receta corta

Prerrequisito: **Docker Desktop corriendo** (lo arranca el usuario, no el asistente).

```bash
# 1. Back de prueba (desde Backend/tpi-roadmap, rama que se quiera probar checked out)
grep APP_VARIANT .tpi/platform/.env          # debe decir polzoni
.tpi/platform/up.sh mesh                     # el Dockerfile compila el jar; minutos la primera vez
.tpi/platform/verify.sh mesh                 # repetir tras ~1 min si Eureka no la vio

# 2. Front local (una vez) apuntado a la variante. No buildea: solo agrega el header X-Tpi-Variant.
#    Para buildear una imagen nueva del front, ver "Buildear la imagen del front desde cualquier worktree".
FRONT=~/dev/TPI_2026/Frontend/local-edge
.tpi/platform/front-variant.sh "$FRONT" on --name polzoni

# 3. Chequeos
curl -s localhost:8000/healthz                                          # ok
curl -s -o /dev/null -w '%{http_code}\n' localhost:8000/.well-known/jwks.json   # 200
curl -s -o /dev/null -w '%{http_code}\n' localhost:8000/_s3/            # 403 = llega a Garage
curl -si localhost:8000/api/roadmap/public/ping | grep -i served-by     # roadmap-service:polzoni
```

Abrir siempre `http://localhost:8000` (nunca el `4200`: las URLs de storage reescritas son relativas al origen).

**Bajar todo**
```bash
.tpi/platform/front-variant.sh "$FRONT" off   # el front vuelve a la estable
.tpi/platform/up.sh mesh --down               # --volumes también borra los datos
docker image rm roadmap-service-polzoni-app
```

**Front: build vs. hot reload.** La imagen sale de un commit (`WEBAPP_IMAGE`), no del árbol de trabajo. Para ver cambios del front al instante: `docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d` (overlay del dev server, ver skill `local-front-through-tailscale-mesh`). Reconstruir tras cambios de nginx: `docker compose up -d --force-recreate` (un `up -d` simple deja el nginx viejo).

### Buildear la imagen del front desde cualquier worktree

**Actualización (2026-10-26).** Copiar y pegar bloque por bloque, en orden. Cada paso dice **dónde pararse** y **qué hace**. Mac = Terminal (zsh/bash). Windows = **PowerShell**, salvo el paso 5, que es un script bash y va en **Git Bash**.

> [!warning] Antes de empezar
> - **Docker Desktop tiene que estar corriendo.**
> - Cambiar `<worktree>` por la carpeta del front que se quiere buildear (por ejemplo `2026-PIV-TPI-FE`).
> - Las rutas suponen el repo en `~/dev/TPI_2026` (Mac) o `$HOME\dev\TPI_2026` (Windows). Si lo tenés en otro lado, ajustalas.
> - Las variables (`WT`, `TAG`) viven solo en esa consola: hacer todos los pasos en la **misma ventana**.
> - Los bloques de Windows no están probados en una PC con Windows: si alguno falla, anotar acá el arreglo.

#### Paso 0. Pararse en el front local y definir qué se buildea

**Dónde:** cualquier lado; el bloque te mueve a `Frontend/local-edge`, donde están el `docker-compose.yml`, el `.env` y el `Dockerfile.front-no-token`.
**Qué hace:** guarda en `WT` la ruta del worktree y en `TAG` el commit actual (9 caracteres), que va a ser el nombre de la imagen.

Mac:
```bash
cd ~/dev/TPI_2026/Frontend/local-edge
WT=~/dev/TPI_2026/Frontend/<worktree>
TAG=$(git -C "$WT" rev-parse --short=9 HEAD)
echo "$TAG"
```

Windows (PowerShell):
```powershell
cd $HOME\dev\TPI_2026\Frontend\local-edge
$WT  = "$HOME\dev\TPI_2026\Frontend\<worktree>"
$TAG = git -C $WT rev-parse --short=9 HEAD
$TAG
```

#### Paso 1. Copiar el código del worktree a la carpeta de build

**Dónde:** `Frontend/local-edge` (paso 0).
**Qué hace:** borra `build/fe` y copia ahí los archivos del worktree que trackea git **más los nuevos sin commitear** (respeta `.gitignore`, así que no copia `node_modules`). Es lo que va a entrar en la imagen. Elegir **una** de las dos opciones.

Opción A: el worktree como está (con cambios sin commitear).

Mac:
```bash
rm -rf build/fe && mkdir -p build/fe
git -C "$WT" ls-files -co --exclude-standard | rsync -a --files-from=- "$WT"/ build/fe/
```

Windows (PowerShell):
```powershell
Remove-Item -Recurse -Force build\fe -ErrorAction SilentlyContinue
git -C $WT ls-files -co --exclude-standard | ForEach-Object {
  $dst = Join-Path build\fe $_
  New-Item -ItemType Directory -Force (Split-Path $dst) | Out-Null
  Copy-Item (Join-Path $WT $_) $dst
}
```

Opción B: `develop` limpio, sin nada local. En este caso el `TAG` tiene que ser el de develop.

Mac:
```bash
git -C "$WT" fetch origin develop
TAG=$(git -C "$WT" rev-parse --short=9 origin/develop)
rm -rf build/fe && mkdir -p build/fe
git -C "$WT" archive -o "$PWD/build/fe.tar" origin/develop && tar -xf build/fe.tar -C build/fe && rm build/fe.tar
```

Windows (PowerShell):
```powershell
git -C $WT fetch origin develop
$TAG = git -C $WT rev-parse --short=9 origin/develop
Remove-Item -Recurse -Force build\fe -ErrorAction SilentlyContinue; New-Item -ItemType Directory build\fe | Out-Null
git -C $WT archive -o "$PWD\build\fe.tar" origin/develop; tar -xf build\fe.tar -C build\fe; Remove-Item build\fe.tar
```

#### Paso 2. Parchear el límite de CSS (solo en la copia)

**Dónde:** `Frontend/local-edge`.
**Qué hace:** en `build/fe/angular.json` sube el `maximumError` del budget `anyComponentStyle` a `200kb`. Sin esto `build:prod` de develop falla porque varios componentes pasan el límite. Toca **solo la copia**, nunca el repo.

Mac:
```bash
sed -i '' '/"anyComponentStyle"/,/maximumError/ s/"maximumError": "[^"]*"/"maximumError": "200kb"/' build/fe/angular.json
grep -A2 anyComponentStyle build/fe/angular.json
```

Windows (PowerShell):
```powershell
$f = "build\fe\angular.json"
(Get-Content $f -Raw) -replace '("anyComponentStyle",\s*"maximumWarning":\s*"[^"]*",\s*"maximumError":\s*)"[^"]*"', '$1"200kb"' | Set-Content $f -NoNewline
Select-String -Path $f -Pattern anyComponentStyle -Context 0,2
```

La última línea tiene que mostrar `"maximumError": "200kb"`.

#### Paso 3. Buildear la imagen (unos 15 minutos)

**Dónde:** `Frontend/local-edge`.
**Qué hace:** compila Angular en modo producción dentro de Docker con lo que hay en `build/` y crea la imagen `tpi-front-webapp:<TAG>`. No hace falta token de GitHub: el UI kit sale del tarball `build/ui-kit.tgz`.

Mac:
```bash
docker build -f Dockerfile.front-no-token -t tpi-front-webapp:$TAG build
```

Windows (PowerShell):
```powershell
docker build -f Dockerfile.front-no-token -t "tpi-front-webapp:$TAG" build
```

#### Paso 4. Usar la imagen nueva y levantar el front

**Dónde:** `Frontend/local-edge`.
**Qué hace:** cambia `WEBAPP_IMAGE` en el `.env` para que apunte a la imagen recién creada y levanta los 3 contenedores (`mesh`, `webapp`, `edge`). Si ya había un front corriendo, lo reemplaza. Le pega al **back estable**.

Mac:
```bash
sed -i '' "s/^WEBAPP_IMAGE=.*/WEBAPP_IMAGE=tpi-front-webapp:$TAG/" .env
docker compose up -d
curl -s localhost:8000/healthz
```

Windows (PowerShell):
```powershell
(Get-Content .env) -replace '^WEBAPP_IMAGE=.*', "WEBAPP_IMAGE=tpi-front-webapp:$TAG" | Set-Content .env
docker compose up -d
curl.exe -s localhost:8000/healthz
```

El último comando tiene que responder `ok`. Abrir **`http://localhost:8000`**.

#### Paso 5 (opcional). Apuntar el front a nuestro back de prueba (variante polzoni)

**Este paso no buildea nada.** Agrega el header `X-Tpi-Variant: polzoni` al nginx del front y lo reinicia, así las llamadas al roadmap van a nuestra variante (`roadmap-service:polzoni`) en vez de a la estable. Solo sirve si la variante está levantada (paso 1 de la receta corta).

**Dónde:** `Backend/tpi-roadmap`, porque el script vive en `.tpi/platform/` de ese repo y la ruta es relativa.

Mac:
```bash
cd ~/dev/TPI_2026/Backend/tpi-roadmap
FRONT=~/dev/TPI_2026/Frontend/local-edge
.tpi/platform/front-variant.sh "$FRONT" on --name polzoni
curl -si localhost:8000/api/roadmap/public/ping | grep -i served-by
```

Windows (**Git Bash**, no PowerShell):
```bash
cd ~/dev/TPI_2026/Backend/tpi-roadmap
FRONT=~/dev/TPI_2026/Frontend/local-edge
.tpi/platform/front-variant.sh "$FRONT" on --name polzoni
curl -si localhost:8000/api/roadmap/public/ping | grep -i served-by
```

Tiene que decir `roadmap-service:polzoni`. Para volver a la estable: el mismo comando con `off` en vez de `on --name polzoni`.

#### Notas

- **Acceso desde otro nodo del tailnet (hipótesis, sin verificar):** `http://group-10-frontend-polzoni-2.tail767776.ts.net:8000`. nginx escucha en el `:8000` dentro del namespace del sidecar, pero depende de que las ACL dejen entrar a `tag:frontend-edge`.
- **Dos fronts a la vez:** el paso 4 reemplaza al que corre. Para tener dos, el segundo stack necesita otro `LOCAL_PORT`, otro `TS_HOSTNAME` y otro nombre de proyecto (`docker compose -p <nombre> ...`).

### Garage y `/_s3`: las dos formas de la URL firmada

> [!warning] Hallazgo del 2026-10-26
> El profe no podía guardar un `.html` desde la vista simple, y el visor 3D no podía leer el material. En DevTools: `POST .../contents` → `201`, el `PUT` del archivo → `(failed)` con **preflight** fallido (CORS), y enseguida `DELETE .../course-contents/{id}` → `204`, porque el front deshace el alta cuando la subida falla.

**Por qué:** Courses firma las URLs para `http://tpi-plataforma.tail767776.ts.net:3900`, pero el **edge de la plataforma** ya las reescribe a su propio `/_s3` antes de que lleguen a nuestro edge. Entonces al front local le llega `http://tpi-plataforma.tail767776.ts.net/_s3/...` (puerto 80, con `/_s3`). El `nginx/default.conf` de `Frontend/local-edge` solo reescribía la forma vieja (`...:3900`), así que esta pasaba sin tocar: el navegador iba a otro origen y CORS la bloqueaba. Afecta subidas (`PUT`) y lecturas (`GET` del visor, PDF, HTML).

**Cómo darse cuenta rápido:** si en los logs del edge (`docker logs front-local-edge-1`) no aparece ningún pedido a `/_s3/` mientras subís o abrís un archivo, la URL no se está reescribiendo.

**Arreglo:** en `Frontend/local-edge/nginx/default.conf`, dentro de `location /api/`, dejar **las dos** líneas `sub_filter` (nginx acepta varias):

```nginx
sub_filter "http://tpi-plataforma.tail767776.ts.net:3900" "$scheme://$http_host/_s3";
# The platform edge may have already rewritten that origin to its own /_s3: point it here too.
sub_filter "http://tpi-plataforma.tail767776.ts.net/_s3" "$scheme://$http_host/_s3";
```

Después, `docker exec front-local-edge-1 nginx -s reload` (o recrear el edge como en el paso 4). No hace falta rebuildear la imagen del front. La location `/_s3/` no se toca: sigue mandando `Host: tpi-plataforma.tail767776.ts.net:3900`, que es el host para el que Garage valida la firma.

**Chequeo:** `curl -s -o /dev/null -w '%{http_code}\n' localhost:8000/_s3/course-materials/x` → `403` (XML de Garage, sin firma) significa que llega. Después, en el navegador, el `PUT` tiene que ir a `http://127.0.0.1:8000/_s3/...` y **sin** preflight (mismo origen).

> [!tip] Recargar
> Tras cambiar la imagen o el nginx, recargar la pestaña con `Cmd+Shift+R`: el navegador puede seguir con el bundle viejo.

## Reglas que no se rompen

- Nunca `ports:`, `networks:`, `dns:` ni `extra_hosts:` en el servicio del micro. Nunca publicar `:8082` ni puertos de la plataforma (JWKS pasa por el gateway).
- Nombres de la tailnet siempre con FQDN (`tpi-plataforma.tail767776.ts.net`).
- Dos personas con el mismo nombre de variante pisan la misma instancia del mismo micro: usamos `polzoni`; un micro de G10 que se sume al camino se levanta con el mismo `APP_VARIANT`.
- Con `KAFKA_MODE=routed`, tras bajar la variante borrar **solo** su grupo `.variant.<grupo>`; nunca el grupo de la estable.
- La plantilla puede quedar vieja (`verify.sh` avisa "template is behind main"): repetir el paso 1 de `levantar-micro` (conserva el `.env`).

## Síntomas frecuentes

| Síntoma | Causa / acción |
|---|---|
| `502` en el edge tras reconstruir | El edge quedó apuntando al contenedor viejo → `docker compose up -d --force-recreate` |
| `503` problem+json que nombra un micro | Ese micro está caído o sin registrar en Eureka; no es el front |
| `404 page not found` en `/api` con el front cargando | `Host` mal: las locations de API deben mandar el FQDN de la plataforma |
| `400` en `/api` | Dos headers `Host` (puesto en el include y en la location) |
| La página se recarga sola cada 30 s | nginx viejo: copiar `default.conf` y `proxy-common.inc` de la plantilla y recrear |
| El sidecar no llega a `Running` | `TS_AUTHKEY` vacía/truncada/con comillas → `docker compose logs mesh` |
| Verify FAIL de Eureka al inicio | Normal 30–60 s; repetir |
| Variante responde pero sin datos de cohortes | Base propia vacía: cargar seed (HT-21) o mirar contra Courses con cohorte real |
| Sin eventos del Motor/inscripciones | Kafka aislado: usar `KAFKA_MODE=routed` (sin garantía de efectos únicos) |
| `ERR_NAME_NOT_RESOLVED` hacia `...:3900` | Página abierta fuera de `localhost:8000` o nginx sin la ruta `/_s3/` |
| `PUT`/`GET` a `...ts.net/_s3/...` con preflight `(failed)`, y `DELETE` del contenido recién creado | Falta el segundo `sub_filter` (forma `/_s3` del edge de la plataforma). Ver "Garage y `/_s3`" arriba |
| El build falla por el UI kit o faltan exports de `@2026-p4-fe/ui` | `build/ui-kit.tgz` no coincide con la versión del `package-lock.json` del commit: `npm pack @2026-p4-fe/ui@<versión>` en `build/` y copiarlo como `ui-kit.tgz` |
| `400 challengeId: must not be blank` tras el 2FA | Desajuste camelCase/snake_case front↔users-service (ver `decisiones/`) |
