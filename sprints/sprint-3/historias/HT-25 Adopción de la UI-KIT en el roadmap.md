---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-25
estado: Propuesta
responsable: ""
epica: "Consistencia visual con la UI-KIT"
sprint: "G10 - Sprint 3"
puntos: 21
prioridad: Must
en_taiga: false
---

# HT-25: Adopción de la UI-KIT en el roadmap

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Consistencia visual con la UI-KIT|Consistencia visual con la UI-KIT]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga. El 2026-10-15 junta en una sola HT todo lo de la UI-KIT, que antes eran HT-25 a HT-29 y HU-70 (27 puntos en 6 historias).

[G10] — HT-25 — Adopción de la UI-KIT en el roadmap
---------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: que todas las pantallas del roadmap usen la UI-KIT 0.8.0 (componentes, controles, diálogos, tablas y tokens) y sumar al kit el componente de grafo
*   **Para**: que el roadmap se vea y se use igual que el resto de la plataforma, en tema claro y oscuro, con teclado y lector de pantalla

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Se reemplazan los controles, botones, diálogos, tablas y chips propios por los del kit, y los colores por tokens (se borra el puente `--color-*`). Quedan afuera `engine/` y el arte. El componente de grafo lo hacemos nosotros (G13) y se publica en el kit. El anonimato del ranking se mantiene (DEC-007). La racha real se resuelve en HU-73.
*   [ ] Validaciones: `npm run verify` y tests visuales en verde. Regla de `stylelint` contra hex/rgb literales en las carpetas de G10. Sin `::ng-deep` nuevos.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Labels, foco y estados de error del kit; los diálogos del kit manejan el foco y Escape; tablas con `caption` y encabezados; el grafo se recorre con teclado, con foco visible y minimapa.
*   [ ] Otros: Avisar a los otros grupos del front de los cambios visuales del bump.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El front está en la UI-KIT 0.8.0 y los TODOs que esperaban al kit están cerrados (incluye HU-22: insignias en solo lectura en `ranking-detail`).
*   [ ] **CA2**: `entity-editor-dialog`, `badges-catalog-page` y `avatar-panel` usan los controles del kit, y los botones y headings sueltos de `course-editor-page`, `section-nodes`, `course-map-page`, `hex-world-page` y `feedback-toast` también.
*   [ ] **CA3**: Sin colores literales fuera de `engine/` y del arte, puente `--color-*` borrado y regla de `stylelint` activa.
*   [ ] **CA4**: `npc-dialogue` y `shop-interior` usan `generic-modal`/`generic-drawer`, y `lives`, `level-hud`, `inventory-item-card` y `role-switch` usan componentes del kit.
*   [ ] **CA5**: El ranking usa `generic-table` y `generic-badge`, con el anonimato intacto.
*   [ ] **CA6**: `generic-node-graph` publicado en una versión del kit, con pan, zoom, minimapa, aristas y teclado, y usado por HU-62.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Roadmap con la UI-KIT

**Escenario 1**  

*   **Dado**: el editor de un nodo
*   **Cuando**: el profesor lo recorre con teclado
*   **Entonces**: todos los controles son del kit, con label, foco visible y estado de error

**Escenario 2**  

*   **Dado**: el roadmap en tema oscuro
*   **Cuando**: el alumno abre el mapa, el HUD y el ranking
*   **Entonces**: los colores salen de los tokens del kit y no hay colores fijos

**Escenario 3**  

*   **Dado**: el diálogo de Archibaldo abierto
*   **Cuando**: el alumno presiona Escape
*   **Entonces**: el diálogo se cierra y el foco vuelve a donde estaba

* * *

Prototipo
---------

*   **Capturas**: Editor, mapa, HUD, diálogos del mundo y ranking, en tema claro y oscuro.
*   **URL Figma**: Pendiente.
*   **Storybook**: Storybook del kit 0.8.0 (`generic-modal`, `generic-drawer`, `generic-table`, `generic-badge`, `generic-xp-bar`, `generic-item-tile`, tokens) y la historia nueva de `generic-node-graph`.
*   **Mock API / Swagger**: No aplica.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 21
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 21 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: Todo el front del roadmap y el ranking; repo `2026-PIV-TPI-UI-KIT` (componente de grafo).
*   Otros equipos / aprobaciones: Equipo del kit, para publicar el componente de grafo (el dueño es G10). Avisar a los otros grupos del front por el bump.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Regresiones visuales en pantallas propias y de otros grupos; mitigación: tests visuales. Que el kit no acepte el componente de grafo; mitigación: acordarlo antes de empezar (T-25.13).

## Tareas

**Bump y TODOs**
- [x] T-25.1 Mergear el bump a 0.8.0 (front `develop`, PR #567)
- [ ] T-25.2 Cerrar los TODOs destrabados (#59, #53, #51, #83/#84/#85 y `::ng-deep` de pagination) e insignias en solo lectura en `ranking-detail` (HU-22)
- [ ] T-25.3 Avisar a los otros grupos del front

**Controles y botones** (antes HT-26)
- [ ] T-25.4 Formularios del kit en `entity-editor-dialog`, `badges-catalog-page` y `avatar-panel`
- [ ] T-25.5 Botones y headings del kit en `course-editor-page`, `section-nodes`, `course-map-page`, `hex-world-page` y `feedback-toast`

**Colores y espaciado con tokens** (antes HT-27)
- [ ] T-25.6 Reemplazar los colores literales por tokens
- [ ] T-25.7 Borrar el puente `--color-*`
- [ ] T-25.8 Regla de `stylelint` contra hex/rgb

**Overlays y componentes locales** (antes HT-28)
- [ ] T-25.9 `npc-dialogue` y `shop-interior` con `generic-modal`/`generic-drawer`
- [ ] T-25.10 HUD con el kit: `lives`, `level-hud`, `inventory-item-card` y `role-switch` (la racha va en HU-73)

**Ranking** (antes HT-29)
- [ ] T-25.11 `generic-table` y `generic-badge` en `ranking/*`
- [ ] T-25.12 Tests del ranking (anonimato y visuales)

**Componente de grafo en el kit** (antes HU-70)
- [ ] T-25.13 Acordar con el equipo del kit
- [ ] T-25.14 Componente `generic-node-graph` (envuelve `ngx-vflow` o `@foblex/flow` + `elkjs`, con tokens)
- [ ] T-25.15 Storybook y release del kit

**Cierre**
- [ ] T-25.16 Tests visuales en tema claro y oscuro

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

- El bump a 0.8.0 ya está en `develop` del front (PR #567). Quedan 9 TODOs que se destraban con 0.8.0 (incluye ui-kit#59 de HU-22).
- `entity-editor-dialog`, `badges-catalog-page` y `avatar-panel` usan `<input>`, `<select>` y `<button>` crudos; hay botones y headings sueltos en `course-editor-page`, `section-nodes`, `course-map-page`, `hex-world-page` y `feedback-toast`.
- 316 colores hardcodeados y un puente de tokens `--color-*` propio.
- `npc-dialogue` y `shop-interior` tienen su propio `role="dialog"`; `lives`, `streak`, `role-switch`, `inventory-item-card` y `level-hud` son componentes propios.
- El ranking tiene 3 `<table>` crudas y chips propios.
- El kit no tiene componente de grafo; la vista de grafo del roadmap es un SVG propio.

Detalle en [[sprints/sprint-3/05-ui-kit|05-ui-kit]].

### Depende de

Nada: se puede empezar ya.

### Deuda técnica que cierra

- [[deuda-tecnica|DT-15]]

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|G13]] El componente de grafo es nuestro (G10). El avatar no se usa como foto de perfil.
- ✅ [[sprints/sprint-3/08-dudas|E12]] Avatares ya está hecho; la racha va en [[sprints/sprint-3/historias/HU-73 Ver mi racha de días con actividad|HU-73]].
