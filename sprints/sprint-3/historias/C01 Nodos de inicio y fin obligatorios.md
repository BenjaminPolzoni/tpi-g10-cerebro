---
tags: [tpi, g10, sprint-3, historia, hu]
id: C01
tipo: HU
epica: "EP-S3-2"
capa: "Back + Front"
esfuerzo: M
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M03]
---

# C01: Nodos de inicio y fin obligatorios

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes|EP-S3-2]] · **HU** · Capa: **Back + Front** · Esfuerzo: **M** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como profesor quiero que el roadmap tenga siempre un nodo de inicio ("Bienvenidos") y uno de fin ("Felicitaciones"), y que no se pueda guardar sin ellos.

## Qué hay hoy

`NodeType` tiene `UNIT`, `CONTENT`, `THEORETICAL_CHALLENGE`, `PRACTICAL_CHALLENGE` y `EXAM`. No existen START ni END.

## Criterios de aceptación

- [ ] Tipos `START` y `END`. Un roadmap nuevo se crea con los dos.
- [ ] Al guardar: exactamente un START y un END, todos los nodos alcanzables desde START, y END alcanzable. Si no, error claro.
- [ ] Visual propio en el mapa 2D y en el mundo 3D ("empieza acá" y "terminaste").
- [ ] Al llegar a END se puede otorgar una insignia de fin de curso (HU-21).

## Depende de

- [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial|M03]] Módulo graph en Neo4j y migración inicial

## Dudas que la frenan

Ninguna.
