---
tags: [tpi, g10, sprint-3, taiga, hu-59, hu-58, back]
fecha: 2026-10-19
estado: propuesta
autor: Santino Fenoglio
---

# 15 — Tarea nueva de back: exponer qué le falta al alumno

> [!info] Para qué sirve este documento
> Deja por escrito la tarea que falta para poder hacer **T-59.3** («Mostrarle al alumno qué le falta»), con el formato de la hoja Tareas listo para cargarla en Taiga, y el registro de lo que ya está hecho de HU-58, HU-59 y HT-20. Se carga como **tarea nueva dentro de HU-59**: no hay historia nueva.

## 1. Por qué hace falta

T-59.3 (front) pide «describir la regla en palabras («Requiere A y (B o C)») marcando lo que ya cumplió». Para eso el front necesita saber **qué le falta a ese alumno**. Hoy no hay forma de saberlo:

- El back **sí lo calcula**: `RuleEvaluator.evaluate` devuelve un `RuleGap` con lo que falta de cada grupo (los elementos no superados, los grupos hijos que no se cumplen y los XP que faltan para el mínimo). Tiene tests.
- Pero **ninguna API lo devuelve**. El avance del alumno (`NodeProgressView`) solo trae `block_reason`, un motivo de una palabra (`prerequisite_pending`, `unit_prerequisite_pending`…), sin decir qué falta. `GateEvaluator.unlockBlock` también descarta el hueco y devuelve solo el motivo.
- El front no lo puede reconstruir solo: no conoce, para cada hoja de la regla, si ese alumno la superó, ni el XP que le falta.

Cubre dos criterios: **HU-59 CA4** («el alumno ve qué le falta para desbloquear el nodo») y **HU-58 CA5** («el alumno ve por qué una sección está bloqueada»). La tarea T-58.4, de Lorenzo, que explica por qué una sección está bloqueada, usa lo mismo.

## 2. La tarea, en formato Taiga

### HU-59 · Dependencias entre nodos con reglas combinadas

#### T-59.5 Devolver en el avance del alumno qué le falta para desbloquear
- **Rol:** Backend · **Hs:** 6 (a confirmar) · **Responsable:** Fenoglio Santino · **Observadores:** a confirmar con la hoja Reparto
- **Qué:** que el avance del alumno traiga, para cada nodo bloqueado por una regla, **lo que le falta**: los elementos que no superó, cómo se combinan (`y` / `o`) y cuántos XP le faltan. Se calcula con el mismo evaluador que decide el gate (`RuleEvaluator`, que ya devuelve el `RuleGap`), así lo que se le muestra es exactamente lo que lo bloquea. Alcanza al bloqueo por la regla del nodo (`prerequisite_pending`) y por la regla de su unidad (`unit_prerequisite_pending`).
- **Por qué hace falta:** T-59.3 (front) no puede explicarle al alumno qué le falta mientras ninguna API devuelva ese dato. T-58.4 lo necesita para el motivo de bloqueo de las unidades.
- **Dónde:** `tpi-roadmap`: `GateEvaluator` (que hoy devuelve solo el motivo), `NodeProgressService` y `ProgressDtos.NodeProgressView`; el hueco sale de `RuleEvaluator` y `RuleGap`. Sin cambios de base de datos.
- **Listo cuando:** un alumno bloqueado por `A y (B o C)` que completó solo A recibe en su avance que le falta «B o C»; con una regla con XP mínimo recibe cuántos XP le faltan; un nodo habilitado o completado no trae el campo; y el gate responde igual que antes, con el mismo vocabulario de motivos.

##### Criterios de aceptación
- [ ] **CA1:** El avance (`GET …/students/{id}/progress`) trae, en cada nodo bloqueado por una regla, un campo opcional con lo que falta. Si el nodo no está bloqueado por una regla, el campo no viaja.
- [ ] **CA2:** El faltante respeta la estructura de la regla: cada grupo dice su operador (`AND` / `OR`), los elementos que faltan, los grupos hijos que no se cumplen y los XP que faltan.
- [ ] **CA3:** Distingue la regla del **nodo** de la regla de su **unidad**.
- [ ] **CA4:** No cambia el gate ni su vocabulario de motivos (acta v1.4, contrato con el Motor G09).
- [ ] **CA5:** Los nodos y secciones dados de baja no aparecen como faltantes; los XP salen del ámbito correcto, por curso o por roadmap.
- [ ] **CA6:** Documentado en el OpenAPI y en la wiki.

##### Propuesta de contrato (a cerrar al implementar)
Sobre `NodeProgressView`, sin tocar `block_reason`:

```json
{
  "node_id": "…",
  "block_reason": "prerequisite_pending",
  "missing": {
    "op": "AND",
    "missing_xp": 0,
    "missing_elements": [],
    "missing_groups": [
      { "op": "OR", "missing_xp": 0, "missing_elements": ["<B>", "<C>"], "missing_groups": [] }
    ]
  },
  "unit_missing": null
}
```

- `missing` es la regla del nodo y `unit_missing` la de su unidad; ambos son opcionales y no viajan si no aplican.
- Es el mismo `RuleGap` que ya existe, serializado en `snake_case`. Solo trae lo que **no** se cumple.

##### Preguntas abiertas
1. **Nombres o ids:** ¿alcanza con los ids de los elementos (el front los resuelve con el roadmap que ya tiene) o conviene mandar también el nombre? Ojo: el detalle de un nodo bloqueado va sin título (HU-05), así que no hay que filtrar por esta vía lo que esa regla oculta.
2. **Campo nuevo o endpoint nuevo:** esta propuesta agrega un campo opcional al avance (cambio aditivo). La alternativa es un endpoint aparte por nodo; costaría una llamada más del front por cada nodo bloqueado.
3. **Costo:** el faltante solo se calcula para nodos bloqueados por una regla y reusa el XP del ámbito que ya se lee una vez por consulta.

##### Pruebas que tiene que traer
Unitarias del evaluador con el hueco expuesto, de integración HTTP sobre el avance (regla `A y (B o C)` con distintos progresos, regla con XP mínimo, regla de unidad, hojas dadas de baja, nodo sin reglas, ámbito por curso y por roadmap) y un escenario BDD «le falta B o C».

## 3. Qué desbloquea

| Tarea | Capa | Quién | Qué cambia |
|---|---|---|---|
| **T-59.3** Mostrarle al alumno qué le falta | Front | Fenoglio Santino | Pasa de bloqueada a libre apenas esta tarea se mergee |
| **T-58.4** Explicarle al alumno por qué una sección está bloqueada | Front | Lorenzo Araujo | Usa `unit_missing` |

## 4. Registro de lo que ya está hecho (HU-58, HU-59, HT-20)

| Tarea | Qué entregó | PR | Estado |
|---|---|---|---|
| **T-59.1** Guardar reglas combinadas como árbol | Árbol AND/OR anidado: modelo, evaluador, validador, V28, `RuleTreeStore` y PATCH de nodo y unidad | [back #224](https://github.com/2026-P4-BE/tpi-roadmap/pull/224) | Mergeada 16/10 |
| **T-59.1** (lectura) | El árbol viaja en las lecturas del editor (`GET` de curso y de roadmap, nodos y secciones) | [back #238](https://github.com/2026-P4-BE/tpi-roadmap/pull/238) | Mergeada 16/10 |
| **T-20.1** Un solo evaluador del gate | `GateEvaluator.unlockBlock` es el único lugar que decide el desbloqueo: gate, avance, detalle, material y marcar como leído | [back #247](https://github.com/2026-P4-BE/tpi-roadmap/pull/247) | Mergeada 17/10 |
| **T-20.3** Escenarios BDD con el ejemplo de los profes | Escenarios Cucumber del ejemplo de las secciones 1 a 5 y de `A y (B o C)` | [back #248](https://github.com/2026-P4-BE/tpi-roadmap/pull/248) | Mergeada 17/10 |
| **T-59.2** Armar reglas combinadas en el editor | El asistente de reglas arma grupos AND/OR con un nivel de anidamiento | [front #691](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/691) | Mergeada 17/10 |
| **T-58.1** XP mínimo por sección y **T-20.2** evaluar el XP mínimo | El XP mínimo vuelve a las reglas (nodo y unidad), el gate lo evalúa con el XP del ámbito, el congelado lo respeta, se registra y publica el desbloqueo por XP y no se saca de la unidad a quien ya trabaja en ella | [back #268](https://github.com/2026-P4-BE/tpi-roadmap/pull/268) | Abierta; falta que Ludmila vuelva a revisar |

Lo que sigue pendiente de las tres historias: **T-20.4** (latencia del gate, espera la caché de reglas de Iker), **T-58.2** (subsecciones, espera la decisión D3 y el lector común), **T-58.3** (editor de unidad, front) y **T-59.3** (front, espera esta tarea).

## 5. Cómo cargarla en Taiga
1. Abrir la historia **HU-59** en el tablero del Sprint 3.
2. Crear una tarea con el título «T-59.5 Devolver en el avance del alumno qué le falta para desbloquear».
3. Pegar en la descripción las secciones **Qué**, **Por qué hace falta**, **Dónde** y **Listo cuando**, y los criterios de aceptación de arriba.
4. Responsable: Fenoglio Santino. Rol: Backend. Estimación: 6 h.
5. Taiga le asigna su número definitivo (`#id`); si no es T-59.5, ajustar el nombre en este documento.
6. Después de cargarla, enlazar T-59.3 y T-58.4 como dependientes de esta.
