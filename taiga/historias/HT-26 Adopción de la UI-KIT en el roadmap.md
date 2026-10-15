---
tags: [tpi, g10, taiga, ht]
codigo: HT-26
ref: 9268
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8630 Consistencia visual con la UI-KIT|EP-8630]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9268
---

# HT-26: Adopción de la UI-KIT en el roadmap

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9268) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8630 Consistencia visual con la UI-KIT|EP-8630]] · Tareas cerradas: **0/7**

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

- [ ] #9276 T-26.1 Formularios con los controles del kit · New · Ludmila Mailen Cejas
- [ ] #9277 T-26.2 Botones y títulos sueltos con el kit · New · Lorenzo Araujo
- [ ] #9278 T-26.3 Diálogos del mundo con el modal del kit · New · Ludmila Mailen Cejas
- [ ] #9279 T-26.4 HUD del mundo con componentes del kit · New · Ludmila Mailen Cejas
- [ ] #9280 T-26.5 Ranking con la tabla y los badges del kit · New · Ludmila Mailen Cejas
- [ ] #9281 T-26.6 Revisar todo con ui-review y tests visuales · New · Ludmila Mailen Cejas
- [ ] #9340 T-26.7 Wiki con capturas y componentes usados · New · Quinteros Tomás
