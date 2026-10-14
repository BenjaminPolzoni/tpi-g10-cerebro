---
tags: [tpi, g10, taiga, hu]
codigo: HU-49
ref: 7211
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-4230 Unidades del roadmap sincronizadas con Courses|EP-4230]]"
sprint: "Backlog"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7211
---

# HU-49: Aplicar en el roadmap las restricciones de sección y actividad que publica Courses

> [!info] Generado desde Taiga (2026-10-14 20:45). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7211) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **Backlog**
> Épica: [[epicas/EP-4230 Unidades del roadmap sincronizadas con Courses|EP-4230]] · Tareas cerradas: **0/8**

[G10] — HU-49 — Aplicar en el roadmap las restricciones de sección y actividad que publica Courses
--------------------------------------------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: que el roadmap respete las restricciones de fecha y de comisión que el profesor configura en Courses sobre secciones y actividades
*   **Para**: no ver ni entrar a lo que todavía no me corresponde

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Courses es dueño de las restricciones (fecha desde/hasta, comisión, operador ALL/ANY y comportamiento HIDDEN/LOCKED); Roadmap las lee y las aplica, no las edita. HIDDEN: la unidad o el nodo no aparece ni cuenta para el avance. LOCKED: aparece bloqueado con el motivo. Las restricciones de la sección y las de la actividad se cumplen juntas: una actividad no anula el bloqueo de su sección. La apertura es inclusiva y el cierre exclusivo, como en Courses. El gate rechaza con group_restricted o date_restricted. Las restricciones de comisión sobre secciones las resuelve HU-44; esta historia suma la fecha y el nivel de actividad. Los cambios rigen hacia adelante y no revierten desbloqueos (RF-CFG-06).
*   [ ] Validaciones: La restricción pertenece a una sección o actividad del curso-cohorte; la actividad está vinculada a un nodo con el identificador que defina el acta con G01.
*   [ ] Datos obligatorios: courseCohortId, course_section_id, identificador de actividad y condiciones.
*   [ ] Performance (tiempos, volumen, límites): Sin llamadas a Courses por consulta del recorrido: se usa la copia local que actualiza el evento.
*   [ ] Seguridad (roles, permisos, datos sensibles): Lectura con token técnico por el API Gateway (scope a proveer por G01/G07).
*   [ ] Accesibilidad (WCAG/teclado/lectores): Motivo en texto, por ejemplo «disponible desde el 12/10 08:00».
*   [ ] Otros: Bloqueada por G01: hoy las restricciones existen solo por sección (GET/PUT /course-sections/{id}/restrictions), solo las leen personas y no se publican eventos. Pedidos en T-49.1 y T-49.2. Los motivos nuevos del gate se piden a G09 en T-44.10.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Una unidad HIDDEN fuera de fecha no aparece ni cuenta para el avance.
*   [ ] **CA2**: Una unidad LOCKED fuera de fecha aparece bloqueada con su motivo.
*   [ ] **CA3**: El gate rechaza un nodo fuera de fecha con date_restricted.
*   [ ] **CA4**: Un cambio de restricción en Courses se refleja sin reiniciar el servicio y sin perder progreso.
*   [ ] **CA5**: Con Courses caído se usa la última copia guardada y se registra el error.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Restricciones de Courses en el roadmap

**Escenario 1**  

*   **Dado**: una unidad HIDDEN disponible desde mañana
*   **Cuando**: el alumno abre su recorrido hoy
*   **Entonces**: no la ve

**Escenario 2**  

*   **Dado**: una actividad LOCKED hasta el viernes dentro de una unidad abierta
*   **Cuando**: el alumno intenta entrar a su nodo
*   **Entonces**: el gate responde date_restricted con la fecha en el motivo

**Escenario 3**  

*   **Dado**: el profesor adelanta la fecha de apertura en Courses
*   **Cuando**: llega el evento de cambio
*   **Entonces**: el alumno ve la unidad en su próxima consulta y conserva su progreso

* * *
Prototipo
---------

*   **Capturas**: Recorrido del alumno con unidades y nodos bloqueados por fecha.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: Consumidos de Courses (a acordar con G01): lectura por lote de las restricciones de la cohorte y evento de cambio de restricciones en courses-lifecycle. Expuestos: GET /api/roadmap/courses/{courseId} y el gate con los motivos nuevos.

* * *
Estimación / Prioridad
----------------------

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Should

* * *
Dependencias / Impactos
-----------------------

*   Servicios involucrados: Courses (G01, bloqueante), Motor (motivos del gate), API Gateway.
*   Módulos afectados: Cliente de restricciones (nuevo), CoursesLifecycleEventListener, GateEvaluator, ProgressService, recorrido del front.
*   Otros equipos / aprobaciones: G01: lectura por servicio, restricciones de actividad y evento de cambio (T-49.1, T-49.2). G07: scope (T-10.6).
*   Impacto en datos / migraciones: Migración nueva con la copia local de restricciones (número a asignar tras V21).
*   Riesgos y mitigación (opcional): Que G01 no exponga las restricciones de actividad a tiempo; mitigación: aplicar primero las de sección.

## Tareas

- [ ] #7212 T-49.1 Pedido a G01: lectura de restricciones por servicio y restricciones de actividad · New · Sin asignar
- [ ] #7213 T-49.2 Pedido a G01: evento de cambio de restricciones · New · Sin asignar
- [ ] #7214 T-49.3 Cliente de restricciones y copia local · New · Sin asignar
- [ ] #7215 T-49.4 Consumir el evento de cambio de restricciones · New · Sin asignar
- [ ] #7216 T-49.5 Evaluar fecha y actividad en el recorrido y en el gate · New · Sin asignar
- [ ] #7217 T-49.6 Front: mostrar lo bloqueado con su motivo y ocultar lo HIDDEN · New · Sin asignar
- [ ] #7218 T-49.7 BDD de restricciones · New · Sin asignar
- [ ] #7219 T-49.8 Wiki, OpenAPI y diagrama de secuencia · New · Sin asignar
