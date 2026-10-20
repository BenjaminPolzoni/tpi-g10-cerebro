---
tags: [tpi, g10, sprint-3, taiga, codigo, patrones, deuda]
fecha: 2026-10-19
estado: borrador
---

# 16 — Brecha entre Taiga, el código y los patrones

Qué tareas del Sprint 3 ya están hechas en el código pero siguen en New en Taiga, qué falta de verdad, y qué mejoras del relevamiento de patrones no tienen tarea. Sirve para ordenar Taiga y decidir qué cargar.

> [!warning] Alcance y límites de este relevamiento
> - **Taiga no se pudo leer en vivo.** El MCP de Taiga no filtra por sprint y `getUserStory` falla con los ids. El estado de Taiga sale del espejo del cerebro ([[sprints/sprint-3/12-responsables|12 — Responsables]]), que es del **2026-10-15**: puede estar desactualizado.
> - **El código se verificó sobre `develop`** al 2026-10-19 (`8f48efb8`, PR #277, migraciones hasta V49) con búsquedas sobre `src/main/java`. Las tareas de la sección 1 salen de los PRs mergeados de [[sprints/sprint-3/14-cambios-recientes|14 — Cambios recientes]] y de `git log develop`.
> - Las búsquedas dicen si algo **existe**, no si funciona. No se corrieron tests ni se creó nada en Taiga.

Fuentes: [[sprints/sprint-3/12-responsables|12]], [[sprints/sprint-3/14-cambios-recientes|14]], [[arquitectura/patrones-de-diseno]], [[arquitectura/patrones-plataforma]], [[deuda-tecnica]].

## 1. Hecho en el código, pero New en Taiga

Hay que cerrar estas tareas en Taiga (o confirmar que ya se cerraron después del 15/10).

| Tarea | Evidencia |
|---|---|
| T-17.1, T-17.2, T-17.3: modelo 1 a N, rutas por roadmap, alcance curso/roadmap | BE#215, BE#218, BE#223 |
| T-57.1, T-57.2: habilitar, crear, renombrar y archivar roadmaps | BE#223 |
| T-19.4: roadmap correcto en los eventos del Motor | BE#217 |
| T-20.1, T-20.3: evaluador único de reglas y BDD | BE#247, BE#248 |
| T-59.1, T-59.2: reglas como árbol AND/OR y asistente | BE#224, BE#238, FE#691 |
| T-65.5: relaciones con tipo en Postgres | BE#260 |
| T-31.1, T-31.2: `origin_unavailable` en el gate | BE#234, FE#624 |
| T-31.5: endpoint de pre-chequeo del alumno | BE#234 |
| T-32.1, T-32.2: «desafío no disponible» | BE#253, FE#672, FE#757 |
| T-32.5: ícono solo en desafíos y exámenes | BE#250 |
| T-45.9, T-45.10, T-45.11: comisión en ranking, comparar comisiones, orden por XP o notas | FE#709, FE#739, BE#277 |
| T-69.2: mentor por curso | BE#254 |
| T-73.1, T-73.2: racha (registro y cálculo) | BE#240, BE#255 y BE#258 (flag `app.features.streak` apagado) |
| T-26.5: ranking con los componentes del kit | FE#615 |

## 2. Falta de verdad (con tarea en Taiga)

| Tema | Tareas | Estado |
|---|---|---|
| Permisos | T-22.1 a T-22.4 | `develop` tiene 29 usos de `hasRole`/`hasAnyRole` (eran 17 al armar HT-22). No hay ninguna referencia al scope `roadmap.gate.read`: `SecurityConfig` solo valida `roadmap.progress.read` (DT-01) |
| Insignias | T-30.3, T-30.4, T-30.5 | `BadgeEvaluator.meets` manda `SECTION_NO_LIVES_LOST`, `NODE_NO_RETRIES` y `LIFE_RECOVERED` a `default -> false` (DT-24) |
| Nodos y vidas | T-32.3, T-32.4 | El PUT resetea `lives_policy`; falta el campo de reintentos permitidos |
| Gate | T-31.3, T-31.4 | Último dato de vidas con aviso de 24 h. En `develop` hay `stale` en ranking e inventario, pero no en `GateEvaluator` |
| Inicio y fin | HU-64 (T-64.1 a T-64.5) | `NodeType` sigue con `UNIT`, `CONTENT`, `THEORETICAL_CHALLENGE`, `PRACTICAL_CHALLENGE` y `EXAM`. Existe la rama `feature/t-64-1-nodos-inicio-fin`, sin mergear |
| Reglas de sección | T-58.2, T-58.3, T-58.4 | Subsecciones sin ciclos, editor con XP mínimo y explicación al alumno. T-58.1 está en BE#268 (abierto) |
| Qué le falta al alumno | T-59.3 | Ver [[sprints/sprint-3/15-tarea-que-le-falta-al-alumno|15]] |
| Relaciones con tipo (front) | T-65.2, T-65.3 | Ver el nombre y elegir el tipo |
| Vista de grafo | HU-62 (T-62.1 a T-62.6), HT-34 | Posiciones guardadas, relaciones arrastrando, teclado. Depende del componente de grafo del kit |
| Neo4j | T-18.2 a T-18.7 | El módulo `graph/` existe pero ningún servicio lo usa y no hay proyector (DT-25, DEC-021) |
| Restricciones de Courses | HU-49 (T-49.9 a T-49.13) | Parcial: existe `CourseRestrictionsClient` y `GraphValidator` lo usa para revalidar prerrequisitos de unidad. No encontré distinción oculto/bloqueado, reacción al evento de cambio ni la ventana horaria del examen. T-49.9 pide verificar qué ya está |
| Roadmaps por grupo | HU-61 (T-61.1 a T-61.3) | Hay `GroupAccessService`, pero no la asignación de roadmap a grupos |
| Clonar | HU-71 | BE#266 abierto |
| Cierre del curso | HU-72 | No hay código de estado académico final |
| Archibaldo | T-69.1, T-69.3 | Enter y destello |
| Lista de nodos | T-68.3, T-68.4 | Obligatoriedad en desafíos y exámenes |
| Demo y docs | HT-21, HT-23 y las tareas «Wiki, OpenAPI y diagrama de secuencia» | Sin empezar |
| UI-KIT | T-26.1 a T-26.4, T-26.6, T-26.7 | Pendientes |

## 3. Sin tarea en Taiga

Salen de [[arquitectura/patrones-de-diseno]] y [[deuda-tecnica]]. Ninguna está en las historias del Sprint 3, salvo la matriz de roles (T-22.1) y los dos puntos de seguridad y permisos (DT-01 y DT-02, cubiertos por T-22.4 y T-22.3).

| Candidata | Origen | Esfuerzo | Referencia para resolverla |
|---|---|---|---|
| `OutboxPoller` no debe mantener la transacción abierta mientras espera el ACK de Kafka | DT-22 | M | `tpi-sandbox` (`OutboxRelay` con `TransactionTemplate`) |
| Publicar `COURSE_LEVEL_UP` y `PERFORMANCE_ZONE_CHANGED`, o corregir `AGENTS.md` y el contexto integral | DT-23 | M | [[decisiones/DEC-002-outbox-transaccional-eventos-salientes\|DEC-002]] |
| Circuit breaker (Resilience4j) en los clientes de Courses y Accounting | DT-26 | M | `tpi-theoristcal-challenge` (`CoursesCallGuard`), `tpi-market` |
| Decidir si se termina el proyector Postgres → Neo4j o se saca `graph/` | DT-25 | L | [[decisiones/DEC-021-postgres-fuente-de-verdad-neo4j-proyeccion\|DEC-021]] |
| Partir `GraphService` (897 líneas) y `RankingService` (514); sacar `@SuppressWarnings("PMD.GodClass")` | patrones §4 y §5 | M | Un service por caso de uso |
| Strategy por tipo de evento en `RoadmapEventListener` | patrones §4 | S | Solo cuando se sume el próximo evento |
| Verificar el posible N+1 de roadmap → secciones → nodos | patrones §4 (hipótesis) | S | Mirar el log de SQL antes de agregar `@EntityGraph` |
| Borrar el listener legado de `challenges.results` y su flag | DT-05 | S | — |
| Confirmar si `TraceIdFilter` se borró a propósito y actualizar el doc | DT-07 | S | — |
| Cerrar las ramas colgadas (`revert-130-…` no se mergea) | DT-17 | S | — |
| Actualizar contratos con camelCase (`courses.md` §7.3, estándar de Kafka) | DT-18 | S | — |
| Ordenar Taiga (15 de 17 épicas en New con HU Done) | DT-19 | S | — |
| Encender `SECTIONS_SYNC_ENABLED` y `ROADMAP_BY_GROUP_ENABLED` | DT-20 | S | — |
| Migraciones fuera de orden: BE#258 trae V39 con V45 ya en `develop` | [[sprints/sprint-3/14-cambios-recientes#Alertas para el equipo\|14 — Alertas]] | S | — |
| Alinear el largo mínimo del nombre del nodo (back 2, front 3) | [[deuda-tecnica]] | S | — |

## 4. Orden sugerido

1. **Ordenar Taiga:** cerrar las tareas de la sección 1 y confirmar contra `develop` las de la sección 2.
2. **Riesgo de seguridad:** T-22.4 (scope del gate, DT-01) antes que el resto de HT-22.
3. **Confiabilidad del outbox y de las llamadas:** DT-22, DT-23 y DT-26.
4. **Decisión pendiente:** qué hacer con Neo4j (DT-25), porque condiciona HT-18 y HU-62.
5. **Cierre de funcionalidad:** HU-49, HU-64, HU-71, HU-72 y HT-21 (la demo depende de casi todo).

> [!question] Para decidir en equipo
> - ¿Cargamos la sección 3 como tareas nuevas o como una HT de deuda técnica? El cerebro la tiene como deuda entre sprints ([[deuda-tecnica]]), no como HU.
> - ¿Se termina el proyector de Neo4j en este sprint o se saca el módulo `graph/` hasta que haga falta?
