---
tags: [tpi, g10, taiga, hu]
codigo: HU-49
ref: 7211
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-4230 Unidades del roadmap sincronizadas con Courses|EP-4230]], [[epicas/EP-8632 Deuda del Sprint 2|EP-8632]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7211
---

# HU-49: Aplicar en el roadmap las restricciones de sección y actividad que publica Courses

> [!info] Generado desde Taiga (2026-10-15 16:54). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7211) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-4230 Unidades del roadmap sincronizadas con Courses|EP-4230]], [[epicas/EP-8632 Deuda del Sprint 2|EP-8632]] · Tareas cerradas: **0/6**

[G10] — HU-49 — Aplicar en el roadmap las restricciones de sección y actividad que publica Courses
--------------------------------------------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: saber por qué un nodo, una sección o un roadmap está oculto o bloqueado por fecha (incluida la ventana horaria de los exámenes), y que se actualice cuando Courses cambia la restricción
*   **Para**: no perderme una actividad habilitada ni intentar una que todavía no lo está

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Courses publica restricciones por sección y actividad. HIDDEN: el alumno no ve el nodo. LOCKED: lo ve bloqueado con la fecha. El gate ya evalúa `DATE_RESTRICTED`. La ventana horaria de un nodo `EXAM` es una restricción de fecha más que publica Courses (P9): el nodo no tiene campos propios. Lo oculto y lo bloqueado se aplica también a un roadmap entero.
*   [ ] Validaciones: Si llega un evento de cambio, se invalida la caché de restricciones del curso. Las fechas se guardan en UTC y se muestran en la zona horaria del curso.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): La fecha de habilitación en texto, no solo con un ícono.
*   [ ] Otros: Depende de G01 (evento de cambio). Con N roadmaps, el profesor define las restricciones de cada roadmap y se copian al clonarlo (G4). E3: puede que ya esté hecha; corroborarlo antes de empezar.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Un nodo HIDDEN no aparece al alumno.
*   [ ] **CA2**: Un nodo LOCKED aparece bloqueado con su fecha de habilitación.
*   [ ] **CA3**: Al llegar el evento de cambio de Courses, el estado se actualiza.
*   [ ] **CA4**: El front muestra el aviso con la fecha.
*   [ ] **CA5**: Un nodo examen fuera de su ventana horaria responde `DATE_RESTRICTED` y muestra «Se habilita el {fecha} a las {hora}», con tests de reloj simulado.
*   [ ] **CA6**: Un roadmap que Courses marca como oculto no aparece al alumno; uno bloqueado aparece con el motivo y la fecha.

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

**Escenario 4**

*   **Dado**: un examen habilitado de 18:00 a 20:00
*   **Cuando**: el alumno entra a las 17:59
*   **Entonces**: el gate responde `DATE_RESTRICTED` y el alumno ve «Se habilita hoy a las 18:00»

* * *

Prototipo
---------

*   **Capturas**: Nodo bloqueado por fecha y examen fuera de horario en el mapa.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-badge` para el estado.
*   **Mock API / Swagger**: Restricciones de Courses (`course.restrictions.read`) y evento de cambio a acordar.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 8 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Courses (restricciones y evento).
*   Módulos afectados: `CourseRestrictionsClient`, `GateEvaluator`, mapa del alumno.
*   Otros equipos / aprobaciones: G01 (bloqueante para el evento; publica las ventanas de examen, P9).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que G01 no publique el evento a tiempo; mitigación: leer por pull con caché corta. Zonas horarias en los exámenes; mitigación: guardar en UTC y mostrar en la del curso.


## Tareas

- [ ] #9311 T-49.9 Corroborar qué ya está hecho · New · Mateo Delgado Costa
- [ ] #9312 T-49.10 Distinguir oculto de bloqueado · New · Mateo Delgado Costa
- [ ] #9313 T-49.11 Actualizar el roadmap cuando Courses cambia una restricción · New · Mateo Delgado Costa
- [ ] #9314 T-49.12 Mostrarle al alumno lo bloqueado y cuándo se habilita · New · Mateo Delgado Costa
- [ ] #9315 T-49.13 Aplicar al examen la ventana horaria que publica Courses · New · Mateo Delgado Costa
- [ ] #9346 T-49.14 Wiki, OpenAPI y diagrama de secuencia · New · Franco Maximiliano Amarilla
