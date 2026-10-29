# Propuesta: editor de grafo unificado del roadmap

Fuente: [[Front - editor de grafo unificado del roadmap]] (plan aprobado el 2026-10-28).

## Intención

El profesor hoy reparte el trabajo entre tres vistas: la de círculos, que no muestra nodos; el grafo, que no crea nada; y General, que no es un grafo. La idea es dejar una sola vista de grafo, sin modos y al estilo n8n, que cree y relacione todo contra el back y se vea igual en General y en el roadmap del alumno.

## Alcance

### Entra
- F1: `/map` monta `GraphEditorPageComponent` y se borra `pages/course-map-page/**` (`map-layout.ts`, `map-drag.ts` y `map-view-mode.ts`).
- F2: lienzo sin modos, con puertos, flecha fantasma con su motivo, selector de los 5 tipos al soltar y asistente al soltar en el vacío.
- F3: subsecciones como marcos anidados y colapsables, con las flechas plegadas al marco.
- F4: `NodeCreationWizardComponent` en el panel derecho, con la sección y el requisito precargados, y «+ Subsección» con `addZone`.
- F5: persistencia según el mapeo del plan (§3), con estado de guardado y reversión ante un error.
- F6: árbol plegable, panel de resumen y barra superior limpia.
- F7: forma del nodo (tarjeta o círculo) como preferencia en `localStorage`.
- F8: chip de requisitos y «Conexiones» en `embeds/section-nodes`.

### No entra
- Tipos de relación creados por el profesor (F9): van en una historia aparte que empieza por el back. Solo se usan los 5 tipos de DEC-018.
- Guardar la posición manual de los marcos (punto 11 del backlog).
- Un endpoint transaccional para cambiar entre Requiere y un tipo informativo.

## Enfoque

Antes de F2 se parte `graph-editor-page.component.ts` (2.267 líneas). El orden es F1 → F2 → (F3, F4, F5, F7 en paralelo) → F6 → F8. El grafo no guarda estado propio: cada mutación pasa por `RoadmapStore`, que llama al back y vuelve a leer. `requires` va por `saveRules`/`saveUnitRules` y los otros 4 tipos por `/roadmaps/{id}/relations`. Ciclos, nodo↔sección contenedora y nodo↔sección informativa se validan en el front antes de llamar al back.

## Áreas afectadas

| Área | Impacto |
|------|---------|
| `roadmap.routes.ts` | Modificada (`/map`, `/graph`) |
| `pages/course-map-page/**` | Eliminada |
| `pages/graph-editor-page` | Modificada y partida |
| `ui/learning-map-canvas` | Modificada (puertos, marcos, formas) |
| `domain/map-layout/*` (`region-packing`, `edge-router`) | Modificadas |
| `ui/node-creation-wizard` | Modificada (precarga, uso en el panel) |
| `embeds/section-nodes` | Modificada |
| `data-access/roadmap/roadmap.store.ts` | Solo se toca si falta un método |
| i18n (`courseMap.*`, `graphEditor.*`) | Se limpian claves |

## Riesgos

| Riesgo | Prob. | Mitigación |
|--------|-------|------------|
| La página crece sin control | Alta | Partirla antes de F2 |
| El cambio Requiere↔informativo no es atómico | Media | Revertir en el front y avisar |
| Arrastrar no está probado en un navegador real | Media | Probarlo a mano al cerrar F2 |
| Mover un nodo borra reglas | Baja | Validar la contención (REPO-04/05) |
| Dependencias de WCAG en el arrastre | Media | Atajos `C` y `N`, selector de sección y lista de conexiones |

## Rollback

Es un cambio solo de front, en una rama y sin migraciones. Se revierte el merge, o cada commit de fase. F1 es el único que borra código: si hay que volver atrás, alcanza con restaurar `course-map-page` y la entrada `map` de las rutas. El back no cambia.

## Preguntas abiertas
1. `/graph` y su `unsavedChangesGuard`: ¿`/graph` redirige a `/map` y el guard pasa a `/map`?
2. ¿Se borran las claves `courseMap.*` o alguna se usa fuera de la página?
3. ¿El roadmap del alumno ya filtra las relaciones ocultas, o F8 tiene que cubrirlo?
4. ¿Se necesita la confirmación del back para un endpoint transaccional, o la reversión del front alcanza para el sprint?

## Criterios de éxito
- [ ] Ninguna ruta ni pestaña lleva a la vista de círculos.
- [ ] Desde el grafo se crean una unidad, una subsección, los dos tipos de desafío y un contenido, con las mismas validaciones que en General.
- [ ] Una flecha Requiere sigue ahí al recargar y se ve en General y en la vista del alumno.
- [ ] Las flechas inválidas se rechazan antes de llamar al back y muestran el motivo.
- [ ] Mover una tarjeta nunca borra reglas.
- [ ] Todo se puede hacer con el teclado, con anuncios `aria-live`.
- [ ] La tarjeta y el círculo muestran la misma información.

## Enmiendas 2026-10-28

Decisiones del usuario posteriores a la propuesta. MANDAN sobre el texto de arriba.

1. **Toda flecha es una regla de desbloqueo.** El editor no crea, no edita y no muestra relaciones informativas (recommends, belongs_to, part_of, related_to); las existentes en la base no se tocan. Arrastrar de A a B crea «B requiere A», sin selector de tipo. Desaparecen el cambio de tipo y el problema de las dos llamadas al back (el riesgo «Requiere↔informativo no es atómico» y la pregunta 4 dejan de aplicar). Los tipos informativos y los creados por el profesor quedan para una historia aparte. Cambia F2 (sin selector de los 5 tipos) y F5 (solo `saveRules`/`saveUnitRules`, sin `/roadmaps/{id}/relations`).
2. **Rutas.** `/roadmap/teacher/course/:id/map` es la única ruta del editor y monta `GraphEditorPageComponent` con `unsavedChangesGuard`. `/graph` redirige a `/map` (responde la pregunta 1) y queda una sola pestaña. Se borra `course-map-page`.

3. **Reglas de sección con nodos.** Una unidad o subsección puede requerir un nodo externo elegible; se guarda como hoja `NODE` vía `PATCH /sections/{id}/rules` y solo se confirma tras 2xx. Se mantiene el rechazo backend por contención; un drop sobre marco colapsado nunca se redirige a un nodo interno.
4. **Control desde un dispositivo móvil (2026-10-29).** El editor del grafo (`/map`), el árbol, el inspector, el asistente y la barra de contexto (roadmap/comisión) MUST poder usarse desde un celular o tablet: táctil y pantallas angostas. Ver R14 en [[spec]] y T-20/T-21 en [[tasks]].

## Iteración 2 — creación integrada y paridad con General (2026-10-29)

Esta iteración amplía el alcance ya implementado; **no reemplaza ni reescribe T-01a–T-21**. El punto de entrada para crear es único: «Crear nodo» abre primero «¿Qué nodo querés crear?» y después usa el editor de entidad/drawer de General (`EntityEditorDialogComponent`) con las pestañas Información, Configuración y Reglas, en vez de reproducir todos sus campos en los pasos propios de `NodeCreationWizardComponent`. El wizard actual puede quedar como picker/contexto y puente de compatibilidad mientras se extrae el formulario compartido; no debe mantenerse como una segunda implementación de configuración.

La paridad cubre también el ciclo de vida estructural y de actividades que hoy se ofrece en General: crear/editar/eliminar y ordenar secciones/subsecciones; visibilidad y bioma/tema; crear/editar/eliminar, mover y reordenar nodos; materiales, desafíos, conexiones y reglas. La superficie será contextual: `+` y menú en el encabezado del marco para secciones; menú contextual del nodo y el inspector para actividades; árbol para seleccionar y abrir acciones; canvas para conexión y reordenamiento espacial. La especificación enumera las diferencias entre una sección administrada por Courses y una unidad OWN, que siguen limitando qué acciones pueden ofrecerse.

Al guardar una entidad, se toma el id y los datos de la respuesta confirmada del back, se relee el roadmap afectado, se calcula su posición de layout dentro del marco destino y se selecciona/enfoca el resultado. No se inserta de forma optimista una entidad ni se inventa una regla; la lectura confirmada alimenta el canvas. Para conexiones a varios requisitos se recoge el conjunto de fuentes y se guarda una sola regla del owner: AND significa «todos» y OR «cualquiera». La iteración registra como coordinación de back cualquier insuficiencia transaccional o de respuesta, sin asumir que la API de relaciones DEC-018 es el mismo contrato que las reglas.

Se incorporan asimismo los ajustes visuales que ya estaban en curso (legibilidad del título de sección en el encabezado del marco y alineación de la lista de unidades del wizard) como verificación explícita: si ya están en el checkout se marcan hechos al validarlos; si no, quedan como tareas de cierre, no como cambios asumidos.

Ver [[spec#r15.-creación-integrada-y-paridad-con-general|R15–R18]], [[design#iteración-2--creación-integrada-y-paridad-con-general|diseño de la iteración]] y [[tasks#iteración-2--creación-integrada-y-paridad-con-general|T-22–T-28]].
