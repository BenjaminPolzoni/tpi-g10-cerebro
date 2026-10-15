# Evento de cierre de intento: Motor de Desafíos (G09)

**Para:** Accounting (Banco) y Roadmap. Cualquier otro micro lo puede consumir igual.
**De:** G09 (Motor de Desafíos)
**Estado:** contrato definido, **en implementación**. El Motor todavía publica el formato anterior; les avisamos cuando esté en `develop`.

## Cómo funciona

- **Un solo evento por intento cerrado, con toda la información.** Cada micro toma lo que necesita e ignora el resto.
- La estructura es la de la imagen que compartimos, con algunos campos agregados a pedido de ustedes.
- Hay dos `event_type`, y **los dos tienen exactamente la misma estructura**:
  - `CHALLENGE_COMPLETED`: el intento se corrigió y tiene veredicto.
  - `CHALLENGE_ABORTED`: el intento se cerró sin veredicto (anulado por un profesor, o el corrector no respondió a tiempo). Es lo que en la imagen aparecía como `ATTEMPT_CANCELED`.

## Canal

| | |
|---|---|
| Topic | `challenges.events` |
| Key del mensaje | `id_user` (orden garantizado por alumno) |
| Formato | JSON plano (`StringSerializer`), sin headers de clase |
| Entrega | at-least-once: **deduplicar por `event_id`** |
| Filtro | por `producer` y `event_type`, porque Tema 05 (Practical) también publica en este topic |

## `CHALLENGE_COMPLETED`

Ejemplo: aprobado, desafío obligatorio.

```json
{
  "event_id": "7a3e813f-b88c-4cf2-9e8a-0d8591ef528c",
  "event_type": "CHALLENGE_COMPLETED",
  "eventVersion": 1,
  "timestamp": "2026-09-27T15:30:00Z",
  "producer": "THEME-02-CHALLENGE-ENGINE",
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
      "completedAt": "2026-09-27T15:29:58Z",
      "late": false,
      "attempt_number": 1,
      "resolution_time": 1420.0,
      "startedAt": "2026-09-27T14:55:10Z",
      "submittedAt": "2026-09-27T15:18:50Z",
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
  "eventVersion": 1,
  "timestamp": "2026-09-27T16:05:00Z",
  "producer": "THEME-02-CHALLENGE-ENGINE",
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
    "difficulty": "EASY",
    "mandatory": false,
    "performed_by_user_id": "c0ffee00-aaaa-4bbb-8ccc-ddddeeeeffff",
    "performed_by_role": "PROFESSOR",
    "result": {
      "status": null,
      "score": null,
      "completedAt": "2026-09-27T16:04:59Z",
      "late": false,
      "attempt_number": 2,
      "resolution_time": null,
      "startedAt": "2026-09-27T15:50:00Z",
      "submittedAt": null,
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
| `eventVersion` | entero | Siempre `1`. Va con este nombre porque la plataforma descarta los mensajes que no lo traen |
| `timestamp` | ISO-8601 UTC | Momento en que se generó el evento |
| `producer` | string | `THEME-02-CHALLENGE-ENGINE` |

### `payload.resources`: lo que se acredita o descuenta

| Campo | Tipo | Detalle |
|---|---|---|
| `coins` | decimal | Monedas que otorga **este** intento (no el saldo) |
| `xp` | entero | Experiencia que otorga **este** intento (delta, no el acumulado) |
| `add_live` | boolean | `true` si el alumno gana una vida |
| `subtract_live` | boolean | `true` si el alumno pierde una vida |
| `active_item` | lista de string | `itemInstanceId` de los ítems consumidos en el intento. Nunca `null`: si no hubo, `[]` |

### `payload`: contexto del intento

| Campo | Tipo | Detalle |
|---|---|---|
| `id_user` | UUID | Alumno |
| `id_course` | UUID | Curso |
| `id_node` | UUID, nullable | Nodo de Roadmap desde el que se abrió el intento. `null` en intentos abiertos antes de este cambio |
| `id_attempt` | UUID | Intento |
| `challenge_id` | UUID | Desafío |
| `challenge_version` | entero | Versión con la que se resolvió |
| `challenge_type` | enum | `NORMAL`, `LIVES` (recuperación de vida) o `LLM` |
| `content_type` | enum | `THEORETICAL` o `PRACTICAL` |
| `difficulty` | enum | `EASY`, `MEDIUM` o `HARD` |
| `mandatory` | boolean | Si el desafío es obligatorio |
| `performed_by_user_id` | UUID, nullable | Quién provocó el cierre (ver tabla de abajo) |
| `performed_by_role` | enum | `STUDENT`, `PROFESSOR`, `ADMIN` o `SYSTEM` |

### `payload.result`: el resultado

| Campo | Tipo | Detalle |
|---|---|---|
| `status` | enum, nullable | `APPROVED` o `DISAPPROVE`, escrito tal cual la imagen. `null` en `CHALLENGE_ABORTED` |
| `score` | entero, nullable | Nota de 0 a 100, redondeada. Es la que usamos para el veredicto. `null` si no hubo corrección |
| `completedAt` | ISO-8601 UTC | Cierre del intento |
| `late` | boolean | Entrega fuera de término |
| `attempt_number` | entero, nullable | Número de intento del alumno en este desafío (`> 1` es repetición). `null` en intentos `LIVES` y `LLM`, que no se numeran |
| `resolution_time` | decimal, nullable | Segundos entre el inicio y la entrega. `null` si no entregó |
| `startedAt` | ISO-8601 UTC | Inicio del intento |
| `submittedAt` | ISO-8601 UTC, nullable | Entrega. `null` si no entregó |
| `approval_threshold` | entero | Umbral de aprobación de la versión |
| `max_attempts` | entero | Intentos permitidos en la versión |
| `last_attempt` | boolean | Si con este intento agotó los permitidos |
| `closure_reason` | enum, nullable | Solo en `CHALLENGE_ABORTED`: `CANCELLED`, `EXPIRED` o `ABANDONED` |
| `closure_detail` | string, nullable | Motivo que escribió el profesor al anular |

## Cómo se calculan los `resources`

El Motor los calcula al cerrar el intento, con los parámetros de Backoffice congelados al abrirlo. **Ustedes no tienen que recalcular nada**: aplican los valores tal como llegan.

| Caso | `coins` | `xp` | `add_live` | `subtract_live` |
|---|---|---|---|---|
| `NORMAL` o `LLM` aprobado | según el desafío | según la dificultad | `false` | `false` |
| `NORMAL` o `LLM` reprobado | `0` | `0` | `false` | `true` |
| `LIVES` (recuperación) aprobado | `0` | `0` | `true` | `false` |
| `LIVES` (recuperación) reprobado | `0` | `0` | `false` | `false` |
| Cualquier `CHALLENGE_ABORTED` | `0` | `0` | `false` | `false` |

**Un `CHALLENGE_ABORTED` nunca mueve recursos:** solo se puede anular un intento que todavía no cerró, así que nunca se acreditó nada que haya que revertir. Y como la vida se descuenta recién al reprobar, tampoco hay una vida que devolver.

**Por ahora, dos campos van con un valor fijo.** `active_item` llega vacío y no se aplican multiplicadores por ítems, porque todavía falta definir de dónde tomamos el inventario del alumno. `late` llega en `false`, porque todavía no manejamos fecha límite de entrega. Los dos campos ya están en el contrato: cuando se sumen, no cambia nada para ustedes.

### Quién provocó el cierre

| Caso | `performed_by_user_id` | `performed_by_role` |
|---|---|---|
| `CHALLENGE_COMPLETED` | el alumno | `STUDENT` |
| `CANCELLED` (anulado) | quien anuló | `PROFESSOR` o `ADMIN` |
| `EXPIRED` (el corrector no respondió en 24 h) | `null` | `SYSTEM` |
| `ABANDONED` | el alumno | `STUDENT` |

## Lo que garantizamos

- `resources` y `result` **vienen siempre**, en los dos tipos de evento.
- **Ningún campo se omite:** si no aplica, viene en `null`. `active_item` nunca es `null`.
- Si agregamos un campo nuevo, no se rompe nada: ignoren los campos que no conozcan.
- **Quitar o renombrar un campo lo coordinamos con ustedes antes de publicarlo.**

## Lo que pidieron y dónde está

**Accounting (Banco):**

| Pidieron | Campo |
|---|---|
| Monedas a acreditar | `resources.coins` en `CHALLENGE_COMPLETED` |
| Monedas a revertir | `resources.coins` en `CHALLENGE_ABORTED` (siempre `0`, ver arriba) |
| `substractLive` | `resources.subtract_live` |
| `addLife` | `resources.add_live` |
| `consumedItems` | `resources.active_item` |
| `performedByUserId` / `performedByRole` | `performed_by_user_id` / `performed_by_role` |
| `idUser` / `idCourse` / `result.status` | `id_user` / `id_course` / `result.status` |

**Roadmap:**

| Esperaban | Campo |
|---|---|
| `studentId` / `courseId` / `challengeId` | `id_user` / `id_course` / `challenge_id` |
| `nodeId` | `id_node` |
| `xp` | `resources.xp` (delta del intento) |
| `lives` / `consumeVida` | `resources.add_live` / `resources.subtract_live` |
| `passed` | `result.status == "APPROVED"` |
| `esRepeticion` | `result.attempt_number > 1` |

## Esto reemplaza lo que les dijimos antes

- **El topic pasa a ser `challenges.events`.** `challenges.results` no existe en el broker de la plataforma.
- **El evento ahora trae monedas, experiencia y vidas.** Antes les habíamos dicho que no.
- **Los nombres de los campos siguen la imagen**, no los que usa hoy el Motor (`studentId`, `verdict`, etc.).
