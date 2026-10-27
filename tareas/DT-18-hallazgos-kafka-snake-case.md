---
tags: [tpi, g10, tarea, deuda-tecnica, kafka, contratos]
fecha: 2026-10-27
estado: resuelta
---

# DT-18 — Contratos Kafka de Roadmap a snake_case (hallazgos)

Referencia: [[deuda-tecnica]] · [[decisiones/DEC-001-wire-kafka-v8-snake-case|DEC-001]] · skill `contratos-kafka` (v12).
Commit en el repo: `9281be3d` (rama `feature/dt-18-kafka-docs-cbd7df`, sin PR). Verificado contra el código de `develop` (`6268b669` + `fea2fece`), leyendo las fuentes en disco: el grafo `codebase-memory-mcp` no estaba disponible en esta sesión.

## Qué se tocó

**Vault (`tpi-g10-cerebro`)**
- `contratos/roadmap-service.asyncapi.yaml`: reescrito (v1.0.0 → v2.0.0), snake_case, canales y payloads según el código.
- `contratos/roadmap-events-v1.md`: payloads y key en snake_case; se agregan `ROADMAP_MANDATORY_AVAILABILITY_CHANGED` y `PARAMETER_CATALOG_DECLARED`.
- `contratos/courses.md` §7.3, §7.5 y tabla de eventos pedidos: payloads de Courses en snake_case.
- `contratos/KAFKA_EVENT_STANDARD (1).md`: campos y `event_type` pasados a snake_case / `SCREAMING_SNAKE_CASE`, con aviso de que manda la skill.
- `contratos/bus-notificaciones.md`, `contratos/accounting-roadmap-v1.md`, `contratos/CONTRATO_T10_BACKOFFICE.md`: ejemplos JSON de eventos y nombres del sobre.
- `arquitectura/contexto-integral.md` §4, `estructura-codigo.md`, `e2e-flujo-completo.md`; `acuerdos/` (backoffice, notificaciones-bus, courses-g01); `microservicios/` 01, 02, 03, 06, 10; `decisiones/DEC-001`.

**Repo (`tpi-roadmap`)**: `README.md`, `AGENTS.md`, `.agents/agent.md`, `docs/faq-notifications-bus.md`.

## Hallazgos doc ↔ código

1. **`COURSE_LEVEL_UP` y `PERFORMANCE_ZONE_CHANGED` no se emiten.** Ningún `outbox.enqueue` los produce (solo `NODE_COMPLETED`, `NODE_UNLOCKED`, `BADGE_AWARDED`, `ROADMAP_MANDATORY_AVAILABILITY_CHANGED`). `AGENTS.md`, `.agents/agent.md`, `microservicios/06` y `10`, y la matriz de `contexto-integral.md` decían que sí. Corregido: figuran como declarados sin emisión.
2. **`ROADMAP_MANDATORY_AVAILABILITY_CHANGED` y `PARAMETER_CATALOG_DECLARED` faltaban** en el asyncapi y en `roadmap-events-v1.md`.
3. **`PAR_STATUS_CHANGED` no existe en el código.** `administration.events` se lee con `GLOBAL_CONFIGURATION_CHANGED` (`ParRefreshListener`, `DynamicParameterListener`) y `PARAMETER_DEFINITION_CREATED`.
4. **`COURSE_ARCHIVED` (ficha 06) es en realidad `COURSE_COHORT_ARCHIVED`.**
5. **`producer`**: los docs mostraban `roadmap-service`; el código emite `tema-10-roadmap-service`. El filtro de `challenges.events` espera `tema-03-challenges-service`.
6. **`challenges.events` consume también `CHALLENGE_ARCHIVED` y `CHALLENGE_RESULT_RECTIFIED`**, que ningún doc listaba.
7. **Courses**: la tabla de §7.5 decía "mismos campos y tipos", pero los payloads de Roadmap leen solo `course_cohort_id` y `student_id`; el resto (`enrollment_id`, `enrolled_at`, …) se ignora. Los nombres snake_case de esos campos no leídos **no se pudieron verificar** contra un evento real de Courses.
8. **`course_id` vs `course_cohort_id`**: `NODE_COMPLETED`, `NODE_UNLOCKED` y `BADGE_AWARDED` llevan la cohorte como `course_id`; `ROADMAP_MANDATORY_AVAILABILITY_CHANGED` la lleva como `course_cohort_id`. Ambos snake_case, pero inconsistentes entre sí. Está documentado tal cual; unificarlo sería un cambio de contrato.
9. **`accounting.ledger.events` (`LIVES_EXHAUSTED`/`LIVES_AVAILABLE`)** figura como consumido en `bus-notificaciones.md` y `contexto-integral.md`, pero el código no tiene listener para ese topic.

## camelCase que quedan en el CÓDIGO (no se tocó, esto es solo docs)

- `ChallengeCompletedPayload` y `ChallengeAbortedPayload` (`events/`): payload camelCase (`attemptId`, `studentId`, `courseId`, `occurredAt`…) del listener v1/v2 de `challenges.results`, que arranca apagado y se borra "el próximo sprint". Documentado como retirado en el asyncapi.
- `AttemptCanceledPayload`/`AttemptCorrectedPayload`: `@JsonAlias("completedAt")`, y el typo heredado `substract_live` (también en snake_case). Mismo listener retirado.
- `LifeMovementPayload`: `@JsonAlias` camelCase (`studentId`, `courseId`, `movementType`) hasta `tpi-accounting#227`. Contradice el "sin alias" de DEC-001, pero DEC-001 ya lo registra como única excepción.
- Comentarios de código y `application.properties` siguen citando `contratos-kafka v3` y `docs/contracts/motor-desafios-evento-cierre.md`, que ya no existe en el repo (vive en el vault: `contratos/motor-desafios-evento-cierre.md`). `application.properties:364` dice que el outbox publica tres eventos; son cuatro.

## Skills del Skill Hub desactualizadas respecto del código

- `challenge-engine-kafka-events` (v1, G09) documenta `eventVersion`, `completedAt`, `startedAt`, `submittedAt` en camelCase y `producer = THEME-02-CHALLENGE-ENGINE`, y dice que la key es `id_user`. El código de Roadmap lee `event_version`, `completed_at`, `started_at`, `submitted_at` y filtra por `tema-03-challenges-service`. Si el Motor publicara tal cual esa skill, Roadmap descartaría el evento por producer y mandaría el sobre a la DLT. Conviene confirmar con G09 cuál es el wire real (la skill tiene una revisión pendiente). Para Roadmap no hay que cambiar nada hasta confirmarlo.
- `snake-case-wire-java` aclara que la regla de `@JsonProperty` es para HTTP y que los payloads Kafka quedan fuera de ella; `contratos-kafka` es la que exige snake_case en Kafka (por eso los payloads de Roadmap declaran `@JsonProperty` en cada campo en vez de una estrategia global).

## No verificado

- Formato exacto de `occurred_at` (Instant serializado por Jackson 3 sin `@JsonFormat`; se documentó ISO-8601 UTC sin correr el productor).
- Que los consumidores de `roadmap.events` (Backoffice, Notificaciones, Gamificación) ya lean snake_case (sigue abierto en DEC-001).
- Texto de la HU-11 en Taiga: vive en Taiga, no en el vault; sigue pendiente (DT-19).
- `mvn verify`: ver el resultado en el informe de la sesión.
