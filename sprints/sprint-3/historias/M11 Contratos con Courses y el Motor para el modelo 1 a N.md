---
tags: [tpi, g10, sprint-3, historia, ht]
id: M11
tipo: HT
epica: "EP-S3-1"
capa: "Back"
esfuerzo: M
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M02]
---

# M11: Contratos con Courses y el Motor para el modelo 1 a N

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HT** · Capa: **Back** · Esfuerzo: **M** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como equipo quiero los contratos con Courses y el Motor adaptados a varios roadmaps por curso.

## Qué hay hoy

Cada sección del roadmap se sincroniza con una sección de Courses (HU-36). El Motor manda `id_course` + `id_node`.

## Criterios de aceptación

- [ ] Acordado con G01 cómo se mapean sus secciones con N roadmaps (P3, G4), registrado en [[acuerdos/courses-g01|acuerdos]].
- [ ] Confirmado con G09 que `node_id` alcanza (G8).
- [ ] Código y contratos (`docs/contracts/`) actualizados.

## Depende de

- [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps|M02]] Modelo 1 a N de curso a roadmaps

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P3]]
- [[sprints/sprint-3/08-dudas|G4]]
- [[sprints/sprint-3/08-dudas|G8]]
