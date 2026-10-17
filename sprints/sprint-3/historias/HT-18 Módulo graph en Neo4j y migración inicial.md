---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-18
estado: New
responsable: "Sin asignar"
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Must
en_taiga: true
ref: 8601
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8601
responsables_tareas: ["Iker Alonso", "Quinteros Tomás"]
tareas_cerradas: "0/8"
---

# HT-18: Módulo graph en Neo4j y migración inicial

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **0/8** · Sprint: **G10 - Sprint 3**
> Cargada en Taiga: [[taiga/historias/HT-18 Módulo graph en Neo4j y migración inicial|HT-18]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8601)) · Épica en Taiga: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]] (7), [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]] (1). El 2026-10-15 suma el corte de lectura a Neo4j (qué base manda) y la validación del esquema cerrado que estaba en HU-60.

> [!warning] 2026-10-17 · Cambio de diseño acordado: [[decisiones/DEC-021-postgres-fuente-de-verdad-neo4j-proyeccion|DEC-021]]
> **Postgres es la fuente de verdad de la estructura y Neo4j es una proyección.** Toda escritura va a Postgres por la API de siempre, se marca en `graph_sync_pending` en la misma transacción, y un proyector copia el roadmap entero a Neo4j. El flag de T-18.6 solo cambia de dónde se lee. Donde esta nota o Taiga digan que las ediciones «se escriben solo en Neo4j», manda DEC-021.

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

*   [ ] Reglas de negocio: Módulo `graph` dentro de roadmap-service. La app genera los UUID y las dos bases los comparten. Solo baja lógica en Neo4j. Las ediciones se escriben en Postgres, se registran en `node_edit_log`, salen por el outbox y dejan una marca en `graph_sync_pending`. Un proyector copia el roadmap a Neo4j (DEC-021). Postgres manda siempre en la estructura; con el flag de lectura encendido, la estructura se lee de Neo4j.
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
*   [ ] **CA2**: Proyector idempotente de Postgres a Neo4j: copia un roadmap después de cada edición, reintenta las marcas pendientes y, corrido sobre todos los roadmaps, hace la migración inicial y la reconstrucción.
*   [ ] **CA3**: Caché de reglas por roadmap para el gate.
*   [ ] **CA4**: `GET /roadmaps/{id}/graph` devuelve `{nodes, edges, layout}`.
*   [ ] **CA5**: Tests con Testcontainers.
*   [ ] **CA6**: Con el flag de lectura encendido, el editor, el roadmap del alumno y la vista de grafo leen la estructura de Neo4j, y el gate la lee de la caché de reglas. Las ediciones de estructura (HU-58, HU-59, HU-64, HU-65) se siguen escribiendo en Postgres, y apagar el flag no pierde ninguna (DEC-021).
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
*   **Entonces**: la regla se guarda en Postgres, se proyecta a Neo4j y el gate evalúa la regla nueva en la siguiente consulta

**Escenario 5**  

*   **Dado**: Neo4j caído
*   **Cuando**: el profesor edita un nodo
*   **Entonces**: la edición se guarda en Postgres, queda marcada como pendiente y se proyecta cuando Neo4j vuelve

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
*   Impacto en datos / migraciones: Grafo nuevo en Neo4j, rearmable desde Postgres. Postgres suma la tabla `graph_sync_pending`; las tablas de estructura y sus claves foráneas se mantienen y se siguen escribiendo siempre (DEC-021).
*   Riesgos y mitigación (opcional): Inconsistencia entre bases; mitigación: una sola base de escritura (Postgres), proyección idempotente por roadmap, reintentos, reconciliación, ids compartidos y baja lógica.

## Tareas

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **0/8**. Historia en Taiga: [[taiga/historias/HT-18 Módulo graph en Neo4j y migración inicial|HT-18]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8601)

- [ ] [#8939](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/8939) **T-18.1 Crear el módulo graph y su esquema en Neo4j** · Back · New · [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]]
    - **Qué:** paquete `graph` dentro de roadmap-service con las entidades de Spring Data Neo4j del modelo de HT-16 (roadmap, sección, nodo, relaciones con tipo, reglas) y el esquema versionado con `neo4j-migrations` (unicidad por `id`).
    - **Listo cuando:** la app arranca contra Neo4j, el esquema se aplica solo y hay tests con Testcontainers de guardar y leer.
- [ ] [#8940](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/8940) **T-18.2 Pasar la estructura actual de Postgres a Neo4j** · Back · New · [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]]
    - **Qué:** proyector que lee de Postgres un roadmap entero (`section`, `node`, `node_prerequisite`, `section_prerequisite`, reglas, tipos de relación y posiciones) y lo escribe en Neo4j con `MERGE` por los mismos UUID, dando de baja lógica lo que ya no está. Corrido sobre todos los roadmaps es la migración inicial y la reconstrucción de Neo4j; T-18.3 lo reutiliza para cada edición (DEC-021). Va detrás de un flag; hasta que se pase la lectura (T-18.6) la estructura se sigue leyendo de Postgres.
    - **Necesita:** T-65.5 (tipo de relación en Postgres) y, para la corrida final, T-64.3 (inicio y fin en los roadmaps existentes).
    - **Listo cuando:** correrlo dos veces deja el mismo grafo, borrar Neo4j y correrlo lo rearma igual, y un reporte compara cantidades de nodos y relaciones entre las dos bases.
- [ ] [#8942](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/8942) **T-18.3 Mantener las dos bases en orden** · Back · New · [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]]
    - **Qué:** cada edición de estructura se escribe en Postgres, se registra en `node_edit_log`, sale por el outbox como hoy y deja una marca en `graph_sync_pending(roadmap_id, marked_at)` en la misma transacción. Un `@TransactionalEventListener(AFTER_COMMIT)` proyecta el roadmap con el proyector de T-18.2, y un `@Scheduled` reintenta las marcas pendientes. La marca se borra solo si la proyección termina bien. Solo baja lógica en Neo4j. Un job de reconciliación compara ids y cantidades y vuelve a marcar los roadmaps que difieran (DEC-021).
    - **Listo cuando:** editar un nodo deja su log, su evento y su marca; con Neo4j caído la edición se guarda igual y se proyecta al volver; y el job reporta y corrige las diferencias de una base de prueba.
- [ ] [#8944](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/8944) **T-18.4 Caché de reglas por roadmap para el gate** · Back · New · [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]]
    - **Qué:** `GateEvaluator` lee las reglas de una caché por roadmap que se invalida cuando se confirma una edición en Postgres, para no ir a Neo4j en cada pedido del Motor ni evaluar con una regla atrasada (DEC-021).
    - **Listo cuando:** una regla editada se aplica en la siguiente consulta del gate. La medición del P95 se hace en HT-20 (T-20.4).
- [ ] [#8945](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/8945) **T-18.5 Endpoint que devuelve el grafo entero para dibujarlo** · Back · New · [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]]
    - **Qué:** `GET /roadmaps/{id}/graph` con `{nodes, edges, layout}`: nodos con tipo y posición, aristas con tipo y visibilidad. Documentado en OpenAPI.
    - **Listo cuando:** el front dibuja el grafo completo con una sola llamada y hay test del contrato.
- [ ] [#9274](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9274) **T-18.6 Pasar la lectura de la estructura a Neo4j** · Back · New · [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]]
    - **Qué:** flag de lectura. Con el flag encendido, el editor, el roadmap del alumno y la vista de grafo leen secciones, nodos, relaciones y reglas de Neo4j, y el gate las lee de la caché de T-18.4. Las ediciones de estructura se siguen escribiendo **solo en Postgres** (con `node_edit_log`, su evento en el outbox y su marca en `graph_sync_pending`) y el proyector las copia a Neo4j. Con el flag apagado todo se lee de Postgres (DEC-021).
    - **Listo cuando:** hay tests con el flag encendido y apagado, apagar el flag no pierde ninguna edición, y la reconciliación (T-18.3) no reporta diferencias antes de encenderlo en la demo.
- [ ] [#9275](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9275) **T-18.7 Rechazar campos libres y tipos de nodo fuera del catálogo** · Back · New · [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]]
    - **Qué:** el esquema es cerrado (P8, DEC-018): el back rechaza con 400 propiedades que no son del modelo y tipos de nodo que no están en el catálogo. Lo personalizable es nombre, ícono, descripción y reglas.
    - **Dónde:** módulo `graph`, `NodeController`.
    - **Listo cuando:** hay tests de lo permitido y lo rechazado.
- [ ] [#9337](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9337) **T-18.8 Wiki, OpenAPI y diagrama de secuencia** · New · [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]]
    - Tarea de documentación agregada en Taiga por el equipo; no estaba en la propuesta.

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
