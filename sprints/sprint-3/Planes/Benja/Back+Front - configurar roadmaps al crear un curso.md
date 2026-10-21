---
tags: [tpi, g10, sprint-3, plan, HU-57, HU-61, HU-45, front, back]
fecha: 2026-10-20
autor: Benja
estado: borrador
tarea: sin tarea en Taiga
repo: 2026-P4-FE/2026-PIV-TPI-FE, 2026-P4-BE/tpi-roadmap
---

# Back + Front · Configurar roadmaps al crear un curso

> [!info] Contexto
> Pedido de Benja (2026-10-20), después de [[T-62.5 Front - alternar roadmaps y unidades en el mapa del profesor|T-62.5]]. El profesor tiene un curso con comisiones (p. ej. 2W1 y 2W2) y quiere poder armar, desde que crea el curso:
> - **Caso 1:** un roadmap para 2W1 y dos roadmaps para 2W2.
> - **Caso 2:** un solo roadmap para las dos comisiones, con el ranking y el avance separados por comisión.
> - Mezclas de ambos (un roadmap compartido y otro solo de una comisión).
>
> Todavía **no hay tarea en Taiga**: este plan sirve para decidir el alcance y crearlas.

## 1. Worktree

- **Carpeta:** `~/dev/TPI_2026/Frontend/2026-PIV-TPI-FE-config-roadmaps` (creada 2026-10-21 en `f781dadca`, sin upstream).
- **Rama:** `feature/roadmap-configurar-al-crear-curso`, **desde `feature/roadmap-multi-vista-profesor`** (T-62.5, `f781dadca`), no desde `develop`. Reusa su selector de roadmaps, `CourseRoadmapsService` en la pestaña General y `reorderSections`.
- **Cuando se mergee T-62.5:** rebasear sobre `origin/develop` antes del primer push. Sin upstream hasta entonces, para que un `git push` no termine en otra rama.
- **Antes de empezar:** `npm ci` (la worktree no trae `node_modules`). Tests con `NODE_OPTIONS=--no-experimental-webstorage` (Node 25).
- **Back:** `~/dev/TPI_2026/Backend/tpi-roadmap-config-roadmaps`, rama `feature/roadmap-configurar-al-crear-curso` desde `origin/develop` en `32b6cbe` (creada 2026-10-21, sin upstream). Es para el evento `COURSE_COHORT_CREATED` (D1) o el campo en `course_settings` (D2).
  - Lleva copiada la plantilla `.tpi/platform/` con soporte de variante y su `.env`, sacadas de `Backend/tpi-roadmap`. **No se commitea:** aparece como cambios en `git status`.
  - Flyway: la última migración en `develop` es `V51__roadmap_section_source.sql`. Antes de crear una nueva, revisar `migration-vendor` y los PRs abiertos para no repetir la versión.
  - **Actualización (2026-10-21):** el PR [#272](https://github.com/2026-P4-BE/tpi-roadmap/pull/272) de Lorenzo Araujo (T-61.1, rama `feature/9161-roadmap-groups`) ya usa **`V52__roadmap_group.sql`** y agrega `PUT /roadmaps/{roadmapId}/groups`. B1 tiene que ir en V53 o en la que siga libre. El PR está abierto, con cambios pedidos y conflictos con `develop`.

> [!info] Relación con T-62.5
> Este plan sigue a [[T-62.5 Front - alternar roadmaps y unidades en el mapa del profesor|T-62.5]]: allá el profesor **alterna** entre los roadmaps del curso; acá los **configura** (cuántos, de qué comisión y con qué ranking). La rama depende de la de T-62.5 hasta que esa entre a `develop`.

## 2. Cómo se crea un curso hoy (verificado 2026-10-20)

- **Curso (cohorte):** "Mis cursos → Crear curso" abre `course-cohort-form-modal` con 3 pasos (datos básicos, horario, inscripción), o 2 si se clona un curso. No tiene nada de roadmap. Es código de Courses (G01). Front: `src/app/features/courses/ui/course-cohort-form-modal/`, `course-list-page`.
- **Comisiones:** se crean después, en la pestaña **Grupos** (`cohort-group-create-modal`), o llegan como grupos externos.
- **Roadmap principal:** no se crea al crear el curso. `tpi-roadmap` solo escucha de Courses `STUDENT_ENROLLED`, `STUDENT_UNENROLLED` y `COURSE_COHORT_ARCHIVED` (`CoursesLifecycleEventListener`). El principal nace cuando el profesor abre el contenido por primera vez y se sincronizan las secciones de Courses (`CourseSectionsReconciliationService`).
- **Roadmaps extra:** en la pestaña **Roadmaps** (HU-57), después de activar `multiple_roadmaps_allowed` en `PUT /courses/{id}/settings`. Se crean con `POST /courses/{id}/roadmaps`.
- **Roadmap ↔ comisión:** **no existe**. No hay tabla ni endpoint en `tpi-roadmap` (`origin/develop` `3445890`). Es [[sprints/sprint-3/historias/HU-61 Roadmaps por grupo del curso y restricciones de visualización|HU-61]] (New).
- **Comisión dentro de un roadmap:**
  - Ranking con filtro opcional por comisión en el back: T-45.8, cerrada (`RankingGroupFilter`, `?groupId=`). Ver [[T-45.8 Back - ranking con filtro por comisión|plan T-45.8]].
  - Avance por comisión: `/groups/{gid}/progress`.
  - Pantalla del ranking con filtro: [[T-45.9 Front - filtro por comisión en el ranking|T-45.9]] (**Closed** el 2026-10-18 en Taiga).
  - Selector de comisión del alumno: [[sprints/sprint-3/historias/HT-33 Comisión y material pendientes de HU-44 y HU-46|HT-33]] (New), detrás de `ROADMAP_BY_GROUP_ENABLED`.
- **Lo que suma T-62.5** (rama `feature/roadmap-multi-vista-profesor`, sin PR aún): el profesor alterna qué roadmap ve en la pestaña General y en el mapa, con la misma tarjeta, arrastrar para ordenar y "Nueva sección" contra el roadmap elegido.

> [!warning] El problema
> La configuración está repartida en 4 pantallas con un orden forzado: curso → comisiones → activar varios roadmaps → crearlos. Y el último paso (asignar cada roadmap a sus comisiones) no existe.

## 3. Qué cubre cada caso

| Caso | Hecho | Falta |
|---|---|---|
| 1 · un roadmap por comisión, o varios para una | 1:N (HU-57), alternar en el profesor (T-62.5) | Asignar roadmap ↔ comisiones y que el alumno vea solo los suyos, con 403 por URL (HU-61: T-61.1, T-61.2, T-61.3) |
| 2 · uno compartido con ranking separado | Filtro por comisión en el back (T-45.8), avance por comisión | Selector del alumno (HT-33) y decidir si "separado" es una configuración del curso (ver D2, §5) |
| Mezcla | Se combinan sin chocar: el ranking se arma por roadmap o por curso según `progress_scope`, y el filtro por comisión va encima | Lo mismo que los dos casos |

## 4. Propuesta

**Recomendación:** no tocar el modal de Courses. Al terminar de crear el curso, ofrecer un paso propio, **"Configurar roadmaps"**, en nuestra pestaña Roadmaps, que junte todo en una pantalla. Así no dependemos de G01, y cada parte se enciende a medida que sale HU-61.

| Paso | Qué agrega | Depende de | Se puede hoy |
|---|---|---|---|
| A | Cargar las comisiones desde la misma pantalla (link o atajo a la pestaña Grupos) | Courses ya crea grupos | ✅ |
| B | Elegir modo: **uno compartido** o **uno por comisión**, y agregar más roadmaps (p. ej. 2 para 2W2). Con más de uno se activa `multiple_roadmaps_allowed` solo | `PUT /courses/{id}/settings`, `POST /courses/{id}/roadmaps` | ✅ |
| C | Asignar cada roadmap a sus comisiones, o a «todas» | HU-61 (tabla y `PUT /roadmaps/{id}/groups`) | ❌ |
| D | En modo compartido, "ranking y avance separados por comisión" (sí/no) | D2 (T-45.9 ya está cerrada) | ❌ |
| E | Al clonar un curso, copiar sus roadmaps y asignaciones | [[sprints/sprint-3/historias/HU-71 Clonar un roadmap con sus restricciones|HU-71]] + HU-61 | ❌ |

## 5. Decisiones abiertas

- **D1 · El principal no existe justo después de crear el curso.** B crea roadmaps extra, pero el principal aparece recién con la sincronización de secciones. Hay dos caminos:
  - el front llama a la sincronización antes de crear los extra (rápido, solo front);
  - `tpi-roadmap` escucha un `COURSE_COHORT_CREATED` de Courses y crea el principal (más prolijo; es back y hay que coordinarlo con G01).
  - **Actualización (2026-10-21):** hay un tercer camino, el más simple. En un curso sin roadmaps, `POST /courses/{id}/roadmaps` ya crea el **principal** (`RoadmapManagementService.open`: `setPrimary(current.isEmpty())`, y el chequeo de `multiple_roadmaps_allowed` solo aplica si ya hay alguno). El front crea primero el principal y después activa el ajuste y crea los demás. **Recomendado; no hace falta back.**
  - **Hipótesis a verificar (B0):** la sincronización de secciones posterior engancha las secciones de Courses a ese principal creado por POST, en vez de crear otro. Tampoco está verificado que Courses publique `COURSE_COHORT_CREATED`: hoy `tpi-roadmap` no lo escucha.
- **D2 · Dónde se guarda "ranking separado por comisión".** Hoy es un parámetro de cada consulta (`groupId`), no una configuración. Si el profesor lo elige una vez, iría como campo nuevo en `course_settings` (back) y el ranking abriría filtrado por defecto.
- **D3 · Quién lo hace.** Meterlo como pasos del modal de crear curso es código de G01. La recomendación (§4) lo evita; si igual se quiere en el modal, hay que acordarlo con G01.
- **D4 · Texto de "roadmap principal".** Con roadmaps por comisión, "principal" pierde sentido para el alumno. Hay que decidir si solo lo ve el profesor.

## 6. Tareas por worktree

> [!info] Cómo leer esto
> Cada tarea dice en qué worktree va (§1), qué paso de §4 cubre, de qué depende y cuándo está lista. Las marcadas **bloqueada** esperan a otra tarea u otro equipo. Lo de HU-61 (asignar roadmap ↔ comisión en el back) es de Lorenzo Araujo y no está acá: solo lo consumimos.

### Back · `Backend/tpi-roadmap-config-roadmaps`

- [ ] **B0 · Verificar que el principal creado por POST recibe las secciones de Courses** (D1, paso B).
  - **Qué:** test de integración: un curso sin roadmaps → `POST /courses/{id}/roadmaps` → `POST /courses/{id}/sections/sync` → las secciones quedan en ese principal, sin un segundo roadmap. Si falla, arreglar la reconciliación (`CourseSectionsReconciliationService`) para que use el principal existente.
  - **Lista cuando:** el test pasa en `./mvnw verify`.
- [ ] **B1 · Ajuste "ranking separado por comisión" en `course_settings`** (D2, paso D). Solo si el equipo elige guardarlo como configuración.
  - **Qué:**
    - Migración con columna `ranking_by_group boolean not null default false`. La versión sigue a `V51` y hay que revisar `migration-vendor` y los PRs abiertos.
    - El campo en `CourseSettingsEntity`.
    - Leerlo y escribirlo en `GET` y `PUT /courses/{id}/settings` (`RoadmapManagementController`), con los mismos permisos (ADMIN, GESTOR o PROFESSOR dueño).
  - **Lista cuando:** hay tests de leer y escribir el ajuste, con default `false` para un curso sin ajustes.
- [ ] **B2 · Ranking por defecto según el ajuste** (D2, paso D). **Bloqueada por B1.**
  - **Qué:** con `ranking_by_group` encendido y sin `groupId` en la consulta, el **alumno** ve el ranking de su comisión: se resuelve con `GroupAccessService` y su caché, y se filtra con `RankingGroupFilter`, que viene de T-45.8. El staff sigue igual, eligiendo la comisión con `?groupId=`. Con el ajuste apagado, no cambia nada.
  - **Lista cuando:** hay tests de ajuste apagado (igual que hoy), encendido para el alumno (solo su comisión) y encendido para el staff (sin filtro).
- [ ] **B3 · Escuchar `COURSE_COHORT_CREATED`** (D1, camino 2). **Solo si B0 falla y no tiene arreglo**, y si Courses (G01) publica ese evento. Si no, se descarta.

### Front · `Frontend/2026-PIV-TPI-FE-config-roadmaps`

- [ ] **F1 · Pantalla "Configurar roadmaps"** (paso B).
  - **Qué:** una pantalla nuestra en la feature roadmap (por ejemplo `/roadmap/teacher/course/:id/roadmaps/setup`), con entrada desde la pestaña Roadmaps. El profesor elige:
    - **Uno compartido:** un solo roadmap.
    - **Uno por comisión:** un roadmap por cada comisión del curso, que sale de `CohortGroupsService`. El nombre por defecto es "Roadmap <comisión>" y se puede editar.
    - **Más roadmaps:** se pueden agregar más (por ejemplo 2 para 2W2).
  - **Al confirmar:**
    1. `POST /courses/{id}/roadmaps` del primero, que queda principal.
    2. Si hay más, `PUT /courses/{id}/settings` con `multipleRoadmapsAllowed: true`.
    3. `POST` de los demás, en secuencia.
    4. Si falla a mitad, se muestra cuáles quedaron creados y el profesor puede reintentar los que faltan.
  - **Componentes del kit:** `generic-segmented` para el modo y `GenericConfirmModal` antes de crear. Reusa `CourseRoadmapsService`.
  - **Lista cuando:** se arman los casos 1 y 2 de §3 sin tocar la pestaña Roadmaps, y hay tests del flujo feliz, de la falla a mitad y del curso que ya tiene roadmaps (ahí la pantalla solo deja agregar).
- [ ] **F2 · Comisiones desde la misma pantalla** (paso A).
  - **Qué:** si el curso no tiene comisiones, un `generic-empty-state` con link a la pestaña Grupos y vuelta a la pantalla. No se duplica el alta de grupos.
  - **Lista cuando:** hay test con 0 comisiones (empty state) y con 2 (las lista).
- [ ] **F3 · Ofrecer la pantalla al crear el curso** (paso B, D3). **Bloqueada por acuerdo con G01** si se toca `course-list-page`.
  - **Qué:** al terminar de crear el curso, un link "Configurar roadmaps" en el aviso de curso creado (`createdCohort`). Mientras no haya acuerdo, la entrada queda solo en la pestaña Roadmaps (F1).
- [ ] **F4 · Asignar comisiones a cada roadmap** (paso C). **Bloqueada por HU-61** (T-61.1 y T-61.2).
  - **Qué:** en F1 y en la pestaña Roadmaps, un `generic-select` múltiple de comisiones por roadmap, o la opción «todas». Se guarda con `PUT /roadmaps/{id}/groups`. En el modo "uno por comisión" viene precargado. Es la T-61.3 de Lorenzo: hay que coordinar quién la hace para no duplicarla.
- [ ] **F5 · Switch "ranking separado por comisión"** (paso D). **Bloqueada por B1.** El filtro en la pantalla ya existe: [[T-45.9 Front - filtro por comisión en el ranking|T-45.9]], cerrada.
  - **Qué:** en el modo "uno compartido" de F1 y en la configuración del curso, un `generic-switch` que lee y escribe `rankingByGroup` en los settings. La pantalla del ranking abre filtrada por la comisión del usuario cuando está encendido.
- [ ] **F6 · Texto de "principal"** (D4). Cuando haya roadmaps por comisión, el alumno no ve la palabra "principal". Depende de lo que se decida en D4.

### Orden sugerido

1. **B0** (back) y **F1 + F2** (front) en paralelo: con eso el profesor ya arma los casos 1 y 2, aunque el alumno todavía vea solo el principal hasta HU-61.
2. **B1 → B2** y **F5**, si el equipo decide guardar el ajuste (D2).
3. **F4** cuando salga HU-61, y **F3** cuando haya acuerdo con G01.

## 7. Tareas de Taiga relacionadas (verificado en Taiga 2026-10-21)

> [!warning] La copia de Taiga del cerebro es del 2026-10-15
> Esa copia está vieja. Hoy HU-57 (T-57.1 a T-57.4), HU-71 (T-71.1 a T-71.4) y T-45.8/T-45.9 están **Closed**. HU-61 (T-61.1 a T-61.3) está **In progress**, de **Lorenzo Araujo**, con el PR #272 abierto.

| Tarea del plan | Tarea de Taiga relacionada | Qué hacer |
|---|---|---|
| B0 | T-57.1 / T-57.2 (Closed) | Tarea nueva en HU-57, o bug si B0 falla |
| B1, B2 | T-45.8 / T-45.9 (Closed) | Tarea nueva en HU-45, solo si se elige D2 |
| F1, F2 | T-57.3 (Closed), la pantalla que se extiende | Tarea nueva en HU-57 |
| F3 | ninguna (el modal es de G01) | Tarea nueva, con acuerdo de G01 |
| F4 | **T-61.3** (In progress, Lorenzo Araujo) | No crear: ya existe |
| F5 | T-45.9 (Closed) | Va con B1 en HU-45 |
| E | T-71.x (Closed) | Copiar las asignaciones es de HU-61 |

## 8. Próximos pasos

1. Decidir D2 a D4 con el equipo. D1 queda resuelto si pasa B0.
2. Crear en Taiga las tareas B0, F1 y F2, colgadas de HU-57; y B1, B2 y F5 si se elige D2.
3. Coordinar con Lorenzo Araujo (HU-61) para que F4 use su endpoint `PUT /roadmaps/{id}/groups` y para no duplicar T-61.3.
4. T-45.9 ya está cerrada: F5 solo espera a B1.
