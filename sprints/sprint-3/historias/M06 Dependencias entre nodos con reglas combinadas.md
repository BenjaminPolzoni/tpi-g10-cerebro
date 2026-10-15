---
tags: [tpi, g10, sprint-3, historia, hu]
id: M06
tipo: HU
epica: "EP-S3-1"
capa: "Back + Front"
esfuerzo: M
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M02, M03]
---

# M06: Dependencias entre nodos con reglas combinadas

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HU** · Capa: **Back + Front** · Esfuerzo: **M** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como profesor quiero definir de qué nodos depende cada nodo, incluso con reglas como `A y (B o C)`.

## Qué hay hoy

Existen dependencias AND/OR entre nodos (V5/V7) con lectura obligatoria, pero un solo modo por nodo.

## Criterios de aceptación

- [ ] El profesor arma una regla con AND, OR y anidamiento.
- [ ] La regla se guarda como árbol (`Rule` en Neo4j).
- [ ] No se puede guardar un ciclo.
- [ ] El alumno ve qué le falta para desbloquear el nodo.

## Depende de

- [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps|M02]] Modelo 1 a N de curso a roadmaps
- [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial|M03]] Módulo graph en Neo4j y migración inicial

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P7]]
