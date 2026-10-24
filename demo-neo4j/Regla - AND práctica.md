---
demo: true
tags: [neo4j-demo]
tipo_entidad: Rule
id: "demo-rule-practice-and"
op: AND
minXp: 100
---

# Regla: AND práctica

Grupo raíz de la regla de desbloqueo de [[Nodo - Práctica integradora]]. Requiere 100 XP y que se cumplan todos sus operandos.

## Relaciones salientes

- **HAS_OPERAND → [[Nodo - Variables]]** — requisito hoja: completar el contenido.
- **HAS_OPERAND → [[Regla - OR quizzes]]** — grupo anidado que aporta una alternativa.

## Relaciones entrantes

- **UNLOCKED_BY ← [[Nodo - Práctica integradora]]** — esta regla controla su desbloqueo.
