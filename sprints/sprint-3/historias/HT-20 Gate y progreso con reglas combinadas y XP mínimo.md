---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-20
estado: New
responsable: "Sin asignar"
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Must
en_taiga: true
ref: 8603
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8603
responsables_tareas: ["Fenoglio Santino", "Franco Maximiliano Amarilla"]
tareas_cerradas: "0/5"
---

# HT-20: Gate y progreso con reglas combinadas y XP mínimo

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **0/5** · Sprint: **G10 - Sprint 3**
> Cargada en Taiga: [[taiga/historias/HT-20 Gate y progreso con reglas combinadas y XP mínimo|HT-20]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8603)) · Épica en Taiga: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Fenoglio Santino|Fenoglio Santino]] (4), [[sprints/sprint-3/12-responsables#Franco Maximiliano Amarilla|Franco Maximiliano Amarilla]] (1).

[G10] — HT-20 — Gate y progreso con reglas combinadas y XP mínimo
-----------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: que el gate y el progreso evalúen las reglas combinadas y el XP mínimo con el mismo evaluador
*   **Para**: que el alumno vea bloqueado exactamente lo que el gate bloquea

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Un único evaluador para el gate y el recorrido (como hoy `block_reason`).
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): El P95 del gate no supera 200 ms con la caché de reglas.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El gate y el recorrido usan el mismo evaluador sobre el árbol de reglas.
*   [ ] **CA2**: El XP mínimo de sección se evalúa.
*   [ ] **CA3**: Tests BDD con el ejemplo de los profes (secciones 1 a 5).
*   [ ] **CA4**: Medición del P95 del gate.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Gate con reglas nuevas

**Escenario 1**  

*   **Dado**: el ejemplo de los profes
*   **Cuando**: un alumno completa las secciones 1 y 2
*   **Entonces**: se desbloquea la 3 y la 5 sigue bloqueada

**Escenario 2**  

*   **Dado**: la sección 4 con XP ≥ 500
*   **Cuando**: el alumno llega a 500 XP
*   **Entonces**: la 4 se desbloquea

**Escenario 3**  

*   **Dado**: una regla `A y (B o C)`
*   **Cuando**: el Motor consulta el gate
*   **Entonces**: responde igual que el recorrido

* * *

Prototipo
---------

*   **Capturas**: No aplica (sin pantalla).
*   **URL Figma**: No aplica.
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: No aplica.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 5
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 5 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: `GateEvaluator`, `GateService`, servicio de progreso.
*   Otros equipos / aprobaciones: G09 (el gate es su contrato).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Latencia; mitigación: caché de reglas.

## Tareas

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **0/5**. Historia en Taiga: [[taiga/historias/HT-20 Gate y progreso con reglas combinadas y XP mínimo|HT-20]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8603)

- [ ] [#9030](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9030) **T-20.1 Un solo evaluador de reglas para el gate y para lo que ve el alumno** · Back · New · [[sprints/sprint-3/12-responsables#Fenoglio Santino|Fenoglio Santino]]
    - **Qué:** `GateEvaluator` evalúa el árbol de reglas (AND/OR anidados, HU-59) y el progreso del alumno usa ese mismo resultado para el motivo de bloqueo.
    - **Dónde:** `GateEvaluator`, `GateService`, `NodeProgressService`.
    - **Listo cuando:** no queda lógica de desbloqueo duplicada y hay tests con reglas anidadas.
- [ ] [#9048](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9048) **T-20.2 Evaluar el XP mínimo** · Back · New · [[sprints/sprint-3/12-responsables#Fenoglio Santino|Fenoglio Santino]]
    - **Qué:** sumar al evaluador la condición de XP mínimo de las reglas (HU-58 y `requires` con XP), tomando el XP del alumno según cómo esté configurado el roadmap (por curso o por roadmap, P2).
    - **Listo cuando:** un alumno con menos XP que el mínimo ve el motivo y el gate lo rechaza. Hay test.
- [ ] [#9058](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9058) **T-20.3 Escenarios BDD con el ejemplo de los profes** · Back · New · [[sprints/sprint-3/12-responsables#Fenoglio Santino|Fenoglio Santino]]
    - **Qué:** escribir en Cucumber el ejemplo de las secciones 1 a 5 del pedido de los profes (`03-requerimientos-profes`) y hacerlo pasar.
    - **Listo cuando:** los escenarios pasan en el CI.
- [ ] [#9060](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9060) **T-20.4 Medir la latencia del gate** · Back · New · [[sprints/sprint-3/12-responsables#Fenoglio Santino|Fenoglio Santino]]
    - **Qué:** medir el P95 del gate con la caché de reglas (HT-18) sobre un roadmap de 150 nodos y dejar el resultado en el PR.
    - **Listo cuando:** el P95 es menor a 200 ms.
- [ ] [#9338](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9338) **T-20.5 Wiki, OpenAPI y diagrama de secuencia** · New · [[sprints/sprint-3/12-responsables#Franco Maximiliano Amarilla|Franco Maximiliano Amarilla]]
    - Tarea de documentación agregada en Taiga por el equipo; no estaba en la propuesta.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

`GateEvaluator` evalúa un modo AND/OR por sección o nodo, sin XP mínimo.

### Depende de

- [[sprints/sprint-3/historias/HU-58 Dependencias entre secciones|HU-58]] Dependencias entre secciones
- [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas|HU-59]] Dependencias entre nodos con reglas combinadas

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P7]] Sí hacen falta reglas combinadas, además de AND/OR + XP mínimo.
