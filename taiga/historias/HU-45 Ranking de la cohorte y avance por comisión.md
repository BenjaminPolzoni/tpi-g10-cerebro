---
tags: [tpi, g10, taiga, hu]
codigo: HU-45
ref: 5374
estado: "New"
responsable: "Lorenzo Araujo"
epicas: "[[epicas/EP-5371 Roadmap por grupo de la cohorte|EP-5371]]"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5374
---

# HU-45: Ranking de la cohorte y avance por comisión

> [!info] Generado desde Taiga (2026-10-14 20:45). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5374) · Estado: **New** · Responsable: **Lorenzo Araujo** · Sprint: **G10 - Sprint 2**
> Épica: [[epicas/EP-5371 Roadmap por grupo de la cohorte|EP-5371]] · Tareas cerradas: **5/6**

[G10] — HU-45 — Ranking y avance por comisión
---------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR y ALUMNO
*   **Quiero**: ver el ranking de mi cohorte y el avance de cada comisión del curso
*   **Para**: comparar la XP de la cohorte en el ranking y seguir el avance de cada comisión por separado

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El ranking es de la COHORTE y se calcula con la XP de la cohorte, que es compartida entre todas las comisiones del alumno. El selector de comisión filtra el AVANCE/recorrido (modelo B), NO el ranking: sirve para ver el avance de una comisión, pero la XP y las posiciones del ranking son siempre de la cohorte. Solo PROFESSOR/MANAGER (Gestor) asignan el grupo de cada alumno; Roadmap solo lee, nunca asigna ni mueve comisiones. Decisión del 08/10 (reemplaza D-02 y P-29).
*   [ ] Validaciones: La comisión elegida (para el avance) pertenece al curso-cohorte; el alumno solo puede pedir el avance de sus comisiones.
*   [ ] Datos obligatorios: courseCohortId; la comisión elegida solo aplica al avance (selector), no al ranking.
*   [ ] Performance (tiempos, volumen, límites): Mismo endpoint de ranking de HU-24 (siempre por cohorte); el parámetro de comisión solo aplica a los endpoints de avance; sin llamadas extra a Courses.
*   [ ] Seguridad (roles, permisos, datos sensibles): El ranking es de la cohorte (visible según HU-24). Para el avance, PROFESSOR dueño, GESTOR o ADMIN eligen cualquier comisión; el alumno solo las suyas (403 si pide otra).
*   [ ] Accesibilidad (WCAG/teclado/lectores): Selector de comisión (para el avance) operable por teclado y con etiqueta en texto.
*   [ ] Otros: Depende de HU-24 y HT-10.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor elige 2W1 y ve el avance de 2W1; el ranking que ve es de la cohorte.
*   [ ] **CA2**: Un alumno de 2W1 y 2W2 aparece una sola vez en el ranking de la cohorte con su XP.
*   [ ] **CA3**: Al quitar a un alumno de 2W1, el avance de 2W1 ya no lo incluye; su posición en el ranking de la cohorte no cambia.
*   [ ] **CA4**: Un alumno que pide el avance de una comisión ajena recibe 403.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Ranking de la cohorte y avance por comisión

**Escenario 1**  

*   **Dado**: un curso con 2W1 y 2W2
*   **Cuando**: el profesor elige 2W2
*   **Entonces**: ve solo a los alumnos de 2W2 en el avance; el ranking sigue siendo de la cohorte

**Escenario 2**  

*   **Dado**: un alumno de 2W1 y 2W2 con 500 XP
*   **Cuando**: se calcula el ranking de la cohorte
*   **Entonces**: aparece una sola vez con 500 XP

**Escenario 3**  

*   **Dado**: un alumno quitado de 2W1
*   **Cuando**: se recalcula el avance de 2W1
*   **Entonces**: ya no aparece en el avance de 2W1; el ranking de la cohorte no cambia

* * *
Prototipo
---------

*   **Capturas**: Selector de comisión (filtra avance, no ranking) en StaffRankingView, teacher-home-page y el ranking del alumno.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/ranking (HU-24, por cohorte); parámetro de comisión solo en los endpoints de avance del profesor.

* * *
Estimación / Prioridad
----------------------

*   **Puntos (Fibonacci)**: 5
*   **Prioridad (MoSCoW / Numérica)**: Should

* * *
Dependencias / Impactos
-----------------------

*   Servicios involucrados: Courses (comisiones, vía HT-10), API Gateway.
*   Módulos afectados: RankingService, RankingController, StaffRankingView, teacher-home-page.
*   Otros equipos / aprobaciones: G01 (HT-10).
*   Impacto en datos / migraciones: Usa student_course_group de HT-10.
*   Riesgos y mitigación (opcional): Ninguno adicional.

## Tareas

- [x] #5421 T-45.1 Ranking de la cohorte con la XP compartida · Closed · Lorenzo Araujo
- [x] #5422 T-45.2 Parámetro de comisión en el avance (no en el ranking) · Closed · Lorenzo Araujo
- [ ] #5423 T-45.3 Selector de comisión (filtra avance, no ranking) en StaffRankingView, teacher-home-page y la vista del alumno · In progress · Lorenzo Araujo
- [x] #5424 T-45.4 Alumno en varias comisiones y alumno quitado de una · Closed · Lorenzo Araujo
- [x] #5425 T-45.5 BDD ranking de la cohorte · Closed · Lorenzo Araujo
- [x] #5426 T-45.6 Wiki, OpenAPI y diagrama de secuencia · Closed · Quinteros Tomás
