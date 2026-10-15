---
tags: [tpi, g10, sprint-3, historia, hu]
id: M04
tipo: HU
epica: "EP-S3-1"
capa: "Back + Front"
esfuerzo: M
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M02]
---

# M04: Habilitar y gestionar varios roadmaps por curso

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HU** · Capa: **Back + Front** · Esfuerzo: **M** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como gestor o profesor quiero habilitar varios roadmaps en un curso y crearlos, renombrarlos y archivarlos.

## Qué hay hoy

Un curso tiene un único roadmap.

## Criterios de aceptación

- [ ] Flag por curso `multiple_roadmaps_allowed`, que solo cambia GESTOR o PROFESSOR dueño.
- [ ] Con el flag apagado, el curso no deja crear un segundo roadmap.
- [ ] Crear, renombrar y archivar roadmaps; archivar no borra el progreso.
- [ ] Pantalla en el front con la UI-KIT.

## Depende de

- [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps|M02]] Modelo 1 a N de curso a roadmaps

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P1]]
