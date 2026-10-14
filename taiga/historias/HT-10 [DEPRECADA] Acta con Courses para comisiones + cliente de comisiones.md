---
tags: [tpi, g10, taiga, ht]
codigo: HT-10
ref: 5372
estado: "Done"
responsable: "Mateo Delgado Costa"
epica: "[G10] — Roadmap por grupo de la cohorte"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5372
---

# HT-10: [DEPRECADA] Acta con Courses para comisiones + cliente de comisiones

> [!info] Generado desde Taiga (2026-10-14 18:47). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5372) · Estado: **Done** · Responsable: **Mateo Delgado Costa** · Sprint: **G10 - Sprint 2**

[G10] — HT-10 — Acta con Courses para comisiones + cliente de comisiones
------------------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: acordar con Courses cómo exponer las comisiones de la cohorte y las comisiones de cada alumno, y construir el cliente que las lee con token técnico
*   **Para**: que HU-44 y HU-45 tengan una fuente real de comisiones y membresías

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Grupo = comisión de Courses dentro del curso-cohorte (por ejemplo 2W1 y 2W2 de Programación IV 2020). Un alumno puede pertenecer a varias comisiones de la misma cohorte: Courses ya lo permite (PUT …/participants/{id}/group, DELETE …/participants/{id}/groups/{cohortGroupId} y PATCH para mover). La XP, los completados y las lecturas son de la cohorte y se comparten entre todas las comisiones del alumno. Decisión del 08/10: reemplaza P-29 y D-02 («un solo grupo por alumno»). Roadmap guarda las membresías como UUID sin FK y nunca da de alta comisiones. Justificación técnica: hoy los endpoints de comisiones de Courses solo aceptan GESTOR y PROFESSOR y no hay evento de cambio de membresía; sin acta ni cliente, HU-44 y HU-45 no tienen fuente de datos. Ningún actor final la percibe (falla la V de INVEST a propósito).
*   [ ] Validaciones: Las membresías se identifican por el user_id del alumno (Roadmap no conoce el enrollment_id). El stub del cliente existe solo en el perfil de test.
*   [ ] Datos obligatorios: courseCohortId; migración student_course_group (student_course_id, cohort_group_id) con baja lógica, número a asignar tras V21.
*   [ ] Performance (tiempos, volumen, límites): Lectura por lote de las membresías de la cohorte, no una llamada por alumno; actualización por evento.
*   [ ] Seguridad (roles, permisos, datos sensibles): Token técnico por el Gateway (scope propuesto course.groups.read, a confirmar con G01 y G07), nunca el JWT de una persona.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica (sin pantalla).
*   [ ] Otros: Con Courses caído se usan las últimas membresías guardadas y se registra el error. El acta se archiva en tpi-roadmap/docs/contracts/ y en la Wiki. Dependencias: G01 (bloqueante) y G07 (scope, T-10.6).

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Acta con G01 con los endpoints de comisiones, las membresías por alumno (varias) y el evento de cambio de membresía.
*   [ ] **CA2**: El cliente devuelve todas las comisiones de cada alumno de la cohorte.
*   [ ] **CA3**: student_course_group se actualiza cuando el alumno se agrega, se quita o se mueve de comisión, sin tocar el progreso.
*   [ ] **CA4**: El stub del cliente solo existe en el perfil de test.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Comisiones de la cohorte desde Courses

**Escenario 1**  

*   **Dado**: un alumno en 2W1 y en 2W2
*   **Cuando**: Roadmap consulta sus comisiones
*   **Entonces**: recibe 2W1 y 2W2

**Escenario 2**  

*   **Dado**: un gestor quita al alumno de 2W2
*   **Cuando**: Roadmap recibe el cambio
*   **Entonces**: student_course_group queda solo con 2W1 y el progreso no cambia

**Escenario 3**  

*   **Dado**: Courses caído
*   **Cuando**: se consultan las comisiones
*   **Entonces**: se usan las últimas guardadas y se registra el error

* * *
Prototipo
---------

*   **Capturas**: Sin pantalla.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: A acordar con G01: comisiones de la cohorte y membresías por lote con identidad de servicio; evento de cambio de membresía en courses-lifecycle.

* * *
Estimación / Prioridad
----------------------

*   **Puntos (Fibonacci)**: 5
*   **Prioridad (MoSCoW / Numérica)**: Must

* * *
Dependencias / Impactos
-----------------------

*   Servicios involucrados: Courses (G01), Users/Identity (G07, scopes), API Gateway.
*   Módulos afectados: Cliente de comisiones (nuevo), CoursesLifecycleEventListener, StudentCourse.
*   Otros equipos / aprobaciones: G01 (acta, bloqueante) y G07 (alta del scope).
*   Impacto en datos / migraciones: Tabla student_course_group.
*   Riesgos y mitigación (opcional): Que Courses no habilite la lectura por servicio a tiempo; mitigación: pedido temprano y flag roadmap-by-group apagado.

---

Deprecada: asumía actualización por evento y almacén local de membresías; el plan vigente es PULL con scopes H1. Reemplazada por la historia nueva HT-10 (pull).

## Tareas

- [x] #5409 T-10.1 Acta con G01: comisiones, membresías por alumno (varias) y aviso de cambio · Closed · Baltasar Rodriguez Teruel
- [x] #5410 T-10.2 Cliente de comisiones (comisiones de la cohorte y de cada alumno); stub solo en test · Closed · Baltasar Rodriguez Teruel
- [x] #5411 [DEPRECADA] T-10.3 Migración student_course_group y actualización al agregar, quitar o mover de comisión · Closed · Mateo Delgado Costa
- [x] #5412 T-10.4 Contract test del cliente de grupos · Closed · Iker Alonso
- [x] #5413 T-10.5 Wiki, OpenAPI y diagrama de secuencia · Closed · Quinteros Tomás
- [x] #7220 T-10.6 Pedido a G07: scopes de comisiones y restricciones para roadmap-service · Closed · Mateo Delgado Costa
