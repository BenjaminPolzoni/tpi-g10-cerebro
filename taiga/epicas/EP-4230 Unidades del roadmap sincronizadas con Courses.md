---
tags: [tpi, g10, taiga, epica]
ref: 4230
estado: "New"
responsable: "Sin asignar"
avance: "5/6"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/4230
---

# EP-4230: Unidades del roadmap sincronizadas con Courses

> [!info] Generado desde Taiga (2026-10-14 20:45). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/4230) · Estado: **New** · Responsable: **Sin asignar** · HU cerradas: **5/6**

[G10] — Unidades del roadmap sincronizadas con Courses
------------------------------------------------------

* * *

Objetivo
--------

Que las unidades del roadmap sean las secciones que el profesor gestiona en Courses, que es la única fuente. Roadmap refleja altas, renombres, reordenamientos y bajas sin que ningún alumno pierda progreso ni desbloqueos.

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: el ABMC de secciones es del equipo de Courses y ya está hecho. Una sección de Courses equivale a una unidad del roadmap (1:1). Roadmap guarda course\_section\_id como UUID sin FK, igual que courseCohortId y challengeId. Los nodos de cada unidad siguen siendo de Roadmap (HU-01): Courses define las unidades y Roadmap lo que se recorre dentro.
*   Restricciones (legales/técnicas): se llama a Courses solo por el Gateway y con token técnico, nunca con el JWT de una persona (agent.md §2.5). Los cambios rigen hacia adelante y nunca revierten desbloqueos (RF-CFG-06). Bajas lógicas (RF-NFR-01). La sincronización nunca borra y regenera el grafo: reconcilia por course\_section\_id. No se inventan payloads de eventos de Courses: lo que figura es propuesta. Prohibido crear topics (P-09).

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] El profesor crea una sección en Cursos y la ve como unidad en el editor del roadmap. Si la renombra, reordena o da de baja, el roadmap lo refleja sin que ningún alumno pierda completados, lecturas, XP ni desbloqueos.
*   [ ] KPIs iniciales: ningún KPI de producto aplica. El indicador propio es el tiempo de sincronización: 20 secciones en menos de 500 ms con una sola llamada a Courses (RF-NFR-03).
*   [ ] Sin regresiones críticas en E3: el gate responde igual antes y después de sincronizar para todo alumno con un nodo ya habilitado.
*   [ ] Observabilidad y alertas: cada sincronización deja un log (cohorte, origen, altas, cambios, bajas, sin vincular). Alerta si Courses rechaza el token más de N veces seguidas.
*   [ ] Documentación publicada: la Wiki con el acta con Courses, la regla de reconciliación y el endpoint en OpenAPI.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: Courses (bloqueante: scope en la lectura de secciones y, si se acuerda, eventos de sección), API Gateway. Notificaciones asigna el topic si hay eventos (P-09).
*   Módulos afectados: clients/courses, SectionEntity, GraphService, RoadmapSimulationService (init-mvp), editor del profesor en el front.
*   Otros equipos: Courses es el bloqueante principal; si no habilita el token técnico a tiempo rige el plan B.
*   Impacto en datos / migraciones: migración V16\_\_section\_course\_section\_id.sql con section.course\_section\_id UUID NULL y único por (roadmap\_id, course\_section\_id) entre las activas.
*   Feature toggles / flags: unidades-desde-courses. Apagado, comportamiento actual; encendido, el alta manual de unidades se rechaza y el front la oculta. Plan B: si Courses no habilita el token técnico a tiempo, se construye y prueba contra el doble con el flag apagado; después se enciende el flag y se pasa COURSES\_SECTIONS\_CLIENT\_MODE=http, sin tocar código.
*   Historias previstas: HT-07, HU-36, HU-17 (redefinida), HU-18 (redefinida), HU-37.


## Historias

| HU | Estado | Responsable | Sprint | Tareas |
|---|---|---|---|---|
| [[historias/HU-36 Sincronizar las unidades del roadmap con las secciones de Courses\|HU-36]] Sincronizar las unidades del roadmap con las secciones de Courses | Done | Mateo Delgado Costa | G10 - Sprint 2 | 9/9 |
| [[historias/HT-07 Acordar con Courses la lectura de secciones con token técnico\|HT-07]] Acordar con Courses la lectura de secciones con token técnico | Done | Mateo Delgado Costa | G10 - Sprint 2 | 5/5 |
| [[historias/HU-17 Reflejar la baja de una sección de Courses sin que los alumnos pierdan progreso\|HU-17]] Reflejar la baja de una sección de Courses sin que los alumnos pierdan progreso | Done | Mateo Delgado Costa | G10 - Sprint 2 | 8/8 |
| [[historias/HU-18 Reflejar el reordenamiento de secciones de Courses\|HU-18]] Reflejar el reordenamiento de secciones de Courses | Done | Mateo Delgado Costa | G10 - Sprint 2 | 4/4 |
| [[historias/HU-37 Ver en el editor del roadmap las unidades de Cursos y sincronizarlas (front)\|HU-37]] Ver en el editor del roadmap las unidades de Cursos y sincronizarlas (front) | Done | Iker Alonso | G10 - Sprint 2 | 6/6 |
| [[historias/HU-49 Aplicar en el roadmap las restricciones de sección y actividad que publica Courses\|HU-49]] Aplicar en el roadmap las restricciones de sección y actividad que publica Courses | New | Sin asignar | Backlog | 0/8 |
