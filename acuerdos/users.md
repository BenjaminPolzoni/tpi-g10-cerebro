---
tags: [tpi, g10, acuerdo, users, identidad, ranking]
fecha: 2026-09-26
grupos: [G10, G07]  # Users = Tema 01; G07 según las correcciones de los profes y Taiga ("[G07] - Users-service")
estado: vigente
contrato: "tpi-roadmap/docs/contracts/reporte-users-contratos-y-endpoints.md"
---

# Acuerdo con Users (Tema 01, G07): perfiles para el ranking, roles y tokens de servicio

> [!info] Fuentes
> - `tpi-roadmap/docs/contracts/reporte-users-contratos-y-endpoints.md` ([GitHub](https://github.com/2026-P4-BE/tpi-roadmap/blob/develop/docs/contracts/reporte-users-contratos-y-endpoints.md)): reporte de contratos de `users-service` (fuente `tpi-users` @ `9f2f976`, 2026-09-23; `ProfileResponse` actualizado contra `develop` `753e5a5`, 2026-10-10).
> - `tpi-roadmap/docs/T-01-7-EUREKA-GATEWAY.md` (emisión del token técnico) y `docs/P-11-5-issues.md` (alta de scopes en el catálogo).
> - Repo de la contraparte: `2026-P4-BE/tpi-users` (issue #89 `ScopeCatalog`).
> - Es un **reporte** (descripción del servicio), no un acta firmada con Users.

## Qué se acordó
- **Users es el dueño de la identidad:** registro, credenciales, 2FA, sesiones, roles, whitelist y emisión de tokens (persona y servicio). No publica puertos: todo entra por el Gateway. No valida el JWT: confía en los headers `X-*` del Gateway.
- Roadmap lee **perfiles de alumnos de a uno** (`GET /api/users/profile/{id}`) para mostrarlos al **profesor** en el ranking (HU-24, T-24.3). Users no tiene lote por ids.
- El **legajo es opcional**: solo se obtiene con el scope `users.legajo.read`. Si Users rechaza el token con ese scope (`400`), Roadmap pide otro solo con `users.profile.read` y muestra el perfil sin legajo.
- Si Users no responde (o el perfil está incompleto), la fila sale con **seudónimo** y el ranking se completa igual; el fallo queda recordado `failure-ttl` 30 s. Un perfil que no cumple el contrato deja sin perfil solo a ese alumno (`1a6ff15`).
- Roadmap obtiene su **token técnico** (`client_credentials`) de Users por Gateway. El alta del cliente `roadmap-service` y de cada scope en el catálogo la hace Identity/Users de forma manual; el secret va por Vault, nunca por chat.

## Quién lo acordó
- G10: equipo Roadmap.
- Otro grupo: equipo Users/Identity (Tema 01), G07. Los scopes se tramitan con issues de onboarding en `tpi-users` y `tpi-system-compose` (`registry/services.yml`).

## Contrato técnico

### Perfil (Roadmap → Users)
| Método y ruta | Auth | Respuesta |
|---|---|---|
| `GET /api/users/profile/{id}` | token de servicio, audience `users-service`, scope `users.profile.read` (+ `users.legajo.read` opcional) | `ProfileResponse`: `id`, `first_names`, `last_names`, `github_username`, `avatar_ref`, `avatar_url` (URL firmada, vale 1 h); `legajo` solo para ADMIN o servicio con `users.legajo.read`; `email` y `account_status` solo ADMIN |

Roadmap mapea a `UserProfile(id, firstNames, lastNames, fileNumber, avatarUrl)`. Caché: perfiles 30 min, desconocidos 5 min, máx 5000; presupuesto de carga 5 s por consulta (el resto sale con seudónimo y se completa después).

### Token técnico (Roadmap → Users vía Gateway)
```http
POST /api/users/public/auth/token
{ "client_id", "client_secret", "grant_type": "client_credentials", "scope", "audience" }
```
- Respuesta: `{ access_token, token_type: "Bearer", expires_in }` (TTL 5 min). Claims del token: `sub`, `roles:["MS"]`, `type:service`, `aud` (obligatoria), `scope`.
- Un scope fuera del catálogo `users.scopes.catalog` da `400 validation`; una audience de otro destino da `403 invalid-audience`.
- Roadmap cachea por `(audience, scope)` y no decodifica el JWT (`HttpTechnicalTokenProvider`). Credenciales por variables de entorno (`ROADMAP_TECHNICAL_CLIENT_ID`/`_SECRET`).

### Identidad y roles (lo que nos llega)
- Persona: `X-Principal-Type: user`, `X-User-Id`, `X-User-Roles`. Roles en uso: `ADMIN`, `GESTOR`, `PROFESSOR`, `STUDENT`. Servicio: `X-Principal-Type: service`, `X-Service-Id`, `X-Service-Scopes` (`MS` + scopes).
- Las personas viajan en la cookie `fu_at` (HttpOnly), **nunca** en `Authorization`; los servicios en `Authorization: Bearer`.
- Errores en `application/problem+json` (RFC 9457) con `type` propio; el Gateway puede agregar `invalid-audience`, `service-unavailable`, etc.
- Gates de cuenta de Users (solo `user`): cuenta activa, cambio de contraseña, onboarding.

### Permisos (Tema 01, [tpi-roadmap#294](https://github.com/2026-P4-BE/tpi-roadmap/pull/294))
Catálogo que trae la PR de adopción de Tema 01 (Ramiro Ibazeta), todavía en draft. Formato `segmento.entidad.acción`, con el `authz-starter` de Users:

- `roadmap.graph.read` / `roadmap.graph.write`, `roadmap.badge.read` / `roadmap.badge.write`, `roadmap.progress.read`, `roadmap.ranking.read`, `roadmap.challenge.read`.
- No viajan en headers: el starter los resuelve contra Users (grant `users.authz.read`) y el catálogo se declara en Compose.
- Con `AUTHZ_MODE=off` (default), cada `@RequirePermission` deja pasar por sus `legacyRoles`: hoy no cambia nada.
- El gate exige `roadmap.gate.read` (resuelve la T-22.4).
- La matriz endpoint por endpoint está en [[arquitectura/T-22-1-matriz-permisos]].

### Eventos
Users publica `user-events` (`STUDENT-REGISTERED`, `ACCOUNT-DEACTIVATED`) y `notification-events`. **Roadmap no los consume.** El reporte los lista con nombres en mayúsculas con guion (contrato v3 anterior).

## Impacto en nuestro código
- `clients/users/*`: `HttpUserProfilesClient`, `UserProfilesClient`, `UserProfile`, `UserProfilesProperties`, `UserProfilesConfig`, `UserProfilesUnavailableException`.
- `services/RankingService` y `dtos/RankingDtos.RankingRowProfile` (`first_names`, `last_names`, `file_number`, `avatar_url`). Ver [[decisiones/DEC-007-anonimato-ranking-en-servidor|DEC-007]].
- `clients/auth/*` (`HttpTechnicalTokenProvider`, `TechnicalTokenTarget`, `TechnicalTokenProperties`).
- `common/security/GatewayHeadersFilter`, `Roles` (`GESTOR`, `ADMIN`, `PROFESSOR`, `STUDENT`; ver [[decisiones/DEC-009-gestores-editan-roadmaps|DEC-009]]), `StudentViewer`.
- `tpi-integration.yml`: `needs` incluye `users.profile.read` y `users.legajo.read`.

## Pendiente / próximos pasos
- [ ] Confirmar con Users que el cliente `roadmap-service` tiene dados de alta `users.profile.read@users-service` y `users.legajo.read@users-service` en el entorno de la demo.
- [ ] Verificar que el vocabulario de roles que emite Users (`GESTOR`, `PROFESSOR`) coincide con el que Courses documenta (`MANAGER`, `PROFESSOR_READ_ONLY`, "GESTOR o PROFESOR").
- [ ] Rol de profesor ayudante (`PROFESSOR_READ_ONLY` de Courses): pendiente #8 de Users, sin definir.
- [ ] Un lote de perfiles por ids evitaría N llamadas (hoy una por alumno con presupuesto de 5 s). Solicitud no registrada.
- [x] **T-22.2, [tpi-users#215](https://github.com/2026-P4-BE/tpi-users/issues/215), respondida y cerrada el 2026-10-25** por Ramiro Ibazeta:
    1. **Sí**, el Gateway sigue mandando `X-User-Roles` con `AUTHZ_MODE=on`: esa propiedad no existe en el Gateway, es del `authz-starter` (decide cómo el micro evalúa `@RequirePermission`), y el starter lee el header igual. Los `@PreAuthorize("hasRole(...)")` de autoservicio del alumno (materiales, lectura, nivel, salud, inventario, marcar leído, avatar/mascota) siguen funcionando sin cambios; no hace falta inventar `roadmap.learning.*`/`roadmap.avatar.*`.
    2. El catálogo de Compose **no asigna roles a permisos** (solo `code`/`label`/`description`/`scope`/`service`); eso es un "pack" (tarea P2 de Users, todavía sin implementar). Los 7 `roadmap.*` están declarados (`scope: organization`, `service: roadmap-service`) en la rama `feature/integration-compose-on-develop` de `tpi-system-compose`, **sin PR todavía**. **Mientras no haya packs**, la paridad de GESTOR (`badge.write`/`progress.read`) se logra agregándolo a los `legacyRoles` de esos `@RequirePermission` en nuestro propio código — sin depender de Compose. Para poder prender `authz.mode=on` en algún momento, los 7 `roadmap.*` van a tener que estar mergeados en el catálogo (`permissions.json`) antes.
- [ ] **Bug encontrado en la #294 (2026-10-25):** `authz-starter-0.1.0.pom` y `maven-metadata.xml`, vendoreados en `.mvn/tpi-libs`, están commiteados en LF sin `.gitattributes` que los proteja; con `core.autocrlf=true` (default de Git en Windows) el checkout los pasa a CRLF y el `checksumPolicy=fail` del repo rechaza la resolución. Bloquea compilar la rama en Windows. Reportado en el [comentario](https://github.com/2026-P4-BE/tpi-roadmap/pull/294#issuecomment-6398768912) de la PR, con la causa confirmada y el arreglo sugerido (`.mvn/tpi-libs/** -text`).

> [!warning] Riesgos
> - Sin `users.legajo.read` el profesor ve el ranking sin legajo hasta que vence la caché (30 min).
> - Con Users caído, el profesor ve seudónimos; el alumno nunca ve perfiles ajenos (ver DEC-007).
> - El reporte de Users es una foto del 2026-09-23/10-10: puede quedar desactualizado.
> - **Secret desactualizado:** si el secret de `roadmap-service` está viejo, Users responde `401` al pedir el token técnico, y todo lo que valida dueño en Courses da `503`. Desde T-45.7 ese `503` lleva el código `courses.ownership-token-unavailable`, no «Courses no responde». Pasó en la variante el 2026-10-15. Ver [[decisiones/DEC-019-ranking-estado-de-datos-y-cache-de-respaldo|DEC-019]].

## Historial
- 2026-10-25: Users respondió y cerró [tpi-users#215](https://github.com/2026-P4-BE/tpi-users/issues/215) (T-22.2): el Gateway sigue mandando `X-User-Roles` con `AUTHZ_MODE=on`; el catálogo de Compose no asigna roles (eso es un pack, P2 de Users, sin implementar), así que la paridad de GESTOR en insignias/progreso se resuelve en T-22.3 agregándolo a los `legacyRoles` propios, no esperando a Compose. Los 7 `roadmap.*` siguen sin PR en `tpi-system-compose` (bloquea prender `authz.mode=on`, no bloquea T-22.3).
- 2026-10-23: la #294 define el catálogo de 7 permisos `roadmap.*` y el scope del gate; se adopta para la matriz (T-22.1) y se preguntan las dos dudas de la T-22.2.
- 2026-10-25: Users vendoreó `authz-starter 0.1.0` en la #294 (antes solo compilaba en estático); encontramos que no compila en Windows por un `.gitattributes` faltante (CRLF corrompe los checksums del `.pom`/`maven-metadata.xml` vendoreados) y lo reportamos. Las dos dudas de T-22.2 se abrieron como [tpi-users#215](https://github.com/2026-P4-BE/tpi-users/issues/215), pidiendo además que GESTOR tenga `badge.write`/`progress.read`.
- 2026-09-26: reporte de contratos de Users incorporado (`reporte-users-contratos-y-endpoints.md`); token técnico (T-01.7).
- 2026-10-10: ranking con perfil de Users (T-24.3) y presupuesto de carga; ranking sigue completo si Users falla.
- 2026-10-15: secret de servicio desactualizado reproducido en la variante (`401` en el token técnico). La falla del token tiene código de error propio (T-45.7, [[decisiones/DEC-019-ranking-estado-de-datos-y-cache-de-respaldo|DEC-019]]).
- 2026-10-11: un perfil incompleto solo deja sin perfil a ese alumno (`1a6ff15`).
- 2026-10-14: nota creada desde `origin/develop` (`57ff06a`).
- 2026-10-15: respuestas en [[sprints/sprint-3/08-dudas|08-dudas]]: el catálogo de permisos es de Users y todavía no está definido (G2); no habrá roles sino permisos, y mientras tanto vale `PROFESSOR`/`GESTOR` (G6); todavía no hay usuarios demo (G7); Users también lleva el Gateway (G11).
