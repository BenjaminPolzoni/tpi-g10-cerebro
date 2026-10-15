# Microservicio: API Gateway (`tpi-api-gateway`)

> **Ficha Técnica Canónica y Contrato Perimetral**  
> Tema: **Tema 11 — Puerta de Enlace de la Plataforma (API Gateway)**  
> Equipo Responsable: **Tema 11 (Infraestructura)**  
> Repositorio: `2026-P4-BE/tpi-api-gateway` (Local: `D:\Dev\IdeaProjects\Progra4\tpi-api-gateway`)  
> Estado: **Vigente (v2.0.0)**

---

## 1. Identidad y Red

| Parámetro | Valor |
|---|---|
| **Nombre de Aplicación (Eureka)** | `api-gateway` |
| **Puerto Público del Gateway** | `8080` (punto de entrada unificado) |
| **Puerto de Gestión (Management/Actuator)** | `8081` |
| **Tecnología Base** | Spring Cloud Gateway (Reactor Netty reactivo) |
| **Descubrimiento de Servicios** | Eureka Client (`http://localhost:8761/eureka/` / Tailnet) |
| **Validación Criptográfica** | JWKS de `users-service` (`${JWKS_URI}`) |
| **Gestión de Sesiones** | Redis (`6379`) con timeout estricto de 500 ms |

---

## 2. Reglas de Ruteo Perimetral

### Derivación de Rutas por Service ID
- El Gateway enruta peticiones mapeando el prefijo de la URL al nombre del microservicio registrado en Eureka:
  $$\text{/api/<segmento>/**} \longrightarrow \text{lb://<segmento>-service}$$
- **Ejemplos:**
  - `/api/roadmap/**` $\rightarrow$ `lb://roadmap-service`
  - `/api/course/**` $\rightarrow$ `lb://course-service`
  - `/api/accounting/**` $\rightarrow$ `lb://accounting-service`
  - `/api/engine-challenge/**` $\rightarrow$ `lb://engine-challenge-service`
  - `/api/users/**` $\rightarrow$ `lb://users-service`
  - `/api/backoffice/**` $\rightarrow$ `lb://backoffice-service`

### Allowlist Obligatoria (`GATEWAY_ALLOWLIST`)
- Registrar un servicio en Eureka **no lo expone automáticamente**. El Gateway solo rutea hacia servicios presentes en la variable `GATEWAY_ALLOWLIST` (DEC-06). Cualquier petición fuera de la lista recibe `404 Not Found`.

---

## 3. Seguridad, Autenticación y Propagación de Identidad

### Validación de Tokens
- El Gateway intercepta toda petición entrante protegida y valida la firma del JWT contra el JWKS de `users-service`.
- Soporta tanto el header `Authorization: Bearer <token>` (llamadas API/M2M) como la cookie `fu_at` (llamadas desde el frontend Angular).

### Inyección de Headers Reservados (`IdentityPropagationFilter`)
Tras validar la autenticación, el Gateway remueve cualquier header falsificado por el cliente y propaga los siguientes encabezados de confianza hacia los microservicios:

| Header | Significado |
|---|---|
| `X-Principal-Type` | `"user"` o `"service"` |
| `X-User-Id` | UUID del usuario autenticado |
| `X-User-Roles` | Roles verificados (`ADMIN,MANAGER,PROFESSOR,STUDENT`) |
| `X-Service-Id` | Microservicio emisor en llamadas técnicas |
| `X-Service-Scopes` | Scopes autorizados |
| `traceparent` / `X-Request-Id` | Contexto de observabilidad distribuida |

---

## 4. Patrones de Resiliencia Perimetral

1. **Circuit Breakers por Ruta:** Cada servicio cuenta con su propia instancia de Circuit Breaker para evitar que la caída de un microservicio bloquee el tráfico de los demás.
2. **Timeouts Acotados:**
   - Timeout por carril de ruta: **28 segundos** (`GATEWAY_VARIANTS_LANE_TIMEOUT`).
   - Timeout de lectura de sesión Redis: **500 ms** (falla cerrado con `503 Service Unavailable` ante saturación de Redis).
3. **Reintentos Idempotentes:** Únicamente se reintentan peticiones con verbo **`GET`** (1 reintento con backoff). Los verbos `POST`, `PUT`, `PATCH`, `DELETE` nunca se reintentan automáticamente para prevenir duplicaciones.
4. **Formato de Error Estándar:** Todo fallo originado en el Gateway se devuelve con `Content-Type: application/problem+json` respetando RFC 9457 / RFC 7807.
