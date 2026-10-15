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

- [ ] T-20.1 Evaluador sobre árbol de reglas
- [ ] T-20.2 XP mínimo
- [ ] T-20.3 BDD del ejemplo de los profes
- [ ] T-20.4 Medir el P95

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

`GateEvaluator` evalúa un modo AND/OR por sección o nodo, sin XP mínimo.

### Depende de

- [[sprints/sprint-3/historias/HU-58 Dependencias entre secciones|HU-58]] Dependencias entre secciones
- [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas|HU-59]] Dependencias entre nodos con reglas combinadas

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P7]]
