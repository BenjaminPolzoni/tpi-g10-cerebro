---
tags: [tpi, g10, decision, kafka, outbox]
fecha: 2026-09-26
estado: aceptada
reemplaza: ""
---

# DEC-002: Eventos salientes por outbox transaccional

## Contexto
Roadmap debe avisar `NODE_COMPLETED`, `NODE_UNLOCKED` y `BADGE_AWARDED` sin perder eventos ni publicar hechos que luego se reviertan. En ese momento (P-09) la lista oficial del bus no traía un topic de Roadmap y está prohibido crear topics.

## Decisión
Los eventos se **encolan en la misma transacción del hecho** en la tabla `outbox_event` (`OutboxService`, `Propagation.MANDATORY`) y un `OutboxPoller` programado los publica en Kafka (cada ~3 s, lotes de 50, `FOR UPDATE SKIP LOCKED`, 5 intentos). Key del mensaje = `studentId`. Se serializa el **sobre completo** al encolar, así cada reintento reutiliza el mismo `event_id` y los consumidores deduplican (at-least-once). Estado `FAILED` en la tabla actúa de DLQ del productor.

## Alternativas descartadas
- **Topic DLQ propio**: si el broker está caído, tampoco llegaría (D-T01125-04).
- **Publicar directo desde el servicio**: no hay alternativa documentada; el outbox da atomicidad con el ledger y un `event_id` estable por reintento (D-T01125-05).
- **Topic vacío por defecto** (D-T01125-01): al principio las filas quedaban `PENDING` hasta que Notificaciones asignara el topic; reemplazado el 2026-10-11 por el default `roadmap.events` (`#134`).
- **Emitir `NODE_UNLOCKED` en el congelado de reglas** (`freezeReachedUnlocks`): no emite, no hay nada nuevo que avisar (D-T01125-03).

## Consecuencias
- Positivas: sin pérdida de eventos ante caída del broker; orden por alumno; idempotencia por `event_id`.
- Negativas / deuda:
  - Reencolar un `FAILED` es manual (`UPDATE ... status='PENDING', attempts=0`).
  - El `payload` guardado es el sobre completo: un cambio de wire (DLQ/v8) exige drenar el outbox antes (ver [[decisiones/DEC-001-wire-kafka-v8-snake-case|DEC-001]]).
  - `COURSE_LEVEL_UP` y `PERFORMANCE_ZONE_CHANGED` siguen sin emitirse.
  - La rama `feature/t-21-7-roadmap-events-topic` figura sin mergear aunque develop ya trae el default.

## Referencias
- Código / PR / doc: `a8b3ff7` (2026-09-26), migración `V15__outbox_event.sql`, `events/outbox/*`, `BadgeEventService` (`a7ef7f1`, 2026-10-03), `e1e0962` (`#134`, 2026-10-11).
- `tpi-roadmap/docs/T-01-12-5-OUTBOX.md` (D-T01125-01..08), `docs/contracts/roadmap-events-v1.md`, `docs/contracts/bus-notificaciones.md`.
- Relacionadas: [[acuerdos/notificaciones-bus|bus de eventos]], [[acuerdos/backoffice|Backoffice]].
