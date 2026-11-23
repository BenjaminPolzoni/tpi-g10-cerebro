---
tags: [tpi, g10, sprint-4, plan, front, roadmap, graph-editor, courses]
fecha: 2026-11-22
autor: Benjamin Polzoni
estado: PR #3131, N-18/N-19 en curso
repo: 2026-P4-FE/2026-PIV-TPI-FE
rama: BenjaminPolzoni/Normalizar-pantallas-videjas-de-la-vista-de-grafos (worktree ~/orca/workspaces/2026-PIV-TPI-FE/Normalizar-pantallas-videjas-de-la-vista-de-grafos)
---

# Plan: normalizar las pantallas de la vista de grafos con las de la vista simple

## Decisión (Benja, 2026-11-22)
En la vista de grafos (`/roadmap/teacher/course/:id/map`), crear y editar secciones, subsecciones, recursos, repositorios de GitHub y desafíos tiene que usar **exactamente las mismas pantallas y opciones que la vista simple** (`/courses/:cohortId/general`). Al guardar, cancelar o volver, siempre se vuelve a la vista de grafos.

## Estado actual (relevado 2026-11-22, después de mergear develop)
| # | Acción | Vista de grafos (`graph-editor-page.component.ts`, GEP) | Vista simple (la referencia) |
|---|---|---|---|
| 1 | Menú «Crear» | `onCreateChosen` (GEP ~1812) con 5 tipos: Contenido teórico, Desafío práctico, Desafío teórico, Subsección, Sección | «+ Añadir a la sección» (`contentActionItems()` en `courses/ui/section-content-actions/section-content-actions.ts`): Recurso, Repositorio de GitHub, Desafío, Subsección |
| 2 | Crear recurso | `…/content/new` → `ContentNodeCreatePage` («Nuevo contenido») | `openResourceWizard()` (RSN ~1752): `ResourceWizardHost` → `ResourceWizard` («Agregar recursos»). También existe la ruta `general/resources/new` → `CohortMaterialCreatePage` |
| 3 | Editar recurso | `navigateNodeEdit` (GEP ~1169) → `…/content/:nodeId/edit` → `ContentNodeCreatePage` («Editar nodo») | `edit(row)` (RSN ~1656): un archivo, link, video o texto abre `openResourceEdit` → `ResourceWizard` en modo edición («Editar recurso») |
| 4 | Repositorio de GitHub | No existe | `CGP.openRepositoryBoard` → `…/sections/:sid/repository` → `RepositorySelectionPage`. En una unidad propia del roadmap, `addRepository` (RSN ~2008) |
| 5 | Desafío | Dos opciones; navega con `?type=PRACTICAL\|THEORETICAL` | Una sola opción, «Desafío» → `…/challenge/new` sin `type`. El tipo se elige dentro de la pantalla |
| 6 | Crear subsección | Chooser → `SubsectionCreatePage` (OK). El «Agregar subsección» del ⋮ abre `SectionFormModal` | `SubsectionCreatePage` |
| 7 | Editar subsección o sección | El ⋮ «Cambiar nombre» abre `SectionFormModal`. La edición termina en la página de prerrequisitos | `openSectionSettings` (CGP ~1644) → `…/sections/:id/edit` → `SectionEditPage` |
| 8 | Crear sección | `openNewSection` (GEP ~1465): `SectionFormModal` o el drawer `sectionFormOpen` | `CGP.openCreateSection` → `general/section/new` → `SubsectionCreatePage` con kind=section |
| 9 | Volver desde prerrequisitos | `RequirementsPickerPage`: «Volver» usa `<app-back-link [to]="returnUrl()">` y `[routerLink]="returnUrl()"`. Si el returnUrl trae `?roadmap=…`, `routerLink` toma el `?` como parte del path y el `**` redirige a `/roadmap/teacher` | «Cancelar» y «Guardar y volver» funcionan porque usan `navigateByUrl` |

## Tareas
- [x] **N-01: chooser «Crear» del grafo.** Mismas opciones que la vista simple, más Sección (5 en total): Recurso, Repositorio de GitHub, Desafío, Subsección y Sección. Mismos textos e iconos que `contentActionItems()`; reutilizar esas claves i18n. Borrar `practical-challenge` y `theoretical-challenge` del tipo `CreateChoice` y del i18n (es/en/pt).
- [x] **N-02: Recurso.** Abre el mismo `ResourceWizard` («Agregar recursos») que la vista simple, con el mismo host o la misma ruta, y se cierra o vuelve al grafo. Ya no navega a `content/new`.
- [x] **N-03: editar recurso.** En el grafo, un nodo de archivo, link, video o texto abre el `ResourceWizard` en modo edición («Editar recurso»), con la misma regla que `edit(row)` de RSN. Los demás nodos siguen con `navigateNodeEdit`.
- [x] **N-04: Repositorio de GitHub.** Mismo flujo que la vista simple: `RepositorySelectionPage`, o el drawer si la unidad es propia del roadmap, con `returnUrl` al grafo.
- [x] **N-05: Desafío.** Una sola opción que navega a `…/challenge/new` **sin** `type`. El tipo se elige en la pantalla.
- [x] **N-06: editar subsección o sección.** Toda acción de editar del grafo (⋮ «Cambiar nombre», el lápiz o el inspector) navega a la misma pantalla que la vista simple, `…/sections/:id/edit` (`SectionEditPage`), con `returnUrl`. «Regla de sección» sigue abriendo prerrequisitos, pero no la usa ninguna acción de «editar». Si `SectionEditPage` no tiene el estilo de `SubsectionCreatePage` (pasos Información y Prerrequisitos), igualarla, porque la vista simple también la usa.
- [x] **N-07: crear sección y subsección desde el ⋮.** «Agregar subsección» del ⋮ → `SubsectionCreatePage`. «Sección» → `general/section/new`. Las dos llevan `returnUrl` y dejan de usar `SectionFormModal` y el drawer. Antes de borrar el modal o el drawer, comprobar si los usa una sección propia del roadmap: en ese caso, mismo criterio que la vista simple.
- [x] **N-08: volver desde prerrequisitos.** Arreglar la causa en `shared/ui/back-link/back-link.component.ts`: si `to` es un string con `?` o `#`, pasar `router.parseUrl(to)` (un UrlTree) a `routerLink`. Lo mismo en los `[routerLink]="returnUrl()"` de `requirements-picker-page.component.html`. Además, `backLabel` compara `endsWith('/graph')` y tiene que reconocer `/map` (ignorando la query).
- [x] **N-09: el regreso al grafo.** Toda pantalla abierta desde el grafo (creación, edición, repositorio, prerrequisitos) vuelve con `returnUrl = router.url` al grafo, a la misma comisión y roadmap.

- [x] **N-10, menú ⋮ de sección (2026-11-22):** quedan Tema/bioma, Editar sección (→ `SectionEditPage`, `stepStart=rules` desde las flechas «requiere»), Agregar subsección, Mostrar/Ocultar y Eliminar. Se quitaron Regla de sección, Crear unidades en General, Cambiar nombre, Subir y Bajar.
- [x] **N-11, atajos y Esc (2026-11-22):** el panel lista solo `+`, `-`, `0` y `Esc`. Esc deselecciona el nodo, la sección o la relación y cierra el panel; si hay un overlay abierto, cierra solo ese overlay.
- [x] **N-12, XP mínimo al crear sección o subsección (2026-11-23):** el paso Prerrequisitos de `SubsectionCreatePage` (que usa `SectionFormModal` con `showPrerequisites`) suma el mismo campo «XP mínimo (opcional)» que el paso Prerrequisitos de `SectionEditPage` (`section-editor-drawer`). Al crear, la regla se guarda con `minXp` por el mismo camino que la edición. Vale para secciones y subsecciones, en Courses y en roadmaps propios. Se puede crear solo con XP, sin elementos.
- [x] **N-13, `reloadAfterWrite` (2026-11-23):** después de un alta en el grafo (asistente de recursos, drawer de repositorio), recargar `cohortContents` con `reloadAfterWrite(resource, injector)` de `core/http`, no con `reload()`. Es la regla nueva de CLAUDE.md.

### Review de la PR #3131 (MateoDelgadoCosta, 2026-11-23, CHANGES_REQUESTED)
- [x] **N-14: vista simple con unidad OWN.** En `cohort-general-page.component.ts` `onAssistantChosen`, decidir por `unit.courseSectionId`. Si la unidad tiene sección de Courses: Recurso → `general/resources/new?sectionId=…` y Repositorio → `general/sections/:sid/repository` (con `roadmapId`/`nodeUnitId` si el roadmap no es el principal). Si no tiene (OWN): Recurso crea el nodo en la unidad, igual que el grafo (ResourceWizard embebido con la unidad, o `content/new?nodeUnitId=…`). Repositorio pasa siempre `roadmapId` + `nodeUnitId`. Specs en `cohort-general-page.component.spec.ts` para los 5 tipos, con sección de Courses y con unidad OWN.
- [x] **N-15: sacar `description` inventado.** Quitarlo de `BackendSectionResponse`, del mapper y de `Section`: tpi-roadmap no lo tiene. En el modal «Editar sección» de una unidad OWN (`graph-editor-page` `ownSectionEditing`), ocultar el campo descripción, como hacía «Cambiar nombre», para no descartarlo en silencio.
- [x] **N-16: código muerto.** Borrar `RoadmapStore.addZone` y su spec, y las claves i18n sin uso `graphEditor.sectionActions.created`, `graphEditor.wizard.newZoneOf` y `graphEditor.ownership.zoneInCourses` (es/en/pt), si grep confirma que no se usan.
- [x] **N-17: Esc con el panel mobile.** Si lo único abierto es el panel mobile, Esc tiene que cancelar el lote o la selección pendiente y deseleccionar, no tratarlo como overlay.
- [ ] **N-18: el grafo usa la página de recursos.** Develop (`fe36f2dec3`) pasó «Recurso» y «Editar» de un recurso en la vista simple a una página propia (`general/[sections/:sid/]resource-wizard`, `ResourceWizardPageComponent` + `ResourceWizardHandoffService`), como `goToResourceWizard` de `roadmap-section-nodes`. El grafo sigue con `ResourceWizardHost` como capa encima de toda la pantalla: tiene que navegar a esa página, con `returnUrl` al grafo, y borrar el host del grafo (`resourceWizardUnitId`/`resourceWizardEdit`).
- [ ] **N-19: el «Crear → Recurso» de la vista simple** (`cohort-general-page` `onAssistantChosen`) va a la misma página, no a `resources/new` ni a `content/new`, tanto con sección de Courses como en una unidad OWN.
- Subir/Bajar: los quitó el usuario a propósito; se le responde así al reviewer.
- `local-verify`: después de agy, `npm run verify` y push **con** el hook. El fallo de compose-quiz ya está arreglado en develop (#3128).

## Fuera de alcance
- «Resumir» en la tarjeta de sección: no es «Organizar». Colapsa la sección a sus nodos de entrada e hitos (`setView(unit,'summary')`) y aparece cuando la sección supera `summaryThreshold` nodos. No hay ninguna acción «Organizar». El único layout es «Restablecer mapa» en la toolbar.
- Back: no hace falta.
