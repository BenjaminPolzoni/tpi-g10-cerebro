---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-18
estado: Propuesta
responsable: ""
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Must
en_taiga: false
---

# HT-18: Módulo graph en Neo4j y migración inicial

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HT-18 — Módulo graph en Neo4j y migración inicial
---------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: guardar la estructura del roadmap en Neo4j y dejar el estado del alumno en Postgres
*   **Para**: modelar relaciones y reglas configurables como pidieron los profes

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Módulo `graph` dentro de roadmap-service. La app genera los UUID y las dos bases los comparten. Solo baja lógica en Neo4j. Las ediciones se registran en `node_edit_log` y salen por el outbox de Postgres.
*   [ ] Validaciones: Constraints de unicidad por `id`. Job de reconciliación de ids huérfanos.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): El gate lee las reglas desde una caché por roadmap que se invalida en cada edición.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: Migración inicial idempotente detrás de un flag; durante la convivencia la lectura sigue en Postgres. Esquema cerrado (DEC-018): 5 tipos de relación, tipos de nodo fijos sin propiedades libres, y subsecciones. Solo se migran los grafos (G1).

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Módulo `graph` con Spring Data Neo4j y esquema versionado (`neo4j-migrations`).
*   [ ] **CA2**: Job de migración inicial desde Postgres, idempotente.
*   [ ] **CA3**: Caché de reglas por roadmap para el gate.
*   [ ] **CA4**: `GET /roadmaps/{id}/graph` devuelve `{nodes, edges, layout}`.
*   [ ] **CA5**: Tests con Testcontainers.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Estructura en Neo4j

**Escenario 1**  

*   **Dado**: un roadmap en Postgres
*   **Cuando**: corre el job de migración
*   **Entonces**: Neo4j tiene las mismas secciones, nodos y prerrequisitos con los mismos UUID

**Escenario 2**  

*   **Dado**: el job ya corrido
*   **Cuando**: corre otra vez
*   **Entonces**: no duplica nada

**Escenario 3**  

*   **Dado**: un roadmap migrado
*   **Cuando**: se pide `/roadmaps/{id}/graph`
*   **Entonces**: devuelve nodos, aristas y layout

* * *

Prototipo
---------

*   **Capturas**: No aplica.
*   **URL Figma**: No aplica.
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: GET /api/roadmap/roadmaps/{roadmapId}/graph → {nodes, edges, layout}.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 8 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Neo4j (nuevo).
*   Módulos afectados: Módulo `graph`, `GateService`, `GateEvaluator`, outbox.
*   Otros equipos / aprobaciones: Plataforma (infra).
*   Impacto en datos / migraciones: Grafo nuevo en Neo4j; Postgres sin cambios.
*   Riesgos y mitigación (opcional): Inconsistencia entre bases; mitigación: ids compartidos, baja lógica y reconciliación.

## Tareas

- [ ] T-18.1 Módulo `graph` y esquema
- [ ] T-18.2 Job de migración inicial
- [ ] T-18.3 Caché de reglas para el gate
- [ ] T-18.4 Endpoint `/graph`
- [ ] T-18.5 Tests con Testcontainers

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Todo está en Postgres (`section`, `node`, `section_prerequisite`, `node_prerequisite`).

### Depende de

- [[sprints/sprint-3/historias/HT-16 Validar la infra de Neo4j y modelar las relaciones|HT-16]] Validar la infra de Neo4j y modelar las relaciones

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P1]] Cada roadmap es un mapa distinto del mismo curso.
- ✅ [[sprints/sprint-3/08-dudas|P4]] 5 tipos de relación; solo `requires` afecta el desbloqueo.
- ✅ [[sprints/sprint-3/08-dudas|P8]] Sin campos libres ni tipos de nodo nuevos: se personalizan nombre, ícono, descripción y reglas.
