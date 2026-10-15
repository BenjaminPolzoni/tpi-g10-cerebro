---
tags: [tpi, g10, sprint-3, historia, spike]
id: M01
tipo: Spike
epica: "EP-S3-1"
capa: "Back + Infra"
esfuerzo: S
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# M01: Validar la infra de Neo4j y modelar las relaciones

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **Spike** · Capa: **Back + Infra** · Esfuerzo: **S** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como equipo quiero confirmar que Neo4j corre en la plataforma y tener el modelo de relaciones antes de migrar.

## Qué hay hoy

Neo4j está decidido (DEC-016) pero no existe en el compose ni en la mesh.

## Criterios de aceptación

- [ ] Neo4j Community levantado en el compose local con volumen.
- [ ] Acordado con plataforma quién lo suma a la mesh y a la demo (G1).
- [ ] Prueba de concepto: Spring Data Neo4j + Testcontainers corriendo en el CI.
- [ ] Modelo de nodos y relaciones (incluye START/END y tipos de relación) escrito en [[sprints/sprint-3/04-base-de-grafos|04]].

## Depende de

Nada: se puede empezar ya.

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G1]]
- [[sprints/sprint-3/08-dudas|P1]]
- [[sprints/sprint-3/08-dudas|P4]]
