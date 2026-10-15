---
tags: [tpi, g10, sprint-3, epica]
estado: Propuesta
sprint: "G10 - Sprint 3"
historias: 11
puntos: 65
---

# Múltiples roadmaps por curso y grafo configurable

> [!info] Épica del Sprint 3 · **11 historias** · **65 pts** · Estado: **Propuesta** (todavía no está en Taiga).

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
*   Restricciones (legales/técnicas): Módulo `graph` dentro de roadmap-service, no un micro nuevo. UUID compartidos y solo baja lógica. Bloqueada en parte por P1 a P4 de las dudas.

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

| HU | Título | En Taiga | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/HT-16 Validar la infra de Neo4j y modelar las relaciones\|HT-16]] | Validar la infra de Neo4j y modelar las relaciones | Nueva | 3 | Must | — | [[sprints/sprint-3/08-dudas\|G1]] ✅, [[sprints/sprint-3/08-dudas\|P1]] ✅, [[sprints/sprint-3/08-dudas\|P4]] ✅ |
| [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]] | Modelo 1 a N de curso a roadmaps | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-16 Validar la infra de Neo4j y modelar las relaciones\|HT-16]] | [[sprints/sprint-3/08-dudas\|P1]] ✅, [[sprints/sprint-3/08-dudas\|P2]] ✅, [[sprints/sprint-3/08-dudas\|P3]] ✅ |
| [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | Módulo graph en Neo4j y migración inicial | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-16 Validar la infra de Neo4j y modelar las relaciones\|HT-16]] | [[sprints/sprint-3/08-dudas\|P1]] ✅, [[sprints/sprint-3/08-dudas\|P4]] ✅, [[sprints/sprint-3/08-dudas\|P8]] ✅ |
| [[sprints/sprint-3/historias/HU-57 Habilitar y gestionar varios roadmaps por curso\|HU-57]] | Habilitar y gestionar varios roadmaps por curso | Nueva | 5 | Should | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]] | [[sprints/sprint-3/08-dudas\|P1]] ✅ |
| [[sprints/sprint-3/historias/HU-58 Dependencias entre secciones\|HU-58]] | Dependencias entre secciones | Nueva | 5 | Must | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]], [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]], [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas\|HU-59]] | [[sprints/sprint-3/08-dudas\|P6]] ✅ |
| [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas\|HU-59]] | Dependencias entre nodos con reglas combinadas | Nueva | 5 | Must | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]], [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | [[sprints/sprint-3/08-dudas\|P7]] ✅ |
| [[sprints/sprint-3/historias/HU-61 Roadmaps por grupo del curso y restricciones de visualización\|HU-61]] | Roadmaps por grupo del curso y restricciones de visualización | Nueva | 5 | Should | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]] | [[sprints/sprint-3/08-dudas\|P1]] ✅, [[sprints/sprint-3/08-dudas\|P2]] ✅, [[sprints/sprint-3/08-dudas\|P5]] ✅ |
| [[sprints/sprint-3/historias/HU-62 Vista de grafo cómoda para el profesor\|HU-62]] | Vista de grafo cómoda para el profesor | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]], [[sprints/sprint-3/historias/HT-34 Componente de grafo en la UI-KIT\|HT-34]], [[sprints/sprint-3/historias/HU-65 Relaciones con tipo\|HU-65]] | [[sprints/sprint-3/08-dudas\|G13]] ✅ |
| [[sprints/sprint-3/historias/HT-19 Contratos con Courses y el Motor para el modelo 1 a N\|HT-19]] | Contratos con Courses y el Motor para el modelo 1 a N | Nueva | 5 | Must | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]] | [[sprints/sprint-3/08-dudas\|P3]] ✅, [[sprints/sprint-3/08-dudas\|G4]] ✅, [[sprints/sprint-3/08-dudas\|G8]] ✅ |
| [[sprints/sprint-3/historias/HT-20 Gate y progreso con reglas combinadas y XP mínimo\|HT-20]] | Gate y progreso con reglas combinadas y XP mínimo | Nueva | 5 | Must | [[sprints/sprint-3/historias/HU-58 Dependencias entre secciones\|HU-58]], [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas\|HU-59]] | [[sprints/sprint-3/08-dudas\|P7]] ✅ |
| [[sprints/sprint-3/historias/HU-71 Clonar un roadmap con sus restricciones\|HU-71]] | Clonar un roadmap con sus restricciones | Nueva | 8 | Should | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]], [[sprints/sprint-3/historias/HU-57 Habilitar y gestionar varios roadmaps por curso\|HU-57]] | [[sprints/sprint-3/08-dudas\|G4]] ✅, [[sprints/sprint-3/08-dudas\|P17]] |

---

## Origen (no va a Taiga)

[[sprints/sprint-3/03-requerimientos-profes|03-requerimientos-profes]], [[sprints/sprint-3/04-base-de-grafos|04-base-de-grafos]], [[decisiones/DEC-016-neo4j-para-la-estructura-del-roadmap|DEC-016]]
