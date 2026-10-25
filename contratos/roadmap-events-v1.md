# Contrato de eventos de Roadmap — `roadmap.events` v1

Respuesta a la solicitud del Tema 12 (Backoffice) —issue #134— para el panel
docente y el seguimiento de alumnos. Roadmap **publica** estos hechos; Backoffice
los consume y construye su read model.

| Dato | Valor |
|---|---|
| Topic | `roadmap.events` (DLT `roadmap.events.DLT`) |
| Producer | `tema-10-roadmap-service` |
| Key | `student_id` (UUID como string) |
| Envelope | 6 campos en snake_case (contratos-kafka v8): `event_id`, `event_type`, `event_version` (entero, siempre `1`), `timestamp`, `producer`, `payload`. Sin alias camelCase |
| `timestamp` | ISO‑8601 UTC del **hecho** (no del encolado) |
| Entrega | At‑least‑once. Idempotencia por `event_id` (un duplicado no reproyecta) |
| Orden | Solo dentro de una partición; la key es `student_id` |

## Frescura

Los eventos se encolan en la **misma transacción** del hecho (tabla `outbox_event`)
y el `OutboxPoller` los publica cada ~3 s. El SLA se mide desde el `timestamp`
del envelope.

## Eventos publicados

### `NODE_COMPLETED` v1

Un alumno superó un nodo del roadmap (desafío o contenido).

```json
{
  "course_id": "uuid (courseCohortId)",
  "student_id": "uuid",
  "node_id": "uuid",
  "challenge_id": "uuid",
  "section_id": "uuid"
}
```

- `course_id` es **el `courseCohortId`** (la cohorte), no el curso base.
- El **XP no viaja** en el evento: Roadmap no lo calcula. Para el XP acumulado
  usar `GET /api/roadmap/courses/{courseId}/students/{studentId}/progress` (`xp_total`).
- `challenge_id` puede ser `null` en nodos que no son desafío.

### `NODE_UNLOCKED` v1

Un nodo pasó a estar habilitado para el alumno.

```json
{
  "course_id": "uuid (courseCohortId)",
  "student_id": "uuid",
  "node_id": "uuid"
}
```

### `BADGE_AWARDED` v1

Un alumno obtuvo una insignia (HU‑21).

```json
{
  "course_id": "uuid (courseCohortId)",
  "student_id": "uuid",
  "badge_id": "uuid"
}
```

## Declarados, aún no emitidos

- `COURSE_LEVEL_UP`, `PERFORMANCE_ZONE_CHANGED`: figuran como idea en el pedido de Backoffice, pero
  **el código de Roadmap no los define ni los emite**. No hay fecha; si se implementan se publicarán
  con el mismo envelope y se agregarán a este contrato antes de salir.

## Varios roadmaps por curso

Un curso puede tener más de un roadmap. Los eventos **no incluyen `roadmap_id`**: identifican al
alumno, la cohorte y el nodo (`node_id` es único, así que alcanza para ubicar el roadmap).
El XP no viaja en el evento (ver arriba).

## Lectura de servicio (arranque en frío)

`GET /api/roadmap/courses/{courseId}/progress?page=0&size=50`
(del roadmap principal del curso; para otro roadmap: `GET /api/roadmap/roadmaps/{roadmapId}/progress`)

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

## Firma

| Equipo | Responsable | Fecha | Aprobación |
|---|---|---|---|
| Roadmap (Tema 10) | — | 2026‑10‑11 | ✅ schema y endpoint implementados |
| Backoffice (Tema 12) | — | — | Pendiente |
