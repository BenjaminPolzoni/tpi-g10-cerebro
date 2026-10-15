# T-01.12.5 — Outbox con reintentos y DLQ para eventos propios

Plan de implementación de la tarea T-01.12.5 de **HT-01**. Contexto normativo en `agent.md` §5.1,
§5.3 y §5.5; contrato de los eventos en `docs/contracts/bus-notificaciones.md` §3–§5 (P-09, sin acta).

> **Alcance**: tabla `outbox_event`, poller `@Scheduled` con `FOR UPDATE SKIP LOCKED`, reintentos y
> estado `FAILED` como DLQ del productor, y emisión de **`NODE_COMPLETED`** y **`NODE_UNLOCKED`**
> desde la misma transacción de negocio. **Nunca `kafkaTemplate.send()` en la lógica de negocio**:
> el único `send` del productor vive en el poller.

Rama: `feature/t-01-12-5-outbox` (desde `develop` `4712f68`). Trazabilidad: HT-01, T-01.12.5,
RF-NFR-01, P-09 (B5), agent.md §5.3.

---

## 1. Decisiones de esta tarea (acordadas con el equipo, 2026-09-26)

| Id | Decisión | Por qué |
|---|---|---|
| D-T01125-01 | **Topic de salida por property, vacío por defecto**: `app.kafka.topics.roadmap-events=${KAFKA_TOPIC_ROADMAP:}`. Vacío ⇒ el poller no publica y las filas quedan `PENDING`. Message key = **`studentId`** (propuesta B5). | P-09 sin acta, la lista del bus no trae topic de Roadmap y está prohibido crear topics. Nada se pierde: al llegar el acta se configura la variable y se publica lo acumulado. Mismo patrón que `app.kafka.topics.dlq`. |
| D-T01125-02 | **Solo `NODE_COMPLETED` y `NODE_UNLOCKED`**. `COURSE_LEVEL_UP` y `PERFORMANCE_ZONE_CHANGED` quedan fuera. `BADGE_AWARDED` es Fase 2. | Son los únicos con punto de disparo ya construido. Niveles y ranking no existen todavía. |
| D-T01125-03 | **`NODE_UNLOCKED` solo con origen `PROGRESS`**. `freezeReachedUnlocks` (`RULE_CHANGE`) **no emite**. | El congelado preserva lo que el alumno ya alcanzaba: no hay nada nuevo que avisarle. |
| D-T01125-04 | **DLQ del productor = estado `FAILED` en la tabla** con `last_error`, tras `OUTBOX_MAX_ATTEMPTS` (5). Sin topic DLQ extra. Reencolar = `UPDATE ... SET status='PENDING', attempts=0` a mano. | Si el broker está caído, un topic DLQ tampoco llegaría. P-09 (P11-13) todavía no define la DLQ del bus. |
| D-T01125-05 | **El envelope completo se serializa al encolar** (columna `payload` = JSON del `EventEnvelope`). | `eventId` y `timestamp` quedan fijos: cada reintento republica **el mismo** `eventId`, así los consumidores deduplican (at-least-once). |
| D-T01125-06 | **Nombres en inglés** (`outbox_event`, `PENDING`/`PUBLISHED`/`FAILED`, `attempts`, `destination_topic`). | Esquema en inglés desde V2. `agent.md` §5.3 usa los nombres en español como descripción, no como literal. |
| D-T01125-07 | **`courseId` del payload = `courseCohortId`** (igual que `ChallengeResult`, `@JsonProperty("courseId")`). | Contrato del bus en `bus-notificaciones.md` §3; el dominio interno usa cohorte desde V12. |
| D-T01125-08 | `outbox_event` lleva **`course_cohort_id`** y **`deleted_at`**, sin purga automática. | Regla de HT-01 / DoD nivel 1 (toda entidad con curso-cohorte y baja lógica, RF-NFR-01, PAR-16). |

---

## 2. Qué ya está construido (no tocar salvo lo indicado)

- `services/ProgressService.recordResult(eventId, result)`: una sola `@Transactional`. Inserta
  `xp_movement`, suma `total_xp` y, si `result.passed()`, guarda `CompletedNodeEntity` y llama a
  `prerequisites.recordUnlocksAfter(node.getId(), studentId, eventId)`. Es el **punto de disparo**
  de los dos eventos. Tiene a mano `result.courseCohortId()`, `result.studentId()`,
  `result.challengeId()`, `node.getId()` y `section.getId()`.
- `services/PrerequisiteService.recordUnlocksAfter(...)`: calcula `inserted` (los nodos que **esta**
  transacción desbloqueó de verdad vía `insertIfAbsent`). Hoy devuelve `void`. Su **único** llamador
  es `ProgressService:179`.
- `events/EventEnvelope<T>`: record con los 5 campos del bus y el constructor de conveniencia
  `(UUID, String, Instant, String, T)`. `timestamp` se escribe como string ISO (`@JsonFormat`).
- `entities/BaseEntity`: `id` UUID `@GeneratedValue`, `created_at`, `deleted_at` y `softDelete()`.
  Cada entidad agrega `@SQLRestriction("deleted_at IS NULL")`.
- `events/KafkaConsumerConfig`: `@ConditionalOnProperty(app.kafka.enabled, matchIfMissing=true)` y
  usa el `KafkaTemplate<Object, Object>` autoconfigurado para la DLQ del **consumidor**. No se toca.
- Tests: H2 en modo PostgreSQL + Flyway real + `ddl-auto=validate` y `app.kafka.enabled=false`
  (`src/test/resources/application.properties`). Los beans de Kafka no existen en tests: los que
  dependen de Kafka se instancian a mano, como `ParRefreshListener`.
- Jackson: el proyecto inyecta `com.fasterxml.jackson.databind.ObjectMapper` (ver
  `clients/backoffice/ParCatalogConfig`). Usar el mismo bean, no crear uno nuevo.
- Última migración: `V14__node_lives_policy.sql` ⇒ la nueva es **`V15`**.

---

## 3. Diseño

```
ProgressService.recordResult  (@Transactional)
  ├─ xp_movement, total_xp, completed_node        (igual que hoy)
  ├─ OutboxService.enqueue(NODE_COMPLETED ...)    ─┐ misma transacción
  └─ for nodeId in recordUnlocksAfter(...)         │ (Propagation.MANDATORY)
        OutboxService.enqueue(NODE_UNLOCKED ...)  ─┘ → INSERT outbox_event (PENDING)

OutboxPoller  @Scheduled(fixedDelay = OUTBOX_POLL_INTERVAL_MS)   [solo si app.kafka.enabled]
  topic vacío → return (log WARN una sola vez)
  @Transactional:
    SELECT ... WHERE status='PENDING' AND deleted_at IS NULL
      ORDER BY created_at LIMIT :batch FOR UPDATE SKIP LOCKED
    por fila: kafkaTemplate.send(topic, messageKey, payload).get(timeout)
      ok    → PUBLISHED, published_at=now, destination_topic=topic
      error → attempts++, last_error; attempts >= max → FAILED
```

### 3.1 Migración `src/main/resources/db/migration/V15__outbox_event.sql`

```sql
CREATE TABLE outbox_event (
    id                UUID          PRIMARY KEY,
    event_id          UUID          NOT NULL,
    event_type        VARCHAR(64)   NOT NULL,
    aggregate_type    VARCHAR(64)   NOT NULL,
    aggregate_id      UUID          NOT NULL,
    course_cohort_id  UUID          NOT NULL,
    message_key       VARCHAR(64)   NOT NULL,
    payload           TEXT          NOT NULL,
    status            VARCHAR(16)   NOT NULL DEFAULT 'PENDING',
    attempts          INTEGER       NOT NULL DEFAULT 0,
    last_error        VARCHAR(1000),
    destination_topic VARCHAR(255),
    created_at        TIMESTAMP WITH TIME ZONE NOT NULL,
    published_at      TIMESTAMP WITH TIME ZONE,
    deleted_at        TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_outbox_event_event_id UNIQUE (event_id),
    CONSTRAINT ck_outbox_event_status CHECK (status IN ('PENDING', 'PUBLISHED', 'FAILED'))
);
CREATE INDEX ix_outbox_event_pending ON outbox_event (status, created_at);
```

- `payload` va como `TEXT` y no como `JSONB`: H2 no mapea JSONB y los tests validan el esquema con
  `ddl-auto=validate`. El consumidor recibe un string JSON igual. Dejarlo comentado en la migración.
- Antes de escribirla, revisar V1/V12 para copiar el tipo de timestamp que ya usa el proyecto
  (`TIMESTAMP WITH TIME ZONE` vs `TIMESTAMP`) y respetarlo.
- `destination_topic` se completa **al publicar**, no al encolar (D-T01125-01): así las filas creadas
  antes del acta toman el topic que se configure después.

### 3.2 Modelo: paquete `com.utn.tpi.roadmap.events.outbox`

Un paquete nuevo y chico, con todo lo del productor:

| Clase | Qué es |
|---|---|
| `OutboxStatus` | enum `PENDING`, `PUBLISHED`, `FAILED`. |
| `OutboxEventEntity` | `@Entity @Table(name="outbox_event")`, extiende `BaseEntity`, `@SQLRestriction("deleted_at IS NULL")`, Lombok como las demás entidades (`@Getter @Builder @NoArgsConstructor @AllArgsConstructor`, mirar `XpMovementEntity`). `status` como `@Enumerated(STRING)`. Métodos de dominio: `markPublished(String topic, Instant at)` y `markFailedAttempt(String error, int maxAttempts)`, que hace `attempts++`, guarda `last_error` truncado a 1000 y pasa a `FAILED` si `attempts >= maxAttempts`. |
| `OutboxEventRepository` | `JpaRepository<OutboxEventEntity, UUID>` + `@Query(nativeQuery = true)` `lockPendingBatch(int limit)` con el SELECT de §3 (`FOR UPDATE SKIP LOCKED`), + `findByEventId` / `countByStatus` para tests. |
| `OutboxProperties` | `@ConfigurationProperties("app.outbox")` record: `pollIntervalMs` (3000), `maxAttempts` (5), `batchSize` (50), `sendTimeout` (`Duration`, 10s). Mirar cómo están hechas las otras `*Properties` en `clients/` y registrarla igual (`@EnableConfigurationProperties` o `@ConfigurationPropertiesScan`, lo que ya se use). |
| `OutboxService` | `@Service`. `@Transactional(propagation = Propagation.MANDATORY) void enqueue(String eventType, String aggregateType, UUID aggregateId, UUID courseCohortId, UUID studentId, Object payload)`. Arma `new EventEnvelope<>(UUID.randomUUID(), eventType, Instant.now(), producer, payload)`, lo serializa con el `ObjectMapper` inyectado y guarda la fila `PENDING` con `message_key = studentId.toString()`. `producer` sale de `spring.application.name` (`roadmap-service`), no se escribe a mano. `MANDATORY` hace que falle fuerte si alguien lo llama fuera de una transacción de negocio. **No toca Kafka.** |
| `OutboxPoller` | `@Component @ConditionalOnProperty(prefix="app.kafka", name="enabled", havingValue="true", matchIfMissing=true)`. Inyecta `KafkaTemplate<Object, Object>` (el autoconfigurado; los serializers por defecto de Boot son `StringSerializer`, así que viaja el JSON tal cual), el repo, `OutboxProperties` y `@Value("${app.kafka.topics.roadmap-events:}") String topic`. `@Scheduled(fixedDelayString = "${app.outbox.poll-interval-ms:3000}") @Transactional public void publishPending()`: aplica el flujo de §3. Cada `send(...).get(sendTimeout)` se envuelve en try/catch (`ExecutionException`, `TimeoutException`, `KafkaException`); ante `InterruptedException`, re-interrumpir el hilo y cortar el lote. Si el topic está vacío, loguea WARN **una sola vez** (flag `AtomicBoolean`) y retorna sin tocar la base. Los logs llevan `eventId` y `eventType`, **nunca el payload** (agent.md §4.5). |
| `OutboxSchedulingConfig` | `@Configuration @EnableScheduling` con el mismo `@ConditionalOnProperty(app.kafka.enabled)`. Es el primer `@Scheduled` del proyecto; en tests no se registra. |

Payloads tipados (records en `com.utn.tpi.roadmap.events`, junto a los demás `*Payload`):

```java
public record NodeCompletedPayload(@JsonProperty("courseId") UUID courseCohortId, UUID studentId,
                                   UUID nodeId, UUID challengeId, UUID sectionId) { }
public record NodeUnlockedPayload(@JsonProperty("courseId") UUID courseCohortId, UUID studentId,
                                  UUID nodeId) { }
```

Constantes de `eventType` (`"NODE_COMPLETED"`, `"NODE_UNLOCKED"`) y de `aggregateType` (`"NODE"`):
dejarlas en un solo lugar, por ejemplo como constantes públicas de `OutboxService` o de cada payload.
Nada de literales sueltos en `ProgressService`.

> ponytail: el poller mantiene la transacción (y los locks de fila) abierta mientras espera el ack de
> cada `send`. Con `batchSize=50` y `sendTimeout` de 10 s alcanza para 120 sesiones. Si algún día hace
> falta más throughput, pasar a "reclamar → commit → publicar → marcar" en dos transacciones.
> Dejar este comentario en el código.

### 3.3 Cambios en el negocio (los únicos)

1. **`PrerequisiteService.recordUnlocksAfter`**: pasa de `void` a `List<UUID>` y devuelve `inserted`,
   los nodos que esta transacción desbloqueó de verdad. No se agregan dependencias al outbox:
   `PrerequisiteService` sigue sin saber de eventos. Actualizar su Javadoc (`@return`).
2. **`ProgressService.recordResult`**, dentro del `if (result.passed() && !alreadyPassed)`, después
   de `completedNodes.save(...)`:
   ```java
   outbox.enqueue(NODE_COMPLETED, NODE, node.getId(), result.courseCohortId(), result.studentId(),
           new NodeCompletedPayload(result.courseCohortId(), result.studentId(), node.getId(),
                   result.challengeId(), section.getId()));
   prerequisites.recordUnlocksAfter(node.getId(), result.studentId(), eventId)
           .forEach(unlocked -> outbox.enqueue(NODE_UNLOCKED, NODE, unlocked, result.courseCohortId(),
                   result.studentId(),
                   new NodeUnlockedPayload(result.courseCohortId(), result.studentId(), unlocked)));
   ```
   Inyectar `OutboxService` como `private final`, con su Javadoc de campo como los demás (Checkstyle).
3. **`freezeReachedUnlocks` no se toca** (D-T01125-03).
4. El duplicado por `eventId` y `esRepeticion` ya salen **antes** de este bloque, así que no encolan
   nada. Solo hay que cubrirlo con tests.

### 3.4 Configuración

`src/main/resources/application.properties`: agregar un bloque nuevo después de `##### Kafka`:

```properties
##### Outbox (T-01.12.5) #####
# PENDIENTE (P-09): sin topic asignado a Roadmap en el bus. Vacío = no se publica y las filas
# quedan PENDING hasta que se configure (D-T01125-01). Key = studentId (propuesta B5).
app.kafka.topics.roadmap-events=${KAFKA_TOPIC_ROADMAP:}
app.outbox.poll-interval-ms=${OUTBOX_POLL_INTERVAL_MS:3000}
app.outbox.max-attempts=${OUTBOX_MAX_ATTEMPTS:5}
app.outbox.batch-size=${OUTBOX_BATCH_SIZE:50}
app.outbox.send-timeout=${OUTBOX_SEND_TIMEOUT:10s}
```

- `src/test/resources/application.properties`: mismas claves con valores fijos
  (`app.kafka.topics.roadmap-events=` vacío).
- `.env.example`: agregar `KAFKA_TOPIC_ROADMAP=` (con el comentario de P-09),
  `OUTBOX_POLL_INTERVAL_MS=3000`, `OUTBOX_MAX_ATTEMPTS=5` y `OUTBOX_BATCH_SIZE=50`.
- `docker/docker-compose.yml`, servicio `app`: `KAFKA_TOPIC_ROADMAP: ${KAFKA_TOPIC_ROADMAP:-}`.
- Revisar si la configuración del productor de Kafka necesita algo más. Por defecto Boot usa
  `StringSerializer` para key y value: **no agregar** `spring.kafka.producer.*` salvo que un test
  demuestre que hace falta.

---

## 4. Tests (H2, sin broker)

Seguir el estilo de `NodeUnlockOnResultTest` y `ProgressServiceIntegrityViolationTest` (mismos
helpers de `support/` para armar roadmap, nodos, aristas e inscripción).

**`OutboxEmissionTest`** (`@SpringBootTest`, llama a `ProgressService.recordResult`):
1. Resultado aprobado en un nodo con dos sucesores alcanzables ⇒ 1 fila `NODE_COMPLETED` y 2
   `NODE_UNLOCKED`, todas `PENDING`, `message_key = studentId`, `course_cohort_id` correcto.
2. El `payload` de la fila, parseado, tiene los **5 campos del envelope**, `producer =
   "roadmap-service"`, `eventType` correcto y `payload.courseId/studentId/nodeId`
   (+ `challengeId` y `sectionId` en `NODE_COMPLETED`).
3. Mismo `eventId` dos veces ⇒ sigue habiendo exactamente las mismas filas (idempotencia).
4. `passed = false` ⇒ 0 filas.
5. Nodo sin sucesores ⇒ solo `NODE_COMPLETED`.
6. AND con un solo prerrequisito aprobado ⇒ 0 `NODE_UNLOCKED`.
7. `freezeReachedUnlocks` ⇒ 0 filas (D-T01125-03).
8. **Atomicidad**: si la transacción de negocio falla después de encolar (por ejemplo, alumno no
   matriculado que ya no llega, o forzando una excepción con un spy), no queda ninguna fila en
   `outbox_event`.
9. `OutboxService.enqueue` fuera de una transacción ⇒ `IllegalTransactionStateException` (`MANDATORY`).

**`OutboxPollerTest`** (repo real en H2 + `KafkaTemplate` mockeado con Mockito; el poller se
instancia **a mano** porque el bean no existe con `app.kafka.enabled=false`):
1. Topic vacío ⇒ `send` nunca se llama y las filas siguen `PENDING` con `attempts = 0`.
2. `send` OK ⇒ `PUBLISHED`, `published_at` no nulo, `destination_topic = topic`, y `send` recibió
   `(topic, studentId, payload)` exactos.
3. `send` falla ⇒ `attempts = 1`, `last_error` no nulo, sigue `PENDING`.
4. Falla `maxAttempts` veces ⇒ `FAILED`, y en la siguiente corrida **no** se vuelve a enviar.
5. `batchSize` respetado y orden por `created_at`.
6. Filas con `deleted_at` no se publican.

Si H2 no soporta `FOR UPDATE SKIP LOCKED` dentro de la query nativa (H2 2.x debería), **no cambiar
la query de producción**: documentarlo y cubrir el lock con un test marcado solo para Postgres. No
inventar otro mecanismo sin avisar.

---

## 5. Documentación a actualizar

- `docs/ESTRUCTURA.md`: sacar la nota de la línea ~269 ("outbox ... fuera de alcance"), agregar el
  paquete `events/outbox` y sus clases, la tabla `outbox_event` en la sección de entidades, `V15` en
  la lista de migraciones y los dos tests nuevos.
- `docs/contracts/bus-notificaciones.md` §3 y §6: los dos eventos ya se encolan, **se publican
  cuando P5/P9 asignen topic y key**. Qué variable hay que setear (`KAFKA_TOPIC_ROADMAP`).
- **No** modificar `agent.md`.

---

## 6. Definition of Done de la tarea

- [ ] `./mvnw -B clean verify` en verde: tests, Checkstyle y PMD sin violaciones, Javadoc en todo lo
      público (el proyecto lo exige).
- [ ] No hay ningún `kafkaTemplate.send` fuera de `OutboxPoller` (salvo la DLQ del consumidor en
      `KafkaConsumerConfig`, que ya existía). Verificar con `grep -rn "\.send(" src/main`.
- [ ] `outbox_event` tiene `course_cohort_id` y `deleted_at` (DoD nivel 1).
- [ ] Sin constantes de negocio: intervalos, intentos, lote y topic salen de properties/env.
- [ ] Compose local: con `KAFKA_TOPIC_ROADMAP` vacío la app levanta y no loguea errores en bucle;
      con `KAFKA_TOPIC_ROADMAP=roadmap.local.test` (solo prueba local, **no commitear**) las filas
      pasan a `PUBLISHED`.
- [ ] Commits con Conventional Commits como el resto del repo (`feat(outbox): ...`), **sin trailers de IA**
      (sin `Co-Authored-By` de Claude ni de ningún agente).

## 7. Fuera de alcance

`COURSE_LEVEL_UP`, `PERFORMANCE_ZONE_CHANGED`, `BADGE_AWARDED` · topic DLQ del productor ·
endpoint o job para reencolar `FAILED` · purga de `PUBLISHED` (prohibida por PAR-16) · cambiar la
DLQ del consumidor.
