---
tags: [tpi, g10, taiga, hu]
codigo: HU-04
ref: 734
estado: "Done"
responsable: "Iker Alonso"
epica: "[G10] — Nodos de contenido y lectura previa"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/734
---

# HU-04: Vincular un nodo de contenido al material publicado por Courses

> [!info] Generado desde Taiga (2026-10-14 18:46). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/734) · Estado: **Done** · Responsable: **Iker Alonso** · Sprint: **G10 - Sprint 2**

[G10] — HU-04 — Vincular un nodo de contenido al material publicado por Courses
-------------------------------------------------------------------------------


* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: elegir qué material de Cursos muestra cada nodo de lectura
*   **Para**: que el alumno lea el material correcto de la unidad


* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El material lo guarda Courses en Garage (D-03); Roadmap guarda solo content_id (UUID sin FK). Solo material publicado de la misma sección o cohorte.
*   [ ] Validaciones: content_id existente y publicado en Courses; nodo de tipo CONTENIDO; PROFESSOR dueño.
*   [ ] Otros: Condicionada a que G01 habilite FILE y LINK y la lectura por lote (P-16). Dependencias / impactos: Servicios: G01 (bloqueante). Relacionadas: HU-42, HU-46, HU-37. Preguntas abiertas: P-16.


* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor elige un material de la sección y queda vinculado.
*   [ ] **CA2**: Un material no publicado o de otra cohorte se rechaza.
*   [ ] **CA3**: El nodo muestra el título que devuelve Courses.


* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Vinculación de nodos de contenido con material de Courses

**Escenario 1**  

*   **Dado**: un material publicado en la sección
*   **Cuando**: el profesor lo vincula al nodo
*   **Entonces**: queda guardado el content_id

**Escenario 2**  

*   **Dado**: un material en borrador
*   **Cuando**: intenta vincularlo
*   **Entonces**: rechazo con mensaje

**Escenario 3**  

*   **Dado**: un nodo vinculado
*   **Cuando**: el alumno abre el detalle
*   **Entonces**: ve el título del material

* * *
Prototipo
---------

*   **Capturas**: Pendiente.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: CoursesCatalogClient (hoy en stub y sin uso) contra el lote de Courses; selector en el editor.


## Tareas

- [x] #1153 T-04.1 node.content_id y validación contra Courses (publicado, misma cohorte) · Closed · Iker Alonso
- [x] #1154 T-04.3 Selector de material de la sección en el editor · Closed · Iker Alonso
- [x] #1155 T-04.2 CoursesCatalogClient a modo http con lectura por lote · Closed · Iker Alonso
- [x] #1157 T-04.4 BDD vincular contenido · Closed · Iker Alonso
- [x] #5376 T-04.5 Wiki, OpenAPI y diagrama de secuencia · Closed · Quinteros Tomás
