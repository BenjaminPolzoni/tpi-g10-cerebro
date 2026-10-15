---
tags: [tpi, g10, acuerdo, notificaciones, bus, kafka, g02]
fecha: 2026-09-24
grupos: [G10, G02]
estado: propuesto  # borrador sin acta (P-09); el wire v8 se usa en la práctica
contrato: "contratos/bus-notificaciones.md"
---

# Acuerdo con Notificaciones / bus de eventos (G02): envelope, topics y claves

> [!info] Fuentes
> - `contratos/bus-notificaciones.md`: **borrador, sin acta** (pendiente P-09).
> - `contratos/KAFKA_EVENT_STANDARD (1).md`: estándar común del bus, **versión anterior** (camelCase, `eventType` con guiones). Reemplazado en la práctica por `contratos-kafka` v8.
> - `contratos/KAFKA.pdf`: PDF del bus.
> - `contratos/roadmap-service.asyncapi.yaml`: AsyncAPI 2.6 de Roadmap.
> - `tareas/T-191-KAFKA-V8-CUTOVER.md`, `tareas/T-01-12-5-OUTBOX.md`.
> - Contraparte: `2026-P4-BE/tpi-notifications` → `docs/contratos-kafka.md`.

## Qué se acordó
- **Está prohibido crear topics** desde un micro; el broker lo aprovisiona la plataforma (Tema 11) y no hay `auto.create.topics`. Se usa **un topic por dominio** (`<dominio>.events`) y el `eventType` discrimina el hecho.
- **Sobre obligatorio de 6 campos:** `event_id`, `event_type`, `event_version` (entero, `1`), `timestamp` (ISO-8601 UTC del hecho), `producer`, `payload`. Desde `contratos-kafka` v8 todo va en `snake_case`. Ver [[decisiones/DEC-001-wire-kafka-v8-snake-case|DEC-001]].
- Mensajes en JSON plano (`StringSerializer`/`StringDeserializer`), `acks=all` en el productor, `enable.auto.commit=false`, ack manual.
- Consumer group propio: **`tema-10-roadmap-service-group`**. Producer: **`tema-10-roadmap-service`** (property `app.kafka.producer`, nunca `spring.application.name`).
- Resiliencia documentada por el bus: 3 reintentos fijos de 2 s y derivación a `<topic>.DLT`. Roadmap no tiene DLQ única: lo no reintentable va a la DLT del dominio origen.
- Todo evento propio sale por **outbox transaccional**, key = `studentId`. Ver [[decisiones/DEC-002-outbox-transaccional-eventos-salientes|DEC-002]].
- No se emite `xp.otorgado`: nadie lo consume.

## Quién lo acordó
- G10: equipo Roadmap.
- G02: equipo Notificaciones, dueño del envelope y del contrato `contratos-kafka` (Grupo 2, según `motor-desafios.md`).
- **No hay acta** firmada de Roadmap con Notificaciones (el propio documento figura como borrador).

## Contrato técnico

### Matriz de topics (Roadmap)
| Topic | Dirección | `event_type` | Contraparte | Estado |
|---|---|---|---|---|
| `challenges.events` | consume | `CHALLENGE_COMPLETED`, `CHALLENGE_ABORTED` | [[acuerdos/motor-desafios-g09\|Motor G09]] | vigente (v8) |
| `courses.events` | consume | `STUDENT_ENROLLED`, `STUDENT_UNENROLLED`, `COURSE_COHORT_ARCHIVED` | [[acuerdos/courses-g01\|Courses G01]] | vigente |
| `administration.events` | consume | `GLOBAL_CONFIGURATION_CHANGED` (key `param_key`) | [[acuerdos/backoffice\|Backoffice]] | vigente; payload v8 por confirmar |
| `accounting.events` | consume | `LIFE_CREDITED`, `LIFE_DEBITED` | [[acuerdos/accounting\|Accounting]] | vigente; payload camelCase (deuda) |
| `accounting.ledger.events` | acordado | `LIVES_EXHAUSTED`, `LIVES_AVAILABLE` | Accounting | sin consumidor en código |
| `roadmap.events` | publica | `NODE_COMPLETED`, `NODE_UNLOCKED`, `BADGE_AWARDED` | Backoffice, Notificaciones, Gamificación, Accounting | **default `roadmap.events`** desde `#134` (2026-10-11); DLT `roadmap.events.DLT` |
| `challenges.results` | consumía (v1/v2) | `ATTEMPT_CORRECTED`/`ATTEMPT_CANCELED` | G09 | **caído**: no existe en el broker; listener apagado por defecto |

### Eventos que publicamos (`roadmap.events`)
- `NODE_COMPLETED {courseId, studentId, nodeId, challengeId, sectionId}`, `NODE_UNLOCKED {courseId, studentId, nodeId}`, `BADGE_AWARDED {courseId, studentId, badgeId}`. `courseId` = `courseCohortId`.
- Previstos pero **sin emisión**: `COURSE_LEVEL_UP {newLevel, totalXp}`, `PERFORMANCE_ZONE_CHANGED {previousZone, currentZone}` (vocabulario `P90/MIDDLE/P10`, solo con >= 10 inscriptos).
- Entrega at-least-once; el `event_id` queda fijo en cada reintento (se serializa el sobre al encolar). Estados `PENDING/PUBLISHED/FAILED` (5 intentos); `FAILED` actúa de DLQ del productor.
- Frescura: poller cada 3 s; el SLA se mide desde `timestamp`.

### Clasificación de errores del consumidor (`KafkaConsumerConfig`)
| Situación | Acción |
|---|---|
| Sobre incompleto, JSON ilegible, UUID malformado, camelCase de v8 | poison pill: `WARN`/DLT, el offset avanza |
| `event_type` desconocido | `INFO`, el offset avanza |
| Alumno no matriculado, nodo/desafío ajeno | `NonRetryableEventException`, log + DLT |
| `event_id` ya registrado | no-op (idempotencia) |
| BD caída, timeout | reintento con `ExponentialBackOff`, luego DLT |

## Impacto en nuestro código
- `events/EventEnvelope`, `EventParser`, `KafkaConsumerConfig`, `RoadmapEventListener`, `CoursesLifecycleEventListener`, `ParRefreshListener`, `lives/AccountingEventsListener`.
- `events/outbox/*`: `OutboxService` (`Propagation.MANDATORY`), `OutboxPoller` (`FOR UPDATE SKIP LOCKED`), `OutboxProperties`.
- Migración `V15__outbox_event.sql`; `application.properties` (`app.kafka.*`, `app.outbox.*`).
- `docs/T-191-KAFKA-V8-CUTOVER.md`: runbook de corte del outbox (drenar `PENDING`, lag a cero, desplegar).

## Pendiente / próximos pasos
- [ ] **`event_version` en el sobre del Motor**: contradice la regla "sin `eventVersion`" de §1; abierto con Notificaciones (no se decide unilateralmente).
- [ ] Confirmar con **Gamificación, Accounting y Notificaciones** que consumen `roadmap.events` en v8 (pendiente declarado en `T-191`).
- [ ] Acta de Roadmap con Notificaciones: topics de salida, key `studentId`, política de DLQ (P5, P8, P9, P11-13).
- [ ] Si Courses publica eventos de sección/actividad, definir `event_type`, payload y key (¿`courseId` = `courseCohortId`?).
- [ ] Regenerar `roadmap-service.asyncapi.yaml` a v8 y actualizar el texto de Taiga HT-11 (dice camelCase).
- [ ] Borrar el listener legado v1/v2 y su flag.
- [ ] `ITEM_EQUIP_*`: la tabla lo ubica en `accounting.holds.events` y el acta de Accounting en `accounting.inventory.commands`.
- [ ] Emitir `COURSE_LEVEL_UP` y `PERFORMANCE_ZONE_CHANGED`.

> [!warning] Riesgos
> - Sin ventana de convivencia v3/v8: un productor que siga en camelCase se pierde en la DLT. Rollback exige drenar el outbox a la inversa.
> - Eventos `PENDING` en `outbox_event` anteriores al corte quedan en camelCase y un consumidor v8 los descarta.
> - La rama `origin/feature/t-21-7-roadmap-events-topic` (`412d74b`, "publicar outbox en roadmap.events por defecto") figura sin mergear, pero `origin/develop` ya trae ese default (`#134`, `e1e0962`).

> [!question] Verificar
> La auditoría de Sprint 3 dice que `KAFKA_TOPIC_ROADMAP` viene vacío; en `origin/develop` el default es `roadmap.events`. Confirmar el valor real en el compose de cada entorno.

## Historial
- 2026-09-24: borrador `bus-notificaciones.md` (preguntas P1 a P13).
- 2026-09-26: outbox transaccional (T-01.12.5), topic vacío por defecto.
- 2026-10-03/04: `BADGE_AWARDED` en el outbox (T-21.2).
- 2026-10-11: `roadmap.events` con default y progreso agregado (`#134`).
- 2026-10-12: migración a `contratos-kafka` v8 snake_case (PR #191).
- 2026-10-14: nota creada desde `origin/develop` (`57ff06a`).
- 2026-10-15: Kafka lo lleva el equipo de Notificaciones (G11 en [[sprints/sprint-3/08-dudas|08-dudas]]). Sigue abierto si algún entorno pisa `KAFKA_TOPIC_ROADMAP` (E6).
