---
tags: [tpi, g10, sprint-3, epica]
id: EP-S3-3
estado: Propuesta
historias: 6
puntos: 27
---

# EP-S3-3: Consistencia visual con la UI-KIT

> [!info] Épica propuesta del Sprint 3. **6 historias**, **27 pts**. Todavía no está en Taiga.
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Objetivo* hasta *Dependencias / Impactos*.

**[G10] — Consistencia visual con la UI-KIT**

* * *

## Objetivo

Que las pantallas del roadmap y del ranking usen la UI-KIT (`@2026-p4-fe/ui`) en vez de controles y colores propios, y aportar al kit el componente de grafo.

* * *

## Suposiciones y Restricciones

- Suposiciones: El front usa la UI-KIT `@2026-p4-fe/ui` 0.7.1; la 0.8.0 está lista en `feature/ui-lib-0-8-0`.
- Restricciones (legales/técnicas): Quedan afuera `engine/` (three.js) y el arte. Lo que falta en el kit se aporta al kit, no se hace local.

* * *

## Criterios de Aceptación a nivel Épico

- [ ] El front está en la UI-KIT 0.8.0 sin TODOs pendientes del kit.
- [ ] Las pantallas de G10 no tienen `<button>`, `<input>` ni `<select>` crudos ni colores hardcodeados (salvo `engine/` y arte).
- [ ] El componente de grafo existe en el kit y lo usa la vista de grafo (M09).
- [ ] KPIs iniciales: Colores hardcodeados en el roadmap: de 316 a 0 fuera de `engine/` y arte. TODOs del kit: de 9 a 0.
- [ ] Sin regresiones críticas: Tests visuales sin diferencias no esperadas en pantallas de otros grupos.
- [ ] Observabilidad y alertas: Regla de `stylelint` en el CI contra colores literales.
- [ ] Documentación publicada: README del kit con el componente de grafo.

* * *

## Dependencias / Impactos

- Servicios / APIs: Ninguno.
- Módulos afectados: Pantallas del roadmap y del ranking; repo de la UI-KIT.
- Otros equipos: Equipo de la UI-KIT; resto de los grupos del front (bump).
- Impacto en datos / migraciones: Sin migración.
- Feature toggles / flags: Ninguno.

---

## Historias

| ID | Tipo | Título | Capa | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | HT | Subir la UI-KIT a 0.8.0 y cerrar sus TODOs | Front | 3 | Must | — | [[sprints/sprint-3/08-dudas\|G13]] |
| [[sprints/sprint-3/historias/U02 Controles y botones del roadmap con el kit\|U02]] | HT | Controles y botones del roadmap con el kit | Front | 3 | Should | [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | — |
| [[sprints/sprint-3/historias/U03 Colores y espaciado del roadmap con tokens\|U03]] | HT | Colores y espaciado del roadmap con tokens | Front | 5 | Could | [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | — |
| [[sprints/sprint-3/historias/U04 Overlays y componentes locales al kit\|U04]] | HT | Overlays y componentes locales al kit | Front | 5 | Should | [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | [[sprints/sprint-3/08-dudas\|E12]] |
| [[sprints/sprint-3/historias/U05 Ranking con componentes del kit\|U05]] | HT | Ranking con componentes del kit | Front | 3 | Should | [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | — |
| [[sprints/sprint-3/historias/U06 Componente de grafo en la UI-KIT\|U06]] | HU | Componente de grafo en la UI-KIT | UI-KIT | 8 | Must | [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | [[sprints/sprint-3/08-dudas\|G13]] |

## Origen

[[sprints/sprint-3/05-ui-kit|05-ui-kit]]
