---
tags: [tpi, g10, taiga, hu]
codigo: HU-18
ref: 4235
estado: "Done"
responsable: "Mateo Delgado Costa"
epicas: "[[epicas/EP-4230 Unidades del roadmap sincronizadas con Courses|EP-4230]]"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4235
---

# HU-18: Reflejar el reordenamiento de secciones de Courses

> [!info] Generado desde Taiga (2026-10-14 20:44). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4235) · Estado: **Done** · Responsable: **Mateo Delgado Costa** · Sprint: **G10 - Sprint 2**
> Épica: [[epicas/EP-4230 Unidades del roadmap sincronizadas con Courses|EP-4230]] · Tareas cerradas: **4/4**

[G10] — HU-18 — Reflejar el reordenamiento de secciones de Courses
------------------------------------------------------------------


* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: ver las unidades en el mismo orden que las secciones de Cursos
*   **Para**: seguir el curso en el orden que pensó el profesor


* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El orden de las unidades es el orderIndex de Courses; reordenar no cambia estados de nodos ni desbloqueos (RF-CFG-06).
*   [ ] Validaciones: El orden se aplica en la misma transacción de la sincronización.
*   [ ] Otros: Dependencias / impactos: Depende de: HU-36. Preguntas abiertas: —


* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Al reordenar secciones en Cursos y sincronizar, las unidades quedan en ese orden.
*   [ ] **CA2**: Ningún estado de nodo ni desbloqueo cambia por reordenar.
*   [ ] **CA3**: El recorrido del alumno muestra el orden nuevo.


* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Orden tomado de Courses

**Escenario 1**  

*   **Dado**: tres secciones en orden A, B, C
*   **Cuando**: el profesor las reordena C, A, B y sincroniza
*   **Entonces**: el recorrido muestra C, A, B

**Escenario 2**  

*   **Dado**: un alumno con la unidad B desbloqueada
*   **Cuando**: se reordena
*   **Entonces**: B sigue desbloqueada

**Escenario 3**  

*   **Dado**: dos sincronizaciones sin cambios
*   **Cuando**: se comparan
*   **Entonces**: el orden no cambia

* * *
Prototipo
---------

*   **Capturas**: Pendiente.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: Parte de la sincronización de HU-36.


---
ACTUALIZACION (plan vigente)
- T-18.1 (aplicar orderIndex a sort_order) y T-18.2 (no retroactividad) ya cerradas.
- El orden de las unidades sigue el orderIndex de Courses dentro del sync (PULL) de HU-36 (modelo B).
- Scopes finales (H1): orden/material de actividades=`course.activities.read`.

## Tareas

- [x] #4269 T-18.1 Aplicar orderIndex de Courses a sort_order en la reconciliación · Closed · Mateo Delgado Costa
- [x] #4270 T-18.2 Test de no retroactividad al reordenar · Closed · Mateo Delgado Costa
- [x] #5378 T-18.3 Mostrar el orden de Courses en el recorrido · Closed · Mateo Delgado Costa
- [x] #5379 T-18.4 Wiki, OpenAPI y diagrama de secuencia · Closed · Quinteros Tomás
