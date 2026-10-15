# Contrato Roadmap ↔ Motor de Desafíos (Grupo 9)

Estado: **§1 y la mayor parte de §4 quedan reemplazadas por
[`motor-desafios-evento-cierre.md`](motor-desafios-evento-cierre.md) (2026-09-27), la fuente
vigente del evento de cierre de intento.** Se conservan §1–§4 como historia (el Motor pasó por
`ATTEMPT_CORRECTED`/`ATTEMPT_CANCELED` → `CHALLENGE_COMPLETED` sin recursos, en
`respuesta-motor-a-roadmap-v2.md` §2 → el evento único con `resources` de hoy). El rework nuestro
de código (§5) y el gate (§6) siguen sin tocar por este cambio: el gate es un contrato aparte
(REST síncrono, ver `roadmap-motor-gate-v1.md` y `respuesta-motor-a-roadmap-v2.md` §4, todavía con
preguntas abiertas propias). Base: `agent.md` §3.0, §3.1 y §5; `docs/T-03-1-LISTENER-RESULTADO-MOTOR.md`.

Cubre: **T-03.2** (schema del evento consumido) y el gate síncrono de habilitación.

> **Grupos**: Motor de Desafíos es el **Grupo 9**; Notificaciones es el **Grupo 2**. Las
> referencias a "Grupo 09" de `docs/T-03-1-...md` y `docs/T-03-3-...md` quedan así confirmadas.

---

## 1. El evento real: `ATTEMPT_CORRECTED`

Payload que nos pasó el Grupo 9:

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

### 1.1 Las dos fases del intento

Un intento pasa por **`TERMINADO`** y después por **`CORREGIDO`**, porque **los profesores corrigen
manualmente cada intento por separado**. Este evento corresponde a la corrección.

- Roadmap consume **solo `ATTEMPT_CORRECTED`**. La fase `TERMINADO` no nos interesa; si publican un
  evento para ella, nuestro listener lo registra como `event_type` desconocido y avanza el offset.
- **Consecuencia operativa**: entre que el alumno termina y que un profe corrige puede pasar
  tiempo indefinido. Durante esa ventana el alumno **no suma XP y no se le desbloquea el nodo
  siguiente**. No es un defecto del contrato, pero el equipo tiene que saberlo, y refuerza que no
  se pueda archivar un curso con intentos sin corregir (RF-IA-34).

### 1.2 Campo por campo

| Campo | Lo usamos | Nota |
|---|---|---|
| `event_id` | **Sí** | Idempotencia. `uq_xp_movement_event_id`: un duplicado no suma dos veces |
| `event_type` | **Sí** | `ATTEMPT_CORRECTED`. Reemplaza al `CHALLENGE_COMPLETED` que habíamos supuesto |
| `timestamp` | Sí | Momento del hecho, UTC |
| `producer` | No | No ramificamos por productor. Ver §4.4: el string parece mal etiquetado |
| `resources.xp` | **Sí** | **XP ya calculado**, con todos los multiplicadores aplicados. Se guarda tal cual, nunca se recalcula (RF-CFG-06) |
| `resources.coins` | **No** | Monedas son de Wallet / Accounting. Roadmap no toca monedas (`agent.md` §2.2) |
| `resources.substract_live` | **Sí** | Para el histórico "nunca perdió una vida" (RF-RNK-05/11/12). Semántica a confirmar (§4.2) |
| `resources.active_item` | **No** | Roadmap no lo procesa. El acta Accounting ↔ Roadmap v1 reemplaza la suposición anterior: Roadmap no envía ítems a Motor al iniciar |
| `id_user` | **Sí** | Nuestro `studentId` |
| `id_course` | **Sí** | Nuestro `courseId` |
| `challenge_id` | **Sí** | Con esto resolvemos el nodo del roadmap |
| `challenge_version` | **No** | Un desafío ya aprobado **queda aprobado** y el alumno sigue su ruta; la versión nueva solo afecta a quien todavía no lo hizo. No lo persistimos |
| `challenge_type` | Ver §4 | `NORMAL` / `LIVES` / `LLM`. `LIVES` es el desafío de recuperación de vida (RF-REC-04/06), que el **gate** necesita conocer **antes** del intento |
| `difficulty` | **No** | Fuera de nuestro scope: solo nos interesa el XP que viene para sumarlo |
| `mandatory` | Ver §4.1 | Lo necesita RF-RNK-05 (100 % de los obligatorios aprobados para ser candidato a promoción) |
| `result.status` | **Sí** | `APPROVED` / `DISAPPROVE`. Reemplaza al `passed` booleano que habíamos supuesto |
| `result.score` | **No** | Es la nota, no el XP. El XP ya viene calculado en `resources.xp` |
| `result.completed_at`, `late`, `resolution_time` | **No** | Insumos del cálculo de XP, que hace el Motor |
| `result.attempt_number` | **No** | Informativo. Ver §2.2: no sirve para detectar repeticiones y ya no hace falta |

### 1.3 El evento de anulación: `ATTEMPT_CANCELED`

Contrato recibido para la anulación de un intento:

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

Diferencias con `ATTEMPT_CORRECTED`:
- `event_type`: `ATTEMPT_CANCELED`.
- `resources.add_live`: sustituye a `substract_live` (indica si se devuelve/suma vida).
- `result.completedAt`: camelCase en el ejemplo enviado (en `ATTEMPT_CORRECTED` figuraba `completed_at`). En Roadmap soportamos ambos alias (`completed_at` y `completedAt`) en ambos eventos.
- `resources.xp`: asumido positivo indicando el monto a revertir (ver §4.5).
- **Procesamiento en Roadmap**: se valida el schema estricto y se registra un log informativo (`event.attempt-canceled-pending`). La lógica de compensación de XP y anulación de completados queda reservada para una tarea posterior (D-HU3-07).

---

## 2. Puntos cerrados con el Grupo 9

### 2.1 El XP viene calculado
Confirmado: `resources.xp` es el XP final, con todos los multiplicadores ya aplicados. Roadmap
**no calcula XP** y lo guarda tal cual (`agent.md` §3.1, RF-CFG-06).

### 2.2 No existen las repeticiones — cae REQ-MOT-03
**Regla del PO: un alumno no puede volver a hacer un ejercicio que ya aprobó.** Puede llegar a ser
configurable por el profesor más adelante, pero hoy no.

Consecuencias:
- **`esRepeticion` desaparece del contrato.** No viene en el payload y no hace falta.
- `attempt_number` **no** lo reemplaza: un alumno que falló el intento 1 y aprobó el 2 llega con
  `attempt_number = 2` y **sí tiene que cobrar el XP**. Distinguir reintento legítimo de repetición
  con ese campo es imposible, y ya no hace falta.
- Se elimina de `ProgressService.recordResult` el camino de descarte por repetición y su test
  (CA2 / BDD-3 de HU-03).
- **Recomendación**: conservar igual la guarda de `completed_node` (si el nodo ya está completado
  para ese alumno, no volver a sumar XP). Cuesta una línea, protege el ledger y el ranking si la
  regla se vuelve configurable, y cubre el caso de la re-corrección (§4.1).

### 2.3 Versionado de desafíos
Un desafío aprobado queda aprobado. Si se publica una versión nueva, afecta solo a quien todavía
no lo hizo. Roadmap ignora `challenge_version` y `completed_node` no cambia.

### 2.4 Qué ignoramos de la vuelta
`coins` van a Wallet, `active_item` a Inventario, `difficulty` no está en nuestro scope. El
`@JsonIgnoreProperties(ignoreUnknown = true)` que ya tenemos los descarta sin ruido.

---

## 3. Casing del envelope: snake_case vs camelCase

El evento viene en **snake_case** (`event_id`, `event_type`). Nuestro `EventEnvelope` está en
**camelCase** porque así lo muestra el PDF del bus citado en `agent.md` §5.1
(`"eventId"`, `"eventType"`).

**No es un bloqueante**: adaptarnos cuesta una anotación de Jackson. Pero la decisión no es del
Grupo 9 ni nuestra: **el dueño del envelope es Notificaciones (Grupo 2)**. Si cada productor elige
su propio casing, cada consumidor termina con un mapper distinto por productor.

→ Pregunta escalada a `docs/contracts/bus-notificaciones.md`. Mientras tanto, nos adaptamos a
snake_case, que es lo que realmente llega.

---

## 4. Lo que sigue abierto (Preguntas para Grupo 9)

### 4.1 🔴 Pregunta 1: Signo de `xp` en `ATTEMPT_CANCELED`
En el contrato recibido para `ATTEMPT_CANCELED`, `resources.xp` figura como número positivo (ej. `250`).
- **Nuestra asunción en HU3-T03.2 (D-HU3-07)**: Asumimos que `resources.xp` siempre viaja como una magnitud positiva que indica el monto a descontar / revertir.
- **Pregunta**: ¿Se confirma que `xp` es un valor positivo o puede llegar con signo negativo (ej. `-250`)? Roadmap valida el schema; la anulación efectiva se implementará en una tarea posterior.

### 4.2 🔴 Pregunta 2: Confirmación de formato UUID en identificadores
En el payload de ejemplo se observan placeholders como `"id_user": "id_user"`, `"id_course": "id_course"`, `"challenge_id": "challenge_id"`.
- **Nuestra implementación en HU3-T03.2 (D-HU3-06)**: Validamos de forma estricta que los tres identificadores parseen a `java.util.UUID` estándar (RFC 4122). Si alguno no es un UUID válido, el evento se descarta como poison pill con log WARN.
- **Pregunta**: ¿Se confirma que en producción los 3 IDs son UUIDs v4 o similares válidos?

### 4.3 🔴 Pregunta 3: Formato de Timestamps ISO-8601 con Offset
Tanto en `timestamp` del envelope como en `result.completed_at` / `result.completedAt`:
- **Nuestra implementación en HU3-T03.2 (D-HU3-04)**: Exigimos JSON strings formateados según ISO-8601 con offset explícito (`Z` o `±hh:mm`), convertidos a UTC `Instant`. Epochs numéricos, strings sin offset (hora local) o valores malformados son rechazados inmediatamente.
- **Pregunta**: ¿Se confirma que el Motor siempre emitirá strings ISO-8601 con offset UTC (`Z`) o huso horario?

### 4.4 🔴 Pregunta 4: Estandarización de casing entre eventos
- En `ATTEMPT_CORRECTED` se definió `completed_at` (snake_case) y `substract_live`.
- En `ATTEMPT_CANCELED` se definió `completedAt` (camelCase) y `add_live`.
- **Nuestra implementación en HU3-T03.2 (D-HU3-05)**: Roadmap acepta tolerar ambos casings mediante `@JsonProperty("completed_at") @JsonAlias("completedAt")`.
- **Pregunta**: ¿Se planea estandarizar la nomenclatura entre eventos del Motor para evitar discrepancias de casing y nombres de campos (`substract_live` con falta de ortografía vs `add_live`)?

### 4.5 🔴 Re-corrección: ¿el `xp` es total o delta?
Como la corrección es **manual**, ¿un profesor puede volver a corregir un intento ya corregido?
Si la respuesta es sí, llega un **segundo `ATTEMPT_CORRECTED` del mismo desafío con otro `event_id`**, y la idempotencia por `event_id` no nos salva:
- Si `resources.xp` es el **total** del intento → hay que reemplazar el movimiento anterior.
- Si es el **delta** → hay que sumarlo.
- Si no puede haber re-corrección → se conserva el registro inicial y no se duplica.

### 4.6 🟠 Semántica de `substract_live`
¿`true` significa **"se descontó una vida"** (hecho consumado, Inventario ya la restó) o **"hay que descontarla"**?
Nota: Roadmap no interpreta vidas en esta tarea (D-HU3-01); se transportan en los DTOs para uso futuro.

### 4.7 🟠 `mandatory` y `challenge_type`: ¿de quién son?
- `mandatory` (RF-RNK-05 para promoción): ¿es dato propio del nodo en Roadmap o fuente de verdad del Motor?
- `challenge_type: LIVES` (desafío de recuperación, RF-REC-04/06): el gate necesita saberlo antes del inicio.

### 4.8 🟡 Detalles adicionales
- **`"DISAPPROVE"`**: Confirmar si es el literal exacto (vocabulario cerrado mapeado en `AttemptStatus`).
- **`producer`**: String `"THEME-02-CHALLENGE-ENGINE"` difiere de la convención de nombres de servicio del bus.

---

## 5. Rework de nuestro lado (Completado en HU3-T03.2)

El schema de eventos y su integración en Roadmap han sido implementados y validados:

| Archivo | Estado en HU3-T03.2 |
|---|---|
| `events/EventEnvelope.java` | Implementado: Soporta camelCase y snake_case vía `@JsonAlias`. Deserializador estricto de timestamps ISO-8601. Captura de campos desconocidos vía `@JsonAnySetter`. |
| `events/AttemptCorrectedPayload.java` | Implementado: Records anidados `Resources` y `Result`, enums tipados, validación estricta en `isComplete()`. |
| `events/AttemptCanceledPayload.java` | Implementado: Schema de anulación con `add_live`, `completed_at`/`completedAt` y validación `isComplete()`. |
| `events/AttemptStatus.java`, `ChallengeType.java`, `Difficulty.java` | Implementado: Enums con valores literales del contrato. |
| `events/StrictTimestampDeserializer.java` | Implementado: Rechazo de numéricos y fechas sin offset; normalización a UTC `Instant`. |
| `events/RoadmapEventListener.java` | Implementado: Ruteo de `ATTEMPT_CORRECTED` a `recordResult` y recepción/log de `ATTEMPT_CANCELED`. Logging WARN de campos desconocidos. `ObjectMapper` local estricto. |
| `dtos/ProgressDtos.ChallengeResult` | Implementado: Adaptado a `idUser`, `idCourse`, `challengeId`, `passed`, `xp`, `subtractLive` (sin `nodeId` ni `esRepeticion`). |
| `services/ProgressService.recordResult` | Implementado: Resolución de nodo por `challengeId`, eliminación de camino de repetición, aplicación de XP. |
| `test/ChallengeResultListenerTest` | Implementado: 28 pruebas cubriendo todos los casos de contrato, fallas de validación, concurrencia e idempotencia. |

---

## 6. Gate de habilitación (síncrono, Motor → Roadmap)

El contrato vigente de Sprint 1 está versionado en
[`roadmap-motor-gate-v1.md`](roadmap-motor-gate-v1.md). Esta sección conserva el resumen dentro
del contrato general con Motor.

Implementado en `controllers/GateController.java` y `services/GateService.java`:

```
GET /api/roadmap/courses/{courseId}/students/{studentId}/nodes/{nodeId}/eligibility
```

```json
{ "data": { "eligible": true,  "reason": null } }
{ "data": { "eligible": false, "reason": "prerequisite_pending" } }
```

- El `studentId` viaja en el **path**, no en un header: Motor llama como servicio
  (`X-Principal-Type: service`), así que `X-User-Id` no aplica.
- `courseId` es el **`courseCohortId`** de Courses (`docs/contracts/courses.md`).
- Evalúa sin efectos: no crea intentos ni modifica progreso.
- `404` si el nodo no existe o no es de ese curso; `403` si el nodo no está disponible.

Vocabulario cerrado de `reason` (`models/GateReason.java`): `not_enrolled`, `course_archived`,
`content_not_read`, `prerequisite_pending`, `no_lives`.

### Estado real de nuestro lado

Devuelve un solo `reason`, el primero que falla en este orden:

| Orden | `reason` | Estado |
|---|---|---|
| 1 | `course_archived` | Evaluado (roadmap archivado) |
| 2 | `not_enrolled` | Evaluado contra `student_course` (matrícula activa del mismo curso), que hoy pueblan los eventos de inscripción de `courses.events` (depende de Courses) |
| 3 | `content_not_read` | Evaluado |
| 4 | `prerequisite_pending` | Evaluado |
| 5 | `no_lives` | Vidas **libres** (`currentLives - reservedLives`) vía `InventoryClient`. Los nodos con `livesPolicy` `RECOVERY` o `LLM` lo saltean sin consultar vidas (T-15.4) |

Una caída de Accounting sin caché vigente produce HTTP 503 Problem Details; nunca `no_lives` ni
`eligible=true`. Haber completado un nodo no agrega una razón: Motor administra los intentos y
reintentos.

La aprobación nominal Roadmap ↔ Motor continúa pendiente de registro; no se infiere de esta
actualización técnica.

---

## 7. Fuera de este contrato

- Topic donde publica el Motor, DLQ, Message Key y el **casing del envelope**: son de
  **Notificaciones, Grupo 2** (`docs/contracts/bus-notificaciones.md`).
- Vidas vigentes e inventario: son responsabilidad de **Accounting**. Roadmap no los envía a
  Motor al iniciar (`docs/contracts/accounting-roadmap-v1.md`).
- Después de `eligible=true`, Motor inicia su flujo con Accounting mediante `ATTEMPT_INIT` y recibe
  `RESERVATION_CREATED` o `RESERVATION_REJECTED`. Roadmap no reserva vidas o ítems, no participa
  de Hold/Commit/Release y no interviene en `challenges.reservations` ni `accounting.holds`.
- Matrícula y estado del curso: son de **Courses** (`docs/contracts/courses.md`).
- La URL de redirección post-`201` hacia Teórico o Práctico: la acuerdan Motor y el frontend.

---

## 8. Qué cerramos con cada respuesta

| Si responden | Cerramos | Si no responden |
|---|---|---|
| **§4.5** — re-corrección, total o delta | El ledger queda protegido ante una segunda corrección del mismo intento | Una re-corrección **suma XP dos veces** y corrompe el ledger y el ranking |
| **§4.6** — `substract_live` | El contador histórico de vidas perdidas → desempate (RF-RNK-11) y candidatura a promoción (RF-RNK-05/12) | El criterio "nunca perdió una vida" no se puede calcular con confianza |
| **§4.7** — `mandatory` y `challenge_type` | El criterio "100 % de los obligatorios" (RF-RNK-05) y el gate del desafío de recuperación (RF-REC-04/06) | Un alumno con 0 vidas no puede ni recuperarlas, y no hay candidatos a promoción |
| **§4.1–§4.4, §4.8** — formato y detalles | Integración sin sorpresas de parseo | Se descubren contra el broker real, que es el peor momento |
| **§6** — gate | Contrato funcional versionado; resta registrar la aprobación nominal | Sin firma nominal, el acta no puede declararse formalmente aprobada |

### Lo mínimo para no frenarnos
**§4.5.** El schema ya está implementado (§5); la re-corrección es lo único que puede corromper
el ledger. El resto puede seguir abierto.

### Lo que el Grupo 9 gana
- Con **§6** tienen el gate real, ya implementado, y dejan de crear intentos que el alumno no
  debería poder tomar.
- Una vez conectado el circuito, publicamos `NODE_COMPLETED` y `NODE_UNLOCKED`: si les sirve saber
  cuándo un alumno abre un camino nuevo, los pueden consumir.

### Lo que NO depende de ustedes
Niveles (PAR-09), ranking con percentiles P90/P10 y desempate, y el cierre de curso son dominio
nuestro y salen de nuestro propio ledger. No esperan a este contrato.
