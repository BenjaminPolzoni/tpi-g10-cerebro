# T-35.1 — Endpoint de inventario (proxy + caché + degradación)

## Alcance

HU-35 / CA1 y CA4: el alumno ve sus ítems con efecto, estado y condición de uso, y ante una
falla de Accounting ve el último dato conocido con aviso, sin bloquear la lectura.

Equipar/activar ítems (T-35.2), el contrato con el Motor (T-35.3) y el HUD (T-35.4) quedan
fuera de esta tarea.

## Endpoint

```http
GET /api/roadmap/courses/{courseId}/inventory
```

- Rol `STUDENT`. El alumno sale del `X-User-Id` puesto por el Gateway, nunca de la URL: solo
  se ve el inventario propio.
- `courseId` es el `courseCohortId`. Un alumno sin inscripción activa recibe `403`
  (`student.not-enrolled`) y no se consulta a Accounting.

```json
{
  "courseId": "…",
  "studentId": "…",
  "currentLives": 3,
  "reservedLives": 1,
  "freeLives": 2,
  "availableBalance": 850.00,
  "items": [
    {
      "itemInstanceId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "catalogItemId": "SHIELD-001",
      "itemName": "Escudo x2",
      "itemType": "SHIELD",
      "itemEffect": "LIFE_PROTECTION",
      "applicableChallengeScope": "ALL",
      "status": "EQUIPPED",
      "maxCharges": 2,
      "remainingUses": 2
    }
  ],
  "stale": false,
  "retrievedAt": "2026-09-26T18:00:00Z",
  "notice": null
}
```

## Flujo

```text
InventoryController
    → InventoryService           (último dato conocido, aviso)
        → InventoryClient.fetchEquipSummary
            → HttpInventoryClient (caché corta)
                → API Gateway
                    → Accounting /equip-summary   (acta v1 §3.7)
```

- **Caché corta**: `HttpInventoryClient` guarda el resumen por curso+alumno con el mismo TTL
  que la caché del Gate (`INVENTORY_CACHE_TTL`), en una caché separada.
- **Validación**: un resumen sin vidas, sin saldo, sin lista de ítems o con un ítem sin
  `itemInstanceId`/`status`/contadores válidos se trata como indisponibilidad; nunca se
  completa con datos inventados.
- **Vocabulario abierto**: `itemType`, `itemEffect`, `applicableChallengeScope` y `status`
  viajan como texto; un valor nuevo de Accounting no rompe la lectura.

## Degradación (acta v1 §6.2)

| Situación | Respuesta |
|---|---|
| Accounting responde | `200`, `stale=false`, `notice=null` |
| Accounting falla y hay último dato conocido dentro de la retención | `200`, `stale=true`, `retrievedAt` del dato original y `notice` con el aviso |
| Accounting falla y no hay último dato | `503` Problem Details (`inventory.items-unavailable`); nunca un inventario vacío ni ceros |

La retención del último dato conocido es configurable (`INVENTORY_LAST_KNOWN_RETENTION`,
default `24h`) y se guarda por curso+alumno: nunca se muestra a otro alumno.

El último dato conocido **solo** se usa para mostrar. El Gate sigue decidiendo con
`fetchLives` y caché vigente (T-03.2 / T-15.2): una caché vencida jamás habilita un intento.

## Configuración

| Propiedad | Variable | Default |
|---|---|---|
| `app.clients.inventory.equip-summary-path` | `ACCOUNTING_EQUIP_SUMMARY_PATH` | `/api/accounting/courses/{courseId}/accounts/{studentId}/equip-summary` |
| `app.clients.inventory.last-known-retention` | `INVENTORY_LAST_KNOWN_RETENTION` | `24h` |

En modo `stub`, `InMemoryInventoryClient` devuelve un resumen determinista (un escudo
equipado y un boost consumido) coherente con sus vidas; `INVENTORY_STUB_UNAVAILABLE=true`
simula la caída.

> **Nota T-09.5 (#4354):** párrafo histórico; el doble se eliminó y los escenarios
> usan `InventoryHttpScenario` (cliente HTTP real guionado).

## Evidencia

- `HttpInventoryClientTest`: mapeo de `equip-summary`, caché vigente, vencimiento y
  respuestas inválidas.
- `InMemoryInventoryClientTest`: doble determinista y caída simulada.
- `InventoryServiceTest`: CA1, CA4, 503 sin dato previo, retención vencida, aislamiento
  entre alumnos y 403 sin inscripción.
- `InventoryControllerTest`: alumno inscripto, no inscripto y rol no permitido.
