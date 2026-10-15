---
tags: [tpi, g10, sprint-3, historia, ht]
id: M03
tipo: HT
epica: "EP-S3-1"
capa: "Back"
esfuerzo: L
puntos: 8
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M01]
---

# M03: Módulo graph en Neo4j y migración inicial

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HT** · Capa: **Back** · **8 pts** · **Must** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HT-xx — Módulo graph en Neo4j y migración inicial** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: EQUIPO DE DESARROLLO
- **Quiero**: guardar la estructura del roadmap en Neo4j y dejar el estado del alumno en Postgres
- **Para**: modelar relaciones y reglas configurables como pidieron los profes

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Módulo `graph` dentro de roadmap-service. La app genera los UUID y las dos bases los comparten. Solo baja lógica en Neo4j. Las ediciones se registran en `node_edit_log` y salen por el outbox de Postgres.
- [ ] Validaciones: Constraints de unicidad por `id`. Job de reconciliación de ids huérfanos.
- [ ] Performance (tiempos, volumen, límites): El gate lee las reglas desde una caché por roadmap que se invalida en cada edición.
- [ ] Otros: Migración inicial idempotente detrás de un flag; durante la convivencia la lectura sigue en Postgres.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Módulo `graph` con Spring Data Neo4j y esquema versionado (`neo4j-migrations`).
- [ ] **CA2**: Job de migración inicial desde Postgres, idempotente.
- [ ] **CA3**: Caché de reglas por roadmap para el gate.
- [ ] **CA4**: `GET /roadmaps/{id}/graph` devuelve `{nodes, edges, layout}`.
- [ ] **CA5**: Tests con Testcontainers.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Estructura en Neo4j

**Escenario 1**

- **Dado**: un roadmap en Postgres
- **Cuando**: corre el job de migración
- **Entonces**: Neo4j tiene las mismas secciones, nodos y prerrequisitos con los mismos UUID

**Escenario 2**

- **Dado**: el job ya corrido
- **Cuando**: corre otra vez
- **Entonces**: no duplica nada

**Escenario 3**

- **Dado**: un roadmap migrado
- **Cuando**: se pide `/roadmaps/{id}/graph`
- **Entonces**: devuelve nodos, aristas y layout

* * *

## Prototipo

- **Capturas**: No aplica.
- **URL Figma**: No aplica.
- **Storybook**: No aplica.
- **Mock API / Swagger**: GET /api/roadmap/roadmaps/{roadmapId}/graph → {nodes, edges, layout}.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 8
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Neo4j (nuevo).
- Módulos afectados: Módulo `graph`, `GateService`, `GateEvaluator`, outbox.
- Otros equipos / aprobaciones: Plataforma (infra).
- Impacto en datos / migraciones: Grafo nuevo en Neo4j; Postgres sin cambios.
- Riesgos y mitigación (opcional): Inconsistencia entre bases; mitigación: ids compartidos, baja lógica y reconciliación.

## Tareas

- [ ] T-M03.1 Módulo `graph` y esquema
- [ ] T-M03.2 Job de migración inicial
- [ ] T-M03.3 Caché de reglas para el gate
- [ ] T-M03.4 Endpoint `/graph`
- [ ] T-M03.5 Tests con Testcontainers

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

Todo está en Postgres (`section`, `node`, `section_prerequisite`, `node_prerequisite`).

### Depende de

- [[sprints/sprint-3/historias/M01 Validar la infra de Neo4j y modelar las relaciones|M01]] Validar la infra de Neo4j y modelar las relaciones

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P1]]
- [[sprints/sprint-3/08-dudas|P4]]
- [[sprints/sprint-3/08-dudas|P8]]
