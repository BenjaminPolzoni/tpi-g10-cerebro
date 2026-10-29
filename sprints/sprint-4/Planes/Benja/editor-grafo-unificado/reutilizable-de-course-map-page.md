# Inventario de la vista de círculos eliminada

Fuente: `2f59b0291^`; líneas de esa revisión (no de la actual). El plan y sus enmiendas prevalecen: toda flecha es un requisito; no restaurar relaciones informativas ni su selector. «Reutilizar» puede significar usar el equivalente actual, no copiar la implementación vieja.

| Pieza (archivo:líneas en `2f59b0291^`) | Qué hace | Tarea | Decisión |
|---|---|---|---|
| `pages/course-map-page/course-map-page.component.ts:3282-3301,3333-3349`; `.html:989-1034` | Protege zonas sincronizadas con General y no borra zonas con hijos. | T-15 | Reutilizar: `domain/section-ownership.ts` preserva la detección por `courseSectionId`; wiring y verificación de hijos quedan para T-15. No implica permitir alta de unidad fuera de OWN. |
| `pages/course-map-page/course-map-page.component.ts:3197-3233,3307-3329`; `.html:1120-1149` | Recorta nombre y valida 3–80 caracteres antes de alta o renombre; conserva formulario ante error; el PUT conserva XP/bioma. | T-06a, T-15 | Reutilizar validación y textos en wizard; conservar el payload completo al renombrar. No copiar el formulario/modal antiguo: wizard va en panel. La autoridad final es el backend. |
| `pages/course-map-page/course-map-page.component.ts:3240-3250`; `.html:1150-1159` | Elige candidatos y guarda regla de sección. | T-05b, T-06d | Reutilizar equivalentes `prerequisite-policy`, `rule-tree` y store; guardar leaf NODE con árbol `{rule}`, no arreglo plano. |
| `pages/course-map-page/course-map-page.component.ts:1900-1952,2040-2053,2093-2099`; `.html:940-953` | Selector accesible de destino y preflight de movimiento; preserva reglas y anuncia rechazo. | T-10, T-11 | Reutilizar `domain/semantic-move.ts`, `describePrerequisiteRejection` y `RoadmapStore.moveActivityToSection`, no duplicar; backend decide elegibilidad de `contentId`. |
| `pages/course-map-page/map-drag.ts:1-108`; `course-map-page.component.ts:1648-1772` | Hit testing circular, swap o mover con drag. | T-03b, T-11 | Descartar implementación: geometría/canvas nuevos, marcos anidados y drop de conexión no equivalen a reparentar implícitamente. Mantener solo principio de no alterar reglas. |
| `pages/course-map-page/course-map-page.component.ts:2395-2410` | Colapsa unidad raíz y expande solo una. | T-03b | Descartar política de círculos: se requieren marcos anidados independientes, proyección de aristas y retorno de foco. |
| `pages/course-map-page/course-map-page.component.ts:3600-3703,3714-3791`; `.html:592-620` | Conexión por teclado, validación y anuncios; antiguo selector de tipos de relación. | T-05b, T-05c | Reutilizar `prerequisite-policy` y patrón de foco/anuncio; descartar selector/tipos informativos y mutaciones de relación, toda flecha es requisito. |
| `pages/course-map-page/course-map-page.component.ts:3544-3552` | Quita conexión o relación según tipo. | T-09 | Descartar implementación: debe quitar leaf del árbol preservando grupos y hacer rollback tras rechazo; no usar eliminación informativa. |
| `pages/course-map-page/course-map-page.component.ts:3351-3358`; `.html:967-987` | Alta contextual en unidad/zona. | T-06a, T-07 | Reutilizar intención/contexto, no página ni modal; wizard precarga sección y, para nodo origen, requisito. |
| `pages/course-map-page/course-map-page.component.html:625-675`; `course-map-page.component.ts:3714-3791` | Picker de prerrequisitos y accesos por teclado. | T-06d | Reutilizar políticas y regla existente; reimplementar interacción de picker del inspector según nuevo contrato. |
| `pages/course-map-page/course-map-page.component.ts:3383-3402` | Mapea error de carga de material con `contentErrorMessage`. | T-06a | Descartar como helper del grafo: ya existe en Courses y pertenece a carga de contenido, no a las mutaciones de grafo. Errores HTTP generales se resuelven en core. |
| `pages/course-map-page/map-layout.ts:1-682`, `map-view-mode.ts:1-26`, `ui/map-unit-list/map-unit-list.component.ts:1-183` | Layout circular, modo de vista y lista anterior. | T-03b, T-12 | Descartar: reemplazados por `domain/map-layout`, canvas y árbol; no hay búsqueda general de mapa recuperable en la página vieja. |
| `src/assets/i18n/{es,en,pt}.json:20211-20425` (líneas de es; consultar cada idioma) | Textos de mapa antiguo. | T-03b, T-06a, T-10, T-11, T-15 | Reutilizar solo textos inequívocos en `graphEditor.wizard.*`, `graphEditor.ownership.*`, `graphEditor.data.moveSection.*`; otros tienen equivalentes actuales, describen círculos/relaciones informativas o no corresponden a los flujos futuros. No inventar equivalentes de búsqueda. |

## Fragmentos de lógica relevantes

Ownership (`course-map-page.component.ts:3286-3288,3335-3337`):
```ts
return !!this.store.sectionById(sectionId)?.courseSectionId;
if (!zone?.parentSectionId || zone.courseSectionId || this.subsectionsOf(sectionId)) return;
```
El helper extraído solo detecta ownership; no sustituye las demás precondiciones de borrado ni supone que una sección ausente se puede editar.

Validación (`course-map-page.component.ts:3223-3229`):
```ts
const name = (this.zoneDraft() ?? '').trim();
if (name.length < this.zoneNameMin || name.length > this.zoneNameMax) {
  this.zoneError.set(this.i18n.t('courseMap.zoneNameHint', { min: this.zoneNameMin, max: this.zoneNameMax }));
  return;
}
```

Rechazo de movimiento (`course-map-page.component.ts:1924-1937`):
```ts
const violations = nodeMoveViolations(this.store.sections(), this.store.connections(), node.id, targetSectionId);
if (violations === null || violations.length > 0) {
  // describePrerequisiteRejection(violations?.[0]?.reasons ?? ['missing'], translate)
  return;
}
```
La traducción de motivos ya existe en `domain/prerequisite-policy.ts`; no se restaura un mapeador duplicado. El preflight no sustituye la validación del servidor.

## Omisión detectada 2026-10-29

| `course-map-page.component.html:99-130` + `.ts` (`routeRoadmapId`, `onRoadmapChange`, `onCommissionChange`, `roadmapOptions`, `commissionOptions`, `activeRoadmapName`, `commissionLabel`) | Selector de comisión, selector de roadmap y barra de contexto del mapa (multi-roadmap, T-57.3). | T-19 | Reutilizar: faltaba en este inventario y el grafo quedó sin forma de ver/cambiar el roadmap activo. |
