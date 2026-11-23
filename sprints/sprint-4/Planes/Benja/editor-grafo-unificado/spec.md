# Spec: editor de grafo unificado del roadmap

Decisiones que mandan sobre la propuesta (2026-10-28): (1) toda flecha es una regla de desbloqueo; (2) `/map` es la única ruta del editor. Ver «Enmiendas» en `proposal.md`.

Convención: «regla» = relación REQUIRES. «B requiere A» = flecha de A hacia B. Nodo = actividad; sección = unidad o subsección.

## Respuestas a las preguntas abiertas (leídas del código)

**Claves `courseMap.*` fuera de `pages/course-map-page`** (`src/assets/i18n/{es,en}.json`, bloque `courseMap`):
| Clave | Dónde se usa | Destino |
|---|---|---|
| `courseMap.mapView` | `roadmap.routes.ts:74` (título de `/map`) | Se conserva, o se renombra a `graphEditor.title` |
| `courseMap.cannotConnect`, `cannotConnectReason`, `connected` | `graph-editor-page.component.ts` ~1825-1876 | Se conservan |
| `courseMap.swapSaved/swapFailed/moveSaved/moveFailed/moveUnsupported` | `roadmap.store.ts` 1323-1361 | Se conservan |
| `courseMap.statusCompleted` | `ui/prerequisite-chips` | Se conserva |
| `courseMap.edgeTypes.*`, `courseMap.hiddenEdge` | `generic-graph.models.ts`, `graph-view.mapper.ts` (y sus specs) | Se conservan: describen relaciones que existen en la base |
| `courseMap.hiddenUnit`, `list*`, `emptyUnitNotice`, `nodesBadgeLabel` | solo `ui/map-unit-list`, que solo usa `course-map-page` | Quedan huérfanas: borrar el componente y las claves |

Las otras ~80 claves que usa la página borrada se limpian solo tras un grep por clave (es y en a la vez).

**Qué espera la vista simple para mostrar reglas.** Es `embeds/section-nodes`. Calcula el texto «Requiere: …» con `nodeRequirementsOf` (`node-requirements.ts`): toma `combinedRuleOf(node)` (árbol de reglas) o, si no hay, `prerequisitesOf(connectionsWithoutBoundary(sections, connections), node.id)` más `prerequisiteModeOf(node)`, y lo redacta con `describeRuleTree`/`describeRule`. Solo lee conexiones REQUIRES y reglas de nodo; no usa relaciones informativas. Por eso no hay que tocar el contrato de datos: las flechas del grafo deben escribirse por el mismo camino (`saveRules`) para que ese texto cambie solo.

## R1. Ruta única

- R1.1 `/roadmap/teacher/course/:id/map` MUST montar `GraphEditorPageComponent` con `unsavedChangesGuard`.
- R1.2 `/graph` MUST redirigir a `/map`; `/list` y las rutas viejas ya redirigen. No MUST quedar más de una pestaña de mapa.
- R1.3 `pages/course-map-page/**` y `ui/map-unit-list` MUST eliminarse sin dejar imports rotos.

#### Escenario: enlace viejo
- GIVEN un enlace guardado a `.../graph`
- WHEN el profesor lo abre
- THEN termina en `.../map` con el editor y una sola pestaña de mapa.

#### Escenario: salir con cambios sin guardar
- GIVEN hay una escritura pendiente o fallida
- WHEN el profesor navega fuera de `/map`
- THEN `unsavedChangesGuard` pide confirmación.

## R2. Lienzo y conexión

- R2.1 El lienzo MUST ser un solo modo, con puertos de entrada y salida en cada nodo y sección.
- R2.2 Arrastrar de A a B MUST crear «B requiere A» directamente. NO MUST haber selector de tipo.
- R2.3 El editor MUST NOT crear, editar ni mostrar relaciones informativas; las existentes en la base MUST permanecer intactas.
- R2.4 Durante el arrastre MUST verse una flecha fantasma; si el destino es inválido, MUST mostrar el motivo.
- R2.5 Soltar en el vacío MUST abrir el asistente para un nodo nuevo que ya requiere a A.
- R2.6 Las reglas de sección (`saveUnitRules`) admiten hojas tipadas `SECTION` y `NODE`; las de nodo (`saveRules`), las hojas admitidas por su contrato. El back valida elegibilidad y contención.

#### Escenario: crear una regla
- GIVEN dos nodos A y B sin relación
- WHEN se arrastra de A a B
- THEN se llama a `saveRules` de B con A y B muestra «Requiere: A» tras releer.

#### Escenario: ciclo
- GIVEN B requiere A
- WHEN se arrastra de B a A
- THEN el preflight puede anticipar el motivo «ciclo», pero el intento de guardar se valida en el back; solo una respuesta 2xx confirma la flecha y el rechazo backend restaura el estado confirmado.

#### Escenario: contención
- GIVEN el nodo N está dentro de la sección S
- WHEN se arrastra entre N y S (en cualquier sentido)
- THEN el preflight puede advertir la contención y, si se intenta guardar, el back decide; su rechazo no cambia la regla confirmada.

#### Escenario: nodo externo hacia sección
- GIVEN el nodo X está fuera de la unidad U y de todas sus subsecciones
- WHEN arrastro X → U
- THEN se guarda la regla de U con la hoja X vía `PATCH /sections/{U}/rules`, y solo se muestra guardado tras 2xx.

#### Escenario: nodo contenido hacia sección
- GIVEN el nodo N está dentro de U o de una de sus subsecciones
- WHEN se arrastra N → U
- THEN la contención se puede advertir como preflight, el back rechaza el intento y no cambia la regla confirmada.

#### Escenario: duplicado
- GIVEN B ya requiere A
- WHEN se vuelve a arrastrar de A a B
- THEN el front puede avisar que la hoja parece duplicada; el back valida igualmente cada intento de guardado y la UI no afirma éxito sin 2xx.

#### Escenario: relaciones informativas existentes
- GIVEN la base tiene una RECOMMENDS entre A y B
- WHEN se abre y se guarda el editor
- THEN la relación no se dibuja ni se modifica ni se borra.

## R3. Marcos anidados y colapso

- R3.1 Las subsecciones MUST dibujarse como marcos anidados dentro de su sección, con su nivel visible.
- R3.2 Un marco MUST poder colapsarse y expandirse con ratón y con teclado.
- R3.3 Las flechas de nodos ocultos por un marco colapsado MUST plegarse al borde del marco, y MUST seguir siendo conectables.
- R3.4 Una sección vacía MUST dibujarse como marco con un aviso de vacío y una acción «agregar nodo».

#### Escenario: flecha hacia un marco colapsado
- GIVEN el marco M está colapsado y contiene a X
- WHEN se arrastra de A al marco M
- THEN si A es un nodo externo elegible, se guarda como hoja `NODE` de la regla de M; si viola contención, se rechaza. Nunca se redirige implícitamente a X.

#### Escenario: plegado de flechas
- GIVEN X requiere A y M, que contiene a X, se colapsa
- WHEN se dibuja el lienzo
- THEN la flecha llega al borde de M y al expandir vuelve a X.

#### Escenario: sección vacía
- GIVEN una sección sin nodos
- WHEN se renderiza
- THEN muestra el marco con el aviso, sin error de layout.

## R4. Creación con el asistente

- R4.1 La creación MUST usar `NodeCreationWizardComponent` en el panel derecho, con la sección y el requisito precargados.
- R4.2 Debe poder crearse unidad, subsección (`addZone`), los dos tipos de desafío y un contenido, con las validaciones de General.
- R4.3 Tras soltar en el vacío, el nodo y su regla MUST guardarse como un solo flujo; si la regla falla, ver R5.3.

#### Escenario: nodo desde el vacío
- GIVEN se soltó una flecha desde A sobre el vacío dentro de la sección S
- WHEN el profesor completa el asistente
- THEN se llama a `addActivity` en S y luego a `saveRules` con A, y el nodo aparece con su flecha.

#### Escenario: cancelar
- GIVEN el asistente abierto desde el vacío
- WHEN se cancela
- THEN no se llama al back y desaparece la flecha fantasma.

## R5. Persistencia y estado de guardado

- R5.1 El grafo MUST NOT guardar estado propio: cada mutación pasa por `RoadmapStore`, llama al back y relee.
- R5.2 La barra MUST mostrar el estado: guardando, guardado o error, y MUST anunciarlo en `aria-live`.
- R5.3 Ante un error del back, el lienzo MUST volver al último estado confirmado, mostrar el mensaje y conservar el contexto para reintentar.

#### Escenario: error del back
- GIVEN `saveRules` responde 4xx/5xx al crear una flecha
- WHEN la respuesta llega
- THEN la flecha desaparece, se muestra el error con `GenericCallout`/aviso y el estado queda en «error».

#### Escenario: nodo creado, regla fallida
- GIVEN `addActivity` tuvo éxito y `saveRules` falla
- WHEN llega el error
- THEN el nodo se conserva sin regla y se avisa que falta; no hay nodo fantasma.

## R6. Movimiento de nodos

- R6.1 Mover un nodo entre secciones MUST usar `moveActivityToSection`, tras validar la contención en el front.
- R6.2 Mover MUST NOT borrar reglas; si la mudanza dejaría una regla inválida (nodo dentro de su sección-requisito), MUST rechazarse.
- R6.3 Reordenar dentro de la misma sección MUST ser posible sin tocar reglas.

#### Escenario: mudanza válida
- GIVEN N en S1 y S2 no está relacionada con N por una regla de contención
- WHEN se mueve N a S2
- THEN se llama a `moveActivityToSection` y las reglas de N permanecen.

#### Escenario: mudanza inválida
- GIVEN S2 es requisito de N
- WHEN se intenta mover N dentro de S2
- THEN el preflight puede advertir la contención, pero la decisión final es del back; un rechazo restaura la ubicación confirmada.

## R7. Árbol plegable y panel de resumen

- R7.1 Un árbol de estructura plegable MUST listar secciones y nodos, y seleccionar uno MUST centrarlo y seleccionarlo en el lienzo.
- R7.2 El panel de resumen MUST mostrar, del seleccionado, sus requisitos y sus dependientes, con acciones para quitar una regla.
- R7.3 La barra superior MUST quedar sin controles de modo.

#### Escenario: seleccionar desde el árbol
- GIVEN un nodo dentro de un marco colapsado
- WHEN se elige en el árbol
- THEN el marco se expande y el nodo queda seleccionado y en vista.

## R8. Forma del nodo

- R8.1 El nodo MUST poder mostrarse como tarjeta o como círculo, con la preferencia en `localStorage` (con try/catch y valor por defecto si falla).
- R8.2 Ambas formas MUST mostrar la misma información (nombre, tipo, obligatoriedad, estado de requisitos).

#### Escenario: preferencia
- GIVEN se eligió círculo
- WHEN se recarga la página
- THEN se vuelve a ver en círculo; con `localStorage` bloqueado, se ve la tarjeta.

## R9. Reflejo en la vista simple y en el roadmap del alumno

- R9.1 Una regla creada en el grafo MUST verse como «Requiere: …» en `embeds/section-nodes` sin cambios de contrato (ver respuesta arriba).
- R9.2 `embeds/section-nodes` MUST ofrecer un chip de requisitos y «Conexiones».
- R9.3 El roadmap del alumno MUST mostrar la misma regla y su bloqueo; las relaciones informativas existentes siguen su filtro actual (`visible`/`hiddenTypes`) y no se tocan.

#### Escenario: regla visible en la vista simple
- GIVEN se creó «B requiere A» en el grafo
- WHEN se abre la vista simple de la sección
- THEN B muestra «Requiere: A».

#### Escenario: alumno
- GIVEN A no está completado
- WHEN el alumno ve B
- THEN B aparece bloqueado por A.

## R10. Accesibilidad (WCAG 2.2 AA)

- R10.1 Ninguna acción MUST depender solo de arrastrar, del hover o del color.
- R10.2 `C` MUST iniciar una conexión desde el elemento enfocado (elegir destino, `Enter` confirma, `Esc` cancela); `N` MUST abrir el asistente para un nodo nuevo que requiere al enfocado.
- R10.3 El asistente MUST ofrecer un selector de sección, y el panel una lista de conexiones con «quitar».
- R10.4 Cada resultado (creada, rechazada con motivo, error, colapso) MUST anunciarse en `aria-live`.
- R10.5 Las flechas válidas e inválidas MUST distinguirse además del color (trazo, icono o texto).

#### Escenario: conexión con teclado
- GIVEN el foco en el nodo A
- WHEN se pulsa `C`, se elige B y `Enter`
- THEN se crea «B requiere A» y se anuncia «conectado».

#### Escenario: rechazo con teclado
- GIVEN el foco en A y B requiere A
- WHEN se pulsa `C` y se elige A como destino de B (ciclo)
- THEN no se crea y se anuncia el motivo.


## R11 — El back es la autoridad

- R11.1 Toda validación local (ciclo, contención, tipo, duplicados, profundidad o campos) MUST ser preflight de UX únicamente. Cada regla y mutación MUST ser validada y decidida por `tpi-roadmap`; el preflight puede advertir temprano pero MUST NOT sustituir la validación backend ni presentarse como decisión final.
- R11.2 El editor MUST considerar guardado únicamente una respuesta 2xx del back. Mientras espera, mantiene `saving` activo y bloquea el doble envío equivalente; no presenta estado optimista de negocio.
- R11.3 Ante rechazo HTTP, timeout o error de red, MUST restaurar la última lectura confirmada, traducir código/status a un mensaje claro y accionable con opción de reintentar. MUST NOT mostrar `detail` técnico crudo.
- R11.4 Si una operación de varios pasos confirma la creación del nodo y falla después la regla, MUST conservar el nodo confirmado, no mostrar la regla y explicar el fallo parcial.
- R11.5 Tras un guardado exitoso, al recuperar foco y al detectar conflicto, MUST releer el estado backend para reflejar cambios concurrentes.

#### Escenario R11.1: el backend detecta un ciclo que el preflight no vio
- GIVEN otro editor agregó una regla después de la última lectura local y el preflight no detecta que la flecha nueva forma un ciclo
- WHEN se envía la regla y el backend responde `409 node.prerequisite-cycle` (o `section.prerequisite-cycle`)
- THEN la UI no anuncia éxito, restaura el grafo confirmado, muestra el motivo de ciclo y permite reintentar tras releer.

#### Escenario R11.2: curso archivado
- GIVEN el profesor tenía abierto un roadmap que luego se archivó
- WHEN intenta guardar cualquier cambio y el back responde `409 course.archived`
- THEN no se muestra el cambio como guardado, se vuelve a la lectura confirmada y se explica que el curso está archivado.

#### Escenario R11.3: error 5xx
- GIVEN el request de guardado llega al servidor pero el servicio responde `5xx`
- WHEN llega la respuesta de error
- THEN el saving termina, no se muestra éxito, la interfaz restaura el último estado confirmado y ofrece reintentar con un mensaje claro de indisponibilidad.

#### Escenario R11.4: se pierde la red entre crear un nodo y guardar su regla
- GIVEN el request de creación del nodo recibió 2xx y se perdió la red antes de confirmar la regla posterior
- WHEN el flujo parcial termina con error de red
- THEN el nodo queda porque el back confirmó su creación, la regla no aparece como guardada, y la UI dice explícitamente que el nodo se creó pero su requisito no; tras recuperar conexión relee antes de ofrecer reintento.


## R12. Ruteo de flechas legible

- R12.1 El router del motor real MUST enrutar cada flecha con segmentos ortogonales y esquinas redondeadas, con un tramo recto visible desde el puerto de origen y otro hasta el puerto de destino, más una punta de flecha visible en el destino.
- R12.2 Ningún segmento MUST atravesar un nodo no extremo ni su etiqueta, ni salir del marco que contiene la ruta. Las rutas paralelas MUST quedar separadas y el cálculo MUST penalizar los giros.
- R12.3 Hover o selección de una flecha MUST resaltar sus dos extremos sin depender solo del color.
- R12.4 Estas garantías MUST mantenerse tras reordenar, alternar visibilidad o forma, y colapsar o expandir marcos anidados.

#### Escenario: obstáculos y marcos anidados
- GIVEN una flecha entre dos puertos y nodos intermedios con etiquetas dentro de marcos anidados
- WHEN el motor calcula o recalcula la ruta por un cambio de orden, visibilidad, forma o colapso
- THEN la ruta evita todo obstáculo que no sea extremo, conserva los stubs y la punta, y no se extiende fuera de su marco.

#### Escenario: aristas paralelas y selección
- GIVEN dos flechas paralelas entre los mismos extremos
- WHEN se muestran, se hoverean o se selecciona una
- THEN sus rutas quedan separadas, los giros evitan zigzags innecesarios y ambos extremos de la flecha activa se resaltan.

#### Escenario: prueba de intersección
- GIVEN el conjunto de obstáculos no extremos del layout
- WHEN se ejecuta la prueba de dominio del router
- THEN ningún segmento de la ruta intersecta el rectángulo de un obstáculo ni la caja de su etiqueta.

## R13. Paneles laterales plegables

- R13.1 El árbol de estructura izquierdo y el panel derecho (overview/inspector/asistente) MUST poder plegarse por separado mediante un botón visible en su borde y atajos `[` (árbol) y `]` (panel derecho). El lienzo MUST ocupar el espacio liberado y conservar el centro de cámara al cambiar el ancho.
- R13.2 Cada preferencia de plegado MUST persistirse por profesor en `localStorage`, dentro de `try/catch`; un error de almacenamiento usa el valor por defecto sin romper el editor.
- R13.3 Si el panel derecho estaba plegado y se selecciona un nodo, sección o flecha, o se abre el asistente, MUST abrirse temporalmente el panel contextual. Al cerrar/limpiar esa selección o cerrar el asistente, MUST volver al estado plegado preferido. El overview nunca MUST abrirse automáticamente.
- R13.4 Los toggles MUST exponer `aria-expanded` y `aria-controls`; al plegar/expandir, el foco permanece en el botón que permite reabrir y se anuncia el nuevo estado en `aria-live`.

#### Escenario: plegar los dos paneles
- GIVEN ambos paneles están abiertos
- WHEN el profesor activa el botón de cada borde o los atajos `[` y `]`
- THEN cada panel se pliega independientemente, el lienzo usa el ancho liberado y la cámara conserva su centro; los botones anuncian y reflejan su estado accesible.

#### Escenario: panel temporal del inspector
- GIVEN la preferencia guardada deja plegado el panel derecho
- WHEN el profesor selecciona nodo, sección o flecha en el mapa
- THEN se abre el inspector contextual temporalmente; al limpiar la selección vuelve a plegarse, y el overview no se abre solo.

#### Escenario: asistente temporal
- GIVEN el panel derecho está plegado
- WHEN el profesor abre el asistente desde un `+` o un drop
- THEN el panel abre el asistente; al cerrar o cancelar recupera la preferencia plegada y el foco vuelve al disparador.

#### Escenario: preferencia por profesor y almacenamiento no disponible
- GIVEN dos profesores o `localStorage` no disponible
- WHEN cada uno alterna paneles, o la lectura/escritura lanza una excepción
- THEN las preferencias disponibles no se mezclan entre profesores y el editor continúa con el default seguro sin excepción visible.

## R14. Uso desde dispositivos móviles (táctil y pantalla angosta)

Agregado 2026-10-29 a pedido del usuario. Aplica al editor (`/map`) y a sus paneles; mismo comportamiento y mismas reglas que en escritorio (el back sigue siendo la autoridad).

- R14.1 **Táctil en el lienzo:** arrastrar con un dedo mueve la cámara; pellizcar hace zoom; tocar selecciona. Implementado con Pointer Events (no eventos de mouse), con `touch-action` acorde para que el navegador no robe el gesto.
- R14.2 **Conectar sin precisión de mouse:** los puertos MUST tener área táctil ≥ 44×44 px (WCAG 2.5.8 / 2.5.5). Además, una alternativa sin arrastre: con un nodo/sección seleccionado, la acción «Conectar» del inspector o del menú contextual activa el modo «elegir destino» (tocar destino → confirmar), equivalente a `C`/`Enter`.
- R14.3 **Mover y reordenar sin arrastre largo:** «Mover a sección» (selector) y acciones «Subir/Bajar» en el inspector cubren el arrastre; un long-press (≈500 ms) inicia el arrastre del cuerpo del nodo, para no confundirlo con desplazar el lienzo.
- R14.4 **Acciones que hoy aparecen al hover** («+», puertos, quitar flecha) MUST ser alcanzables al tocar/seleccionar el elemento (sin hover).
- R14.5 **Pantalla angosta (< 768 px):** árbol y panel derecho pasan a hojas/drawers superpuestos (no columnas fijas), uno a la vez, con cierre accesible y foco gestionado; el lienzo ocupa el ancho completo. La barra superior (búsqueda, roadmap, comisión, forma, zoom) se compacta en un menú sin perder ninguna opción.
- R14.6 **Asistente y confirmaciones** se ven completos en 360 px de ancho, sin scroll horizontal; los campos usan tipos de input móviles adecuados.
- R14.7 **Sin teclado físico:** ningún flujo depende solo de atajos (`C`, `N`, `[`, `]`, Supr); cada uno tiene un control visible equivalente.
- R14.8 Preferencias (forma, paneles) MAY guardarse por separado para móvil y escritorio.

#### Escenario: conectar en el celular
- GIVEN un profesor en un celular con el mapa abierto
- WHEN toca un nodo A, elige «Conectar», toca el nodo B y confirma
- THEN se guarda «B requiere A» con el mismo flujo pesimista que en escritorio y se anuncia el resultado.

#### Escenario: paneles en pantalla angosta
- GIVEN un ancho de 375 px
- WHEN el profesor abre el árbol
- THEN aparece como hoja superpuesta, el foco entra en ella, y al cerrarla vuelve al botón que la abrió; el panel derecho no queda abierto al mismo tiempo.

#### Escenario: zoom y paneo táctil
- GIVEN el mapa en una tablet
- WHEN el profesor pellizca y arrastra con un dedo sobre el fondo
- THEN cambia el zoom y se mueve la cámara, sin mover nodos ni crear flechas.

## Iteración 2 — creación integrada y paridad con General

Esta adenda agrega R15–R18 sin alterar los requisitos ni las tareas anteriores. «General» refiere a `/o/:org/courses/:courseId/general` (actualmente `CohortGeneralPageComponent`). La fuente observada para editar nodos es `RoadmapSectionNodesComponent` dentro de `SectionResourcesContainerComponent`, que abre `EntityEditorDialogComponent`; `NodeCreationWizardComponent` es el asistente separado, no el editor por pestañas que usa la edición inline de General.

### Inventario de paridad: acciones de General y superficie del grafo

| Acción disponible en General | Fuente actual | Cómo queda disponible en el grafo |
|---|---|---|
| Crear sección/unidad | Toolbar de `CohortGeneralPageComponent`; `SectionFormModalComponent` / `RoadmapStore.addSection` | «+» de barra/lienzo; picker «Sección» y formulario. Unidad Courses-managed del roadmap principal sigue perteneciendo a General/sync; OWN permite crear desde el grafo. |
| Crear subsección (hasta nivel 5) | `contentActionItems`; tarjetas `GeneralSectionCardComponent` y `GeneralSubsectionCardComponent`; `RoadmapStore.addZone` | «+» de marco/árbol precarga padre; misma regla de profundidad, ownership y endpoint. |
| Editar nombre/descripción | Menú ⋮ de las tarjetas; `SectionFormModalComponent` o `SectionEditorDrawerComponent`; `RoadmapStore.editSection` | Kebab de marco e inspector/árbol. Preservar XP/bioma y demás campos; no ofrecer edición de entidades `managedInCourses` cuyo sync impone General. |
| Eliminar sección/subsección | Menú ⋮ + `SectionDeleteConfirmModalComponent`; `SectionsService.deleteSection` o `RoadmapStore.removeSection` | Kebab/árbol con confirmación, estado ocupado, anuncio y rechazo backend visible. |
| Ordenar secciones | Drag CDK y Alt+↑/↓ en `CohortGeneralPageComponent`; `SectionsService.reorderSections` o `RoadmapStore.reorderSections` | Drag de marco y «Subir/Bajar» accesible en inspector/árbol; solo entre hermanos. |
| Expandir/colapsar todo | Toolbar de `CohortGeneralPageComponent`; disclosure de tarjeta | Acciones de árbol «Expandir todo / Plegar todo», más colapso individual del marco (R7). |
| Visibilidad | Menú de tarjeta + `CohortGeneralPageComponent.toggleSectionVisibility`; Courses `SectionsService.updateSection`, OWN `RoadmapStore.updateSectionVisibility` | Kebab de marco/inspector; chip actualizado tras respuesta y lectura, ownership gobierna disponibilidad. |
| Tema/bioma | `RoadmapUnitSettingsComponent` en `GeneralSectionCardComponent`; `RoadmapStore` | Selector en header del marco/inspector, reutilizando widget o extrayéndolo, sin duplicar opciones/persistencia. |
| Añadir contenido/material teórico | Menú `section-content-actions.ts`; `SectionResourcesContainerComponent.addContent`; `RoadmapSectionNodesComponent.addContent`; `EntityEditorDialogComponent` y servicios Courses | Picker único → contenido teórico → mismo drawer/tabs; conservar material existente, carga/publicación/vínculo y tipos archivo/enlace/video/texto-Markdown. |
| Añadir desafío práctico/teórico; «Lista completa» o «Crear desafío nuevo» | Menú de contenido, `RoadmapSectionNodesComponent.addChallenge`, `EntityEditorDialogComponent`, `ChallengePoolStore`/`ChallengesService` | Picker de tipo único y editor compartido; mantener catálogo, permisos/authoring, retorno y borrador. Nombre de nodo separado del título del desafío. |
| Editar datos/configuración/reglas | Menú ⋮ de fila; `EntityEditorDialogComponent` y `RoadmapStore.editActivity` + `saveRules` | Kebab del nodo, inspector y árbol; pestañas Información/Configuración/Reglas con validación y campos completos de General. |
| Borrar nodo o material no vinculado | Menú ⋮ y confirmación de `RoadmapSectionNodesComponent`; `RoadmapStore.removeActivity` o `CourseContentService.deleteContent` | Menú/inspector/árbol con confirmación y diferenciación «quitar nodo» vs borrar material; rollback/relectura. |
| Reordenar nodos dentro de sección | Drag, flechas/atajos de `RoadmapSectionNodesComponent`; `RoadmapStore.moveActivityTo` / reorder | Drag dentro del marco + acciones «Subir/Bajar» del inspector/árbol; conservar reglas. |
| Mover nodo entre secciones | Acción propia del grafo: `moveActivityToSection` (no es acción equivalente en General) | Mantener selector y drop actuales con R6/R11; presentarlo también en inspector/árbol. |
| Reglas de sección/subsección | `SectionEditorDrawerComponent` o `RoadmapSectionNodesComponent.openUnitRules` → `RulesWizardComponent`; `saveUnitRules` | Reglas del marco/inspector y puertos; fuentes SECTION/NODE elegibles y AND/OR. |
| Reglas de nodo / conexiones | `EntityEditorDialogComponent`, `RulesWizardComponent`, `PrerequisitePickerComponent`; `RoadmapStore.saveRules` | Inspector, árbol, puertos/canvas, lista accesible «Conexiones» y quitar requisito. |
| Abrir/leer recursos y desafíos | `SectionResourcesContainerComponent` + `RoadmapSectionNodesComponent` | Mantener enlaces y vista de lectura en el inspector/árbol; estudiante nunca recibe acciones de edición. |

El grafo ofrece capacidades editables de General donde son propias del roadmap. Publicación o borrado de material, authoring externo de desafíos, navegación y lectura siguen usando servicios/rutas existentes, no copias de negocio.

## R15. Entrada única y editor de entidad compartido

- R15.1 «Crear nodo» MUST abrir primero «¿Qué nodo querés crear?» con contenido teórico, desafío práctico, desafío teórico, subsección y sección, filtrado por propiedad/permisos/contexto.
- R15.2 Luego, contenido/desafío MUST abrir el mismo editor de General (`EntityEditorDialogComponent` o extracción compatible), con tabs Información, Configuración y Reglas y todos sus campos/validaciones. Sección/subsección usa el formulario de sección y reglas que correspondan.
- R15.3 Debe haber un solo flujo visual de alta; barra, `+` contextual y creación desde vacío llaman al mismo flujo. Un contexto solo precarga sección, requisito, posición y tipo si ya fue elegido. Cancelar no escribe.
- R15.4 Se prefiere reutilizar `EntityEditorDialogComponent` antes que duplicar configuración en el `NodeCreationWizardComponent`; este puede actuar de wrapper/picker o migrar callers gradualmente. Si su contrato actual no sirve en el panel, extraer formulario presentacional compartido sin crear un segundo editor.
- R15.5 Conservar «Lista completa» / «Crear desafío nuevo», selección práctico/teórico, authoring y retorno del borrador; contenido conserva elección, publicación y vínculo de material.

#### Escenario: crear contenido desde un marco
- GIVEN el profesor está en un marco elegible
- WHEN elige «Crear nodo» → «Contenido teórico»
- THEN se abre el drawer de General con Información/Configuración/Reglas y sección precargada; cancelar no llama al backend.

#### Escenario: crear desafío y volver del authoring
- GIVEN se eligió «Desafío práctico» desde un nodo o marco
- WHEN se elige «Crear desafío nuevo» y vuelve del authoring
- THEN se conservan borrador, nombre, configuración y sección, y una sola confirmación crea el nodo.

## R16. Paridad funcional contextual con General

- R16.1 El grafo MUST exponer todas las acciones editables de la tabla anterior mediante `+`/kebab del marco, menú contextual de nodo, inspector o árbol. Ninguna acción depende solo de hover/drag; incluye controles táctiles de R14.
- R16.2 Paridad estructural: alta/edición/borrado confirmado/orden/visibilidad/tema/reglas de secciones y subsecciones. Paridad de nodos: alta de contenido/desafío, edición completa, borrado confirmado, orden interno, movimiento y reglas/conexiones.
- R16.3 Ambos lugares usan store/adapters/servicios compartidos y respetan ownership Courses vs OWN; el front puede orientar, el back decide.
- R16.4 Operaciones no propias del grafo (publicar material, abrir recursos, authoring de desafíos) mantienen sus componentes/rutas actuales.
- R16.5 Mutaciones se reflejan tras relectura; errores, confirmaciones, foco y anuncios cumplen R11/WCAG.

#### Escenario: entidad Courses-managed
- GIVEN una sección tiene `courseSectionId` y es `managedInCourses`
- WHEN se abre el menú de marco del roadmap principal
- THEN no ofrece renombrar/borrar lo que gobierna General/sync; indica la vista propietaria y sí permite reglas/conexiones compatibles.

#### Escenario: tema y edición conservan configuración
- GIVEN una unidad OWN tiene nombre, XP y tema
- WHEN se cambia el tema y luego el nombre
- THEN cada cambio se guarda sin restablecer XP/tema, y el canvas coincide con la lectura del back.

#### Escenario: edición completa de desafío
- GIVEN General permite editar datos/configuración/reglas de un desafío
- WHEN se edita ese nodo desde menú o inspector del grafo
- THEN aparecen los mismos campos y validaciones; cancelar no cambia el grafo y guardar actualiza lista, inspector y canvas.

## R17. Respuesta, layout y foco tras guardar

- R17.1 Capturar la respuesta de creación/edición (id, `sortOrder`, owner y campos normalizados disponibles); la lectura fresca del roadmap sigue siendo la proyección confirmada del canvas.
- R17.2 Tras 2xx, releer owner/roadmap, actualizar nodos, relaciones y reglas; ubicar el nuevo elemento dentro del marco destino usando su orden confirmado y seleccionar/centrar/enfocar. No insertar entidad ni regla de modo optimista.
- R17.3 Edición conserva selección/layout; movimiento usa owner confirmado. Ante fallo se conserva estado confirmado y no se enfoca una entidad inexistente.
- R17.4 Crear nodo + guardar requisito sigue siendo no transaccional: ante fallo del segundo paso se conserva el nodo, se informa error parcial y se reintenta solo regla, sin duplicar alta (R11.4).
- R17.5 El anuncio «Guardado» espera el fin de relectura; anunciar nombre, sección y resultado. Si la persona inició otra acción durante el request, no robarle foco.

#### Escenario: alta con id y orden normalizado
- GIVEN el backend acepta alta y responde con id/`sortOrder`
- WHEN finaliza la recarga
- THEN el nodo aparece en la sección y posición confirmadas con relaciones/reglas leídas, queda seleccionado/centrado y solo entonces se anuncia éxito.

#### Escenario: alta confirmada con regla rechazada
- GIVEN alta 2xx y PATCH posterior de regla rechazado
- WHEN termina la secuencia
- THEN queda el nodo confirmado sin flecha, con mensaje parcial y acción de reintento que no repite alta.

## R18. Requisitos de varias fuentes, también entre secciones

- R18.1 Permitir conectar varias fuentes al mismo destino (nodo o sección), de unidades/subsecciones distintas, además de reglas sección→sección; ofrecer multiselección + «Conectar a…» y selector de fuentes en el owner como alternativa al drag.
- R18.2 AND significa «todos»; OR «cualquiera». El usuario ve/elige operador de grupo antes de guardar. Guardar un owner reemplaza su regla completa y una lectura confirma cada conexión.
- R18.3 Un gesto multifuente se serializa como un único árbol/regla completo por owner; no hacer PATCH por fuente en paralelo. Quitar/editar una fuente preserva otros grupos, operadores y XP mínimo.
- R18.4 Ciclos, duplicados, elegibilidad fuera de roadmap, referencias ocultas/eliminadas, contención (nodo dentro de sección destino o sus descendientes) y profundidad son preflight UX y validación final backend. Marco colapsado es destino sección, nunca se redirige a hijo.
- R18.5 Multiselección, destino y operador se operan con teclado/táctil, foco y `aria-live`; no confirmar antes del 2xx y relectura.

#### Escenario: varios nodos de diferentes unidades, AND
- GIVEN A está en Unidad 1, B en una subsección y C en Unidad 2
- WHEN se selecciona A y B y se conectan a C con «Todos (AND)»
- THEN se envía una regla de C con ambos leaves; tras aceptación y lectura aparecen ambas flechas.

#### Escenario: regla alternativa OR
- GIVEN un owner puede desbloquearse al completar A o B
- WHEN el profesor elige «Cualquiera (OR)» y guarda
- THEN se persiste el grupo OR y General/alumno recibe la misma semántica.

#### Escenario: sección con nodo y otra sección como requisito
- GIVEN S no contiene A ni Unidad 1
- WHEN se agrega A (NODE) y Unidad 1 (SECTION) como AND en S
- THEN la llamada usa `PATCH /roadmap/sections/{S}/rules` con árbol `{rule}` y leaves tipadas; la UI solo confirma tras 2xx y lectura.

#### Escenario: rechazo backend por ciclo o contención
- GIVEN una fuente elegida causa ciclo o está dentro del owner sección
- WHEN el backend rechaza después del preflight
- THEN se restaura el árbol confirmado, se anuncia motivo, y se permite releer/reintentar.

**Contrato observado:** `RuleGroup` ya expresa múltiples leaves y AND/OR; `RoadmapStore.saveRules` / `saveUnitRules` reemplazan la regla de un owner, y `HttpRoadmapAdapter` envía PATCH a `/nodes/{id}/rules` o `/sections/{id}/rules`, usando `{rule}` para árboles y leaves tipadas. El backend inspeccionado acepta NODE externo elegible en reglas de sección y valida subsecciones, ciclos y contención. Verificar la versión desplegada; no usar `/roadmaps/{id}/relations` para reglas de desbloqueo: DEC-018 y ese endpoint corresponden a relaciones tipadas, no al árbol AND/OR.
