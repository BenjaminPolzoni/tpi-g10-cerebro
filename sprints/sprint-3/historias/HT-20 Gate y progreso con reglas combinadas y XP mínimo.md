---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-20
estado: Propuesta
responsable: ""
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Must
en_taiga: false
---

# HT-20: Gate y progreso con reglas combinadas y XP mínimo

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

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

- [ ] **T-20.1 Un solo evaluador de reglas para el gate y para lo que ve el alumno** · Back
    - **Qué:** `GateEvaluator` evalúa el árbol de reglas (AND/OR anidados, HU-59) y el progreso del alumno usa ese mismo resultado para el motivo de bloqueo.
    - **Dónde:** `GateEvaluator`, `GateService`, `NodeProgressService`.
    - **Listo cuando:** no queda lógica de desbloqueo duplicada y hay tests con reglas anidadas.
- [ ] **T-20.2 Evaluar el XP mínimo** · Back
    - **Qué:** sumar al evaluador la condición de XP mínimo de las reglas (HU-58 y `requires` con XP), tomando el XP del alumno según cómo esté configurado el roadmap (por curso o por roadmap, P2).
    - **Listo cuando:** un alumno con menos XP que el mínimo ve el motivo y el gate lo rechaza. Hay test.
- [ ] **T-20.3 Escenarios BDD con el ejemplo de los profes** · Back
    - **Qué:** escribir en Cucumber el ejemplo de las secciones 1 a 5 del pedido de los profes (`03-requerimientos-profes`) y hacerlo pasar.
    - **Listo cuando:** los escenarios pasan en el CI.
- [ ] **T-20.4 Medir la latencia del gate** · Back
    - **Qué:** medir el P95 del gate con la caché de reglas (HT-18) sobre un roadmap de 150 nodos y dejar el resultado en el PR.
    - **Listo cuando:** el P95 es menor a 200 ms.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

`GateEvaluator` evalúa un modo AND/OR por sección o nodo, sin XP mínimo.

### Depende de

- [[sprints/sprint-3/historias/HU-58 Dependencias entre secciones|HU-58]] Dependencias entre secciones
- [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas|HU-59]] Dependencias entre nodos con reglas combinadas

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P7]] Sí hacen falta reglas combinadas, además de AND/OR + XP mínimo.
