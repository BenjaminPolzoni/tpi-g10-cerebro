---
tags: [tpi, g10, decision, neo4j]
fecha: 2026-10-17
estado: aceptada
reemplaza: ""
---

# DEC-021: Postgres es la fuente de verdad de la estructura y Neo4j es una proyección

> [!info] Precisa [[decisiones/DEC-016-neo4j-para-la-estructura-del-roadmap|DEC-016]]
> DEC-016 sigue vigente: la estructura se consulta en Neo4j. Lo que cambia es **dónde se escribe**. Reemplaza el punto 5 del diseño de [[sprints/sprint-3/04-base-de-grafos|04-base-de-grafos]] («escribir en Neo4j, luego registrar en Postgres») y la decisión D8 («quitar las claves foráneas de Postgres hacia `node` y `section` con T-18.6»). Acordada por el equipo el 2026-10-17.

## Contexto
T-18.6 decía que, con el flag de lectura encendido, las ediciones de estructura se escribían **solo en Neo4j**. No hay una transacción común entre Postgres y Neo4j: `GraphPersistenceConfig` declara dos administradores de transacciones separados. Con ese diseño:

- Una edición que falla a mitad de camino deja las dos bases distintas, y nada lo deshace.
- Desde que se enciende el flag, Postgres queda desactualizado. Si Neo4j falla, se rompe su volumen o hay que apagar el flag, se pierde todo lo editado mientras estuvo encendido.
- El estado del alumno (progreso, XP, vidas, intentos) sigue en Postgres y apunta a los UUID de secciones y nodos. Si las bases divergen, ese estado queda huérfano.

## Decisión
**Toda escritura de estructura va a Postgres** por la API de siempre, y **Neo4j se reconstruye desde Postgres**. Nadie escribe directo en Neo4j.

1. **Marca en la misma transacción.** Cada edición de estructura (sección, nodo, prerrequisito, regla, tipo de relación, posición) guarda en el mismo `@Transactional` una fila en `graph_sync_pending(roadmap_id, marked_at)`. O se guardan la edición y la marca, o ninguna.
2. **Proyección del roadmap entero.** Un proyector lee de Postgres el roadmap completo (secciones, nodos, relaciones, reglas, posiciones) y lo escribe en Neo4j con `MERGE` por UUID, dando de baja lógica en Neo4j lo que ya no está en Postgres. Es idempotente y no depende del orden de los eventos.
3. **Dos disparadores.** Un `@TransactionalEventListener(AFTER_COMMIT)` proyecta apenas se confirma la edición, y un `@Scheduled` toma las marcas pendientes y reintenta (por ejemplo, si Neo4j estaba caído). La marca se borra solo cuando la proyección termina bien.
4. **Reconstrucción y reconciliación.** El mismo proyector, corrido sobre todos los roadmaps, es la migración inicial (T-18.2) y la forma de rearmar Neo4j desde cero. La reconciliación (T-18.3) compara ids y cantidades entre las dos bases y marca para volver a proyectar los roadmaps que difieran.
5. **El flag de T-18.6 solo cambia de dónde se lee.** Con el flag encendido, el editor, el roadmap del alumno y la vista de grafo leen de Neo4j. Las escrituras siguen en Postgres. Apagar el flag vuelve a Postgres sin perder nada.
6. **El gate no lee de Neo4j sin caché.** Lee de Postgres o de la caché de reglas de T-18.4, que se invalida al confirmar la edición en Postgres, para no evaluar con una regla atrasada.

**Regla para todos:** todo dato nuevo del modelo de grafo (tipos de relación, visibilidad, subsecciones, inicio y fin, posiciones) se agrega **primero en Postgres** (migración Flyway y API), y después al proyector. Si un dato existe solo en Neo4j, el proyector lo borra en la siguiente proyección.

## Alternativas descartadas
- **Escribir solo en Neo4j con el flag encendido** (T-18.6 original): pierde datos si falla Neo4j o si se apaga el flag.
- **Escribir en las dos bases en la misma petición:** sin transacción común, un fallo entre las dos escrituras las deja distintas.
- **Transacción distribuida (XA / two-phase commit):** Neo4j Community no participa de XA y suma complejidad que no se justifica para este volumen.
- **Copia periódica completa sin marcas:** Neo4j quedaría atrasado hasta la siguiente corrida y se copiarían todos los roadmaps aunque no cambien.
- **Proyectar cambio por cambio (eventos de diferencia):** depende del orden y de no perder ningún evento. Copiar el roadmap entero es barato (decenas de nodos) y siempre converge.

## Consecuencias
- Positivas:
  - No se pierden datos de estructura: Neo4j siempre se puede rearmar desde Postgres.
  - El progreso del alumno nunca queda huérfano, porque los UUID salen siempre de Postgres y se conservan las claves foráneas.
  - Si Neo4j se cae, las ediciones siguen funcionando y la marca espera.
  - Encender y apagar el flag de lectura es seguro.
- Negativas / deuda:
  - Neo4j queda atrasado unos milisegundos después de cada edición, o más si Neo4j estaba caído. Quien lea de Neo4j justo después de guardar puede ver la versión anterior.
  - Postgres necesita columnas para todo lo que tiene el modelo de Neo4j. Faltaban las relaciones que no bloquean y los tipos ocultos: se agregó **T-65.5**, con tablas nuevas (`node_relation`, `section_relation`, `roadmap_hidden_relation_type`); `REQUIRES` sigue en las tablas de prerrequisitos, en [[sprints/sprint-3/historias/HU-65 Relaciones con tipo|HU-65]].
  - Se mantienen las tablas de estructura de Postgres y sus claves foráneas, así que D8 de [[sprints/sprint-3/04-base-de-grafos|04-base-de-grafos]] queda descartada.

## Qué cambia en las tareas
| Tarea | Cambio |
|---|---|
| [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|T-18.2]] | El job de migración es el proyector, corrido sobre todos los roadmaps. Se reutiliza para mantener Neo4j al día y para rearmarlo |
| [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|T-18.3]] | Tabla `graph_sync_pending`, proyector por roadmap, reintentos y reconciliación |
| [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|T-18.4]] | La caché se invalida al confirmar la edición en Postgres |
| [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|T-18.6]] | El flag solo cambia de dónde se lee. Las escrituras siguen en Postgres |
| [[sprints/sprint-3/historias/HU-65 Relaciones con tipo\|T-65.5]] (nueva) | Tablas nuevas para los 4 tipos que no bloquean y los tipos ocultos, y API única `/roadmaps/{roadmapId}/relations` (un `requires` se delega al editor de prerrequisitos) |
| [[sprints/sprint-3/historias/HU-62 Vista de grafo cómoda para el profesor\|T-62.2]] | Las posiciones se guardan en Postgres (`node.position_x` y `node.position_y`, V23) |
| [[sprints/sprint-3/historias/HU-62 Vista de grafo cómoda para el profesor\|T-62.3]] | Crear y borrar relaciones arrastrando usa `/roadmaps/{roadmapId}/relations` (T-65.5), no una ruta que escriba en Neo4j |
| [[sprints/sprint-3/historias/HU-64 Nodos de inicio y fin obligatorios\|HU-64]], HU-58, HU-59 | Se implementan sobre Postgres. El proyector los copia a Neo4j |

## Referencias
- Código: `tpi-roadmap/src/main/java/com/utn/tpi/roadmap/graph/config/GraphPersistenceConfig.java` (dos administradores de transacciones), `events/outbox/OutboxPoller.java` (mismo patrón de tabla pendiente + `@Scheduled`), `db/migration/V23__node_editor_fields.sql` (posiciones), `V5__node_prerequisite.sql` y `V25__section_prerequisite.sql` (sin tipo de relación).
- [[decisiones/DEC-002-outbox-transaccional-eventos-salientes|DEC-002]] (outbox transaccional), [[decisiones/DEC-005-baja-logica-sin-borrar-progreso|DEC-005]] (baja lógica), [[decisiones/DEC-016-neo4j-para-la-estructura-del-roadmap|DEC-016]], [[decisiones/DEC-018-catalogo-de-relaciones-y-tipos-de-nodo|DEC-018]].
- Taiga: [T-65.5 #10591](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/10591).
