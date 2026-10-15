---
tags: [tpi, g10, sprint-3, epica]
estado: Propuesta
sprint: "G10 - Sprint 3"
historias: 2
puntos: 16
---

# Consistencia visual con la UI-KIT

> [!info] Épica del Sprint 3 · **2 historias** · **16 pts** · Estado: **Propuesta** (todavía no está en Taiga).

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
*   [ ] El componente de grafo existe en el kit (HT-34) y lo usa la vista de grafo (HU-62).
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
| [[sprints/sprint-3/historias/HT-26 Adopción de la UI-KIT en el roadmap\|HT-26]] | Adopción de la UI-KIT en el roadmap | Nueva | 8 | Must ⭐ 1 | — | [[sprints/sprint-3/08-dudas\|G13]] ✅, [[sprints/sprint-3/08-dudas\|E12]] ✅ |
| [[sprints/sprint-3/historias/HT-34 Componente de grafo en la UI-KIT\|HT-34]] | Componente de grafo en la UI-KIT | Nueva | 8 | Must ⭐ 1 | — | [[sprints/sprint-3/08-dudas\|G13]] ✅ |

---

## Origen (no va a Taiga)

[[sprints/sprint-3/05-ui-kit|05-ui-kit]]
