---
tags:
  - tpi
  - g10
  - arquitectura
  - patrones
fecha: 2026-10-19
estado: vigente
---

# Patrones de diseño y arquitectura — roadmap-service

Qué patrones GoF y arquitectónicos usa `tpi-roadmap`, cuáles están bien, cuáles conviene mejorar y cuáles vale la pena sumar. La comparación con los otros 13 backends de la plataforma está en [[arquitectura/patrones-plataforma|patrones de la plataforma]].

> [!info] Cómo se armó
> Relevamiento del 2026-10-19 sobre `develop` (commit `f5ed143`). Cinco agentes Antigravity recorrieron el código de los 14 repos Java del org `2026-P4-BE` y de `tpi-roadmap-mocks`. Las afirmaciones fuertes se verificaron a mano contra el código. Lo que no se verificó dice **Hipótesis**. Las rutas son relativas a `src/main/java/com/utn/tpi/roadmap/`.

## 1. Estilo arquitectónico

- **Capas por paquete técnico** (`controllers`, `services`, `repositories`, `entities`, `dtos`, `models`), con dos islas de **puertos y adaptadores**:
  - `clients/`: interfaces (`LostLivesClient`, `ParCatalogClient`, `CoursesMaterialClient`…) con implementación `Http*` y doble en memoria, que se elige con `ClientMode`.
  - `rules/`: árbol de reglas de desbloqueo en Java puro, sin Spring ni JPA. Se guarda a través del puerto `RuleTreeStore`, que implementa `services/JpaRuleTreeStore`.
- **Modelo separado de la persistencia:** `entities/ → toModel() → models/ → dtos/`. Las entidades JPA son anémicas (getters y setters). La lógica vive en los services.
- Mapa de paquetes: [[arquitectura/estructura-codigo]].

## 2. Patrones GoF

| Patrón | Dónde | Veredicto |
|---|---|---|
| **Composite** | `rules/RuleNode` (sealed) → `RuleGroup` (AND/OR con `operands`) y `RuleLeaf` | ✅ Perfecto |
| **Interpreter** | `rules/RuleEvaluator` evalúa el árbol de `RuleNode` contra `RuleContext` (incluye `min_xp`) | ✅ Perfecto |
| **Visitor** (forma moderna) | `RuleEvaluator` y `dtos/RuleDtoMapper` recorren el árbol con `instanceof` sobre la interfaz sellada. Reemplaza al Visitor clásico | ✅ Correcto para Java 21 |
| **Factory Method** | `RuleGroup.and(...)`/`or(...)`, `ApiEnvelope.ok(...)`, `EventParser.parse(...)`, `GateEvaluation.blocked/allowed(...)` | ✅ Bien |
| **Builder** | Lombok `@Builder` en entidades y modelos (`OutboxEventEntity`, `models/Node`); `RestClient.Builder` | ✅ Bien |
| **Prototype** (withers) | `RuleGroup.withMinXp(...)`, `RankingEntry.withStanding(...)`: copia inmutable con un campo distinto | ✅ Bien |
| **Singleton** | Lo da Spring (beans singleton). Utilitarios con constructor privado (`RankingRules`) | ✅ Bien |
| **Abstract Factory** (por configuración) | `@ConditionalOnProperty(app.clients.*.mode)` elige la familia `Http*` o la `InMemory*`. `IntegratedClientsValidator` aborta el arranque si queda un stub en el perfil `integrated` ([[decisiones/DEC-008-perfil-integrated-falla-con-stubs\|DEC-008]]) | ✅ Perfecto |
| **Adapter** | `clients/**/Http*Client` traducen JSON y status ajenos a tipos propios | ✅ Bien |
| **Bridge** | `RuleTreeStore` (abstracción) / `JpaRuleTreeStore` (implementación) | ✅ Bien |
| **Decorator** | `ApiEnvelopeAdvice` envuelve respuestas; `CorrelationPropagationInterceptor` agrega `traceparent` a las llamadas salientes | ✅ Bien |
| **Proxy** | Lo da Spring: `@Transactional`, `@PreAuthorize`, repositorios Spring Data | ✅ Bien |
| **Facade** | `services/GraphService`, `GateEvaluator`, `CourseSectionSyncService` | 🟡 Mejorable: `GraphService` tiene 897 líneas y `@SuppressWarnings("PMD.GodClass")` (ver §5) |
| **Chain of Responsibility** | Filtros servlet (`GatewayHeadersFilter`). En `GateEvaluator.evaluate` hay una secuencia corta: `commonBlockReason` → unidad → lectura → prerrequisito → vidas | ✅ Alcanza así (ver §4) |
| **Command** | Fila de `outbox_event` = orden diferida de publicar. `Supplier<StudentLives>` en el Gate posterga la llamada a Accounting | ✅ Bien |
| **Iterator** | Recorrido DFS iterativo con `ArrayDeque` en `PrerequisiteGraphService` (detecta ciclos sin recursión) | ✅ Bien |
| **Memento** | `GraphService` guarda `before`/`after` del nodo en `NodeEditLogEntity`; `freezeReachedUnlocks` congela desbloqueos ya ganados | ✅ Bien |
| **Observer** | `@KafkaListener` en `RoadmapEventListener`, `CoursesLifecycleEventListener`, `AccountingEventsListener`, `ParRefreshListener` | ✅ Bien. El despacho interno es mejorable (§3) |
| **Strategy** | `RankingRules` (cadena de `Comparator` para el desempate RF-RNK-11), clientes intercambiables por interfaz, `BadgeEvaluator.meets` con `switch` por criterio | ✅ Bien |
| **Template Method** | Spring (`KafkaTemplate`, `ResponseEntityExceptionHandler`) y `entities/BaseEntity` (`softDelete()`/`softRestore()`) | ✅ Bien |
| **State** | `NodeStatus` y `OutboxStatus` son `enum` con transiciones en los services | ✅ Alcanza: son pocos estados. No hace falta el State GoF |
| **Flyweight** | Valores compartidos en caché: PAR (Caffeine), token técnico, `RankingFallbackCache` | ✅ Bien (en rigor es caché; se cuenta como Flyweight en sentido amplio) |
| Mediator, Abstract Factory clásico, Memento formal | No hay implementaciones a mano. No se necesitan | — |

## 3. Patrones arquitectónicos

| Patrón | Dónde | Veredicto |
|---|---|---|
| **Microservicio + API Gateway** | Prefijo `/api/roadmap/**`, identidad por headers `X-User-*` (`GatewayHeadersFilter`) | ✅ Bien |
| **Service Discovery** (Eureka) | `roadmap-service` | ✅ Bien |
| **Database per Service** + Flyway | `roadmap_db`, migraciones V1..V28 | ✅ Bien |
| **Event-Driven** (Kafka, envelope v8, snake_case) | `events/EventEnvelope`, `EventParser`, `KafkaConsumerConfig` (ACK manual, DLT) | ✅ Bien ([[decisiones/DEC-001-wire-kafka-v8-snake-case\|DEC-001]]) |
| **Consumidor idempotente / ledger** | `xp_movement` append-only con `UNIQUE(event_id)` | ✅ Perfecto ([[decisiones/DEC-013-roadmap-no-calcula-xp-ledger-idempotente\|DEC-013]]) |
| **Transactional Outbox** | `events/outbox/OutboxService` (`Propagation.MANDATORY`), `OutboxPoller` con `SKIP LOCKED` | 🟡 Mejorable: ver §4.1 y §4.2 ([[decisiones/DEC-002-outbox-transaccional-eventos-salientes\|DEC-002]]) |
| **Anti-Corruption Layer** | `clients/**`, `AccountingErrors`, mapeo de 4xx de Accounting ([[decisiones/DEC-015-4xx-de-accounting-no-es-indisponibilidad\|DEC-015]]) | ✅ Bien |
| **Cache-Aside** con invalidación por evento | PAR en `HttpParCatalogClient` (Caffeine) + `ParRefreshListener`; `HttpLostLivesClient`; `RankingFallbackCache` ([[decisiones/DEC-019-ranking-estado-de-datos-y-cache-de-respaldo\|DEC-019]]) | ✅ Bien |
| **Fail-closed / degradación explícita** | El Gate responde `origin_unavailable` en vez de suponer elegibilidad ([[decisiones/DEC-020-gate-origen-no-disponible-en-vez-de-503\|DEC-020]]) | ✅ Perfecto |
| **Feature Toggle** apagado por defecto | `SECTIONS_SYNC_ENABLED`, `ROADMAP_BY_GROUP_ENABLED` ([[decisiones/DEC-004-flags-apagados-por-defecto\|DEC-004]]) | ✅ Bien |
| **Problem Details** (RFC 9457) | `common/web/ApiExceptionHandler` + `ErrorCatalog` + `trace_id` | ✅ Bien |
| **Soft delete** | `BaseEntity` + `@SQLRestriction("deleted_at IS NULL")` ([[decisiones/DEC-005-baja-logica-sin-borrar-progreso\|DEC-005]]) | ✅ Bien |
| **Health check / puerto de gestión** | `8011`, `FlywayHealthIndicator` saca de readiness si faltan migraciones | ✅ Bien |
| **Sidecar** (Tailscale) | `.tpi/platform/docker-compose.mesh.yml` (`network_mode: service:mesh`) | ✅ Bien |
| **Timeouts** | `clients/ClientHttpTimeouts` | ✅ Bien, pero sin circuit breaker (§4.3) |
| **CQRS / proyección Neo4j** | `graph/` (modelos OGM, repos, `GraphPersistenceConfig`) | 🔴 Incompleto: nada fuera de `graph/` usa esos repos y no existe el proyector ([[decisiones/DEC-016-neo4j-para-la-estructura-del-roadmap\|DEC-016]], [[decisiones/DEC-021-postgres-fuente-de-verdad-neo4j-proyeccion\|DEC-021]]) |
| **Service virtualization** (repo `tpi-roadmap-mocks`) | Mocks Node.js que se registran en Eureka real y publican en Kafka real, con inyección de fallas (`/mock/fault`) | ✅ Bien |

## 4. Veredicto

### ✅ Lo que está perfecto (no tocar)

1. **Composite + Interpreter en `rules/`.** Es el mejor código GoF del repo y de toda la plataforma para este problema: interfaz sellada, árbol inmutable, evaluador puro y testeable sin Spring, y persistencia detrás de un puerto.
2. **Ledger de XP idempotente.** Una restricción `UNIQUE` en la base, sin tabla inbox aparte. Es lo mínimo que garantiza idempotencia.
3. **Clientes por interfaz con doble en memoria y validación de arranque.** Permite testear sin red y garantiza que en `integrated` no quede un stub.
4. **Fail-closed del Gate** (`origin_unavailable`): degradación explícita y honesta.
5. **Cache-aside de PAR invalidada por Kafka**: frescura sin hacer polling.
6. **`RankingRules` como cadena de `Comparator`**: el desempate en cascada se lee igual que el requisito.

### 🟡 Lo que se puede mejorar

1. **Outbox: transacción abierta durante el envío a Kafka.** `events/outbox/OutboxPoller.java:65` (`@Transactional`) envuelve `kafkaTemplate.send(...).get(timeout)` (`:96-97`). Mientras Kafka responde, quedan tomadas la conexión de Hikari y las filas bloqueadas.
   - Arreglo: reclamar y marcar el lote en una transacción corta, enviar fuera de ella y marcar `PUBLISHED`/`FAILED` en otra.
   - Referencia en la plataforma: `tpi-sandbox` (`executions/adapter/OutboxRelay`, con `TransactionTemplate`) y `tpi-users` (outbox con *leases*).
2. **Outbox: faltan eventos documentados.** `COURSE_LEVEL_UP` y `PERFORMANCE_ZONE_CHANGED` no aparecen en ningún `.java`. Sin embargo, `AGENTS.md` y [[arquitectura/contexto-integral]] dicen que se publican. O se implementan, o se corrigen los docs.
3. **Facades que crecieron hasta ser God classes:**
   - `GraphService` (897 líneas), `RankingService` (514) y `RoadmapEventListener` (449). Las tres llevan `@SuppressWarnings("PMD.GodClass")`.
   - Partir `GraphService` por caso de uso: edición de nodos, orden, baja y reglas.
4. **Despacho de eventos en `RoadmapEventListener`.** Usa cadenas `if/else` por `eventType` (`:163-169` y `:198-202`). Un `Map<String, Handler>` (Strategy) deja un handler por evento y saca la supresión de PMD.
   - Hacerlo **cuando se sume el próximo tipo de evento**, no antes.
5. **Insignias sin otorgar.** `BadgeCriterion` define `SECTION_NO_LIVES_LOST`, `NODE_NO_RETRIES` y `LIFE_RECOVERED`, pero `BadgeEvaluator.meets` los manda a `default -> false`. Ninguna insignia con esos criterios se otorga nunca.
6. **Neo4j (DEC-016/021).** Hay que decidir entre dos caminos:
   - terminar el proyector (Postgres → Neo4j, después del commit);
   - sacar el módulo `graph/` hasta que haga falta.

   Hoy suma dependencias y configuración sin uso.
7. **Hipótesis (sin verificar):** posible N+1 al cargar roadmap → secciones → nodos con `toModel()` sobre relaciones *lazy*. Verificar con el log de SQL antes de agregar `@EntityGraph`/`JOIN FETCH`.

### ➕ Lo que conviene implementar

1. **Circuit Breaker (Resilience4j) en los clientes de Courses y Accounting.** El Gate y el ranking llaman de forma sincrónica. Con el origen lento, cada request espera el timeout completo de `ClientHttpTimeouts` y se puede agotar el pool de Tomcat. El breaker corta rápido y el Gate ya sabe responder `origin_unavailable`.
   - Referencias en la plataforma: `tpi-theoristcal-challenge` (`services/CoursesCallGuard` + `configs/CoursesClientConfig`) y `tpi-market` (`CourseCircuitBreaker`).
2. **Strategy por tipo de evento en el listener.** Es el punto 4 de mejoras, cuando toque.

### ❌ Lo que NO conviene implementar ahora

- **Chain of Responsibility o Specification en `GateEvaluator`.** Son 5 chequeos en orden, con la parte común ya extraída a `commonBlockReason`, y la variante de lectura reutiliza `unlockBlock`. Convertir cada regla en un bean suma clases sin resolver un problema actual. Reconsiderarlo si las reglas pasan a ser configurables por curso.
- **State GoF para `NodeStatus`/`OutboxStatus`.** Tres estados con transiciones simples: un `enum` alcanza.
- **Domain events internos (`ApplicationEventPublisher`).** El outbox ya cumple ese rol para lo que sale del micro.

## 5. Antipatrones detectados

| Olor | Dónde | Nota |
|---|---|---|
| God class suprimida | `services/GraphService.java:50`, `services/RankingService.java:56`, `events/RoadmapEventListener.java:42` | Ver §4 mejoras 3 y 4 |
| E/S de red dentro de una transacción SQL | `events/outbox/OutboxPoller.java:65-97` | Ver §4 mejora 1 |
| Modelo anémico | `entities/*` | Aceptable por la separación `entities → models`. No es prioridad |
| Fallback con constantes | `RoadmapEventListener` (XP base por dificultad si Backoffice no responde) | Documentado en el Javadoc como excepción deliberada. Revisar que siga alineado con [[decisiones/DEC-013-roadmap-no-calcula-xp-ledger-idempotente\|DEC-013]] (el Motor calcula el XP) |

## 6. Decisiones contra código

| Decisión | ¿Se cumple? |
|---|---|
| DEC-001, 003, 004, 005, 007, 008, 009, 010, 011, 012, 013, 014, 015, 018, 019, 020 | Sí |
| [[decisiones/DEC-002-outbox-transaccional-eventos-salientes\|DEC-002]] Outbox | Parcial: faltan `COURSE_LEVEL_UP` y `PERFORMANCE_ZONE_CHANGED` |
| [[decisiones/DEC-006-insignias-sistema-y-curso\|DEC-006]] Insignias | Parcial: 3 criterios nunca se otorgan |
| [[decisiones/DEC-016-neo4j-para-la-estructura-del-roadmap\|DEC-016]] / [[decisiones/DEC-021-postgres-fuente-de-verdad-neo4j-proyeccion\|DEC-021]] Neo4j | No: módulo sin uso y sin proyector |
| [[decisiones/DEC-017-n-roadmaps-por-curso-configurables\|DEC-017]] N roadmaps | Sí (`is_primary`, `RoadmapResolver`) |

Las deudas que salen de acá están en [[deuda-tecnica]] (DT-22 a DT-26).
