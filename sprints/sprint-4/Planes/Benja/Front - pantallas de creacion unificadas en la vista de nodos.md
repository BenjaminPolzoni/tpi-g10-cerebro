---
tags: [tpi, g10, sprint-4, plan, front, roadmap, graph-editor, courses]
fecha: 2026-11-05
autor: Benjamin Polzoni
estado: propuesta
repo: 2026-P4-FE/2026-PIV-TPI-FE
rama: BenjaminPolzoni/unified-node-creation-pages (worktree ~/orca/workspaces/2026-PIV-TPI-FE/unified-node-creation-pages)
---

# Plan — Pantallas de creación unificadas en la vista de nodos

## Decisión (acordada con Benja, 2026-11-05)
- La **vista de nodos** (editor de grafo, `/roadmap/teacher/course/:id/map`) deja de crear contenido y desafíos con el panel lateral `app-node-creation-wizard` y usa **las mismas pantallas completas de la vista simple** (Courses → «Añadir a la sección»):
  - Contenido teórico / actividad / recurso → `ContentNodeCreatePageComponent`.
  - Desafío teórico o práctico (crear nuevo o asignar uno existente) → `ChallengeNodeCreatePageComponent`.
  - Subsección → `SubsectionCreatePageComponent`.
- Se navega a la pantalla y **al guardar o cancelar se vuelve siempre a donde estaba** (mismo roadmap, comisión, selección y scroll).
- **Todas las pantallas iguales**: vista de nodos y vista simple usan el mismo flujo. El panel viejo se elimina de las dos.
- **Editar** un nodo existente sigue con el panel lateral `app-entity-editor-dialog` (sin cambios de diseño). Se rediseña más adelante; ahora solo tiene que seguir funcionando igual.
- **Quién puede**: Profesor, Gestor y Admin.

## Estado actual (relevado en el código, 2026-11-05)
| Dónde | Crear | Editar |
|---|---|---|
| Vista simple, `roadmap/embeds/section-nodes/roadmap-section-nodes.component.ts` | Ya navega a las pantallas (`openCreationPage`, línea ~1595). Queda un camino viejo: `resumeDraft` reabre el wizard cuando un borrador tiene `draft.wizard` (línea ~1893), más `openWizard` (línea ~2209) y el `<app-node-creation-wizard>` del HTML (línea ~287). | `app-entity-editor-dialog` |
| Vista de nodos, `roadmap/pages/graph-editor-page/graph-editor-page.component.ts` | `openCreation` → `app-create-type-chooser` → `app-node-creation-wizard` (HTML línea ~714). Tipos: `theory`, `practical-challenge`, `theoretical-challenge`, `subsection`, `section`. Para un desafío nuevo sale a `/challenges/new` y vuelve con el borrador del wizard. | `app-entity-editor-dialog` (HTML línea ~749) |

Rutas de las pantallas: `features/courses/courses.routes.ts` líneas ~216–276:
- `courses/:cohortId/general[/sections/:sectionId]/{challenge|content}/new?nodeUnitId=&returnUrl=`
- `courses/:cohortId/general/sections/:sectionId/subsection/new`

Permisos de hoy:
- Las pantallas pasan por `cohortProfessorGuard` (`features/courses/data-access/cohort-professor.guard.ts`), que solo deja entrar a los miembros de la comisión con rol Manager, Professor o ReadOnlyProfessor.
- La de desafío pide además `permissionGuard('authorChallenges')`.
- El editor de grafo usa `permissionGuard('editRoadmap')` = `['PROFESSOR','GESTOR','ADMIN']`, o el código `roadmap.graph.write`.
- `authorChallenges` es **solo PROFESSOR**: `core/services/permissions.service.ts:31` dice que los servicios de payload teórico y práctico rechazan a GESTOR y ADMIN.

## Huecos que hay que cerrar
1. **Roadmap elegido.** Las pantallas abren el roadmap principal (`store.ensureOpen(cohortId)`, sin `roadmapId`). En cambio, la vista de nodos puede estar en un roadmap secundario o filtrada por comisión (`?roadmap=&group=`). Hay que pasar `roadmap` y `group` en la query y que la pantalla abra ese roadmap (`store.open(cohortId, roadmapId)`). Ver las memorias «multi-roadmap es central» y «mismo contenido en todos los roadmaps».
2. **Contexto del «+» del mapa.** El wizard recibe `initialPrerequisiteId`/`initialPrerequisiteKind` cuando se crea desde un nodo o una sección. Las pantallas no lo reciben: hay que sumar `prerequisiteId` y `prerequisiteKind` en la query y precargar la regla.
3. **Tipo preelegido.** El chooser ya distingue práctico y teórico. La pantalla de desafío debería recibir `type=PRACTICAL|THEORETICAL` para abrir con ese tipo marcado.
4. **Unidad sin sección de Courses.** En el grafo hay unidades que solo existen en el roadmap: usar las rutas `general/{challenge|content}/new` (sin `:sectionId`), igual que `openCreationPage` con `roadmapOnly()`.
5. **Vuelta al mapa.** El `returnUrl` sale de `router.url` del editor: conserva `roadmap`, `group` y `select`. Al volver, el editor tiene que seleccionar el nodo creado (`?select=<nodeId>`), igual que la vista simple vuelve con `#section-…`.
6. **Gestor y Admin.**
   - `cohortProfessorGuard` los manda a `/courses/:id/general` si no son miembros de la comisión. Hay que dejarlos pasar cuando tienen `editRoadmap`, y que la pantalla quede con permiso de escritura (`facade.canWrite`).
   - **Hipótesis a verificar:** que `cohortMembershipGuard` (anterior en la cadena) también los deje pasar.
7. **Desafío nuevo para Gestor y Admin.** **Riesgo:** hoy el back rechaza que GESTOR o ADMIN creen el payload de un desafío. Propuesta: la ruta `challenge/new` pasa a `editRoadmap`. Dentro de la pantalla, «Crear desafío nuevo» solo se ofrece con `authorChallenges`, y «Asignar desafío existente» del pool (`readChallengePool`) se ofrece a todos. Si se quiere que Gestor y Admin también creen desafíos, es un cambio de back (practical/theoretical payload) y va aparte.

## Tareas
- [ ] **T-01 Inventario antes de borrar** (memoria «reutilizar antes de borrar»). Listar qué hace el wizard que las pantallas no hacen: subida de contenido (`contentUploadRequested`), IA (`aiEnabled`), regla precargada, alta de sección desde el chooser, borradores de `NodeDraftStorage`. Lo que falte se porta a la pantalla, no se pierde.
- [ ] **T-02 Query nueva en las pantallas.** `roadmap`, `group`, `prerequisiteId`, `prerequisiteKind` y `type` (solo desafío) como `input()` en `ContentNodeCreatePageComponent` y `ChallengeNodeCreatePageComponent`. Abrir el roadmap pedido y precargar regla y tipo.
- [ ] **T-03 Navegación desde la vista de nodos.** En `graph-editor-page`, `onCreateChosen`:
  - `theory` → `content/new`.
  - `practical-challenge` / `theoretical-challenge` → `challenge/new?type=…`.
  - `subsection` → `subsection/new`.
  - Usar `courseSectionId` de la unidad o la ruta sin sección. Pasar `nodeUnitId` y `returnUrl = router.url`.
  - `section` queda como hoy, con el formulario de sección.
- [ ] **T-04 Volver con el nodo seleccionado.** Las pantallas devuelven `select=<nodeId>` al `returnUrl` cuando vienen del mapa, y el editor lo enfoca y lo anuncia.
- [ ] **T-05 Quitar el wizard de la vista de nodos.** Sacar `<app-node-creation-wizard>` y su estado del editor: `creationKind`, `wizardDraft`, `onWizardCreateChallenge`, `saveCreatedNode`, `saveCreatedSubsection`, `contentUpload*` si no quedan usos. El chooser se mantiene como paso previo.
- [ ] **T-06 Quitar el wizard de la vista simple.** Sacar `openWizard`, `wizardSectionId`, `wizardDraft`, el camino `draft.wizard` de `resumeDraft` y el `<app-node-creation-wizard>` del HTML de `roadmap-section-nodes`. Los borradores viejos con `wizard` se descartan.
- [ ] **T-07 Borrar `ui/node-creation-wizard/`** (componente, CSS, specs) y las claves i18n que queden huérfanas, una vez que T-05 y T-06 no dejen usos.
- [ ] **T-08 Permisos Profesor, Gestor y Admin.**
  - Rutas `content/new`, `challenge/new` y `subsection/new` con `permissionGuard('editRoadmap')`.
  - `cohortProfessorGuard`, o un guard nuevo para estas tres rutas, deja pasar a quien tenga `editRoadmap` aunque no sea miembro.
  - Dentro de la pantalla de desafío, «crear nuevo» solo con `authorChallenges` (ver hueco 7).
  - Verificar con la skill `tpi-front-permissions`.
- [ ] **T-09 Edición sin cambios.** Comprobar que `app-entity-editor-dialog` sigue editando igual en las dos vistas, incluida la ida y vuelta a `/challenges/new` para cambiar el desafío.
- [ ] **T-10 Tests y verify** solo antes de abrir la PR (memoria «sin tests al programar»): specs de las pantallas (query nueva), del editor (navegación) y de los guards.

## Fuera de alcance
- Rediseño del panel de edición (`app-entity-editor-dialog`): se hace después.
- Alta de **sección** (no subsección): sigue con su formulario actual.
- Que Gestor y Admin creen el payload de un desafío nuevo: necesita back.

## Preguntas abiertas
- Hueco 7: ¿alcanza con que Gestor y Admin **asignen** desafíos existentes, o hace falta pedir el cambio de back para que también los **creen**?
