---
demo: true
tags: [neo4j-demo]
tipo_entidad: Section
id: "demo-section-001"
name: "Unidad 1: Fundamentos"
sortOrder: 1
visible: true
x: 120
y: 80
---

# Sección: Unidad 1

Sección de primer nivel del roadmap sintético.

## Relaciones salientes

- **HAS_SUBSECTION → [[Sección - Subunidad variables]]** — agrupa una subsección.
- **HAS_NODE → [[Nodo - Inicio]]** — contiene un nodo de inicio.
- **HAS_NODE → [[Nodo - Variables]]** — contiene un nodo de contenido.
- **HAS_NODE → [[Nodo - Quiz de variables]]** — contiene un desafío teórico.
- **HAS_NODE → [[Nodo - Quiz alternativo]]** — contiene un desafío teórico.
- **HAS_NODE → [[Nodo - Práctica integradora]]** — contiene un desafío práctico.
- **HAS_NODE → [[Nodo - Cierre]]** — contiene un nodo de fin.

## Relaciones entrantes

- **HAS_SECTION ← [[Roadmap - Programación inicial]]** — pertenece al roadmap.
