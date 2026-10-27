# Contrato Roadmap ↔ Bus de eventos (Notificaciones, Grupo 2)

Estado: **borrador, sin acta**. Es el pendiente **P-09** de `agent.md` §10.2.
Base: `agent.md` §5.1–§5.5; `docs/T-03-1-LISTENER-RESULTADO-MOTOR.md` §2.1 (B1, B3, B5); contraste actualizado con el contrato de plataforma en `2026-P4-BE/tpi-notifications/docs/contratos-kafka.md` (`main`).

Bloquea: **T-03.2** (topic del evento consumido) y **T-01.12.5** (outbox y eventos propios).

> Regla que ya sabemos: **está prohibido crear topics**. Se usan los del bus; si necesitamos uno,
> se pide a Notificaciones (`agent.md` §5.2). Por eso todo esto depende de ustedes.

---

## 1. Contrato general documentado por Notificaciones

El contrato vigente publicado en el repositorio de Notificaciones define:

- Envelope obligatorio de **6 campos**: `event_id`, `event_type`, `event_version`, `timestamp`, `producer`, `payload`.
- `event_version` es entero obligatorio; el contrato documentado exige `1`.
- `event_type`: hecho pasado, `SCREAMING_SNAKE_CASE`, en **inglés**. Estable una vez publicado.
- `timestamp`: ISO 8601 **UTC**, el momento del hecho (uno solo, no hecho vs. publicación).
- Los campos del envelope se serializan en **snake_case** (`contratos-kafka` v8 en adelante; la versión inicial de este borrador decía camelCase, corregido en DT-18).
- No se crean topics unilateralmente: el broker se aprovisiona centralmente y usa un topic por dominio (`<dominio>.events`).
- La tabla oficial registra `courses.events` y `courses.events.DLT`; para consumidores se documentan 3 reintentos con espera fija de 2 s antes de derivar a la DLT.

El `EventEnvelope` de Roadmap ya modela seis campos y versiona con `event_version`; el doc previo de cinco campos estaba desactualizado. El contrato sigue figurando como borrador en este documento hasta registrar el acuerdo formal aplicable a Roadmap.

---

## 2. Lo que consumimos

| Evento | Productor | Topic | Estado |
|---|---|---|---|
| `CHALLENGE_COMPLETED` / `CHALLENGE_ABORTED` | `tema-03-challenges-service` | `challenges.events` | **Vigente** (`motor-desafios-evento-cierre.md`): `key = id_user`, envelope y payload en snake_case (tpi-roadmap#120) **con** `event_version: 1` (contradice el "sin `event_version`" de §1: abierto con Notificaciones), se filtra por `producer` porque Tema 05 comparte el topic. Reemplaza al formato v2 (`challenges.results`, `key = attemptId`, `producer = "challenges-service"`), que sigue con su listener hasta que el Motor migre |
| Ajuste de XP posterior | `challenge-service` | **?** | `event_type` sin definir (ver contrato de Motor) |
| `ITEM_EQUIP_REQUESTED` / `ITEM_EQUIP_RESULT` | Roadmap ↔ Accounting | `accounting.holds.events` | Request y respuesta por el mismo topic, correlación por `correlationId` = nuestro `event_id`. Acordado con Accounting; firma nominal pendiente |
| `LIVES_EXHAUSTED` / `LIVES_AVAILABLE` | Accounting | `accounting.ledger.events` | Confirmado por el acta Accounting ↔ Roadmap v1; **el código de Roadmap hoy no tiene listener para este topic** (solo `accounting.events`) |
| `LIFE_CREDITED` / `LIFE_DEBITED` | Accounting | `accounting.events` | Consumido por `AccountingEventsListener` para proyectar `recovery_pending` (informativo; el Gate sigue leyendo Accounting). Sobre en snake_case; payload aún camelCase de Accounting (`tpi-accounting#227`), leído con alias |
| Inscripción / archivado de curso | Courses | `courses.events` | Topic de dominio documentado; los nombres/payloads específicos de ciclo de vida quedan en sus contratos de dominio. |
| Cambios de sección/actividad | Courses | `courses.events` | El topic de dominio está documentado; no encontramos contrato de eventos específicos de sección/actividad ni payloads. La tabla de Notificaciones solo describe el dominio Courses en general. |
| Cambios de PAR globales | BackOffice | `administration.events` | `GLOBAL_CONFIGURATION_CHANGED` (key = `param_key`); DLT: `administration.events.DLT` |

Nuestra configuración actual (`application.properties`, todo por entorno, se cambia sin tocar código):

```properties
spring.kafka.consumer.group-id=roadmap-service
spring.kafka.consumer.auto-offset-reset=earliest
app.kafka.topics.challenge-result=${KAFKA_TOPIC_CHALLENGE_RESULT:challenges.results}
app.kafka.topics.challenge-events=${KAFKA_TOPIC_CHALLENGE_EVENTS:challenges.events}
app.kafka.topics.dlq=${KAFKA_TOPIC_DLQ:}
```

`challenge-result` es el formato anterior (v1/v2) y `challenge-events` el evento de cierre vigente:
nunca deben apuntar al mismo topic (mismo `groupId`, Kafka repartiría los mensajes entre listeners).

### Preguntas

1. **¿En qué topic publica el Motor el resultado del desafío?** (B1) Respondido por
   escrito y **revertido** por G09 (`motor-desafios-evento-cierre.md`, 2026-09-27): `challenges.events`,
   `key = id_user`; `challenges.results` no existe en el broker de la plataforma. Historia: primero
   `challenge-events` (inventado nuestro), después `challenges.results` (respuesta v2 §2.1). A
   confirmar con el primer evento integrado.
2. **Resuelto por el contrato de plataforma:** un topic general por dominio, con el `event_type`
   discriminando eventos; los topics no se crean unilateralmente.
3. **`groupId`**: confirmamos `roadmap-service` como consumidor. ¿Hay convención distinta?
4. **`auto-offset-reset=earliest`**: nos apoyamos en la idempotencia por `event_id` para absorber
   replays. ¿Hay algún topic donde eso sea problema?

### 2.1 Casing del envelope y compatibilidad del productor

El sobre y los payloads viajan en **snake_case** (`event_id`, `event_type`, `event_version`), según `contratos-kafka` v8 en adelante.
Nuestro `EventEnvelope` escribe y lee **solo snake_case**, sin alias; un sobre camelCase va a la DLT
([[decisiones/DEC-001-wire-kafka-v8-snake-case|DEC-001]]). Hasta v3 el contrato de plataforma figuraba en camelCase y Roadmap
toleraba ambos; esa ventana se cerró (DT-18, 2026-10-27).

No queda pregunta abierta sobre el contrato común de envelope. Sí falta confirmar con el equipo de
Courses si sus futuros eventos de secciones/actividades usarán el estándar publicado, y definir sus
`event_type`, payload y clave.

La tabla estándar presenta claves por agregado; para Courses indica `courseId`. Confirmar con
Courses si esa clave representa `courseCohortId` para eventos cuya entidad afectada sea una cohorte.

### 2.2 Topics, claves y resiliencia declarados por la plataforma

- El estándar registra un topic por dominio, prohíbe crearlos por cuenta propia y documenta `courses.events` con DLT `courses.events.DLT`.
- El estándar general describe `courseId` como clave para Courses, pero no define si para cambios de una cohorte esa clave es el UUID de cohorte ni fija eventos de secciones.
- El consumidor Kafka de Notificaciones documenta 3 reintentos en memoria separados por 2000 ms y derivación al topic `<topic>.DLT`; esto es la política documentada para esa implementación. Cada consumidor debe confirmar que su configuración concreta cumple la política.

---

## 3. Lo que publicamos (vía outbox, T-01.12.5)

Cinco eventos, todos con `producer: "roadmap-service"`.

> **Estado T-01.12.5**: `NODE_COMPLETED` y `NODE_UNLOCKED` ya se encolan en la misma transacción de
> negocio dentro de la tabla `outbox_event`. La publicación diferida en Kafka la realiza `OutboxPoller`
> usando la variable de entorno `KAFKA_TOPIC_ROADMAP` (`app.kafka.topics.roadmap-events`).
> Si la variable está vacía (por defecto, D-T01125-01), los eventos permanecen acumulados como `PENDING`.
> Message key = `student_id` (propuesta B5). Al asignarse el topic en el bus, basta configurar dicha
> variable para que el poller publique lo acumulado sin pérdida de eventos.

### `NODE_COMPLETED`
```json
{
  "event_id": "uuid", "event_type": "NODE_COMPLETED", "event_version": 1,
  "timestamp": "2026-09-02T19:31:00Z", "producer": "tema-10-roadmap-service",
  "payload": { "course_id": "uuid", "student_id": "uuid", "node_id": "uuid",
               "challenge_id": "uuid", "section_id": "uuid" }
}
```

### `NODE_UNLOCKED`
```json
{
  "event_id": "uuid", "event_type": "NODE_UNLOCKED", "event_version": 1,
  "timestamp": "2026-09-02T19:31:00Z", "producer": "tema-10-roadmap-service",
  "payload": { "course_id": "uuid", "student_id": "uuid", "node_id": "uuid" }
}
```

### `COURSE_LEVEL_UP` (curva PAR-09) — forma propuesta, NO emitido por el código hoy
```json
{
  "event_id": "uuid", "event_type": "COURSE_LEVEL_UP", "event_version": 1,
  "timestamp": "2026-09-02T19:31:00Z", "producer": "tema-10-roadmap-service",
  "payload": { "course_id": "uuid", "student_id": "uuid", "new_level": 3, "total_xp": 1250 }
}
```

### `PERFORMANCE_ZONE_CHANGED` (entrada/salida de P90/P10) — forma propuesta, NO emitido por el código hoy
```json
{
  "event_id": "uuid", "event_type": "PERFORMANCE_ZONE_CHANGED", "event_version": 1,
  "timestamp": "2026-09-02T19:31:00Z", "producer": "tema-10-roadmap-service",
  "payload": { "course_id": "uuid", "student_id": "uuid",
               "previous_zone": "MIDDLE", "current_zone": "P90" }
}
```

### `BADGE_AWARDED` (HU-21, T-21.2)
Se encola en el outbox en la misma transacción que el otorgamiento (`BadgeEventService`) y queda
`PENDING` hasta que se configure `KAFKA_TOPIC_ROADMAP`. Message key = `student_id`. El momento del
otorgamiento es el `timestamp` del envelope.
```json
{
  "event_id": "uuid", "event_type": "BADGE_AWARDED", "event_version": 1,
  "timestamp": "2026-10-03T19:31:00Z", "producer": "tema-10-roadmap-service",
  "payload": { "course_id": "uuid", "student_id": "uuid", "badge_id": "uuid" }
}
```
> Pendiente con Notificaciones: confirmar el topic, la key, el envelope y la política de DLQ (P8).

> No emitimos `xp.otorgado`: nadie lo consume (`agent.md` §5.1).

### Preguntas

5. **(lista oficial del bus NO trae topic de Roadmap: 21 topics y ninguno nuestro) **¿A qué topic va cada uno de los cuatro del MVP?** ¿Uno solo `roadmap-events`, o uno por
   evento? Sin esto el outbox no puede setear `topic_destino`.
6. **¿Hay consumidores además de Notificaciones?** Nos sirve saber quién escucha para no romperles
   el payload más adelante.
7. **`PERFORMANCE_ZONE_CHANGED`**: ¿les sirve el vocabulario `P90` / `MIDDLE` / `P10`? Las zonas
   solo existen con **≥ 10 alumnos inscriptos** (RF-RNK-09); con menos no emitimos nada.
8. **`BADGE_AWARDED`**: ¿lo reservamos ahora o lo pedimos recién en Fase 2?

---

## 4. Message Key

Propuesta: **`studentId`**.

Razón: el orden de Kafka se garantiza **solo dentro de una partición**, y lo que nos importa es
que dos resultados del mismo alumno no se procesen desordenados. Descartamos `challengeId` porque
concentra a todos los alumnos de un desafío popular en una sola partición.

9. **¿Se confirma `studentId` como key?** (B5) Afecta a nuestro productor, no al consumidor.
10. **¿Todos los productores del bus usan la misma convención de key?** Si el Motor usa otra, el
    orden por alumno no está garantizado y tenemos que asumir desorden.

---

## 5. DLQ y reintentos

Hoy: `app.kafka.topics.dlq` **vacío por defecto**. Sin DLQ configurada, un error no reintentable
se registra en el log y el offset avanza — nunca frenamos la partición.

Nuestra clasificación actual (`KafkaConsumerConfig`):

| Situación | Qué hacemos |
|---|---|
| Envelope incompleto, JSON ilegible, UUID malformado | Poison pill: log `WARN`, offset avanza |
| `event_type` desconocido | Log `INFO`, offset avanza, sin interpretar |
| Alumno no matriculado, nodo/desafío ajenos al curso | `NonRetryableEventException` → log + DLQ si está configurada |
| `esRepeticion = true` | Descarte de negocio, log `DEBUG` |
| `event_id` ya registrado | No-op silencioso (idempotencia) |
| BD caída, timeout | Reintento con `ExponentialBackOff`, después DLQ |

### Preguntas

11. **¿Hay un topic de DLQ del bus, o cada micro arma el suyo?** (B3) Si hay uno común, ¿cuál es
    el nombre y qué formato espera el mensaje?
12. **Política de reintentos**: ¿hay un estándar del bus (cantidad, backoff), o lo define cada
    consumidor? Hoy usamos backoff exponencial con tope.
13. **¿Alguien monitorea la DLQ?** Si nadie la mira, mandar ahí es equivalente a perder el evento.

---

## 6. Qué cerramos con cada respuesta

Tabla para Notificaciones: qué queda habilitado de nuestro lado según qué contesten. Cada bloque
es independiente, no hace falta responder todo junto.

| Si responden | Cerramos | Si no responden |
|---|---|---|
| **P1** — topic donde publica el Motor | **T-03.2** (schema del evento consumido) y el consumidor queda apuntando a un topic real. Es **un solo dato** y es lo único que nos frena | El listener del evento vigente escucha `challenges.events` (el del formato anterior, `challenges.results`); DLQ del dominio: `challenges.results.DLT`. Nuestra prop DLQ sigue vacía (una sola DLQ compartida): mapear a la del dominio cuando se configure. |
| **P2-4** — topics por dominio, `groupId`, `earliest` | Confirmar la forma del consumidor (un `@KafkaListener` por topic o uno por tipo) | Asumimos lo que tenemos y lo corregimos después |
| **P5 + P9** — topics de salida y Message Key | **T-01.12.5 implementado**: `NODE_COMPLETED` y `NODE_UNLOCKED` ya se encolan y quedan en `PENDING`. Se publican al configurar `KAFKA_TOPIC_ROADMAP`. Key = `studentId`. `COURSE_LEVEL_UP` y `PERFORMANCE_ZONE_CHANGED` se integrarán en sus respectivas tareas | Los eventos quedan acumulados en `outbox_event` (PENDING) hasta configurar el topic |
| **P7** — vocabulario de zonas | `PERFORMANCE_ZONE_CHANGED` con el formato que ustedes consumen (entrada y salida de P90/P10) | Lo emitimos con nuestro vocabulario y ustedes lo traducen |
| **P8** — `BADGE_AWARDED` | Reservarlo ahora o pedirlo en Fase 2. Está fuera del MVP (`agent.md` §9) | Lo pedimos más adelante |
| **P11-13** — DLQ y reintentos | Endurecer el consumidor: los errores no reintentables van a una cola observable en lugar de morir en un log | Sigue funcionando sin frenar la partición, pero **un evento que falla se pierde** y nadie se entera |

### Lo que Notificaciones gana

Los cuatro eventos que publicamos son, casi todos, **para ustedes**:

- `NODE_COMPLETED` y `NODE_UNLOCKED` → avisarle al alumno que superó un nodo y qué caminos se le
  abrieron.
- `COURSE_LEVEL_UP` → notificación de subida de nivel (curva PAR-09).
- `PERFORMANCE_ZONE_CHANGED` → entrada o salida de las zonas P90/P10, que es la notificación con
  más valor del ranking: "estás cerca de promocionar" / "estás en riesgo de perder la regularidad".

Ninguno de los cuatro se puede emitir hasta que nos asignen topics (**P5**).

### Lo mínimo para no frenarnos

**P1.** Un solo dato: el nombre del topic donde el Motor publica el resultado del desafío. Con eso
cerramos T-03.2. **P5 y P9** vienen justo después, para arrancar el outbox.

### Lo que NO depende de ustedes

El consumidor ya está implementado y testeado (idempotencia por `event_id`, clasificación de
errores, poison pills, `event_type` desconocido). Los cuatro eventos de salida ya tienen su payload
definido. Solo falta **a dónde mandarlos y de dónde leer**.
