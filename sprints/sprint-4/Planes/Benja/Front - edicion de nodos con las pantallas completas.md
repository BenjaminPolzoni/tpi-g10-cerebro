---
tags: [tpi, g10, sprint-4, plan, front, roadmap, graph-editor, courses]
fecha: 2026-11-06
autor: Benjamin Polzoni
estado: propuesta
repo: 2026-P4-FE/2026-PIV-TPI-FE
rama: BenjaminPolzoni/unified-node-creation-pages (worktree ~/orca/workspaces/2026-PIV-TPI-FE/unified-node-creation-pages)
---

# Plan — Edición de nodos con las pantallas completas

Sigue al plan [[sprints/sprint-4/Planes/Benja/Front - pantallas de creacion unificadas en la vista de nodos|pantallas de creación unificadas]], que ya está implementado (T-01 a T-10).

## Decisión (pedido de Benja, 2026-11-06)
- Al tocar **Editar** en un nodo ya no se abre el panel lateral `app-entity-editor-dialog` en modo `drawer`.
- Se navega a la **misma pantalla completa que se usa para crear**, en modo edición:
  - contenido / actividad / recurso → `ContentNodeCreatePage`;
  - desafío práctico o teórico → `ChallengeNodeCreatePage`.
- En modo edición se ven **todos los pasos** desde el inicio, sin bloqueo lineal. Las validaciones son las mismas que al crear y se revisan todas al guardar.
- Guardar hace un **PUT** del nodo con los valores nuevos, y queda guardado.
- Al guardar o cancelar se vuelve a donde estaba el usuario (`returnUrl` con `select=<nodeId>`), igual que al crear.
- Vale en las dos vistas: la de nodos (grafo) y la simple (Courses).

## Estado actual (relevado en el código, 2026-11-06)

### Dónde se edita hoy
| Dónde | Cómo abre | Cómo guarda |
|---|---|---|
| Vista de nodos, `roadmap/pages/graph-editor-page/graph-editor-page.component.ts` | Menú del nodo, acciones `edit` y `change`, en `onNodeAction` (~1209-1216): pone `editingNodeId` y abre `<app-entity-editor-dialog kind="node">` (HTML ~722). | `saveNodeEdit` (~1238-1335). |
| Vista simple, `roadmap/embeds/section-nodes/roadmap-section-nodes.component.ts` | `editNode(sectionId, node)` (~1882) pone `editing` con `isNew:false`; el diálogo está en el HTML ~204. | `onSave` (~2188-2290): es la **misma cadena copiada** que en el grafo. |

Las dos vistas guardan con esta cadena:
1. `store.editActivity`.
2. La disponibilidad: `turnOff` (con confirmación si otros nodos lo requieren) o `updateAvailability`.
3. Las reglas: `saveRules`, salvo en un nodo de recuperación.
4. Los efectos de ítems: `updateItemEffects`.
5. La IA: `updateAiUsage`.
6. Al final, `reloadConfirmed`, que recarga y enfoca el nodo.

### El PUT ya existe
`roadmap-http/http-roadmap.adapter.ts:730` `updateActivity`:
- Con `replaceBoundaries` (ventana y límites del desafío) hace `PUT /nodes/{id}`.
- Si no, hace `PATCH` solo con lo que cambió.

En el back, `GraphController` (`PUT /nodes/{nodeId}`, línea ~277) exige `roadmap.graph.write`, valida el body con `@Valid` y exige ser dueño (`requireOwner`). **No hace falta cambiar el back.**

### Más usos del panel lateral (no son edición, pero siguen usando el drawer)
- **Vista simple, alta desde el drawer.** Todavía crea con el drawer (`isNew:true`) en tres lugares: la fila de un recurso pendiente (~1455), `newNode` (~1866) y retomar un borrador (`resumeDraft`, ~1830). Al sacar el drawer hay que mandar estos tres a las pantallas.
- **`courses/pages/cohort-general-page`** (~435): crea a mano el **nodo de recuperación** (`recoveryOnly`, `RECOVERY`) con el drawer.
- **`ContentNodeCreatePage` ya reutiliza el mismo componente** en modo `inline` (`content-node-create-page.component.html:59`, `presentation="inline"`, `[isNew]="true"`). Para contenido, editar es pasarle el nodo existente: casi no hay trabajo nuevo.

## Inventario del panel de edición (qué no se puede perder)
Entradas que el grafo le pasa al editar (`graph-editor-page.component.html` ~722-790):
- **Datos generales:** nombre, descripción, tipo, icono (`iconKey`), obligatorio.
- **Contenido:** `contentId`, URL del recurso, materiales del curso (con reintento), subida de un archivo.
- **Desafío:** `challengeId`, «Cambiar desafío» (acción `change`), pool de desafíos (con reintento), aviso si el desafío no está disponible (`challengeUnavailable`).
- **Configuración:** dificultad, política de vidas (`STANDARD` o `RECOVERY`), visible (`available`), ventana desde/hasta, reintentos (`allowedRetries`), tiempo por intento, efectos de ítems, uso de IA (`usesAi`, tres estados) y roles de IA (`aiRoles`).
- **Reglas:** candidatos, modo `AND`/`OR`, lista de ids y **regla combinada** (`RuleGroup`, árbol).
- **Comportamiento:** confirmación al apagar un nodo que otros requieren (`pendingTurnOff`) y la pestaña Historial, oculta (`showHistory = false`, PR #2058).

## Huecos
1. **Cargar un nodo existente.** Las pantallas solo crean. Tienen que aceptar un `:nodeId`, buscarlo en el store cuando el roadmap esté listo y precargar todos los campos. Si el nodo no existe, muestran un error con salida (`app-error-state`).
2. **Pasos libres al editar.** `ChallengeNodeCreatePage` bloquea cada paso hasta que el anterior es válido (`reached`, ~475; `locked` en `steps`, ~481). Al editar, todos los pasos arrancan abiertos. Al guardar se usa la misma `firstInvalidStep` (~485) y, si algo falla, se salta al paso con el error.
3. **Qué pasos tiene un desafío al editar.** Pasos actuales: `challenge`, `rules`, `course`, `content`, `review` (~179).
   - `rules` y `content` editan el **contenido del desafío** (el quiz o el práctico), que pertenece a los servicios de desafíos de otros grupos.
   - Al editar un nodo, el desafío ya existe: se edita **qué desafío está vinculado** (paso `challenge`, con «Cambiar desafío») y **la configuración del nodo** (paso `course`).
   - Propuesta: `rules` y `content` se muestran **solo para leer**, con un enlace a la pantalla de edición del desafío, que ya existe en `/challenges/...`. Ver pregunta 1.
4. **Campos que la pantalla de desafío no tiene y el panel sí:**
   - reintentos por nodo (`allowedRetries`, que no aparece en la página);
   - roles de IA (`aiRoles`);
   - **regla combinada** (`RuleGroup`): la página arma solo una lista con modo AND/OR.
   
   Hay que sumarlos al paso `course` copiando los controles del panel, para que no se pierda nada al editar un nodo que ya los tiene.
5. **Guardar con PUT.** El modo edición llama a la misma cadena que hoy usa el panel (`editActivity` → disponibilidad → reglas → efectos → IA). Esa cadena está **copiada en dos lugares** (grafo y vista simple). Se pasa a un único método del store (por ejemplo, `RoadmapStore.saveNodeEdit`) y lo usan las dos pantallas.
6. **Apagar un nodo requerido.** La confirmación `pendingTurnOff` pasa a la pantalla con `GenericConfirmModal destructive`.
7. **Rutas de edición.** Junto a las de alta en `courses/courses.routes.ts`:
   - `general[/sections/:sectionId]/content/:nodeId/edit`;
   - `general[/sections/:sectionId]/challenge/:nodeId/edit`.
   
   Llevan la misma query que el alta (`roadmapId`, `group`, `returnUrl`) y los mismos guards (`editRoadmap`, el guard de profesor que ya acepta a Gestor y Admin, y `unsavedChangesGuard`). Para editar un desafío **no** se exige `authorChallenges`, porque solo se cambia el vínculo.
8. **Volver.** Igual que al crear: `returnUrl` con `select=<nodeId>`, y el editor enfoca el nodo y lo anuncia.
9. **Sacar el drawer del todo.** Si se quiere borrar el modo `drawer` del componente, también hay que pasar a las pantallas los tres altos de la vista simple y el nodo de recuperación de `cohort-general-page`. Ver pregunta 2.

## Tareas
- [ ] **E-01 Store: un solo guardado de edición.** Pasar la cadena de `saveNodeEdit` (grafo, ~1238) y de `onSave` (vista simple, ~2188) a un método del `RoadmapStore`. Las dos vistas lo llaman y por ahora no cambia nada visible.
- [ ] **E-02 Contenido en modo edición.**
  - Ruta `content/:nodeId/edit`.
  - `ContentNodeCreatePage` lee `nodeId`, busca el nodo y le pasa al editor inline todas las entradas `initial*` que hoy le pasa el grafo, con `isNew=false`.
  - Al guardar, usa E-01.
  - Título «Editar nodo».
- [ ] **E-03 Desafío en modo edición: carga.**
  - Ruta `challenge/:nodeId/edit`.
  - `ChallengeNodeCreatePage` lee `nodeId` y precarga la fuente (`existing`) con el desafío vinculado, el tipo, el icono, el paso `course` completo y las reglas.
- [ ] **E-04 Desafío en modo edición: pasos libres.** Todos los pasos abiertos, guardado desde cualquier paso, validación completa al guardar y salto al primer paso con error. `rules` y `content` según la respuesta a la pregunta 1.
- [ ] **E-05 Campos que le faltan a la página de desafío.** Sumar reintentos por nodo, roles de IA y regla combinada (`RuleGroup`) al paso `course`, copiando los controles del panel.
- [ ] **E-06 Desafío en modo edición: guardar.** Arma el resultado de la edición y llama a E-01 (PUT). Confirmación de apagado con `GenericConfirmModal destructive`. Vuelve con `select=<nodeId>`.
- [ ] **E-07 La vista de nodos navega.** Las acciones `edit` y `change` del menú del nodo llevan a `content/:id/edit` o a `challenge/:id/edit` según el tipo; `change` abre directamente en el paso `challenge`. Se borran `editingNodeId`, `saveNodeEdit`, `pendingTurnOff` y el `<app-entity-editor-dialog>` del grafo.
- [ ] **E-08 La vista simple navega.** `editNode` lleva a las mismas rutas. Se borran `onSave` (la parte de edición) y su estado.
- [ ] **E-09 (según la pregunta 2) Altas que quedan en el drawer.** Pasar a las pantallas las altas de la vista simple (recurso pendiente, `newNode`, `resumeDraft`) y el nodo de recuperación de `cohort-general-page`. Después borrar el modo `drawer` de `entity-editor-dialog` y su CSS.
- [ ] **E-10 (opcional) Historial.** Borrar la pestaña oculta (pestaña, panel, carga de `getNodeEditLog`, claves `entityEditor.history.*`, specs). Antes hay que confirmar con backend qué pasa con `GET /nodes/{id}/edit-log`.
- [ ] **E-11 Tests y verify** solo antes de la PR: specs de las pantallas en modo edición, del método del store, de la navegación de las dos vistas y de las rutas.

## Fuera de alcance
- Editar el **contenido del desafío** (preguntas, enunciado, plantilla): es de los servicios de desafíos y ya tiene su propia pantalla.
- Editar **unidades y subsecciones** (nombre, bioma, reglas de la unidad): siguen con sus diálogos actuales.
- Cambios de back: no hacen falta, porque el PUT y el PATCH ya existen y validan.

## Preguntas abiertas
1. En un nodo de desafío, ¿los pasos «Reglas» y «Contenido» se muestran solo para leer, con un enlace para editar el desafío en su pantalla, o se ocultan al editar?
2. ¿Sacamos **todo** el drawer, incluidas las altas que todavía lo usan en la vista simple y el nodo de recuperación de la página general (E-09)? ¿O solo la edición, dejando esas altas para otra PR?
3. ¿Borramos ahora la pestaña Historial oculta (E-10), o esperamos la decisión de backend?
