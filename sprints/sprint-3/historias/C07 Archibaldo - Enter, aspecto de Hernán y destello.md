---
tags: [tpi, g10, sprint-3, historia, hu]
id: C07
tipo: HU
epica: "EP-S3-2"
capa: "Front (3D)"
esfuerzo: M
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# C07: Archibaldo: Enter, aspecto de Hernán y destello

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes|EP-S3-2]] · **HU** · Capa: **Front (3D)** · Esfuerzo: **M** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como alumno quiero hablar con Archibaldo con Enter, que tenga el aspecto de Hernán y que un destello me guíe por el camino.

## Qué hay hoy

El NPC usa la skin del capitán pirata del kit (`world-3d.service.ts:3109`). El diálogo se abre con clic. No hay destello.

## Criterios de aceptación

- [ ] Con el NPC en rango, Enter abre el diálogo; el foco queda en el diálogo (`generic-modal`).
- [ ] Modelo o skin de Hernán.
- [ ] Destello sobre el camino al próximo nodo disponible.

## Depende de

Nada: se puede empezar ya.

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P11]]
