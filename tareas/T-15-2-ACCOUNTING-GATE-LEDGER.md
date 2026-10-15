# T-15.2 — Integración del Gate con Accounting y ledger XP

## Estado

La tarea queda cubierta mediante la composición de implementaciones existentes. T-15.2 no crea
un segundo cliente ni otro ledger:

- T-15.1 publicó el endpoint de elegibilidad y conectó `GateService` con `InventoryClient`.
- T-15.4 definió vidas libres y la exención de `RECOVERY`/`LLM`.
- T-03.2 implementó `HttpInventoryClient`, caché vigente y degradación 503.
- T-03.3 y el listener de resultados ya registran el XP en el ledger propio `xp_movement`.

## Flujo de vidas del Gate

```text
GateController
    → GateService
        → InventoryClient
            → HttpInventoryClient (T-03.2)
                → API Gateway
                    → Accounting /lives-availability
```

`GateService` depende solamente del puerto `InventoryClient`. `StudentLives.hasLives()` evalúa
`freeLives = currentLives - reservedLives`:

- `freeLives > 0`: la validación de vidas no bloquea; las demás reglas conservan su precedencia.
- `freeLives <= 0` y política `STANDARD`: `eligible=false`, `reason=no_lives`.
- política `RECOVERY` o `LLM`: no consulta vidas y no bloquea por `no_lives`.
- `InventoryUnavailableException`: error técnico HTTP 503 Problem Details. Nunca se transforma en
  `no_lives`, `eligible=true` ni en un `reason` adicional.

La caché, TTL, llamada HTTP, token y tratamiento de timeout/5xx pertenecen a T-03.2 y no se
duplican en el Gate.

## XP y ledger propio

`RoadmapEventListener` recibe el resultado del Motor y delega en
`ProgressService.recordResult`. Dentro de una misma transacción, el servicio:

1. inserta un `XpMovementEntity` en `xp_movement` mediante
   `XpMovementRepository.saveAndFlush`;
2. aplica el mismo `result.xp()` sobre la proyección `student_course.total_xp`;
3. protege la idempotencia con `uq_xp_movement_event_id`.

Roadmap no consulta XP a Accounting, Motor ni otro servicio. El BDD de resultados verifica que
`student_course.total_xp` sea igual a `SUM(xp)` de `xp_movement`, incluso ante entregas duplicadas
y resultados concurrentes.

## Decisiones vigentes

- El ledger mencionado por T-15.2 es el ledger XP propio de Roadmap, no un ledger de Accounting.
- Los ítems y `equip-summary` no participan de la elegibilidad; pertenecen a HU-35.
- `origin_unavailable` y `origen_no_disponible` están obsoletos.
- T-15.5 cerró el vocabulario de Sprint 1 sin agregar razones para fallos técnicos.
- La ejecución HTTP real continúa dependiendo del proveedor de token técnico de Gateway/Users.

## Evidencia de tests reutilizada

- `GateLivesAndEnrollmentTest`: vidas reservadas, una vida libre, recuperación sin consulta a
  Inventario y 503 sin respuesta funcional del Gate.
- `GateServiceTest`: `currentLives=0` produce `no_lives` y recuperación con cero vidas es elegible.
- `StudentLivesTest`: cálculo de vidas libres.
- `HttpInventoryClientTest`: mapeo, caché, expiración, timeout, 5xx y respuestas inválidas.
- `ChallengeResultBddSuiteTest`: persistencia, idempotencia y equivalencia entre `total_xp` y la
  suma del ledger `xp_movement`.
