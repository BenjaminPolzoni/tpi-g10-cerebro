---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-49
estado: Propuesta
responsable: ""
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Should
en_taiga: true
---

# HU-49: Aplicar en el roadmap las restricciones de sección y actividad que publica Courses

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Ya existe en Taiga: [[taiga/historias/HU-49 Aplicar en el roadmap las restricciones de sección y actividad que publica Courses|HU-49]] (épica EP-4230). En el Sprint 3 se **reabre** con lo que falta.

[G10] — HU-49 — Aplicar en el roadmap las restricciones de sección y actividad que publica Courses
--------------------------------------------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: saber por qué un nodo está oculto o bloqueado por fecha, y que se actualice cuando Courses cambia la restricción
*   **Para**: no perderme una actividad habilitada ni intentar una que todavía no lo está

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Courses publica restricciones por sección y actividad. HIDDEN: el alumno no ve el nodo. LOCKED: lo ve bloqueado con la fecha. El gate ya evalúa `DATE_RESTRICTED`.
*   [ ] Validaciones: Si llega un evento de cambio, se invalida la caché de restricciones del curso.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): La fecha de habilitación en texto, no solo con un ícono.
*   [ ] Otros: Depende de G01 (evento de cambio). La ventana horaria de los exámenes también la publica Courses (P9). Con N roadmaps, el profesor define las restricciones de cada roadmap y se copian al clonarlo (G4). E3: puede que ya esté hecha; corroborarlo antes de empezar.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Un nodo HIDDEN no aparece al alumno.
*   [ ] **CA2**: Un nodo LOCKED aparece bloqueado con su fecha de habilitación.
*   [ ] **CA3**: Al llegar el evento de cambio de Courses, el estado se actualiza.
*   [ ] **CA4**: El front muestra el aviso con la fecha.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Restricciones de Courses

**Escenario 1**  

*   **Dado**: un nodo con restricción HIDDEN
*   **Cuando**: el alumno abre el roadmap
*   **Entonces**: no lo ve

**Escenario 2**  

*   **Dado**: un nodo LOCKED hasta el 20/10
*   **Cuando**: el alumno lo abre el 18/10
*   **Entonces**: lo ve bloqueado con «se habilita el 20/10»

**Escenario 3**  

*   **Dado**: Courses cambia la fecha de un nodo
*   **Cuando**: llega el evento
*   **Entonces**: el roadmap muestra la fecha nueva

* * *

Prototipo
---------

*   **Capturas**: Nodo bloqueado por fecha en el mapa.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-badge` para el estado.
*   **Mock API / Swagger**: Restricciones de Courses (`course.restrictions.read`) y evento de cambio a acordar.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 8 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Courses (restricciones y evento).
*   Módulos afectados: `CourseRestrictionsClient`, `GateEvaluator`, mapa del alumno.
*   Otros equipos / aprobaciones: G01 (bloqueante para el evento).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que G01 no publique el evento a tiempo; mitigación: leer por pull con caché corta.

## Tareas

- [ ] T-49.9 HIDDEN vs LOCKED en el back
- [ ] T-49.10 Consumir el evento de cambio de restricción
- [ ] T-49.11 Front: oculto, bloqueado y aviso con fecha
- [ ] T-49.12 Tests y acta con G01

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

El gate aplica la restricción por fecha. Falta distinguir oculto (HIDDEN) de bloqueado (LOCKED), consumir el evento de cambio y avisar. El front no tiene nada. Depende de G01.

### Depende de

- [[sprints/sprint-3/historias/HU-67 Nodo examen con ventana horaria|HU-67]] Nodo examen con ventana horaria

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P9]] La ventana horaria la publica Courses.
- ✅ [[sprints/sprint-3/08-dudas|G4]] Restricciones por roadmap, definidas por el profesor; se copian al clonar.
- ✅ [[sprints/sprint-3/08-dudas|E3]] Ya debería estar hecho: corroborarlo.
