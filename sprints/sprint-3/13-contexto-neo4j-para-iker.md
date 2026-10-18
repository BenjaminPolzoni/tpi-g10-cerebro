---
tags: [tpi, g10, sprint-3, neo4j, reglas, contexto, iker]
fecha: 2026-10-16
estado: vigente
autor: Santino Fenoglio
para: Iker Alonso
---

# 13 — Contexto para Iker: qué hay hecho de reglas y qué falta para encender Neo4j

> [!info] Para quién es
> Para Iker y para su agente. Lo escribió Santino (T-59.1) con el estado del código al **2026-10-16, 20:10** (ya mergeadas las lecturas, #238, y el gate de Camacho, #234). Si algo de acá no coincide con `develop`, manda `develop`: mirá `git log origin/develop` antes de seguir. Complementa a [[sprints/sprint-3/11-plan-ejecucion-grafo|11 — Plan de ejecución del grafo]], que es el plan de Iker.

> [!tip] Cómo leerlo
> Orden sugerido: **1 TL;DR → 3 Qué hay en el código → 5 Qué choca con Neo4j → 7 Camino propuesto**. El resto es referencia.

## 1. TL;DR

- **Neo4j ya está en el repo:** compose (T-16.1, #222), Spring Data Neo4j con módulo `graph` mínimo y Testcontainers (T-16.3, #237), y el modelo en `docs/T-16-4-MODELO-GRAFO.md`.
- **Las reglas combinadas ya funcionan, pero en Postgres:** Santino hizo T-59.1 (#224, mergeada). Un nodo o una sección puede exigir `A y (B o C)`, el gate lo respeta y el editor lo guarda. Todo está detrás de la interfaz **`RuleTreeStore`**, pensada para que el día que Neo4j sea la fuente solo se cambie su implementación.
- **Lo que choca con Neo4j** (sección 5): el orden de los operandos, las reglas de sección, las aristas planas que hoy siguen siendo la fuente para ciclos y para Courses, y la conversión de las reglas planas a árbol.
- **Lo que falta para «poner Neo4j ya»** son T-18.1, T-18.9 (`StructureReader`/`StructureWriter`), T-18.2, T-18.3, T-18.6 y T-16.2. El grueso es T-18.9: **12 clases** leen o escriben las aristas planas por JPA (lista en la sección 5.3).

## 2. Estado por tarea

| Tarea | Dueño | Estado al 16/10 | Dónde |
|---|---|---|---|
| T-16.1 Neo4j en el compose | Iker | Mergeada (#222) | `docker/docker-compose.yml`, `docs/T-16-1-NEO4J-COMPOSE.md` |
| T-16.3 Spring Data Neo4j + Testcontainers | Iker | Mergeada (#237) | `docs/T-16-3-SPRING-DATA-NEO4J.md`, paquete `graph/` |
| T-16.4 Modelo del grafo | Iker | Mergeada (#220) | `docs/T-16-4-MODELO-GRAFO.md` |
| T-59.1 Reglas combinadas como árbol | Santino | Mergeada (#224) | paquete `rules/`, V28, `UnlockRuleService` |
| T-59.1 Lectura del árbol en los GET | Santino | Mergeada (#238) | `GraphDtos`, `UnlockRuleService.nodeRulesOf` |
| T-16.2 Neo4j en la plataforma | Stefano | Sin hacer | `tpi-system-compose` |
| T-18.1 Módulo `graph` completo + esquema | Iker | Sin hacer | solo hay el módulo mínimo de T-16.3 |
| T-18.9 Lector/escritor común | Iker | Sin hacer | no hay rama |
| T-18.2 a T-18.7 | Iker | Sin hacer | |
| T-17.3 XP por roadmap | Baltasar | Rama sin mergear, **choca en V28** | ver sección 8 |

## 3. Qué hay en el código sobre reglas

### 3.1 Dominio puro: `rules/`

No tocan ninguna base de datos. **No hay que cambiarlos** para pasar a Neo4j.

| Clase | Qué es |
|---|---|
| `RuleNode` (sellada) | Hoja o grupo |
| `RuleLeaf(elementId)` | Un nodo o una sección que el alumno tiene que haber superado |
| `RuleGroup(op, minXp, operands)` | Grupo AND/OR con XP mínimo opcional. `operands` mezcla hojas y grupos hijos **en orden** |
| `RuleEvaluator` | Único lugar que decide si un alumno cumple una regla y qué le falta (`RuleGap`) |
| `RuleTreeValidator` | Forma de la regla: grupo vacío, XP negativo, operando repetido, profundidad máxima (`app.rules.max-depth`, por defecto 5) |
| `RuleContext(passed, xp)` | Lo que se sabe del alumno al evaluar |
| `RuleTreeStore` | **La interfaz de persistencia. Es tu punto de entrada** |

`RuleGroup.ofLegacy(mode, ids)` pasa «un modo + una lista plana» a un árbol de un grupo. `RuleGroup.prune(keep)` quita las hojas que ya no rigen.

### 3.2 `RuleTreeStore`

```java
Optional<RuleGroup> find(UUID ownerId, RuleOwnerType type);
Map<UUID, RuleGroup> findAll(Collection<UUID> ownerIds, RuleOwnerType type);   // lectura en lote
void replace(UUID ownerId, RuleOwnerType type, UUID courseCohortId, RuleGroup tree);
void clear(UUID ownerId, RuleOwnerType type);
```

`RuleOwnerType` es `NODE` o `SECTION`. Hoy lo implementa `JpaRuleTreeStore` (`services/`). Quien lo usa: `UnlockRuleService`, `PrerequisiteService` (el gate de nodos) y `SectionPrerequisiteService` (el gate de secciones).

### 3.3 Tablas (V28, en `db/migration-vendor/{h2,postgresql}`)

| Tabla | Columnas relevantes |
|---|---|
| `unlock_rule_group` | `id`, `course_cohort_id`, `owner_id`, `owner_type` (`NODE`/`SECTION`), `parent_group_id` (nulo = raíz), `op` (`AND`/`OR`), `min_xp`, `sort_order`, `deleted_at` |
| `unlock_rule_operand` | `id`, `course_cohort_id`, `group_id`, `element_id`, `sort_order`, `deleted_at` |

- Un solo grupo raíz vivo por dueño: índice único parcial en Postgres; en H2 se emula con una columna calculada.
- `sort_order` ordena **juntos** a los operandos y a los grupos hijos del mismo padre.
- Editar una regla da de baja todo su árbol y guarda uno nuevo (no hay `UPDATE` de un árbol).
- Los operandos no tienen clave foránea hacia el elemento (el destino depende de `owner_type`): la integridad la cuida la aplicación.

### 3.4 API que el front va a usar

El mismo árbol viaja en el `PATCH` y en las lecturas. Es el contrato que **la implementación de Neo4j no puede cambiar**:

```json
{ "op": "AND", "operands": [
    { "element_id": "<uuid del nodo A>" },
    { "op": "OR", "operands": [ { "element_id": "<B>" }, { "element_id": "<C>" } ] } ] }
```

- `PATCH /api/roadmap/nodes/{id}/rules` y `PATCH /api/roadmap/sections/{id}/rules` aceptan `{"rule": <árbol>}` o el formato plano de siempre (`mode` + `prerequisite_node_ids`). Si vienen los dos, manda el árbol. Una regla vacía quita las reglas.
- `GET /courses/{id}` y `GET /roadmaps/{id}` traen `rule` en cada nodo y cada sección que tenga reglas (#238, ya mergeado). Una regla plana se lee como un grupo de un nivel.
- El XP mínimo **se rechaza con 400** (`rule.min-xp-not-enforced`) hasta que T-20.2 y T-58.1 lo evalúen en el gate.

## 4. Cómo se decide qué se guarda como árbol

Esta es la decisión que más afecta a la migración:

> **Solo se guarda un árbol en `unlock_rule_*` cuando la regla es más que un modo y una lista plana** (grupos anidados, o XP mínimo). Las reglas planas **no** se guardan como árbol: viven en `node_prerequisite` / `section_prerequisite` (más `node.prerequisite_mode` / `section.prerequisite_mode`).

Y además:

> **Las aristas planas llevan siempre todas las hojas** de cualquier árbol. Así el detector de ciclos, la restauración por Courses (HU-17) y el reverso «qué desbloquea este nodo» siguen leyendo de ahí.

Cómo decide el gate (`PrerequisiteService.isSatisfied`): si hay árbol, lo evalúa con `RuleEvaluator`; si no, evalúa la lista plana. Con el árbol evalúa la regla tal cual y, **solo si no se cumple**, la regla podada de nodos dados de baja. El congelado de desbloqueos ya alcanzados (HU-13 CA4, `freezeReachedUnlocks`) usa ese mismo criterio.

## 5. Qué choca con Neo4j

### 5.1 Diferencias entre el árbol y tu `GraphRule`

| # | Tema | Hoy en Postgres | En tu modelo (T-16.3) | Qué conviene |
|---|---|---|---|---|
| 1 | **Orden de los operandos** | `sort_order` mezcla hojas y grupos hijos | `GraphRule` separa `nodeOperands` y `groupOperands` en dos listas: **se pierde el orden entre ellas** | Guardar una propiedad `order` en `HAS_OPERAND` y reconstruir el orden al leer |
| 2 | **Reglas de sección** | `owner_type = SECTION`, operandos que son secciones | `GraphSection` no tiene `unlockedBy`, y `GraphRule` solo tiene operandos hacia `:Node` y `:Rule` | `GraphSection` necesita `UNLOCKED_BY` y un `HAS_OPERAND` hacia `:Section` (T-18.1) |
| 3 | **Reglas planas** | No son árbol: viven en las aristas | Son un `:Rule` con operandos | El job de migración (T-18.2) las convierte con `RuleGroup.ofLegacy(mode, ids)` |
| 4 | **Id del `:Rule`** | UUID aleatorio al guardar un árbol | T-16.4 pide un id determinístico (UUID v3 de `"rule:" + ownerId`) para que la migración sea idempotente | Para las reglas planas usar el determinístico; para los árboles ya guardados decidí si conservás el `id` del grupo o también lo derivás |
| 5 | **Id del `HAS_OPERAND`** | `unlock_rule_operand.id` (árbol) o `node_prerequisite.id` (arista plana) | `NodeOperand.id` | T-16.4 dice: el id de la fila de prerrequisito. Conservalo en ambos casos |
| 6 | **Baja lógica** | Se da de baja el árbol entero al editar; las aristas planas se dan de baja y se restauran (HU-17) | `deletedAt` en cada `HAS_OPERAND` | Respetar que Courses puede **restaurar** una sección y sus aristas |
| 7 | **Cohorte** | `course_cohort_id` en las dos tablas (RF-NFR-01) | No está en `GraphRule`/`GraphNode` | Decidir si la cohorte se agrega al `:Rule` o se llega por el roadmap |

### 5.2 Transacciones

No hay transacción común entre las dos bases (DEC-016). Un servicio que escriba en Neo4j usa `@Transactional(GraphPersistenceConfig.NEO4J_TRANSACTION_MANAGER)`. Hoy `UnlockRuleService.save` y `GraphService.updateRules` escriben **en Postgres** (aristas planas y árbol) dentro de una sola transacción JPA: con Neo4j esa escritura pasa a ser doble y la consistencia la cuida T-18.3.

### 5.3 Las 12 clases que hoy leen o escriben las aristas planas por JPA

Son lo que T-18.9 (`StructureReader`/`StructureWriter`) tiene que abstraer antes de poder leer de Neo4j. Todas usan `NodePrerequisiteRepository` o `SectionPrerequisiteRepository`:

| Grupo | Clases |
|---|---|
| Gate | `PrerequisiteService`, `SectionPrerequisiteService` |
| Ciclos | `PrerequisiteGraphService`, `SectionPrerequisiteGraphService` |
| Escritura | `PrerequisiteEditor`, `SectionPrerequisiteEditor` |
| Lectura para respuestas | `PrerequisiteReader`, `SectionPrerequisiteReader` |
| Otros | `GraphValidator` (`findOutOfScopeEdges`), `CourseSectionsReconciliationService` (da de baja y restaura aristas cuando Courses saca o devuelve una unidad) |
| Repos | `NodePrerequisiteRepository`, `SectionPrerequisiteRepository` |

> [!warning] Importante para T-18.6
> Con el flag de lectura encendido, HT-18 CA6 dice que las ediciones de estructura se escriben **solo en Neo4j**. Eso deja sin sentido la regla «las aristas planas llevan todas las hojas»: el detector de ciclos, el gate y la reconciliación con Courses tienen que leer del árbol de Neo4j. Por eso conviene que esas 12 clases dependan de `StructureReader` y no de los repositorios JPA **antes** de apagar las aristas planas.

## 6. Reglas de negocio que no se pueden perder al migrar

- **HU-13 CA4:** un desbloqueo ya alcanzado no se revierte al cambiar las reglas. Vive en `node_unlock` (Postgres) y se escribe con `freezeReachedUnlocks`, que **debe correr antes de reemplazar la regla**.
- **Hojas dadas de baja:** un nodo o una sección borrada no deja bloqueado para siempre a quien lo exigía (se poda al evaluar y no viaja en las lecturas).
- **Las ediciones se registran** en `node_edit_log` y salen por el outbox de Postgres (T-18.3), como hoy.
- **El editor lee con un solo formato:** una regla plana y una anidada se devuelven igual (`rule`). Si se migra la lectura, hay que conservarlo.
- **Un solo grupo raíz vivo por dueño.**
- **XP mínimo:** hoy rechazado en el `PATCH`. Cuando T-20.2 lo habilite, ya está en `GraphRule.minXp` y en `unlock_rule_group.min_xp`.

## 7. Camino propuesto (a validar con Iker)

> [!note] Es una propuesta, no una decisión
> Surge de leer el código. Iker conoce su plan ([[sprints/sprint-3/11-plan-ejecucion-grafo|11]]) y puede reordenar.

1. **T-18.9 primero, con la implementación sobre Postgres.** Que las 12 clases de la sección 5.3 dependan de `StructureReader`/`StructureWriter`. Es el cambio más grande y el único que no se puede hacer a medias. Con `RuleTreeStore` ya hay un ejemplo de cómo dejar la puerta abierta.
2. **T-18.1:** completar el módulo `graph` con lo que falta según la sección 5.1 (reglas de sección, `order`, cohorte) y el esquema versionado con `neo4j-migrations`.
3. **Implementar `Neo4jRuleTreeStore`** (`find`, `findAll`, `replace`, `clear`) con el mapeo `RuleGroup` ↔ `GraphRule`. El dominio, el evaluador y el validador **no cambian**.
4. **T-18.2:** migración idempotente. Para los árboles de `unlock_rule_*` y, aparte, las reglas planas con `RuleGroup.ofLegacy`.
5. **T-18.3 y T-18.6:** reconciliación y flag de lectura.

**Red de seguridad:** hay tests de integración por HTTP que no dependen de la base de datos y sirven como criterios de aceptación de la migración. Si los corrés con el flag encendido (usando `GraphNeo4jContainer`), prueban el comportamiento completo:

| Test | Qué cubre |
|---|---|
| `UnlockRuleTreeTest` (55 pruebas) | Guardar, reemplazar y borrar árboles; el gate; prerrequisito suelto; hojas dadas de baja; congelado; cohorte; raíz único |
| `UnlockRuleReadTest` (16 pruebas) | Lectura del árbol en nodos y secciones |
| `RuleEvaluatorTest`, `RuleGroupTest`, `RuleTreeValidatorTest` | Dominio puro |

## 8. Coordinación pendiente

| Con quién | Tema |
|---|---|
| **Baltasar** | Su rama `feature/t-17-3-alcance-xp-por-roadmap` tiene `V28__roadmap_progress_scope.sql` en `db/migration`. **Ya existe `V28__unlock_rule_tree.sql`** (en `db/migration-vendor`), así que Flyway falla con «más de una migración con versión 28». Su rama de gestión (`t-57-1-2`) ya la pasó a V29. Hay que renumerar la de T-17.3. Para tus migraciones nuevas, **mirá la última versión mergeada** y las de las ramas abiertas antes de elegir número |
| **Camacho** | T-31.1 (#234) ya está mergeada: `GateService` ahora responde `origin_unavailable` en vez de 503 y se sacó `ProgressService.startChallenge`. No tocó `GateEvaluator` ni `NodeProgressService`, así que no choca con T-20.1 |
| **Stefano** | T-16.2: Neo4j en `tpi-system-compose`. Sin eso, Neo4j no existe en el entorno de la plataforma ni en la demo |
| **Santino** | Cuando mergee T-20.2 y T-58.1 se quita el rechazo del XP mínimo. Avisale si cambiás `RuleTreeStore` |

## 9. Convenciones del repo que te pueden frenar

- **Migraciones:** las que difieren entre motores van en `db/migration-vendor/{h2,postgresql}/`, la misma versión en las dos (precedentes: V21, V27, V28). H2 no soporta índices parciales: se emulan con una columna calculada.
- **PMD `CommentSize`:** máximo 6 líneas de comentario por bloque y 80 columnas. Checkstyle exige Javadoc con un `@param` por cada parámetro o componente de record. El archivo `GraphDtos` tiene un único `@SuppressWarnings("PMD.CommentSize")` a nivel de interfaz; un supresor a nivel de record **no** cubre el Javadoc que está arriba.
- **Hook de pre-push:** corre `mvn verify`. No se salta con `--no-verify`.
- **Los tests con Testcontainers** necesitan Docker. Sin Docker se saltan solos (`assumeTrue`).
- **Windows:** el árbol de trabajo queda con CRLF y Git normaliza a LF al commitear. Si automatizás ediciones de texto en varias líneas, normalizá los saltos de línea antes de buscar.

## 10. Dónde mirar

| Qué | Dónde |
|---|---|
| Modelo del grafo | `docs/T-16-4-MODELO-GRAFO.md` (repo `tpi-roadmap`) |
| Spring Data Neo4j | `docs/T-16-3-SPRING-DATA-NEO4J.md` |
| Compose de Neo4j | `docs/T-16-1-NEO4J-COMPOSE.md` |
| Decisiones | [[decisiones/DEC-016-neo4j-para-la-estructura-del-roadmap\|DEC-016]], [[decisiones/DEC-018-catalogo-de-relaciones-y-tipos-de-nodo\|DEC-018]], [[decisiones/DEC-011-quitar-umbral-xp-seccion-v8\|DEC-011]], [[decisiones/DEC-005-baja-logica-sin-borrar-progreso\|DEC-005]] |
| Tu plan | [[sprints/sprint-3/11-plan-ejecucion-grafo\|11 — Plan de ejecución del grafo]] |
| Historias | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]], [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas\|HU-59]], [[sprints/sprint-3/historias/HU-58 Dependencias entre secciones\|HU-58]] |
| Quién tiene qué | [[sprints/sprint-3/12-responsables\|12 — Responsables]] |
| Repo del back | `C:\Users\Santino04\Desktop\tpi-roadmap` en la máquina de Santino; `2026-P4-BE/tpi-roadmap` en GitHub |

> [!check] Para que el agente no se pierda
> 1. Leé `docs/T-16-4-MODELO-GRAFO.md` y este documento.
> 2. Abrí `rules/RuleTreeStore.java`, `services/JpaRuleTreeStore.java` y `services/UnlockRuleService.java`.
> 3. Abrí `graph/model/GraphRule.java` y compará con la sección 5.1.
> 4. Antes de tocar una de las 12 clases de la sección 5.3, corré `UnlockRuleTreeTest` y `UnlockRuleReadTest` para tener la línea base en verde.
