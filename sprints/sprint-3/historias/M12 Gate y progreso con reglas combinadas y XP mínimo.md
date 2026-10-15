---
tags: [tpi, g10, sprint-3, historia, ht]
id: M12
tipo: HT
epica: "EP-S3-1"
capa: "Back"
esfuerzo: M
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M05, M06]
---

# M12: Gate y progreso con reglas combinadas y XP mínimo

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HT** · Capa: **Back** · Esfuerzo: **M** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como equipo quiero que el gate y el progreso evalúen las reglas nuevas igual que hoy evalúan AND/OR.

## Qué hay hoy

`GateEvaluator` evalúa un modo AND/OR por sección o nodo, sin XP mínimo.

## Criterios de aceptación

- [ ] El gate y el recorrido usan el mismo evaluador sobre el árbol de reglas.
- [ ] El XP mínimo de sección se evalúa.
- [ ] Tests BDD con el ejemplo de los profes (secciones 1 a 5).
- [ ] El tiempo del gate no empeora (caché de reglas).

## Depende de

- [[sprints/sprint-3/historias/M05 Dependencias entre secciones|M05]] Dependencias entre secciones
- [[sprints/sprint-3/historias/M06 Dependencias entre nodos con reglas combinadas|M06]] Dependencias entre nodos con reglas combinadas

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P7]]
