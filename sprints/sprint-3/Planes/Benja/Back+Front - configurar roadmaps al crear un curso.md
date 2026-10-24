---
tags: [tpi, g10, sprint-3, plan, HU-57, HU-61, HU-45, front, back]
fecha: 2026-10-20
actualizado: 2026-10-24
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
- **Roadmap ↔ comisión:** **no existe**. No hay tabla ni endpoint en `tpi-roadmap` (`origin/develop` `3445890`). Es [[sprints/sprint-3/historias/HU-61 Roadmaps por grupo del curso y restricciones de visualización|HU-61]] (New). **Actualización (2026-10-24):** ya existe en `origin/develop` (V58, `PUT /roadmaps/{id}/groups`, filtro del alumno y 403). Ver §9.
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

- [x] **F1 · Pantalla "Configurar roadmaps"** (paso B). **Hecha 2026-10-24** (`d50a27648`, `f1ff214ca`); ver §9.8.
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
- [x] **F2 · Comisiones desde la misma pantalla** (paso A). **Hecha 2026-10-24** (`d50a27648`, `f1ff214ca`); ver §9.8.
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

## 9. Actualización 2026-10-24 · decisiones y análisis contra `develop`

> [!info] Qué cambió
> Decisiones de Benja del 2026-10-24 (D2, D3, D4) y verificación del plan contra `origin/develop` del back (`c6aa13e3`) y del front. Lo que sigue **reemplaza** lo que decían D2 a D4 en §5 y marca qué tareas de §6 ya no hacen falta.

### 9.1 Lo que ya está en `develop` (verificado)

**Back (`tpi-roadmap`)**

- **T-61.1 hecha.** `V58__roadmap_group.sql` (tabla `roadmap_group`), `RoadmapEntity.groupIds` y `visibleToAll` (TRUE por defecto, como los roadmaps anteriores a V58), y `PUT /roadmaps/{roadmapId}/groups` con `{all, group_ids}` (`RoadmapManagementService.assignGroups`). Errores `roadmap.groups-required` y `roadmap.group-unknown`. Esto reemplaza lo de V52 y el PR #272 que decía §1.
- **T-61.2 hecha.** `RoadmapVisibilityService.visibleTo` filtra la lista del alumno y `requireVisible` da **403 `roadmap.not-visible`** al entrar por URL a un roadmap de otra comisión (`RoadmapResolver`). Los tests están en `RoadmapVisibilityTest` y `RoadmapVisibilityServiceTest`.
- **Todo cuelga de un flag.** Con `app.features.roadmap-by-group.enabled=${ROADMAP_BY_GROUP_ENABLED:false}` apagado, no se filtra nada y el alumno ve todos los roadmaps. Hay que encenderlo en la demo.
- **Ranking:** `GET /courses/{id}/ranking?group_id=` y `GET /roadmaps/{id}/ranking?group_id=`. Cada roadmap tiene `progress_scope` (`COURSE` o `ROADMAP`, V44), que decide si su XP suma al curso o solo al roadmap.
- **No hay** ningún ajuste `ranking_by_group` en `course_settings` (solo `multiple_roadmaps_allowed`).
- **No hay** ninguna regla que obligue a que cada comisión tenga al menos un roadmap visible.

**Front**

- **T-61.3 hecha.** `CourseRoadmapsService.assignGroups` y la asignación de comisiones en `course-roadmaps-page` (commit `ab2b44f21`), con los modelos `visibleToAll` y `groupIds`.
- **Ranking:** la pantalla ya filtra por comisión (T-45.9), pero su puerto solo llama a `getRanking(courseCohortId, groupId)` (`ranking-data.port.ts`). **No consulta el ranking de un roadmap** (`/roadmaps/{id}/ranking`).
- **No hay** en el profesor ningún selector de comisión que cambie la vista general ni el mapa. T-62.5 solo alterna roadmap.

### 9.2 Decisiones (Benja, 2026-10-24)

**D2 · El ranking sale del contenido, no de un ajuste.**

- Si las comisiones **comparten contenido** (mismos roadmaps), **comparten el ranking**.
- Si cada comisión tiene **contenido distinto**, el ranking está **separado** y el profesor elige cuál ver.
- Consecuencia: **no se guarda una configuración `ranking_by_group`**. Se deriva de cómo se asignaron los roadmaps (`visibleToAll` y `groupIds`).
- **Hipótesis a verificar:** que el ranking por roadmap tenga sentido solo con `progress_scope = ROADMAP`. Con `COURSE` el XP suma a todo el curso y un ranking por roadmap puede no distinguir comisiones. Hay que decidir si, al asignar un roadmap solo a una comisión, `progress_scope` pasa a `ROADMAP` solo o lo elige el profesor.
- **Descartadas:** B1, B2 y F5 de §6.

**D4 · "Principal" y mínimo de un roadmap por comisión.**

- Si las comisiones comparten contenido, el **principal** es el compartido.
- Si no, es el **primer roadmap** que aparezca, y los demás van después.
- **Regla nueva:** cada comisión tiene que ver **como mínimo un roadmap**, el compartido o uno propio. Los adicionales se suman al inicial.
- El back **no lo valida hoy**. Mientras no lo haga, el front avisa en la pantalla del profesor qué comisiones se quedan sin roadmap.
- F6 queda así: el alumno no ve la palabra "principal", y el profesor sí.

**D3 · Courses (G01).**

- Benja va a abrir una **issue** para que G01 sepa lo que se piensa hacer. No se toca el modal de crear curso hasta que respondan. F3 sigue bloqueada.
- Pendiente: agregar acá el número de la issue cuando exista.

### 9.3 Tareas de §6 después de esto

| Tarea | Estado |
|---|---|
| B0 | Sigue. Verificar que el principal creado por POST recibe las secciones de Courses. |
| B1, B2, F5 | **Descartadas por D2.** |
| B3 | Sigue condicionada a B0 y a G01. |
| F1, F2 | ✅ **Hechas 2026-10-24** (§9.8). F1 incluye la regla de D4 (al menos un roadmap por comisión). |
| F4 | **Ya existe** (T-61.3). Solo falta integrarla en F1 y precargarla en el modo "uno por comisión". |
| F6 | Resuelta por D4. |
| **F7 (nueva)** | ✅ **Hecha 2026-10-24** (§9.8). **Selector de comisión del profesor.** Un selector de comisión por encima del de roadmap, en la pestaña General y en el mapa. Al elegir una comisión muestra solo los roadmaps que ve esa comisión (los de `visibleToAll` más los suyos). |
| **F8 (nueva)** | **Ranking según el alcance.** En la pantalla del ranking, el alcance sale de las asignaciones: roadmaps compartidos, ranking del curso (con filtro de comisión opcional); roadmaps propios de una comisión, `/roadmaps/{id}/ranking`. Falta agregar esa consulta al puerto. |
| **B4 (nueva, opcional)** | Validar en el back que cada comisión del curso vea al menos un roadmap. Hoy solo avisa el front. |

### 9.4 Por dónde empezar

**Por el front.** El back ya tiene lo que necesita: asignar comisiones, filtrar al alumno, el 403 y el ranking por comisión. No hay ningún endpoint nuevo para F1, F2, F7 ni F8. El back tiene dos pendientes chicos: B0 (un test) y el flag `ROADMAP_BY_GROUP_ENABLED` encendido en la demo. Orden: **F7 → F1 + F2 → F8 → B0 / B4**.

### 9.5 Próximos pasos

1. Abrir la issue a G01 (D3) y anotar su número acá.
2. Decidir la hipótesis de D2 sobre `progress_scope`.
3. Crear en Taiga F1, F2, F7 y F8 colgadas de HU-57 o HU-61, según corresponda con Lorenzo Araujo, que lleva HU-61.

### 9.6 Orden de arranque y worktrees (2026-10-24)

> [!info] Dos pares de worktrees
> F1, F2 y B0 siguen en los worktrees de §1 (`config-roadmaps`). Verificado el 2026-10-24: el del **back existe**; el del **front y su rama ya no existen** (`git worktree list`), hay que recrearlos desde `feature/roadmap-multi-vista-profesor`. F7, F8 y B4 son otra funcionalidad, la **vista del profesor por comisión**, y van en worktrees propios para no mezclar ramas ni PR.

| Worktree | Carpeta | Rama | Se crea desde | Tareas |
|---|---|---|---|---|
| Front, configurar | `~/dev/TPI_2026/Frontend/2026-PIV-TPI-FE-config-roadmaps` (**por recrear**: ya no existe en disco) | `feature/roadmap-configurar-al-crear-curso` | `feature/roadmap-multi-vista-profesor` (T-62.5) | F1, F2 |
| Back, configurar | `~/dev/TPI_2026/Backend/tpi-roadmap-config-roadmaps` (existe) | `feature/roadmap-configurar-al-crear-curso` | `origin/develop` | B0 |
| **Front, vista por comisión** | `~/dev/TPI_2026/Frontend/2026-PIV-TPI-FE-vista-comision` (creado 2026-10-24) | `feature/roadmap-vista-por-comision` | `feature/roadmap-multi-vista-profesor` (T-62.5, ya rebaseada sobre `origin/develop`; decidido 2026-10-24: F7 arranca antes del merge) | F7, F8 |
| **Back, vista por comisión** | `~/dev/TPI_2026/Backend/tpi-roadmap-vista-comision` (creado 2026-10-24) | `feature/roadmap-vista-por-comision` | `origin/develop` | B4 (opcional) |

Reglas al crearlos, como en §1:

- Sin upstream hasta que T-62.5 esté mergeada; al entrar a `develop`, rebasear antes del primer push.
- Front: `npm ci` antes de empezar y tests con `NODE_OPTIONS=--no-experimental-webstorage`.
- Back: copiar la plantilla `.tpi/platform/` con soporte de variante y su `.env` desde `Backend/tpi-roadmap`, sin commitearla. La migración nueva, si hace falta, va después de V58: revisar `migration-vendor` y los PR abiertos antes de numerar.
- Con `ROADMAP_BY_GROUP_ENABLED=true` en el back de prueba, si no el alumno no ve ningún filtro.

**Orden para arrancar**

1. **F7** · selector de comisión del profesor (front, vista por comisión). Primero, porque es la pieza que no existe y no depende de ningún endpoint nuevo.
2. **F1 + F2** · pantalla "Configurar roadmaps" y comisiones desde la misma pantalla (front, configurar). Se pueden hacer en paralelo con F7 si hay dos personas; F4 se integra acá.
3. **F8** · ranking según el alcance (front, vista por comisión). Necesita decidir antes la hipótesis de D2 sobre `progress_scope`.
4. **B0** · test de integración del principal creado por POST (back, configurar). Se puede hacer en cualquier momento; no bloquea al front.
5. **B4** · validación de al menos un roadmap por comisión (back, vista por comisión). Opcional: hasta entonces avisa el front.

Paralelo con todo: abrir la issue a G01 (D3).

### 9.7 Lo que le pedimos a G01 al crear el curso (D3)

> [!warning] Descartado (2026-10-24)
> Benja decidió no abrir la issue: ya existen "crear grupos" y "gestionar roadmaps". La configuración pasa al momento de crear un grupo (§10). F3 queda descartada.

> [!info] Alcance
> Es lo mínimo para que el profesor llegue a "Configurar roadmaps" justo después de crear el curso, sin tocar el modal de 3 pasos. Corresponde a F3 de §6. La issue la abre Benja; este texto es el borrador. **Estado: sin abrir** (2026-10-24).

**Cómo es hoy (verificado 2026-10-24, front de `develop`)**

- "Crear curso" abre `course-cohort-form-modal` (3 pasos; 2 si se clona). Al confirmar, `course-list-page.component.ts` llama a `createCourseCohort` (o `cloneCourseCohort`), guarda la respuesta en la señal `createdCohort` (línea 721, asignada en 940 y 961), cierra el modal y recarga la lista.
- Con `createdCohort` se muestra un `generic-callout` de éxito ("Curso creado", con fechas, estado y código de invitación; plantilla alrededor de la línea 195). **No tiene ninguna acción.**
- El modal no tiene nada de roadmap ni de comisiones: las comisiones se crean después, en la pestaña Grupos.

**Qué pedimos (en orden de importancia)**

1. **Un botón en el aviso de "Curso creado".** `generic-button` (`genericButton` sobre un `<a>`, variante `secondary`) con el texto "Configurar roadmaps" que lleve a la pantalla de F1: `/roadmap/teacher/course/<cohort.id>/roadmaps/setup`. Solo se muestra a quien puede configurar (ADMIN, GESTOR o PROFESSOR dueño). **Cambio de unas 10 líneas en `course-list-page` y 2 claves de i18n.** Lo hacemos nosotros en un PR chico si G01 está de acuerdo, para no sumarles trabajo.
2. **Confirmar que el aviso se mantiene al clonar un curso.** Hoy `cloneCourseCohort` también llena `createdCohort`. Con HU-71 el clon puede traer los roadmaps y sus asignaciones; el botón sirve igual para revisarlos.
3. **Que no cambie el contrato de la respuesta de crear/clonar** (`CourseCohortResponse.id`), porque la ruta del botón depende de ese id.

**Qué no pedimos**

- No pedimos pasos nuevos en el modal ni que Courses conozca los roadmaps.
- No pedimos el alta de comisiones en esta pantalla: F2 solo manda al profesor a la pestaña Grupos y vuelve.
- **El evento `COURSE_COHORT_CREATED` queda fuera**, salvo que B0 falle (§5, D1, camino 2). Hoy `tpi-roadmap` no lo escucha y no está verificado que Courses lo publique.

**Qué hacemos nosotros mientras no responden**

- F1 y F2 funcionan igual: la entrada queda en la pestaña Roadmaps del curso, sin depender del aviso.
- F3 queda **bloqueada hasta que G01 diga que sí**; no se toca `course-list-page` sin su acuerdo.

**Criterio de listo (F3)**

- Tras crear o clonar un curso, el aviso muestra "Configurar roadmaps" solo a quien puede configurar, y el botón abre la pantalla de F1 con el id del curso nuevo.
- Hay tests del aviso con y sin permiso, y de la ruta que arma el botón.
- Sin regresiones en `course-list-page` ni en el modal.

**Borrador de la issue (para G01)**

> **Título:** Botón "Configurar roadmaps" en el aviso de curso creado
>
> **Contexto:** G10 (roadmap) está armando una pantalla para que el profesor decida cuántos roadmaps tiene el curso y cuáles ve cada comisión, y que cada comisión vea al menos uno. Hoy, al crear un curso, el aviso de éxito de `course-list-page` no ofrece ningún siguiente paso.
>
> **Pedido:** agregar al aviso de "Curso creado" un botón secundario "Configurar roadmaps" hacia `/roadmap/teacher/course/<id>/roadmaps/setup`, visible solo para ADMIN, GESTOR o PROFESSOR dueño del curso. No cambia el modal ni el contrato de Courses.
>
> **Quién lo hace:** podemos mandar nosotros el PR (≈10 líneas en `course-list-page` y 2 claves de i18n) si están de acuerdo.
>
> **Pregunta:** ¿les parece bien que toquemos ese archivo, y el aviso se mantiene al clonar?

> [!info] Actualización (2026-10-24) · base del worktree front
> El worktree `2026-PIV-TPI-FE-vista-comision` se movió a `e173e68c9`, la punta de `feature/roadmap-multi-vista-profesor` (T-62.5 + D-1 a D-3), para que F7 use la pestaña General con roadmap alternable antes del merge. **Cuando T-62.5 entre a `develop`:** `git rebase origin/develop` en esta rama; los 4 commits de T-62.5 se descartan solos si el merge conserva los parches, y si fue squash hay que usar `git rebase --onto origin/develop e173e68c9`.

### 9.8 Avance de implementación (2026-10-24)

> [!success] F7, F1 y F2 implementadas
> Las hizo codex (orquestado con Orca, run `run_a6bfbe42abe5`). Van **todas juntas en una sola PR a `develop`** junto con T-62.5, en vez de una PR por rama, para no esperar una aprobación por cada una.

**Rama de la PR:** `feature/roadmap-configurar-al-crear-curso` (worktree `~/dev/TPI_2026/Frontend/2026-PIV-TPI-FE-config-roadmaps`, recreado el 2026-10-24). Ya tiene mergeado `origin/develop` (`e8f9c6d50`). **Sin push ni PR todavía.** Los worktrees `vista-comision` y `multi-roadmap` quedan de más cuando se pushee.

| Tarea | Estado | Commits | Qué quedó |
|---|---|---|---|
| T-62.5 | ✅ en la rama | 4 commits hasta `e173e68c9` | Alternar roadmaps en General y mapa (ya no se sube por separado) |
| **F7** | ✅ hecha | `1388dbc52` (cherry-pick de `387415296`) | Selector de comisión sobre el de roadmap, en General y en el mapa. Filtra `visibleToAll` + `groupIds` de la comisión (`roadmapsVisibleToGroup`), cae al primero visible, aviso si la comisión no ve ninguno, se mantiene al ir al modo aventura |
| **F1** | ✅ hecha | `d50a27648`, `f1ff214ca` | Pantalla `roadmap/teacher/course/:id/roadmaps/setup` con entrada desde la pestaña Roadmaps. Modo compartido o uno por comisión, roadmaps extra, asignación de comisiones, aviso D4 que bloquea confirmar, creación en secuencia (principal → settings → resto → asignaciones) y reintento sin duplicar |
| **F2** | ✅ hecha | `d50a27648`, `f1ff214ca` | Sin comisiones: empty state con link a Grupos (el modo compartido sigue disponible) |
| F3 | ❌ descartada | — | Ver §10: no se pide nada a G01 |
| F8 | ✅ hecha | `f1acb864b` | Ranking del roadmap (`/roadmaps/{id}/ranking`) para el alumno con un roadmap de su grupo en scope `ROADMAP`; el profesor elige entre el del curso y el de cada roadmap separado (§10.4) |
| **F9** | ✅ hecha | `6af748f53` + fix | Modal al crear un grupo: compartir, nuevo o clonar (§10). El nuevo o clonado queda en scope `ROADMAP` y solo para el grupo, y los compartidos pasan a los grupos previos |
| B0, B4 | ⏸ sin empezar | — | Back |

**Merge con `develop` (2026-10-24, 239 commits):** 6 conflictos resueltos.

- El menú "Más acciones" de General pasó a un botón dorado "Roadmap" (M-09). El botón ahora lleva `?group=` y `?roadmap=` para que el mapa abra con la selección del profesor.
- El asistente guiado nuevo (E-12) de "Agregar contenido" **no aparece en los roadmaps no principales**, igual que las subsecciones. Es una línea si se quiere mostrar.

**Verificación:** con F9 y F8 (`6ac9ed4fc`), `npm run verify` pasó: 1414 archivos y 21.951 tests, 1 fallo esperado, 0 errores de lint. Antes, merge commiteado en `e8f9c6d50`. `npm run verify` completo pasó después del merge: 1412 archivos y 21.938 tests, 1 fallo esperado, 0 errores de lint (155 warnings).

## 10. Rediseño 2026-10-24 · el roadmap se elige al crear un grupo

> [!info] Decisión de Benja (2026-10-24)
> No se toca el alta del curso: no hay issue a G01 y F3 queda descartada. La regla sale de cómo están armados los grupos y los roadmaps, y la única pregunta nueva aparece **al crear un grupo**.

### 10.1 Reglas

| Grupos | Roadmaps | Resultado | Ranking |
|---|---|---|---|
| 0 o 1 | 1 | Como hoy: un roadmap para todos | Compartido |
| Varios | 1 | El mismo roadmap para todos los grupos | Compartido: el contenido es igual |
| 0 o 1 | Varios | Todos ven todos los roadmaps | Compartido |
| **Se crea un grupo nuevo y ya hay otro grupo y al menos un roadmap** | — | **Se pregunta:** compartir, nuevo desde 0 o clonar | Según la opción |

**Las tres opciones, al crear el grupo G:**

1. **Compartir el vigente.** G usa un roadmap que ya existe; si hay varios, se elige cuál. Si ese roadmap es `visibleToAll`, no se cambia nada. Si está asignado a algunos grupos, se agrega G a sus `groupIds`. **Ranking compartido** con los grupos que usan ese roadmap.
2. **Nuevo desde 0.** Se crea un roadmap vacío solo para G. Si hacía falta, se enciende antes `multipleRoadmapsAllowed`. **Ranking separado.**
3. **Clonar.** Se clona el vigente en el mismo curso (`POST /roadmaps/{id}/clone` con `targetCourseId` = el curso, ya existe por T-71.3), con su estructura y sin el progreso, y se asigna solo a G. **Ranking separado.**

> [!warning] Detalle clave de las opciones 2 y 3
> Para que G quede separado, los roadmaps que hoy son `visibleToAll` pasan a estar asignados a **los grupos que ya existían**, sin G. Si no se hace, G seguiría viendo el roadmap compartido y su contenido y su ranking se mezclarían.
> - **Riesgo:** un alumno que no está en ningún grupo deja de ver esos roadmaps cuando `ROADMAP_BY_GROUP_ENABLED` está encendido.
> - **Qué hacer:** el modal lo avisa si el curso tiene alumnos sin grupo.

### 10.2 Ranking separado (F8)

Verificado en el back (`origin/develop` `0f3b4b9d`, `RankingController`):

- `GET /roadmaps/{id}/ranking` solo es un ranking propio del roadmap si su `progress_scope` es **`ROADMAP`**. Con **`COURSE`** devuelve el ranking del curso, con todos los alumnos mezclados.
- `GET /courses/{id}/ranking?group_id=` filtra por **un solo** grupo.

**Consecuencia:** con `progress_scope` como está hoy (`COURSE`), los grupos separados no tienen rankings distintos. La única salida sería filtrar por grupo, y eso rompe el caso de dos grupos que comparten roadmap mientras un tercero tiene el suyo: el ranking de A no incluiría a B. Se resolvió en §10.4.

### 10.3 Tareas

| Tarea | Qué | Dónde | Estado |
|---|---|---|---|
| **F9** | ✅ **Hecha 2026-10-24** (`6af748f53` + fix de reintento). Modal "¿Qué roadmap usa este grupo?" después de crear un grupo, con las 3 opciones de §10.1, el aviso de alumnos sin grupo, reintento si falla a mitad y cancelar = compartir (el comportamiento de hoy). Componente en `features/roadmap/ui/`; `cohort-groups-page` solo lo abre después de `createGroup` | front, `cohort-groups-page` (Courses) + roadmap | ✅ hecha |
| **F8** | Ranking según el alcance: si el roadmap del alumno es solo de su grupo, `/roadmaps/{id}/ranking`; si no, el del curso. Falta agregar esa consulta a `ranking-data.port.ts` | front, `features/ranking` | ✅ hecha (`f1acb864b`) |
| F1/F2 | La pantalla "Configurar roadmaps" queda como atajo para armar todo de una vez, con las mismas reglas | ya hecha | ✅ |
| F7 | Selector de comisión del profesor | ya hecha | ✅ |
| F3 | Botón en el aviso de curso creado | — | ❌ descartada |
| **B0** | Tests: el principal creado por POST recibe las secciones de Courses; si fallan, arreglar la reconciliación | back `tpi-roadmap-vista-comision`, rama `feature/roadmap-vista-por-comision` | 🔄 en curso (codex, 2026-10-24) |
| **B4** | **Obligatoria** (Benja, 2026-10-24). Cada grupo ve siempre al menos un roadmap: 409 `roadmap.group-uncovered` en `assignGroups` y `archive` | mismo worktree back | 🔄 en curso (codex, 2026-10-24) |
| Flag | `ROADMAP_BY_GROUP_ENABLED=true`: lo prueba Benja a mano | entorno | ⏸ manual |

### 10.4 Decisión (Benja, 2026-10-24): los separados pasan a `ROADMAP`

> [!success] Resuelta
> Un roadmap que se crea nuevo o se clona para un grupo queda con `progress_scope = ROADMAP`, y tiene ranking propio en `/roadmaps/{id}/ranking`. Los que ya existían no cambian de scope, para no tocar el XP que ya se ganó.
>
> **Límite conocido:** el ranking del curso de los grupos que comparten roadmap puede listar al final, con 0 XP, a alumnos de los grupos separados. Se revisa al probar F8.

Opciones que se compararon:

- **Recomendado:** pasa a `ROADMAP` solo, al crearlo o clonarlo para un grupo (`PATCH` con `progressScope`, que ya existe). Así su ranking es propio, y los compartidos siguen en `COURSE`.
- **Alternativa:** dejarlo en `COURSE` y que el ranking del alumno se filtre por su grupo. No hace falta tocar el scope, pero los grupos que comparten roadmap no comparten ranking.
