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
- R2.6 Una regla de sección SOLO admite secciones (`saveUnitRules`); una de nodo, nodos (`saveRules`).

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

#### Escenario: nodo hacia sección
- GIVEN un nodo N y una sección S no contenedora
- WHEN se arrastra de N a S
- THEN se rechaza: las reglas de sección solo admiten secciones.

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
- THEN se trata como una regla de sección (A debe ser sección) o se rechaza con motivo si A es nodo; nunca se crea contra X de forma implícita.

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
