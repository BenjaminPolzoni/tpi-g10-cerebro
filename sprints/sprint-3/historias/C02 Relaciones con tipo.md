---
tags: [tpi, g10, sprint-3, historia, hu]
id: C02
tipo: HU
epica: "EP-S3-2"
capa: "Back + Front"
esfuerzo: L
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M03]
---

# C02: Relaciones con tipo

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes|EP-S3-2]] · **HU** · Capa: **Back + Front** · Esfuerzo: **L** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como profesor quiero relacionar nodos y unidades con tipos de relación (4 niveles), ver su nombre y elegir cuáles se muestran.

## Qué hay hoy

Solo existe la relación "prerrequisito" con modo AND/OR.

## Criterios de aceptación

- [ ] Catálogo de tipos de relación: `REQUIRES`, `BELONGS_TO`, `RELATED_TO` y el cuarto que definan los profes (P4).
- [ ] Cada tipo tiene nombre visible y se puede configurar si se muestra.
- [ ] La arista muestra el nombre del tipo.
- [ ] Solo `REQUIRES` afecta el desbloqueo.

## Depende de

- [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial|M03]] Módulo graph en Neo4j y migración inicial

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P4]]
