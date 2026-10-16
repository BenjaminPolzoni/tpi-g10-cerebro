---
tags: [tpi, g10, acuerdo, motor, g09, kafka, gate]
fecha: 2026-09-27
grupos: [G10, G09]
estado: vigente  # evento de cierre v8 y gate v1.3 vigentes; gate v1.4 propuesto (T-31.1); firma nominal del gate pendiente
contrato: "contratos/motor-desafios-evento-cierre.md"
---

# Acuerdo con Motor de Desafíos (G09): evento de cierre, gate y catálogo

> [!info] Fuentes
> | Contrato | Ruta en el cerebro | Estado |
> |---|---|---|
> | Evento de cierre de intento | `contratos/motor-desafios-evento-cierre.md` | **vigente** (v8 snake_case) |
> | Gate de elegibilidad v1.3 | `contratos/roadmap-motor-gate-v1.md` | **vigente** (firma pendiente) |
> | Respuesta de G09 v2 (catálogo §1, gate §4, corrección diferida §5) | `contratos/respuesta-motor-a-roadmap-v2.md` | vigente salvo §2 (evento), que quedó **reemplazado** |
> | Contrato Roadmap-Motor original | `contratos/motor-desafios.md` | **reemplazado** en §1 y buena parte de §4 (historia) |
> | Mensaje original del evento de cierre | `contratos/contrato-evento-motor-v2.md` | **reemplazado** (camelCase, `producer = THEME-02-CHALLENGE-ENGINE`) |
> | Contrato del lado G09 | `2026-P4-BE/tpi-engine-challenge` → `docs/contracts/eventos-bus.md` y `roadmap-eligibility.yaml` | fuente de verdad del Motor |

## Qué se acordó
- **Roadmap no calcula XP.** El Motor calcula `coins`, `xp`, `add_live`, `subtract_live` y `active_item` al cerrar el intento (con los parámetros de Backoffice congelados al abrirlo). Roadmap aplica `resources.xp` **tal cual**, como delta, en un ledger append-only. Ver [[decisiones/DEC-013-roadmap-no-calcula-xp-ledger-idempotente|DEC-013]].
- `add_live`/`subtract_live`/`active_item` **no son de Roadmap**: son de [[acuerdos/accounting|Accounting]].
- **Un evento por intento cerrado** (`CHALLENGE_COMPLETED` o `CHALLENGE_ABORTED`, misma estructura). `CHALLENGE_ABORTED` nunca mueve recursos.
- **Gate síncrono por pull:** Motor llama a Roadmap antes de crear el intento. `eligible=true` termina la participación de Roadmap; después Motor y Accounting siguen solos (`ATTEMPT_INIT`, reservas). Roadmap no reserva vidas ni ítems ni participa de Hold/Commit/Release.
- Si el gate no responde válido, Motor falla cerrado (`503`, sin intento colgado). Un `403` de Roadmap = alumno no elegible; con `eligible=false` Motor rechaza con `403` y reenvía el `reason` como texto.
- **Roadmap no envía vidas ni ítems a Motor** al iniciar un intento (Accounting es la fuente).
- Catálogo: el desafío vinculado a un nodo debe existir en el Motor; un desafío archivado responde `200` con `status: ARCHIVED` (no `404`).

## Quién lo acordó
- G10: equipo Roadmap.
- G09: equipo Motor de Desafíos (`tpi-engine-challenge`, producer `tema-03-challenges-service`). Respuestas por escrito (`respuesta-motor-a-roadmap-v2.md`, 2026-09-25/27) y por issue (`tpi-engine-challenge#124`, cerrado el 2026-10-09 con su PR #127).
- Firma nominal: **pendiente** (la tabla de aprobación del gate no tiene responsables).

## Contrato técnico

### 1. Evento de cierre (Motor → Roadmap, Kafka)
| Campo | Valor |
|---|---|
| Topic | `challenges.events` (el topic transitorio `challenges.results` **no existe** en el broker) |
| Key | `id_user` |
| Entrega | at-least-once; deduplicar por `event_id` (`uq_xp_movement_event_id`) |
| Filtro | `producer == "tema-03-challenges-service"`; Tema 05 (Practical) comparte el topic |
| Formato | **contratos-kafka v8**: sobre **y** payload en `snake_case`, sin alias. Un camelCase va a la DLT (`challenges.events.DLT`) |
| Consumer group | `tema-10-roadmap-service-group` |

Sobre: `event_id`, `event_type`, `event_version` (=1), `timestamp`, `producer`, `payload`.
Payload: `resources{coins,xp,add_live,subtract_live,active_item[]}`, `id_user`, `id_course`, `id_node`, `id_attempt`, `challenge_id`, `challenge_version`, `challenge_type` (`NORMAL|LIVES|LLM`), `content_type` (`THEORETICAL|PRACTICAL`), `difficulty`, `mandatory`, `performed_by_user_id`, `performed_by_role`, `result{status APPROVED|DISAPPROVE, score, completed_at, late, attempt_number, resolution_time, started_at, submitted_at, approval_threshold, max_attempts, last_attempt, closure_reason, closure_detail}`.

**Resolución del nodo (D-EVCIERRE-02, `ChallengeNodeResolver`):** `id_node` resuelve solo si existe en el roadmap de la cohorte **y** su `challenge_id` coincide. Si no, `WARN` (`error.node.id-hint-mismatch` / `id-hint-unknown`) y fallback por `challenge_id` con cardinalidad estricta: 0 nodos `node.not-found`, 1 nodo ese nodo, 2+ `node.challenge-ambiguous`.

### 2. Gate (Motor → Roadmap, REST)
```http
GET /api/roadmap/courses/{courseId}/students/{studentId}/nodes/{nodeId}/eligibility
```
- Solo **principal de servicio** (`X-Principal-Type: service`, `X-Service-Id`, `X-Service-Scopes`); `studentId` va en el path, no en `X-User-Id`. Roadmap no parsea el JWT. `serviceId` y scope nominales del Motor siguen **sin confirmar**; `tpi-integration.yml` ofrece `roadmap.gate.read`.
- Respuesta (envelope global `data`): `{ "eligible": bool, "reason": string|null, "challenge_id": uuid|null, "attempt_type": "NORMAL|LIVES|LLM" }`. `challenge_id`/`attempt_type` son aditivos (v1.2, HU-48). `attempt_type` sale de `node.livesPolicy`: `STANDARD→NORMAL`, `RECOVERY→LIVES`, `LLM→LLM`.
- Vocabulario cerrado de `reason`: `not_enrolled`, `course_archived`, `group_restricted` (v1.1), `date_restricted` (v1.3), `unit_prerequisite_pending`, `content_not_read`, `prerequisite_pending`, `no_lives`; `origen_no_disponible` en la v1.4 **propuesta**. Retirados: `recovery_pending`, `already_passed`. `unit_prerequisite_pending` el Gate ya lo emitía y faltaba en el acta.
- Orden: `course_archived`, `not_enrolled`, `group_restricted|date_restricted`, `unit_prerequisite_pending`, `content_not_read`, `prerequisite_pending`, `no_lives`.
- Bloqueos funcionales: `200`. Errores: `401`, `403` (principal o nodo no autorizado; `node.unit-unresolved`), `404` (nodo inexistente; también cuenta ausente en Accounting, ver [[acuerdos/inventario|Inventario]]), `502` (rechazo `4xx` de Accounting, [[decisiones/DEC-015-4xx-de-accounting-no-es-indisponibilidad|DEC-015]]) y, hasta la v1.3, `503` Problem Details si Accounting o Courses caen (nunca `no_lives` ni `eligible=true`). En la v1.4 propuesta ([[decisiones/DEC-020-gate-origen-no-disponible-en-vez-de-503|DEC-020]], T-31.1) ese `503` pasa a `200` con `eligible=false` y `reason=origen_no_disponible`.
- Solo lectura e idempotente. Los motivos de comisión/fecha requieren `ROADMAP_BY_GROUP_ENABLED=true`.

### 3. Catálogo y pool (Roadmap → Motor, REST por Gateway)
| Método y ruta | Uso | Auth |
|---|---|---|
| `GET /api/engine-challenge/challenges/{challengeId}` | Existe/estado/tipo del desafío (HU-01) | token de servicio, audience `engine-challenge-service`, scope `challenges.catalog.read` |
| `GET /api/engine-challenge/challenges` (paginado, `pool-size=100`, máx 3 páginas) | Pool de publicados para asignar desafíos y validar autor (HU-47) | ídem |

Roadmap expone `GET /api/roadmap/courses/{courseId}/challenge-pool` (ADMIN, GESTOR o profesor dueño). Desde 2026-10-13 el pool **no filtra por autor para admin/gestor** (`1dbdd81`).

## Impacto en nuestro código
- `events/RoadmapEventListener` (`@KafkaListener` sobre `challenge-events`), `ChallengeClosurePayload`, `ChallengeCompletedPayload`, `ChallengeAbortedPayload`, `EventParser`, `KafkaConsumerConfig` (backoff + DLT).
- `services/ProgressService.recordResult`, `ChallengeNodeResolver`, `BadgeEvaluator` (se evalúa al procesar el cierre).
- `controllers/GateController` -> `GateService` -> `GateEvaluator` (único evaluador; también alimenta `block_reason`).
- `clients/motor/*` (`HttpMotorCatalogClient`, `MotorCatalogProperties`), `ChallengePoolController`, `GraphValidator` (existe/PUBLISHED/autor/tipo, HU-47).
- `common/security/SecurityConfig` + `GatewayHeadersFilter` (el gate admite solo servicio).

## Pendiente / próximos pasos
- [ ] **`id_node`**: G09 debe confirmar (`tpi-engine-challenge#124`) que el Motor siempre manda un `id_node` consistente con el `challenge_id`. Política implementada, ítem abierto.
- [ ] **Gate v1.4 (T-31.1, bloquea su merge):** mandar el acta a G09 y registrar su aprobación de que el Gate deje de devolver `503` por Accounting o Courses caídos y responda `200` con `origen_no_disponible`. Su cliente ya reenvía el `reason` con `eligible=false`; lo que cambia es que ya no recibe ese `503`.
- [ ] G09 debe sumar `unit_prerequisite_pending` y `origen_no_disponible` a `roadmap-eligibility.yaml` y a `RoadmapIneligibilityReason`, y confirmar el `403` de `node.unit-unresolved`. El yaml ya lista los 7 valores de la v1.3 (`develop` `e95adac6`, 2026-10-15; antes eran 5, seguimiento `tpi-engine-challenge#234`).
- [ ] G09 debe tratar el `404 inventory.account-not-found` del gate (hoy su cliente define solo `403` y `503`).
- [ ] `RECOVERY_PENDING` sigue en el enum del Motor (deprecado): confirmar su retiro.
- [ ] `event_version` en el sobre: contradice la regla del PDF del bus; **abierto con Notificaciones** ([[acuerdos/notificaciones-bus|bus]]).
- [ ] Borrar el listener legado v1/v2 (`RoadmapEventListener.onMessage`, payloads `AttemptCorrected`/`AttemptCanceled` y flag `app.kafka.topics.challenge-result.enabled=false`).
- [ ] Re-corrección manual de un intento (¿`xp` total o delta?): un segundo evento con otro `event_id` **suma XP otra vez** (según `motor-desafios.md` §8, pregunta §4.5 sin respuesta registrada); el contrato vigente no lo aclara.
- [ ] HU-48: falta un pre-chequeo que el alumno llame con su JWT (hoy el gate es solo servicio) y se retiró `/start`.
- [ ] Baja/archivado de un desafío ubicado: el Motor no emite evento (HU-01 CA8 sin consumidor).
- [ ] Firma nominal del acta del gate.

> [!warning] Riesgos
> - Si el Motor cambia el string de `producer`, sus eventos se **descartan en silencio** (pasó el 2026-10-05, `tpi-roadmap#120`).
> - `active_item` llega vacío y `late` en `false` por ahora (falta inventario/fecha límite en G09).
> - El asyncapi `roadmap-service.asyncapi.yaml` declara aún `challenges.results` y camelCase (v3): está desactualizado respecto de v8.

## Historial
- 2026-09-24: contrato inicial `motor-desafios.md` (`ATTEMPT_CORRECTED`/`ATTEMPT_CANCELED`).
- 2026-09-26: acta del gate v1.0.
- 2026-09-27: G09 revierte la decisión de v2 y manda `resources`; el evento pasa a `challenges.events` (key `id_user`).
- 2026-10-05/06: `producer` pasa a `tema-03-challenges-service` (`tpi-roadmap#120`).
- 2026-10-09: gate v1.1 (`group_restricted`); G09 cierra `#124`.
- 2026-10-11: gate v1.2 (`challenge_id`, `attempt_type`).
- 2026-10-12: wire v8 snake_case (PR #191); gate v1.3 (`date_restricted`).
- 2026-10-14: nota creada desde `origin/develop` (`57ff06a`).
- 2026-10-15: gate v1.4 propuesto (T-31.1): `origen_no_disponible` en vez de `503`; se documenta `unit_prerequisite_pending`.
- 2026-10-15: respuestas en [[sprints/sprint-3/08-dudas|08-dudas]]: `node_id` único global, también en roadmaps clonados (G8); el profesor configura si el ranking ordena por XP o por notas, y las notas vienen del Motor (P14, falta acordar cómo llegan); "multiple choice con boss fight" es de Desafíos teóricos (P16).
