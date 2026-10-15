---
tags: [tpi, g10, taiga, epica]
ref: 8633
estado: "New"
responsable: "Sin asignar"
avance: "0/11"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/8633
---

# EP-8633: Múltiples roadmaps por curso y grafo configurable

> [!info] Generado desde Taiga (2026-10-15 16:56). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/8633) · Estado: **New** · Responsable: **Sin asignar** · HU cerradas: **0/11**

[G10] — Múltiples roadmaps por curso y grafo configurable
---------------------------------------------------------

* * *

Objetivo
--------

Que un curso pueda tener uno o más roadmaps, con secciones y nodos relacionados por reglas configurables, guardados en Neo4j y editables desde el mapa (vista de grafo) y desde la lista de nodos de cada sección en «Contenido del curso» de Courses.

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: Neo4j es pedido de los profes (DEC-016). Ya existen dependencias AND/OR entre secciones (V25) y entre nodos (V5/V7). El estado del alumno se queda en Postgres.
*   Restricciones (legales/técnicas): Módulo `graph` dentro de roadmap-service, no un micro nuevo. UUID compartidos y solo baja lógica. P1 a P4 respondidas por los profes el 2026-10-15 (DEC-017, DEC-018).

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] Un curso de demo tiene 2 roadmaps y el alumno recorre cada uno con su progreso.
*   [ ] El profesor define dependencias entre secciones y entre nodos (AND/OR, XP mínimo, reglas combinadas) y el gate las respeta.
*   [ ] La estructura vive en Neo4j y el estado del alumno sigue en Postgres, con los mismos UUID.
*   [ ] El mapa y la lista de nodos de «Contenido del curso» editan el mismo roadmap y muestran lo mismo.
*   [ ] KPIs iniciales alcanzan: Un curso de demo con 2 roadmaps recorrido de punta a punta. P95 del gate por debajo de 200 ms.
*   [ ] Sin regresiones críticas en: Las rutas `/courses/{id}/...` siguen funcionando mientras el front migra. Los tests existentes del gate y del progreso pasan.
*   [ ] Observabilidad y alertas configuradas: Latencia del gate y del endpoint `/graph`; alerta por ids huérfanos entre Neo4j y Postgres.
*   [ ] Documentación de uso y operación publicada: Modelo del grafo, endpoints nuevos en OpenAPI y contratos con G01/G09 actualizados.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: Neo4j (nuevo), Courses, Motor.
*   Módulos afectados: Módulo `graph`, gate, progreso, editor del profesor (mapa y lista de nodos embebida en Courses), roadmap del alumno.
*   Otros equipos: Plataforma (infra de Neo4j), G01 (secciones), G09 (eventos), equipo UI-KIT (componente de grafo).
*   Impacto en datos / migraciones: Grafo nuevo en Neo4j con migración inicial desde Postgres; se quita el UNIQUE de `roadmap.course_cohort_id`.
*   Feature toggles / flags: Flag de lectura desde Neo4j durante la convivencia; `multiple_roadmaps_allowed` por curso.


## Historias

| HU | Estado | Responsable | Sprint | Tareas |
|---|---|---|---|---|
| [[historias/HT-16 Validar la infra de Neo4j y modelar las relaciones\|HT-16]] Validar la infra de Neo4j y modelar las relaciones | New | Sin asignar | G10 - Sprint 03 | 0/4 |
| [[historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]] Modelo 1 a N de curso a roadmaps | New | Sin asignar | G10 - Sprint 03 | 0/4 |
| [[historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] Módulo graph en Neo4j y migración inicial | New | Sin asignar | G10 - Sprint 03 | 0/8 |
| [[historias/HT-19 Contratos con Courses y el Motor para el modelo 1 a N\|HT-19]] Contratos con Courses y el Motor para el modelo 1 a N | New | Sin asignar | G10 - Sprint 03 | 1/5 |
| [[historias/HT-20 Gate y progreso con reglas combinadas y XP mínimo\|HT-20]] Gate y progreso con reglas combinadas y XP mínimo | New | Sin asignar | G10 - Sprint 03 | 0/5 |
| [[historias/HU-57 Habilitar y gestionar varios roadmaps por curso\|HU-57]] Habilitar y gestionar varios roadmaps por curso | New | Sin asignar | G10 - Sprint 03 | 0/4 |
| [[historias/HU-58 Dependencias entre secciones\|HU-58]] Dependencias entre secciones | New | Sin asignar | G10 - Sprint 03 | 0/5 |
| [[historias/HU-59 Dependencias entre nodos con reglas combinadas\|HU-59]] Dependencias entre nodos con reglas combinadas | New | Sin asignar | G10 - Sprint 03 | 0/4 |
| [[historias/HU-61 Roadmaps por grupo del curso y restricciones de visualización\|HU-61]] Roadmaps por grupo del curso y restricciones de visualización | New | Sin asignar | G10 - Sprint 03 | 0/4 |
| [[historias/HU-62 Vista de grafo cómoda para el profesor\|HU-62]] Vista de grafo cómoda para el profesor | New | Sin asignar | G10 - Sprint 03 | 0/6 |
| [[historias/HU-71 Clonar un roadmap con sus restricciones\|HU-71]] Clonar un roadmap con sus restricciones | New | Sin asignar | G10 - Sprint 03 | 0/4 |
