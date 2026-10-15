---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-26
estado: Propuesta
responsable: ""
epica: "Consistencia visual con la UI-KIT"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Must
prioridad_sprint: 1
en_taiga: false
---

# HT-26: Adopción de la UI-KIT en el roadmap

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Consistencia visual con la UI-KIT|Consistencia visual con la UI-KIT]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga. El 2026-10-15 junta en una sola HT todo lo de la UI-KIT que seguía en el sprint: HT-26, HT-28, HT-29 y HU-70 (19 puntos). HT-25 (bump y TODOs) y HT-27 (tokens) ya se habían borrado del sprint. El 2026-10-15 se dividió en dos HT de 8 (máximo por historia): esta queda con las pantallas y [[sprints/sprint-3/historias/HT-34 Componente de grafo en la UI-KIT|HT-34]] con el componente de grafo.

> [!important] Prioridad 1 del sprint (2026-10-15)
> Va primero, junto con las otras prioridad 1: HT-30 a HT-33 (criterios pendientes de HU cerradas) y HT-34 (componente de grafo). Es la parte visual: que el roadmap se vea y se use con la UI-KIT.

[G10] — HT-26 — Adopción de la UI-KIT en el roadmap
---------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: que las pantallas del roadmap usen los componentes de la UI-KIT (controles, botones, diálogos, HUD y tablas)
*   **Para**: que el roadmap se vea y se use igual que el resto de la plataforma, con teclado y lector de pantalla

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Se reemplazan los controles, botones, diálogos, componentes del HUD, tablas y chips propios por los del kit. Quedan afuera `engine/` y el arte. El componente de grafo va en HT-34. El anonimato del ranking se mantiene (DEC-007). La racha real va en HU-73.
*   [ ] Validaciones: `npm run verify` y tests visuales en verde. Sin `::ng-deep` nuevos.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Labels, foco y estados de error del kit; los diálogos del kit manejan el foco y Escape; tablas con `caption` y encabezados.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: `entity-editor-dialog`, `badges-catalog-page` y `avatar-panel` usan los controles del kit, y los botones y headings sueltos de `course-editor-page`, `section-nodes`, `course-map-page`, `hex-world-page` y `feedback-toast` también.
*   [ ] **CA2**: `npc-dialogue` y `shop-interior` usan `generic-modal`/`generic-drawer`, y `lives`, `level-hud`, `inventory-item-card` y `role-switch` usan componentes del kit.
*   [ ] **CA3**: El ranking usa `generic-table` y `generic-badge`, con el anonimato intacto.
*   [ ] **CA4**: `ui-review` no reporta hallazgos nuevos en roadmap y ranking y los tests visuales están en verde.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Roadmap con la UI-KIT

**Escenario 1**  

*   **Dado**: el editor de un nodo
*   **Cuando**: el profesor lo recorre con teclado
*   **Entonces**: todos los controles son del kit, con label, foco visible y estado de error

**Escenario 2**  

*   **Dado**: el diálogo de Archibaldo abierto
*   **Cuando**: el alumno presiona Escape
*   **Entonces**: el diálogo se cierra y el foco vuelve a donde estaba

**Escenario 3**  

*   **Dado**: el ranking de un curso
*   **Cuando**: el alumno lo abre
*   **Entonces**: lo ve en la tabla del kit, con las filas ajenas sin datos personales

* * *

Prototipo
---------

*   **Capturas**: Editor, mapa, HUD, diálogos del mundo y ranking.
*   **URL Figma**: Pendiente.
*   **Storybook**: Storybook del kit (`generic-modal`, `generic-drawer`, `generic-table`, `generic-badge`, `generic-xp-bar`, `generic-item-tile`).
*   **Mock API / Swagger**: No aplica.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Must · 1 (máxima del sprint)

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 8 | Must · 1 (máxima del sprint) |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: Pantallas del roadmap y del ranking.
*   Otros equipos / aprobaciones: Ninguno (el acuerdo con el equipo del kit está en HT-34).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Regresiones visuales; mitigación: tests visuales.

## Tareas

- [ ] **T-26.1 Formularios con los controles del kit** · Front
    - **Qué:** reemplazar `<input>`, `<select>` y `<button>` crudos por `generic-input`, `generic-select`, `generic-checkbox` y `generic-button`, con los labels y mensajes de error del kit.
    - **Dónde:** `entity-editor-dialog`, `badges-catalog-page`, `avatar-panel`.
    - **Listo cuando:** ninguno de los tres tiene controles crudos y `ui-review` no marca nada en esos archivos.
- [ ] **T-26.2 Botones y títulos sueltos con el kit** · Front
    - **Qué:** pasar los botones y headings armados a mano a `generic-button` y `generic-title`.
    - **Dónde:** `course-editor-page`, `section-nodes`, `course-map-page`, `hex-world-page`, `feedback-toast`.
    - **Listo cuando:** `ui-review` no marca botones ni títulos propios en esas pantallas.
- [ ] **T-26.3 Diálogos del mundo con el modal del kit** · Front
    - **Qué:** `npc-dialogue` y `shop-interior` dejan su `role="dialog"` propio y usan `generic-modal` o `generic-drawer`, que manejan el foco y Escape.
    - **Listo cuando:** los dos se abren y se cierran con teclado y el foco vuelve a donde estaba.
- [ ] **T-26.4 HUD del mundo con componentes del kit** · Front
    - **Qué:** `lives` con `generic-icon`/`generic-progress`, `level-hud` con `generic-xp-bar`, `inventory-item-card` con `generic-item-tile` y `role-switch` con el componente del kit que corresponda. La racha va en HU-73.
    - **Listo cuando:** el HUD no usa componentes propios para esas piezas y se ve igual o mejor que hoy.
- [ ] **T-26.5 Ranking con la tabla y los badges del kit** · Front
    - **Qué:** las 3 `<table>` crudas pasan a `generic-table` y los chips `rk-chip`/`rk-status` a `generic-badge`. El anonimato de las filas ajenas no cambia (DEC-007).
    - **Dónde:** `ranking/*` (incluye el TODO #59 de `ranking-detail`).
    - **Listo cuando:** el ranking se ve con el kit y hay tests del anonimato y visuales.
- [ ] **T-26.6 Revisar todo con `ui-review` y tests visuales** · Front
    - **Qué:** correr `ui-review` (llegó a develop en el PR #579) sobre roadmap y ranking y dejar los tests visuales en verde.
    - **Listo cuando:** `ui-review` no reporta hallazgos nuevos en roadmap y ranking.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

- `entity-editor-dialog`, `badges-catalog-page` y `avatar-panel` usan `<input>`, `<select>` y `<button>` crudos; hay botones y headings sueltos en `course-editor-page`, `section-nodes`, `course-map-page`, `hex-world-page` y `feedback-toast`.
- `npc-dialogue` y `shop-interior` tienen su propio `role="dialog"`; `lives`, `streak`, `role-switch`, `inventory-item-card` y `level-hud` son componentes propios.
- El ranking tiene 3 `<table>` crudas y chips propios.
- El kit no tiene componente de grafo: va en HT-34.
- El front ya está en la UI-KIT 0.8.0 (PR #567).

Detalle en [[sprints/sprint-3/05-ui-kit|05-ui-kit]].

### Depende de

Nada: se puede empezar ya.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|G13]] El componente de grafo es nuestro (G10). El avatar no se usa como foto de perfil.
- ✅ [[sprints/sprint-3/08-dudas|E12]] Avatares ya está hecho; la racha va en [[sprints/sprint-3/historias/HU-73 Ver mi racha de días con actividad|HU-73]].
