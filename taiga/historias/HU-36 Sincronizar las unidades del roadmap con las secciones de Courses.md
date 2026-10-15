---
tags: [tpi, g10, taiga, hu]
codigo: HU-36
ref: 4229
estado: "Done"
responsable: "Mateo Delgado Costa"
epicas: "[[epicas/EP-4230 Unidades del roadmap sincronizadas con Courses|EP-4230]]"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4229
---

# HU-36: Sincronizar las unidades del roadmap con las secciones de Courses

> [!info] Generado desde Taiga (2026-10-15 16:53). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4229) · Estado: **Done** · Responsable: **Mateo Delgado Costa** · Sprint: **G10 - Sprint 2**
> Épica: [[epicas/EP-4230 Unidades del roadmap sincronizadas con Courses|EP-4230]] · Tareas cerradas: **9/9**

[G10] — HU-36 — Sincronizar las unidades del roadmap con las secciones de Courses
---------------------------------------------------------------------------------


* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: que las unidades de mi roadmap sean las secciones que gestiono en Cursos
*   **Para**: no cargar dos veces la estructura del curso y que el alumno vea el mismo orden que en Cursos


* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Una sección equivale a una unidad (1:1). La sincronización reconcilia por course_section_id: crea la unidad si no existe y renombra si cambió el título, sin tocar sus nodos. Nunca borra y regenera el grafo (regenerate queda deshabilitado con el flag encendido). Los nodos de cada unidad siguen siendo de Roadmap (HU-01).
*   [ ] Validaciones: Solo PROFESSOR dueño del curso-cohorte o ADMIN; curso no archivado (409).
*   [ ] Datos obligatorios: V16: section.course_section_id UUID NULL, único por (roadmap_id, course_section_id) entre activas; sin FK.
*   [ ] Performance (tiempos, volumen, límites): 20 secciones en menos de 500 ms con una sola llamada a Courses (RF-NFR-03).
*   [ ] Otros: Cada sincronización deja un log; alerta si Courses rechaza el token más de N veces seguidas. Flag unidades-desde-courses (apagado = comportamiento actual). Dependencias / impactos: Depende de: HT-07. Datos: migración V16. Relacionadas: HU-17, HU-18, HU-37, HU-44 (la restricción GROUP se cruza por course_section_id). Preguntas abiertas: decisión #2 del PO (aristas huérfanas, para HU-17).


* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Una sección nueva en Cursos aparece como unidad al sincronizar.
*   [ ] **CA2**: Renombrar una sección renombra la unidad sin tocar sus nodos ni el progreso.
*   [ ] **CA3**: Sincronizar dos veces seguidas no duplica unidades (idempotente).
*   [ ] **CA4**: Las unidades creadas por init-mvp quedan vinculadas a su sección sin regenerarse.
*   [ ] **CA5**: Con Courses caído la sincronización falla con error explícito y el roadmap queda como estaba.


* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Unidades tomadas de las secciones de Courses

**Escenario 1**  

*   **Dado**: una sección nueva en Cursos
*   **Cuando**: el profesor sincroniza
*   **Entonces**: aparece una unidad nueva vacía con ese título y ese orden

**Escenario 2**  

*   **Dado**: una unidad con nodos y alumnos avanzando
*   **Cuando**: la sección se renombra y se sincroniza
*   **Entonces**: la unidad cambia de nombre y ningún estado de nodo cambia

**Escenario 3**  

*   **Dado**: Courses no responde
*   **Cuando**: el profesor sincroniza
*   **Entonces**: error explícito, log registrado y roadmap sin cambios

* * *
Prototipo
---------

*   **Capturas**: Pendiente.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: POST /api/roadmap/courses/{courseId}/sections/sync (propuesta). Botón en el editor (HU-37).


## Tareas

- [x] #4252 T-36.1 Migración V18: section.course_section_id e índice único entre activas · Closed · Mateo Delgado Costa
- [x] #4253 T-36.2 Servicio de reconciliación por course_section_id (alta y renombre sin tocar nodos) · Closed · Mateo Delgado Costa
- [x] #4254 T-36.3 Endpoint de sincronización (PROFESSOR dueño o ADMIN) detrás del flag unidades-desde-courses · Closed · Mateo Delgado Costa
- [x] #4255 T-36.4 Vincular las unidades existentes de init-mvp a su sección sin regenerar · Closed · Mateo Delgado Costa
- [x] #4256 T-36.5 Log de sincronización y alerta por rechazos de token consecutivos · Closed · Mateo Delgado Costa
- [x] #4257 T-36.6 Medir 20 secciones en menos de 500 ms con una sola llamada · Closed · Mateo Delgado Costa
- [x] #4258 T-36.7 Guard lista vacia + BDD extra (baja puntual, 401/403) · Closed · Ludmila Mailen Cejas
- [x] #4259 T-36.8 Wiki, OpenAPI y diagrama de secuencia · Closed · Quinteros Tomás
- [x] #7475 Sync de nodos/orden desde actividades de Courses · Closed · Mateo Delgado Costa
