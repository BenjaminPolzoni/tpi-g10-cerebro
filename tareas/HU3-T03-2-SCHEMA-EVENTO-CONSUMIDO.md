# HU3-T03.2 — Schema del evento consumido

Tarea de **HU-03**: clases del envelope y del payload del resultado del Motor, con validación de
obligatorios y de tipos; los campos desconocidos se registran y no se interpretan. Contexto en
`agent.md` §5.1 y §5.4, `docs/T-03-1-LISTENER-RESULTADO-MOTOR.md` y
`docs/contracts/motor-desafios.md`.

> **Etiqueta**: `HU3-T03.2`, no `T-03.2`. En el repo, `T-03.2` ya se usa (README, `ESTRUCTURA.md`,
> `T-03-5-DOBLES-CLIENTES.md`, Javadoc de `clients/inventory`) para el cliente HTTP de Inventario,
> que según `T-15-1-GATE-V3.md` corresponde a T-15.2. Esas referencias no se tocan.

---

## Decisiones

### D-HU3-01 — Vidas fuera de alcance
En Roadmap, las vidas se consultan siempre a Wallet y se usan solo para mostrarlas, para el gate
(y los ejercicios de recuperación) y para el desempate del ranking. Esta tarea no agrega lógica de
vidas: los campos de vidas del payload se transportan pero no se interpretan.

Queda pendiente para la tarea de ranking: la fuente del desempate por vidas y el espejo
`StudentCourse.lives/lostLives`, que hoy leen `applyResult` y `startChallenge` a pesar de
`agent.md` §3.1b.

### D-HU3-02 — Un listener por topic, payload tipado por `eventType`
`agent.md` §5.4 dice "`@KafkaListener` por tipo". Se interpreta como **payload tipado por
`eventType`**, con **un listener por topic** mientras siga abierta la P2 de
`docs/contracts/bus-notificaciones.md` (un topic por dominio o uno por tipo).

Motivo: en Kafka un listener se suscribe a un topic, no a un `eventType`. Dos `@KafkaListener` con
el mismo `groupId` sobre el mismo topic se reparten las particiones y cada uno pierde los mensajes
del otro. `RoadmapEventListener` rutea por `eventType` y convierte cada payload a su clase tipada.
No se modifica `agent.md`.

### D-HU3-03 — Envelope dual: snake_case y camelCase
El envelope del bus acepta indistintamente snake_case (`event_id`, `event_type`) y camelCase
(`eventId`, `eventType`) mediante anotaciones `@JsonAlias`. Campos obligatorios: `eventId` (UUID),
`eventType`, `timestamp`, `producer`, `payload`. Si alguno falta o es inválido, el mensaje se descarta
como poison pill sin reintentar.

### D-HU3-04 — Validación estricta de timestamps ISO-8601 con offset
Los campos de fecha/hora (`timestamp` del envelope y `completed_at` / `completedAt` de los payloads)
exigen un string JSON con formato ISO-8601 y offset explícito (`Z` o `±hh:mm`), normalizado a `Instant`
en UTC mediante `StrictTimestampDeserializer`. Se rechazan timestamps numéricos (epoch), cadenas sin offset
o texto malformado con `InvalidTimestampException`, descartando el evento y registrando un log con el
campo y valor inválidos.

### D-HU3-05 — Tolerancia en `completed_at` / `completedAt`
Se soporta indistintamente `completed_at` y `completedAt` en ambos eventos (`ATTEMPT_CORRECTED` y
`ATTEMPT_CANCELED`) mediante `@JsonProperty("completed_at")` y `@JsonAlias("completedAt")`.

### D-HU3-06 — Identificadores UUID estrictos
Los identificadores `id_user`, `id_course` y `challenge_id` deben ser UUID válidos (la base de datos usa UUID).
Cualquier valor que no sea un UUID válido se clasifica como poison pill y se descarta con log sin propagar
error al broker.

### D-HU3-07 — Convención de `xp` en ATTEMPT_CANCELED
En `ATTEMPT_CANCELED`, el valor de `resources.xp` se asume positivo representando la cantidad a descontar.
En esta tarea únicamente se valida su estructura y se emite un log informativo; la lógica de anulación y
compensación de XP queda postergada para una historia de usuario posterior.

### D-HU3-08 — DTO interno ChallengeResult
El DTO interno `ProgressDtos.ChallengeResult` se desacopla del payload del Motor: conserva `passed`
(`result.status == APPROVED`), `xp` y `subtractLive` (transportado sin interpretar). Se eliminan
`nodeId` (resuelto internamente en `ProgressService` por `challengeId` dentro del roadmap) y
`esRepeticion` (inexistente en el contrato del Motor).

### D-HU3-09 — Manejo de campos no reconocidos
Cualquier campo desconocido presente en el envelope o en los payloads se captura dinámicamente mediante
`@JsonAnySetter` y se emite una advertencia en log (WARN con clave `event.unknown-field`, indicando el `eventId`
y el nombre del campo). Los campos declarados por el contrato pero no utilizados por Roadmap (`coins`,
`active_item`, `difficulty`, `score`, `late`, `attempt_number`, `resolution_time`, `challenge_version`,
`challenge_type`, `mandatory`) se modelan explícitamente en los records y no son considerados desconocidos.

### D-HU3-10 — Tipado estricto local al consumidor de eventos
La configuración estricta de Jackson se aísla exclusivamente en el `ObjectMapper` del consumidor de eventos
(`RoadmapEventListener`): `FAIL_ON_NULL_FOR_PRIMITIVES`, coerción escalar deshabilitada (`"true"` como boolean
o `"250"` como int fallan) y `ACCEPT_FLOAT_AS_INT` deshabilitado. No se altera el `ObjectMapper` global de Spring,
preservando el comportamiento estándar de la API REST.

---

## Contratos Recibidos (Grupo 9, Motor de Desafíos)

### ATTEMPT_CORRECTED
```json
{
  "event_id": "UUID",
  "event_type": "ATTEMPT_CORRECTED",
  "timestamp": "TIMESTAMP",
  "producer": "THEME-02-CHALLENGE-ENGINE",
  "payload": {
    "resources": {
      "coins": 12.5,
      "xp": 250,
      "substract_live": false,
      "active_item": ["id_item", "id_item"]
    },
    "id_user": "id_user",
    "id_course": "id_course",
    "challenge_id": "challenge_id",
    "challenge_version": 1,
    "challenge_type": "NORMAL",
    "difficulty": "MEDIUM",
    "mandatory": true,
    "result": {
      "status": "APPROVED",
      "score": 87,
      "completed_at": "TIMESTAMP",
      "late": false,
      "attempt_number": 2,
      "resolution_time": 412.5
    }
  }
}
```

### ATTEMPT_CANCELED
```json
{
  "event_id": "UUID",
  "event_type": "ATTEMPT_CANCELED",
  "timestamp": "TIMESTAMP",
  "producer": "THEME-02-CHALLENGE-ENGINE",
  "payload": {
    "resources": {
      "coins": 12.5,
      "xp": 250,
      "add_live": true,
      "active_item": ["id_item", "id_item"]
    },
    "id_user": "id_user",
    "id_course": "id_course",
    "challenge_id": "challenge_id",
    "challenge_version": 1,
    "challenge_type": "NORMAL",
    "difficulty": "MEDIUM",
    "mandatory": true,
    "result": {
      "status": "APPROVED",
      "score": 87,
      "completedAt": "TIMESTAMP",
      "late": false,
      "attempt_number": 2,
      "resolution_time": 412.5
    }
  }
}
```

---

## Archivos Modificados y Creados

| Archivo | Acción | Descripción |
|---|---|---|
| `events/AttemptStatus.java` | Creado | Enum `APPROVED`, `DISAPPROVE` (valores literales del contrato). |
| `events/ChallengeType.java` | Creado | Enum `NORMAL`, `LIVES`, `LLM`. |
| `events/Difficulty.java` | Creado | Enum `EASY`, `MEDIUM`, `HARD`. |
| `events/StrictTimestampDeserializer.java` | Creado | Deserializador estricto para ISO-8601 con offset obligatorio y conversión a UTC `Instant`. |
| `events/InvalidTimestampException.java` | Creado | Excepción ante timestamps numéricos, sin offset o inválidos. |
| `events/EventEnvelope.java` | Modificado | `@JsonAlias` snake/camelCase, deserializador estricto, `@JsonAnySetter` para campos desconocidos. |
| `events/AttemptCorrectedPayload.java` | Creado | Records anidados `Resources` y `Result`, validación `isComplete()`, captura de campos desconocidos. |
| `events/AttemptCanceledPayload.java` | Creado | Schema de anulación con `add_live` y validación `isComplete()`. |
| `events/ChallengeCompletedPayload.java` | Eliminado | Reemplazado por los nuevos payloads del contrato real. |
| `events/RoadmapEventListener.java` | Modificado | Ruteo de eventos, `ObjectMapper` local estricto, logging WARN de campos no reconocidos. |
| `dtos/ProgressDtos.java` | Modificado | `ChallengeResult` adaptado sin `nodeId` ni `esRepeticion`; incluye `subtractLive`. |
| `models/StudentCourse.java` | Modificado | Método `addXp(long)` preservando las vidas (D-HU3-01). |
| `services/ProgressService.java` | Modificado | Resolución de nodo por `challengeId` en el roadmap, eliminación de chequeo de repetición. |
| `messages.properties` | Modificado | Mensajes i18n para campos desconocidos, timestamp inválido y desafío ambiguo. |
| `test/.../ChallengeResultListenerTest.java` | Modificado | 28 tests cubriendo el contrato completo de `ATTEMPT_CORRECTED` y `ATTEMPT_CANCELED`. |
| `test/.../events/StrictTimestampDeserializerTest.java` | Creado | Pruebas unitarias de deserialización estricta de timestamps. |
| Otros tests (`GraphEditorScenariosTest`, `NodeUnlockOnResultTest`, etc.) | Modificado | Adaptación al nuevo `ChallengeResult`. |
| `docs/ESTRUCTURA.md`, `README.md`, `contracts/motor-desafios.md` | Modificado | Actualización documental de arquitectura y contratos. |

---

## Preguntas Abiertas para Grupo 9 (Motor)

1. **Signo de `xp` en `ATTEMPT_CANCELED`**: Asumido positivo indicando cantidad a restar. ¿Confirmado?
2. **Formato UUID**: ¿Se garantiza que `id_user`, `id_course` y `challenge_id` son siempre UUID estándar válidos?
3. **Offset en Timestamps**: ¿Se confirma que todos los timestamps emitidos incluyen offset explícito (`Z` o `±hh:mm`)?
4. **Estandarización de Casing**: ¿Se unificará `completed_at` vs `completedAt` y `substract_live` vs `add_live` entre eventos?

