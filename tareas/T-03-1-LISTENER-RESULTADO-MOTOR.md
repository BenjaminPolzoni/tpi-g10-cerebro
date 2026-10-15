# T-03.1 — Listener del evento de resultado del Motor

Plan de implementación de la tarea T-03.1 de **HU-03** (consumir el resultado del Motor y
registrar XP y progreso). Contexto funcional en `agent.md` §3.0, §3.1 y §5; contrato de
integración en `docs/T-01-7-EUREKA-GATEWAY.md`.

> **Alcance de T-03.1**: `@KafkaListener` tipado, con `group-id` propio, que valida el envelope
> y delega en el servicio de progreso dentro de una transacción; errores no reintentables a DLQ
> (P-09) y poison pills registradas y salteadas sin frenar el offset.

---

## 1. Qué ya está construido

| Pieza | Dónde | Estado |
|---|---|---|
| Registro del resultado, transaccional e idempotente por `eventId` | `ProgressService.recordResult` | Hecho |
| `xp_movement` append-only con `event_id UUID NOT NULL UNIQUE` | `V1__esquema_inicial.sql` | Hecho |
| `completed_node` con `uq_completed_node (student_id, node_id)` | `V1__esquema_inicial.sql` | Hecho |
| Suma de XP y derivación de vidas perdidas | `StudentCourse.applyResult` | Hecho |
| Desbloqueo AND/OR y congelado de desbloqueos alcanzados | `PrerequisiteService` | Hecho |
| Test del duplicado at-least-once | `RoadmapFlowTest` | Hecho |

**No existe nada de Kafka**: ni dependencia en el `pom.xml`, ni configuración, ni broker en
`docker/docker-compose.yml`. Los únicos llamadores de `recordResult` son el seeder `demo` y los tests.

---

## 2. Huecos: lo que falta y lo que está bloqueado

### 2.1 Bloqueantes externos (no se inventan, `agent.md` §10)

| # | Hueco | Bloquea | Mitigación en este plan |
|---|---|---|---|
| B1 | **Topic** donde publica el Motor (P-09, Notificaciones) | `topics` del listener | Property `app.kafka.topics.challenge-result` con valor propuesto; se cambia por entorno sin tocar código |
| ~~B2~~ | ~~Contrato del payload (REQ-MOT-02)~~ | — | **Resuelto**: contrato acordado en §3.2. `nodeId`, `consumeVida` y `esRepeticion` quedan a confirmar con el Motor; se ignoran campos desconocidos (§5.4) |
| B3 | **Topic de DLQ y política de reintentos** (P-09) | `DeadLetterPublishingRecoverer` | Property `app.kafka.topics.dlq`, vacía por defecto: sin DLQ, el error no reintentable se registra y se saltea |
| B4 | **Delta o total** en los ajustes (REQ-MOT-04, Grupo 09) | Nada de esta tarea | Fuera de T-03.1: solo se consume `CHALLENGE_COMPLETED` |
| B5 | **Message key** (propuesta `studentId`, a confirmar) | Nada del consumidor | Solo afecta al productor; se documenta |

Ninguno frena la tarea: todos salen por properties. Lo que **sí** hay que dejar marcado en el
código y en el PR es que el valor por defecto es una propuesta nuestra, igual que se hizo con
`COURSES_CONTENTS_BATCH_PATH` en T-03.4.

### 2.2 Huecos del código nuestro

| # | Hueco | Decisión |
|---|---|---|
| H1 | `ChallengeResult` no tiene `esRepeticion` ni `nodeId` | Se agregan al DTO del evento; el descarte por repetición vive en el service (regla de negocio, testeable sin broker) |
| H2 | `recordResult` lanza `ApiException(404)` si el alumno no está matriculado | En un listener una excepción reintenta para siempre. Hay que **clasificar**: no reintentable → log + offset avanzado (CA4) |
| H3 | Carrera de idempotencia: `existsByEventId` + insert no es atómico | Con 120 eventos concurrentes dos hilos pasan el check. Atrapar `DataIntegrityViolationException` → no-op, mismo patrón que `ProgressService.insertReading` |
| H4 | La HU pide validar que `nodeId` **y** `challengeId` son del curso | Hoy el nodo se busca solo por `challengeId`. Se agrega la verificación cruzada de `nodeId` |
| H5 | "Evalúa los desbloqueos" (CA1) | El desbloqueo **ya es derivado**: `PrerequisiteService.isSatisfied` lo calcula al leer. No se agrega persistencia nueva; `node_unlock` sigue siendo solo el congelado de HU-13 |
| H6 | `GET /api/roadmap/historial-xp` | `@Profile("!prod")` sobre un controller aparte. El resto de la API está en inglés: se propone `/api/roadmap/xp-history` y se deja la decisión al equipo |
| H7 | Sin broker en Compose ni en tests | Tests sin `@EmbeddedKafka`: el listener se invoca como POJO. No arranca un broker en CI |

---

## 3. Diseño

```
Kafka ──► RoadmapEventListener (@KafkaListener, groupId roadmap-service)
            1. valida el envelope: 5 campos obligatorios
            2. eventType desconocido  → log + return (offset avanza, §5.4)
            3. payload tipado         → ChallengeCompletedPayload
            4. delega                 → ProgressService.recordResult(...)   @Transactional
                 · esRepeticion=true      → no-op (REQ-MOT-03)
                 · eventId ya registrado  → no-op (idempotencia)
                 · alumno/nodo inválido   → NonRetryableEventException
            5. DefaultErrorHandler clasifica:
                 · NonRetryableEventException, deserialización → log + DLQ si está configurada
                 · el resto (BD caída, etc.)                   → backoff y reintento
```

### 3.1 Archivos nuevos

```
src/main/java/com/utn/tpi/roadmap/
├── events/
│   ├── EventEnvelope.java              Envelope del PDF del bus (5 campos, sin eventVersion)
│   ├── ChallengeCompletedPayload.java  Payload propuesto (B2)
│   ├── RoadmapEventListener.java       @KafkaListener
│   ├── NonRetryableEventException.java Marca lo que no mejora por reintentar
│   └── KafkaConsumerConfig.java        ErrorHandler, clasificación y DLQ opcional
└── controllers/XpHistoryController.java  @Profile("!prod"), depuración (H6)
```

Sin `events/dto/`, sin interfaz de listener, sin mapper: un record por mensaje y un método por
`eventType`. El paquete `events/` se comparte después con el outbox de T-01.12.5.

### 3.2 Envelope y payload

```java
record EventEnvelope<T>(UUID eventId, String eventType, Instant timestamp, String producer, T payload) { }
```

Los cinco campos son obligatorios: si falta alguno, es poison pill (log + skip). `eventType` en
SNAKE inglés; sin `eventVersion` (D-KAFKA).

Contrato acordado de `CHALLENGE_COMPLETED` (producer `challenge-service`):

```json
{
  "eventId": "123e4567-e89b-12d3-a456-426614174000",
  "eventType": "CHALLENGE_COMPLETED",
  "timestamp": "2026-09-02T19:30:00Z",
  "producer": "challenge-service",
  "payload": {
    "courseId": "uuid", "studentId": "uuid", "challengeId": "uuid", "nodeId": "uuid",
    "xp": 250, "lives": 2, "passed": true, "consumeVida": true, "esRepeticion": false
  }
}
```

```java
record ChallengeCompletedPayload(UUID courseId, UUID studentId, UUID challengeId, UUID nodeId,
                                 long xp, int lives, boolean passed, boolean consumeVida,
                                 boolean esRepeticion) { }
```

- `xp`, `lives` y `passed` mapean uno a uno con el `ChallengeResult` actual: el DTO interno no cambia.
- `nodeId`, `consumeVida` y `esRepeticion` son los campos que agrega §5.5, **a confirmar con el Motor**.
- **`consumeVida` se deserializa pero no se usa**: las vidas las descuenta Inventario (§2.2). Se deja
  en el record para no perderlo y para documentar que la decisión es deliberada.
- `lives` llega como **valor vigente**, que es lo que `StudentCourse.applyResult` necesita para
  derivar las vidas perdidas (RF-RNK-05/11/12).
- Sigue pendiente el **topic** (B1) y si el ajuste posterior viaja como delta o total (B4).

### 3.3 Properties

```properties
##### Kafka (T-03.1) #####
spring.kafka.bootstrap-servers=${KAFKA_BOOTSTRAP:localhost:29092}
spring.kafka.consumer.group-id=roadmap-service
spring.kafka.consumer.auto-offset-reset=earliest
spring.kafka.listener.concurrency=${KAFKA_CONCURRENCY:3}
# PENDIENTE (P-09): topic y DLQ son propuestas nuestras hasta el acta con Notificaciones.
app.kafka.topics.challenge-result=${KAFKA_TOPIC_CHALLENGE_RESULT:challenge-events}
app.kafka.topics.dlq=${KAFKA_TOPIC_DLQ:}
app.kafka.enabled=${KAFKA_ENABLED:true}
```

`app.kafka.enabled=false` solo en tests (sin broker, H7). En Compose el default es `true`: el servicio
`event-bus` levanta el broker y `docker/docker-compose.yml` reenvía `KAFKA_CONCURRENCY`, los dos topics y
`KAFKA_ENABLED` al contenedor `app`, coherente con `.env.example`.

### 3.4 Clasificación de errores

| Situación | Clase | Qué hace |
|---|---|---|
| Envelope incompleto, JSON ilegible | Poison pill | Log `WARN` con el `eventId` si se pudo leer; offset avanza |
| `eventType` desconocido | Ignorado | Log `INFO`; offset avanza, sin interpretar (§5.4) |
| Alumno no matriculado, nodo o desafío ajenos al curso | `NonRetryableEventException` | Log `WARN` + DLQ si está configurada; offset avanza (CA4) |
| `esRepeticion = true` | Descarte de negocio | No es error: log `DEBUG`, sin registro (CA2) |
| `eventId` ya registrado | Idempotencia | No-op silencioso (CA3) |
| BD caída, timeout | Reintentable | `DefaultErrorHandler` con `ExponentialBackOff`, tope de intentos, después DLQ |

**Nunca** se frena el offset por un mensaje que no va a poder procesarse: sería bloquear la
partición entera (§5.4).

---

## 4. Pasos

1. **`pom.xml`**: agregar `spring-kafka` sin versión explícita (la fija el BOM de Spring Boot 4.0.0).
2. **`events/EventEnvelope` + `ChallengeCompletedPayload`**: records con Javadoc por campo (Checkstyle).
3. **`ProgressService`**: extender `recordResult` con `esRepeticion` (H1), verificación cruzada de
   `nodeId` (H4), `DataIntegrityViolationException` → no-op (H3) y `NonRetryableEventException` en
   lugar de `ApiException` para lo que llega por evento (H2). Adaptar el seeder `demo` y
   `RoadmapFlowTest` en el mismo commit.
4. **`RoadmapEventListener`**: `@KafkaListener(topics = "${app.kafka.topics.challenge-result}")`,
   validación del envelope, ruteo por `eventType`, delegación.
5. **`KafkaConsumerConfig`**: `DefaultErrorHandler`, `ExponentialBackOff`,
   `addNotRetryableExceptions`, `DeadLetterPublishingRecoverer` solo si `app.kafka.topics.dlq`
   tiene valor. `@ConditionalOnProperty(app.kafka.enabled)`.
6. **`XpHistoryController`**: `@Profile("!prod")`, `GET` paginado de `xp_movement` por alumno y curso.
7. **`docker/docker-compose.yml`**: servicio `event-bus` (`apache/kafka` en modo KRaft, §6) y
   `KAFKA_BOOTSTRAP` en la app. `.env.example` con las variables nuevas.
8. **Tests** (`ChallengeResultListenerTest`, sin broker):
   - CA1 / BDD-1: `CHALLENGE_COMPLETED` aprobado → `xp_movement` + `completed_node` + el nodo
     siguiente queda desbloqueado.
   - CA2 / BDD-3: `esRepeticion = true` → sin cambios en base.
   - CA3 / BDD-2: mismo `eventId` dos veces → un solo movimiento; más el caso concurrente (H3).
   - CA4 / BDD-4: alumno no matriculado → sin registro y sin excepción que frene el offset.
   - Envelope incompleto y `eventType` desconocido → skip.
9. **`mvn verify`** local antes de pushear (hook `pre-push`); actualizar `README.md` y
   `docs/ESTRUCTURA.md` con el paquete `events/`.

---

## 5. Fuera de alcance de T-03.1

- Outbox y emisión de `NODE_COMPLETED` / `NODE_UNLOCKED` (T-01.12.5).
- Ajustes posteriores de XP, REQ-MOT-04 (falta B4).
- Consumo de eventos de Courses, Inventario o BackOffice.
- Niveles y ranking: dependen del XP registrado, pero son historias aparte.

---

## 6. Preguntas para el equipo antes de cerrar el PR

1. Motor (acta del día 3): idioma de los campos del payload, vidas vigentes vs. `consumeVida`, y si
   `courseId` / `studentId` viajan en el payload (B2).
2. Notificaciones (P-09): topic del resultado, topic de DLQ y política de reintentos (B1, B3).
3. Equipo: `/api/roadmap/historial-xp` en español o `/api/roadmap/xp-history` en inglés, y cuál es
   el nombre del perfil de producción para el `@Profile` (H6).
