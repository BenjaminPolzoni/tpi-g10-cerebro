---
tags: [tpi, g10, sprint-3, historia, hu]
id: M09
tipo: HU
epica: "EP-S3-1"
capa: "Front (+ Back)"
esfuerzo: L
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M02, U06]
---

# M09: Vista de grafo cómoda para el profesor

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HU** · Capa: **Front (+ Back)** · Esfuerzo: **L** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como profesor quiero ver y editar el roadmap como un grafo cómodo.

## Qué hay hoy

La vista de grafo existe pero es incómoda. `moveNode` devuelve 501: las posiciones no se guardan.

## Criterios de aceptación

- [ ] Acomodo automático (`elkjs`), zoom, pan y minimapa.
- [ ] Las posiciones se guardan y se recuperan.
- [ ] Se crean y borran aristas arrastrando de un nodo a otro.
- [ ] Usa el componente de grafo del kit (U06) y el endpoint `/roadmaps/{id}/graph`.
- [ ] Se puede usar con teclado (foco y selección).

## Depende de

- [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps|M02]] Modelo 1 a N de curso a roadmaps
- [[sprints/sprint-3/historias/U06 Componente de grafo en la UI-KIT|U06]] Componente de grafo en la UI-KIT

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G13]]
