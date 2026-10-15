---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-28
estado: Propuesta
responsable: ""
epica: "Consistencia visual con la UI-KIT"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Should
en_taiga: false
---

# HT-28: Overlays y componentes locales al kit

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Consistencia visual con la UI-KIT|Consistencia visual con la UI-KIT]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HT-28 — Overlays y componentes locales al kit
-----------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: USUARIO
*   **Quiero**: diálogos y componentes del roadmap accesibles y consistentes con el kit
*   **Para**: usar el mundo con teclado y lector de pantalla

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: `streak` se saca de la UI o se conecta a datos reales (hoy muestra 7 fijo, DT-13).
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Los diálogos del kit manejan el foco y Escape.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: `npc-dialogue` y `shop-interior` con `generic-modal`/`generic-drawer`.
*   [ ] **CA2**: `lives`, `level-hud`, `inventory-item-card` y `role-switch` con componentes del kit.
*   [ ] **CA3**: `streak` sacado o conectado a datos reales.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Componentes del kit

**Escenario 1**  

*   **Dado**: el diálogo de un NPC
*   **Cuando**: se abre
*   **Entonces**: el foco entra y Escape lo cierra

**Escenario 2**  

*   **Dado**: las vidas del alumno
*   **Cuando**: se muestran
*   **Entonces**: usan `generic-progress [hearts]`

**Escenario 3**  

*   **Dado**: la racha
*   **Cuando**: se mira el HUD
*   **Entonces**: no muestra un número falso

* * *

Prototipo
---------

*   **Capturas**: HUD y diálogos del mundo.
*   **URL Figma**: No aplica.
*   **Storybook**: `generic-modal`, `generic-xp-bar`, `generic-item-tile`.
*   **Mock API / Swagger**: No aplica.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 5
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 5 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: Componentes listados.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Ninguno.

## Tareas

- [ ] T-28.1 Diálogos
- [ ] T-28.2 HUD
- [ ] T-28.3 Racha

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

`npc-dialogue` y `shop-interior` tienen su propio `role="dialog"`. `lives`, `streak`, `role-switch`, `inventory-item-card` y `level-hud` son componentes propios.

### Depende de

- [[sprints/sprint-3/historias/HT-25 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs|HT-25]] Subir la UI-KIT a 0.8.0 y cerrar sus TODOs

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E12]]

### Deuda técnica que cierra

- [[deuda-tecnica|DT-13]]
