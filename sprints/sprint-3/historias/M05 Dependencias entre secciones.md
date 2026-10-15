---
tags: [tpi, g10, sprint-3, historia, hu]
id: M05
tipo: HU
epica: "EP-S3-1"
capa: "Back + Front"
esfuerzo: M
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M02, M03]
---

# M05: Dependencias entre secciones

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HU** · Capa: **Back + Front** · Esfuerzo: **M** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como profesor quiero definir de qué secciones depende cada sección (AND/OR), con un XP mínimo opcional y un atajo para "todas las anteriores".

## Qué hay hoy

Ya existen las dependencias AND/OR entre secciones (V25). El XP mínimo por sección se borró en V8 (DEC-011).

## Criterios de aceptación

- [ ] El profesor elige las secciones requeridas y el modo AND/OR.
- [ ] Puede poner un XP mínimo opcional para la sección.
- [ ] "Todas las anteriores" selecciona de una vez todas las secciones previas.
- [ ] No se puede guardar un ciclo.
- [ ] El alumno ve por qué una sección está bloqueada.

## Depende de

- [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps|M02]] Modelo 1 a N de curso a roadmaps
- [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial|M03]] Módulo graph en Neo4j y migración inicial

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P6]]
