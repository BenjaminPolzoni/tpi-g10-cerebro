---
demo: true
tags: [neo4j-demo]
tipo_entidad: Node
id: "demo-node-practice-001"
type: PRACTICAL_CHALLENGE
name: "Práctica integradora"
sortOrder: 4
mandatory: true
available: true
---

# Nodo: Práctica integradora

Ejercicio ficticio cuya regla es `Variables AND (Quiz de variables OR Quiz alternativo)`.

## Relaciones salientes

- **UNLOCKED_BY → [[Regla - AND práctica]]** — la regla define qué requisitos habilitan este nodo.

## Relaciones entrantes

- **HAS_NODE ← [[Sección - Unidad 1]]** — ubicado dentro de la sección.
- **RECOMMENDS ← [[Nodo - Quiz de variables]]** — sugerencia informativa, independiente de `UNLOCKED_BY`.
