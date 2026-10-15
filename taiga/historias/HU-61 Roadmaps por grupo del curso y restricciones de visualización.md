---
tags: [tpi, g10, taiga, hu]
codigo: HU-61
ref: 8611
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8611
---

# HU-61: Roadmaps por grupo del curso y restricciones de visualización

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8611) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Tareas cerradas: **0/4**

[G10] — HU-61 — Roadmaps por grupo del curso y restricciones de visualización
-----------------------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: asignar un roadmap distinto a cada grupo o división del curso
*   **Para**: que cada alumno vea solo el recorrido que le corresponde a su grupo

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Un curso puede tener varios roadmaps; cada uno se asigna a uno o más grupos o divisiones del curso (comisiones u otras que tenga el curso), o a todos. Lo oculto y lo bloqueado que define Courses (también para un roadmap entero) lo aplica HU-49; el selector de comisión dentro de un roadmap es HT-33 (HU-44). Elegir qué recorrer entre los roadmaps visibles ya está implementado.
*   [ ] Validaciones: Un grupo que no existe en el curso se rechaza. Un roadmap sin grupos asignados no lo ve ningún alumno, salvo que esté marcado para todos.
*   [ ] Datos obligatorios: Roadmap y al menos un grupo, o la marca «todos».
*   [ ] Performance (tiempos, volumen, límites): La resolución de grupos del alumno se cachea igual que hoy (`GroupAccessService`).
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño del curso asignan. Un alumno no puede abrir por URL un roadmap de otro grupo (403).
*   [ ] Accesibilidad (WCAG/teclado/lectores): La asignación de grupos y la lista de roadmaps del alumno se usan con teclado y lector de pantalla.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor asigna un roadmap a uno o más grupos del curso, o a todos.
*   [ ] **CA2**: Un alumno solo ve los roadmaps asignados a sus grupos.
*   [ ] **CA3**: Un roadmap marcado para todos lo ven todos los alumnos del curso.
*   [ ] **CA4**: Un alumno que entra por URL a un roadmap de otro grupo recibe 403.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Roadmaps por grupo del curso

**Escenario 1**

*   **Dado**: un curso con el roadmap A asignado al grupo 2W1 y el B al 2W2
*   **Cuando**: un alumno de 2W1 abre el curso
*   **Entonces**: ve solo el roadmap A

**Escenario 2**

*   **Dado**: el roadmap C marcado para todos
*   **Cuando**: un alumno de 2W2 abre el curso
*   **Entonces**: ve los roadmaps B y C

**Escenario 3**

*   **Dado**: un alumno de 2W1
*   **Cuando**: entra por URL al roadmap B
*   **Entonces**: recibe 403

* * *

Prototipo
---------

*   **Capturas**: Asignación de grupos en el editor del profesor; lista de roadmaps del alumno.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-select` (multi) para los grupos.
*   **Mock API / Swagger**: PUT /api/roadmap/roadmaps/{roadmapId}/groups; GET /api/roadmap/courses/{courseId}/roadmaps.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 5
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 5 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Courses (grupos del curso y restricciones de visualización).
*   Módulos afectados: Asignación de roadmaps, `GroupAccessService`, roadmap del alumno, editor del profesor.
*   Otros equipos / aprobaciones: G01 (grupos y restricciones que publica Courses).
*   Impacto en datos / migraciones: Tabla roadmap ↔ grupo.
*   Riesgos y mitigación (opcional): Ninguno abierto: el límite con HU-44/HT-33 (comisión dentro del roadmap) y HU-49 (oculto y bloqueado) quedó definido el 2026-10-15.


## Tareas

- [ ] #9161 T-61.1 Asignar un roadmap a grupos del curso · New · Stefano Zoffoli
- [ ] #9162 T-61.2 Que el alumno vea solo los roadmaps de sus grupos · New · Stefano Zoffoli
- [ ] #9164 T-61.3 Asignación de grupos en la pantalla del profesor · New · Stefano Zoffoli
- [ ] #9350 T-61.4 Wiki, OpenAPI y diagrama de secuencia · New · Franco Maximiliano Amarilla
