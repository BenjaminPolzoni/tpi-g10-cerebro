# Contrato de eventos de Roadmap — `roadmap.events` v1

Respuesta a la solicitud del Tema 12 (Backoffice) —issue #134— para el panel
docente y el seguimiento de alumnos. Roadmap **publica** estos hechos; Backoffice
los consume y construye su read model.

| Dato | Valor |
|---|---|
| Topic | `roadmap.events` (DLT `roadmap.events.DLT`) |
| Producer | `tema-10-roadmap-service` |
| Key | `student_id` (UUID como string; es el valor, el nombre se escribe en snake_case) |
| Envelope | 6 campos obligatorios en snake_case: `event_id`, `event_type`, `event_version`, `timestamp`, `producer`, `payload`, más `organization_id` (UUID) en todo evento con organización; los globales no lo llevan |
| Header Kafka | `organization_id` (mismo valor que el del sobre) en todos los eventos del outbox; también `traceparent` y `X-Request-Id` cuando el hecho los tenía |
| `timestamp` | ISO‑8601 UTC del momento en que Roadmap **encoló** el evento (`Instant.now()` al encolar), no necesariamente el del hecho. Formato real: `Instant.toString()` con `Z`, p. ej. `2026-10-29T00:10:16.446930500Z`; la fracción de segundo puede tener 0, 3, 6 o 9 dígitos, así que no hay que asumir un ancho fijo |
| Entrega | At‑least‑once. Idempotencia por `event_id` (un duplicado no reproyecta). Los duplicados llevan **siempre el mismo `event_id`**: el reintento del poller y el redrive manual (`POST /api/roadmap/admin/outbox/{eventId}/retry`, solo ADMIN, sobre filas `FAILED` del outbox) reenvían el JSON que quedó guardado, con el mismo `event_id` y el mismo `timestamp` |
| Orden | Solo dentro de una partición; la key es `student_id` |

### Ejemplo de mensaje completo

Salida real de `OutboxService` + el `ObjectMapper` de la aplicación, capturada ejecutando
el código (2026-10-28). Los mensajes del outbox salen con la key `student_id` y el header
Kafka `organization_id` con el mismo valor que el del sobre.

```json
{"event_id":"5db61343-6968-4adc-ba44-eec30ebfd959","event_type":"NODE_COMPLETED","event_version":1,"timestamp":"2026-10-29T00:10:16.446930500Z","producer":"tema-10-roadmap-service","organization_id":"450e6922-983f-442c-b468-c0adb38dde85","payload":{"course_cohort_id":"21a38868-1450-4c04-b31a-718eeea6d87f","course_id":"21a38868-1450-4c04-b31a-718eeea6d87f","student_id":"982ece9f-5011-4665-9fa1-61f26b76d86a","node_id":"14e6dbe5-6e07-4f15-b288-8bb02626b056","challenge_id":"672748ff-a831-4256-9d37-dbe86fdec35e","section_id":"0fdadbbe-8c3b-4858-9bac-ed57242d4fef"}}
```

### `organization_id` y versiones

`develop` (desde #294) lo incluye siempre en los eventos del outbox, en el JSON y en el header.
La versión en `main` (release 3.0.0) todavía no lo incluye: hasta el próximo release, los
eventos publicados desde una instancia basada en `main` salen **sin `organization_id`**.
Los consumidores deben aceptar las dos formas.

Eventos globales, sin `organization_id` en el sobre ni en el header: `PARAMETER_CATALOG_DECLARED`
(el único que Roadmap publica; los otros dos, `GLOBAL_CONFIGURATION_CHANGED` y
`PARAMETER_DEFINITION_CREATED`, los publica Backoffice).

## Frescura

Los eventos se encolan en la tabla `outbox_event` y el `OutboxPoller` los publica cada ~3 s.
El SLA se mide desde el `timestamp` del envelope, o sea desde el **encolado**; la demora entre
el hecho y el encolado no entra en la métrica.

- `NODE_COMPLETED`, `NODE_UNLOCKED` y `BADGE_AWARDED` se encolan en la **misma transacción** del
  hecho, así que el `timestamp` coincide con él.
- `ROADMAP_MANDATORY_AVAILABILITY_CHANGED` se calcula y se encola **después del commit** del hecho
  que lo origina (en su propia transacción). Su `timestamp` es el del encolado; el momento del
  cambio viaja en `occurred_at`.
- Preservar el momento original del hecho en un reintento o redrive no es posible hoy: el
  `timestamp` se fija una sola vez al encolar y los reenvíos mantienen ese mismo valor.

## Eventos publicados

### `NODE_COMPLETED` v1

Un alumno superó un nodo del roadmap (desafío o contenido).

```json
{
  "course_cohort_id": "uuid",
  "course_id": "uuid (deprecado, mismo valor)",
  "student_id": "uuid",
  "node_id": "uuid",
  "challenge_id": "uuid",
  "section_id": "uuid"
}
```

- `course_cohort_id` es la cohorte, no el curso base. `course_id` lleva el mismo valor y queda
  **deprecado**: los eventos encolados antes de este cambio solo traen `course_id`, así que los
  consumidores tienen que aceptar los dos nombres. Se quita cuando todos hayan migrado.
- El **XP no viaja** en el evento: Roadmap no lo calcula. Para el XP acumulado
  usar `GET /api/roadmap/courses/{courseId}/students/{studentId}/progress` (`xp_total`).
- `challenge_id` puede ser `null` en nodos que no son desafío.

### `NODE_UNLOCKED` v1

Un nodo pasó a estar habilitado para el alumno.

```json
{
  "course_cohort_id": "uuid",
  "course_id": "uuid (deprecado, mismo valor)",
  "student_id": "uuid",
  "node_id": "uuid"
}
```

### `BADGE_AWARDED` v1

Un alumno obtuvo una insignia (HU‑21).

```json
{
  "course_cohort_id": "uuid",
  "course_id": "uuid (deprecado, mismo valor)",
  "student_id": "uuid",
  "badge_id": "uuid"
}
```

### `ROADMAP_MANDATORY_AVAILABILITY_CHANGED` v1

Cambió la cantidad de desafíos obligatorios/opcionales disponibles o completados
de un alumno en una cohorte (#252). Se emite solo si algún contador cambia.

```json
{
  "student_id": "uuid",
  "course_cohort_id": "uuid",
  "mandatory_completed_count": 3,
  "mandatory_available_count": 2,
  "optional_available_count": 1,
  "occurred_at": "2026-10-15T08:30:00Z"
}
```

- La cohorte viaja solo como `course_cohort_id`: este evento nunca tuvo `course_id`.
- Se calcula después del commit del hecho y se encola en su propia transacción
  (`MandatoryAvailabilityWriter`); no sale en la misma transacción que `NODE_COMPLETED`.

### `PARAMETER_CATALOG_DECLARED` v1

Snapshot del catálogo de parámetros dinámicos de Roadmap, publicado al arrancar (#311) y
reenviado cada 30 s mientras Kafka no confirme la entrega, key `T10_ROADMAP`, mismo topic
`roadmap.events`. Todos los intentos de un arranque llevan el mismo `event_id`: un consumidor
puede recibir el evento repetido, igual que con cada arranque o instancia. Contrato propio en el repo:
`docs/contracts/roadmap-parameter-catalog.asyncapi.yaml`. Es un evento **global**: no lleva
`student_id` en el payload ni `organization_id` en el sobre ni en el header, y se publica
directo al arrancar, sin pasar por el outbox. Un consumidor que valide `student_id` u
`organization_id` en todo mensaje de `roadmap.events` lo va a marcar como incompleto: tiene que
exceptuarlo por `event_type`.

## Tipos de evento publicados hoy

| `event_type` | `event_version` | Origen | `organization_id` |
|---|---|---|---|
| `NODE_COMPLETED` | 1 | outbox, misma transacción que el hecho | sí (desde #294) |
| `NODE_UNLOCKED` | 1 | outbox, misma transacción que el hecho | sí (desde #294) |
| `BADGE_AWARDED` | 1 | outbox, misma transacción que el hecho | sí (desde #294) |
| `ROADMAP_MANDATORY_AVAILABILITY_CHANGED` | 1 | outbox, después del commit del hecho | sí (desde #294) |
| `PARAMETER_CATALOG_DECLARED` | 1 | directo al arrancar, con reintento y sin outbox | no (global) |

No existen eventos de subida de nivel, promoción ni abandono: hoy no se publica ninguno con esos nombres.

## Declarados, aún no emitidos

- `COURSE_LEVEL_UP`, `PERFORMANCE_ZONE_CHANGED`: en el catálogo de Roadmap pero
  todavía sin emisión; se publicarán con la misma forma de envelope.

## Lectura de servicio (arranque en frío)

`GET /api/roadmap/courses/{courseId}/progress?page=0&size=50`

- Autoriza: servicio con el scope **`roadmap.progress.read`** (audience
  `roadmap-service`), o usuario `ADMIN`/`PROFESSOR`.
- Respuesta paginada (envelope de plataforma):

```json
{
  "data": {
    "content": [
      { "student_id": "uuid", "course_id": "uuid", "xp_total": 1250,
        "current_lives": 3, "nodes": [ { "node_id": "uuid", "status": "COMPLETED", "block_reason": null } ] }
    ],
    "page": 0, "size": 50, "total_elements": 85, "total_pages": 2
  },
  "message": null, "success": true, "timestamp": "…"
}
```

- `size` se acota a 200. El listado incluye **solo matrículas activas**, en orden
  estable por `student_id`.
- El scope `roadmap.progress.read` se ofrece en el registry de la plataforma
  (`tpi-system-compose`, PR #193).

## Pendiente de confirmación (#360)

### Verificado ejecutando el código (2026-10-28)

- Los eventos `NODE_COMPLETED`, `NODE_UNLOCKED`, `BADGE_AWARDED` y
  `ROADMAP_MANDATORY_AVAILABILITY_CHANGED`, armados con `OutboxService` y las clases de payload
  reales y serializados con el `ObjectMapper` de `Jackson2AutoConfiguration` (la configuración de Spring Boot de la aplicación), tienen exactamente los
  campos de los ejemplos de este documento, en snake_case, con `organization_id` y `producer =
  tema-10-roadmap-service`. `timestamp` y `occurred_at` salen como texto ISO‑8601 UTC
  (`WRITE_DATES_AS_TIMESTAMPS` desactivado); la cohorte viaja como `course_cohort_id` en los cuatro
  y, además, como `course_id` deprecado en los tres primeros.
- `OutboxPoller` publica en `roadmap.events` con key `student_id` y header `organization_id`.
- `PARAMETER_CATALOG_DECLARED` sale con los 6 campos, key `T10_ROADMAP`, sin `organization_id` ni `student_id`.
- Los campos del AsyncAPI para los eventos consumidos (`challenges.events`, `accounting.events`,
  `courses.events`) coinciden con los de los DTOs reales, y los DTOs aceptan un mensaje armado con
  todos los campos del contrato. `organization_id` en el JSON o en el header se acepta; JSON y
  header distintos, o un header que no es UUID, se rechazan sin reintento; un evento consumido sin
  organización falla con error reintentable; los tres eventos globales pasan sin organización.
- El AsyncAPI pasa el parser oficial `@asyncapi/parser` (sin errores) y cada `kafka` binding cumple
  el esquema oficial de bindings Kafka 0.4.0.

### Lo que sigue sin poder verificarse desde el repo

Puntos del pedido de Backoffice (#360) que este contrato no puede cerrar solo con lo que hay en el repo:

- **Publicación en el entorno compartido.** El código publica en `roadmap.events` por defecto
  (`app.kafka.topics.roadmap-events`), pero desde el repo no se puede confirmar qué corre en la
  mesh. Lo confirma quien despliega.
- **Estabilidad de los tipos.** La tabla "Tipos de evento publicados hoy" refleja lo que se emite
  hoy con `event_version` 1. Ningún tipo está declarado estable por contrato: eso lo decide el equipo.
- **`organization_id` en la mesh.** Solo se verificó que `main` (3.0.0) no lo incluye y que
  `develop` (desde #294) sí. Hasta el próximo release, los consumidores aceptan las dos formas
  (con y sin `organization_id`).
- **Reenvío por `POST /api/roadmap/admin/outbox/{eventId}/retry`.** No es un redrive de la DLT:
  reenvía desde el outbox el mismo JSON guardado, con el mismo `event_id` y el mismo `timestamp`
  (ver la fila "Entrega" de la tabla de arriba).
- **Reintentos y DLT por falta de organización.** Que un evento consumido sin `organization_id`
  termine en la DLT después de 3 reintentos es lo que configura el código, pero no se ejecutó
  contra un broker; solo se verificó que la validación lanza el error reintentable.
- **Subida de nivel, promoción y abandono.** Esos eventos no existen: hoy no se publica ninguno
  con esos nombres (ver "Declarados, aún no emitidos" para `COURSE_LEVEL_UP` y
  `PERFORMANCE_ZONE_CHANGED`).

## Firma

| Equipo | Responsable | Fecha | Aprobación |
|---|---|---|---|
| Roadmap (Tema 10) | — | 2026‑10‑11 | ✅ schema y endpoint implementados |
| Backoffice (Tema 12) | — | — | Pendiente |
