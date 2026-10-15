---
tags: [tpi, g10, acuerdo, plataforma, gateway, eureka, kafka, identidad]
fecha: 2026-09-26
grupos: [G10, Gxx]  # API Gateway / Identity (Tema 01) y Kafka (Tema 11); grupos a verificar
estado: vigente
contrato: "tpi-roadmap/docs/contracts/08-comunicacion-gateway.md"
---

# Acuerdo con la plataforma (API Gateway, Eureka, Identity y Kafka)

> [!info] Fuentes
> - `tpi-roadmap/docs/contracts/08-comunicacion-gateway.md` ([GitHub](https://github.com/2026-P4-BE/tpi-roadmap/blob/develop/docs/contracts/08-comunicacion-gateway.md)): checklist de integración con el Gateway (basado en el deck Tema 01).
> - `tpi-roadmap/docs/contracts/api-gateway.pptx.pdf` ([GitHub](https://github.com/2026-P4-BE/tpi-roadmap/blob/develop/docs/contracts/api-gateway.pptx.pdf)): deck del Gateway, **existe, no se leyó**.
> - `tpi-roadmap/docs/T-01-7-EUREKA-GATEWAY.md` (Eureka, probes, token técnico, provisión del cliente) y `docs/P-11-5-issues.md` (alta de scopes).
> - `tpi-roadmap/tpi-integration.yml` (offers y needs) y `.tpi/platform/*` (compose de plataforma).
> - Repos de la contraparte: `tpi-api-gateway` (PR #29), `tpi-users` (`ScopeCatalog.java`), `tpi-system-compose` (`registry/services.yml`, issues #92, #137, PR #193).

## Qué se acordó
- **Un solo nombre** en tres lugares: repo `tpi-roadmap`, Eureka `spring.application.name=roadmap-service`, prefijo del Gateway `/api/roadmap/**`. El `serviceId` de Eureka es la fuente del ruteo (`lb://ROADMAP-SERVICE`). No cambiar sin avisar al grupo del Gateway.
- **Toda llamada saliente va por el Gateway**: nunca micro a micro directo.
- **El Gateway valida la firma del JWT y propaga identidad; no autoriza por rol.** La autorización por rol y por pertenencia al curso es nuestra. Roadmap **no parsea el JWT**.
- **Anti-spoofing:** el `IdentityPropagationFilter` borra los headers `X-*` entrantes e inyecta los verificados.
- **Identidad de servicio:** los micros se identifican con token `client_credentials` (audience = serviceId destino, scope `<segmento>.<recurso>.<acción>`). No existe `on_behalf_of`: Roadmap llama en contexto propio.
- **Kafka:** broker compartido (`event-bus:29092`), topics provisionados centralmente por **Tema 11**; prohibido crearlos. Ver [[acuerdos/notificaciones-bus|bus de eventos]].

## Quién lo acordó
- G10: equipo Roadmap.
- Plataforma: equipo API Gateway, Identity/Users (Tema 01) y Tema 11 (Kafka), Gxx (verificar). Según G11 (2026-10-15): el Gateway lo lleva Users (G07) y Kafka, Notificaciones. Los trámites son issues de onboarding en `tpi-users` y `tpi-system-compose` (Identity los convierte en PR `feature/onboard-<serviceId>`).

## Contrato técnico

### Registro y rutas
| Concepto | Valor |
|---|---|
| Eureka | `register-with-eureka=true`, `fetch-registry=false`, `healthcheck.enabled=true`; sonda de readiness `/actuator/health/readiness` (Flyway + BD) |
| Puertos | app `8010`, actuator `8011` (solo red interna) |
| Rutas | público `/api/roadmap/public/**` (hoy `GET /public/ping`); privado `/api/roadmap/**` (JWT válido) |
| Path | el controller recibe la URL completa, sin `RewritePath` |
| Probes | `liveness` (solo proceso), `readiness` (contexto + Flyway + BD) |

### Headers que llegan del Gateway
| Header | Contenido |
|---|---|
| `X-Principal-Type` | `user` o `service` |
| `X-User-Id`, `X-User-Roles` | persona (UUID, roles separados por coma) |
| `X-Service-Id`, `X-Service-Scopes` | servicio (`MS` + scopes, sin espacios); scopes tratados como texto opaco |
| `traceparent`, `X-Request-Id` | trazabilidad; alimentan el `trace_id` de los Problem Details |

`GatewayHeadersFilter` rechaza mezclas de headers de usuario y servicio y `X-Delegated-User`. Una lista de roles con elementos vacíos no autentica.

### Token técnico saliente
- `POST /api/users/public/auth/token` con `client_credentials`; respuesta `access_token` / `expires_in`; TTL 5 min; caché por `(audience, scope)`; sin retries locales. Ver [[acuerdos/users|Users]].
- Audiences y scopes que usamos:

| Destino | Audience | Scope |
|---|---|---|
| Courses | `course-service` | `course.sections.read`, `course.enrollment.read`, `course.groups.read`, `course.restrictions.read`, `course.activities.read`, `course.teaching-membership.read` |
| Accounting | `accounting-service` | `accounting.account.read` |
| Motor | `engine-challenge-service` | `challenges.catalog.read` |
| Backoffice | `backoffice-service` | `backoffice.parameters.read` |
| Users | `users-service` | `users.profile.read`, `users.legajo.read` |

- **Lo que ofrecemos** (`tpi-integration.yml`): `roadmap.gate.read` y `roadmap.progress.read`. Solo `roadmap.progress.read` se **exige** en código (lectura de progreso agregado); el gate admite cualquier principal de servicio.
- Credenciales: `ROADMAP_TECHNICAL_CLIENT_ID` / `ROADMAP_TECHNICAL_CLIENT_SECRET` por entorno y Vault (`secret/tpi/shared/clients/<team>`). **Nunca en el repo ni por chat.**

### Formato de errores y envelope
- Errores: `application/problem+json` (RFC 7807/9457) con `trace_id`.
- Respuestas OK: envelope global `{ data, message, success, timestamp }`. HTTP en `snake_case` (migración `ced4ba0`, 2026-10-05; `f936760`, 2026-10-08).

## Impacto en nuestro código
- `common/security/SecurityConfig`, `GatewayHeadersFilter`, `ServiceIdentity`, `Roles`, `StudentViewer`.
- `clients/auth/*`, `clients/ClientHttpTimeouts`, `clients/CorrelationPropagationInterceptor`, `clients/IntegratedClientsValidator`.
- `common/web/ApiExceptionHandler`, `ApiEnvelopeAdvice`.
- `common/config/SpringDocConfig`, `docs/api_doc/swagger.json` (el Gateway exige el contrato OpenAPI para dar de alta el micro).
- `application.properties` (Eureka, actuator, `app.clients.*`), `tpi-integration.yml`, `.tpi/platform/` (compose de la plataforma).

## Pendiente / próximos pasos
- [ ] **Allowlist del Gateway** (`include-expression` del discovery locator): el checklist §8 la marca "pendiente, pedir al squad Gateway"; no hay evidencia de cierre en el repo.
- [ ] La ruta pública `/api/roadmap/public/**` sigue pendiente de confirmación con Gateway (`T-01-7`).
- [ ] `serviceId` y scope nominales de **Motor** para el gate (hoy cualquier servicio puede llamar el gate; ver [[acuerdos/motor-desafios-g09|Motor]]).
- [ ] `vidas.read`/`inventario.read` quedaron como propuesta nuestra y no se usan; limpiar la mención en el acta de Accounting.
- [ ] Verificar que los scopes H1 de Courses y `users.legajo.read` están emitidos en el registry del entorno de la demo. G12 (2026-10-15): existe `student.enrollment.read`, que lee la matrícula del alumno en el curso.

> [!warning] Riesgos
> - Sin allowlist, el Gateway ignora el servicio en silencio (404 para el cliente).
> - Un scope fuera del catálogo da `400`; una audience equivocada da `403 invalid-audience`.
> - El micro debe seguir inaccesible directamente desde Internet: confía por completo en los headers.

> [!question] Verificar
> `08-comunicacion-gateway.md` menciona un `TraceIdFilter` (`infrastructure/config`) que **no aparece** en `origin/develop`; el `trace_id` hoy lo arma `ApiExceptionHandler` desde `traceparent`/`X-Request-Id`. Confirmar si el filtro y el MDC de `logback-spring.xml` siguen vigentes.

## Historial
- 2026-09-26: checklist del Gateway (`08-comunicacion-gateway.md`), Eureka y probes (T-01.7); token técnico (`46f3b73`).
- 2026-10-04: lectura M2M de secciones y scope `course.sections.read` (P-11.5).
- 2026-10-09: scopes H1 de Courses declarados como `needs`.
- 2026-10-11: se ofrece `roadmap.progress.read` (`roadmap-events-v1`).
- 2026-10-14: nota creada desde `origin/develop` (`57ff06a`).
- 2026-10-15: respuestas en [[sprints/sprint-3/08-dudas|08-dudas]]: Gateway = Users (G07), Kafka = Notificaciones (G11); existe `student.enrollment.read` (G12); `TraceIdFilter` se borró a propósito (E7); Neo4j es solo para roadmap-service (G1).
