---
tags: [tpi, g10, taiga, ht]
codigo: HT-18
ref: 8601
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8601
---

# HT-18: Módulo graph en Neo4j y migración inicial

> [!info] Generado desde Taiga (2026-10-15 16:54). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8601) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Tareas cerradas: **0/8**

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

*   [ ] Reglas de negocio: Módulo `graph` dentro de roadmap-service. La app genera los UUID y las dos bases los comparten. Solo baja lógica en Neo4j. Las ediciones se registran en `node_edit_log` y salen por el outbox de Postgres. Con el flag de lectura encendido, Neo4j manda en la estructura (secciones, nodos, relaciones y reglas) y Postgres queda con el estado del alumno, `node_edit_log` y el outbox.
*   [ ] Validaciones: Constraints de unicidad por `id`. Job de reconciliación de ids huérfanos. Se rechazan con 400 las propiedades libres y los tipos de nodo fuera del catálogo (DEC-018).
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): El gate lee las reglas desde una caché por roadmap que se invalida en cada edición. La medición del P95 del gate está en HT-20.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: Migración inicial idempotente detrás de un flag; hasta encender el flag de lectura la estructura se lee de Postgres; con el flag encendido se lee de Neo4j (T-18.6). Esquema cerrado (DEC-018): 5 tipos de relación, tipos de nodo fijos sin propiedades libres, y subsecciones. Solo se migran los grafos (G1).

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Módulo `graph` con Spring Data Neo4j y esquema versionado (`neo4j-migrations`).
*   [ ] **CA2**: Job de migración inicial desde Postgres, idempotente.
*   [ ] **CA3**: Caché de reglas por roadmap para el gate.
*   [ ] **CA4**: `GET /roadmaps/{id}/graph` devuelve `{nodes, edges, layout}`.
*   [ ] **CA5**: Tests con Testcontainers.
*   [ ] **CA6**: Con el flag de lectura encendido, el gate, el editor y el roadmap del alumno leen la estructura de Neo4j, y las ediciones de estructura (HU-58, HU-59, HU-64, HU-65) se escriben solo en Neo4j.
*   [ ] **CA7**: El back rechaza con 400 propiedades libres y tipos de nodo fuera del catálogo (DEC-018).

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

**Escenario 4**

*   **Dado**: el flag de lectura encendido
*   **Cuando**: el profesor cambia una regla de un nodo
*   **Entonces**: el gate evalúa la regla nueva leyéndola de Neo4j

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
*   Impacto en datos / migraciones: Grafo nuevo en Neo4j. Postgres no cambia de esquema: `node_edit_log` y el outbox siguen recibiendo cada edición, y las tablas de estructura dejan de escribirse cuando se enciende el flag de lectura.
*   Riesgos y mitigación (opcional): Inconsistencia entre bases; mitigación: ids compartidos, baja lógica y reconciliación.


## Tareas

- [ ] #8939 T-18.1 Crear el módulo graph y su esquema en Neo4j · New · Iker Alonso
- [ ] #8940 T-18.2 Pasar la estructura actual de Postgres a Neo4j · New · Iker Alonso
- [ ] #8942 T-18.3 Mantener las dos bases en orden · New · Iker Alonso
- [ ] #8944 T-18.4 Caché de reglas por roadmap para el gate · New · Iker Alonso
- [ ] #8945 T-18.5 Endpoint que devuelve el grafo entero para dibujarlo · New · Iker Alonso
- [ ] #9274 T-18.6 Pasar la lectura de la estructura a Neo4j · New · Iker Alonso
- [ ] #9275 T-18.7 Rechazar campos libres y tipos de nodo fuera del catálogo · New · Iker Alonso
- [ ] #9337 T-18.8 Wiki, OpenAPI y diagrama de secuencia · New · Quinteros Tomás
