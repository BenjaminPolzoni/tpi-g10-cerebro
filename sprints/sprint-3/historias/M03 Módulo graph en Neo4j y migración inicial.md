---
tags: [tpi, g10, sprint-3, historia, ht]
id: M03
tipo: HT
epica: "EP-S3-1"
capa: "Back"
esfuerzo: L
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M01]
---

# M03: Módulo graph en Neo4j y migración inicial

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HT** · Capa: **Back** · Esfuerzo: **L** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como equipo quiero la estructura del roadmap en Neo4j, con el estado del alumno en Postgres.

## Qué hay hoy

Todo está en Postgres (`section`, `node`, `section_prerequisite`, `node_prerequisite`).

## Criterios de aceptación

- [ ] Módulo `graph` dentro de roadmap-service con Spring Data Neo4j.
- [ ] Esquema versionado con `neo4j-migrations` (unicidad por `id`).
- [ ] Job de migración inicial desde Postgres, idempotente, detrás de un flag.
- [ ] UUID compartidos entre Neo4j y Postgres; solo baja lógica.
- [ ] Caché de reglas por roadmap para el gate, invalidada en cada edición.
- [ ] `GET /roadmaps/{id}/graph` devuelve `{nodes, edges, layout}`.

## Depende de

- [[sprints/sprint-3/historias/M01 Validar la infra de Neo4j y modelar las relaciones|M01]] Validar la infra de Neo4j y modelar las relaciones

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P1]]
- [[sprints/sprint-3/08-dudas|P4]]
- [[sprints/sprint-3/08-dudas|P8]]
