---
tags: [tpi, g10, exposicion, preguntas, roadmap, reglas]
fecha: 2026-11-08
autor: Benjamin Polzoni
---

# 1. Reglas de acceso de una sección

## Preguntas probables
- ¿Qué puede exigir una sección para abrirse?
- ¿Una sección puede depender de algo que está "más adelante"?
- ¿Cómo evitan que el alumno quede trabado para siempre (ciclos)?
- ¿Dónde se valida, en el front o en el back?

## Respuesta corta
Una sección (unidad o subsección) se abre cuando se cumple su **regla**: un árbol de grupos
**Todos (Y)** / **Cualquiera (O)** cuyas hojas son **secciones** o **nodos obligatorios**, y cada grupo
puede pedir además un **XP mínimo**. No importa el orden en el mapa: lo único prohibido es que la
regla **cierre un ciclo** (que para abrir algo haga falta algo que solo se abre después). Lo valida
el **back** siempre (es la red de seguridad) y el **front** lo anticipa para no dejar ni clickear lo
inválido.

## El modelo (por qué hay ciclo)
- Un **nodo** solo se puede completar con su **sección abierta** (entrar).
- **Completar** una sección = entrar y completar sus nodos obligatorios, también los de sus
  subsecciones.
- Una **subsección** solo se abre con su **sección padre** abierta.
- Sin regla, una sección **no** depende de la anterior: el orden del mapa no crea dependencias.

Hay ciclo si, siguiendo esas flechas desde lo que quiero exigir, llego otra vez a la sección que
estoy editando.

## Casos de uso (validados con el equipo)
Estructura: **A** Introducción (`A1`, `A2`, sin regla) · **B** BD I (`B1`, `B2`; regla: requiere A) ·
**C** BD II (`C1`, `C2` opcional; sin regla) · **D** BD III (`D1` requiere el nodo `B2`) ·
**B.1** subsección de B (`B1.1`).

| # | Edito | Quiero exigir | Resultado | Por qué |
|---|---|---|---|---|
| 1 | B | sección A | ✅ | Caso normal. |
| 2 | A | nodo A1 (de A) | ⛔ | A1 solo se abre con A abierta: misma sección. |
| 3 | A | sección B | ⛔ ciclo | B ya espera a A. |
| 4 | A | nodo B1 | ⛔ ciclo | B1 está en B, y B espera a A. |
| 5 | A | nodo C1 (más adelante) | ✅ | C no depende de A: no hay ciclo. El alumno entra a C, hace C1 y se abre A. |
| 6 | C | nodo A1 | ✅ | A no depende de C. |
| 7 | C (con el caso 5 guardado) | sección A | ⛔ ciclo | A ya espera a C1. |
| 8 | B | nodo D1 | ⛔ ciclo | D1 exige B2, que está en B (ciclo a través de una regla de nodo). |
| 9 | A | nodo C2 (opcional) | ⛔ | Un opcional se puede saltear: nunca es prerrequisito. |
| 10 | B.1 | sección B (su padre) | ⛔ | Una contiene a la otra: quedarían trabadas. |
| 11 | B.1 | nodo A2 | ✅ | A no depende de B.1. |
| 12 | B | solo XP ≥ 500 | ✅ | El XP nunca forma ciclos. |
| 13 | B | A **o** (C1 **y** XP ≥ 300) | ✅ | Grupos anidados; ninguna hoja cierra ciclo. |
| 14 | A | C1 **o** B1 | ⛔ B1 / ✅ C1 | B1 queda bloqueado (caso 4); la regla queda solo con C1. |

## Con qué valores trabaja el código

### Contrato (tpi-roadmap)
- `PUT` de reglas de sección (`GraphService.updateSectionRules`): `mode` (`AND`/`OR`),
  `prerequisite_section_ids` (forma plana, solo secciones) y `rule` (árbol).
- Árbol (`RuleDto`): `op` (`AND`/`OR`), `min_xp` (entero ≥ 0 o nulo), `operands`: grupos o hojas
  `{ element_id, element_type: SECTION | NODE }`.
- Un grupo sin operandos y con `min_xp` solo exige XP. Sin operandos ni `min_xp` se rechaza.
- Una regla vacía borra la regla (idempotente).

### Orden de validación en el back (`updateSectionRules`)
1. `RuleTreeValidator`: grupos vacíos, XP negativo.
2. `RuleLeafEligibility.requireEligibleForSection`: la hoja existe en el roadmap; si es nodo, tiene que
   ser obligatorio, no frontera, no de recuperación, y no estar en la misma sección ni en una
   subsección de ella.
3. `SubsectionGuard.requireNoContainment`: una sección no puede exigir a su padre ni a su hija.
4. `DependencyGraphService.assertNoCycle`: grafo único de nodos y secciones con pasos
   `ENTER`/`COMPLETE` (el modelo de arriba); si alguna hoja alcanza a la sección, 409.

### Errores y mensajes del back (`messages.properties`)
| Código | HTTP | Mensaje |
|---|---|---|
| `rule.empty-group` | 400 | Un grupo de la regla no tiene operandos ni XP mínimo: no exigiría nada. |
| `rule.min-xp-negative` | 400 | El XP mínimo no puede ser negativo (se recibió {0}). |
| `rule.optional-prerequisite` | 400 | El elemento {0} es opcional: puede tener reglas propias, pero no puede ser prerrequisito de otro elemento. |
| `rule.self-reference` | 400 | El elemento {0} no puede exigirse a sí mismo ni a un contenedor que lo incluye. |
| `node.boundary-no-prerequisites` | 400 | (nodo de inicio/fin de unidad que arma el sistema) |
| `section.prerequisite-containment` | 409 | La sección {1} no puede ser requisito de la sección {0}: una es subsección de la otra y quedarían trabadas. |
| `section.prerequisite-cycle` | 409 | La unidad {1} no puede ser requisito de la unidad {0}: cerraría un ciclo en el grafo. |

Los `{0}`/`{1}` son ids; el front traduce el código a su propio texto (`roadmapErrorMessage`).

### Front
- Misma lógica que el back en `src/app/features/roadmap/domain/prerequisite-policy.ts`
  (`prerequisitePolicy`): motivos `self`, `optional`, `boundary`, `recovery`, `containment`, `cycle`.
- Las filas inválidas del selector se muestran **deshabilitadas con su motivo**, así no se puede
  armar una regla que el back vaya a rechazar.
