# users-service · Contratos y Endpoints

**Servicio:** `users-service` (Tema 01 — Identidad y Usuarios, TPI Programación IV)
**Repo:** `tpi-users` @ `9f2f976` (2026-09-23)
**Fecha del reporte:** 2026-09-24
**Fuente:** código en `tpi-users/src/main/java`, `application.properties`, `docs/KAFKA-EVENT-CONTRACTS.md` y contrato del gateway (`tpi-api-gateway`).

---

## 1. Resumen

`users-service` es el dueño de la identidad de la plataforma: registro, credenciales, 2FA, sesiones, roles, whitelist y emisión de tokens (persona y servicio).

- **No publica puertos.** Todo entra por el API Gateway (`:8080` vía nginx `:3000`).
- **No valida el JWT.** Confía en los headers `X-*` que inyecta el gateway.
- **Prefijo público (anónimo):** `/api/users/public/**`
- **Prefijo privado (requiere token):** `/api/users/**`
- **JWKS (sin prefijo, RFC 8615):** `/.well-known/jwks.json`
- **Todos los errores son** `application/problem+json` (RFC 9457) y se distinguen por `type`.

El locator del gateway rutea `/api/{servicio}/**` y **no reescribe el path**: el servicio recibe la URL completa.

---

## 2. Contratos transversales

### 2.1 Headers de identidad (entrada, inyectados por el gateway)

| Header | Token de persona | Token de servicio |
|---|---|---|
| `X-Principal-Type` | `user` | `service` |
| `X-User-Id` | UUID (`sub`) | — |
| `X-User-Roles` | roles separados por coma | — |
| `X-Service-Id` | — | client id (`sub`) |
| `X-Service-Scopes` | — | `MS`, luego scopes por coma |
| `X-Request-Id` | id de correlación (también se devuelve en el body de error como `requestId`) | igual |

- Formato: coma, sin espacios, sin duplicados. Roles en uso: `ADMIN`, `GESTOR`, `PROFESSOR`, `STUDENT` (+ `MS` solo en tokens de servicio).
- El gateway **borra estos headers en toda request (incluidas las públicas)** y recién después inyecta los suyos. Una request sin `X-Principal-Type` es anónima.
- `hasRole('X')` matchea `ROLE_X`: el prefijo lo agrega `GatewayIdentityFilter` al construir las authorities; los scopes van como authority plana (`hasAuthority('users.profile.read')`).

### 2.2 Cookies de sesión

| Cookie | Contenido | Path | TTL | Atributos |
|---|---|---|---|---|
| `fu_at` | access token JWT | `/` | 10 min (`users.jwt.access-ttl=PT10M`) | `HttpOnly`, `SameSite=Strict`, `Secure` según config |
| `fu_rt` | `jti` del refresh token | `/api/users/` | 7 días (`users.jwt.refresh-ttl=P7D`) | `HttpOnly`, `SameSite=Strict`, `Secure` según config |

- `users.cookie.secure=true` por defecto; el compose del proyecto lo baja a `false` porque no termina TLS.
- Las personas viajan en la cookie `fu_at`, **nunca** en `Authorization` (el gateway rechaza un token de persona por Bearer). Los servicios viajan en `Authorization: Bearer`.
- Logout y cambio de contraseña borran ambas cookies (`Max-Age=0`).

### 2.3 JWT emitidos

**Token de persona** (`/auth/2fa/verify`, `/auth/refresh`):

| Claim | Valor |
|---|---|
| `iss` | `users-service` |
| `sub` | UUID del usuario |
| `roles` | `["ADMIN"]` etc. |
| `type` | `user` |
| `jti` | UUID |
| `sid` | id de sesión (single session) |
| `est` | estado de cuenta (`ACTIVE`, `PENDING_EMAIL`, …) |
| `pwd` | booleano, cambio de contraseña pendiente |
| `onb` | booleano, onboarding pendiente |
| `iat` / `exp` | 10 minutos |

**Token de servicio** (`POST /auth/token`, `client_credentials`):

| Claim | Valor |
|---|---|
| `sub` | client id |
| `roles` | `["MS"]` |
| `type` | `service` |
| `aud` | servicio destino (obligatorio, sin default) |
| `scope` | scopes separados por espacio |
| `exp` | 5 minutos (`users.jwt.service-ttl=PT5M`) |

Catálogo de scopes emisibles (config `users.scopes.catalog`, default): `users.profile.read:users-service`, `market.catalog.read:market-service`. Un scope o audiencia fuera del catálogo → `400 validation`.

### 2.4 Contrato de errores (RFC 9457 / problem+json)

Campos: `type` (identidad del error, es lo que el cliente debe ramificar), `title`, `status`, `detail`, `instance`, y opcionalmente:
- `request_id` si vino `X-Request-Id`
- `retry_after_seconds` en `429` (junto con header `Retry-After`)
- `account_status` en `pending-account`

Tipos propios del servicio (todos bajo `https://tpi.utn.frc/errors/`):

| `type` | HTTP | Cuándo |
|---|---|---|
| `validation` | 400 | Body/parámetro inválido (Bean Validation, tipo, JSON ilegible) |
| `invalid-code` | 400 | Código 2FA incorrecto o expirado |
| `invalid-link` | 400 | Link de activación/reset expirado, usado o inexistente |
| `invalid-link-state` | 400 | State OAuth ausente, vencido, consumido o corrupto |
| `provider-not-supported` | 400 | Proveedor git desconocido |
| `invalid-credentials` | 401 | Login o reautenticación fallida |
| `not-authenticated` | 401 | Sin identidad válida (mismo tipo que usa el gateway) |
| `session-closed` | 401 | Sesión cerrada: logout, cambio de password, reuse, cookie ausente |
| `session-superseded` | 401 | Login más nuevo en otro dispositivo |
| `pending-account` | 403 | Cuenta no `ACTIVE` (+ `account_status`) |
| `password-change-required` | 403 | `must_change_password=true` |
| `onboarding-pending` | 403 | `first_login=true` |
| `email-not-whitelisted` | 403 | Email fuera de dominio permitido / sin autorización |
| `access-denied` | 403 | Rol insuficiente o GESTOR excediendo su alcance |
| `route-not-found` | 404 / 405 | Ruta inexistente / método no soportado |
| `provider-not-linked` | 404 | No hay link activo con ese proveedor |
| `last-admin` | 409 | La operación dejaría la plataforma sin ADMIN activo |
| `invalid-transition` | 409 | Transición de estado no permitida |
| `duplicate-email` | 409 | Email duplicado / ya autorizado |
| `link-user-mismatch` | 409 | El state OAuth pertenece a otra sesión (nunca 401) |
| `provider-already-linked` | 409 | El usuario ya tiene ese proveedor vinculado |
| `provider-account-taken` | 409 | La cuenta del proveedor ya está vinculada a otro usuario |
| `too-many-attempts` | 429 | Límite de intentos excedido (+ `Retry-After`) |
| `provider-unavailable` | 502 | El proveedor git no respondió |

Tipos que puede agregar el **gateway** antes de llegar al servicio: `invalid-audience` (403), `method-not-allowed` (405), `unexpected-error` (500), `service-unavailable` (503, con `Retry-After`).

### 2.5 Gates de cuenta (solo principal `user`)

Un interceptor aplica tres gates en orden sobre `/api/users/**` (los tokens de servicio no pasan por gates):

1. **ACCOUNT_STATUS** → cuenta distinta de `ACTIVE` ⇒ `403 pending-account`
2. **PASSWORD** → `must_change_password` ⇒ `403 password-change-required`
3. **ONBOARDING** → `first_login` ⇒ `403 onboarding-pending`

Endpoints exentos (la salida del gate nunca queda bloqueada por el gate):

| Endpoint | Exento de |
|---|---|
| `GET /me` | los 3 |
| `POST /auth/logout` | los 3 |
| `PATCH /me/onboarding` | PASSWORD + ONBOARDING |
| `POST /auth/password/change` | PASSWORD + ONBOARDING |
| `POST /me/git-links/{provider}/start` | PASSWORD + ONBOARDING |
| `POST /me/git-links/{provider}/callback` | PASSWORD + ONBOARDING |

---

## 3. Endpoints

Leyenda de la columna **Auth**:
`anónimo` = sin token · `persona` = token de persona (cualquier rol) · `ROLE` = rol requerido · `servicio@scope` = token de servicio con scope.
**Gates:** `n/a` público · `todos` los tres gates · `exento 3` / `exento PW+ONB`.

### 3.1 Autenticación pública — `/api/users/public/auth`

| Método y ruta | Auth | Body | Respuesta 200 | Errores propios |
|---|---|---|---|---|
| `POST /auth/login` | anónimo | `LoginRequest` | `LoginResponse` — **no emite tokens** | 401 `invalid-credentials`; 429 `too-many-attempts` |
| `POST /auth/2fa/verify` | anónimo | `VerifyTwoFactorRequest` | `SessionResponse` + `Set-Cookie fu_at`/`fu_rt` | 400 `invalid-code`/`validation`; 429 |
| `POST /auth/refresh` | anónimo (cookie `fu_rt`) | — | `SessionResponse` + rota cookies | 400 `validation` (cookie no UUID); 401 `session-closed`/`session-superseded` |
| `POST /auth/password/reset` | anónimo | `ResetRequest` | `{ "message": "..." }` — respuesta constante | 429 |
| `POST /auth/password/reset/confirm` | anónimo | `ResetConfirmRequest` | vacío | 400 `invalid-link`/`validation` |
| `POST /auth/token` | anónimo (client credentials) | `ClientCredentialsRequest` | `{ access_token, token_type: "Bearer", expires_in }` | 400 `validation`; 401 `invalid-credentials` |

**Login en dos fases:** `login` valida credenciales y encola un código de 6 dígitos (sin mail server: el código queda en `outbox_events`); `/2fa/verify` es el único endpoint que emite el par access+refresh de una persona. El refresh **rota** el token en cada uso; reusar uno viejo revoca toda la familia y devuelve `session-closed`.

### 3.2 Sesión privada — `/api/users/auth`

| Método y ruta | Auth | Body | Respuesta | Errores | Gates |
|---|---|---|---|---|---|
| `POST /auth/logout` | persona | opcional `refreshToken` (no necesario: va en cookie) | vacío + limpia cookies | — | exento 3 |
| `POST /auth/password/change` | persona | `PasswordChangeRequest` | vacío + limpia cookies (cierra sesión) | 401 `invalid-credentials`/`not-authenticated` | exento PW+ONB |

### 3.3 Registro — `/api/users/public/registration`

| Método y ruta | Auth | Body | Respuesta 200 | Errores propios |
|---|---|---|---|---|
| `POST /registration/student` | anónimo | `StudentRegistrationRequest` | vacío (queda `PENDING_EMAIL`) | 403 `email-not-whitelisted`; 409 `duplicate-email` |
| `POST /registration/professor` | anónimo | `StaffRegistrationRequest` | vacío | 403 `email-not-whitelisted`; 409 `duplicate-email` |
| `POST /registration/gestor` | anónimo | `StaffRegistrationRequest` | vacío | 403 `email-not-whitelisted`; 409 `duplicate-email` |
| `POST /registration/activate` | anónimo | `ActivateAccountRequest` | vacío (cuenta activada) | 400 `invalid-link`/`validation` |
| `POST /registration/resend-activation` | anónimo | `ResendCodeRequest` | `{ "message": "..." }` constante | 429 |

- Student exige `invitation_code`; professor/gestor exigen email en whitelist (rol PROFESSOR/GESTOR según corresponda).
- `terms_version` debe ser la versión vigente que devuelve `/legal/terms` (hoy `v1`).
- Anti-enumeración: los tres endpoints de mail (reset, resend, activate) devuelven siempre lo mismo exista o no la cuenta.
- `activate` es **POST a propósito**: un `GET` lo consumen los escáneres de correo institucional antes que la persona.

### 3.4 Legal — `/api/users/public/legal`

| Método y ruta | Auth | Respuesta 200 |
|---|---|---|
| `GET /legal/terms` | anónimo | `{ "version": "v1", "texto": "<markdown>" }` (clave `texto` en castellano, es contenido de usuario) |

### 3.5 JWKS — raíz del servicio

| Método y ruta | Auth | Respuesta 200 |
|---|---|---|
| `GET /.well-known/jwks.json` | anónimo | Documento JWKS (RFC 7517) con las claves públicas de firma |

El gateway obtiene acá las claves para validar cada JWT. Ruta estática en el gateway, fuera de `/api`.

### 3.6 Cuenta propia y perfil — `/api/users`

| Método y ruta | Auth | Body | Respuesta 200 | Errores | Gates |
|---|---|---|---|---|---|
| `GET /me` | persona | — | `UserMeResponse` | — | exento 3 |
| `PATCH /me/onboarding` | persona | `OnboardingRequest` | vacío | 400 `validation` | exento PW+ONB |
| `GET /profile/{id}` | persona **o** servicio@`users.profile.read` | — | `ProfileResponse` | 403 `access-denied`; 404 `route-not-found` | todos |

`GET /me` es la única ruta exenta de los 3 gates para que el front pueda explicar **por qué** está bloqueada la cuenta (`account_status`, `must_change_password`, `first_login`).

### 3.7 Administración de usuarios — `/api/users`

| Método y ruta | Auth | Body | Respuesta 200 | Errores propios | Gates |
|---|---|---|---|---|---|
| `GET /` (directorio) | ADMIN, GESTOR | — | `List<UserListItemResponse>` (solo `ACTIVE`, más nuevos primero) | — | todos |
| `POST /` | ADMIN | `CreateUserRequest` | `{ "id": "<uuid>" }` (crea **solo ADMIN**) | 409 `duplicate-email` | todos |
| `DELETE /{id}` (baja lógica) | ADMIN, GESTOR | `AdminDeactivationRequest` | vacío | 400 `invalid-code`; 401 `invalid-credentials`; 403 `access-denied`; 409 `last-admin` | todos |
| `PATCH /{id}/role` | ADMIN, GESTOR | `RoleChangeRequest` | vacío | 403 `access-denied`; 409 `last-admin` | todos |

- El directorio: ADMIN ve todo; GESTOR ve solo PROFESSOR/GESTOR.
- La baja exige reautenticación completa del operador (password actual + código 2FA fresco + username escrito), cierra la sesión del objetivo y publica `ACCOUNT-DEACTIVATED`.
- GESTOR solo puede operar sobre PROFESSOR/GESTOR, nunca ADMIN ni STUDENT.
- Nada se borra físicamente (`deleted_at`); la unicidad de email considera solo filas activas.

### 3.8 Whitelist — `/api/users/whitelist`

| Método y ruta | Auth | Body | Respuesta 200 | Errores propios | Gates |
|---|---|---|---|---|---|
| `POST /whitelist` | ADMIN, GESTOR | `AddEmailRequest` | `{ "id": "<uuid>" }` | 409 `duplicate-email` | todos |
| `GET /whitelist` | ADMIN, GESTOR | — | `List<WhitelistEntryResponse>` | — | todos |
| `DELETE /whitelist/{id}` | ADMIN, GESTOR | — | vacío (no afecta cuentas ya creadas) | — | todos |
| `POST /whitelist/requests` | PROFESSOR | `CreateWhitelistRequest` | `{ "id": "<uuid>" }` | 409 `duplicate-email` (ya hay una pendiente) | todos |
| `GET /whitelist/requests` | ADMIN, GESTOR | — | `List<WhitelistRequestResponse>` (pendientes y resueltas) | — | todos |
| `PATCH /whitelist/requests/{id}` | ADMIN, GESTOR | `ResolveWhitelistRequest` | vacío | 400 `validation` (sin `rejection_reason`, ya resuelta, email ya autorizado) | todos |

`role` en `AddEmailRequest` es opcional y acepta solo `PROFESSOR` (default) o `GESTOR`; la whitelist nunca otorga ADMIN.

### 3.9 Links con proveedor git — `/api/users/me/git-links`

| Método y ruta | Auth | Body | Respuesta | Errores propios | Gates |
|---|---|---|---|---|---|
| `POST /me/git-links/{provider}/start` | persona | — | `GitLinkStartResponse` | 400 `provider-not-supported`; 409 `provider-already-linked` | exento PW+ONB |
| `POST /me/git-links/{provider}/callback` | persona | `GitLinkCallbackRequest` | `GitLinkResponse` | 400 `invalid-link-state`/`provider-not-supported`; 409 `link-user-mismatch`/`provider-account-taken`; 502 `provider-unavailable` | exento PW+ONB |
| `DELETE /me/git-links/{provider}` | persona | — | **204** vacío | 404 `provider-not-linked` | todos |
| `GET /me/git-links` | persona | — | `List<GitProviderLinkView>` | — | todos |

- `{provider}` se parsea por nombre; hoy solo `GITHUB` (`users.git-providers.github.enabled`, default `false`: sin credenciales el proveedor queda deshabilitado y la app arranca igual).
- Flujo OAuth en dos pasos con `state` de un solo uso (TTL 5 min); el `state` se consume **antes** de canjear el código.
- Un link exitoso + tour completado limpia `first_login` (DEC-GL-14).

---

## 4. Esquemas de request/response

### 4.1 Requests

| DTO | Campos | Validación |
|---|---|---|
| `LoginRequest` | `email`, `password` | ambos obligatorios; email con formato |
| `VerifyTwoFactorRequest` | `challenge_id`, `code` | obligatorios; `code` = 6 dígitos (`\d{6}`) |
| `ResetRequest` | `email` | obligatorio, formato email |
| `ResetConfirmRequest` | `token`, `new_password` | obligatorios |
| `ClientCredentialsRequest` | `client_id`, `client_secret`, `grant_type`, `scope`, `audience` | primeros 4 obligatorios; `grant_type` debe ser `client_credentials`; `audience` obligatorio a nivel negocio |
| `StudentRegistrationRequest` | `first_names`, `last_names`, `legajo`, `email`, `password`, `invitation_code`, `terms_version` | todos obligatorios; email con formato |
| `StaffRegistrationRequest` | `first_names`, `last_names`, `email`, `password`, `terms_version` | todos obligatorios; email con formato |
| `ActivateAccountRequest` | `token` | obligatorio; `[A-Za-z0-9_-]{40,64}` |
| `ResendCodeRequest` | `email` | obligatorio, formato email |
| `OnboardingRequest` | `tour_ok` | debe ser `true`; ignora campos extra |
| `CreateUserRequest` | `first_names`, `last_names`, `email`, `password` | todos obligatorios |
| `AdminDeactivationRequest` | `password`, `two_factor_code`, `username_confirmation` | todos obligatorios |
| `RoleChangeRequest` | `role` | obligatorio; enum `ADMIN\|GESTOR\|PROFESSOR\|STUDENT` |
| `AddEmailRequest` | `email`, `role` (opcional) | email obligatorio; `role` string crudo: `PROFESSOR` (default) o `GESTOR` |
| `CreateWhitelistRequest` | `email`, `reason` | ambos obligatorios |
| `ResolveWhitelistRequest` | `approve`, `rejection_reason` | `rejection_reason` obligatorio si `approve=false` |
| `GitLinkCallbackRequest` | `code`, `state` | ambos obligatorios |

### 4.2 Responses

| DTO | Campos |
|---|---|
| `LoginResponse` | `challenge_id` (string), `message` (string) |
| `SessionResponse` | `expires_in` (segundos del access token) |
| Token de servicio | `access_token`, `token_type` (`Bearer`), `expires_in` |
| `UserMeResponse` | `id`, `first_names`, `last_names`, `legajo`, `email`, `role`, `account_status`, `must_change_password`, `first_login`, `guided_tour_completed`, `github_username`, `avatar_ref`, `email_verified`, `created_at`, `terms_accepted_at`, `terms_version` |
| `ProfileResponse` | `id`, `first_names`, `last_names`, `github_username`, `avatar_ref`, `avatar_url` (URL firmada, vale 1 h); `legajo` solo para ADMIN o servicio con `users.legajo.read`; `email` y `account_status` solo para ADMIN (nulos en otro caso). Actualizado contra `tpi-users` `develop` (753e5a5, 2026-10-10) |
| `UserListItemResponse` | `id`, `first_names`, `last_names`, `legajo`, `email`, `role`, `account_status`, `created_at` |
| `WhitelistEntryResponse` | `id`, `email`, `role`, `created_at` |
| `WhitelistRequestResponse` | `id`, `email`, `requested_by`, `status`, `reason`, `rejection_reason`, `created_at` |
| `GitLinkStartResponse` | `authorization_url` |
| `GitLinkResponse` | `provider`, `username` |
| `GitProviderLinkView` | `provider`, `username`, `linked_at` |

Respuestas ad-hoc: `{ "id": "..." }` (create user, add whitelist, create request), `{ "message": "..." }` (reset, resend), `{ "version", "texto" }` (terms).

### 4.3 Enums

| Enum | Valores |
|---|---|
| `Role` | `ADMIN`, `GESTOR`, `PROFESSOR`, `STUDENT` |
| `AccountStatus` | `PENDING_EMAIL`, `PENDING_COURSE`, `ACTIVE`, `DEACTIVATED` |
| `RequestStatus` | `PENDING`, `APPROVED`, `REJECTED` |
| `GitProvider` | `GITHUB` |

---

## 5. Eventos Kafka (contrato entre servicios)

### 5.1 Producidos — topic `user-events` (key = `userId`, v1)

| Evento | Cuándo | Payload |
|---|---|---|
| `STUDENT-REGISTERED` | El estudiante verificó su email y entra a validación de curso | `userId`, `studentNumber`, `invitationCode` |
| `ACCOUNT-DEACTIVATED` | Baja lógica por ADMIN/GESTOR | `userId`, `role`, `deactivatedBy`, `deactivatedAt` |

### 5.2 Producidos — topic `notification-events` (key = `userId`, v1)

Payload común: `to`, `subject`, `html`. Tipos:
`TWO-FACTOR-EMAIL-PREPARED`, `ACCOUNT-ACTIVATION-EMAIL-PREPARED`, `PASSWORD-RESET-EMAIL-PREPARED`, `REQUEST-PENDING-EMAIL-PREPARED`, `ENABLING-RESOLVED-EMAIL-PREPARED`, `BREAKGLASS-ALERT-EMAIL-PREPARED`, `WHITELIST-SUBMISSION-EMAIL-PREPARED`, `WHITELIST-DECISION-EMAIL-PREPARED`.

### 5.3 Consumido — topic `course-events` (borrador, productor `tema-02-cursos`)

`COURSE-VALIDATION-RESOLVED` v1, payload `userId`, `result`, `courseId`. La message key aún no está definida por el equipo de Cursos; el contrato figura como draft.

**Outbox transaccional:** todo evento se persiste en `outbox_events` dentro de la misma transacción del cambio de datos y lo publica un poller (3 s). Tipos/versiones desconocidos se ignoran; envelope o payload inválido se rechaza antes de tocar estado de negocio.

---

## 6. Límites y resiliencia

### 6.1 Límites del servicio (429 `too-many-attempts` + `Retry-After`)

| Regla | Límite |
|---|---|
| Fallos de login por email | 5 / 15 min |
| Pedidos de reset por email | 3 / 15 min |
| Desafíos 2FA emitidos por email | 5 / 15 min |
| Reenvíos de activación por email | 3 / 15 min |
| Intentos de código OTP | 5 (TTL 2FA 5 min; activación 30 min) |

### 6.2 Límites y garantías del gateway

| Regla | Valor |
|---|---|
| `POST /api/users/public/auth/**` | 600 req/min por IP |
| `/api/users/public/registration/**` | 10 req/min por IP |
| Timeout al servicio | 3 s (después: `503 service-unavailable` + `Retry-After`) |
| Retry | solo GET, 1 reintento |
| Bulkhead | 64 llamadas concurrentes (rechazo inmediato) |
| Circuit breaker | abre al 50 % de fallas sobre 20 llamadas |
| Caché de sesión | 3 s ⇒ esperar ~4 s después de login/logout antes de sacar conclusiones |

---

## 7. Dónde consultar el contrato vivo

Con el stack levantado:

- **Swagger UI:** `http://localhost:3000/api/users/public/docs`
- **OpenAPI crudo:** `http://localhost:3000/api/users/public/v3/api-docs`
- **Dropdown de todos los servicios:** `http://localhost:3000/api/docs/ui`

Las rutas de docs cuelgan del prefijo público a propósito: el gateway solo deja pasar sin JWT lo que matchea `/api/*/public/**`, y el servicio no publica puertos.

## 8. Archivos fuente principales

| Tema | Archivo |
|---|---|
| Controladores | `tpi-users/src/main/java/.../auth/controllers/*.java`, `.../users/controllers/*.java` |
| DTOs | `.../auth/dto/*.java`, `.../users/dto/*.java` |
| Errores | `.../shared/web/ErrorTypes.java`, `ApiException.java`, `GlobalExceptionHandler.java` |
| Gates | `.../shared/gates/SkipAccountGate.java`, `AccountGateInterceptor.java` |
| Headers | `.../shared/security/IdentityHeaders.java`, `GatewayIdentityFilter.java` |
| Cookies/JWT | `.../auth/services/SessionCookieService.java`, `.../auth/tokens/TokenClaims.java` |
| Eventos | `tpi-users/docs/KAFKA-EVENT-CONTRACTS.md` |
| Config | `tpi-users/src/main/resources/application.properties` |
| Gateway | `tpi-api-gateway/src/main/resources/application.yml` |
