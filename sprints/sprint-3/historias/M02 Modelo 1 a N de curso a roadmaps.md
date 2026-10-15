---
tags: [tpi, g10, sprint-3, historia, ht]
id: M02
tipo: HT
epica: "EP-S3-1"
capa: "Back"
esfuerzo: L
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M01]
---

# M02: Modelo 1 a N de curso a roadmaps

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HT** · Capa: **Back** · Esfuerzo: **L** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como equipo quiero que un curso pueda tener varios roadmaps sin romper lo que ya funciona.

## Qué hay hoy

`roadmap.course_cohort_id` es UNIQUE (V1/V12) y todas las rutas son `/courses/{id}/...`. XP, vidas, nivel y ranking dependen de `student_course`, por curso.

## Criterios de aceptación

- [ ] Se quita el UNIQUE y se agrega `roadmap_id` en rutas y DTOs.
- [ ] Las rutas `/courses/{id}/...` siguen funcionando (apuntan al roadmap principal) mientras migra el front.
- [ ] XP, vidas, nivel y ranking quedan donde diga P2 (por curso o por roadmap).
- [ ] Los tests existentes pasan sin cambios de comportamiento.

## Depende de

- [[sprints/sprint-3/historias/M01 Validar la infra de Neo4j y modelar las relaciones|M01]] Validar la infra de Neo4j y modelar las relaciones

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P1]]
- [[sprints/sprint-3/08-dudas|P2]]
- [[sprints/sprint-3/08-dudas|P3]]
