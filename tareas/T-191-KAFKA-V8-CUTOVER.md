# T-191 — Cutover del wire Kafka a contratos-kafka v8 (snake_case)

Nota operativa del PR #191 (`fix/kafka-v8-snake-case`). Migra el wire de Roadmap a
**contratos-kafka v8**: un solo nombre por campo, **snake_case** en el sobre y en el
payload, sin alias ni convivencia con camelCase. Un mensaje camelCase va a la DLT.

## 1. Productores y consumidores (verificado en `develop`)

| Servicio | Evidencia | Estado |
|---|---|---|
| Courses (`tpi-course`) | `src/main/java/.../events/KafkaEventWire.java` configura `PropertyNamingStrategies.SNAKE_CASE` para sobre y payload; `EventEnvelope` documenta `event_id`/`event_type`/`event_version` | **v8 snake** ✓ |
| Backoffice (`tpi-backoffice`) | `GlobalConfigurationChangedPayloadDto` usa `@JsonProperty("param_key")`, `previous_version`, `actor_id` | **v8 snake** ✓ |
| Motor (`tpi-engine-challenge`) | El evento de cierre v3 se lee en Roadmap con `id_user`/`id_course`/`id_node`/`challenge_id`/`content_type`/`resources` (v8) | **v8 snake** ✓ |
| Consumidores de lo que Roadmap publica (`roadmap.events`: `NODE_COMPLETED`, `NODE_UNLOCKED`, `BADGE_AWARDED`) | Gamificación, Accounting y Notificaciones | **Pendiente confirmar** que ya consumen v8 antes del corte |

Roadmap pasa a escribir y leer en snake_case; un camelCase (sobre del Motor v2 o fila del
outbox previa) se descarta a la DLT, sin reintentos.

## 2. Cutover del outbox (filas pendientes)

`OutboxService` guarda el **sobre ya serializado** en `outbox_event.payload`
(`objectMapper.writeValueAsString(envelope)`). Las filas `PENDING` creadas antes del corte
quedan en camelCase y un consumidor v8 las descarta. Pasos antes de desplegar la build v8:

1. **Frenar la publicación**: dejar `app.kafka.topics.roadmap-events` sin tópico o detener el
   poller, para no generar filas nuevas.
2. **Drenar el outbox**: esperar a que `outbox_event` no tenga filas `PENDING`.
   ```sql
   SELECT status, count(*) FROM outbox_event GROUP BY status;
   ```
3. **Alternativa a (2)** — migrar las filas pendientes: re-serializar `payload` a snake_case
   (o descartar las que ya estén representadas en el ledger). No se hace un UPDATE a ciegas:
   el `payload` es el sobre completo y hay que reescribir sus claves.
4. **Lag a cero** en los tópicos que Roadmap consume (`challenges.events`, `courses.events`,
   `administration.events`) antes del corte: un mensaje viejo en vuelo llegaría camelCase.
5. **Desplegar** la build v8.

## 3. Verificación post-corte

- `roadmap.events.DLT` sin mensajes nuevos (ni en la DLT de los tópicos de entrada).
- Lag de los grupos de Roadmap vuelve a cero tras el arranque.
- Un cierre de intento de punta a punta actualiza `xp_movement` y `completed_node`
  (evidencia E2E; repetir con envelope v8, no con la evidencia camelCase de #190).
- `outbox_event` sigue publicando y no acumula `FAILED`.

## 4. Rollback

Revertir la build a la versión camelCase solo si Producers/consumers volvieron a camelCase.
No hay ventana de convivencia: el rollback necesita el mismo drenado del outbox a la inversa.

## 5. Pendientes declarados

- Confirmar con **Gamificación, Accounting y Notificaciones** que consumen `roadmap.events` en v8.
- Borrar el listener v1/v2 (`RoadmapEventListener.onMessage`), sus payloads y su flag
  (`app.kafka.topics.challenge-result.enabled`): quedó apagado por #190 y es código muerto.
  No entra en #191 para no arrastrar la migración de sus suites de test; seguimiento aparte.
