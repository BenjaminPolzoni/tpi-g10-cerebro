---
tags: [tpi, g10, taiga, hu]
codigo: HU-45
ref: 5374
estado: "New"
responsable: "Lorenzo Araujo"
epicas: "[[epicas/EP-5371 Roadmap por grupo de la cohorte|EP-5371]], [[epicas/EP-8632 Deuda del Sprint 2|EP-8632]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5374
---

# HU-45: Ranking de la cohorte y avance por comisión

> [!info] Generado desde Taiga (2026-10-15 16:54). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5374) · Estado: **New** · Responsable: **Lorenzo Araujo** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-5371 Roadmap por grupo de la cohorte|EP-5371]], [[epicas/EP-8632 Deuda del Sprint 2|EP-8632]] · Tareas cerradas: **5/13**

[G10] — HU-45 — Ranking de la cohorte y avance por comisión
-----------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO / PROFESOR
*   **Quiero**: ver el ranking sin errores, por curso por defecto y filtrable por comisión, y como profesor ver el avance por comisión
*   **Para**: comparar el avance con el curso o la comisión

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Default: ranking por curso; la comisión (= grupo) es un filtro (P10, confirmado). El profesor configura si el ranking ordena por XP o por notas (P14); las notas vienen del Motor de desafíos y falta acordar con G09 cómo llegan. El desempate en cascada (HU-25) se mantiene. Corrección de los profes: hoy el ranking por grupo da error (sin reproducir); se arregla en este sprint (E1).
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): Anonimato de filas ajenas (DEC-007). El avance por comisión: ADMIN o PROFESSOR.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Filtro accesible con teclado.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Error del ranking por grupo reproducido y documentado.
*   [ ] **CA2**: El ranking muestra el del curso por defecto, con filtro opcional por comisión.
*   [ ] **CA3**: El profesor ve el avance por comisión (`GET /courses/{id}/groups/{gid}/progress`).
*   [ ] **CA4**: Test que cubre el caso que fallaba.
*   [ ] **CA5**: El profesor elige si el ranking ordena por XP o por notas.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Ranking y avance por comisión

**Escenario 1**

*   **Dado**: un curso con 2 comisiones
*   **Cuando**: el alumno abre el ranking
*   **Entonces**: ve el del curso completo

**Escenario 2**

*   **Dado**: el mismo curso
*   **Cuando**: elige su comisión
*   **Entonces**: ve solo los de su comisión, sin datos personales ajenos

**Escenario 3**

*   **Dado**: un profesor del curso
*   **Cuando**: abre el avance por comisión
*   **Entonces**: ve el progreso de cada comisión

* * *

Prototipo
---------

*   **Capturas**: Ranking con filtro; panel del profesor.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-select`, `generic-table`.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/ranking?group_id=… y GET /api/roadmap/courses/{courseId}/groups/{groupId}/progress.

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

*   Servicios involucrados: Courses (comisiones).
*   Módulos afectados: `RankingController`, `RankingService`, `GroupProgressController`, `ranking-panel`.
*   Otros equipos / aprobaciones: G09 (cómo llegan las notas del Motor; solo para CA5).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que G09 no defina a tiempo cómo llegan las notas; mitigación: pedirlo la semana 1 (T-45.12).


## Tareas

- [x] #5421 T-45.1 Ranking de la cohorte con la XP compartida · Closed · Lorenzo Araujo
- [x] #5422 T-45.2 Parámetro de comisión en el avance (no en el ranking) · Closed · Lorenzo Araujo
- [ ] #5423 T-45.3 Selector de comisión (filtra avance, no ranking) en StaffRankingView, teacher-home-page y la vista del alumno · In progress · Lorenzo Araujo
- [x] #5424 T-45.4 Alumno en varias comisiones y alumno quitado de una · Closed · Lorenzo Araujo
- [x] #5425 T-45.5 BDD ranking de la cohorte · Closed · Lorenzo Araujo
- [x] #5426 T-45.6 Wiki, OpenAPI y diagrama de secuencia · Closed · Quinteros Tomás
- [ ] #9305 T-45.7 Reproducir y arreglar el error del ranking por comisión · New · Benjamin Polzoni
- [ ] #9306 T-45.8 Ranking del curso con filtro opcional por comisión · New · Benjamin Polzoni
- [ ] #9307 T-45.9 Filtro por comisión en la pantalla del ranking · New · Benjamin Polzoni
- [ ] #9308 T-45.10 Avance por comisión para el profesor · New · Benjamin Polzoni
- [ ] #9309 T-45.11 Elegir si el ranking ordena por XP o por notas · New · Benjamin Polzoni
- [ ] #9310 T-45.12 Acordar con el Motor (G09) cómo llegan las notas · New · Benjamin Polzoni
- [ ] #9345 T-45.13 Wiki, OpenAPI y diagrama de secuencia · New · Quinteros Tomás
