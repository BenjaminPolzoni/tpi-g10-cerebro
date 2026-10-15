---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-61
estado: Propuesta
responsable: ""
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Should
en_taiga: false
---

# HU-61: Roadmaps por grupo del curso y restricciones de visualización

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HU-61 — Roadmaps por grupo del curso y restricciones de visualización
-----------------------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: asignar un roadmap distinto a cada grupo o división del curso y que se respeten las restricciones de visualización que el curso define para sus alumnos
*   **Para**: que cada alumno vea solo el recorrido que le corresponde a su grupo

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Un curso puede tener varios roadmaps; cada uno se asigna a uno o más grupos o divisiones del curso (comisiones u otras que tenga el curso), o a todos. Las restricciones de visualización (oculto, visible pero bloqueado, por fecha) las define el curso y Roadmap solo las aplica. Elegir qué recorrer entre los roadmaps visibles ya está implementado.
*   [ ] Validaciones: Un grupo que no existe en el curso se rechaza. Un roadmap sin grupos asignados no lo ve ningún alumno, salvo que esté marcado para todos.
*   [ ] Datos obligatorios: Roadmap y al menos un grupo, o la marca «todos».
*   [ ] Performance (tiempos, volumen, límites): La resolución de grupos del alumno se cachea igual que hoy (`GroupAccessService`).
*   [ ] Seguridad (roles, permisos, datos sensibles): Solo el profesor dueño del curso asigna. Un alumno no puede abrir por URL un roadmap de otro grupo (403).
*   [ ] Accesibilidad (WCAG/teclado/lectores): El aviso de bloqueo se lee con lector de pantalla.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor asigna un roadmap a uno o más grupos del curso, o a todos.
*   [ ] **CA2**: Un alumno solo ve los roadmaps asignados a sus grupos.
*   [ ] **CA3**: Un roadmap o una sección que el curso marca como oculta no aparece para ese alumno.
*   [ ] **CA4**: Lo que el curso marca como visible pero bloqueado aparece bloqueado, con el motivo y la fecha si la hay.
*   [ ] **CA5**: Un alumno que entra por URL a un roadmap de otro grupo recibe 403.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Roadmaps por grupo del curso

**Escenario 1**  

*   **Dado**: un curso con el roadmap A asignado al grupo 2W1 y el B al 2W2
*   **Cuando**: un alumno de 2W1 abre el curso
*   **Entonces**: ve solo el roadmap A

**Escenario 2**  

*   **Dado**: una sección que el curso marca como oculta para 2W1
*   **Cuando**: un alumno de 2W1 abre el roadmap
*   **Entonces**: la sección no aparece

**Escenario 3**  

*   **Dado**: un alumno de 2W1
*   **Cuando**: entra por URL al roadmap B
*   **Entonces**: recibe 403

* * *

Prototipo
---------

*   **Capturas**: Asignación de grupos en el editor del profesor; vista del alumno con lo bloqueado.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-select` (multi) para los grupos.
*   **Mock API / Swagger**: PUT /api/roadmap/roadmaps/{roadmapId}/groups; GET /api/roadmap/courses/{courseId}/roadmaps.

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

*   Servicios involucrados: Courses (grupos del curso y restricciones de visualización).
*   Módulos afectados: Asignación de roadmaps, `GroupAccessService`, roadmap del alumno, editor del profesor.
*   Otros equipos / aprobaciones: G01 (grupos y restricciones que publica Courses).
*   Impacto en datos / migraciones: Tabla roadmap ↔ grupo.
*   Riesgos y mitigación (opcional): Se superpone con HU-44 (comisiones) y HU-49 (restricciones de Courses); acordar el límite entre las tres antes de arrancar.

## Tareas

- [ ] T-61.1 Asignación de roadmap a grupos (modelo y endpoint)
- [ ] T-61.2 Filtrar los roadmaps visibles por los grupos del alumno
- [ ] T-61.3 Aplicar las restricciones de visualización del curso (oculto, bloqueado)
- [ ] T-61.4 Asignación en el editor del profesor y vista del alumno
- [ ] T-61.5 Tests

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Según el equipo, la versión anterior de esta HU («El alumno elige qué roadmap recorrer») ya está implementada. Hay filtrado por comisión detrás de `ROADMAP_BY_GROUP_ENABLED` (`GroupAccessService`, `GroupSelectionService`, HU-44) y el gate aplica la restricción por fecha (HU-49). Falta asignar roadmaps distintos por grupo y aplicar oculto y bloqueado.

### Depende de

- [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps|HT-17]] Modelo 1 a N de curso a roadmaps
- [[sprints/sprint-3/historias/HU-49 Aplicar en el roadmap las restricciones de sección y actividad que publica Courses|HU-49]] Aplicar en el roadmap las restricciones de sección y actividad que publica Courses

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P1]] Cada roadmap es un mapa distinto del mismo curso: puede armarse por grupos del curso.
- ✅ [[sprints/sprint-3/08-dudas|P5]] Lo configura el profesor: todos los roadmaps o por comisión.
