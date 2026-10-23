---
tags: [tpi, g10, sprint-3, plan, resolver-issue, back, xp, progreso, ranking, integración, motor]
fecha: 2026-10-23
autor: Benja
responsable: Benja
estado: pendiente - decisiones D1-D5 a responder en la issue
repo: 2026-P4-BE/tpi-roadmap
issue: https://github.com/2026-P4-BE/tpi-roadmap/issues/312
taiga: sin tarea en Taiga
---

# Issue #312 — Consumir `CHALLENGE_RESULT_RECTIFIED`: XP y progreso por rectificación de un intento

> [!todo] Tarea de Benja
> Responder D1-D5 en la #312, implementar el PR 1 (guardar el intento en el cierre) y después el PR 2 (el manejador). Avisar en la issue el nombre de la bandera cuando esté desplegado.

> [!info] Contexto
> Motor (G09, PR tpi-engine-challenge#345) recalcula **sobre el mismo intento** la nota, el veredicto, las monedas y la XP cuando un docente cambia una nota (HU53/HU54 en Teóricos, o un ajuste de la corrección automática en Prácticos). Para avisarlo publica `CHALLENGE_RESULT_RECTIFIED` v1 en `challenges.events`. Esta issue **reemplaza a #307** (cerrada). Contrato adjunto: `Contrato-Roadmap-Motor-rectificacion-v0.2.md`, en el comentario de la issue.
>
> Resuelve la D1 que dejé abierta en [[Back - corrección de XP por recalificación (delta y nivel)]]: Motor manda el **total del intento**, no un delta. También toca la política de [[Back - política de recálculo de nota y progreso monótono]].

## 1. Qué pide la issue

Motor informa `target_experience` (cuánta XP vale el intento ahora). Roadmap la compara con lo que **él** registró para ese intento y asienta la diferencia como movimiento compensatorio en `xp_movement`. Un evento perdido, repetido o fuera de orden no rompe la cuenta.

Payload que nos importa (el resto se ignora): `id_user`, `id_course`, `id_attempt`, `challenge_id`, `result_revision` (≥ 2; el cierre es la 1), `status` (`APPROVED`/`DISAPPROVE`), `score` (entero 0-100) y `target_experience` (entero ≥ 0). **No trae `id_node` ni `attempt_number`.**

Garantías que exige el contrato (§7):
1. Es una rectificación, no un cierre: **no pasa por `recordResult`**.
2. La XP del intento queda en `target_experience`, con el mismo alcance que tuvo el cierre (sección, roadmap, modo curso o `ROADMAP`).
3. Idempotente por `event_id` **y** por `(id_attempt, result_revision)`. Revisión ≤ última aplicada → se ignora; una mayor se aplica aunque salte revisiones. Motor puede reenviar **la misma revisión con otro `event_id`**.
4. El veredicto se compara con el que Roadmap tiene aplicado, nunca con `previous_status`.
5. Intento sin cierre registrado → se ignora con log, sin error.
6. El ranking por notas usa la nota de la última revisión del intento, no la máxima histórica.
7. Sin respuesta a Motor.
8. Bandera encendida en producción (`true` por defecto).

## 2. Estado actual (verificado en `origin/develop` `57e3f13b`)

Rutas relativas a `Backend/tpi-roadmap/src/main/java/com/utn/tpi/roadmap/`.

| Pieza | Hoy | Qué implica |
|---|---|---|
| `events/RoadmapEventListener.onChallengeClosureEvent` | Filtra el productor `tema-03-challenges-service`; atiende `CHALLENGE_COMPLETED`, `CHALLENGE_ABORTED` y `CHALLENGE_ARCHIVED`; **el resto lo loguea con `event.type-unknown` y lo confirma** | Un evento publicado antes de tener el manejador se pierde (por eso Motor espera el aviso) |
| `events/ChallengeClosurePayload` | Recibe `id_attempt`, `id_node` y `result.attempt_number` | `id_attempt` **no se guarda en ningún lado** |
| `services/ProgressService.recordResult` | Lock de `student_course`, idempotencia por `event_id`, inserta el movimiento, `addXp`, completa el nodo, `NODE_COMPLETED`/`NODE_UNLOCKED`, desbloqueos por XP, insignias y `mandatoryAvailability.request` | La issue dice que lanza `node.already-passed`: **está desactualizada**. Desde #270 (V62) un nodo ya aprobado se registra con XP 0 y `post_pass_repeat = true`, sin error |
| `entities/XpMovementEntity` | Append-only, `event_id` único (`uq_xp_movement_event_id`), `xp` sin restricción de signo, `score`, `post_pass_repeat`, `section_id`, `roadmap_id`, `counted_in_course` | Faltan `id_attempt`, `result_revision`, `status`, y para D3 también nodo y número de intento |
| `models/StudentCourse.addXp` | Suma sin validar signo | Un delta negativo ya funciona |
| `LevelService` | Nivel calculado al leer desde `total_xp` | Con delta negativo el nivel baja solo |
| `repositories/XpMovementRepository.findAverageBestScoresByStudent` (usado en `RankingService:174`) | `MAX(score)` por alumno y desafío, sin `post_pass_repeat` | Hay que cambiarlo (garantía 6) |
| `lastXpAtByStudentInCourse/InRoadmap` (`RankingService:210`, desempate `reached_first` de T-45.18) | Último `recorded_at` con `xp <> 0` | Un compensatorio con XP ≠ 0 mueve el desempate. Motor sugiere dejarlo así |
| `sumXp` / `sumXpByStudent` (modo `ROADMAP`) | Suma del ledger | Funciona solo con el compensatorio, sin tocar nada |
| `dashboard/CohortSummaryService:131` (`findStudentIdsWithMovementSince`, #326) | Cualquier movimiento cuenta como alumno activo | **Una rectificación la hace el docente**: contaría al alumno como activo (D5) |
| `dashboard/XpTimelineService:62` | Suma la XP por semana | El delta negativo resta en la semana de la rectificación. Es coherente (XP neta) |
| `services/BadgeEvaluator` | `NODE_NO_RETRIES` usa `passed && attemptNumber == 1` | Para D3 hay que guardar el número de intento desde el cierre |
| `logUnknownFields` | WARN por cada campo no declarado | Con ~16 campos ignorados llenaría el log: hay que declararlos o ignorarlos |
| Última migración | `V65__xp_movement_course_recorded_idx.sql` | La nueva es **V66** |
| Banderas | Convención `app.features.<x>.enabled=${ENV:...}` | Propuesta: `app.features.rectification.enabled=${RECTIFICATION_ENABLED:true}` |

**Front (`2026-PIV-TPI-FE`, `origin/develop` `c5615d213`):** no hace falta cambiar nada. El front lee `total_xp`, el nivel y el ranking ya calculados por el back (`roadmap-mapper.ts`, `level-hud`, `course-roadmap-progress.service.ts`, `ranking-mapper.ts`), y no hay lógica que suponga que la XP solo sube. La rectificación la dispara G04 o Motor desde su pantalla (los textos `annulItemMessage`/`annulAttemptMessage` del i18n). Al front le toca **solo prueba manual**: que la XP o el nivel bajen y la barra de nivel se vea bien, y que el puesto en el ranking por notas cambie.

## 3. Decisiones a responder en la #312

Motor propone defaults; si no objetamos, quedan acordados.

| # | Pregunta | Default de Motor | Mi recomendación |
|---|---|---|---|
| D1 | Aprobado → desaprobado: ¿qué pasa con el nodo completado, los desbloqueos y el `NODE_COMPLETED` ya publicado? | No revertir nada; solo XP y nota | **Aceptar.** Coincide con el progreso monótono que ya propuse. La XP sí baja a 0 (un desaprobado vale 0) |
| D2 | Con delta negativo, ¿no se vuelve a bloquear nodos ni se quitan insignias? | Sí | **Aceptar**, y aceptar que el nivel baje. Cambia lo que recomendé el 22/10 («la XP solo sube»): con el modelo de total, un piso en 0 haría que Roadmap y Motor no coincidan para siempre |
| D3 | Desaprobado → aprobado: ¿se completa el nodo y se desbloquea como en un cierre? | Sí, si no lo completó otro intento | **Aceptar.** Hace falta guardar el nodo y el número de intento en el cierre (la rectificación no los trae) |
| D4 | Desaprobado → aprobado cuando **otro intento ya completó el nodo** | Acreditar la XP del intento rectificado | **Objetar.** El intento posterior ya cobró la XP completa en Roadmap (en ese momento el nodo no estaba aprobado), así que acreditar los dos paga el nodo dos veces. Propongo la regla de #270: un nodo se paga una vez; la XP esperada del rectificado es 0 y solo se actualiza su nota |
| D5 | ¿La rectificación cuenta como actividad del alumno en el dashboard de cohorte (#309)? | — (no lo menciona) | **No.** Excluir `result_revision > 1` en `findStudentIdsWithMovementSince`. El desempate `reached_first` lo dejamos como sugiere Motor |

También: nombre de la bandera = `app.features.rectification.enabled` (env `RECTIFICATION_ENABLED`, `true` por defecto). Ranking por la nota de la última revisión = **sí**.

## 4. Plan de implementación

### PR 1 — Guardar el intento en el cierre (se puede hacer ya; Motor pide que salga primero)

1. **Migración `V66__xp_movement_attempt.sql`**: columnas nullable `id_attempt UUID`, `result_revision INT`, `status VARCHAR(16)`, `node_id UUID` y `attempt_number INT`. Índice único `uq_xp_movement_attempt_revision (id_attempt, result_revision)`; los `NULL` de los datos viejos no chocan ni en Postgres ni en H2. Índice simple por `id_attempt` si el único no alcanza para las búsquedas.
2. **`XpMovementEntity`**: los cinco campos.
3. **`ChallengeResult` (`dtos/ProgressDtos`)**: agregar `attemptId` y `status`. En el cierre se completan desde `ChallengeClosurePayload` (`attemptId()`, `result().status()`). Los caminos v1/v2 apagados pasan `null`.
4. **`ProgressService.insertMovement`**: guardar `id_attempt`, `result_revision = 1`, `status`, `node_id` (el resuelto) y `attempt_number`. También para la repetición de un nodo aprobado (`post_pass_repeat`).
5. **`isEventIdConstraintViolation`**: tratar también `uq_xp_movement_attempt_revision` como duplicado (contrato §9).
6. **Tests**: el cierre guarda los campos nuevos (`ProgressServiceTest`) y la migración corre en H2.

### PR 2 — Manejador de la rectificación (detrás de la bandera)

1. **`events/ChallengeResultRectifiedPayload`** (record): los 8 campos más los 16 que se ignoran, declarados con `@JsonIgnoreProperties` para que `logUnknownFields` no emita WARN por ellos. `isComplete()` exige los 8 campos, `score` entre 0 y 100, `result_revision ≥ 2` y `target_experience ≥ 0`. Si falla → `NonRetryableEventException` (a la DLT).
2. **Listener**: rama `CHALLENGE_RESULT_RECTIFIED` en `onChallengeClosureEvent`. Con la bandera apagada → log y confirmar. Llama a `progressService.applyRectification(eventId, payload)`. Una `DuplicateEventException` se loguea en debug, igual que el cierre.
3. **`ProgressService.applyRectification`** (`@Transactional`, sin pasar por `recordResult`):
   1. Si `existsByEventId` → ignorar.
   2. Lock de `student_course` (`findWithLockByCourseCohortIdAndStudentId`). Si no está inscripto → ignorar con log, sin error (garantía 5).
   3. Volver a chequear `existsByEventId`, como el cierre.
   4. `movements.findByAttemptId(id_attempt)`. Si está vacío → ignorar con log (garantía 5).
   5. Si `result_revision ≤ MAX(result_revision)` del intento → ignorar (garantía 3; cubre el reenvío con otro `event_id`).
   6. `closure` = el movimiento con revisión 1; `last` = el de la revisión más alta.
   7. **XP esperada**: `target_experience`, salvo que `closure.postPassRepeat` sea verdadero o se dé el caso de D4; en esos casos es 0. `delta = esperada − SUM(xp del intento)`.
   8. Insertar el movimiento con `event_id`, `id_attempt`, `result_revision`, `status`, `score`, `xp = delta` (puede ser 0 o negativo), y con `section_id`, `roadmap_id`, `counted_in_course`, `post_pass_repeat`, `node_id`, `attempt_number` y `challenge_id` **copiados del cierre**.
   9. Si `counted_in_course` → `StudentCourse.addXp(delta)`.
   10. **Veredicto** contra `last.status`:
       - `DISAPPROVE → APPROVED` y el nodo no está en `completed_node` → hacer lo mismo que el cierre: `completed_node`, `activityDays.registerNow`, `NODE_COMPLETED` y `recordUnlocksAfter`. Extraer ese bloque de `recordResult` a un método privado compartido (`completeNode`), sin cambiar su comportamiento.
       - `APPROVED → DISAPPROVE` → nada más (D1).
   11. Si `delta > 0` → `recordXpUnlocks` con el mismo `XpScope` que arma el cierre.
   12. Si hubo `delta > 0` o completado → `badgeEvaluator.awardEarned(..., closure.attemptNumber, aprobadoAhora)`.
   13. `mandatoryAvailability.request` (ya corre después del commit).
4. **Ranking por notas** (`findAverageBestScoresByStudent`): en el subselect, quedarse con la fila de mayor `result_revision` de cada intento antes del `MAX` por desafío. Por ejemplo, `AND (id_attempt IS NULL OR result_revision = (SELECT MAX(r.result_revision) FROM xp_movement r WHERE r.id_attempt = m.id_attempt AND r.deleted_at IS NULL))`. SQL portable a H2 y Postgres. Los datos viejos sin intento siguen igual.
5. **Dashboard (D5)**: en `findStudentIdsWithMovementSince`, `AND (m.resultRevision IS NULL OR m.resultRevision = 1)`.
6. **Bandera** en `application.properties`: `app.features.rectification.enabled=${RECTIFICATION_ENABLED:true}`, con comentario como las demás.
7. **`messages.properties`**: claves para «rectificación sin cierre registrado», «revisión vieja», «aplicada (delta X)» y «bandera apagada».
8. **Tests** (`ProgressServiceRectificationTest` y el test del listener). Solo los pertinentes, sin la suite completa:
   - XP sube y baja sin cambio de veredicto; delta 0 que igual avanza la revisión.
   - Desaprobado → aprobado: nodo completado, `NODE_COMPLETED`, desbloqueos, e insignia `NODE_NO_RETRIES` si fue el intento 1.
   - Desaprobado → aprobado con el nodo ya completado por otro intento (D4).
   - Aprobado → desaprobado: XP a 0 y nodo intacto.
   - Mismo `event_id` dos veces; misma revisión con otro `event_id`; revisión vieja; salto de revisiones (2 → 4).
   - Intento sin cierre registrado: se ignora sin excepción.
   - Repetición de un nodo ya aprobado: XP 0 y fuera del ranking.
   - Modo `ROADMAP`: `total_xp` intacto y `sumXp` del roadmap ajustado.
   - Ranking por notas: baja la nota y baja el promedio.
   - Bandera apagada: se confirma y se ignora. Payload inválido (nota nula o fuera de rango) → `NonRetryableEventException`.
9. `mvn verify` (Checkstyle, PMD y CPD) en verde antes del PR.

### Después del merge

- Avisar en la #312 que está desplegado con la bandera encendida, para que Motor active la publicación.
- Prueba conjunta con G09 (contrato §13): un teórico y un práctico.
- Front: prueba manual de la barra de nivel y del ranking por notas con una rectificación que baje la XP.
- Actualizar [[acuerdos/motor-desafios-g09]] con el evento nuevo y las decisiones D1-D5, y marcar como superados los planes del 22/10 que esta issue resuelve.

## 5. Fuera de alcance

- `CHALLENGE_REVERSED`: Roadmap no lo consume (contrato §8).
- Revertir el progreso (descompletar nodos, re-bloquear o quitar insignias): ver la sección 4 de [[Back - política de recálculo de nota y progreso monótono]].
- Exponer los campos nuevos en `XpHistoryController` (endpoint de depuración): se agregan solo si alguien los pide.
- Borrar el listener v1/v2 apagado (deuda aparte).

## 6. Riesgos

- **Cierres anteriores al PR 1** no tienen `id_attempt` y sus rectificaciones se ignoran. Motor dice que va a vaciar las bases antes de habilitar.
- **Evento en la DLT**: el intento queda sin corregir hasta reprocesarlo o hasta la siguiente rectificación (el modelo de total lo repara).
- **D4**: si Motor no acepta la objeción, Roadmap y Motor no van a coincidir en la XP en ese caso. Hay que dejarlo escrito en el acuerdo.
