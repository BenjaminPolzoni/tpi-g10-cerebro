# T-15.4 — Evaluación de no_inscripto, sin_vidas y recuperación

## Alcance

> Verifica matrícula; 0 vidas bloquea salvo desafío de recuperación (RF-REC-04) y desafíos LLM;
> el alumno bloqueado ve existencia y condición, nunca contenido.

Cubre CA3 (`not_enrolled`) y CA4 (`no_lives`, salvo recuperación o LLM) de HU-15, y los escenarios
BDD 3 y 5. El orden del gate definido en T-15.1 no cambia.

## Política de vidas del nodo

**Desactualizado y corregido (2026-09-27):** esta sección decía que el Motor no distinguía
desafíos de recuperación ni LLM. Ya no es así: `docs/contracts/motor-desafios-evento-cierre.md`
confirma que el Motor manda `challenge_type` (`NORMAL`/`LIVES`/`LLM`) separado de `content_type`
(`THEORETICAL`/`PRACTICAL`). Aun así, ese dato llega **al cerrar el intento**, y el Gate decide
**antes** de que exista intento: `LivesPolicy` sigue siendo dato propio de Roadmap, cargado por
el profesor en el nodo, porque el Gate no tiene otra fuente en ese momento.

`models/LivesPolicy` reemplaza al booleano `lifeRecovery`:

| Valor | Significado | ¿Exige vidas libres? |
|---|---|---|
| `STANDARD` | Desafío común (default) | Sí |
| `RECOVERY` | Recuperación de vida (RF-REC-04) | No |
| `LLM` | Desafío LLM | No |

- Migración `V14__node_lives_policy.sql`: `life_recovery = true` en un desafío pasa a `RECOVERY`;
  el resto queda `STANDARD`. La columna vieja se elimina.
- API del editor: el campo JSON `lifeRecovery` pasa a ser `livesPolicy`. En el alta y el `PUT`,
  si no viene, vale `STANDARD`; en el `PATCH`, si no viene, se conserva el valor.
- Solo un desafío (teórico o práctico) puede tener una política distinta de `STANDARD`. Si no,
  responde `400 node.lives-policy-requires-challenge`, también cuando un `PATCH` cambia el tipo.
- `ProgressService.startChallenge` usa la misma regla (`exemptFromLivesCheck()`), así el inicio
  y el gate no se desincronizan.

## Vidas libres

Accounting devuelve `currentLives` y `reservedLives` (vidas retenidas por intentos abiertos).
`StudentLives.hasLives()` exige **vidas libres**: `currentLives - reservedLives > 0`. Un
alumno con todas sus vidas reservadas no puede abrir otro desafío común.

- El doble `InMemoryInventoryClient` no simula intentos abiertos: siempre informa 0 reservadas.
  (Nota T-09.5: doble histórico, eliminado en #4354.)
- **T-03.2** implementó el cliente HTTP y mapea `currentLives`/`reservedLives` desde Accounting a
  `StudentLives`; T-15.2 consume ese puerto sin conocer el transporte.

Un nodo `RECOVERY` o `LLM` no consulta a Inventario: se evalúa la política **antes** de pedir
vidas. Es una llamada externa menos (ayuda al P95) y hace que la caída de Inventario no bloquee
esos desafíos.

## Proyección `recovery_pending` (informativa)

El consumidor de los movimientos de vidas de Accounting (`LIFE_CREDITED` /
`LIFE_DEBITED` en `accounting.events`, `AccountingEventsListener`) guarda en
`student_course.recovery_pending` (migración `V24`) si el alumno quedó sin vidas
libres: relee `InventoryClient.fetchLives(courseId, studentId)` y escribe
`!lives.hasLives()`. Es absoluto e idempotente (no acumula ni depende del orden)
y omite al alumno sin matrícula. Si Accounting no responde, conserva el valor
previo y loguea; el evento se confirma igual.

El flag es **de solo lectura informativa** y se expone en el progreso del alumno
(`ProgressDtos.StudentProgress.recovery_pending`): **no** participa del orden del
Gate ni de la elegibilidad. El Gate y `startChallenge` siguen leyendo las vidas
directo de Accounting (`StudentLives.hasLives()`); un `recovery_pending = true`
no bloquea por sí solo, ni un `false` habilita por sí solo.

## Matrícula

`not_enrolled` se evalúa contra `student_course` con matrícula **activa** en **el mismo**
curso-cohorte. Se agregaron tests para la matrícula inactiva, para la matrícula en otro curso y
para la precedencia (`not_enrolled` gana sobre `no_lives`).

A partir de la integración con Courses (`2026-P4-BE/tpi-course`), `student_course` se puebla y actualiza
automáticamente en producción mediante los eventos de dominio de Kafka en el topic `courses.events`
(consumidos por `CoursesEventListener`):
- `STUDENT_ENROLLED`: realiza un upsert de la matrícula marcando `active = true` (e inicializando vidas a 3 y XP en 0).
- `STUDENT_UNENROLLED`: marca la matrícula como inactiva (`active = false`), impidiendo que el alumno no matriculado acceda a los nodos.
- De forma complementaria, Courses expone `GET /api/course/course-cohorts/{courseCohortId}/membership` para validar síncronamente si un usuario pertenece a la cohorte con rol `STUDENT` (`canRead = true`, `canWrite = false`).

Los datos de matrícula sembrados quedan restringidos únicamente a tests y entornos locales.

## Existencia y condición, nunca contenido

Dentro del envelope global, `data` contiene solo `{eligible, reason}`: ningún dato del nodo. Un
test verifica que la decisión bloqueada no expone más campos. El detalle de un nodo bloqueado para
el alumno ya lo cubre `NodeDetailService` con la vista `locked` (HU-05).

## Pendientes fuera de T-15.4

- **Contrato del Gate**: T-15.5 fija el GET por nodo, el envelope y cinco razones de Sprint 1 en
  `docs/contracts/roadmap-motor-gate-v1.md`.
- **Degradación**: T-03.2 implementó caché vigente y error técnico 503. El valor histórico
  `origen_no_disponible` no pertenece al vocabulario vigente del Gate.
