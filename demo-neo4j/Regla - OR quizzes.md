---
demo: true
tags: [neo4j-demo]
tipo_entidad: Rule
id: "demo-rule-practice-or"
op: OR
minXp: null
---

# Regla: OR quizzes

Grupo anidado: basta cumplir uno de sus operandos. Es una regla ficticia para ilustrar la expresión `A AND (B OR C)`.

## Relaciones salientes

- **HAS_OPERAND → [[Nodo - Quiz de variables]]** — primera alternativa del grupo OR.
- **HAS_OPERAND → [[Nodo - Quiz alternativo]]** — segunda alternativa del grupo OR.

## Relaciones entrantes

- **HAS_OPERAND ← [[Regla - AND práctica]]** — grupo OR anidado dentro del AND.
