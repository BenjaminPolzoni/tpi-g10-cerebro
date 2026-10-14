---
tags: [tpi, g10, acuerdo, users, identidad, ranking]
fecha: 2026-09-26
grupos: [G10, Gxx]  # Users = Tema 01 (Identidad y Usuarios); número de grupo no aparece en los docs (verificar)
estado: vigente
contrato: "tpi-roadmap/docs/contracts/reporte-users-contratos-y-endpoints.md"
---

# Acuerdo con Users (Tema 01, Gxx verificar): perfiles para el ranking, roles y tokens de servicio

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
- Otro grupo: equipo Users/Identity (Tema 01), Gxx (verificar). Los scopes se tramitan con issues de onboarding en `tpi-users` y `tpi-system-compose` (`registry/services.yml`).

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

> [!warning] Riesgos
> - Sin `users.legajo.read` el profesor ve el ranking sin legajo hasta que vence la caché (30 min).
> - Con Users caído, el profesor ve seudónimos; el alumno nunca ve perfiles ajenos (ver DEC-007).
> - El reporte de Users es una foto del 2026-09-23/10-10: puede quedar desactualizado.

## Historial
- 2026-09-26: reporte de contratos de Users incorporado (`reporte-users-contratos-y-endpoints.md`); token técnico (T-01.7).
- 2026-10-10: ranking con perfil de Users (T-24.3) y presupuesto de carga; ranking sigue completo si Users falla.
- 2026-10-11: un perfil incompleto solo deja sin perfil a ese alumno (`1a6ff15`).
- 2026-10-14: nota creada desde `origin/develop` (`57ff06a`).
