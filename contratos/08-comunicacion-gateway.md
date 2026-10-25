# 08 · Comunicación con el API Gateway y otros microservicios

> Checklist de integración antes de subir a la plataforma.
> Basado en el deck Tema 01 y las convenciones del API Gateway.

## 1. Identidad del microservicio

Cada servicio tiene un **único nombre** que se usa en tres lugares con el mismo valor:

| Dónde | Propiedad | Nuestro valor |
|---|---|---|
| Repositorio | `tpi-{nombre}` | `tpi-roadmap` |
| Eureka | `spring.application.name` | `roadmap-service` |
| Gateway externo | Prefijo de ruta | `/api/roadmap/**` |

> **Regla**: el `serviceId` en Eureka (`roadmap-service`) es la fuente del ruteo.
> El Gateway lo normaliza y arma `lb://ROADMAP-SERVICE`.

## 2. Configuración Eureka (obligatoria)

```yaml
spring:
  application:
    name: roadmap-service   # ← mismo valor en repo, eureka y path

eureka:
  client:
    service-url:
      defaultZone: ${EUREKA_URL:http://localhost:8761/eureka/}
    register-with-eureka: true      # SIEMPRE true
    fetch-registry: false           # SIEMPRE false (no descubrimos otros por Eureka)
    healthcheck:
      enabled: true                 # SIEMPRE true (requiere /actuator/health)
  instance:
    prefer-ip-address: true
```

La configuración real está en `application.properties` (claves `eureka.client.*`, con el mismo valor).
Además, el servicio publica la salud en un **puerto de gestión aparte** (`management.server.port`, por defecto `8011`,
variable `MANAGEMENT_PORT`) y lo informa a Eureka en `eureka.instance.metadata-map.management.port`.

**Checklist Eureka:**
- [x] `register-with-eureka=true`
- [x] `fetch-registry=false`
- [x] `healthcheck.enabled=true`
- [x] `/actuator/health/liveness` y `/readiness` exponen probe status (expone `health`, `info` y `prometheus`; la readiness incluye `flyway` y `db`)

## 3. Rutas públicas vs privadas

```properties
# application.properties
app.api.public-path=/api/roadmap/public
app.api.private-path=/api/roadmap
```

| Nivel | Path | Acceso |
|---|---|---|
| **Público** | `/api/roadmap/public/**` | Sin autenticación (healthcheck, docs) |
| **Privado** | `/api/roadmap/**` | Requiere JWT válido (el Gateway lo valida) |

> Los controllers privados usan `@RequestMapping("${app.api.private-path}")` y los públicos
> (hoy solo `PingController`) `@RequestMapping("${app.api.public-path}")`. No existe una
> propiedad `app.api.base-path`.

## 4. Headers que el Gateway inyecta

El **IdentityPropagationFilter** del Gateway:
1. **Borra** cualquier header entrante con estos nombres (anti-spoofing)
2. **Inyecta** el set real ya verificado

| Header | Tipo | Contenido |
|---|---|---|
| `X-Principal-Type` | `String` | `user` o `service` |
| `X-User-Id` | `UUID` | Identidad del usuario autenticado |
| `X-User-Roles` | `String` | Roles verificados (`ROLE_PROFESOR,ROLE_ALUMNO`) |
| `X-Service-Id` | `String` | ID del servicio (si `X-Principal-Type=service`) |
| `X-Service-Scopes` | `String` | Scopes del servicio |
| `traceparent` | `String` | W3C Trace Context (`00-<traceId>-<spanId>-<flags>`) |
| `X-Request-Id` | `UUID` | Correlación de la request |

> **Nunca** reinventar headers. Consumir estos tal cual.

`GatewayHeadersFilter` arma la identidad solo con estos headers y **no autentica** si llegan mezclados:
un pedido de usuario (`X-Principal-Type: user`) con `X-User-Id` UUID válido se rechaza si trae también
`X-Service-Id`, `X-Service-Scopes` o `X-Delegated-User`; un pedido de servicio (`service`) exige
`X-Service-Id` y `X-Service-Scopes` y se rechaza si trae `X-User-Id`, `X-User-Roles` o `X-Delegated-User`.
Un `X-User-Roles` con un elemento vacío (por ejemplo `A,,B`) también se rechaza.

## 5. Autorización: el Gateway NO autoriza por rol

El Gateway solo valida la **firma JWT** (borde técnico). La autorización por **rol** y
**pertenencia al curso** es responsabilidad del microservicio:

```java
@PreAuthorize("hasRole('MS') or hasRole('ADMIN')")
@GetMapping("/profile/{id}")
public UserProfile getProfile(@PathVariable UUID id) { ... }
```

**Lectura de headers en controllers:**

```java
@RequestHeader(value = "X-User-Roles", required = false) String rolesHeader,
@RequestHeader(value = "X-User-Id", required = false) UUID userId
```

**En dev local** (sin Gateway), `X-User-Roles` puede venir vacío — logear warning:

```java
if (rolesHeader == null || rolesHeader.isBlank()) {
    log.warn("X-User-Roles ausente — dev local sin Gateway. No se debe deployar así.");
}
```

## 6. Trace ID en las respuestas de error

Roadmap **no tiene** un filtro que cargue el trace ID en el log (el `TraceIdFilter` se borró a propósito,
decisión E7 de HT-23, y no hay `logback-spring.xml` con `%X{traceId}`). Hoy el trace ID se usa solo
en los errores HTTP:

- `TraceId.from(traceparent, X-Request-Id)` toma el `traceId` del header W3C `traceparent`
  (`00-<traceId>-<spanId>-<flags>`, segunda parte) o, si no vino, el `X-Request-Id`.
- `ApiExceptionHandler` y los handlers de seguridad (`ProblemJsonSecurityHandlers`) lo agregan como
  `trace_id` al problem+json de la respuesta; se omite si no vino ninguno de los dos headers.

**Checklist trace:**
- [x] Los errores devuelven `trace_id` cuando el Gateway manda `traceparent` o `X-Request-Id`
- [ ] No loguear el JWT ni headers sensibles (solo traceId/requestId)

## 7. Registro en el Gateway (allowlist)

El Gateway tiene un `include-expression` que controla qué services del discovery
locator se exponen. **Pedir inclusión** antes de deployar:

```yaml
spring.cloud.gateway.discovery.locator.enabled=true
spring.cloud.gateway.discovery.locator.include-expression=
  "'Roadmap-service,...'.contains(serviceId)"
```

> Si tu servicio no está en la allowlist, el Gateway lo ignora silenciosamente
> (404 para el cliente).

## 8. Checklist pre-deploy

| # | Punto | Estado |
|---|---|---|
| 1 | Nombre acordado (repo = eureka = path) | `tpi-roadmap` / `roadmap-service` / `/api/roadmap/**` |
| 2 | Eureka: register=true, fetch=false, healthcheck=true | ✅ `application.yml` |
| 3 | Rutas public/private configuradas | ✅ `app.api.public-path` / `app.api.private-path` |
| 4 | Allowlist en Gateway solicitada | ⬜ Pendiente (pedir al squad Gateway) |
| 5 | Consumir headers del Gateway, no reinventar | ✅ `@RequestHeader` en controllers |
| 6 | Devolver el trace ID en los errores | ✅ `TraceId` + `ApiExceptionHandler` (`trace_id` en el problem+json) |

## 9. Docker (ya configurado)

`docker/docker-compose.yml` incluye cuatro servicios:
- **postgres** (base de datos del servicio)
- **neo4j** (estructura del roadmap, T-18.1)
- **event-bus** (Kafka en modo KRaft, sin Zookeeper; puerto 29092 hacia el host)
- **app** (el servicio, perfil `dev` por defecto)

**No** incluye stand-ins de Eureka ni del Gateway. Dentro del contenedor Eureka está apagado
(`EUREKA_CLIENT_ENABLED=false`) y toda llamada saliente va a `GATEWAY_URL`, que por defecto
apunta al Gateway del host (`http://host.docker.internal:8080`). Con `KAFKA_TOPIC_ROADMAP` vacío
(el valor por defecto del compose) el outbox no publica en el bus.

Para levantar todo: `docker compose -f docker/docker-compose.yml up --build -d`
