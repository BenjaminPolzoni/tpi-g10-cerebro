> [!warning] Documento histórico, actualizado en DT-18 (2026-10-27)
> La fuente canónica vigente es la skill `contratos-kafka` del Skill Hub (v12): sobre de 6 campos obligatorios en
> **snake_case** (`event_id`, `event_type`, `event_version`, `timestamp`, `producer`, `payload`), payload en snake_case,
> `event_type` en `SCREAMING_SNAKE_CASE` y un tópico `<dominio>.events` por dominio. Los nombres de campo y de evento de este
> texto se pasaron de camelCase/guiones a snake_case ([[decisiones/DEC-001-wire-kafka-v8-snake-case|DEC-001]]); lo demás (nombres de
> topic de ejemplo como `challenge-events`, claves, DLT, `organization_id`) puede estar desactualizado: ante cualquier
> diferencia manda la skill.

# Kafka Event Standard

## 1. Objetivo

Este documento define el **estándar común para la publicación y consumo de eventos mediante Apache Kafka** dentro de la plataforma.

Su objetivo es garantizar que todos los microservicios produzcan y consuman eventos de forma consistente, independientemente del dominio al que pertenezcan.

Este documento debe utilizarse como referencia para:

- Implementar nuevos productores Kafka.
- Implementar nuevos consumidores Kafka.
- Definir nuevos eventos.
- Definir topics.
- Definir Kafka Message Keys.
- Evolucionar contratos existentes.
- Validar eventos recibidos.
- Proporcionar contexto a asistentes y agentes de IA utilizados durante el desarrollo.

> **Regla fundamental:** todos los eventos publicados en Kafka por los microservicios de la plataforma DEBEN respetar las reglas definidas en este documento.

---

# 2. Principios generales

La arquitectura de eventos se basa en los siguientes principios:

1. Los eventos se serializan en **JSON**.
2. Los topics se organizan **por dominio**.
3. Todos los eventos utilizan un **envelope común**.
4. Cada tipo de evento define su propio `payload`.
5. Cada evento posee una versión explícita mediante `event_version`.
6. Cada dominio debe definir una estrategia de **Kafka Message Key**.
7. Los contratos publicados deben considerarse una **API pública entre microservicios**.
8. Los cambios incompatibles requieren una nueva versión del contrato.
9. Los consumidores deben contemplar duplicados, errores y eventos desconocidos.
10. Los productores no deben depender del conocimiento de sus consumidores.

El principio central del diseño es:

> **Envelope estable, payload flexible, contratos explícitos.**

---

# 3. Anatomía de un mensaje Kafka

Un mensaje Kafka debe entenderse conceptualmente como:

```text
Kafka Message
│
├── Topic
├── Key
│
└── Value
     │
     ├── event_id
     ├── event_type
     ├── event_version
     ├── timestamp
     ├── producer
     │
     └── payload
```

Cada elemento cumple una responsabilidad diferente:

| Elemento | Responsabilidad |
|---|---|
| Topic | Determina a qué dominio pertenece el evento |
| Key | Determina qué eventos deben mantenerse relacionados y ordenados |
| event_id | Identifica una instancia única del evento |
| event_type | Indica qué ocurrió |
| event_version | Identifica la versión del contrato |
| timestamp | Indica cuándo ocurrió |
| producer | Identifica quién publicó el evento |
| payload | Contiene los datos específicos del evento |

---

# 4. Estrategia de Topics

Los topics Kafka se organizan **por dominio**.

Un topic NO debe crearse para cada tipo individual de evento.

Por ejemplo, en lugar de:

```text
message-sent
message-edited
message-deleted
```

se utiliza un topic correspondiente al dominio:

```text
chat-events
```

Dentro del topic pueden existir diferentes `event_type`:

```text
chat-events
│
├── MESSAGE_SENT
├── MESSAGE_EDITED
├── MESSAGE_DELETED
├── USER_BLOCKED
└── CHANNEL_CLOSED
```

Otros ejemplos podrían ser:

```text
course-events
user-events
challenge-events
exchange-events
notification-events
```

Los nombres definitivos de los topics deben ser acordados y documentados por el equipo.

### Regla

> Un topic representa un dominio de negocio. El `event_type` identifica el hecho específico ocurrido dentro de ese dominio.

---

# 5. Formato común de eventos

Todos los eventos Kafka se serializan como JSON utilizando el siguiente envelope:

```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "NOMBRE_DEL_EVENTO",
  "event_version": 1,
  "timestamp": "2026-09-11T17:30:25.123Z",
  "producer": "tema-XX-nombre",
  "payload": {}
}
```

Los campos:

```text
event_id
event_type
event_version
timestamp
producer
payload
```

son parte del **contrato global de la plataforma**.

No deben modificarse, eliminarse o renombrarse unilateralmente por un microservicio.

---

# 6. `event_id`

`event_id` identifica de manera única una instancia concreta de un evento.

Ejemplo:

```json
"event_id": "550e8400-e29b-41d4-a716-446655440000"
```

## Reglas

- DEBE ser un UUID.
- DEBE generarse al crear el evento.
- Dos eventos diferentes NO DEBEN compartir el mismo `event_id`.
- NO representa una entidad de negocio.
- NO debe utilizarse como reemplazo de la Kafka Message Key.

Los consumidores pueden utilizarlo para detectar eventos procesados previamente e implementar mecanismos de idempotencia.

---

# 7. `event_type`

`event_type` identifica qué hecho ocurrió dentro del sistema.

Ejemplo:

```json
"event_type": "CHALLENGE_COMPLETED"
```

Los eventos representan **hechos que ya ocurrieron**, no órdenes para realizar acciones.

## Convención

Los nombres:

- DEBEN estar escritos en mayúsculas.
- DEBEN utilizar `_` como separador (`SCREAMING_SNAKE_CASE`, p. ej. `CHALLENGE_COMPLETED`).
- DEBEN representar hechos del dominio.
- DEBEN mantenerse estables una vez publicados.

### Correcto

```text
CHALLENGE_COMPLETED
MESSAGE_SENT
USER_BLOCKED
COURSE_CREATED
COURSE_PUBLISHED
PASSWORD_CHANGED
RETENTION_PERIOD_EXPIRED
```

### Evitar

```text
CREATE_COURSE
SEND_MESSAGE
BLOCK_USER
```

Preferir:

```text
COURSE_CREATED
MESSAGE_SENT
USER_BLOCKED
```

---

# 8. `event_version`

`event_version` identifica la versión del **contrato público de un determinado tipo de evento**.

Ejemplo:

```json
"event_version": 1
```

La versión:

- DEBE ser un número entero positivo.
- Comienza en `1`.
- NO representa la versión del microservicio.
- NO representa la versión de la aplicación.
- NO debe incrementarse por modificaciones internas del productor.
- DEBE incrementarse cuando se introduce un cambio incompatible en el contrato del evento.

Por ejemplo:

```text
chat-service v5.2
```

puede seguir produciendo:

```json
{
  "event_type": "MESSAGE_SENT",
  "event_version": 1
}
```

si el contrato público de `MESSAGE_SENT` no cambió.

---

# 9. `timestamp`

`timestamp` representa el momento en el que ocurrió el evento.

Ejemplo:

```json
"timestamp": "2026-09-11T17:30:25.123Z"
```

## Formato

Los timestamps DEBEN utilizar:

> **ISO 8601 en UTC.**

Formato recomendado:

```text
YYYY-MM-DDTHH:mm:ss.sssZ
```

No utilizar formatos locales o ambiguos:

```text
11/09/2026
09-11-2026
11/09/26 14:30
```

Todos los productores deben normalizar los timestamps a UTC antes de publicar el evento.

---

# 10. `producer`

`producer` identifica al microservicio responsable de publicar el evento.

Ejemplo:

```json
"producer": "tema-05-chat"
```

## Reglas

- DEBE identificar inequívocamente al microservicio productor.
- DEBE utilizar el identificador acordado por el proyecto.
- Representa quién publicó el evento.
- NO representa el consumidor.
- NO debe modificarse dependiendo de quién vaya a consumir el evento.

Un mismo evento puede ser consumido por múltiples microservicios.

---

# 11. `payload`

`payload` contiene la información específica necesaria para representar el evento.

Ejemplo:

```json
{
  "student_id": "123",
  "challenge_id": "456",
  "xp_earned": 50,
  "attempt_id": "789",
  "grade": "APROBADO"
}
```

La estructura del payload depende **100 % del `event_type` y de su `event_version`**.

Por ejemplo:

```text
CHALLENGE_COMPLETED v1
        │
        └── payload
             ├── student_id
             ├── challenge_id
             ├── xp_earned
             ├── attempt_id
             └── grade
```

Otro evento puede utilizar una estructura completamente diferente:

```json
{
  "event_type": "MESSAGE_SENT",
  "event_version": 1,
  "payload": {
    "message_id": "msg-123",
    "channel_id": "channel-456",
    "sender_id": "user-789"
  }
}
```

No existe una estructura global obligatoria dentro de `payload`.

Sin embargo:

> Una vez publicado el contrato de un `event_type` y `event_version`, productores y consumidores DEBEN respetarlo.

---

# 12. Kafka Message Key

La Kafka Message Key es un valor asociado al mensaje **fuera del JSON del evento**.

Conceptualmente:

```text
Topic:
chat-events

Key:
channel-456

Value:
{
  "event_id": "...",
  "event_type": "MESSAGE_SENT",
  "event_version": 1,
  ...
}
```

La key se utiliza principalmente para determinar la partición donde Kafka almacenará el mensaje.

Kafka garantiza el orden de los mensajes **dentro de una partición**, no un orden global entre todas las particiones.

Por esta razón, la elección de la key afecta directamente a:

- Orden de procesamiento.
- Distribución de eventos.
- Paralelismo.
- Escalabilidad.

---

# 13. Estrategia de Message Key

La key debe representar la **entidad lógica cuyo orden de eventos interesa preservar**.

Por ejemplo, para Chat:

```text
Topic: chat-events
Key: channel_id
```

Los eventos:

```text
MESSAGE_SENT
MESSAGE_SENT
MESSAGE_EDITED
MESSAGE_DELETED
```

del mismo canal utilizan:

```text
channel_id = channel-456
```

como key.

Conceptualmente:

```text
channel-456

MESSAGE_SENT
      │
MESSAGE_SENT
      │
MESSAGE_EDITED
      │
MESSAGE_DELETED
      │
      ▼
Partition N
```

Los eventos correspondientes a otro canal pueden terminar en otra partición:

```text
channel-789
      │
      ▼
Partition M
```

Esto permite obtener:

> **Orden dentro de una entidad + paralelismo entre entidades.**

---

# 14. Reglas para seleccionar una Message Key

Al definir la key de un dominio, debe responderse:

> **¿Qué eventos necesitan conservar su orden relativo?**

Si la respuesta es:

> Todos los eventos relacionados con un canal.

Entonces:

```text
key = channel_id
```

Si la respuesta es:

> Todos los eventos relacionados con un usuario.

Entonces:

```text
key = user_id
```

Si la respuesta es:

> Todos los eventos relacionados con un curso.

Entonces:

```text
key = course_id
```

La estrategia de key debe evitar concentrar innecesariamente grandes cantidades de eventos en una única entidad.

Por ejemplo:

```text
key = challenge_id
```

podría provocar que todos los estudiantes resolviendo el mismo desafío envíen eventos hacia la misma partición.

Dependiendo del dominio, podría ser más apropiado utilizar:

```text
student_id
```

o:

```text
attempt_id
```

La elección debe realizarse según las necesidades reales de orden y distribución.

---

# 15. Message Key vs `event_id`

Estos conceptos NO deben confundirse.

## `event_id`

Identifica:

> **¿Qué evento individual es este?**

Ejemplo:

```text
550e8400-e29b-41d4-a716-446655440000
```

## Kafka Message Key

Identifica normalmente:

> **¿A qué flujo lógico o entidad pertenece este evento?**

Ejemplo:

```text
channel-456
```

Dos mensajes pueden tener:

```text
Key: channel-456
```

y diferentes:

```text
event_id
```

Esto es completamente correcto.

---

# 16. Documentación obligatoria de Message Keys

Cada dominio DEBE documentar explícitamente su estrategia de key.

Ejemplo:

```md
## Dominio Chat

Topic: `chat-events`

Message Key: `channel_id`

Justificación:
Los eventos pertenecientes al mismo canal deben conservar su orden relativo.

Ejemplos de eventos:
- MESSAGE_SENT
- MESSAGE_EDITED
- MESSAGE_DELETED
- CHANNEL_CLOSED
```

La estrategia NO debe ser inferida por cada desarrollador o por una IA.

Debe existir una decisión explícita del equipo.

---

# 17. Tabla de dominios

Esta tabla debe mantenerse actualizada a medida que se definan los dominios.

| Dominio | Topic | Message Key | Justificación |
|---|---|---|---|
| Chat | `chat-events` | `channel_id` | Preservar orden dentro del canal |
| Cursos | `course-events` | Pendiente | Pendiente |
| Usuarios | `user-events` | Pendiente | Pendiente |
| Challenges | `challenge-events` | Pendiente | Pendiente |
| Intercambios | `exchange-events` | Pendiente | Pendiente |
| Notificaciones | `notification-events` | Pendiente | Pendiente |

> Los valores marcados como `Pendiente` NO deben ser inventados durante la implementación. Deben ser definidos explícitamente por el equipo responsable.

---

# 18. Versionado de contratos

Los contratos Kafka deben considerarse una **API pública entre microservicios**.

Modificar un contrato existente puede romper consumidores desarrollados por otros equipos.

Por esta razón, los eventos utilizan:

```json
"event_version": 1
```

La versión debe incrementarse únicamente cuando exista un **breaking change**.

---

# 19. Cambios compatibles

Un cambio compatible permite que consumidores existentes continúen procesando el evento.

Por ejemplo, versión original:

```json
{
  "student_id": "123",
  "challenge_id": "456",
  "xp_earned": 50
}
```

Agregar un campo opcional:

```json
{
  "student_id": "123",
  "challenge_id": "456",
  "xp_earned": 50,
  "course_id": "999"
}
```

puede mantenerse como:

```json
"event_version": 1
```

si los consumidores existentes pueden ignorar campos desconocidos.

---

# 20. Breaking Changes

Los siguientes cambios deben considerarse potencialmente incompatibles:

### Eliminar un campo

```text
student_id → eliminado
```

### Renombrar un campo

```text
xp_earned → experience
```

### Cambiar el tipo

Antes:

```json
"xp_earned": 50
```

Después:

```json
"xp_earned": "50 XP"
```

### Cambiar el significado semántico

Por ejemplo, reutilizar:

```text
grade
```

para representar un concepto diferente al definido originalmente.

### Convertir un campo opcional en obligatorio

Un consumidor o productor anterior puede no conocerlo.

### Modificar de manera incompatible la estructura

Antes:

```json
"user_id": "123"
```

Después:

```json
"user": {
  "id": "123"
}
```

Estos cambios requieren evaluar una nueva versión.

---

# 21. Regla de versionado

Como regla general:

| Cambio | ¿Nueva versión? |
|---|---:|
| Agregar campo opcional | No |
| Agregar metadata opcional al payload | No |
| Renombrar campo | Sí |
| Eliminar campo | Sí |
| Cambiar tipo de dato | Sí |
| Cambiar significado de un campo | Sí |
| Convertir campo opcional en obligatorio | Sí |
| Cambio estructural incompatible | Sí |

La regla fundamental es:

> **Si un consumidor existente puede dejar de funcionar correctamente debido al cambio, debe crearse una nueva versión.**

---

# 22. Ejemplo de evolución

## Versión 1

```json
{
  "event_id": "uuid",
  "event_type": "CHALLENGE_COMPLETED",
  "event_version": 1,
  "timestamp": "2026-09-11T17:30:25.123Z",
  "producer": "tema-03-challenges",
  "payload": {
    "student_id": "123",
    "challenge_id": "456",
    "xp_earned": 50
  }
}
```

Supongamos que posteriormente se decide reemplazar:

```text
xp_earned
```

por una estructura más compleja:

```json
"reward": {
  "xp": 50,
  "bonus": 10
}
```

Esto rompe el contrato anterior.

Debe publicarse como:

```json
{
  "event_id": "uuid",
  "event_type": "CHALLENGE_COMPLETED",
  "event_version": 2,
  "timestamp": "2026-09-11T17:30:25.123Z",
  "producer": "tema-03-challenges",
  "payload": {
    "student_id": "123",
    "challenge_id": "456",
    "reward": {
      "xp": 50,
      "bonus": 10
    }
  }
}
```

---

# 23. Convivencia de versiones

Una nueva versión no implica necesariamente que la versión anterior pueda eliminarse inmediatamente.

Durante una migración pueden coexistir:

```text
CHALLENGE_COMPLETED v1
CHALLENGE_COMPLETED v2
```

Los consumidores pueden necesitar soportar temporalmente ambas versiones:

```text
Evento recibido
      │
      ▼
event_type
      │
      ▼
event_version
      │
      ├── 1 → Handler V1
      │
      └── 2 → Handler V2
```

Una versión anterior debe eliminarse únicamente cuando los consumidores afectados hayan migrado o exista una decisión explícita de retirar dicho contrato.

---

# 24. Responsabilidades del productor

Todo productor Kafka debe:

1. Seleccionar el topic correspondiente a su dominio.
2. Utilizar la estrategia de Message Key definida para ese dominio/evento.
3. Generar un `event_id` único.
4. Utilizar un `event_type` documentado.
5. Indicar el `event_version` correspondiente.
6. Generar un timestamp ISO 8601 UTC.
7. Identificarse mediante `producer`.
8. Construir el payload según el contrato documentado.
9. Serializar el evento como JSON.
10. Publicar el mensaje en Kafka.

El productor NO debe:

- Asumir quién consumirá el evento.
- Adaptar el evento específicamente para un consumidor concreto.
- Cambiar unilateralmente un contrato existente.
- Inventar nuevas versiones sin necesidad.
- Modificar la estrategia de key sin documentarlo.

---

# 25. Responsabilidades del consumidor

Todo consumidor debe:

1. Recibir el mensaje del topic correspondiente.
2. Validar el envelope.
3. Identificar `event_type`.
4. Identificar `event_version`.
5. Interpretar el payload según ese contrato.
6. Ignorar campos adicionales que no necesite cuando sea posible.
7. Manejar eventos desconocidos.
8. Manejar versiones desconocidas.
9. Contemplar procesamiento duplicado.
10. Aplicar las políticas de error/reintento definidas por el proyecto.

Conceptualmente:

```text
Mensaje recibido
       │
       ▼
Validar envelope
       │
       ▼
Identificar event_type
       │
       ▼
Identificar event_version
       │
       ▼
Validar payload
       │
       ▼
Procesar evento
```

---

# 26. Idempotencia

Kafka puede entregar un mensaje más de una vez dependiendo de la configuración y las condiciones de procesamiento.

Por esta razón:

> Los consumidores que ejecuten operaciones sensibles deben contemplar idempotencia.

El `event_id` puede utilizarse para detectar eventos previamente procesados.

Ejemplo:

```text
Recibir evento
      │
      ▼
Consultar event_id
      │
      ├── Ya procesado
      │       │
      │       └──► No repetir operación
      │
      └── Nuevo
              │
              ▼
         Procesar evento
              │
              ▼
         Registrar event_id
```

La existencia de `event_id` NO implementa idempotencia automáticamente.

Cada consumidor debe implementar la estrategia correspondiente cuando sea necesaria.

---

# 27. Eventos desconocidos

Un consumidor puede recibir un `event_type` que no reconoce.

Esto puede ocurrir porque un productor comenzó a publicar un nuevo evento dentro del mismo dominio.

Los consumidores NO deben asumir que conocen todos los eventos existentes en un topic.

Un `event_type` desconocido debe ser manejado de forma segura según la política definida por el proyecto.

En particular:

> La incorporación de un nuevo `event_type` dentro de un topic no debería romper consumidores existentes.

---

# 28. Versiones desconocidas

Un consumidor también puede recibir:

```json
{
  "event_type": "MESSAGE_SENT",
  "event_version": 3
}
```

cuando solamente conoce:

```text
MESSAGE_SENT v1
MESSAGE_SENT v2
```

El consumidor NO debe interpretar automáticamente el payload como una versión conocida.

Debe aplicar la política de error definida por el proyecto.

---

# 29. Registro de eventos

Todo nuevo evento debe documentarse antes de considerarse parte estable del contrato entre microservicios.

Formato recomendado:

```md
## CHALLENGE_COMPLETED

### Descripción

Se publica cuando un estudiante completa un desafío.

### Dominio

Challenges

### Topic

`challenge-events`

### Event Type

`CHALLENGE_COMPLETED`

### Event Version

`1`

### Producer

`tema-03-challenges`

### Message Key

`student_id`

### Consumidores conocidos

- `tema-XX-nombre`
- `tema-YY-nombre`

### Payload

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| student_id | string | Sí | Identificador del estudiante |
| challenge_id | string | Sí | Identificador del desafío |
| xp_earned | number | Sí | XP obtenido |
| attempt_id | string | Sí | Identificador del intento |
| grade | string | Sí | Resultado del desafío |

### Ejemplo

{
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "CHALLENGE_COMPLETED",
  "event_version": 1,
  "timestamp": "2026-09-11T17:30:25.123Z",
  "producer": "tema-03-challenges",
  "payload": {
    "student_id": "123",
    "challenge_id": "456",
    "xp_earned": 50,
    "attempt_id": "789",
    "grade": "APROBADO"
  }
}
```

---

# 30. Template para registrar nuevos eventos

Copiar y completar esta plantilla:

```md
## NOMBRE_DEL_EVENTO

### Descripción

[Explicar qué hecho del dominio representa y cuándo se publica.]

### Dominio

[NOMBRE_DOMINIO]

### Topic

`[nombre-topic]`

### Event Type

`NOMBRE_DEL_EVENTO`

### Event Version

`1`

### Producer

`tema-XX-nombre`

### Message Key

`[campo utilizado como key]`

### Justificación de la Message Key

[Explicar qué orden se busca preservar.]

### Consumidores conocidos

- Pendiente

### Payload

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| campo | string | Sí | Descripción |

### Ejemplo

{
  "event_id": "UUID",
  "event_type": "NOMBRE_DEL_EVENTO",
  "event_version": 1,
  "timestamp": "2026-09-11T17:30:25.123Z",
  "producer": "tema-XX-nombre",
  "payload": {}
}
```

---

# 31. Checklist para crear un nuevo evento

Antes de publicar un nuevo evento debe verificarse:

- [ ] El evento representa un hecho y no un comando.
- [ ] El `event_type` sigue la convención definida.
- [ ] El dominio está identificado.
- [ ] El topic está definido.
- [ ] El producer está identificado.
- [ ] La Message Key está definida.
- [ ] La elección de la Message Key está justificada.
- [ ] El payload está documentado.
- [ ] Cada campo tiene un tipo definido.
- [ ] Cada campo indica si es obligatorio u opcional.
- [ ] El evento comienza con `event_version: 1`.
- [ ] Existe un ejemplo JSON válido.
- [ ] Los consumidores conocidos están documentados.
- [ ] Se verificó que no exista ya otro evento equivalente.

---

# 32. Reglas para asistentes y agentes de IA

Este documento puede utilizarse como contexto para agentes de IA encargados de implementar productores, consumidores o integraciones Kafka.

Las siguientes reglas son obligatorias.

## La IA DEBE

- Utilizar JSON para el Value del mensaje.
- Mantener exactamente la estructura común del envelope.
- Generar `event_id` como UUID.
- Utilizar `event_version`.
- Utilizar timestamps ISO 8601 UTC.
- Utilizar el `event_type` documentado.
- Identificar correctamente al `producer`.
- Consultar el contrato específico antes de construir un payload.
- Consultar la estrategia de Message Key del dominio.
- Publicar en el topic correspondiente al dominio.
- Mantener compatibilidad con contratos existentes.
- Advertir cuando un cambio solicitado constituya un breaking change.
- Diferenciar entre versión del evento y versión del microservicio.
- Manejar versiones desconocidas de forma explícita.
- Preservar la separación entre envelope y payload.

## La IA NO DEBE

- Inventar campos en el envelope.
- Renombrar campos del envelope.
- Inventar topics.
- Inventar Message Keys.
- Inventar contratos marcados como `Pendiente`.
- Inventar campos del payload cuando existe un contrato documentado.
- Cambiar tipos de datos arbitrariamente.
- Eliminar campos obligatorios.
- Cambiar un `event_type` existente unilateralmente.
- Incrementar `event_version` por cambios compatibles.
- Realizar breaking changes sin advertirlo.
- Asumir que todos los consumidores conocen una nueva versión.
- Utilizar `event_id` como Message Key salvo que exista una decisión explícita que lo justifique.
- Asumir que Kafka garantiza orden global entre particiones.

Cuando exista información marcada como:

```text
Pendiente
TBD
Por definir
```

la IA debe solicitar o señalar la necesidad de una decisión del equipo en lugar de inventarla.

---

# 33. Ejemplo completo de publicación

Supongamos:

```text
Dominio: Chat
Topic: chat-events
Message Key: channel-456
```

El mensaje Kafka sería conceptualmente:

```text
Topic:
chat-events

Key:
channel-456

Value:
```

```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "MESSAGE_SENT",
  "event_version": 1,
  "timestamp": "2026-09-11T17:30:25.123Z",
  "producer": "tema-05-chat",
  "payload": {
    "message_id": "message-999",
    "channel_id": "channel-456",
    "sender_id": "user-123"
  }
}
```

Un segundo evento relacionado con el mismo canal podría ser:

```text
Topic:
chat-events

Key:
channel-456
```

```json
{
  "event_id": "6d70d204-d33d-47ea-9751-f12ab7f718a2",
  "event_type": "MESSAGE_EDITED",
  "event_version": 1,
  "timestamp": "2026-09-11T17:32:10.456Z",
  "producer": "tema-05-chat",
  "payload": {
    "message_id": "message-999",
    "channel_id": "channel-456"
  }
}
```

Al utilizar la misma key:

```text
channel-456
```

Kafka puede mantener estos eventos en la misma partición y preservar su orden relativo.

---

# 34. Resumen del estándar

Cada mensaje Kafka debe poder responder claramente las siguientes preguntas:

```text
Topic
│
└── ¿A qué dominio pertenece?

Message Key
│
└── ¿Qué eventos deben permanecer relacionados y ordenados?

event_type
│
└── ¿Qué ocurrió?

event_version
│
└── ¿Qué versión del contrato representa?

event_id
│
└── ¿Qué instancia concreta del evento es?

timestamp
│
└── ¿Cuándo ocurrió?

producer
│
└── ¿Qué microservicio lo publicó?

payload
│
└── ¿Qué información específica describe el evento?
```

El contrato mínimo obligatorio es:

```json
{
  "event_id": "UUID",
  "event_type": "NOMBRE_DEL_EVENTO",
  "event_version": 1,
  "timestamp": "ISO-8601-UTC",
  "producer": "tema-XX-nombre",
  "payload": {}
}
```

Y cada publicación debe además tener definidos:

```text
Topic
Message Key
```

---

# 35. Decisiones arquitectónicas actuales

Las siguientes decisiones se consideran parte del estándar actual del proyecto:

| Decisión | Estándar |
|---|---|
| Serialización | JSON |
| Organización de topics | Por dominio |
| Envelope | Común para todos los microservicios |
| Payload | Específico por `event_type` y versión |
| Identificador de evento | UUID |
| Timestamp | ISO 8601 UTC |
| Versionado | `event_version` dentro del envelope |
| Primera versión | `1` |
| Nueva versión | Solo ante breaking changes |
| Message Key | Definida explícitamente por dominio según necesidades de orden |
| Orden | Garantizado únicamente dentro de una partición |
| Idempotencia | Responsabilidad del consumidor cuando corresponda |
| Contratos pendientes | No deben ser inventados por desarrolladores ni IAs |

---

# 36. Temas pendientes de definición

Este estándar no define todavía las políticas operativas relacionadas con:

- Retries.
- Dead Letter Topics / Dead Letter Queues.
- Cantidad de particiones por topic.
- Replication factor.
- Retención de mensajes.
- Consumer Groups.
- Política frente a errores de deserialización.
- Política frente a versiones desconocidas.
- Observabilidad y métricas Kafka.
- Trazabilidad distribuida.
- Schema Registry, en caso de incorporarse en el futuro.

Estas decisiones deben documentarse separadamente cuando sean acordadas.

Hasta entonces, ninguna implementación o IA debe asumir una política global no documentada.

---

# 37. Regla final

> **Todo evento Kafka es un contrato entre microservicios.**

El productor es propietario del evento, pero una vez publicado el contrato debe asumir que otros servicios pueden depender de él.

Por lo tanto:

> **Los contratos deben ser explícitos, documentados, versionados y compatibles siempre que sea posible.**

La combinación de:

```text
Topic por dominio
+
Message Key explícita
+
Envelope común
+
event_type
+
event_version
+
Payload documentado
```

constituye el estándar de integración Kafka de la plataforma.