---
tags: [tpi, g10, decision, comisiones, courses]
fecha: 2026-10-08
estado: aceptada
reemplaza: ""
---

# DEC-014: Comisiones: un roadmap por cohorte (modelo B), pertenencia múltiple y evaluación en Roadmap

## Contexto
HU-44/45 piden ver el roadmap y el avance por comisión. El 2026-10-08 producto decidió que un alumno puede estar en **varias comisiones a la vez**, lo que reemplazó la hipótesis previa de "un grupo activo por alumno y cohorte" (P-29/D-02, `tpi-course#59`). Courses no evalúa restricciones por alumno ni emite eventos de cambio de grupo.

## Decisión
- **Modelo B:** un `roadmap` por cohorte (`courseCohortId`); la vista por comisión es un **filtro**, no un roadmap por grupo. El alumno que está en varias comisiones elige cuál ve (si no hay selección, `400 group.selection-required` con las opciones).
- **Pull y evaluación en Roadmap ("opción R"):** Roadmap lee de Courses grupos, participantes y restricciones (sección primero, actividad/nodo después) y evalúa `DATE`/`GROUP` con su propio progreso y los grupos del alumno; aplica `ALL`/`ANY` sobre todas las condiciones. No hay caché en el gate.
- **Solo lectura y asignación humana:** solo `PROFESSOR`/`MANAGER` asignan comisión; el principal de servicio nunca asigna.
- **El ranking de cohorte no depende de las comisiones.** Todo detrás del flag `ROADMAP_BY_GROUP_ENABLED`.
- **Regla (c):** un prerrequisito no puede quedar fuera del alcance de visibilidad del nodo que lo exige (validación transitiva en el editor y en el sync).

## Alternativas descartadas
- **Un roadmap por comisión**: duplicaría el grafo y el progreso.
- **Un único grupo activo por alumno**: reemplazado por la decisión de producto del 2026-10-08.
- **Evento Kafka de cambio de grupo**: no existe en Courses; se acordó consultar por pull "por ahora".
- **Evaluación por alumno en Courses**: Courses no expone endpoints con `studentId`.

## Consecuencias
- Positivas: modelo simple, sin duplicar datos; contrato de solo lectura con Courses.
- Negativas / deuda:
  - Varias llamadas HTTP a Courses por evaluación; si Courses cae, `503`.
  - `SECTION_COMPLETED` no se evalúa en el gate.
  - HU-49: traducir `HIDDEN` vs `LOCKED`, evento de cambio y aviso siguen pendientes (bloqueo G01).
  - El front no tiene selector de comisión (HU-44) y falta UI para HU-45.

## Referencias
- Código / PR / doc: `services/groups/*` (`GroupVisibilityRules`, `GroupAccessService`, `UnitRestrictionRules`, `NodeVisibilityScope`), `GraphValidator`, `PrerequisiteGraphService`; `52a17b3` (2026-10-08), `1849cc2` (regla c, 2026-10-10), `f0cd488`, `7bac6fa`, `c4a4237` (ranking independiente).
- `tpi-roadmap/docs/contracts/courses-grupos-t-10-1.md` (§1, §3.6, §4), `docs/contracts/courses.md` §7.9.
- Relacionadas: [[acuerdos/courses-g01|Courses]], [[decisiones/DEC-004-flags-apagados-por-defecto|DEC-004]], [[decisiones/DEC-010-prerrequisitos-por-seccion-v25|DEC-010]].
