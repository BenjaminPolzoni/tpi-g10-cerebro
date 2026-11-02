---
tags: [tpi, g10, sprint-4, plan, back, roadmap, gate, unidades, prerrequisitos]
fecha: 2026-11-02
autor: Benjamin Polzoni
estado: borrador
repo: 2026-P4-BE/tpi-roadmap
base: origin/develop 15ac3721 (2026-11-02)
worktree: ~/orca/workspaces/tpi-roadmap/gate-cross-unit-node-entry (rama feature/gate-cross-unit-node-entry)
antecedentes: DEC-010, HU-58 (T-58.1, T-58.2), HU-13 CA4, contrato roadmap-motor-gate-v1 (unit_prerequisite_pending)
---

# Back · Entrar a una isla bloqueada solo para hacer el nodo que desbloquea otra unidad

> [!info] Alcance
> Si un nodo de la unidad 1 desbloquea un nodo de la unidad 2, y ese nodo **no tiene otra dependencia**, el alumno tiene que poder entrar a la isla 2 **solo para hacer ese nodo**, aunque la unidad 2 siga bloqueada por requisito de unidad o por XP. Todo es back (`GateEvaluator`); el front ya muestra lo que el back devuelve. Es una propuesta. Todavía no hay código.

## 1. Qué hay hoy (verificado en `origin/develop`)

- **La unidad manda sobre el nodo.** `GateEvaluator.evaluate` y `unlockBlock` evalúan primero `SectionPrerequisiteService.isSatisfied(sección)` y recién después `PrerequisiteService.isSatisfied(nodo)`. Si la unidad está bloqueada, el nodo sale `LOCKED` con `UNIT_PREREQUISITE_PENDING` aunque su propio prerrequisito (un nodo de otra unidad) esté cumplido.
- **Quién usa esa decisión** (todos pasan por los mismos dos métodos, así que un solo cambio los cubre): `GateService.evaluate` (Motor), `NodeProgressService.viewOf` (mapa del alumno), `NodeDetailService` (detalle), `UnitMaterialService` (material) y `ProgressService.requireUnlocked` (marcar lectura).
- **Regla de unidad** (`SectionPrerequisiteService.gapOf`), en este orden: (1) si el alumno ya superó **algún** nodo de la unidad, devuelve «no falta nada» **sin mirar XP ni requisitos**; (2) si es zona, exige poder entrar al padre; (3) evalúa el árbol de la unidad (hojas de unidad + `minXp`). Es un `minXp` más del grupo (`RuleEvaluator`).
- **Regla de nodo** (`PrerequisiteService.treeGap`): árbol AND/OR de hojas. Una hoja de nodo se cumple si el alumno lo superó (`completed_node`); una hoja de sección, si la unidad está completa (`isComplete`). El árbol del nodo también puede llevar `minXp`. No revierte desbloqueos ya alcanzados (`node_unlock`, HU-13 CA4).
- **XP del alumno** para ambas reglas: `RuleXpService` → `XpScopeService` (`total_xp` del curso, o el propio del roadmap si está en modo ROADMAP).

## 2. Qué cambia

Nueva excepción, aplicada **solo al nodo**, no a la unidad:

> Un nodo N de la unidad U se evalúa sin la regla de U si **su regla propia** es exactamente **una hoja de nodo** (sin `minXp`, sin otras hojas, sin grupos anidados) y esa hoja es un nodo **de otra unidad** que el alumno ya superó.

Con eso:
- N queda `ENABLED`; el resto de los nodos de U siguen `LOCKED` por `UNIT_PREREQUISITE_PENDING` (o por XP).
- Siguen aplicando, sin cambios: archivado, matrícula, ventana de fechas, comisión (`GROUP_RESTRICTED` / `DATE_RESTRICTED`), vidas y nodo no disponible.
- Si N es de una zona, se saltea también la regla del padre (misma excepción, mismo criterio).

## 3. Decisiones

| # | Decisión | Propuesta | Estado |
|---|---|---|---|
| D1 | Hoja única o también OR con varias hojas | Solo **hoja única**. Con OR de varias hojas cumplidas no se salta la unidad. | pendiente de confirmar |
| D2 | Zona dentro de una unidad bloqueada | Se saltea también la regla del **padre** para ese nodo. | pendiente de confirmar |
| D3 | Dónde vive la lógica | En `GateEvaluator` (único lugar, ya compartido). `PrerequisiteService` expone la pregunta «¿la regla del nodo es una hoja de nodo de otra unidad?»; no se duplica en cada llamador. | propuesta |
| D4 | Hoja de nodo dado de baja | No cuenta como hoja única (la regla podada queda vacía y se cumple sola). Tratarlo como «sin excepción» y que decida la regla de la unidad. | propuesta |
| D5 | Contrato del Motor | No cambia el vocabulario: el nodo pasa de `unit_prerequisite_pending` a elegible. Es aditivo desde el punto de vista del contrato; avisar a G09 igual. | propuesta |

## 4. Pasos

1. `PrerequisiteService`: método `Optional<UUID> soleCrossUnitNodeLeaf(UUID nodeId)` (o booleano) que lea el árbol del nodo con `RuleReads` (caché) y devuelva la hoja si cumple la forma de §2.
2. `GateEvaluator`: en `evaluate`, `unlockBlock` y `evaluateForReading` (que usa `unlockBlock`), antes de consultar `sectionPrerequisites`, saltear la regla de la unidad cuando la excepción aplica **y** `prerequisites.isSatisfied(nodo)` es verdadero. Mantener el orden de motivos para el resto.
3. `missingOf`: si el motivo es `UNIT_PREREQUISITE_PENDING` en un nodo con la excepción pero cuyo prerrequisito aún no se cumple, el faltante correcto es el del **nodo** (`PREREQUISITE_PENDING`), no el de la unidad. Hoy el alumno vería «te falta la unidad X» cuando en realidad le falta el nodo.
4. Tests (solo los pertinentes, ver [[tests-solo-pertinentes]]): `SubsectionRuleGateTest`, `GateOutcomesContract`, `GateRoadmapFixtureTest`, `UnlockRuleServiceTest`. Casos nuevos: nodo con hoja única superada en unidad bloqueada por requisito → elegible; lo mismo bloqueada por XP; hermano del nodo en la misma unidad → sigue bloqueado; hoja no superada → `PREREQUISITE_PENDING`; OR de dos hojas → sin excepción; nodo con `minXp` propio → sin excepción; zona bajo padre bloqueado.
5. Verificar con Neo4j: `RULE_CACHE_ENABLED` / `GRAPH_READ_ENABLED` encendidos y apagados (el árbol del nodo llega por `RuleReads` en ambos).

## 5. Qué revisar contra lo que ya está en el cerebro

| Documento | Qué dice hoy | Qué hay que contrastar o actualizar |
|---|---|---|
| `decisiones/DEC-010-prerrequisitos-por-seccion-v25` | La unidad exige completar otras unidades **antes de entrar**. | La excepción contradice «antes de entrar» para un nodo puntual. Anotar consecuencia o abrir DEC nueva. |
| `sprints/sprint-3/historias/HU-58 Dependencias entre secciones` | XP mínimo por sección; ejemplo «sección 4 con XP ≥ 500, sigue bloqueada y ve "te faltan 200 XP"». | Ese ejemplo deja de valer para el nodo con la excepción. Ver T-58.1, T-58.2 (zonas dentro de la unidad) y T-58.4 (explicar el bloqueo al alumno). |
| `contratos/roadmap-motor-gate-v1` §4/§5 | `unit_prerequisite_pending` cuando la unidad no se cumple. | Aclarar que el motivo no se emite para un nodo con la excepción. |
| `arquitectura/estructura-codigo.md` (`PrerequisiteService`, tests de retroactividad) | Nodo: AND/OR sobre `completed_node`, `node_unlock` no revierte. | Sumar la nueva pregunta del servicio y el orden de evaluación del gate. |
| `terminado/Fix Front - orden de nodos y restricciones` | «El orden entre unidades es una regla de las unidades, no de los nodos.» | Esto lo cambia en el back; el front no poda nada, pero la frase queda desactualizada. |
| `sprints/sprint-4/Planes/Benja/Back - copia y lectura de reglas del gate desde Neo4j` | El gate leerá reglas crudas de Neo4j. | La excepción lee el árbol del nodo por `RuleReads`; no depende de ese plan pero conviene probar con el flag encendido. |

## 6. Hallazgo relacionado (no incluido en este plan)

`SectionPrerequisiteService.gapOf` devuelve «no falta nada» a quien ya superó **un** nodo de la unidad, **antes** de mirar el XP. Es la causa más probable del caso «300 XP entra a una unidad que pide 400». Con esta excepción cobra más importancia: un nodo superado por el camino nuevo abre la unidad entera por esa regla. Decidir si «ya estaba adentro» sigue siendo intencional o se acota (por ejemplo, solo cuenta si el nodo se superó antes de que existiera la regla).

## 7. Riesgos

- **Entrada por la puerta de atrás:** completar ese único nodo habilita, por el atajo de §6, el resto de la unidad. Resolver §6 antes o junto con este cambio.
- **Reglas editadas después:** el desbloqueo ya alcanzado no se revierte (HU-13 CA4); sin cambios.
- **Comisión y fechas** siguen bloqueando: el alumno puede ver «entra a la isla» en el mapa y aun así recibir `GROUP_RESTRICTED`.
