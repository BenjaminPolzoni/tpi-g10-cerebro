---
tags: [tpi, g10, sprint-4, plan, back, roadmap, neo4j, gate, grafo]
fecha: 2026-10-27
autor: Benjamin Polzoni
estado: borrador
repo: 2026-P4-BE/tpi-roadmap
base: origin/develop fea2fece (2026-10-27)
antecedentes: HT-18 (T-18.3 copia, T-18.4 caché del gate, T-18.6 lectura), DEC-016, DEC-021, DEC-004
---

# Back · Encender copia y lectura de reglas del gate desde Neo4j

> [!info] Alcance
> Que el **gate** (desbloqueo de nodos y unidades, avance, detalle y material) lea sus reglas de **Neo4j** y no de Postgres. Para eso, la copia a Neo4j tiene que llevar la regla **cruda**, sin podar. Después se encienden los flags en la plataforma. Postgres sigue siendo la fuente de verdad (DEC-021): las escrituras no cambian y, ante cualquier duda, se lee de Postgres. Es una propuesta. Todavía no hay código.

## 1. Qué hay hoy (verificado en `origin/develop`)

- **La caché del gate se carga de Postgres.** `RoadmapRulesLoader.load` (`services/rulecache`) arma la foto `RoadmapRules` con unas 10 consultas SQL y `JpaRuleTreeStore`. `RoadmapRuleCache` la guarda en Caffeine y la tira cuando llega `GraphStructureChanged`. Detrás de `RULE_CACHE_ENABLED`, que está **apagado** por default y **no figura** en `.tpi/platform/docker-compose.yml`.
- **T-18.6 dejó el gate afuera a propósito.** Lo dicen `docs/T-18-6-LECTURA-NEO4J.md` y el comentario de `GraphReadSwitch` ("El gate no lee de acá"). El motivo es que `RoadmapGraphMapper.addLeaf` **no copia las hojas que apuntan a piezas dadas de baja**, y eso puede dejar un grupo anidado vacío. El gate necesita el árbol crudo: lo evalúa así primero y sólo poda si no se cumple. Con `OR(tema borrado que el alumno completó, otro tema)`, el árbol crudo se cumple y el podado no.
- **Lo demás que necesita la foto ya está en Neo4j** desde T-18.6:
  - `prerequisiteMode`, `storedRule` y `requirementIds` (la lista plana **cruda**, con las bajas incluidas) en `:Node` y `:Section`;
  - `visible` y `deletedAt` en `:Section`, y `deletedAt` en `:Node`. El proyector marca la baja y no borra la pieza;
  - `HAS_SUBSECTION` para las zonas, que hace falta porque una zona de una unidad oculta tampoco es visible.
- **`Neo4jStructureLoader`** ya arma `Neo4jStructure` con secciones, nodos, `rules` (dueño → `RuleGroup`) y `parentOf`, todo en una sola transacción de lectura. Pero sólo lee las reglas de los dueños **vigentes**, y las lee **podadas**.
- **`GraphReadSwitch.fromNeo4j`** ya resuelve si Neo4j está al día: flag, marca en `graph_sync_pending` antes y después de leer, y `isActive`. Si falla, cae a Postgres.
- **Plataforma** (`.tpi/platform/docker-compose.yml`): Neo4j 5.26 levantado, `GRAPH_SYNC_ENABLED: "true"` fijo, `GRAPH_READ_ENABLED` a `false` por default, `NEO4J_HEALTH_ENABLED` a `false`, y `RULE_CACHE_ENABLED` ausente, o sea apagado.
- **`RoadmapDigest`** (la reconciliación) compara los operandos de cada regla. Si la regla cruda no entra en la comparación, una copia vieja no se detecta como diferente.

## 2. Decisiones (confirmadas 2026-10-27; D4 ajustada a Neo4j)

| # | Decisión | Recomendación |
|---|---|---|
| D1 | Cómo se guarda en Neo4j una hoja que apunta a una pieza dada de baja | Guardarla como **propiedad** de `:Rule`, `prunedLeaves: ["<posición>\|<NODE\|SECTION\|>\|<uuid>"]`, y no como arista. Una pieza que se dio de baja antes del primer `rebuild` **no existe** en Neo4j, así que no hay hacia dónde trazar la arista. Además, el editor, `/relations` y la vista de grafo no leen esa propiedad, así que la paridad de T-18.6 no se toca. |
| D2 | Flag | **No sumar un flag nuevo.** El gate lee de Neo4j cuando `RULE_CACHE_ENABLED` y `GRAPH_READ_ENABLED` están los dos en `true`. Si se quiere apagar sólo el gate, se puede sumar `GRAPH_RULES_ENABLED`, pero no parece necesario. |
| D3 | Ids dados de baja que Neo4j no conoce | Quedan como «desconocidos» en la foto, y `CachedRuleReads` los resuelve con `DirectRuleReads` (Postgres). El resultado es correcto, sólo cuesta una consulta más en ese caso raro. No se agrega una consulta de bajas a Postgres. |
| D4 | `roadmapOf(ownerId)` | **Se lee de Neo4j** (`(:Roadmap)-[:HAS_SECTION]->(:Section {id})`, o `-[:HAS_NODE]->(:Node {id})`). Va a SQL sólo si el flag está apagado, si Neo4j falla o si no conoce la pieza, como pasa con una pieza recién creada cuya copia está pendiente. Caffeine no guarda los `null`, así que esa pieza se vuelve a buscar en el pedido siguiente. El resultado queda en caché sin vencer, porque el roadmap de una pieza no cambia. |
| D5 | Encender en la estable | La instancia estable del roadmap **la corre un compañero**. Se prueba primero en la variante `polzoni` y después se le pasa la secuencia de encendido al dueño de la estable. |

## 3. Pasos — Copia cruda (`graph/sync`, `graph/model`)

1. `GraphRule`: sumar `private List<String> prunedLeaves = new ArrayList<>();`. Es una propiedad común, así que no necesita migración de Neo4j: las de `src/main/resources/neo4j/migrations` son sólo de restricciones e índices.
2. `RoadmapGraphMapper.addLeaf`: cuando la hoja no encuentra ni sección ni nodo, en lugar de descartarla se agrega a `rule.getPrunedLeaves()` con posición, tipo (vacío si es heredada) e id. Actualizar el comentario de la línea anterior a `addLeaf`, que hoy dice "no se copia". El caso `rule == null` de una regla vacía no cambia: una regla cuyas hojas son todas bajas **no** está vacía, porque `group.isEmpty()` mira los operandos crudos.
3. `RoadmapDigest.operandsOf`: meter `prunedLeaves` en la cadena ordenada por posición, del lado de Postgres y del de Neo4j, para que la reconciliación marque como diferentes las copias sin el dato nuevo.
4. El proyector no se toca: `MERGE` con el mismo id deriva el grupo, y la propiedad se reescribe completa en cada copia.

## 4. Pasos — Lectura del gate desde Neo4j (`graph/read`, `services/rulecache`)

1. `Neo4jStructureLoader`: sumar un método `rawRulesOf(roadmapId)` (o un parámetro en `rulesOf`) que:
   - lea los grupos de **todos** los dueños, también los dados de baja, porque la foto tiene que conocer la regla de un nodo vigente aunque sus hojas sean bajas, y los dueños dados de baja no tienen regla en la foto;
   - traiga `rule.prunedLeaves` en la consulta `GROUPS` y, en `treeOf`, las intercale como `RuleLeaf` según su posición.
   El método de hoy, el podado, queda igual para el editor y `/relations`.
2. Nuevo `Neo4jRulesLoader` en `services/rulecache`, o un método `fromNeo4j` en `RoadmapRulesLoader`, que convierta `Neo4jStructure` a `RoadmapRules`:

   | Campo de `RoadmapRules` | De dónde sale en Neo4j |
   |---|---|
   | dueños nodo y unidad: modo, árbol y lista plana | `prerequisiteMode`; árbol crudo **sólo si `storedRule`**, si no `null` como en SQL; `requirementIds` |
   | todos los nodos y unidades | todas las piezas del roadmap en Neo4j, incluidas las de `deletedAt` |
   | unidades visibles | `visible && deletedAt == null`, menos las zonas cuyo padre no es visible (misma regla que en `load`, T-58.2) |
   | padres | `parentOf` |
3. `RoadmapRuleCache.load`: `graphReadSwitch.fromNeo4j(roadmapId, () -> neo4jLoader.load(roadmapId)).orElseGet(() -> loader.load(roadmapId))`. Con la marca pendiente, con Neo4j caído o con el flag apagado, sigue cargando de Postgres como hoy. La invalidación por `GraphStructureChanged` no cambia: después de una edición, la próxima foto sale de Postgres mientras haya marca, y de Neo4j una vez que la copia termina.
4. `RoadmapRuleCache.rulesOwning`: el índice pieza → roadmap se carga con `neo4jLoader.roadmapOf(ownerId)` y, si devuelve `null` o falla, con `loader.roadmapOf(ownerId)` en SQL (ver D4). La consulta Cypher hace `MATCH` por `id`, que tiene índice único desde la migración `V0001`. Agregar a `RoadmapRuleCacheTest` el caso en que Neo4j no conoce la pieza y responde Postgres.
5. Borrar el comentario "El gate no lee de acá" de `GraphReadSwitch` y actualizar `docs/T-18-6-LECTURA-NEO4J.md`, en la sección «Por qué el gate y el progreso siguen en Postgres»: el progreso sigue en Postgres y el gate ya no.

## 5. Pasos — Encender

1. `application.properties`: los defaults no cambian, siguen apagados (DEC-004).
2. `.tpi/platform/docker-compose.yml` y `.env.example`: agregar `RULE_CACHE_ENABLED: ${RULE_CACHE_ENABLED:-true}` y pasar `GRAPH_READ_ENABLED` a `true` por default. Ver si conviene `NEO4J_HEALTH_ENABLED=true`: el micro quedaría DOWN en el Gateway si se cae Neo4j, y la lectura ya cae a Postgres sola. **Recomendación: dejarlo en `false`.**
3. Secuencia, primero en la variante `polzoni` y después en la estable (ver D5):
   1. desplegar la versión nueva con `GRAPH_SYNC_ENABLED=true`, que en la plataforma ya está;
   2. `POST /admin/graph/rebuild`, una vez, para que todos los roadmaps queden con `prunedLeaves`;
   3. `POST /admin/graph/reconcile`, que tiene que dar **sin diferencias**;
   4. `RULE_CACHE_ENABLED=true` y `GRAPH_READ_ENABLED=true` y reiniciar.
4. Verificar en los logs que no haya `warn` de "No se pudo leer de Neo4j", y repetir el escenario del §6.3 contra la app levantada.

## 6. Tests (sólo los del cambio)

1. `RoadmapGraphMapperTest`: una hoja hacia un nodo dado de baja termina en `prunedLeaves` con su posición. Y un grupo anidado con todas sus hojas en baja se copia con `prunedLeaves` y sin operandos.
2. `RoadmapDigest`/`GraphReconciliationTest`: una copia sin `prunedLeaves` da diferencia.
3. **Paridad Neo4j ↔ Postgres de la foto**: un test nuevo con Testcontainers, `RoadmapRulesNeo4jParityTest`, que reutiliza `ReadParityFixtures` y los casos de `RuleReadsParityTest`:
   - listas planas AND y OR, árbol anidado, hoja dada de baja, unidad oculta, unidad dada de baja y zona de una unidad oculta;
   - **el caso que motivó T-18.6:** `OR(tema dado de baja ya completado, otro tema)`, con el resultado del gate igual por las dos fuentes;
   - comparación pieza por pieza: `OwnerRules`, ids conocidos, visibles y padres.
4. `RoadmapRuleCacheTest`: con marca pendiente carga del loader de Postgres; sin marca, del de Neo4j. Si Neo4j tira una excepción, cae a Postgres.
5. Comandos:
   ```bash
   mvn test -Dtest='RoadmapGraphMapperTest,RoadmapRuleCacheTest,GraphReconciliationTest'
   mvn test -Dtest='RoadmapRulesNeo4jParityTest,Neo4jRoadmapReaderParityTest'   # Docker
   ```
   `Neo4jRoadmapReaderParityTest` va para confirmar que el editor sigue podado. Antes del PR: `mvn verify` (Checkstyle, PMD y CPD).

## 7. Orden y dependencias

§3 (copia) → §6.1 y §6.2 → §4 (lectura) → §6.3 y §6.4 → PR a `develop` → §5 en `polzoni` → avisar al dueño de la estable. Sin dependencias de otros grupos.

## 8. Riesgos

- **Ventana teórica de T-18.6:** si una edición confirma, la copia termina y la marca se borra **mientras** se carga la foto, la foto puede no incluir esa edición. Dura como mucho el TTL (5 min) o hasta la próxima invalidación. Cerrarla del todo pide una columna de versión por roadmap, y queda fuera de este plan.
- **Varias réplicas:** sigue igual que con T-18.4, una caché por réplica con TTL de respaldo. Hoy hay una sola réplica.
- **Latencia:** cargar la foto desde Neo4j suma las dos consultas de la marca y las de `Neo4jStructureLoader`. Como se carga una vez por roadmap y por edición, no por consulta, el P95 del gate (T-20.4) casi no cambia. Conviene medirlo antes y después.
- **Paridad del editor:** si se usa `prunedLeaves` en la lectura podada por error, el editor mostraría hojas hacia piezas borradas. La cubre `Neo4jRoadmapReaderParityTest`.
- **Apagar** cualquiera de los dos flags vuelve al comportamiento de hoy sin perder nada: ninguna regla vive sólo en Neo4j.
