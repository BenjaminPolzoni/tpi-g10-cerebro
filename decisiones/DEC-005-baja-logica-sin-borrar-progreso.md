---
tags: [tpi, g10, decision, datos, rf-nfr-01]
fecha: 2026-09-24
estado: aceptada
reemplaza: ""
---

# DEC-005: Baja lógica en todo y el progreso del alumno nunca se borra

## Contexto
RF-NFR-01 no admite excepciones: nada se elimina físicamente. Courses puede dar de baja o inactivar secciones que Roadmap ya reflejó como unidades con alumnos avanzando, y los profesores pueden editar o dar de baja nodos con dependientes.

## Decisión
Todas las entidades llevan `deleted_at` (`BaseEntity.softDelete()`); incluso `completed_node` y `xp_movement` (V12). Cuando una sección desaparece del catálogo activo de Courses, el sync da de baja lógica **la unidad, sus nodos y sus aristas**, pero **conserva** `completed_node`, `content_reading` y `xp_movement`. Si Courses vuelve a publicar la sección, la unidad se **reactiva** con sus nodos en lugar de crear otra. Una lista vacía de secciones no da de baja nada. El ledger de XP es append-only: nunca se edita ni recalcula (RF-CFG-06) y editar reglas no revierte desbloqueos ya alcanzados.

## Alternativas descartadas
- **Borrado físico o cascada**: prohibido por RF-NFR-01.
- **Interpretar una lista vacía como "baja masiva"**: causó el guard T-36.7 (`476b5bd`); una respuesta vacía o incompleta no modifica el grafo.
- **Asignar IDs de Courses por aproximación** en roadmaps viejos: solo se vincula si coinciden exactamente nombre normalizado y posición; si hay ambigüedad, `409` y revisión manual.

## Consecuencias
- Positivas: el alumno conserva XP y avance ante cambios del catálogo; auditable; reactivable.
- Negativas / deuda:
  - Las restricciones únicas cuentan filas dadas de baja (p. ej. `uq_badge_award_student_badge`, `student_avatar`): guardar de nuevo **restaura** la fila.
  - Crece el volumen de filas sin purga automática (D-T01125-08).
  - Toda consulta debe filtrar `deleted_at IS NULL`; es fuente de bugs.

## Referencias
- Código / PR / doc: `V12__course_cohort_and_soft_delete.sql` (2026-09-24), `04277bc` (baja y reactivación, 2026-10-10), `476b5bd` (guard, 2026-10-06), `V26__student_avatar.sql` (2026-10-13), `services/CourseSectionSyncService`, `entities/BaseEntity`.
- `tpi-roadmap/docs/contracts/courses.md` §7.8, `docs/backlog/HU-02-HU-13-baja-nodo-con-dependientes.md`.
- Relacionadas: [[acuerdos/courses-g01|Courses]], [[decisiones/DEC-013-roadmap-no-calcula-xp-ledger-idempotente|DEC-013]].
