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

**Checklist Eureka:**
- [ ] `register-with-eureka=true`
- [ ] `fetch-registry=false`
- [ ] `healthcheck.enabled=true`
- [ ] `/actuator/health/liveness` y `/readiness` exponen probe status

## 3. Rutas públicas vs privadas

```yaml
app:
  api:
    base-path: /api/roadmap
    public-path: /api/roadmap/public
    private-path: /api/roadmap
```

| Nivel | Path | Acceso |
|---|---|---|
| **Público** | `/api/roadmap/public/**` | Sin autenticación (healthcheck, docs) |
| **Privado** | `/api/roadmap/**` | Requiere JWT válido (el Gateway lo valida) |

> Los controllers usan `@RequestMapping("${app.api.base-path:/api/roadmap}")`
> como base, y los endpoints públicos van bajo `/public/`.

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

## 6. Trace ID en logs

El `TraceIdFilter` (`infrastructure/config/TraceIdFilter.java`) extrae:
- `traceparent` → MDC `traceId` (32 hex chars)
- `X-Request-Id` → MDC `requestId`

Formato de log (configurado en `logback-spring.xml`):

```
2026-09-16 20:17:29.123 [main] [abc123:def456] INFO  c.u.f.r.RoadmapService - Procesando...
```

**Checklist trace:**
- [ ] `TraceIdFilter` registrado como `@Component`
- [ ] `logback-spring.xml` con `%X{traceId}:%X{requestId}` en el pattern
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
| 6 | Loguear trace ID | ✅ `TraceIdFilter` + `logback-spring.xml` |

## 9. Docker (ya configurado)

`docker-compose.yml` ya incluye:
- **eureka** (stand-in local, puerto 8761)
- **gateway** (stand-in local, puerto 8080)
- **ms-roadmap** (con `EUREKA_URL=http://eureka:8761/eureka/`)
- **postgres** + **kafka**

Para levantar todo: `docker compose up --build`
