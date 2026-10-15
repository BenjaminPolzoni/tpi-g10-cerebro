# Motor de Desafíos (G09) → Roadmap (T10) — v2

Respuesta a las cinco consultas, verificada contra la rama `develop` del motor al 25/09/2026.

> **Esta versión reemplaza la anterior.** Cambió la respuesta 2: al revisarla en detalle encontramos que **les estamos mandando el resultado ya calculado y nos estamos guardando los datos con los que lo calculamos**, así que ustedes no pueden aplicar criterio propio ni recalcular nada. Está corregido y propuesto abajo, en "2.4".

## Antes que nada: tres cosas que atraviesan todo

1. **Nuestro segmento es `/api/engine-challenge`, no `/api/challenge`.** Sale de la property `app.api.private-path` y así está dado de alta en el Gateway. Cualquier path armado con `/api/challenge` no nos llega.
2. **No validamos JWT** (DEC-08 del spec del Gateway). La identidad llega en headers ya validados: `X-User-Id` y `X-User-Roles` para personas, `X-Service-Id` y `X-Service-Scopes` para llamadas entre micros. Toda llamada de ustedes tiene que pasar por el Gateway con token de servicio.
3. **Los errores salen en RFC 9457** (`application/problem+json`), con `type`, `title`, `status`, `detail`, `instance` y `requestId` opcional.

### Resumen de discrepancias

| Lo que asumieron | Cómo es en realidad |
|---|---|
| `GET /api/challenge/catalog/exists` | No existía. **Ya lo construimos**, ver punto 1 |
| Topic `challenge-events` (`app.kafka.topics.challenge-result`) | Topic `challenges.results`, property `app.kafka.topic.results` |
| El evento trae `xp`, `lives`, `consumeVida`, `nodeId` | No trae ninguno de los cuatro |
| El evento les da con qué calcular | **Hoy no. Les da el resultado ya calculado. Ver 2.4** |
| `GET .../eligibility` → `{eligible, reason}` | Hacemos `POST` y esperamos una autorización firmada |
| `ATTEMPT_CANCELED` | Se llama `CHALLENGE_ABORTED`, con `reason = CANCELLED` |

---

## 1. Catálogo: `existsChallenge` — RESUELTO

Su path no existía. **Ya está implementado el definitivo** (PR #36, pendiente de merge):

```
GET /api/engine-challenge/challenges/{challengeId}
```

**200:**

```json
{
  "id": "6f70dc0d-e25f-4053-9387-e07085ea38a3",
  "status": "PUBLISHED",
  "currentVersion": 3,
  "type": "PRACTICAL"
}
```

| Campo | Tipo | Detalle |
|---|---|---|
| `id` | UUID | Identificador estable del desafío |
| `status` | enum | `DRAFT`, `PUBLISHED` o `ARCHIVED` |
| `currentVersion` | entero, nullable | Versión vigente; `null` si todavía no tiene |
| `type` | enum | `THEORETICAL` o `PRACTICAL` |

- **Autenticación:** token de servicio con el scope `challenges.catalog.read`, o sesión de PROFESSOR/ADMIN. Alumno 403, sin identidad 401. *El alta del scope en el Gateway está pendiente del equipo Gateway/Identity; hasta que eso pase, sus llamadas no van a llegar.*
- **404** en `problem+json` si no existe.
- **Un desafío archivado responde 200 con `status: ARCHIVED`, no 404.** Es deliberado: tienen que poder distinguir "no existe" de "existe pero ya no se puede usar".
- **No devuelve** título, consigna ni referencia de material.
- El timeout de 2s no es problema: es una lectura por id.

Avisamos cuando mergee para que saquen el doble `PendingMotorCatalogClient`.

---

## 2. `CHALLENGE_COMPLETED`

> **Superada por `motor-desafios-evento-cierre.md` (2026-09-27).** El Motor revirtió la decisión
> de este punto 2: ya no es "solo veredicto académico", ahora calcula y manda `xp`, `coins`,
> `add_live`/`subtract_live` y `active_item`. Topic, key y forma del payload también cambiaron
> (`challenges.events` / `id_user`, no `challenges.results` / `attemptId`). Se conserva esta
> sección como historia; el resto del documento (catálogo §1, gate §4, corrección diferida §5)
> sigue vigente.

### 2.1 Canal (histórico, ver nota de arriba)

- **Topic:** `challenges.results` (property `app.kafka.topic.results`). El default `challenge-events` no existe de nuestro lado.
- **Key:** `attemptId`, garantiza orden por intento dentro de la partición.
- **Entrega:** at-least-once con patrón outbox. **Deduplicar por `eventId`.**
- **Envelope:** `{ eventId, eventType, timestamp, producer, payload }`, `producer = "challenges-service"`, JSON camelCase, timestamps ISO-8601 UTC.

### 2.2 Payload actual

```json
{
  "eventId": "7a3e813f-b88c-4cf2-9e8a-0d8591ef528c",
  "eventType": "CHALLENGE_COMPLETED",
  "timestamp": "2026-09-20T23:15:30.125000Z",
  "producer": "challenges-service",
  "payload": {
    "eventId": "7a3e813f-b88c-4cf2-9e8a-0d8591ef528c",
    "attemptId": "e1582fc8-12c8-4770-bc56-02f4a13d7821",
    "openingAuthorizationId": "8f5d0701-d0ba-40a2-944f-d0061e803a64",
    "studentId": "09819779-7a70-424a-bb10-91a5e117498c",
    "courseId": "34f19b88-1065-4f46-813c-74cf47113115",
    "challengeId": "6f70dc0d-e25f-4053-9387-e07085ea38a3",
    "version": 2,
    "type": "PRACTICAL",
    "difficulty": "MEDIUM",
    "mandatory": true,
    "score": 85.50,
    "verdict": "PASSED",
    "resolutionTimeSeconds": 1420,
    "attemptNumber": 1,
    "lastAttempt": false,
    "occurredAt": "2026-09-20T23:15:28.000000Z"
  }
}
```

### 2.3 Sobre `xp`: no es delta ni total, no lo mandamos

El evento no lleva XP, vidas ni monedas, y es una decisión de arquitectura: el motor es un evaluador académico, no un calculador de progresión ni un ledger. Eso no cambia.

Lo que sí cambia es lo de abajo.

### 2.4 Corrección: hoy les damos el resultado calculado, no los insumos

Revisando el código encontramos un problema real en lo que les habíamos contestado. Les decimos "apliquen sus propias fórmulas", pero **dos campos del payload ya son una decisión nuestra, y no les mandamos los parámetros con los que la tomamos**:

| Campo | Cómo sale |
|---|---|
| `verdict` | **Calculado por nosotros**: `resolveVerdict(nota, version.approvalThreshold)`. **No les mandamos el umbral.** |
| `lastAttempt` | **Calculado por nosotros**: compara el número de intento contra `1 + version.retries`. **No les mandamos `retries`.** |
| `resolutionTimeSeconds` | **Calculado por nosotros**, desde los timestamps. No les mandamos los timestamps crudos. |
| `score` | Dato crudo: la nota tal cual la informó el corrector. |
| `type`, `difficulty`, `mandatory`, `version` | Datos crudos de la versión con la que se resolvió el intento. |
| `attemptNumber` | Dato crudo. |

En la práctica eso significa que **no pueden aplicar criterio propio ni recalcular nada**: solo pueden confiar en nuestro veredicto. Si su fórmula de XP quisiera, por ejemplo, premiar por margen sobre el umbral, o penalizar distinto según cuántos intentos le quedaban, hoy no tienen con qué.

**Propuesta: agregamos al payload los insumos crudos.** Lo podemos hacer sin romperles nada, porque son campos nuevos:

| Campo propuesto | Para qué les sirve |
|---|---|
| `approvalThreshold` | Umbral de la versión. Con `score` pueden calcular el margen y aplicar su propio criterio |
| `maxAttempts` | `1 + retries` de la versión. Con `attemptNumber` saben cuántos le quedaban |
| `startedAt`, `submittedAt`, `completedAt` | Timestamps crudos, por si quieren medir distinto que nuestro `resolutionTimeSeconds` |

**`verdict` se queda igual**, porque que el umbral lo aplique Challenge es un acuerdo cerrado del sprint (ningún otro servicio declara un veredicto propio). La diferencia es que ahora van a poder ver **con qué** lo aplicamos, en vez de recibir solo el sí o el no.

**Díganos qué campos necesitan y los agregamos.** Si quieren otros que no están en la lista, pídanlos: es mejor definirlo ahora que cuando ya estén consumiendo en producción.

### 2.5 Contra el payload que esperaban

| Esperaban | Está | Cómo resolverlo |
|---|---|---|
| `courseId`, `studentId`, `challengeId` | Sí | — |
| `passed` | No | Usen `verdict` (`PASSED` / `FAILED`) |
| `esRepeticion` | No | `attemptNumber > 1`; además va `lastAttempt` |
| `nodeId` | No | El motor no conoce nodos. Si lo necesitan, mándenlo en la autorización de apertura y lo propagamos |
| `xp`, `lives`, `consumeVida` | No | Los calculan ustedes y Wallet, con los insumos de 2.4 |

### 2.6 El otro evento que publicamos

`CHALLENGE_ABORTED`, en el mismo topic:

```json
{ "eventId": "...", "attemptId": "...", "openingAuthorizationId": "...",
  "studentId": "...", "courseId": "...", "challengeId": "...",
  "reason": "EXPIRED", "occurredAt": "..." }
```

`reason` puede ser `EXPIRED`, `CANCELLED` o `ABANDONED`. Si para compensar necesitan más contexto (por ejemplo `attemptNumber`), pídanlo y lo agregamos junto con lo de 2.4.

---

## 3. Baja o modificación de un desafío ubicado

**Hoy no emitimos ningún evento cuando un desafío se archiva o se edita.** Solo publicamos cierres de intento. Si lo necesitan, hay que agregar un evento nuevo (algo tipo `CHALLENGE_ARCHIVED`): díganlo y lo damos de alta.

Probablemente no haga falta para el caso que les preocupa, por cómo está resuelto el versionado:

- **Editar un desafío publicado no toca los intentos en curso.** Cada intento queda atado a la versión con la que se abrió y se evalúa siempre contra esa. Una edición no les rompe nada retroactivamente.
- **Archivar es baja lógica.** Bloquea aperturas nuevas; los intentos abiertos siguen su curso y terminan.

**Sobre el nombre del evento:** no existe `ATTEMPT_CANCELED`. Cuando se anula un intento emitimos `CHALLENGE_ABORTED` con `reason = CANCELLED`.

**Aviso importante:** la lógica de anulación existe, pero **todavía no está expuesta por HTTP**, así que hoy nadie puede anular un intento desde afuera. Ya lo tomamos como trabajo propio y lo vamos a implementar; les avisamos cuando esté.

**Sobre su criterio** (anulación como movimiento compensatorio append-only, nunca update ni borrado, 404 `node.not-found` y conservar XP y desbloqueos): **lo aprobamos**. Es coherente con cómo trabajamos: nunca borramos ni pisamos en destructivo, y el intento conserva su versión y su resultado.

---

## 4. Gate de elegibilidad

Dos confirmaciones que pidieron, las dos en sí:

- **Llamamos a Roadmap antes de crear el intento.** Si no hay respuesta válida no se persiste nada: fail-closed, 503, sin intento colgado.
- **El 201 ya devuelve el `attemptId`.** La respuesta es `{ attemptId, challengeId, challengeVersionId, courseId, attemptNumber, status, startedAt }`, sobre `POST /api/engine-challenge/challenges/{challengeId}/intentos` con body `{ courseId }` y rol STUDENT.

**Pero el contrato que implementamos no es el que describen:**

| | Lo que hicieron | Lo que hicimos |
|---|---|---|
| Método | `GET` | `POST` |
| Path | `/api/roadmap/courses/{courseId}/students/{studentId}/nodes/{nodeId}/eligibility` | configurable (`app.roadmap.eligibility-path`) |
| Request | por path params, incluye `nodeId` | body `{ alumno_id, desafio_id, curso_id }` |
| Response | `{ eligible, reason }` | autorización firmada |

Lo que esperamos como respuesta:

```json
{ "autorizacion_id": "...", "alumno_id": "...", "desafio_id": "...",
  "emitida_en": "...", "expira_en": "...", "firma": "..." }
```

Validamos, antes de abrir el intento, que el alumno y el desafío coincidan con lo pedido, que venga firma y que no esté vencida. Un 403 lo leemos como "no elegible" y devolvemos 403 al alumno; cualquier otra falla es 503 sin crear intento.

**Preferimos la autorización firmada** por un motivo concreto: guardamos el `autorizacion_id` en el intento y se los devolvemos en el evento como `openingAuthorizationId`. Eso permite trazar con qué permiso se abrió cada intento y detectar reuso. Con `{ eligible, reason }` eso se pierde.

Si van por el GET, necesitamos que devuelva **al menos un identificador de autorización**. Su vocabulario de razones (`not_enrolled`, `course_archived`, `content_not_read`, `prerequisite_pending`, `no_lives`, `recovery_pending`) lo mapeamos sin problema.

**Esto es lo más urgente de todo el documento:** hoy `app.roadmap.eligibility-path` está vacío, así que **toda apertura de intento responde 503**. Sin cerrar esto no hay flujo de punta a punta.

---

## 5. Corrección diferida

**Confirmado: el evento sale solo con el intento ya corregido.** La entrega no publica nada. El flujo es:

```
entrega (SUBMITTED) → despacho al corrector → callback firmado →
aplicamos el umbral → veredicto → COMPLETED → outbox → Kafka
```

El umbral lo aplica el motor con el valor de la **versión con la que se abrió el intento**; el corrector solo informa la nota.

**Nunca se quedan esperando un cierre que no llega:** si el callback no aparece dentro del plazo (`app.correction.deadline-hours`, hoy 24h), cerramos el intento como FAILED y emitimos `CHALLENGE_ABORTED` con `reason = EXPIRED`.

**Sobre los scores de IA: hoy no existe el concepto de "pendiente".** El callback trae `score_uso_ia` opcional en el mismo mensaje que la nota; no lo persistimos ni lo publicamos, y no hay estado intermedio. Si RF-IA-34 necesita bloquear el archivado hasta que llegue, hay que definir con T04/T05:

- **(a)** el corrector no dispara el callback hasta tener todo → no cambia nada de nuestro lado;
- **(b)** manda la nota primero y completa el score de IA después → implica un segundo callback, un estado nuevo nuestro y un evento adicional para avisarles.

Nos adaptamos a lo que acuerden, pero hoy no está.

---

## Qué vamos a hacer de nuestro lado

Ya hecho o en curso, sin esperar respuesta:

1. **El endpoint de catálogo del punto 1 ya está implementado** (PR #36), con sus tests y el contrato documentado. Les avisamos al mergear.
2. **Vamos a exponer la anulación de intento** por HTTP, que hoy existe solo como lógica interna. Ya está tomado como trabajo propio.
3. **Ofrecemos ampliar el payload del evento** con los insumos crudos del punto 2.4 (`approvalThreshold`, `maxAttempts`, timestamps). Lo hacemos apenas nos digan cuáles necesitan.
4. **Sostenemos el límite** de no mandar XP, monedas ni vidas, y les documentamos todo lo necesario para que los calculen ustedes.

Lo que necesitamos de ustedes, en orden de urgencia:

1. **Definir el gate (punto 4).** Hoy toda apertura responde 503. Es lo único que bloquea el flujo completo.
2. **Decirnos qué campos del punto 2.4 necesitan** para calcular XP y vidas. Si no nos dicen nada, van a seguir recibiendo solo el veredicto.
3. **Confirmar que el topic es `challenges.results`** y que van a deduplicar por `eventId`.
4. **Decirnos si necesitan `nodeId` en el evento.** Si es que sí, tienen que mandárnoslo en la autorización de apertura: el motor no conoce nodos.
5. **Decirnos si necesitan enterarse del archivado de un desafío.**
6. **Definir con T04/T05 el tema del score de IA** (punto 5).

Para el punto 1 conviene una llamada corta: son dos contratos incompatibles y por mensajes se estira.

— Equipo G09, Motor de Desafíos
