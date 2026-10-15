# T-01.7: contrato de integración de Roadmap

## Registro en Eureka

Roadmap se registra como `roadmap-service` cuando Eureka está habilitado. `EUREKA_URL`
indica la URL del servidor y `EUREKA_PREFER_IP_ADDRESS` controla si anuncia su IP
(valor local por defecto: `true`). El puerto anunciado sigue `server.port` (8080 por
defecto). Si se necesita un nombre DNS en lugar de la IP, configurar
`EUREKA_PREFER_IP_ADDRESS=false` y `EUREKA_INSTANCE_HOSTNAME` con un nombre resoluble
desde Gateway. Roadmap y Gateway deben compartir una red que permita alcanzar esa
dirección y puerto. El health check anunciado es `/actuator/health/readiness` (ver «Probes» más abajo).

En el entorno integrado, comprobar que `GET /eureka/apps/ROADMAP-SERVICE` en el
servidor Eureka muestre una instancia `UP`, con la dirección y el puerto esperados,
y que Gateway pueda consultar su `/actuator/health/readiness`. El Compose aislado de la tarea
T-01.4 desactiva Eureka a propósito; por eso no prueba este registro.

## Probes: liveness y readiness

- `GET /actuator/health/liveness`: `UP` si el proceso está vivo. No incluye la base: si
  Postgres cae, reiniciar el contenedor no lo arregla.
- `GET /actuator/health/readiness`: `UP` cuando el contexto terminó de arrancar, Flyway aplicó
  todas las migraciones (`FlywayHealthIndicator`) y la base responde. Si falla, responde `503`;
  también es `503` durante el arranque y en el apagado.

Son de red interna y no requieren headers de identidad. Eureka usa la de readiness
(`eureka.instance.health-check-url-path`), así una instancia que todavía no migró no recibe
tráfico. Los grupos se configuran en `application.properties` (`management.endpoint.health.group.*`)
y `HealthProbesTest` los verifica. El `Dockerfile` es distroless (sin `curl`), por lo que un
`healthcheck` de Compose contra estos endpoints necesitaría otra herramienta.

## Ruta y confianza en los headers

Los controllers reciben `/api/roadmap/**` completo, sin eliminar el prefijo.
El equipo Gateway debe admitir `roadmap-service` en su allowlist, resolverlo mediante
Eureka, enrutar `/api/roadmap/**` sin `RewritePath` y verificar el contrato OpenAPI.
También debe autenticar el token, quitar los headers de identidad enviados por el
cliente e inyectar los suyos. Roadmap interpreta esos headers; no valida el JWT.
El micro debe permanecer inaccesible directamente desde Internet. La ruta pública
`/api/roadmap/public/**` sigue pendiente de confirmación con Gateway.

Roadmap acepta `X-Principal-Type: user` con `X-User-Id` UUID y `X-User-Roles` separado
por comas, como ya hacía. Una lista de roles con elementos vacíos no autentica.
Para `X-Principal-Type: service`, exige `X-Service-Id` y `X-Service-Scopes` no vacíos.
Los scopes se conservan como texto opaco: Gateway aún no definió su serialización.
`on_behalf_of` no se traduce a un header para Roadmap y `X-Delegated-User` se rechaza.
Se rechazan mezclas de headers de usuario y servicio. El endpoint de eligibility de
T-15.1 admite principales de servicio; `studentId` viaja como dato funcional en el
path. Como todavía no hay `serviceId` ni scope formal acordado para Motor, Roadmap no
interpreta esos valores ni restringe el endpoint a un identificador inventado.

`traceparent` y `X-Request-Id` se usan para el `trace_id` de Problem Details. La propagación
saliente de `traceparent`/`tracestate` debe comprobarse en la integración E2E.

## Token técnico saliente: infraestructura local implementada

Roadmap obtiene sus tokens mediante el contrato consolidado del Gateway:

```http
POST /api/users/public/auth/token
Content-Type: application/json
```

```json
{
  "client_id": "...",
  "client_secret": "...",
  "grant_type": "client_credentials",
  "scope": "...",
  "audience": "..."
}
```

La respuesta contiene `access_token`, `token_type: Bearer` y `expires_in` en segundos.
`HttpTechnicalTokenProvider` realiza el POST por el Gateway, valida esos campos y conserva una
entrada separada por `(audience, scope)`. No decodifica el JWT. Un token se reutiliza únicamente
antes del límite calculado con `expires_in`; un margen anticipado opcional es configurable y vale
`0s` por defecto. La renovación del mismo destino está sincronizada para no disparar solicitudes
concurrentes duplicadas. No hay retries locales.

Los clientes dependen de `TechnicalTokenProvider` y sólo entregan un `TechnicalTokenTarget`.
No conocen el endpoint, el clientId, el secret ni la caché. Las credenciales se leen de
`ROADMAP_TECHNICAL_CLIENT_ID` y `ROADMAP_TECHNICAL_CLIENT_SECRET`; nunca se versionan ni se
registran en logs. `TECHNICAL_TOKEN_PATH` conserva como default el path contractual anterior.

Inventory permanece en `stub` por defecto. Su modo HTTP requiere
`ACCOUNTING_TOKEN_AUDIENCE` y `ACCOUNTING_TOKEN_SCOPE` no vacíos; el repositorio no fija valores
porque todavía no fueron acordados. La falta de credenciales o la imposibilidad de obtener el
token produce `TechnicalTokenUnavailableException`, que el adapter traduce a
`InventoryUnavailableException` y el Gate expone como HTTP 503, nunca como `no_lives`.

## Provisión del cliente técnico (respondido, pendiente de trámite)

Verificado contra `tpi-users` (develop), `tpi-api-gateway` (PR #29) y
`tpi-system-compose` (develop), solo lectura:

- El catálogo es `users.scopes.catalog` con entradas `scope:audience` (un scope
  mapea a una sola audience, que es el serviceId destino). Un scope fuera de
  catálogo → `400 validation`; `aud` ausente → `400`; `aud` de otro destino →
  `403 invalid-audience` (el Gateway lo valida contra la ruta resuelta,
  fail-closed).
- El alta es manual: `clientId` propuesto por nosotros (`roadmap-service`),
  fila en `service_clients` (`client_id` + hash bcrypt + descripción) y secret
  entregado una sola vez por canal seguro (script de Identity,
  Vault `secret/tpi/shared/clients/<team>`). No hay endpoint ni topic de Kafka
  para altas.
- El registro en plataforma es un issue de onboarding en `tpi-system-compose`
  (`registry/services.yml`: `segment/port/team/database/offers/needs`);
  Identity lo convierte en PR `feature/onboard-<serviceId>`. Roadmap todavía no
  tiene entrada ni rama de onboarding.
- TTL del token: 5 min; caché local por `(audience, scope)` con renovación
  anticipada (ya implementado en `HttpTechnicalTokenProvider`).
- `X-Service-Scopes` llega como `MS` + scopes por coma, sin espacios.
- Motor (`tpi-engine-challenge`) no declara `spring.application.name`: su
  serviceId/audience sale del acta G09, no se inventa.

### P-11 v1 (pedido a Identity/Users)

| # | Qué | Estado |
|---|---|---|
| 1 | Alta `clientId: roadmap-service` + secret por canal seguro | Pendiente de trámite |
| 2 | Altas en catálogo: `course.enrollment.read@course-service`, `accounting.account.read@accounting-service` | Pendiente de trámite |
| 3 | `vidas.read` / `inventario.read@accounting-service` (propuesta nuestra) | Pendiente de confirmación por Accounting |
| 4 | Scopes de Motor | Fuera de v1: sin serviceId ni acta G09 |
| 5 | `course.sections.read@course-service` para leer secciones con token de servicio | Pendiente de trámite (P-11.5) |

### P-11.5 – lectura de secciones con identidad de servicio

El listado de secciones de Courses (`GET /api/course/course-cohorts/{courseCohortId}/sections`)
exige hoy rol humano (`GESTOR/PROFESSOR/STUDENT`), no un principal `service`. El cliente
`roadmap-service` ya existe con scopes `course.enrollment.read` y `accounting.account.read`;
falta dar de alta el scope nuevo en el catálogo y en el cliente. Camino M2M, no "como alumno":
Roadmap backend no tiene token de persona (la persona viaja en la cookie `fu_at`, solo navegador)
ni hay `on_behalf_of`; el micro llama en contexto propio (sync/job/evento). El servicio debe ver
solo secciones **activas y no ocultas** (`isActive=true ∧ isVisible=true`), equivalente a la vista
de alumno, no las ocultas de Gestor.

Tareas: (1) PR a `tpi-users` `ScopeCatalog.java` con `course.sections.read` → `course-service`;
(2) sumar el scope a `needs` de `roadmap-service` en `tpi-system-compose/registry/services.yml`;
(3) re-run idempotente de `seed-service-client-v2.sh --team roadmap roadmap-service course.sections.read`.
Fase 2 (no ahora): `course.activities.read` cuando G01 exponga el catálogo de actividades.

## Valores contractuales todavía pendientes

- clientId real de Roadmap y provisión segura del clientSecret (trámite P-11.1);
- altas en catálogo de los scopes de la tabla P-11 (trámite P-11.2/3/5);
- serviceId, audience y scopes de Motor (acta G09);
- serviceId y scope autorizados para que Motor invoque el Gate;
- serialización definitiva de múltiples scopes en `X-Service-Scopes`.

No se adapta `HttpParCatalogClient` hasta resolver la contradicción específica del contrato de
Backoffice. Tampoco se habilita `INVENTORY_CLIENT_MODE=http` con valores inventados.

## Prueba E2E pendiente

La implementación local se prueba con HTTP simulado. Para cerrar la integración desplegada aún
se debe verificar: emisión con credenciales reales, rechazo de audience/scope inválidos,
renovación, allowlist, descubrimiento Eureka, path preservado, saneamiento de headers y el circuito
Roadmap → Gateway → servicio destino.

## Pendiente con otros equipos

- Gateway: allowlist, ruteo real, path preservado, saneamiento e inyección confiable
  de headers, validación de `aud`/`scope` y disponibilidad del endpoint de emisión.
- Users/Identidad: alta del cliente técnico y entrega segura de credenciales.
- Servicios destino: audiences y scopes concretos autorizados.
