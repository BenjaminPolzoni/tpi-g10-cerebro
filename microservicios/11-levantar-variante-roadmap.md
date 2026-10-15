---
tags: [tpi, g10, runbook, variante, tailscale]
actualizado: 2026-10-15
---

# Levantar nuestra variante del roadmap-service (back + front local)

> [!info] Para qué sirve
> Probar cambios (por ejemplo HU-45) con **nuestro** back y **nuestro** front corriendo en paralelo, pegándole a los otros micros de la plataforma, **sin tocar la instancia estable** (que es de otra persona, ver [[microservicios/10-roadmap-service]]). Solo los pedidos que llevan el nombre de la variante llegan a ella; el resto sigue a la estable.

## Skills que lo cubren (en `~/.claude/skills/`)

| Skill | Para qué |
|---|---|
| `own-variant-of-a-micro-beside-the-stable` | **La principal.** Levanta la variante del micro en la malla Tailscale (header `X-Tpi-Variant`), con su propia base y su propio Kafka, y apunta el front local a ella. |
| `local-front-through-tailscale-mesh` | Arma el front local (nginx de borde + sidecar de Tailscale) contra la API compartida, incluido `/_s3/` para el Garage. |
| `levantar-micro` | Levanta un micro **sin** variante (`APP_VARIANT` vacío). Solo si no se quiere variante. |
| `integrate-micro-gateway` | Antes de todo: genera `tpi-integration.yml`. Ya está hecho en el roadmap. |

Documentación del equipo de plataforma: `tpi-system-compose/docs/variants.md` y `docs/mesh.md`.

## Qué hace falta

- Docker Desktop **corriendo** (no lo arranca el asistente).
- Back (`Backend/tpi-roadmap`): `tpi-integration.yml` (existe) y `.tpi/platform/` (plantilla ya instalada; `.env` y `.generated/` están ignorados).
- `.tpi/platform/.env` con: `SERVICE_ID=roadmap-service`, `SEGMENT=roadmap`, `PORT=8010`, `DATABASE=postgres`, `BUILD_CONTEXT=../..`, `APP_VARIANT=polzoni`, y las claves `TS_AUTHKEY` (clave reutilizable de Tailscale con tag `tag:microservicio`), `DB_PASSWORD` y `APP_CLIENT_SECRET` (la propia del roadmap).
- Front (`Frontend/local-edge`): carpeta con su `docker-compose.yml`, `nginx/` y `.env` con `LOCAL_PORT=8000`, `TS_HOSTNAME=group-10-frontend-polzoni-2`, `TS_AUTHKEY` (clave **distinta**, con tag `tag:frontend-edge`) y `WEBAPP_IMAGE=tpi-front-webapp:<commit>`.
- Las claves se piden a Rami Ibazeta o Santiago Moya. Van **solo** en esos `.env`: nunca en el chat, un log, un commit ni esta nota.

> [!warning] Nombre de la variante
> Dos personas con el mismo nombre pisan la misma instancia del mismo micro. Usamos `polzoni`. Si otro micro de G10 quiere sumarse al mismo camino, se levanta con `APP_VARIANT=polzoni`.

## Pasos

1. **Back** (desde `Backend/tpi-roadmap`):
   ```bash
   .tpi/platform/up.sh mesh
   ```
   El `Dockerfile` compila el jar él mismo (no hace falta `mvnw` antes). Construye lo que haya en la rama que tengas **checked out**. Tarda unos minutos la primera vez.
2. **Front**, una sola vez: copiar el par de nginx de la plantilla al front y apuntarlo a la variante.
   ```bash
   FRONT=/Users/benjaminpolzoni/dev/TPI_2026/Frontend/local-edge
   cp -n $FRONT/nginx/default.conf $FRONT/nginx/default.conf.pre-storage
   cp -n $FRONT/nginx/proxy-common.inc $FRONT/nginx/proxy-common.inc.pre-storage
   cp .tpi/platform/front-nginx/default.conf .tpi/platform/front-nginx/proxy-common.inc $FRONT/nginx/
   .tpi/platform/front-variant.sh "$FRONT" on --name polzoni
   ```
   Levanta tres contenedores (`mesh`, `webapp`, `edge`) y deja todo lo que sale del front con `X-Tpi-Variant: polzoni`.
3. **Verificar**:
   ```bash
   .tpi/platform/verify.sh mesh        # repetir tras ~1 min si Eureka no la vio todavía
   curl -s localhost:8000/healthz                                   # ok
   curl -s -o /dev/null -w '%{http_code}\n' localhost:8000/.well-known/jwks.json   # 200
   curl -s -o /dev/null -w '%{http_code}\n' localhost:8000/_s3/     # 403 = llega al Garage
   curl -si localhost:8000/api/roadmap/public/ping | grep -i served-by   # X-Tpi-Served-By: roadmap-service:polzoni
   ```
4. **Usar**: abrir `http://localhost:8000` (siempre por el puerto de loopback, no por el 4200).

## Bajar todo

```bash
.tpi/platform/front-variant.sh "$FRONT" off        # el front deja de apuntar a la variante
.tpi/platform/up.sh mesh --down                    # el micro, su sidecar y su base (--volumes borra los datos)
docker image rm roadmap-service-polzoni-app
```

## Qué esperar (lo que aprendimos el 2026-10-15)

- Primera corrida: `verify.sh` puede dar FAIL de Eureka durante 30–60 s; se resuelve solo. Con la variante registrada, la respuesta trae `X-Tpi-Served-By: roadmap-service:polzoni`.
- **Kafka aislado** (`KAFKA_MODE` vacío): la variante tiene su propio broker, vacío; **no recibe eventos reales** (XP del Motor, inscripciones, etc.). Para probar con eventos reales hay que usar `KAFKA_MODE=routed`, con la salvedad de que no garantiza efectos únicos frente a la estable.
- **Base propia y vacía**: la variante aplica sus migraciones pero no tiene datos de cohortes. Para probar el ranking hace falta cargar datos (seed, ver HT-21) o mirar contra Courses con una cohorte real.
- La imagen del front sale de un commit concreto (`WEBAPP_IMAGE=tpi-front-webapp:<hash>`): no es el árbol de trabajo. Para ver cambios del front hay que reconstruirla o usar el overlay de hot reload (ver la skill `local-front-through-tailscale-mesh`, sección "Dev server").
- `verify.sh` avisa "template is behind main": la plantilla instalada es vieja; repetir el paso 1 de `levantar-micro` para actualizarla (conserva el `.env`).
- Nunca agregar `ports:` al micro ni publicar `:8082`. Los nombres de la tailnet van siempre con FQDN (`tpi-plataforma.tail767776.ts.net`).

## Relacionado

[[microservicios/10-roadmap-service]] · [[sprints/sprint-3/historias/HU-45 Ranking de la cohorte y avance por comisión|HU-45]] · [[sprints/sprint-3/12-responsables]]
