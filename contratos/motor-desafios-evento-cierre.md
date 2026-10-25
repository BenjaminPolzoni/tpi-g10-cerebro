# Evento de cierre de intento: Motor de Desafíos (G09) — vigente

Estado: **vigente y publicado por G09**. El Motor publica este evento con
`producer = tema-03-challenges-service` en el wire **contratos-kafka v8**: sobre y payload en
**snake_case**, un solo nombre por campo. Roadmap lo lee así desde #191. Fuente de verdad del lado del Motor:
[`docs/contracts/eventos-bus.md`](https://github.com/2026-P4-BE/tpi-engine-challenge/blob/develop/docs/contracts/eventos-bus.md).

> **Migración a v8 (2026-10, #191).** El payload viajaba en camelCase (`contratos-kafka` v5, con
> mezcla de snake_case). Roadmap lee **solo** snake_case, sin alias: un sobre o payload en camelCase
> va a la DLT. El cutover del outbox y la verificación con los otros equipos están en
> [`T-191-KAFKA-V8-CUTOVER.md`](../T-191-KAFKA-V8-CUTOVER.md).

> **Cambio de nombres (2026-10-05, tpi-roadmap#120).** Hasta esa fecha el `producer` era
> `THEME-02-CHALLENGE-ENGINE`. Ese `producer` se ignora; el formato vigente usa
> `tema-03-challenges-service` y el wire en snake_case de v8.

> **Este documento reemplaza, para el evento de cierre de intento, a `motor-desafios.md` §1 y a
> `respuesta-motor-a-roadmap-v2.md` §2.** El resto de `respuesta-motor-a-roadmap-v2.md` (catálogo
> §1, gate §4, corrección diferida §5) sigue vigente y no lo toca este documento.
>
> **Cambio de fondo respecto de v2**: v2 decía que el Motor "es un evaluador académico, no un
> calculador de progresión ni un ledger" y que no manda XP, monedas ni vidas. Esta versión lo
> revierte: **el Motor sí calcula y manda `coins`, `xp`, `add_live`, `subtract_live` y
> `active_item`**, con los parámetros de Backoffice congelados al abrir el intento. Roadmap
> aplica esos valores tal cual llegan; no recalcula nada.

Mensaje original recibido de G09, para Accounting (Banco) y Roadmap.

## Cómo funciona

- **Un solo evento por intento cerrado, con toda la información.** Cada micro toma lo que
  necesita e ignora el resto.
- Dos `event_type`, misma estructura:
  - `CHALLENGE_COMPLETED`: el intento se corrigió y tiene veredicto.
  - `CHALLENGE_ABORTED`: el intento se cerró sin veredicto (anulado por un profesor, o el
    corrector no respondió a tiempo). Reemplaza a `ATTEMPT_CANCELED`.

## Canal

| | |
|---|---|
| Topic | `challenges.events` |
| Key del mensaje | `id_user` (orden garantizado por alumno) |
| Formato | JSON plano (`StringSerializer`), sin headers de clase |
| Entrega | at-least-once: **deduplicar por `event_id`** |
| Filtro | por `producer` y `event_type`, porque Tema 05 (Practical) también publica en este topic |

> **Cambia el topic y la key respecto de lo ya implementado**: hoy `application.properties`
> (`app.kafka.topics.challenge-result`) apunta a `challenges.results` (default de v2) y el
> listener asumía `id_attempt` como key conceptual. Con este contrato el topic vuelve a
> `challenges.events` (ya era el default anterior a v2, ver `docs/contracts/bus-notificaciones.md`
> §2) y la key pasa a ser `id_user`.

> **Filtro en Roadmap**: `onChallengeClosureEvent` procesa solo `producer = tema-03-challenges-service`
> (constante `CHALLENGE_ENGINE_PRODUCER`); el resto se ignora en `DEBUG`. Si el Motor cambiara ese
> string, sus eventos se descartarían en silencio: coordinar el cambio antes (pasó con el cambio
> del 2026-10-05, tpi-roadmap#120).

## `CHALLENGE_COMPLETED`

Ejemplo: aprobado, desafío obligatorio.

```json
{
  "event_id": "7a3e813f-b88c-4cf2-9e8a-0d8591ef528c",
  "event_type": "CHALLENGE_COMPLETED",
  "event_version": 1,
  "timestamp": "2026-09-27T15:30:00Z",
  "producer": "tema-03-challenges-service",
  "payload": {
    "resources": {
      "coins": 100.00,
      "xp": 250,
      "add_live": false,
      "subtract_live": false,
      "active_item": ["b1c2d3e4-0000-4000-8000-000000000001"]
    },
    "id_user": "09819779-7a70-424a-bb10-91a5e117498c",
    "id_course": "34f19b88-1065-4f46-813c-74cf47113115",
    "id_node": "5d2a7c10-3e4f-4a5b-9c6d-7e8f90a1b2c3",
    "id_attempt": "e1582fc8-12c8-4770-bc56-02f4a13d7821",
    "challenge_id": "6f70dc0d-e25f-4053-9387-e07085ea38a3",
    "challenge_version": 2,
    "challenge_type": "NORMAL",
    "content_type": "PRACTICAL",
    "difficulty": "MEDIUM",
    "mandatory": true,
    "performed_by_user_id": "09819779-7a70-424a-bb10-91a5e117498c",
    "performed_by_role": "STUDENT",
    "result": {
      "status": "APPROVED",
      "score": 86,
      "completed_at": "2026-09-27T15:29:58Z",
      "late": false,
      "attempt_number": 1,
      "resolution_time": 1420.0,
      "started_at": "2026-09-27T14:55:10Z",
      "submitted_at": "2026-09-27T15:18:50Z",
      "approval_threshold": 60,
      "max_attempts": 3,
      "last_attempt": false,
      "closure_reason": null,
      "closure_detail": null
    }
  }
}
```

## `CHALLENGE_ABORTED`

Ejemplo: un profesor anuló un intento que estaba en curso.

```json
{
  "event_id": "3c98863f-67db-45f8-8bb8-f58c704e9c71",
  "event_type": "CHALLENGE_ABORTED",
  "event_version": 1,
  "timestamp": "2026-09-27T16:05:00Z",
  "producer": "tema-03-challenges-service",
  "payload": {
    "resources": {
      "coins": 0.00,
      "xp": 0,
      "add_live": false,
      "subtract_live": false,
      "active_item": []
    },
    "id_user": "09819779-7a70-424a-bb10-91a5e117498c",
    "id_course": "34f19b88-1065-4f46-813c-74cf47113115",
    "id_node": "5d2a7c10-3e4f-4a5b-9c6d-7e8f90a1b2c3",
    "id_attempt": "a4b5c6d7-1111-4222-8333-944455556666",
    "challenge_id": "6f70dc0d-e25f-4053-9387-e07085ea38a3",
    "challenge_version": 2,
    "challenge_type": "NORMAL",
    "content_type": "THEORETICAL",
    "difficulty": "BASIC",
    "mandatory": false,
    "performed_by_user_id": "c0ffee00-aaaa-4bbb-8ccc-ddddeeeeffff",
    "performed_by_role": "PROFESSOR",
    "result": {
      "status": null,
      "score": null,
      "completed_at": "2026-09-27T16:04:59Z",
      "late": false,
      "attempt_number": 2,
      "resolution_time": null,
      "started_at": "2026-09-27T15:50:00Z",
      "submitted_at": null,
      "approval_threshold": 60,
      "max_attempts": 3,
      "last_attempt": false,
      "closure_reason": "CANCELLED",
      "closure_detail": "Consigna publicada con un error"
    }
  }
}
```

## Campos

### Sobre (envelope)

| Campo | Tipo | Detalle |
|---|---|---|
| `event_id` | UUID | Único por evento. Clave de deduplicación |
| `event_type` | string | `CHALLENGE_COMPLETED` o `CHALLENGE_ABORTED` |
| `event_version` | entero | Siempre `1`. Rompe con `agent.md` §5.1 / `bus-notificaciones.md` §1, que daban por cerrado "sin `event_version`, rige el PDF del bus" — **abierto con Notificaciones, ver §"Lo que sigue abierto"** |
| `timestamp` | ISO-8601 UTC | Momento en que se generó el evento |
| `producer` | string | `tema-03-challenges-service` |

### `payload.resources`: lo que se acredita o descuenta

| Campo | Tipo | Detalle |
|---|---|---|
| `coins` | decimal | Monedas que otorga **este** intento (no el saldo) |
| `xp` | entero | Experiencia que otorga **este** intento (delta, no el acumulado) |
| `add_live` | boolean | `true` si el alumno gana una vida |
| `subtract_live` | boolean | `true` si el alumno pierde una vida |
| `active_item` | lista de UUID | `itemInstanceId` de los ítems consumidos en el intento. Nunca `null`: si no hubo, `[]` |

### `payload`: contexto del intento

| Campo | Tipo | Detalle |
|---|---|---|
| `id_user` | UUID | Alumno (nuestro `studentId`) |
| `id_course` | UUID | Curso (nuestro `id_course`) |
| `id_node` | UUID | Nodo de Roadmap desde el que se abrió el intento. **Resolución primaria condicionada** del nodo: resuelve solo si el nodo existe en un roadmap de **ese mismo curso** (`id_course`) **y** su `challenge_id` coincide con el del evento; ese roadmap puede ser el principal o cualquier otro del curso (HT-17). Si existe con un `challenge_id` distinto, Roadmap **no** usa ese nodo inconsistente: registra un WARN y cae a la resolución por `challenge_id`. Si no viene o no existe, también cae a la resolución por `challenge_id` (D-EVCIERRE-02; ver "Resolución del nodo") |
| `id_attempt` | UUID | Intento |
| `challenge_id` | UUID | Desafío |
| `challenge_version` | entero | Versión con la que se resolvió |
| `challenge_type` | enum | `NORMAL`, `LIVES` (recuperación de vida) o `LLM` |
| `content_type` | enum | `THEORETICAL` o `PRACTICAL` |
| `difficulty` | enum | `BASIC`, `MEDIUM` o `ADVANCED` (internamente `EASY`, `MEDIUM`, `HARD`: ver `Difficulty`) |
| `mandatory` | boolean | Si el desafío es obligatorio |
| `performed_by_user_id` | UUID, nullable | Quién provocó el cierre |
| `performed_by_role` | enum | `STUDENT`, `PROFESSOR`, `ADMIN` o `SYSTEM` |

### `payload.result`: el resultado

| Campo | Tipo | Detalle |
|---|---|---|
| `status` | enum, nullable | `APPROVED` o `DISAPPROVE`. `null` en `CHALLENGE_ABORTED` |
| `score` | entero, nullable | Nota de 0 a 100, redondeada. `null` si no hubo corrección |
| `completed_at` | ISO-8601 UTC | Cierre del intento |
| `late` | boolean | Entrega fuera de término. Fijo en `false` por ahora (no hay fecha límite todavía) |
| `attempt_number` | entero | Número de intento del alumno en este desafío |
| `resolution_time` | decimal, nullable | Segundos entre inicio y entrega. `null` si no entregó |
| `started_at` | ISO-8601 UTC | Inicio del intento |
| `submitted_at` | ISO-8601 UTC, nullable | Entrega. `null` si no entregó |
| `approval_threshold` | entero | Umbral de aprobación de la versión |
| `max_attempts` | entero | Intentos permitidos en la versión |
| `last_attempt` | boolean | Si con este intento agotó los permitidos |
| `closure_reason` | enum, nullable | Solo en `CHALLENGE_ABORTED`: `CANCELLED`, `EXPIRED` o `ABANDONED` |
| `closure_detail` | string, nullable | Motivo que escribió el profesor al anular |

## Cómo se calculan los `resources`

El Motor los calcula al cerrar el intento, con los parámetros de Backoffice congelados al abrirlo.
**Roadmap no recalcula nada**: aplica los valores tal como llegan.

| Caso | `coins` | `xp` | `add_live` | `subtract_live` |
|---|---|---|---|---|
| `NORMAL` o `LLM` aprobado | según el desafío | según la dificultad | `false` | `false` |
| `NORMAL` o `LLM` reprobado **con vida reservada** | `0` | `0` | `false` | `true` |
| `NORMAL` o `LLM` reprobado **sin vida reservada** | `0` | `0` | `false` | `false` |
| `LIVES` (recuperación) aprobado | `0` | `0` | `true` | `false` |
| `LIVES` (recuperación) reprobado | `0` | `0` | `false` | `false` |
| Cualquier `CHALLENGE_ABORTED` | `0` | `0` | `false` | `false` |

Un `CHALLENGE_ABORTED` nunca mueve recursos. `active_item` llega vacío por ahora (falta definir
inventario) y `late` en `false` (falta manejar fecha límite); ya están en el contrato para cuando
se activen.

### Quién provocó el cierre

| Caso | `performed_by_user_id` | `performed_by_role` |
|---|---|---|
| `CHALLENGE_COMPLETED` | el alumno | `STUDENT` |
| `CANCELLED` (anulado) | quien anuló | `PROFESSOR` o `ADMIN` |
| `EXPIRED` (el corrector no respondió en 24 h) | `null` | `SYSTEM` |
| `ABANDONED` | el alumno | `STUDENT` |

## Garantías del Motor

- `resources` y `result` vienen siempre, en los dos tipos de evento.
- Ningún campo se omite: si no aplica, viene en `null`. `active_item` nunca es `null`.
- Un campo nuevo no rompe nada: se ignoran los que no se conocen.
- Quitar o renombrar un campo se coordina antes de publicarlo.

## Lo que pidieron y dónde está

**Accounting**: `coins` (acreditar/revertir), `subtract_live`, `add_live`, `active_item`,
`performed_by_user_id`/`performed_by_role`, `id_user`/`id_course`/`result.status` — todos en
`resources` y `payload` de arriba.

**Roadmap**: `id_user`/`id_course`/`challenge_id` → los mismos; `id_node` → nuevo; `xp` →
`resources.xp` (delta); `passed` → `result.status == "APPROVED"`; `esRepeticion` →
`result.attempt_number > 1` (regla del PO: hoy no existen repeticiones, ver `motor-desafios.md`
§2.2; el campo queda disponible si se habilita).

> **`add_live`/`subtract_live` no son de Roadmap (corrección 2026-09-27).** Son enteramente de
> Accounting, incluido el histórico "nunca perdió una vida" que antes se le pedía a Roadmap
> construir desde este evento (`agent.md` §3.1b, versión anterior). Roadmap no los procesa.

## Coordinación con G09 — `id_node` y motivos del gate (T-44.10)

Pedido a G09 registrado en
[tpi-engine-challenge#124](https://github.com/2026-P4-BE/tpi-engine-challenge/issues/124)
(2026-10-08). Roadmap sólo documenta el pedido; **no cambia el contrato del Motor**.

**1. `id_node` real en el evento de cierre.** `payload.id_node` debe ser siempre el nodo con el que
se abrió el intento. Roadmap usa `id_node` para resolver el nodo **solo si el nodo existe y su
`challenge_id` coincide**; si no, cae al fallback por `challenge_id`. El pedido a G09 es
confirmar que el evento siempre traiga el `id_node` real:

- la apertura (`POST /api/engine-challenge/challenges/{challenge_id}/intentos`) recibe `node_id` en
  [`AttemptStartRequest`](https://github.com/2026-P4-BE/tpi-engine-challenge/blob/d07cdbb665a0d1b25e39b81298750379d5218575/src/main/java/ar/edu/utn/frc/tup/p4/shared/api/attempts/AttemptStartRequest.java),
  `@NotNull`: para un intento nuevo el campo **siempre** viene;
- el `nullable` de `attempt.node_id`
  ([`V24__closure_event_node_and_message_key.sql`](https://github.com/2026-P4-BE/tpi-engine-challenge/blob/d07cdbb665a0d1b25e39b81298750379d5218575/src/main/resources/db/migration/V24__closure_event_node_and_message_key.sql))
  y el fallback a `challenge_id` en
  [`AttemptOpeningService`](https://github.com/2026-P4-BE/tpi-engine-challenge/blob/d07cdbb665a0d1b25e39b81298750379d5218575/src/main/java/ar/edu/utn/frc/tup/p4/attempts/service/AttemptOpeningService.java)
  (`UUID id_node = request.id_node() == null ? challenge_id : request.id_node();`) quedan acotados a
  **intentos legacy ya cerrados**, no alcanzan a intentos nuevos.

Evidencia verificada en el repo de G09 `tpi-engine-challenge`, rama `develop`, commit
`d07cdbb665a0d1b25e39b81298750379d5218575` (2026-10-08):

| Evidencia | Qué respalda |
|---|---|
| [`V24__closure_event_node_and_message_key.sql`](https://github.com/2026-P4-BE/tpi-engine-challenge/blob/d07cdbb665a0d1b25e39b81298750379d5218575/src/main/resources/db/migration/V24__closure_event_node_and_message_key.sql) | `attempt.node_id` **nullable** (comentario: intentos abiertos antes de la migración no lo guardan) |
| [`AttemptOpeningService`](https://github.com/2026-P4-BE/tpi-engine-challenge/blob/d07cdbb665a0d1b25e39b81298750379d5218575/src/main/java/ar/edu/utn/frc/tup/p4/attempts/service/AttemptOpeningService.java) | fallback `request.id_node() == null ? challenge_id : request.id_node()` |
| [`AttemptStartRequest`](https://github.com/2026-P4-BE/tpi-engine-challenge/blob/d07cdbb665a0d1b25e39b81298750379d5218575/src/main/java/ar/edu/utn/frc/tup/p4/shared/api/attempts/AttemptStartRequest.java) | `node_id` `@NotNull` en la apertura |

Detalle del pedido en
[tpi-engine-challenge#124](https://github.com/2026-P4-BE/tpi-engine-challenge/issues/124).

**2. Motivos del gate.** El Motor llama a Roadmap
`GET /api/roadmap/courses/{id_course}/students/{studentId}/nodes/{id_node}/eligibility` y ante
no-elegible lanza `StudentNotEligibleException(reason)` con el string crudo (ya se muestra). Pedido:
ampliar el enum cerrado `RoadmapIneligibilityReason` del Motor con dos motivos **PROPUESTA**:

- `group_restricted` — **vigente desde el gate v1.1 (T-44.3)**: HU-44 (roadmap por comisión) — el
  alumno no pertenece a ninguna comisión que habilite el nodo;
- `date_restricted` — **PROPUESTA**: restricciones de fecha (`DATE`) que llegan de Courses
  ([`courses-grupos-t-10-1.md`](courses-grupos-t-10-1.md) §3.4, acta T-10.1);

y confirmar que cualquier motivo nuevo se trata como "no habilitado" y se muestra tal cual
(passthrough del string, sin descartarlo por no estar en el enum).

El vocabulario del gate se versionó del lado **Roadmap**: `group_restricted` figura en `GateReason` y
en el §4 de [`roadmap-motor-gate-v1.md`](roadmap-motor-gate-v1.md) desde la v1.1 (T-44.3), y solo se
emite con el flag `ROADMAP_BY_GROUP_ENABLED` encendido. `date_restricted` sigue siendo **PROPUESTA**:
Roadmap no lo emite ni lo lista en su contrato, a la espera de la tarea que evalúe las restricciones
`DATE` de Courses (acta T-10.1 §3.4).

> **A realinear con G09**: `RoadmapIneligibilityReason` del Motor todavía lleva `RECOVERY_PENDING`
> (`"recovery_pending"`), retirado del gate de Roadmap
> ([`roadmap-motor-gate-v1.md`](roadmap-motor-gate-v1.md) §4). Verificado en
> [`RoadmapIneligibilityReason.java`](https://github.com/2026-P4-BE/tpi-engine-challenge/blob/d07cdbb665a0d1b25e39b81298750379d5218575/src/main/java/ar/edu/utn/frc/tup/p4/shared/integration/roadmap/dto/RoadmapIneligibilityReason.java)
> del repo G09 `tpi-engine-challenge`, rama `develop`, commit
> `d07cdbb665a0d1b25e39b81298750379d5218575` (2026-10-08). Confirmar su retiro del enum del Motor
> en la misma respuesta.

**Estado**: G09 cerró el issue el 2026-10-09 con su PR #127. Verificado en su código (`develop`,
commit `3ee47b4`): `RoadmapIneligibilityReason` incluye `group_restricted` y `date_restricted` y
conserva el `reason` recibido. `RECOVERY_PENDING` sigue en su enum, marcado como deprecado. Queda
pendiente que actualicen su `docs/contracts/roadmap-eligibility.yaml`, que lista cinco valores.

## Lo que sigue abierto (no se resuelve en este documento)

- **`event_version`**: contradice la regla cerrada del PDF del bus (`agent.md` §5.1,
  `bus-notificaciones.md` §1). A confirmar con Notificaciones (Grupo 2), dueño del envelope —
  todavía no sabemos si el bus lo tolera como campo extra ignorable o si rompe algo. **No se
  decide unilateralmente.**
- **Convivencia con el formato anterior** (`ATTEMPT_CORRECTED`/`ATTEMPT_CANCELED` de
  `motor-desafios.md`, o el `CHALLENGE_COMPLETED` sin `resources` de v2): el Motor ya publica
  solo este evento y avisa que `challenges.results` no existe en el broker. El listener de ese
  topic sigue en el código pero **apagado por defecto**
  (`app.kafka.topics.challenge-result.enabled=false`, `autoStartup` del `@KafkaListener`), así
  que no se suscribe al topic inexistente ni genera `UNKNOWN_TOPIC_OR_PARTITION`. **Deuda
  técnica: borrar ese listener, sus payloads v1/v2 y el flag en el próximo sprint.**
- **`id_node`**: la política de resolución está implementada (sección siguiente), pero falta que
  G09 (`tpi-engine-challenge#124`) confirme que el Motor siempre manda un `id_node` consistente
  con el `challenge_id` del intento. No se cierra hasta esa respuesta.

## Resolución del nodo (D-EVCIERRE-02)

Un curso puede tener **varios roadmaps** (HT-17, DEC-017), así que primero se decide **en qué roadmap** se registra el resultado y después **qué nodo** de ese roadmap. Cuando solo hay uno, el comportamiento es el de siempre.

**Paso 0: roadmap del resultado** (T-19.4, `ResultRoadmapLocator`):

- Si el evento trae `id_node` y ese nodo existe, su `challenge_id` coincide con el del evento y su roadmap es **del mismo curso** (`id_course`), el resultado se registra en **ese roadmap**, sea el principal o no.
- En cualquier otro caso (sin `id_node`, nodo inexistente, `challenge_id` distinto o nodo de otro curso) se usa el **roadmap principal del curso**. Si el curso no tiene principal, el evento falla sin reintento (`node.not-found`).

**Resolución del nodo dentro de ese roadmap**, implementada en `ChallengeNodeResolver`:

1. Si el evento trae `id_node`, ese nodo resuelve **solo si existe en el roadmap elegido
   y su `challenge_id` coincide con el del evento**. Si existe pero su `challenge_id` no
   coincide, se registra un `WARN` (`error.node.id-hint-mismatch`), **no** se usa ese nodo
   inconsistente y se pasa al paso 3.
2. Si el evento trae `id_node` pero no existe en el roadmap, se registra un `WARN`
   (`error.node.id-hint-unknown`) y se pasa al paso 3.
3. Fallback por `challenge_id` con cardinalidad estricta, **solo dentro del roadmap elegido en el paso 0** (no se buscan los otros roadmaps del curso): `0` nodos →
   `node.not-found`; `1` nodo → ese nodo; `2+` nodos → `node.challenge-ambiguous`.

Esto preserva la compatibilidad con los eventos legacy (v1/v2) que no incluyen `id_node` y evita
completar un nodo ajeno cuando el `id_node` del evento apunta a un nodo cuyo `challenge_id` no
coincide.

**Efecto en el XP con varios roadmaps (HT-17, T-17.3).** El movimiento del ledger guarda en qué roadmap se ganó (`roadmap_id`) y si suma al total del curso (`counted_in_course`), según el `progress_scope` que tenía ese roadmap al llegar el evento: `COURSE` (por defecto) suma al total del curso; `ROADMAP` queda como XP propio del roadmap. El evento del Motor **no cambia**: el Motor sigue informando por curso y Roadmap asigna el resultado al roadmap que corresponde. Cambiar el modo rige hacia adelante y no reescribe lo anterior.

**Estado del ítem `id_node`:** la política de resolución está **implementada** en
`ChallengeNodeResolver`; el ítem queda **abierto** hasta la confirmación de G09
(`tpi-engine-challenge#124`) de que el Motor siempre manda un `id_node` consistente con el
`challenge_id` del intento. Por eso se mantiene en "Lo que sigue abierto".
