---
tags: [tpi, g10, sprint-4, plan, back, front, courses, roadmap, multi-roadmap]
fecha: 2026-11-06
autor: Benjamin Polzoni
estado: hecho
repo: 2026-P4-BE/tpi-course, 2026-P4-BE/tpi-roadmap, 2026-P4-FE/2026-PIV-TPI-FE
rama: BenjaminPolzoni/unified-node-creation-pages (front)
---

# Plan — Visibilidad de una sección para varios grupos

## Qué se pide

En el drawer de edición de sección (General de la comisión → editar sección → **Visibilidad**), el campo "Grupo requerido" hoy permite **un solo grupo**. Se pide:

- Que el selector aparezca **solo cuando el roadmap seleccionado lo comparten 2 o más grupos**.
- Que permita elegir **ninguno, uno o varios** de esos grupos (ej. 2W1 + 2W2).
- Que las fechas desde–hasta se apliquen a los grupos elegidos: "(2W1 **o** 2W2) **y** entre estas fechas".

No se copia la sección ni sus nodos: es la misma sección con otra restricción.

## Por qué hoy no se puede

La restricción de una sección (tpi-course) es una lista plana de condiciones con **un único operador** (`ALL` / `ANY`) para todas, y cada `GROUP` lleva un solo `cohortGroupId`.

- `SectionRestrictionEvaluator.evaluate` (tpi-course) cuenta cada `GROUP` como una condición más: con `ALL` y dos grupos el alumno tiene que estar en **los dos**; con `ANY` el OR se aplica también a las fechas, así que basta con estar en un grupo para verla fuera de fecha.
- `GroupVisibilityRules.isVisibleIn` (tpi-roadmap) replica lo mismo: con `ALL` exige `studentGroupIds.containsAll(groupIds)`.

"(grupo A o grupo B) y fechas" no se puede expresar con el contrato actual.

## Decisión

**Las condiciones `GROUP` de una sección se combinan siempre con OR entre sí**, y ese bloque cuenta como **una sola condición** frente al operador general (`ALL`/`ANY`) junto con `DATE` y `SECTION_COMPLETED`.

- No cambia el contrato HTTP: se siguen mandando N condiciones `GROUP`, una por grupo.
- Fuera de alcance: rango de fechas **distinto por grupo** (2W1 del 1 al 10, 2W2 del 5 al 15). Si lo piden, es otro cambio de modelo en tpi-course.

## Pedido a tpi-course

> **Asunto:** Restricciones de sección — varias condiciones GROUP combinadas con OR
>
> Necesitamos que una sección pueda restringirse a varios grupos de la cohorte a la vez y además tener un rango de fechas, con el significado "(grupo A o grupo B) y entre estas fechas".
>
> Hoy `SectionRestrictionEvaluator.evaluate` cuenta cada condición `GROUP` por separado frente al operador del set: con `ALL` el alumno tiene que pertenecer a todos los grupos, y con `ANY` el OR alcanza también a la condición `DATE`.
>
> Propuesta, sin cambiar el contrato HTTP:
> 1. En `evaluate`, agrupar todas las condiciones `GROUP` activas en un único bloque, que se cumple si el alumno pertenece a **al menos uno** de esos grupos. Ese bloque cuenta como una sola condición para el operador `ALL`/`ANY`, junto con `DATE` y `SECTION_COMPLETED`.
> 2. Si en `unmetReason` falla el bloque, informar una sola razón de grupo, no una por grupo.
> 3. Verificar que `PUT /course-sections/{id}/restrictions` acepte varias `GROUP` con distinto `cohortGroupId` y rechace el mismo grupo repetido (400).
> 4. Tests: `ALL` + 2 GROUP + DATE (alumno en uno de los grupos y dentro de fecha → accede; fuera de fecha → no; en ningún grupo → no); `ANY` + 2 GROUP; set con un solo GROUP sin cambios.
> 5. Documentar la regla en el Swagger de `SectionRestrictionConfiguration`.
>
> Impacto en datos: solo cambia el resultado para sets con `ALL` y 2 o más `GROUP`, que hoy casi nadie puede ver.

## Tareas

### tpi-course

- [x] **V-01** Pedido a Courses en [tpi-course#316](https://github.com/2026-P4-BE/tpi-course/issues/316) (evaluador + validación de grupo repetido + tests + Swagger). Lo implementa el equipo de Courses; nosotros no tocamos ese repo.

### tpi-roadmap

- [x] **V-02** `GroupVisibilityRules.isVisibleIn`: con `GROUP` alcanza con `restriction.groupIds().contains(groupId)`; quitar la rama `ALL → containsAll`. Actualizar el Javadoc (acta T-10.1 §4 ya no aplica a grupos) y los tests: `ALL` con 2 grupos → visible en la vista de cualquiera de los dos.
- [x] **V-03** Revisar `StudentGroupUnits` y los demás usos de `SectionGroupRestriction.operator()` para que nada vuelva a exigir pertenecer a todos los grupos.

### Front (`section-editor-drawer`)

- [x] **V-04** `cohort-general-page.component.ts`: calcular los grupos que comparten el roadmap seleccionado (`selectedRoadmapId`). Si el roadmap tiene `visibleToAll !== false`, son todos los grupos de la cohorte; si no, sus `groupIds`. Pasarlos al drawer con un input nuevo (`roadmapGroupIds`).
- [x] **V-05** Drawer: mostrar el bloque de grupos solo si `roadmapGroupIds().length >= 2`. Las fechas siguen visibles siempre.
- [x] **V-06** Drawer: reemplazar `generic-select` por una lista de `generic-checkbox` dentro de un `fieldset` con `legend`, como en `roadmap-setup-page`, una por grupo del roadmap. Ninguno marcado = la ven todos. El estado pasa de `selectedGroupId: string` a `selectedGroupIds: string[]`.
- [x] **V-07** Carga (`section-editor-drawer.component.ts` ~l.320): leer **todas** las condiciones `GROUP`, no solo la primera con `find`. Si alguno de los grupos guardados no comparte el roadmap, conservarlo en `otherConditions` para no borrarlo al guardar.
- [x] **V-08** Guardado (`saveVisibility`, ~l.650): una condición `GROUP` por grupo marcado; sin cambios en `DATE` ni en el operador.
- [x] **V-09** i18n (es/en/pt): label "Grupos que ven la sección", ayuda "Si no marcás ninguno, la ven todos los grupos del roadmap. Las fechas aplican a los grupos marcados.". Quitar `sectionDrawer.visibility.anyGroup` si queda sin uso.
- [x] **V-10** Specs del drawer: el bloque se oculta con 1 grupo y se muestra con 2; marcar 2 grupos manda 2 `GROUP`; se conservan los grupos ajenos al roadmap.

## Orden

V-01 → V-02/V-03 → front. El front puede ir en paralelo, pero no se mergea antes que V-01: sin ese cambio, marcar 2 grupos deja la sección invisible para casi todos.

## Notas

- El editor avanzado `section-restriction-editor` (página de ajustes de sección) ya permite varias `GROUP` a mano. Con V-01 cambia su significado con `ALL` (pasa a ser OR entre grupos); no requiere cambios de código.
- Como las unidades con `sectionSource: COURSE` siguen a las secciones de Courses, la restricción es de la sección, no del roadmap: filtrar por los grupos del roadmap es solo una ayuda de la UI.
