# Front general y editor de ROADMAP — insumos para presentación

**Alcance y evidencia.** Lectura estática del front en `origin/develop` (HEAD `d1c5766227`), sin ejecutar aplicación, builds ni pruebas. Las rutas siguientes son relativas a `/Users/benjaminpolzoni/dev/TPI_2026/_presentacion-src/fe/`, salvo indicación. «Existe en código» significa que hay interfaz y lógica conectada, no que se haya comprobado el ambiente integrado ni que todos los servicios respondan. No se analizó el render 3D. El vault contiene historias y planes, pero no se usa como evidencia de funcionalidad entregada.

## 1. Arquitectura general — verificado en código

### Explicación de producto/técnica media

Roadmap está integrado al curso: Angular ofrece pantallas distintas para editar, jugar y seguir el progreso; el servidor conserva la autoridad.

### Detalle técnico

- Angular `^22.2.3` (`package.json:69`), organizado por funcionalidades en `src/app/features/roadmap/`, con páginas, componentes de interfaz `ui`, dominio y acceso a datos. Las rutas se cargan bajo el shell autenticado: `roadmap` y `ranking` son funcionalidades hermanas (`src/app/core/routing/authenticated-shell.routes.ts:219-228`).
- `ROADMAP_ROUTES` monta un shell propio y providers compartidos; carga páginas en forma diferida. Incluye inicio docente, editor `teacher/course/:id/map`, gestión `roadmaps` y `roadmaps/setup`, catálogo `badges`, progreso docente `teacher/progress/:id`, y experiencia del alumno `play/:id` y `play/:id/:sectionId`. La antigua portada de alumno redirige a Cursos; las vistas de juego están bajo un gate de escritorio (`src/app/features/roadmap/roadmap.routes.ts:57-180`).
- Estado mediante servicios y stores con señales: `RoadmapStore`, selección de roadmap y adaptadores inyectados por providers; HTTP real para roadmap, insignias y progreso (`src/app/features/roadmap/roadmap.providers.ts:17-44`). Existe también un adaptador en memoria para escenarios aislados, por lo que no corresponde presentar sus datos de ejemplo como producción (`src/app/features/roadmap/data-access/roadmap/in-memory-roadmap.adapter.ts:57`).
- `HttpGenericService` y adaptadores HTTP encapsulan lecturas/escrituras; el entorno usa `/api` y Roadmap agrega `/roadmap`, es decir `/api/roadmap/**` a través del gateway (`src/environments/environment.ts:4`, `src/app/features/roadmap/data-access/roadmap-http/http-roadmap.adapter.ts:115-119`). La configuración real de infraestructura no fue comprobada.
- Las rutas docentes usan `permissionGuard('editRoadmap')`; el guard consulta el snapshot de capacidades y resuelve carga, denegación y errores, no solo oculta botones (`src/app/features/roadmap/roadmap.routes.ts:25-29,65-88`; `src/app/core/guards/permission.guard.ts:40-93`). El catálogo tiene permisos propios (`src/app/features/roadmap/pages/teacher-home-page/teacher-home-page.component.ts:74`). Esto es control de interfaz: la autorización del servidor debe verificarse aparte.

## 2. Docente: primer roadmap y edición

### Explicación de producto/técnica media

El docente parte del curso y sus unidades, deja que se sincronicen o usa el asistente, y luego organiza contenidos y dependencias en el mapa.

### Detalle técnico

- El curso y sus unidades nacen en **Courses**, no en el inicio docente de Roadmap. Allí se listan las cohortes activas, borrador y archivadas; las archivadas se presentan de solo lectura (`src/app/features/roadmap/pages/teacher-home-page/teacher-home-page.component.ts:45-48,91-106`).
- Al abrir la edición se lee el roadmap y, una vez terminada la lectura, se sincronizan automáticamente las secciones de Courses; si todavía no existe un roadmap, la sincronización puede construirlo. No hay botón de sincronizar; los errores sí se muestran y permiten reintentar. La sincronización refleja las secciones en el roadmap principal, no en los alternativos (`src/app/features/roadmap/embeds/course-status/roadmap-course-status.component.ts:9-12,30-36,74-80,97-120`). **No afirmar que el alta inicial es exclusivamente manual.**
- Además hay un asistente de configuración: para un curso nuevo ofrece uno compartido o borradores por comisión; se valida nombre no vacío y longitud máxima, se crea el primero y luego los demás con su asignación. Si una parte ya se creó, el reintento conserva ese resultado y completa lo pendiente (`src/app/features/roadmap/pages/roadmap-setup-page/roadmap-setup-page.component.ts:118-126,145-165,177-207,249-273`).
- El mapa unificado permite inspeccionar unidades, nodos y reglas; la edición de contenido de nodos se integra en la sección de Courses (`src/app/features/roadmap/roadmap.routes.ts:89-112`; `src/app/features/roadmap/pages/course-editor-page/course-editor-page.component.ts:55-61`). Hay alta de nodos de lectura y desafíos, vinculación de materiales, y posibilidad de cargar archivos o enlaces publicados en Courses; la creación de lectura se agrega al final de su unidad y admite carga por lotes (`src/app/features/roadmap/embeds/section-nodes/roadmap-section-nodes.component.ts:523-535,1722-1725,1936`; `src/app/features/roadmap/pages/content-node-create-page/content-node-create-page.component.ts:72-99,268-272,294-309`).
- Al relacionar dos elementos se ofrece **Requiere**, **Recomienda** o **Relacionado**. La primera representa una regla de desbloqueo; las otras son relaciones informativas. El front rechaza conectar un elemento consigo mismo y duplicados del mismo tipo; para requisitos evalúa también ciclos, incluso transitivos, y restricciones de contención. No deja usar como requisito nodos opcionales, de recuperación o límites del sistema; se excluyen referencias inexistentes o inválidas (`src/app/features/roadmap/pages/graph-editor-page/graph-editor-page.component.ts:3249-3312`; `src/app/features/roadmap/domain/prerequisite-policy.ts:18-30,80-91,251-262`; `src/app/features/roadmap/ui/learning-map-canvas/learning-map-canvas.component.ts:1870`).
- START y END son límites conectados por el sistema, no prerrequisitos elegidos por el docente (`src/app/features/roadmap/embeds/section-nodes/roadmap-section-nodes.component.ts:1114`; `src/app/features/roadmap/domain/prerequisite-policy.ts:18-21`). Las reglas admiten grupos AND/OR y XP mínimo (`src/app/features/roadmap/roadmap.routes.ts:72-75`). Al guardar una conexión no se altera el grafo confirmado hasta completar una nueva lectura exitosa (`src/app/features/roadmap/pages/graph-editor-page/graph-editor-session.ts:148-149`).
- Se pueden reordenar nodos por arrastre en el mapa y por acciones en las listas; también se envía el nuevo orden de unidades (`src/app/features/roadmap/ui/learning-map-canvas/learning-map-canvas.component.ts:449,2765`; `src/app/features/roadmap/pages/graph-editor-page/graph-editor-page.component.ts:1396,1646,2491`; `src/app/features/roadmap/embeds/section-nodes/roadmap-section-nodes.component.html:186`).
- **Publicación:** distinguir publicar archivos/material en Courses, publicar un desafío y disponibilizar su nodo; el front distingue desafío publicado de borrador (`src/app/features/roadmap/embeds/section-nodes/roadmap-section-nodes.component.ts:2136-2158`). No se verificó un botón de «publicar el roadmap completo»: no prometerlo ni confundirlo con publicar un recurso.

## 3. Varios roadmaps, comisiones y visibilidad

### Explicación de producto/técnica media

Un curso puede tener un mapa principal y alternativas destinadas a distintas comisiones; la interfaz permite elegir contexto y filtrar.

### Detalle técnico

- Hay pestaña de roadmaps del curso: listar, crear, renombrar, definir principal, archivar y clonar; los comandos HTTP incluyen asignación a grupos y clonación (`src/app/features/roadmap/roadmap.routes.ts:114-128`; `src/app/features/roadmap/data-access/course-roadmaps/course-roadmaps.service.ts:92-113,126-153,174-176`).
- El editor abre el principal por defecto o uno alternativo mediante `?roadmap=<id>`; muestra que se está editando otro. La lista explica audiencia general o grupos asignados y contempla grupos borrados (`src/app/features/roadmap/pages/course-editor-page/course-editor-page.component.ts:49-61,95-98,168-171`; `src/app/features/roadmap/ui/course-roadmaps-list/course-roadmaps-list.component.ts:56-68,91-102`).
- La interfaz ofrece asignación por comisión y modo compartido (`src/app/features/roadmap/pages/roadmap-setup-page/roadmap-setup-page.component.ts:145-163,270-273`). No se comprobó con cuentas reales el filtrado efectivo ni los casos de alumno en varias comisiones: mostrarlo solo con datos y permisos preparados.

### Selección, filtros y posición: precisión actual

**Explicación de producto/técnica media.** En el mar aparecen selectores si hay más de una comisión o roadmap disponible. En el editor se filtra por comisión y por tipo de vínculo. Arrastrar para ordenar contenido no es lo mismo que acomodar visualmente el mapa.

**Detalle técnico.** Los selectores de alumno se muestran con más de una opción y envían la selección al store (`src/app/features/roadmap/pages/worlds-page/worlds-page.component.ts:163-182,487-489,562-565`). El editor filtra los nodos por grupo y ofrece todas/requiere/informativas (`src/app/features/roadmap/pages/graph-editor-page/graph-editor-page.component.ts:535-544,859-862`); ocultar el dibujo de REQUIRES no elimina su efecto (`:1483-1497`). Drag de nodo solicita reordenar o mover a otra sección (`src/app/features/roadmap/ui/learning-map-canvas/learning-map-canvas.component.ts:2756-2767`). El layout visual de regiones y rutas sí intenta persistirse en servidor con ETag, respaldo local y resolución de cambios pendientes; si el endpoint falla queda local y no se garantiza compartirlo (`src/app/features/roadmap/data-access/roadmap/roadmap-layout.store.ts:129-173,215-250,364-417`; clave local por organización/usuario/curso/roadmap en `src/app/features/roadmap/pages/graph-editor-page/graph-editor-page.component.ts:1505-1513`). No confundirlo con una posición 3D ni prometer que cualquier drag de nodo guarda coordenadas libres.

## 4. Alumno

### Explicación de producto/técnica media

El alumno entra desde Cursos, elige el mapa disponible y recorre actividades, progreso e insignias.

### Detalle técnico

- Desde Cursos entra al hub y a las unidades del mapa; el hub muestra nivel y XP total y enlaza al ranking (`src/app/features/roadmap/roadmap.routes.ts:150-179`; `src/app/features/roadmap/pages/worlds-page/worlds-page.component.ts:188-202,478-479`). Los desbloqueos dependen también de XP además de nodos completados (`src/app/features/roadmap/pages/worlds-page/worlds-page.component.ts:802`).
- El mundo de unidad conecta el inicio de intentos con confirmación, sus ítems y bloqueo, y utiliza servicios de feedback, resumen por ítem y resultado económico; la pantalla considera estado, veredicto e intentos restantes (`src/app/features/roadmap/pages/hex-world-page/hex-world-page.component.ts:126-150,360-390,571-575`). No se verificó una corrección real ni disponibilidad de feedback para todos los tipos de desafío.
- Existen catálogo de insignias y componentes de insignias del estudiante; el catálogo docente es una ruta diferenciada (`src/app/features/roadmap/roadmap.routes.ts:130-137,180-186`; `src/app/features/roadmap/ui/student-badges/student-badges.component.ts:1`; `src/app/features/roadmap/pages/badges-catalog-page/badges-catalog-page.component.ts:1`). El ranking es una funcionalidad hermana, no una pantalla interna del editor (`src/app/core/routing/authenticated-shell.routes.ts:224-228`).

## 5. Docente: seguimiento y cierre

### Explicación de producto/técnica media

El docente puede observar avances por comisión; otras pantallas de cohorte y cierre pertenecen a Courses o Backoffice.

### Detalle técnico

- En `teacher/progress/:id` se elige comisión y se ve por alumno XP y avance: nodos completados sobre total. Con al menos dos comisiones hay tabla comparativa. El ranking enlazado es de **toda la cohorte**, no queda filtrado por la comisión elegida (`src/app/features/roadmap/pages/group-progress-page/group-progress-page.component.ts:54-59,102-107,143-188,248-258,327-342`).
- El dashboard general de cohorte vive en **Courses**, no exclusivamente en Roadmap; consulta resumen, progreso, evolución de XP y otros bloques (`src/app/features/courses/pages/cohort-dashboard-page/cohort-dashboard-page.component.ts:140-163`). El bloque de riesgo/salud viene de Backoffice y requiere capacidad específica (`src/app/features/courses/pages/cohort-dashboard-page/cohort-dashboard-page.component.ts:68,189-195`; `src/app/features/courses/pages/cohort-dashboard-page/cohort-dashboard-page.component.html:63-68`). No atribuirlo al motor Roadmap.
- El listado distingue cursos archivados y limita edición; el front de Courses modela errores y condiciones de archivado (`src/app/features/roadmap/pages/teacher-home-page/teacher-home-page.component.ts:45-48`; `src/app/features/courses/data-access/cohort-archive.models.ts:7,69-94`). No se comprobó aquí el flujo de cierre completo ni sus efectos reales sobre todos los roadmaps.

## Ranking: datos del servidor y cálculos de interfaz

### Explicación de producto/técnica media

El back entrega el ranking y recorta los datos según el rol; el front los presenta, arma posiciones visuales y permite al staff comparar comisiones. Por eso una posición o zona visual puede diferir del puesto empatado recibido.

### Detalle técnico

- El DTO trae posición, percentil, zona, XP y estadísticas; el adaptador consulta `/courses/{id}/ranking` o `/roadmaps/{id}/ranking` y completa identidades y grupos desde Courses (`src/app/features/ranking/data-access/ranking-http/backend-ranking.dto.ts:33-50,73-94`; `http-ranking.adapter.ts:119-129,169-184`). El mapper no calcula el ranking base y redondea promedios (`ranking-mapper.ts:71-87,142-155`).
- Para su presentación el front numera consecutivamente respetando orden de posiciones del servidor; con lista parcial conserva huecos. Calcula percentil `round((total-puesto+1)*100/total)` y zonas por primer/último décimo, solo desde 10 inscriptos; visualmente pueden diferir de empates del back (`src/app/features/ranking/domain/ranking.rules.ts:26,289-318`; `src/app/features/ranking/pages/ranking-page/ranking-page.component.ts:1078-1086`).
- En otra vista de orden, `rankBy` compara XP o nota, luego insignias, menos vidas perdidas, ejercicios y fecha de logro; si faltan vidas ese criterio es neutral para el empate (`ranking.rules.ts:164-224`). La vista de staff puede preferir orden personal en almacenamiento local (`src/app/features/ranking/data-access/ranking-view-preference.ts:69-85`). No confundirlo con cambiar el criterio oficial.
- El ranking de grupos se calcula en el front cruzando integrantes con filas recibidas: promedio XP de miembros encontrados, nota solo de quienes tienen nota, redondeo a un decimal, desempate por otra métrica y nombre; excluye grupos sin integrantes encontrados (`ranking.rules.ts:227-286`; `ranking-page.component.ts:982-992`). La DEC-022 documenta estas decisiones, pero no prueba que el entorno esté operativo.

## 6. Recorrido sugerido de demo

1. **Profesor / Cursos:** abrir una cohorte activa ya preparada y explicar que unidades y curso pertenecen a Courses. Si se quiere mostrar el primer alta, hacerlo en una cohorte limpia y confirmar previamente el comportamiento de sincronización.
2. **Roadmaps:** mostrar lista, principal y alternativa; abrir el asistente y audiencia por comisiones sin confirmar cambios que afecten la demo.
3. **Contenido de una unidad:** agregar o mostrar una lectura y un desafío ya publicado; explicar que el recurso y el nodo son cosas distintas.
4. **Mapa docente:** señalar unidades y nodos, crear o mostrar una relación «Requiere» y una informativa; intentar un ciclo o duplicado para mostrar el motivo del rechazo. Mostrar reordenamiento y regla de desbloqueo. Preparar nodos obligatorios válidos.
5. **Alumno:** ingresar con cuenta inscripta en comisión habilitada; mostrar mapa, un contenido disponible y otro condicionado, XP y un intento con feedback ya preparado. Luego mostrar insignias y ranking de cohorte.
6. **Profesor / seguimiento:** mostrar progreso por comisión y comparación; aclarar alcance del ranking. Si hay permisos y datos reales, mostrar dashboard de Courses y riesgo de Backoffice como integración, no como funcionalidad exclusiva G10.
7. **Cierre:** si se incluye, usar una cohorte descartable y verificar previamente las condiciones; archivar cambia el estado y no conviene ejecutar esto en la cohorte principal de demo.

**Preparación indispensable:** gateway y servicios disponibles, escritorio compatible, cuentas docente/alumno en la organización correcta, permisos, cohorte con comisiones, nodos y resultados precargados. Este informe no demuestra funcionamiento extremo a extremo.

## 7. Planes del cerebro versus código

### Explicación de producto/técnica media

El cerebro explica decisiones y ofrece una demo conceptual del grafo; no es una base de datos ni prueba de despliegue.

### Detalle técnico

La guía `tpi-g10-cerebro/demo-neo4j/README.md` advierte que las notas y UUID son simulados y no sincronizan con Neo4j. `tpi-g10-cerebro/arquitectura/mapa-modelo-neo4j.md` describe el modelo; DEC-016 queda precisada por DEC-021: Postgres fuente de escritura, Neo4j proyección de lectura; DEC-018 documenta catálogo y DEC-022 visualización del ranking. Son documentación, no verificación de implementación o datos en vivo. El cerebro contiene historias sobre múltiples roadmaps y visibilidad por grupo (`tpi-g10-cerebro/sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable.md`, `tpi-g10-cerebro/sprints/sprint-3/historias/HU-61 Roadmaps por grupo del curso y restricciones de visualización.md`) y un plan de cierre (`tpi-g10-cerebro/sprints/sprint-4/Planes/Benja/HU-72 Back+Front - cierre del curso y roadmap archivado.md`). La existencia de esos documentos **no prueba** que todo su alcance esté implementado; para la presentación usar exclusivamente los comportamientos concretos y citas de código de las secciones anteriores. No se realizó una comparación exhaustiva de cada criterio del vault.

## Dudas para el usuario

- ¿La demo debe incluir dashboard de Courses, salud de Backoffice y ranking de otra feature, o limitarse a lo que desarrolla G10?
- ¿Quieren mostrar creación inicial desde curso vacío? Hay dos caminos visibles —sincronización automática y asistente— y conviene acordar cuál mostrar tras comprobarlo en el ambiente.
- ¿Se incluye cierre real de curso? Sus precondiciones y efectos transversales requieren validación integrada; el plan HU-72 por sí solo no alcanza como prueba.
- ¿Hay datos preparados para demostrar diferencias de visibilidad entre comisiones, feedback e insignias sin depender de tiempos de procesamiento?
- ¿Qué entienden por «publicar roadmap»: publicar desafíos/materiales o una publicación global? En esta revisión no se verificó un comando global.
