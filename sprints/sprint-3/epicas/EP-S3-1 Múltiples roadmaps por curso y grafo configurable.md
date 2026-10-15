---
tags: [tpi, g10, sprint-3, epica]
id: EP-S3-1
estado: Propuesta
historias: 12
puntos: 68
---

# EP-S3-1: Múltiples roadmaps por curso y grafo configurable

> [!info] Épica propuesta del Sprint 3. **12 historias**, **68 pts**. Todavía no está en Taiga.
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Objetivo* hasta *Dependencias / Impactos*.

**[G10] — Múltiples roadmaps por curso y grafo configurable**

* * *

## Objetivo

Que un curso pueda tener uno o más roadmaps, con secciones y nodos relacionados por reglas configurables, guardados en Neo4j y editables desde dos vistas (Moodle y grafo).

* * *

## Suposiciones y Restricciones

- Suposiciones: Neo4j es pedido de los profes (DEC-016). Ya existen dependencias AND/OR entre secciones (V25) y entre nodos (V5/V7). El estado del alumno se queda en Postgres.
- Restricciones (legales/técnicas): Módulo `graph` dentro de roadmap-service, no un micro nuevo. UUID compartidos y solo baja lógica. Bloqueada en parte por P1 a P4 de las dudas.

* * *

## Criterios de Aceptación a nivel Épico

- [ ] Un curso de demo tiene 2 roadmaps y el alumno recorre cada uno con su progreso.
- [ ] El profesor define dependencias entre secciones y entre nodos (AND/OR, XP mínimo, reglas combinadas) y el gate las respeta.
- [ ] La estructura vive en Neo4j y el estado del alumno sigue en Postgres, con los mismos UUID.
- [ ] Las dos vistas del profesor editan el mismo roadmap y se mantienen sincronizadas.
- [ ] KPIs iniciales: Un curso de demo con 2 roadmaps recorrido de punta a punta. P95 del gate por debajo de 200 ms.
- [ ] Sin regresiones críticas: Las rutas `/courses/{id}/...` siguen funcionando mientras el front migra. Los tests existentes del gate y del progreso pasan.
- [ ] Observabilidad y alertas: Latencia del gate y del endpoint `/graph`; alerta por ids huérfanos entre Neo4j y Postgres.
- [ ] Documentación publicada: Modelo del grafo, endpoints nuevos en OpenAPI y contratos con G01/G09 actualizados.

* * *

## Dependencias / Impactos

- Servicios / APIs: Neo4j (nuevo), Courses, Motor.
- Módulos afectados: Módulo `graph`, gate, progreso, editor del profesor (vista Moodle y grafo), roadmap del alumno.
- Otros equipos: Plataforma (infra de Neo4j), G01 (secciones), G09 (eventos), equipo UI-KIT (componente de grafo).
- Impacto en datos / migraciones: Grafo nuevo en Neo4j con migración inicial desde Postgres; se quita el UNIQUE de `roadmap.course_cohort_id`.
- Feature toggles / flags: Flag de lectura desde Neo4j durante la convivencia; `multiple_roadmaps_allowed` por curso.

---

## Historias

| ID | Tipo | Título | Capa | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/M01 Validar la infra de Neo4j y modelar las relaciones\|M01]] | Spike | Validar la infra de Neo4j y modelar las relaciones | Back + Infra | 3 | Must | — | [[sprints/sprint-3/08-dudas\|G1]], [[sprints/sprint-3/08-dudas\|P1]], [[sprints/sprint-3/08-dudas\|P4]] |
| [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps\|M02]] | HT | Modelo 1 a N de curso a roadmaps | Back | 8 | Must | [[sprints/sprint-3/historias/M01 Validar la infra de Neo4j y modelar las relaciones\|M01]] | [[sprints/sprint-3/08-dudas\|P1]], [[sprints/sprint-3/08-dudas\|P2]], [[sprints/sprint-3/08-dudas\|P3]] |
| [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial\|M03]] | HT | Módulo graph en Neo4j y migración inicial | Back | 8 | Must | [[sprints/sprint-3/historias/M01 Validar la infra de Neo4j y modelar las relaciones\|M01]] | [[sprints/sprint-3/08-dudas\|P1]], [[sprints/sprint-3/08-dudas\|P4]], [[sprints/sprint-3/08-dudas\|P8]] |
| [[sprints/sprint-3/historias/M04 Habilitar y gestionar varios roadmaps por curso\|M04]] | HU | Habilitar y gestionar varios roadmaps por curso | Back + Front | 5 | Should | [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps\|M02]] | [[sprints/sprint-3/08-dudas\|P1]] |
| [[sprints/sprint-3/historias/M05 Dependencias entre secciones\|M05]] | HU | Dependencias entre secciones | Back + Front | 5 | Must | [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps\|M02]], [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial\|M03]] | [[sprints/sprint-3/08-dudas\|P6]] |
| [[sprints/sprint-3/historias/M06 Dependencias entre nodos con reglas combinadas\|M06]] | HU | Dependencias entre nodos con reglas combinadas | Back + Front | 5 | Should | [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps\|M02]], [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial\|M03]] | [[sprints/sprint-3/08-dudas\|P7]] |
| [[sprints/sprint-3/historias/M07 Propiedades personalizadas en nodos y secciones\|M07]] | HU | Propiedades personalizadas en nodos y secciones | Back + Front | 3 | Could | [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial\|M03]] | [[sprints/sprint-3/08-dudas\|P8]] |
| [[sprints/sprint-3/historias/M08 El alumno elige qué roadmap recorrer\|M08]] | HU | El alumno elige qué roadmap recorrer | Back + Front | 5 | Should | [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps\|M02]] | [[sprints/sprint-3/08-dudas\|P1]], [[sprints/sprint-3/08-dudas\|P2]], [[sprints/sprint-3/08-dudas\|P5]] |
| [[sprints/sprint-3/historias/M09 Vista de grafo cómoda para el profesor\|M09]] | HU | Vista de grafo cómoda para el profesor | Front (+ Back) | 8 | Must | [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps\|M02]], [[sprints/sprint-3/historias/U06 Componente de grafo en la UI-KIT\|U06]] | [[sprints/sprint-3/08-dudas\|G13]] |
| [[sprints/sprint-3/historias/M10 Vista tipo Moodle con la UI-KIT\|M10]] | HU | Vista tipo Moodle con la UI-KIT | Front | 8 | Should | [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]], [[sprints/sprint-3/historias/U02 Controles y botones del roadmap con el kit\|U02]] | [[sprints/sprint-3/08-dudas\|P1]] |
| [[sprints/sprint-3/historias/M11 Contratos con Courses y el Motor para el modelo 1 a N\|M11]] | HT | Contratos con Courses y el Motor para el modelo 1 a N | Back | 5 | Must | [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps\|M02]] | [[sprints/sprint-3/08-dudas\|P3]], [[sprints/sprint-3/08-dudas\|G4]], [[sprints/sprint-3/08-dudas\|G8]] |
| [[sprints/sprint-3/historias/M12 Gate y progreso con reglas combinadas y XP mínimo\|M12]] | HT | Gate y progreso con reglas combinadas y XP mínimo | Back | 5 | Must | [[sprints/sprint-3/historias/M05 Dependencias entre secciones\|M05]], [[sprints/sprint-3/historias/M06 Dependencias entre nodos con reglas combinadas\|M06]] | [[sprints/sprint-3/08-dudas\|P7]] |

## Origen

[[sprints/sprint-3/03-requerimientos-profes|03-requerimientos-profes]], [[sprints/sprint-3/04-base-de-grafos|04-base-de-grafos]], [[decisiones/DEC-016-neo4j-para-la-estructura-del-roadmap|DEC-016]]
