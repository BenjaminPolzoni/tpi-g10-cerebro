---
tags: [tpi, g10, sprint-3, epica]
estado: Propuesta
sprint: "G10 - Sprint 3"
historias: 6
puntos: 27
---

# Consistencia visual con la UI-KIT

> [!info] Épica del Sprint 3 · **6 historias** · **27 pts** · Estado: **Propuesta** (todavía no está en Taiga).

[G10] — Consistencia visual con la UI-KIT
-----------------------------------------

* * *

Objetivo
--------

Que las pantallas del roadmap y del ranking usen la UI-KIT (`@2026-p4-fe/ui`) en vez de controles y colores propios, y aportar al kit el componente de grafo.

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: El front usa la UI-KIT `@2026-p4-fe/ui` 0.7.1; la 0.8.0 está lista en `feature/ui-lib-0-8-0`.
*   Restricciones (legales/técnicas): Quedan afuera `engine/` (three.js) y el arte. Lo que falta en el kit se aporta al kit, no se hace local.

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] El front está en la UI-KIT 0.8.0 sin TODOs pendientes del kit.
*   [ ] Las pantallas de G10 no tienen `<button>`, `<input>` ni `<select>` crudos ni colores hardcodeados (salvo `engine/` y arte).
*   [ ] El componente de grafo existe en el kit y lo usa la vista de grafo (HU-62).
*   [ ] KPIs iniciales alcanzan: Colores hardcodeados en el roadmap: de 316 a 0 fuera de `engine/` y arte. TODOs del kit: de 9 a 0.
*   [ ] Sin regresiones críticas en: Tests visuales sin diferencias no esperadas en pantallas de otros grupos.
*   [ ] Observabilidad y alertas configuradas: Regla de `stylelint` en el CI contra colores literales.
*   [ ] Documentación de uso y operación publicada: README del kit con el componente de grafo.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: Ninguno.
*   Módulos afectados: Pantallas del roadmap y del ranking; repo de la UI-KIT.
*   Otros equipos: Equipo de la UI-KIT; resto de los grupos del front (bump).
*   Impacto en datos / migraciones: Sin migración.
*   Feature toggles / flags: Ninguno.

## Historias

| HU | Título | En Taiga | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/HT-25 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|HT-25]] | Subir la UI-KIT a 0.8.0 y cerrar sus TODOs | Nueva | 3 | Must | — | [[sprints/sprint-3/08-dudas\|G13]] |
| [[sprints/sprint-3/historias/HT-26 Controles y botones del roadmap con el kit\|HT-26]] | Controles y botones del roadmap con el kit | Nueva | 3 | Should | [[sprints/sprint-3/historias/HT-25 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|HT-25]] | — |
| [[sprints/sprint-3/historias/HT-27 Colores y espaciado del roadmap con tokens\|HT-27]] | Colores y espaciado del roadmap con tokens | Nueva | 5 | Could | [[sprints/sprint-3/historias/HT-25 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|HT-25]] | — |
| [[sprints/sprint-3/historias/HT-28 Overlays y componentes locales al kit\|HT-28]] | Overlays y componentes locales al kit | Nueva | 5 | Should | [[sprints/sprint-3/historias/HT-25 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|HT-25]] | [[sprints/sprint-3/08-dudas\|E12]] |
| [[sprints/sprint-3/historias/HT-29 Ranking con componentes del kit\|HT-29]] | Ranking con componentes del kit | Nueva | 3 | Should | [[sprints/sprint-3/historias/HT-25 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|HT-25]] | — |
| [[sprints/sprint-3/historias/HU-70 Componente de grafo en la UI-KIT\|HU-70]] | Componente de grafo en la UI-KIT | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-25 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|HT-25]] | [[sprints/sprint-3/08-dudas\|G13]] |

---

## Origen (no va a Taiga)

[[sprints/sprint-3/05-ui-kit|05-ui-kit]]
