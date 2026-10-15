# Contrato de eventos de Roadmap — `roadmap.events` v1

Respuesta a la solicitud del Tema 12 (Backoffice) —issue #134— para el panel
docente y el seguimiento de alumnos. Roadmap **publica** estos hechos; Backoffice
los consume y construye su read model.

| Dato | Valor |
|---|---|
| Topic | `roadmap.events` (DLT `roadmap.events.DLT`) |
| Producer | `tema-10-roadmap-service` |
| Key | `studentId` (UUID como string) |
| Envelope | 6 campos: `eventId`, `eventType`, `eventVersion`, `timestamp`, `producer`, `payload` |
| `timestamp` | ISO‑8601 UTC del **hecho** (no del encolado) |
| Entrega | At‑least‑once. Idempotencia por `eventId` (un duplicado no reproyecta) |
| Orden | Solo dentro de una partición; la key es `studentId` |

## Frescura

Los eventos se encolan en la **misma transacción** del hecho (tabla `outbox_event`)
y el `OutboxPoller` los publica cada ~3 s. El SLA se mide desde el `timestamp`
del envelope.

## Eventos publicados

### `NODE_COMPLETED` v1

Un alumno superó un nodo del roadmap (desafío o contenido).

```json
{
  "courseId": "uuid (courseCohortId)",
  "studentId": "uuid",
  "nodeId": "uuid",
  "challengeId": "uuid",
  "sectionId": "uuid"
}
```

- `courseId` es **el `courseCohortId`** (la cohorte), no el curso base.
- El **XP no viaja** en el evento: Roadmap no lo calcula. Para el XP acumulado
  usar `GET /api/roadmap/courses/{courseId}/students/{studentId}/progress` (`xp_total`).
- `challengeId` puede ser `null` en nodos que no son desafío.

### `NODE_UNLOCKED` v1

Un nodo pasó a estar habilitado para el alumno.

```json
{
  "courseId": "uuid (courseCohortId)",
  "studentId": "uuid",
  "nodeId": "uuid"
}
```

### `BADGE_AWARDED` v1

Un alumno obtuvo una insignia (HU‑21).

```json
{
  "courseId": "uuid (courseCohortId)",
  "studentId": "uuid",
  "badgeId": "uuid"
}
```

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

## Firma

| Equipo | Responsable | Fecha | Aprobación |
|---|---|---|---|
| Roadmap (Tema 10) | — | 2026‑10‑11 | ✅ schema y endpoint implementados |
| Backoffice (Tema 12) | — | — | Pendiente |
