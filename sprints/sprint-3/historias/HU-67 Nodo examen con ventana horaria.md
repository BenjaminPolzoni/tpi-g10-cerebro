---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-67
estado: Propuesta
responsable: ""
epica: "Correcciones de los profes"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Must
en_taiga: false
---

# HU-67: Nodo examen con ventana horaria

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Correcciones de los profes|Correcciones de los profes]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HU-67 — Nodo examen con ventana horaria
-----------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: habilitar un nodo examen (parcial) solo dentro de una ventana horaria
*   **Para**: tomar parciales en el horario de la clase

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Campos `available_from` y `available_until` en nodos `EXAM`. Fuera de la ventana el gate responde `DATE_RESTRICTED`. Si Courses también define una ventana, gana lo que diga P9.
*   [ ] Validaciones: `available_from` < `available_until`.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): El alumno ve en texto cuándo se habilita.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Ventana horaria en nodos examen.
*   [ ] **CA2**: Fuera de la ventana el gate bloquea con `DATE_RESTRICTED`.
*   [ ] **CA3**: El alumno ve cuándo se habilita.
*   [ ] **CA4**: Tests con hora simulada.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Examen por hora

**Escenario 1**  

*   **Dado**: un examen habilitado de 18:00 a 20:00
*   **Cuando**: el alumno entra a las 17:59
*   **Entonces**: el gate responde `DATE_RESTRICTED`

**Escenario 2**  

*   **Dado**: el mismo examen
*   **Cuando**: el alumno entra a las 18:30
*   **Entonces**: puede rendir

**Escenario 3**  

*   **Dado**: el mismo examen
*   **Cuando**: el alumno lo mira antes de hora
*   **Entonces**: ve «se habilita a las 18:00»

* * *

Prototipo
---------

*   **Capturas**: Nodo examen bloqueado por hora.
*   **URL Figma**: Pendiente.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: PATCH /api/roadmap/nodes/{nodeId}/availability.

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

*   Servicios involucrados: Courses (si también define ventanas).
*   Módulos afectados: `GateEvaluator`, editor de nodo, mapa del alumno.
*   Otros equipos / aprobaciones: G01 (según P9).
*   Impacto en datos / migraciones: Columnas o props de ventana.
*   Riesgos y mitigación (opcional): Zonas horarias; mitigación: guardar en UTC y mostrar en la del curso.

## Tareas

- [ ] T-67.1 Ventana en el nodo
- [ ] T-67.2 Evaluación en el gate
- [ ] T-67.3 Front: aviso al alumno
- [ ] T-67.4 Tests con reloj simulado

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

El gate evalúa `DATE_RESTRICTED` con ventanas que publica Courses (HU-49). El nodo no tiene ventana propia.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P9]]
