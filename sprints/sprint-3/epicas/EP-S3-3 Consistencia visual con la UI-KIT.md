---
tags: [tpi, g10, sprint-3, epica]
id: EP-S3-3
estado: Propuesta
historias: 6
---

# EP-S3-3: Consistencia visual con la UI-KIT

> [!info] Épica propuesta del Sprint 3. **6 ítems** (3 S · 2 M · 1 L). Todavía no está en Taiga.

## Objetivo

Que las pantallas del roadmap y del ranking usen la UI-KIT (`@2026-p4-fe/ui`) en vez de controles y colores propios, y aportar al kit el componente de grafo.

## Criterios de aceptación a nivel épica

- [ ] El front está en la UI-KIT 0.8.0 sin TODOs pendientes del kit.
- [ ] Las pantallas de G10 no tienen `<button>`, `<input>` ni `<select>` crudos ni colores hardcodeados (salvo `engine/` y arte).
- [ ] El componente de grafo existe en el kit y lo usa la vista de grafo (M09).

## Historias

| ID | Tipo | Título | Capa | Esf. | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | HT | Subir la UI-KIT a 0.8.0 y cerrar sus TODOs | Front | S | — | [[sprints/sprint-3/08-dudas\|G13]] |
| [[sprints/sprint-3/historias/U02 Controles y botones del roadmap con el kit\|U02]] | HT | Controles y botones del roadmap con el kit | Front | S | [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | — |
| [[sprints/sprint-3/historias/U03 Colores y espaciado del roadmap con tokens\|U03]] | HT | Colores y espaciado del roadmap con tokens | Front | M | [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | — |
| [[sprints/sprint-3/historias/U04 Overlays y componentes locales al kit\|U04]] | HT | Overlays y componentes locales al kit | Front | M | [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | [[sprints/sprint-3/08-dudas\|E12]] |
| [[sprints/sprint-3/historias/U05 Ranking con componentes del kit\|U05]] | HT | Ranking con componentes del kit | Front | S | [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | — |
| [[sprints/sprint-3/historias/U06 Componente de grafo en la UI-KIT\|U06]] | HU | Componente de grafo en la UI-KIT | UI-KIT | L | [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | [[sprints/sprint-3/08-dudas\|G13]] |

## Origen

[[sprints/sprint-3/05-ui-kit|05-ui-kit]]
