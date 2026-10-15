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
> Nueva: todavía no está cargada en Taiga. El 2026-10-15 suma el corte de lectura a Neo4j (qué base manda) y la validación del esquema cerrado que estaba en HU-60.

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

- [ ] **T-18.1 Crear el módulo `graph` y su esquema en Neo4j** · Back
    - **Qué:** paquete `graph` dentro de roadmap-service con las entidades de Spring Data Neo4j del modelo de HT-16 (roadmap, sección, nodo, relaciones con tipo, reglas) y el esquema versionado con `neo4j-migrations` (unicidad por `id`).
    - **Listo cuando:** la app arranca contra Neo4j, el esquema se aplica solo y hay tests con Testcontainers de guardar y leer.
- [ ] **T-18.2 Pasar la estructura actual de Postgres a Neo4j** · Back
    - **Qué:** job que lee `section`, `node`, `node_prerequisite` y `section_prerequisite` y arma el grafo con los mismos UUID. Va detrás de un flag; hasta que se pase la lectura (T-18.6) la estructura se sigue leyendo de Postgres.
    - **Listo cuando:** correrlo dos veces deja el mismo grafo y un reporte compara cantidades de nodos y relaciones entre las dos bases.
- [ ] **T-18.3 Mantener las dos bases en orden** · Back
    - **Qué:** cada cambio del grafo se registra en `node_edit_log` y sale por el outbox de Postgres como hoy; solo baja lógica en Neo4j; un job de reconciliación detecta ids que existen en una base y no en la otra.
    - **Listo cuando:** editar un nodo deja su log y su evento, y el job reporta los huérfanos de una base de prueba.
- [ ] **T-18.4 Caché de reglas por roadmap para el gate** · Back
    - **Qué:** `GateEvaluator` lee las reglas de una caché por roadmap que se invalida en cada edición, para no ir a Neo4j en cada pedido del Motor.
    - **Listo cuando:** una regla editada se aplica en la siguiente consulta del gate. La medición del P95 se hace en HT-20 (T-20.4).
- [ ] **T-18.5 Endpoint que devuelve el grafo entero para dibujarlo** · Back
    - **Qué:** `GET /roadmaps/{id}/graph` con `{nodes, edges, layout}`: nodos con tipo y posición, aristas con tipo y visibilidad. Documentado en OpenAPI.
    - **Listo cuando:** el front dibuja el grafo completo con una sola llamada y hay test del contrato.
- [ ] **T-18.6 Pasar la lectura de la estructura a Neo4j** · Back
    - **Qué:** flag de lectura: con el flag encendido, el gate, el editor y el roadmap del alumno leen secciones, nodos, relaciones y reglas de Neo4j, y las ediciones de estructura se escriben solo ahí (siguen dejando `node_edit_log` y su evento en el outbox). Con el flag apagado todo sigue en Postgres.
    - **Listo cuando:** hay tests con el flag encendido y apagado, y la reconciliación (T-18.3) no reporta diferencias antes de encenderlo en la demo.
- [ ] **T-18.7 Rechazar campos libres y tipos de nodo fuera del catálogo** · Back
    - **Qué:** el esquema es cerrado (P8, DEC-018): el back rechaza con 400 propiedades que no son del modelo y tipos de nodo que no están en el catálogo. Lo personalizable es nombre, ícono, descripción y reglas.
    - **Dónde:** módulo `graph`, `NodeController`.
    - **Listo cuando:** hay tests de lo permitido y lo rechazado.

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
