---
tags: [tpi, g10, taiga, epica]
ref: 5371
estado: "New"
responsable: "Sin asignar"
avance: "2/3"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/5371
---

# EP-5371: Roadmap por grupo de la cohorte

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/5371) · Estado: **New** · Responsable: **Sin asignar** · HU cerradas: **2/3**

[G10] — Roadmap por grupo de la cohorte
---------------------------------------


* * *
Objetivo
--------

Que dentro de un mismo curso-cohorte el roadmap distinga a los alumnos por grupo (comisión: 2W1, 2W2, …) tal como los define Courses: el ranking es por grupo, cada alumno ve y avanza solo en las unidades habilitadas para su grupo y el profesor sigue el avance de cada grupo, sin duplicar el roadmap ni perder progreso.


* * *
Suposiciones y Restricciones
----------------------------

*   Suposiciones: el grupo es de Courses: cohort_group (course_cohort_id, name, is_active) y cohort_group_member (cohort_group_id, enrollment_id) existen desde su V1, y la restricción de sección por GROUP desde su V12. Roadmap guarda cohort_group_id como UUID sin FK. El roadmap sigue siendo uno por curso-cohorte (no uno por grupo). Las restricciones GROUP de cada sección deciden qué unidad ve cada grupo. Un alumno puede pertenecer a varios grupos (comisiones) de la cohorte y solo un PROFESSOR o GESTOR lo agrega, quita o mueve, en Courses. La XP, los completados y las lecturas son de la cohorte y se comparten entre sus comisiones (decisión del 08/10, reemplaza P-29).
*   Restricciones (legales/técnicas): llamadas a Courses solo por el Gateway y con token técnico (agent.md §2.5). Roadmap no tiene ABM de grupos. Un cambio de grupo es hacia adelante y no revierte desbloqueos (RF-CFG-06). Bajas lógicas (RF-NFR-01). Prohibido crear topics (P-09).


* * *
Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] Un alumno de 2W1 ve en su recorrido solo las unidades sin restricción o restringidas a 2W1; las de 2W2 no aparecen ni cuentan para su avance.
*   [ ] El gate rechaza la entrega en un nodo de una unidad que no corresponde al grupo del alumno.
*   [ ] El ranking es por grupo: un alumno de 2W1 se compara solo con los de 2W1 (posición, percentiles y zonas); el profesor elige el grupo para ver su ranking y su avance.
*   [ ] Un alumno de 2W1 y 2W2 ve el roadmap de cada comisión y aparece en los dos rankings con la misma XP; al agregarlo, quitarlo o moverlo conserva completados, lecturas, XP y desbloqueos.
*   [ ] Sin regresiones en E3: una cohorte sin grupos se comporta igual que hoy.
*   [ ] Documentación publicada: la Wiki con el acta de G01 sobre grupos y los endpoints en OpenAPI.


* * *
Dependencias / Impactos
-----------------------

*   Servicios / APIs: G01 — Courses (bloqueante: hoy no hay ningún endpoint de grupos; tiene que exponer con token técnico los grupos de la cohorte, el grupo de cada matrícula y las restricciones GROUP de cada sección; avisar el cambio de grupo por evento o permitir consultarlo). API Gateway.
*   Épicas relacionadas: Unidades del roadmap sincronizadas con Courses (HT-07, HU-36): la unidad necesita course_section_id para cruzarla con la restricción GROUP de su sección. Ranking y cierre académico: HU-24 y HU-25 calculan posiciones, percentiles y zonas dentro del grupo.
*   Impacto en datos / migraciones: tabla student_course_group (student_course_id, cohort_group_id) (migración nueva, número a asignar tras V21).
*   Front: selector de grupo en teacher-home-page y en StaffRankingView; el recorrido del alumno no cambia de pantalla.
*   Feature toggles / flags: roadmap-por-grupo (apagado = toda la cohorte ve todas las unidades, como hoy).
*   Historias previstas: HT-10 (acta con Courses para grupos + cliente de grupos), HU-44 (el alumno ve solo las unidades de su grupo), HU-45 (ranking por grupo y avance por grupo para el profesor). Pedido 8 del Sprint 2.


## Historias

| HU | Estado | Responsable | Sprint | Tareas |
|---|---|---|---|---|
| [[historias/HT-10 [DEPRECADA] Acta con Courses para comisiones + cliente de comisiones\|HT-10]] [DEPRECADA] Acta con Courses para comisiones + cliente de comisiones | Done | Mateo Delgado Costa | G10 - Sprint 2 | 6/6 |
| [[historias/HU-44 Ver el roadmap de cada una de mis comisiones\|HU-44]] Ver el roadmap de cada una de mis comisiones | Done | Baltasar Rodriguez Teruel | G10 - Sprint 2 | 10/10 |
| [[historias/HU-45 Ranking de la cohorte y avance por comisión\|HU-45]] Ranking de la cohorte y avance por comisión | New | Lorenzo Araujo | G10 - Sprint 03 | 5/13 |
