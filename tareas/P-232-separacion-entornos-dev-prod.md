# P-232 — Separación de entornos dev y prod (plan de implementación)

> **Estado:** plan, sin implementación ni deploy. **Fecha:** 2026-10-22. **Fuente:** [issue paraguas #232, tpi-system-compose](https://github.com/2026-P4-BE/tpi-system-compose/issues/232). **Repo principal:** `Backend/tpi-system-compose` (`main`).
>
> **Alcance:** preparar un deploy de producción repetible y ensayarlo en laptop/VM temporal; **no hay servidor de producción todavía**. Los checks de abajo son trabajo pendiente, no evidencia de que ya se cumplió.

## 1. Resultado esperado y límites

`dev` conserva desarrollo local/Tailscale, mocks y seeds permitidos. `prod` arranca con perfil explícito, solo versiones fijas desde `main`, sin datos de demo ni fallbacks inseguros. Faltan variables obligatorias → falla antes de levantar servicios. El primer release se ensaya completo con volúmenes vacíos antes de disponer de un servidor definitivo.

**Exigencias expresas de #232:** `.env.prod`, dominio/puertos y `COMPOSE_PROJECT_NAME`; TLS/cookies; credenciales de Grafana desde Vault; dominio institucional de registro; KID JWT real; imagen FE de la organización; host tailnet parametrizado en Nginx/Kafka; Mailpit excluido; admin institucional y custodia de contraseña; OpenAPI apagado; perfiles explícitos de users/gateway/notificaciones; imágenes `:X.Y.Z`; workflow manual con aprobación; backups/rollback/recuperación del admin; ensayo de arranque limpio.

**Decisiones propuestas, no aprobadas por la issue:** guardar solo `.env.prod.example` en Git y generar `.env.prod` real fuera de Git; overlay dedicado a prod; script `preflight` que falle en forma cerrada; publicar por HTTPS en un edge definido; GitHub Environment `production` con aprobación manual. Confirmar responsables y arquitectura antes de codificar.

**Fuera de alcance de este plan:** contratar/configurar el servidor final, resolver toda la promoción `develop → main` de cada micro, cambiar contratos funcionales o cargar datos reales, cerrar los issues de los demás repos sin evidencia propia, ejecutar un deploy productivo.

## 2. Estado actual verificado y puntos de intervención

| Área | Estado / riesgo | Archivos a revisar o cambiar |
|---|---|---|
| Compose dev | `.env.example` + base + micros generados; varias variables tienen defaults de dev. Users/gateway sin perfil explícito. | `.env.example`, `docker-compose.yml`, `registry/generated/micros.yml`, `config/users-service.env` |
| Servidor/tailnet | `.env.server.example` y overlays de mesh/Vault/notificaciones/storage todavía son similares a dev; **no existe** plantilla/overlay/runbook de prod. | `.env.server.example`, nuevos `.env.prod.example` y `docker-compose.prod.yml` (nombres propuestos) |
| Secretos/perfiles | Base permite `JWT_ACTIVE_KID:-dev`, email admin de fallback, Kafka tailnet fallback, `GF_SECURITY_ADMIN_PASSWORD:-admin`; `config/users-service.env` define `COOKIE_SECURE=false`; `team/` y micros remotos generados usan `${SPRING_PROFILES_ACTIVE:-prod}`. | `docker-compose.yml`, `config/users-service.env`, `team/`, `registry/generated/micros.yml` |
| Notificaciones/storage | Overlay de notificaciones fija perfil `kafka`, depende de Mailpit; storage vuelve a añadir Mailpit `:8025`. | `docker-compose.notifications.yml`, `docker-compose.storage.yml` |
| Edge/URLs | Nginx tiene host S3 tailnet en dos lugares y cookie de variante sin `Secure`; URLs prefirmadas S3 pueden romperse si se cambia host/protocolo tras firmar. Grafana necesita `GF_SERVER_ROOT_URL` HTTPS externo. | `nginx/default.conf.template`, configuración Grafana en Compose |
| Identity/Vault | Vault Agent de users y healthcheck de Vault intervienen en el arranque; el seed actual usa `jwks/dev.pem` y KID `dev`. Hay procedimiento escalonado de rotación JWT. La clave de unseal hoy queda en el mismo servidor. | `vault/agent/users.hcl`, `docker-compose.vault.yml`, `scripts/vault-seed-identity.sh`, `docs/vault-jwt-rotation.md` |
| Validación/despliegue | `scripts/ci-verify.sh` valida combinaciones dev/server, no una variante prod. No hay deploy manual aprobado, backup/restore prod ni runbook de rollback. | `scripts/ci-verify.sh`, nuevos workflow y runbooks en `docs/` |

**Cuidado:** no cambiar el default compartido a `prod` o `dev` sin auditar `team/` y micros generados: la meta es que **prod** falle en cerrado sin romper los flujos actuales de desarrollo. `.gitignore` ignora `.env.*` salvo ejemplos; comprobar que `.env.prod` real no se versiona.

## 3. Plan por fases (orden recomendado)

### Fase 0 — Contratos, responsables y decisiones bloqueantes

- [ ] Compose/operaciones designa responsable de integración de #232 y checklist de evidencias; cada equipo micro conserva sus issues enlazadas. **No confundir asignación del paraguas con propiedad de los cambios de Accounting**: [Accounting #252](https://github.com/2026-P4-BE/tpi-accounting/issues/252) figura cerrado, pero eso no valida el stack.
- [ ] Acordar dominio, exposición pública vs tailnet, terminación TLS, certificados/renovación, host externo de S3 y URLs de Kafka. Definir si el ensayo usa DNS/cert de prueba y cómo se emula el edge.
- [ ] Obtener SMTP real (host, puerto, TLS, remitente, credenciales), dominio(s) de registro institucional, email de bootstrap admin y custodio de contraseña/recuperación.
- [ ] Definir custodios separados para token de GitHub Actions, Vault init/unseal/backup, contraseñas Grafana/admin y secretos S3; no escribir valores reales en Git, Obsidian ni logs.
- [ ] Acordar promoción de imágenes por servicio: `main`, tag semántico `:X.Y.Z` (o digest además del tag), repositorio FE `2026-P4-FE`, release candidate coherente. Detectar divergencias `develop/main` antes de ensayar; `tpi-theoristcal-challenge` requiere atención especial porque `main` va más adelante.
- [ ] Registrar decisiones y owner en el issue antes de implementar; no bloquear preparación local por la ausencia del servidor final.

### Fase 1 — Configuración prod separada y preflight fail-closed

- [ ] Crear `.env.prod.example` **sin secretos** con `COMPOSE_PROJECT_NAME`, `SPRING_PROFILES_ACTIVE=prod`, dominio/puertos, URLs externas HTTPS, tags/digests, referencias Vault, identidad, SMTP, S3 y Grafana. Generar `.env.prod` real por canal seguro; verificar que Git lo ignora.
- [ ] Crear `docker-compose.prod.yml` mínimo y explícito sobre `docker-compose.yml` + overlays necesarios. Evitar heredar Mailpit/seeds/dev hosts por accidente; documentar **orden exacto** de `-f` y `--env-file` en `docs/prod-deploy.md`. No reutilizar `.env.server.example` como sinónimo de prod.
- [ ] Añadir `scripts/prod-preflight.sh` (nombre propuesto) que exija variables obligatorias no vacías; rechace `localhost`/tailnet hardcodeado cuando corresponda, `JWT_ACTIVE_KID=dev`, `admin/admin`, gmail en `REGISTRATION_ALLOWED_DOMAINS`, imagen `:latest`, FE personal, `COOKIE_SECURE!=true`, `OPENAPI_ENABLED!=false`, perfil distinto de `prod` y SMTP de Mailpit. La excepción de ensayos locales debe ser **explícita y acotada**, no un fallback silencioso.
- [ ] Dar `SPRING_PROFILES_ACTIVE=prod` explícito a users y api-gateway y sobreescribir `config/users-service.env` con `COOKIE_SECURE=true` en prod. Auditar todos los servicios del stack, incluidos `team/` y `registry/generated/micros.yml`: el default `${SPRING_PROFILES_ACTIVE:-prod}` no sustituye una verificación de variables.
- [ ] Ampliar `scripts/ci-verify.sh` con `docker compose --env-file .env.prod -f docker-compose.yml -f ... -f docker-compose.prod.yml config` sobre **fixtures falsas** y pruebas negativas de preflight. Mantener intactos los casos dev/server.

**Salida de fase:** un config renderizado reproducible y tests que demuestran tanto un caso válido como fallos ante cada secreto/variable crítica omitida o insegura.

### Fase 2 — TLS, identidad, Vault y almacenamiento

- [ ] Configurar TLS en el edge decidido y redirección HTTP→HTTPS; `COOKIE_SECURE=true` para users **y** cookie de variante de `nginx/default.conf.template`. Revisar `SameSite`, dominios y `X-Forwarded-*`; probar login y renovación de sesión por HTTPS.
- [ ] Parametrizar las dos referencias al S3 tailnet en `nginx/default.conf.template`, el advertised listener Kafka y `GF_SERVER_ROOT_URL` con la URL pública HTTPS. **Prueba obligatoria:** firmar y consumir un URL S3 desde cliente externo; la firma SigV4 incluye host/ruta y puede invalidarse si el proxy reescribe el host después de firmar.
- [ ] Separar `REGISTRATION_ALLOWED_DOMAINS` (sin `gmail.com`), `ADMIN_BOOTSTRAP_EMAIL` institucional y `OPENAPI_ENABLED=false` para users/gateway. Garantizar un solo ADMIN, contraseña inicial forzada a cambio y procedimiento break-glass auditado.
- [ ] Desacoplar `scripts/vault-seed-identity.sh` de `jwks/dev.pem`/KID `dev`; cargar material real mediante Vault y seguir la secuencia de `docs/vault-jwt-rotation.md`: publicar JWKS, validar consumidores y **luego** activar el KID. Revisar `vault/agent/users.hcl` y healthcheck en `docker-compose.vault.yml` para el arranque prod. Nunca cambiar solo el KID.
- [ ] Mover contraseña de Grafana a Vault sin fallback `admin`; restringir permisos de Vault y planificar backup off-host/unseal fuera del host. No pegar secretos en fixtures, logs, capturas o esta nota.

**Salida de fase:** HTTPS y cookies seguros, OpenAPI cerrado, JWT verificable extremo a extremo, presigned S3 funcional y sin credenciales dev.

### Fase 3 — Dependencias e imágenes productivas

- [ ] En `docker-compose.notifications.yml`, eliminar dependencia/host Mailpit en prod y sustituir perfil `kafka` hardcodeado por `prod` donde corresponda; integrar SMTP real por secretos. En `docker-compose.storage.yml`, no publicar ni iniciar Mailpit `:8025` en prod. `docker compose config --services` y `ps` deben demostrar ausencia total.
- [ ] Fijar versiones de **todos** los servicios y FE con tags de release `:X.Y.Z` de `main`; no `:latest`, ramas o imagen FE personal. Registrar matriz servicio→tag/digest→commit/PR.
- [ ] Coordinar issues por micro: [Gateway #61](https://github.com/2026-P4-BE/tpi-api-gateway/issues/61), [Users #161](https://github.com/2026-P4-BE/tpi-users/issues/161), [Notifications #185](https://github.com/2026-P4-BE/tpi-notifications/issues/185) y el resto enlazado en #232. Confirmar en cada imagen que perfil `prod` implica **cero mocks, cero seeds demo, ninguna referencia a localhost**, y que omitir una variable obligatoria causa fallo de arranque.

**Salida de fase:** matriz de versiones reproducible y stack renderizado sin Mailpit ni imágenes mutables.

### Fase 4 — Operación previa al primer deploy

- [ ] Crear workflow `.github/workflows/deploy-prod.yml` (nombre propuesto), solo `workflow_dispatch`, GitHub Environment `production` con required reviewers, sin disparador automático. Validar preflight, aprobación, digest/versión, backup previo, despliegue y smoke tests; el workflow puede permanecer sin credenciales/servidor hasta que existan.
- [ ] Escribir `docs/prod-deploy.md` con preparación de entorno, orden Compose, generación de secretos, TLS/DNS, preflight, comandos de deploy, post-checks y recolección de evidencias. No incluir `.env.prod` real ni contraseñas.
- [ ] Escribir `docs/prod-backup-restore.md`: bases de datos de **todos** los micros, Garage/S3 y Vault, frecuencia/retención/ubicación off-host/cifrado, dueño y prueba periódica de restauración. Nunca usar `docker compose down -v` para rollback o mantenimiento.
- [ ] Escribir `docs/prod-rollback.md`: conservar el release anterior y volver a tags/digests previos tras backup; **no revertir a ciegas una migración de esquema**. Si hay incompatibilidad de DB, activar plan específico de restore y ventana de mantenimiento.
- [ ] Documentar recuperación del ADMIN único: verificación de identidad, acceso break-glass autorizado, rotación/reset por mecanismo de users, auditoría, revocación de credenciales temporales y prueba en ensayo. El custodio del secreto inicial debe estar designado.

**Salida de fase:** runbooks revisados, workflow validado sin deploy real y restauración/rollback ejecutables por una persona distinta a quien los escribió.

### Fase 5 — Ensayo general con volúmenes vacíos

- [ ] Cortar release candidate coherente desde `main`; guardar tags, digests y commits. Levantar stack completo con `SPRING_PROFILES_ACTIVE=prod`, `.env.prod` temporal seguro y volúmenes **nuevos** en laptop/VM temporal; nunca reutilizar/borrar volúmenes dev o reales.
- [ ] Verificar en DB/servicios: **exactamente 1 ADMIN, 0 cursos, 0 cohortes, 0 desafíos**; login obliga cambio de contraseña; FE sin demos; `flyway_schema_history` sin migraciones/seeds exclusivamente de dev. Dejar consultas/evidencia por servicio, no solo una captura del FE.
- [ ] Probar que falta de variable obligatoria bloquea arranque; HTTPS y cookies `Secure`; OpenAPI deshabilitado users/gateway; Mailpit no existe; SMTP real prueba entrega controlada; JWT KID no `dev` y validación completa; URL S3 firmada funciona fuera del host; Kafka usa endpoint anunciado correcto.
- [ ] Ejecutar backup→restore en instancia aislada y rollback de imagen a versión anterior compatible, medir tiempo y documentar resultado. Ensayar recuperación del admin bloqueado. Revisar logs para que no filtren secretos.
- [ ] Anexar al issue #232 evidencia de `docker compose config`, tests/preflight, matriz de imágenes, checks de datos, smoke tests y ensayo de recuperación. Cerrar el paraguas solo cuando los checks de cada micro queden corroborados; issue cerrado no equivale a prueba integrada.

## 4. Dependencias, criterios de aceptación y riesgos

**Ruta crítica:** decisiones de Fase 0 → overlay/preflight Fase 1 → TLS/Vault/SMTP e imágenes Fases 2–3 (en paralelo tras Fase 1) → runbooks/workflow Fase 4 → ensayo Fase 5. Sin dominio/certificados/SMTP/identidad de admin se puede avanzar en plantilla, tests y workflow, pero no declarar listo el ensayo extremo a extremo.

**Aceptación mínima para #232:** configuración prod reproducible y sin fallbacks dev; tags fijados desde `main`; separación dev intacta; aprobación manual; documentación de backup/restore/rollback/admin; ensayo con volúmenes vacíos y resultados exactos indicados; pruebas negativas; HTTPS, Vault/JWT, S3 y notificaciones verificadas. La aprobación de producción real es **posterior** y separada.

**Riesgos / mitigaciones:** release inicial grande por divergencia `develop/main` → RC y smoke por micro; `main` de theoretical challenge más avanzado → comparación explícita antes de tag; SigV4 roto por rewrite de host → test externo antes de release; JWT inválido por rotación fuera de orden → seguir runbook existente; secreto unseal en mismo host → custodia/backup off-host; rollback con migraciones incompatibles → backup y plan de compatibilidad; `prod` de remote micros como default → pruebas de overlay sin alterar dev/team.

## 5. Próximo paso concreto

Abrir subtareas de implementación de Fases 0–1 para Compose, asignar responsables y dejar en #232 decisiones pendientes. **No editar configuración productiva ni crear credenciales** hasta cerrar el contrato de edge, identidad y secretos. Referencias de seguimiento: [#232](https://github.com/2026-P4-BE/tpi-system-compose/issues/232) y `Backend/tpi-system-compose/docs/vault-jwt-rotation.md` (runbook del checkout).
