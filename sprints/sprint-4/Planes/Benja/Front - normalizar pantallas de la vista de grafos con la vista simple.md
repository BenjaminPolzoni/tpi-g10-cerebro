---
tags: [tpi, g10, sprint-4, plan, front, roadmap, graph-editor, courses]
fecha: 2026-11-22
autor: Benjamin Polzoni
estado: en curso
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
- [ ] **N-01: chooser «Crear» del grafo.** Mismas opciones que la vista simple, más Sección (5 en total): Recurso, Repositorio de GitHub, Desafío, Subsección y Sección. Mismos textos e iconos que `contentActionItems()`; reutilizar esas claves i18n. Borrar `practical-challenge` y `theoretical-challenge` del tipo `CreateChoice` y del i18n (es/en/pt).
- [ ] **N-02: Recurso.** Abre el mismo `ResourceWizard` («Agregar recursos») que la vista simple, con el mismo host o la misma ruta, y se cierra o vuelve al grafo. Ya no navega a `content/new`.
- [ ] **N-03: editar recurso.** En el grafo, un nodo de archivo, link, video o texto abre el `ResourceWizard` en modo edición («Editar recurso»), con la misma regla que `edit(row)` de RSN. Los demás nodos siguen con `navigateNodeEdit`.
- [ ] **N-04: Repositorio de GitHub.** Mismo flujo que la vista simple: `RepositorySelectionPage`, o el drawer si la unidad es propia del roadmap, con `returnUrl` al grafo.
- [ ] **N-05: Desafío.** Una sola opción que navega a `…/challenge/new` **sin** `type`. El tipo se elige en la pantalla.
- [ ] **N-06: editar subsección o sección.** Toda acción de editar del grafo (⋮ «Cambiar nombre», el lápiz o el inspector) navega a la misma pantalla que la vista simple, `…/sections/:id/edit` (`SectionEditPage`), con `returnUrl`. «Regla de sección» sigue abriendo prerrequisitos, pero no la usa ninguna acción de «editar». Si `SectionEditPage` no tiene el estilo de `SubsectionCreatePage` (pasos Información y Prerrequisitos), igualarla, porque la vista simple también la usa.
- [ ] **N-07: crear sección y subsección desde el ⋮.** «Agregar subsección» del ⋮ → `SubsectionCreatePage`. «Sección» → `general/section/new`. Las dos llevan `returnUrl` y dejan de usar `SectionFormModal` y el drawer. Antes de borrar el modal o el drawer, comprobar si los usa una sección propia del roadmap: en ese caso, mismo criterio que la vista simple.
- [ ] **N-08: volver desde prerrequisitos.** Arreglar la causa en `shared/ui/back-link/back-link.component.ts`: si `to` es un string con `?` o `#`, pasar `router.parseUrl(to)` (un UrlTree) a `routerLink`. Lo mismo en los `[routerLink]="returnUrl()"` de `requirements-picker-page.component.html`. Además, `backLabel` compara `endsWith('/graph')` y tiene que reconocer `/map` (ignorando la query).
- [ ] **N-09: el regreso al grafo.** Toda pantalla abierta desde el grafo (creación, edición, repositorio, prerrequisitos) vuelve con `returnUrl = router.url` al grafo, a la misma comisión y roadmap.

## Fuera de alcance
- «Resumir» en la tarjeta de sección: no es «Organizar». Colapsa la sección a sus nodos de entrada e hitos (`setView(unit,'summary')`) y aparece cuando la sección supera `summaryThreshold` nodos. No hay ninguna acción «Organizar». El único layout es «Restablecer mapa» en la toolbar.
- Back: no hace falta.
