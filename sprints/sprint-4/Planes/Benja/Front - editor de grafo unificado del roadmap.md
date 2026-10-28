---
tags: [tpi, g10, sprint-4, plan, front, roadmap, graph-editor]
fecha: 2026-10-28
autor: Benjamin Polzoni
estado: propuesta - mockup aprobado
actualizado: 2026-10-28
repo: 2026-P4-FE/2026-PIV-TPI-FE
rama: BenjaminPolzoni/fix-vista-y-uso-del-roadmap-en-el-mapa-de-nodos
---

# Plan — Editor de grafo unificado del roadmap

> **Autor / responsable del plan:** Benjamin Polzoni (`412056-1w3-Polzoni-Benjamin`)
> **Fecha:** 2026-10-28
> **Estado:** mockup aprobado por Benjamin el 2026-10-28; **nada implementado todavía**.
> **Rama / worktree (frontend):** `BenjaminPolzoni/fix-vista-y-uso-del-roadmap-en-el-mapa-de-nodos` en `~/orca/workspaces/2026-PIV-TPI-FE/fix-vista-y-uso-del-roadmap-en-el-mapa-de-nodos`.
> **Mockup interactivo:** https://claude.ai/artifact/JmibnuzGacvRCWzzTZnVxa
> **Objetivo:** una sola vista de grafo para el profesor donde pueda hacer todo lo que hace la vista simple (General): crear secciones, subsecciones, desafíos y contenido con el mismo paso a paso, y armar las restricciones arrastrando flechas entre nodos y secciones, al estilo n8n. Todo lo que se haga se guarda en el back y se ve igual en la vista simple y en el roadmap del alumno.

## 1. Situación actual

Hoy hay tres pantallas que hacen partes del mismo trabajo:

| Vista | Código | Problema |
| --- | --- | --- |
| «Mapa» (círculos) | `pages/course-map-page` (~4.000 líneas) + `map-layout.ts`, `map-drag.ts` | No muestra nodos ni relaciones; los círculos no dicen nada; la leyenda ocupa tres filas; el panel repite «Sin nodos todavía» |
| «Mapa de aprendizaje» | `pages/graph-editor-page` + `ui/learning-map-canvas` | Tiene regiones, tarjetas, flechas con tipo, modo Relacionar e inspector, pero **no crea nada**: «+ Agregar primer nodo» navega a la vista de círculos (`graph-editor-page.component.ts:613`). Las zonas no se ven anidadas. Para relacionar hay que cambiar de modo. No guarda reglas de unidad (no llama a `saveUnitRules`) |
| Vista simple (General) | `embeds/section-nodes` | Tiene el asistente completo (`NodeCreationWizardComponent`: tipo → sección → detalle → prerrequisitos → revisión), pero no se ve como grafo |

El `RoadmapStore` ya tiene todas las operaciones que hacen falta: `addSection`, `addZone`, `addActivity`, `moveActivityToSection`, `saveRules`, `saveUnitRules`, `addRelation`, `updateRelation`, `removeRelation`. La ruta del roadmap y el embed de Cursos usan **instancias separadas del store** (`roadmap.providers.ts` y `embeds/roadmap-editor.providers.ts`), y cada una lee del back al entrar. Por eso, que «se vea reflejado» depende de que todo pase por el back y no por estado local.

## 2. Decisiones tomadas (2026-10-28)

1. **La vista de círculos se borra.** La ruta `/roadmap/teacher/course/:id/map` pasa a mostrar el editor de grafo. Se van `course-map-page`, `map-layout.ts`, `map-drag.ts` y `map-view-mode.ts`, y se revisa que nada más los use.
2. **Sin modos, al estilo n8n.** Desaparece el toggle Seleccionar/Relacionar:
   - arrastrar desde el punto de conexión crea una relación;
   - arrastrar el cuerpo mueve la tarjeta;
   - soltar la flecha en un espacio vacío abre el asistente con un nodo nuevo ya conectado.
3. **Las subsecciones son marcos anidados** dentro de su unidad, colapsables. Al colapsar un marco, sus flechas pasan a apuntar al marco.
4. **La creación usa el mismo asistente de la vista simple**, abierto en el panel derecho (no en un modal) y con la sección y el requisito ya cargados.
5. **La forma del nodo se puede elegir:** tarjeta o círculo (grafo clásico), con la misma estética. Es una preferencia del profesor guardada en `localStorage`, porque no es dato del curso.
6. **El árbol de estructura del panel izquierdo se pliega y despliega** por sección, y tiene «Desplegar todo / Plegar todo». Al seleccionar algo en el lienzo se despliega su camino.

## 3. Mapeo al back (lo que se guarda y dónde)

| Acción en el grafo | Llamada | Notas |
| --- | --- | --- |
| Flecha **Requiere** a un nodo | `saveRules` (regla del nodo destino) | `requires` no es una relación: es una hoja de la regla. El back responde 400 `relation.requires-uses-rules` si se manda como relación |
| Flecha **Requiere** a una unidad o subsección | `saveUnitRules` | La regla de una sección solo admite otras secciones. La flecha de un nodo a una sección se rechaza en la UI con el motivo |
| Flecha **Recomienda / Pertenece a / Parte de / Relacionado** | `addRelation` → `POST /roadmaps/{id}/relations` | Une dos nodos o dos secciones, nunca un nodo con una sección. Tiene visibilidad para el alumno |
| Cambiar el tipo de una flecha | `updateRelation` entre tipos informativos; si pasa de Requiere a informativo o al revés: quitar la hoja de la regla y crear la relación (o al revés) | Son dos llamadas. Si falla la segunda, se deshace la primera y se avisa |
| Borrar una flecha | `removeRelation` o quitar la hoja de la regla con `saveRules` / `saveUnitRules` | Se confirma en línea, sin modal |
| Invertir una flecha | Borrar y volver a crear | Antes se valida que no cierre un ciclo |
| Crear desafío, contenido o subsección | `addActivity` / `addZone` + regla con los requisitos elegidos | Es el mismo camino que usa la vista simple |
| Mover una tarjeta a otra sección | `moveActivityToSection` | Antes se valida la contención: si el nodo quedaría adentro de una sección con la que tiene una regla, se rechaza el movimiento y no se borra nada (REPO-04 / REPO-05) |
| Reordenar dentro de la sección | `moveActivityTo` | Las reglas no se tocan |
| Mover un marco de unidad en el lienzo | Solo es posición visual | Persistir las posiciones manuales queda pendiente: punto 11 del backlog `learning-map-improvements.md` |

El indicador «Guardando… / Guardado» de la barra superior refleja el estado real de la llamada. Si una llamada falla, el grafo vuelve al estado anterior y se avisa con el motivo, nunca con un éxito falso (REPO-09).

## 4. Tipos de relación creados por el profesor

El catálogo es **cerrado** (DEC-018, `CREATEABLE_RELATION_TYPES`) y el back rechaza cualquier otro tipo. El mockup muestra «+ Tipo nuevo» para validar la idea, pero esa opción **necesita trabajo en tpi-roadmap**:

- Modelo nuevo: tipo de relación por roadmap, con nombre, si es visible para el alumno y si es simétrico. Siempre es informativo: no bloquea.
- Endpoints: `GET/POST/PATCH/DELETE /roadmaps/{id}/relation-types`, y que `relations` acepte el id de un tipo propio además del enum.
- Front: el catálogo pasa a ser la unión del enum y los tipos del roadmap. El estilo de línea de los tipos propios es fijo (punteado verde, con etiqueta).

**Decisión (2026-10-28):** este cambio usa solo los 5 tipos del catálogo. Los tipos propios van en una **historia aparte**, empezando por el back; F9 sale de este cambio y el botón «+ Tipo nuevo» no se implementa todavía.

## 5. Que se vea igual en la vista simple y en el roadmap

- El grafo **no tiene estado propio** fuera del store: toda mutación pasa por el back y, cuando termina, el store vuelve a leer lo que le afecta.
- **Vista simple** (`embeds/section-nodes`): ya muestra lo que se crea con `addActivity` y `addZone`, y las reglas con `saveRules`. Falta mostrar las relaciones informativas: agregar en la fila del nodo un chip con el candado y la cantidad de requisitos, y en su menú ⋮ la entrada «Conexiones» con la lista de relaciones en texto.
- **Roadmap del alumno:** lee las mismas reglas y relaciones. Hay que comprobar que una relación oculta no se le muestra y que las visibles respetan el tipo.
- **Prueba de aceptación cruzada:** crear un nodo con un requisito y una relación en el grafo, abrir General y la vista del alumno, y ver lo mismo sin recargar a mano. En General, la recarga la da la navegación.

## 6. Fases

| # | Fase | Archivos principales | Depende de |
| --- | --- | --- | --- |
| F1 | Ruta única: `/map` monta `GraphEditorPageComponent`, se borra la vista de círculos y se ajustan los redirects y los specs de rutas | `roadmap.routes.ts`, `pages/course-map-page/**`, `course-editor-page` (pestañas) | — |
| F2 | Lienzo sin modos: puertos en nodos y encabezados de marco, flecha fantasma con destinos válidos e inválidos y su motivo, selector de tipo al soltar (5 tipos), soltar en el vacío abre el asistente | `ui/learning-map-canvas`, `pages/graph-editor-page` | F1 |
| F3 | Marcos anidados para zonas y colapso con flechas plegadas | `domain/map-layout/*` (`packRegions`, `edge-router`), `learning-map-canvas` | F2 |
| F4 | Creación en el panel: `NodeCreationWizardComponent` dentro del inspector, «+» en marcos y nodos, pasos con la sección y el requisito precargados, «+ Subsección» con `addZone` | `graph-editor-page`, `ui/node-creation-wizard` | F2 |
| F5 | Persistencia completa según la tabla de la sección 3, con el estado de guardado y la reversión ante un error | `graph-editor-page`, `roadmap.store.ts` (solo si falta algún método) | F2 |
| F6 | Panel izquierdo plegable, panel de resumen («Para revisar», atajos) y barra superior limpia (fuera la fila de chips y la leyenda grande) | página + `ui/` nuevo para el árbol | F1 |
| F7 | Forma del nodo: tarjeta o círculo; el layout cambia el tamaño de celda y los puertos | `learning-map-canvas`, `map-layout` | F2 |
| F8 | Vista simple: chip de requisitos y «Conexiones» en el menú del nodo | `embeds/section-nodes` | F5 |
| F9 | Tipos de relación propios (opcional, después del back) | `generic-graph.models.ts`, adapter HTTP | Back |

## 7. Criterios de aceptación

- No queda ninguna ruta ni pestaña que lleve a la vista de círculos.
- Desde el grafo se puede crear una unidad, una subsección, un desafío práctico, un desafío teórico y un contenido, con los mismos pasos y validaciones que en General.
- Arrastrar de un nodo a otro y elegir «Requiere» guarda la regla. Al recargar la página, la flecha sigue ahí y se ve en General.
- Una flecha que cerraría un ciclo, que une un nodo con la sección que lo contiene o que mezcla un nodo con una sección en un tipo informativo, se rechaza antes de llamar al back, con el motivo en palabras.
- Mover una tarjeta nunca borra reglas: o se mueve con todo o se rechaza.
- Todo se puede hacer sin mouse: «Conectar con…» (`C`), «Nuevo» (`N`), el selector de sección en Datos como alternativa a arrastrar, y la lista de conexiones como alternativa a las flechas. Foco visible y anuncios en `aria-live`.
- Tarjetas y círculos muestran la misma información: tipo, nombre, XP, candado con la cantidad de requisitos, oculto y opcional.

## 8. Riesgos

- `graph-editor-page.component.ts` ya tiene ~2.300 líneas. Conviene partirla primero, como dice el punto 2 de `learning-map-improvements.md`, o cada fase la va a agrandar más.
- Arrastrar para relacionar todavía no se probó en un navegador real (punto 1 del backlog).
- Cambiar el tipo entre Requiere e informativo no es atómico en el back: se necesita la reversión del lado del front o un endpoint transaccional.
- La pantalla está excluida de la estandarización de UI (`ui-standardization` no aplica a `features/roadmap/**`), pero igual usa solo `@2026-p4-fe/ui` y los tokens `--tpi-*`. El lienzo de grafo no existe en el kit y queda como componente de la feature, como hoy.

## Relacionado

- `docs/roadmap/graph-editor-requirements.md` y `graph-editor-handoff.md` (repo FE)
- `docs/roadmap/learning-map-improvements.md` (backlog del editor)
- `docs/roadmap/prerequisite-gate-policy.md`
