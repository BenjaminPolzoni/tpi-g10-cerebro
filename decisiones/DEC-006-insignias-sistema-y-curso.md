---
tags: [tpi, g10, decision, insignias, gamificacion]
fecha: 2026-10-03
estado: aceptada
reemplaza: ""
---

# DEC-006: Dos orígenes de insignias, las del sistema y las del curso

## Contexto
El front trabajaba con insignias fijas (semilla) y el profesor necesita crear las suyas por cohorte. HU-20 a 22 piden catálogo, otorgamiento y vista del alumno, con un catálogo coherente entre entornos.

## Decisión
`badge` distingue `origin`: **`SYSTEM`** (12 insignias fijas, globales, sin cohorte, con IDs fijos `b0d6e000-0000-4000-8000-000000000001` a `...000012` y criterios definidos por el equipo el 2026-10-03) y **`TEACHER`** (creadas por el profesor para su cohorte, siempre con `course_cohort_id`). `BadgeType`: `CROSS_CUTTING` o `PER_NODE` (exige `node_id`). Los 10 criterios (`BadgeCriterion`) aprobados por el PO mantienen los nombres del front. Cada alumno recibe una insignia una sola vez (`uq_badge_award_student_badge`, que cuenta también las dadas de baja), el otorgamiento corre al final de `recordResult` con la fila del alumno bloqueada y encola `BADGE_AWARDED` en el outbox. La vista del alumno une las del sistema más las propias de la cohorte (ganadas y pendientes).

## Alternativas descartadas
- **Insignias del sistema con nodo (Boss, Evento)**: quedaron afuera; una insignia global no puede apuntar a un nodo de un curso (comentario de `V17`).
- **Sembrar IDs aleatorios por entorno**: los IDs son fijos para ser iguales en todos los entornos y la clave primaria impide duplicarlas.

## Consecuencias
- Positivas: catálogo estable más personalización por curso; idempotente ante replays (BDD T-21.4).
- Negativas / deuda:
  - Tres criterios del catálogo **nunca se otorgan** (`SECTION_NO_LIVES_LOST`, `NODE_NO_RETRIES`, `LIFE_RECOVERED`): implementar o quitar.
  - Edición y baja de insignias de profesor sin UI en el front.
  - Los hitos de XP (600, 1800, 4200) se anotaron como niveles 3, 5 y 7 de PAR-09.
  - `hasReachedLevel` devuelve `false` si Backoffice no responde, para no frenar el registro de XP.

## Referencias
- Código / PR / doc: `V16__badge_and_badge_award.sql` (`2f65f5a`), `V17__system_badges.sql` (`9fce938`, 2026-10-03), `30f063a` (catálogo del curso, T-20.2, 2026-10-06), `e797d5d` (evaluador, T-21.1), `a7ef7f1` (outbox, T-21.2), `models/BadgeOrigin`, `BadgeType`, `BadgeCriterion`, `services/BadgeEvaluator`.
- `tpi-roadmap/docs/ESTRUCTURA.md` (BadgeEvaluator, BadgeCriteriaChecks), `docs/contracts/roadmap-events-v1.md`.
- Relacionadas: [[decisiones/DEC-002-outbox-transaccional-eventos-salientes|DEC-002]], [[decisiones/DEC-012-curva-de-niveles-desde-par-09|DEC-012]].

> [!question] Verificar
> `V17` anota 600 = nivel 3, 1800 = nivel 5 y 4200 = nivel 7, pero la curva de ejemplo de Backoffice da 1200, 3500 y 7300. Confirmar qué curva PAR-09 está activa.
