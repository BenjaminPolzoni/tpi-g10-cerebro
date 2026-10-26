---
tags: [tpi, g10, sprint-4, plan, HU-72, back, front, cierre, archivado]
fecha: 2026-10-26
autor: Benjamin Polzoni
estado: borrador
historia: HU-72
tareas: [T-72.1, T-72.2, T-72.3, T-72.4]
taiga: [9222, 9223, 9225, 9226]
repo: 2026-P4-BE/tpi-roadmap, 2026-P4-FE/2026-PIV-TPI-FE (+ pedido a 2026-P4-BE/tpi-course)
base: BE origin/develop 6268b669 · FE origin/develop 264d37e10 · Courses tpi-course main (2026-10-26)
---

# HU-72 · Back + Front — Cierre del curso y roadmap archivado

> [!info] Contexto
> Arrastre del Sprint 3: son las **únicas tareas mías que quedaron en New**. Son T-72.1 [#9222](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9222), T-72.2 [#9223](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9223), T-72.3 [#9225](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9225) y T-72.4 [#9226](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9226). T-72.5 (docs) es de Tomás.
> Historia: [[sprints/sprint-3/historias/HU-72 Cerrar el curso con el estado académico final|HU-72]] · Acuerdo: [[acuerdos/courses-g01|Courses G01]] · Duda abierta: [[sprints/sprint-3/08-dudas|G14]].
> **Está lista cuando** el profesor ve los candidatos P90/P10, confirma el estado final de cada alumno, exporta el resumen, archiva el curso y, a partir de ahí, el roadmap y el ranking no cambian más (CA1–CA5).

## 1. Qué hay hoy (verificado en el código)

### Archivado del curso en Roadmap: ya funciona en el back
- `CoursesLifecycleEventListener.handleCourseCohortArchived` → `CourseCohortSyncService.archiveCohort` (`:141`) pone `roadmap.archived = true` en **todos** los roadmaps de la cohorte.
- Las escrituras del editor ya rechazan con `409 course.archived`: `GraphService.validateEditable` (`:768`), `PrerequisiteEditor.editableNode` (`:159`), `TypedRelationService.editableRoadmap` (`:283`), `RoadmapManagementService.editable` (`:333`). El gate responde `course_archived` (`GateEvaluator:197`) y `markAsRead` devuelve 403 (`ProgressService:439`).
- No hay que confundirlo con **archivar un roadmap** (T-57.3, `POST /roadmaps/{id}/archive`). Eso es una baja lógica (`softDelete`) de un roadmap secundario y ya está hecho.

### Huecos en el back
1. **El XP se sigue moviendo con el curso archivado.** `ProgressService.recordResult` (`:130`) y `applyRectification` (`:221`) no miran `archived`. Courses no deja archivar con intentos abiertos ni con evaluaciones LLM pendientes, pero una **rectificación del Motor** (`CHALLENGE_RESULT_RECTIFIED`, [[issue-312-rectificacion|#312]]) que llegue después del cierre cambia el XP y el ranking. Eso rompe CA5.
2. **El catálogo de insignias sigue editable.** `BadgeCatalogService` no tiene guard de `archived`.
3. **No hay endpoint de cierre.** Los candidatos y el resumen no existen como recurso. El ranking del profesor (`StaffRankingView`) ya trae todo lo que hace falta para los candidatos: `zone` p90/p10, `cutoffs` (null con menos de 10 inscriptos, `RankingRules.activeCutoffs`), `profile.file_number` y nombres de Users, `stats.lost_lives`, `stats.mandatory_passed` / `mandatory_total` / `mandatory_passed_pct`, `stats.badges` (cantidad) y `xp_total`.
4. Insignias **por nombre** por alumno: hay `BadgeAwardRepository.findByCourseCohortIdAndStudentId` (de a un alumno) y `countAwardsByStudent` (solo cantidad). Falta una consulta por cohorte.

### Courses (G01): el bloqueo real
- `tpi-course` `CohortArchiveRules.assertEveryEnrollmentHasFinalStatus` **rechaza el archivado** con `409 MISSING_FINAL_ACADEMIC_STATUS` si una matrícula `VALIDATED` activa no tiene `finalAcademicStatus`.
- **Ningún código de `src/main` escribe `finalAcademicStatus`.** Solo lo leen el mapper y el DTO, y lo setean los tests. Resultado: **hoy un curso con alumnos validados no se puede archivar**. El evento `COURSE_COHORT_ARCHIVED` nunca sale y nuestro freeze nunca se dispara.
- El front de Courses ya archiva: `courses.service.archiveCourseCohort` → `POST /course/course-cohorts/{id}/archive`. El error se mapea en `cohort-archive.models.ts`, que ya conoce `MISSING_FINAL_ACADEMIC_STATUS`, y `cohort-context.facade.isArchived` sale del `status` de la cohorte.

### Front de Roadmap
- **Ignora `archived` por completo.** Ni `features/roadmap` ni `features/ranking` lo leen, aunque `GET /courses/{id}/roadmaps` (`RoadmapManagementDtos:110`) y `RoadmapResponse` (`GraphDtos:460`) lo mandan. El profesor puede editar y recién se entera por el 409.
- Lo que se reutiliza: `ExportService.exportToCsv` (`core/services/export.service.ts`, con protección contra fórmulas de Excel), el adapter `HttpRankingAdapter` y `BackendStaffRankingView`, las pestañas de `CourseEditorPageComponent` (`teacher/course/:id/...`) y `generic-table`, `generic-select`, `generic-badge`, `generic-button`.

## 2. Decisiones (a confirmar)

| # | Pregunta | Propuesta | Por qué |
|---|---|---|---|
| D1 (T-72.1 / G14) | ¿Dónde se guarda el estado final? | **En Courses** (`Enrollment.finalAcademicStatus`, que ya existe). Se le pide a G01 un endpoint de escritura en lote: `PUT /course/course-cohorts/{id}/final-academic-statuses` con `[{ enrollment_id \| student_id, final_academic_status }]`, solo para el profesor dueño (MANAGER/PROFESSOR) y con la cohorte ACTIVE. | La regla de archivado de Courses ya lo exige, así que el dato es de ellos. Una tabla propia en Roadmap **no destraba nada**: Courses seguiría sin poder archivar. |
| D2 | ¿Quién llama a ese endpoint? | **El front, directo a Courses**, con el token del profesor y por el gateway, como ya hace `archiveCourseCohort`. Roadmap back no lo toca. | Sin cliente técnico nuevo, sin scope `course.enrollments.write` y sin una consistencia distribuida que mantener. |
| D3 | ¿Qué pasa con XP que llega con el curso archivado (rectificación tardía)? | **Se descarta y se loguea** (`event.course-archived-ignored`) y se hace ack sin reintentar. El ledger y el ranking quedan congelados. | Es CA5. El estado final ya se confirmó con ese ranking. Si los profes quieren otra cosa, se cambia en un solo lugar. |
| D4 | ¿Endpoint de candidatos separado o se reutiliza el ranking? | **Un solo endpoint** `GET /api/roadmap/courses/{courseId}/closure` que devuelve todas las filas del ranking de staff más las insignias por nombre y el estado final, si se pasa. Los «candidatos» son las filas con `zone` p90/p10. | La lógica de zonas, cortes y desempate ya está en `RankingService`; no se duplica. |
| D5 | ¿El CSV lo arma el back o el front? | **El front**, con `ExportService.exportToCsv` sobre la respuesta de D4. | El profesor ya recibe legajos en el ranking de staff, así que no hay exposición nueva. Se ahorra un endpoint `text/csv` más su OpenAPI y su test. Si piden el CSV desde el back, `GET /closure/summary.csv` reusa el mismo servicio. |
| D6 | ¿Con qué ranking se calculan los candidatos si el curso tiene varios roadmaps? | Con el **del curso** (`XpScope.ofCourse`), igual que `GET /courses/{id}/ranking`. | Es el ranking «oficial» de la cohorte. Los roadmaps en modo ROADMAP no suman al curso (T-17.3). |
| D7 | ¿Quién archiva? | **Courses**, desde el botón «Cerrar curso» de la pantalla de cierre, que llama a `archiveCourseCohort`. Roadmap se entera por `COURSE_COHORT_ARCHIVED`, que ya consume. | Courses es el dueño del ciclo de vida de la cohorte. |

> [!warning] Bloqueante
> Sin el endpoint de D1, el CA2 y el archivado no se pueden probar de punta a punta. **Primera acción: mandarle el pedido a G01** (issue en `tpi-course` + nota en [[acuerdos/courses-g01]]). El resto del plan (pasos 3 a 5) se puede hacer en paralelo usando un mock.

## 3. Pasos — Coordinación (T-72.1)

1. Abrir un issue en `2026-P4-BE/tpi-course` con el título «Escribir finalAcademicStatus antes de archivar». Incluir la evidencia (`CohortArchiveRules` exige el dato y nadie lo escribe), el contrato de D1, los valores `PROMOTED | REGULAR | NOT_REGULAR | DROPPED_OUT` y que fuera de esos cuatro responda 400.
2. Pedir que `GET /course/course-cohorts/{id}/enrollments` (o el que use la pantalla) devuelva `finalAcademicStatus` y `studentNumber`, para mostrar lo ya confirmado.
3. Registrar el acuerdo en `acuerdos/courses-g01.md` («Pendiente / próximos pasos» y la tabla de eventos) y marcar G14 como resuelta en `08-dudas`.
4. Mock: agregar el endpoint a `Mock_back_micros/tpi-roadmap-mocks/mocks/services/courses/enrollments.mjs`, que ya maneja `finalAcademicStatus` en `store.mjs`.

## 4. Pasos — Back (`tpi-roadmap`, T-72.2 + D3)

Rama `feature/hu-72-cierre-curso` desde `origin/develop`, en un worktree `~/dev/TPI_2026/Backend/tpi-roadmap-hu-72`.

### 4.1 Freeze del XP (CA5)
1. **Test primero** (`ProgressServiceTest`): con `roadmap.archived = true`, `recordResult` y `applyRectification` no insertan movimiento, no cambian `total_xp` y no lanzan excepción (el evento queda con ack).
2. En `recordResult`, después de `roadmapLocator.locate(result)`, y en `applyRectification`, después de resolver el roadmap del intento: `if (roadmap.isArchived()) { log.warn(message("event.course-archived-ignored", eventId, courseCohortId)); return; }`. Sumar la clave a `messages*.properties`.
3. `BadgeCatalogService`: en las escrituras (crear, editar, borrar), el mismo `409 course.archived` que `GraphService.validateEditable`, con test.

### 4.2 Endpoint de cierre (CA1, CA4; datos para CA3)
1. **Test primero** (`ClosureServiceTest`). Escenario 1 de la HU: 24 alumnos → `cutoffs` no nulo y filas p90/p10 marcadas. Escenario 3: 7 alumnos → `cutoffs: null`, todas las filas con `zone: none`. Las insignias salen por nombre.
2. `BadgeAwardRepository`: `@Query("SELECT a.studentId, b.name FROM BadgeAwardEntity a JOIN a.badge b WHERE a.courseCohortId = :id")` (ajustar a cómo se mapea `badge` en la entidad).
3. `ClosureService.closureOf(courseCohortId)` arma la respuesta con `rankingService.staffView(courseCohortId)` (sin paginar) más las insignias por alumno. Nada más.
4. DTO `ClosureDtos.ClosureView`: `rows` (el `RankingRow` de staff con `badge_names: string[]`), `cutoffs`, `total_enrolled`, `data_status`, `archived` (si el roadmap principal está archivado) y `generated_at`. Todo en snake_case.
5. `ClosureController`: `GET ${app.api.private-path}/courses/{courseId}/closure`, con la misma autorización que el ranking de staff (ADMIN, GESTOR o `CohortOwnershipGuard.requireProfessorOwner`). El alumno recibe 403. Va con OpenAPI completo (200/401/403/503).
6. Checks: `mvn -B test -Dtest='Closure*Test,ProgressServiceTest,BadgeCatalog*Test'`, Checkstyle, PMD y `docs/api_doc/swagger.json`. Solo los tests pertinentes, no la suite completa.

> Fuera de alcance: el estado final **no** se guarda en Roadmap (D1) y el back no genera CSV (D5).

## 5. Pasos — Front (`2026-PIV-TPI-FE`, T-72.3 + T-72.4)

Rama del mismo nombre desde `origin/develop`, en un worktree `~/dev/TPI_2026/Frontend/2026-PIV-TPI-FE-hu-72` (con `npm ci`). Hacer push con `NODE_OPTIONS=--no-experimental-webstorage`.

### 5.1 Solo lectura con el curso archivado (CA5)
1. `course-roadmaps.service.ts`: mapear `archived` en `CourseRoadmap`. `CourseEditorPageComponent`: `readonly archived = computed(...)`. Con `archived`:
   - un `generic-callout` informativo, «Curso cerrado: el roadmap y el ranking son de solo lectura», con texto y sin depender solo del color;
   - las pestañas `graph`, `roadmaps` y `badges` ocultan o deshabilitan las acciones de escritura (crear, mover, borrar, guardar). Hay que usar un único `input`/signal que bajen los hijos, no un `if` en cada botón.
2. `RankingPageComponent`: mismo callout cuando el curso está archivado. Sale del `archived` del cierre (paso 5.2) o del roadmap.
3. Tests: el spec de `course-editor-page` (con `archived` no se ve el botón de guardar en grafo) y el de `ranking-page` (se ve el banner).

### 5.2 Pantalla de cierre (CA1, CA2, CA4)
1. Ruta nueva hija de `teacher/course/:id`: `{ path: 'closure', loadComponent: CourseClosurePageComponent }`, más la pestaña `closure` en `tabs` («Cierre»).
2. `ClosureService` (en `data-access/closure/`): `get(courseId)` → `GET /roadmap/courses/{id}/closure`, y `confirm(courseId, items)` → `PUT /course/course-cohorts/{id}/final-academic-statuses` (D1/D2). Errores inline, igual que `archiveCourseCohort`.
3. `CourseClosurePageComponent`:
   - `generic-table` con puesto, nombre, legajo, XP, insignias, vidas perdidas, obligatorios (n/total) y zona (`generic-badge` «Candidato a promoción» / «Riesgo de regularidad», con texto). Con `cutoffs == null` no se muestra ninguna zona (CA4).
   - Por fila, un `generic-select` con los 4 estados. La propuesta inicial es P90 → `PROMOTED`, P10 → `NOT_REGULAR` y el resto → `REGULAR`, pero **nada se guarda hasta que el profesor confirma**. Si ya hay un estado en Courses, se muestra ese.
   - «Confirmar estados» queda deshabilitado mientras falte algún alumno (dato obligatorio). Llama a `confirm`.
   - «Cerrar curso» se habilita después de confirmar. Llama a `CoursesService.archiveCourseCohort` y muestra los 409 con `archiveErrorMessage`, que ya existe. Al terminar bien, recarga y la pantalla queda en solo lectura.
4. **Exportar (T-72.4, CA3):** el botón «Exportar resumen» llama a `ExportService.exportToCsv(rows, 'cierre-<curso>', columns)` con las columnas legajo, nombre, estado final, XP e insignias (nombres separados por `; `). Está disponible antes y después del cierre.
5. i18n: claves `courseClosure.*` en es/en.
6. Tests (BDD de la HU, specs del componente):
   - 24 filas con `cutoffs` → se ven badges p90/p10;
   - 7 filas con `cutoffs: null` → no hay badges de zona;
   - con todos los estados confirmados, exportar → `exportToCsv` recibe una fila por alumno con las 5 columnas;
   - si falta un estado → «Confirmar» está deshabilitado;
   - si `archive` responde 409 `MISSING_FINAL_ACADEMIC_STATUS` → se ve el mensaje inline.

## 6. Orden y dependencias

```
T-72.1 pedido a G01 ──┐
                      ├─► 5.2 confirmar + cerrar (necesita el endpoint de Courses o el mock)
4.1 freeze XP ────────┤
4.2 GET /closure ─────┴─► 5.2 tabla + 5.2.4 export
5.1 solo lectura (independiente: se puede mergear primero)
```

PRs: **BE** (4.1 + 4.2) y **FE** (5.1 + 5.2). Si G01 se demora, se mergea igual con el PUT apuntando al mock y el botón de confirmar detrás del flag de entorno `closureConfirmEnabled`, apagado por defecto ([[decisiones/DEC-004-flags-apagados-por-defecto|DEC-004]]).

## 7. Riesgos

- **G01 no expone la escritura.** Ningún curso con alumnos se puede archivar y CA2 y CA5 no se demuestran con datos reales. Mitigación: el issue con evidencia el día 1 y el mock.
- **`total_enrolled` del ranking ≠ matrículas VALIDATED de Courses** (matrícula sin evento, fallback pull de HU-48). Faltaría el estado de un alumno y Courses rechazaría el archivado. Mitigación: la pantalla compara contra el listado de enrollments de Courses y marca a los que faltan.
- **`data_status` DEGRADED** (Accounting caído → `lost_lives: null`). Se muestra «sin dato» y no se usa para proponer el estado.
- La rectificación descartada (D3) puede sorprender a G09. Hay que avisarles en [[acuerdos/motor-desafios-g09]].
