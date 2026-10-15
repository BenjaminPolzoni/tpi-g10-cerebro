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

*   [ ] Reglas de negocio: La ventana horaria del examen la publica Courses (P9), como las restricciones de HU-49: el nodo `EXAM` no tiene campos propios. Fuera de la ventana el gate responde `DATE_RESTRICTED`.
*   [ ] Validaciones: La ventana llega de Courses.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): El alumno ve en texto cuándo se habilita.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El nodo examen usa la ventana horaria que publica Courses.
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
*   Otros equipos / aprobaciones: G01 (publica la ventana, P9).
*   Impacto en datos / migraciones: Columnas o props de ventana.
*   Riesgos y mitigación (opcional): Zonas horarias; mitigación: guardar en UTC y mostrar en la del curso.

## Tareas

- [ ] **T-67.1 Aplicar al examen la ventana que publica Courses** · Back
    - **Qué:** la restricción de fecha que Courses publica para la actividad (`CourseRestrictionsClient`) se aplica al nodo `EXAM` correspondiente (P9: la ventana la define Courses).
    - **Listo cuando:** el examen toma la ventana de Courses sin datos propios en el nodo.
- [ ] **T-67.2 Bloquear el examen fuera de la ventana** · Back
    - **Qué:** el gate responde `DATE_RESTRICTED` antes y después de la ventana.
    - **Listo cuando:** hay tests con reloj simulado a las 17:59, 18:30 y 20:01.
- [ ] **T-67.3 Mostrarle al alumno cuándo se habilita** · Front
    - **Qué:** el nodo examen dice «Se habilita el {fecha} a las {hora}» en texto.
    - **Listo cuando:** se ve en el mapa y en el mundo.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

El gate evalúa `DATE_RESTRICTED` con ventanas que publica Courses (HU-49). El nodo no tiene ventana propia.

### Depende de

Nada: se puede empezar ya.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P9]] La ventana horaria la publica Courses.
