---
tags: [tpi, g10, sprint-3, plan, HU-57, HU-61, HU-45, front, back]
fecha: 2026-10-20
autor: Benja
estado: borrador
tarea: sin tarea en Taiga
repo: 2026-P4-FE/2026-PIV-TPI-FE, 2026-P4-BE/tpi-roadmap
---

# Plan · Configurar roadmaps al crear un curso

> [!info] Contexto
> Pedido de Benja (2026-10-20), después de [[T-62.5 Front - alternar roadmaps y unidades en el mapa del profesor|T-62.5]]. El profesor tiene un curso con comisiones (p. ej. 2W1 y 2W2) y quiere poder armar, desde que crea el curso:
> - **Caso 1:** un roadmap para 2W1 y dos roadmaps para 2W2.
> - **Caso 2:** un solo roadmap para las dos comisiones, con el ranking y el avance separados por comisión.
> - Mezclas de ambos (un roadmap compartido y otro solo de una comisión).
>
> Todavía **no hay tarea en Taiga**: este plan sirve para decidir el alcance y crearlas.

## 1. Cómo se crea un curso hoy (verificado 2026-10-20)

- **Curso (cohorte):** "Mis cursos → Crear curso" abre `course-cohort-form-modal` con 3 pasos (datos básicos, horario, inscripción), o 2 si se clona un curso. No tiene nada de roadmap. Es código de Courses (G01). Front: `src/app/features/courses/ui/course-cohort-form-modal/`, `course-list-page`.
- **Comisiones:** se crean después, en la pestaña **Grupos** (`cohort-group-create-modal`), o llegan como grupos externos.
- **Roadmap principal:** no se crea al crear el curso. `tpi-roadmap` solo escucha de Courses `STUDENT_ENROLLED`, `STUDENT_UNENROLLED` y `COURSE_COHORT_ARCHIVED` (`CoursesLifecycleEventListener`). El principal nace cuando el profesor abre el contenido por primera vez y se sincronizan las secciones de Courses (`CourseSectionsReconciliationService`).
- **Roadmaps extra:** en la pestaña **Roadmaps** (HU-57), después de activar `multiple_roadmaps_allowed` en `PUT /courses/{id}/settings`. Se crean con `POST /courses/{id}/roadmaps`.
- **Roadmap ↔ comisión:** **no existe**. No hay tabla ni endpoint en `tpi-roadmap` (`origin/develop` `3445890`). Es [[sprints/sprint-3/historias/HU-61 Roadmaps por grupo del curso y restricciones de visualización|HU-61]] (New).
- **Comisión dentro de un roadmap:**
  - Ranking con filtro opcional por comisión en el back: T-45.8, cerrada (`RankingGroupFilter`, `?groupId=`). Ver [[T-45.8 Back - ranking con filtro por comisión|plan T-45.8]].
  - Avance por comisión: `/groups/{gid}/progress`.
  - Pantalla del ranking con filtro: [[T-45.9 Front - filtro por comisión en el ranking|T-45.9]] (New).
  - Selector de comisión del alumno: [[sprints/sprint-3/historias/HT-33 Comisión y material pendientes de HU-44 y HU-46|HT-33]] (New), detrás de `ROADMAP_BY_GROUP_ENABLED`.
- **Lo que suma T-62.5** (rama `feature/roadmap-multi-vista-profesor`, sin PR aún): el profesor alterna qué roadmap ve en la pestaña General y en el mapa, con la misma tarjeta, arrastrar para ordenar y "Nueva sección" contra el roadmap elegido.

> [!warning] El problema
> La configuración está repartida en 4 pantallas con un orden forzado: curso → comisiones → activar varios roadmaps → crearlos. Y el último paso (asignar cada roadmap a sus comisiones) no existe.

## 2. Qué cubre cada caso

| Caso | Hecho | Falta |
|---|---|---|
| 1 · un roadmap por comisión, o varios para una | 1:N (HU-57), alternar en el profesor (T-62.5) | Asignar roadmap ↔ comisiones y que el alumno vea solo los suyos, con 403 por URL (HU-61: T-61.1, T-61.2, T-61.3) |
| 2 · uno compartido con ranking separado | Filtro por comisión en el back (T-45.8), avance por comisión | Filtro en la pantalla (T-45.9), selector del alumno (HT-33) y decidir si "separado" es una configuración del curso (ver D2) |
| Mezcla | Se combinan sin chocar: el ranking se arma por roadmap o por curso según `progress_scope`, y el filtro por comisión va encima | Lo mismo que los dos casos |

## 3. Propuesta

**Recomendación:** no tocar el modal de Courses. Al terminar de crear el curso, ofrecer un paso propio, **"Configurar roadmaps"**, en nuestra pestaña Roadmaps, que junte todo en una pantalla. Así no dependemos de G01, y cada parte se enciende a medida que salen HU-61 y T-45.9.

| Paso | Qué agrega | Depende de | Se puede hoy |
|---|---|---|---|
| A | Cargar las comisiones desde la misma pantalla (link o atajo a la pestaña Grupos) | Courses ya crea grupos | ✅ |
| B | Elegir modo: **uno compartido** o **uno por comisión**, y agregar más roadmaps (p. ej. 2 para 2W2). Con más de uno se activa `multiple_roadmaps_allowed` solo | `PUT /courses/{id}/settings`, `POST /courses/{id}/roadmaps` | ✅ |
| C | Asignar cada roadmap a sus comisiones, o a «todas» | HU-61 (tabla y `PUT /roadmaps/{id}/groups`) | ❌ |
| D | En modo compartido, "ranking y avance separados por comisión" (sí/no) | T-45.9 y D2 | ❌ |
| E | Al clonar un curso, copiar sus roadmaps y asignaciones | [[sprints/sprint-3/historias/HU-71 Clonar un roadmap con sus restricciones|HU-71]] + HU-61 | ❌ |

## 4. Decisiones abiertas

- **D1 · El principal no existe justo después de crear el curso.** B crea roadmaps extra, pero el principal aparece recién con la sincronización de secciones. Hay dos caminos:
  - el front llama a la sincronización antes de crear los extra (rápido, solo front);
  - `tpi-roadmap` escucha un `COURSE_COHORT_CREATED` de Courses y crea el principal (más prolijo; es back y hay que coordinarlo con G01).
- **D2 · Dónde se guarda "ranking separado por comisión".** Hoy es un parámetro de cada consulta (`groupId`), no una configuración. Si el profesor lo elige una vez, iría como campo nuevo en `course_settings` (back) y el ranking abriría filtrado por defecto.
- **D3 · Quién lo hace.** Meterlo como pasos del modal de crear curso es código de G01. La recomendación (§3) lo evita; si igual se quiere en el modal, hay que acordarlo con G01.
- **D4 · Texto de "roadmap principal".** Con roadmaps por comisión, "principal" pierde sentido para el alumno. Hay que decidir si solo lo ve el profesor.

## 5. Próximos pasos

1. Decidir D1 a D4 con el equipo.
2. Crear la tarea en Taiga para B (front), colgada de HU-57.
3. Coordinar con Stefano Zoffoli (HU-61) para que C use su endpoint `PUT /roadmaps/{id}/groups`.
4. Retomar [[T-45.9 Front - filtro por comisión en el ranking|T-45.9]] para D.
