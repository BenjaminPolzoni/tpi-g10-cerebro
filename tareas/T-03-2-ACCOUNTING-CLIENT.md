# T-03.2 — Cliente HTTP de Accounting con caché y degradación

Implementación del contrato vigente en
`docs/contracts/accounting-roadmap-v1.md`. No redefine el contrato ni implementa HU-35 o los
eventos asíncronos de Accounting.

## Flujo

```text
GateService / NodeProgressService
        ↓
InventoryClient
        ↓
HttpInventoryClient
        ↓ Authorization: Bearer <token técnico de Roadmap>
API Gateway
        ↓
GET /api/accounting/courses/{courseId}/accounts/{studentId}/lives-availability
```

El adapter traduce `{currentLives, reservedLives}` a `StudentLives`. El dominio calcula
`freeLives = currentLives - reservedLives` y no conoce URLs, HTTP, Gateway ni el DTO externo.

## Caché

- Caffeine con clave `(courseId, studentId)`.
- `expireAfterWrite`: una entrada es vigente hasta cumplir
  `app.clients.inventory.cache-ttl` desde su escritura.
- Una entrada vigente se devuelve sin llamar a Accounting.
- Una entrada vencida deja de ser visible y nunca respalda una decisión del Gate.
- `INVENTORY_CACHE_TTL=30s` es solamente el default técnico local, configurable y provisional;
  no forma parte del contrato funcional.
- El tamaño máximo también es configurable mediante `INVENTORY_CACHE_MAX_SIZE`.

## Degradación

Sin caché vigente, un timeout, error HTTP, respuesta inválida o falta de token se convierte en
`InventoryUnavailableException`. El manejo global lo devuelve como HTTP 503 y
`application/problem+json`. Nunca se sintetizan cero vidas, `no_lives` ni `eligible=true`.

Un `404` de Accounting solo se toma como cuenta ausente cuando el cuerpo marca el código
`ACCOUNT_NOT_FOUND` (campo `error` de ErrorApi, o `code` como tolerancia). Ese caso es un faltante
de datos, no una caída: se informa como 404 con `inventory.account-not-found` y los IDs consultados,
sin asumir disponibilidad ni habilitar la apertura (acta v1 §6; ver
`roadmap-motor-gate-v1.md` §6.2). Un `404` sin ese código (ruta mal ruteada, error del Gateway) es
indisponibilidad: sigue siendo el 503 de abajo.

Se agregó un timeout local de conexión y lectura (`app.clients.inventory.timeout`, 2 s por defecto)
para que un Accounting que no responde degrade a indisponibilidad en vez de colgar la request del
Gate. No se agregaron retries locales: se respeta la política del Gateway.

**W1:** el Gate lee las vidas del endpoint liviano §3.1 (`lives-availability`), no de
`equip-summary`: así deja de depender del flag `app.inventory.queries.enabled` de Accounting.
`equip-summary` (acta v1 §3.7) queda solo para la pantalla de inventario. Un interceptor
(`CorrelationPropagationInterceptor`) copia `traceparent` y `X-Request-Id` de la request entrante a
las llamadas salientes a Accounting (vidas, inventario y lote de vidas perdidas).

## Token técnico

`TechnicalTokenProvider` desacopla al cliente de clientId, secret, audience, scopes y endpoint de
emisión. T-01.7 implementa el POST `client_credentials` a
`/api/users/public/auth/token`, la validación de `expires_in` y la caché por `(audience, scope)`.

El default continúa en `stub`. Para activar `mode=http` se deben proveer credenciales y los valores
confirmados `ACCOUNTING_TOKEN_AUDIENCE` y `ACCOUNTING_TOKEN_SCOPE`; no existen defaults porque
Accounting/Gateway todavía no los acordaron. Los tests usan valores ficticios limitados al fixture.

> **Nota T-09.5 (#4354):** el modo `stub` de Inventario se eliminó; el cliente siempre
> va por HTTP y la fila `app.clients.inventory.mode` de la tabla de abajo ya no existe.

## Configuración

| Property | Variable | Uso |
|---|---|---|
| `app.clients.inventory.base-url` | `GATEWAY_URL` | Host configurable del Gateway |
| `app.clients.inventory.lives-availability-path` | `ACCOUNTING_LIVES_AVAILABILITY_PATH` | Path contractual `/api/accounting/.../lives-availability` (§3.1, el que usa el Gate) |
| `app.clients.inventory.equip-summary-path` | `ACCOUNTING_EQUIP_SUMMARY_PATH` | Path del resumen de vidas, saldo e ítems (§3.7, pantalla de inventario) |
| `app.clients.inventory.timeout` | `ACCOUNTING_INVENTORY_TIMEOUT` | Timeout de conexión y lectura hacia Accounting |
| `app.clients.inventory.cache-ttl` | `INVENTORY_CACHE_TTL` | Vigencia técnica de la entrada |
| `app.clients.inventory.max-cache-size` | `INVENTORY_CACHE_MAX_SIZE` | Límite de pares curso/alumno |
| `app.clients.inventory.token-audience` | `ACCOUNTING_TOKEN_AUDIENCE` | Audience confirmada, sin default |
| `app.clients.inventory.token-scope` | `ACCOUNTING_TOKEN_SCOPE` | Scope confirmado, sin default |
| `app.clients.inventory.mode` | `INVENTORY_CLIENT_MODE` | `http` o `stub` |

## Fuera de alcance

- endpoints de monedas, históricos, ranking e inventario;
- caché stale para visualización de ítems;
- `LIVES_EXHAUSTED`, `LIVES_AVAILABLE` y eventos de equipamiento;
- definición externa del audience y scope concretos de Accounting;
- HU-35 y T-15.2 más allá del puerto de vidas que ya consume el Gate.
