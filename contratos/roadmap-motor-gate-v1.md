# Acta del contrato del Gate Roadmap ↔ Motor

| Dato | Valor |
|---|---|
| Tarea | T-15.5 — Acta y publicación OpenAPI del contrato; T-44.3 — motivo `group_restricted` (v1.1); T6-HU48 — `challenge_id` y `attempt_type` (v1.2); restricciones `DATE` (v1.3, acta T-10.1 §3.6); T-31.1 — `origin_unavailable` en vez de `503` (v1.4, HT-31) |
| Versión | **1.4 — Sprint 3** (1.3 — Sprint 3; 1.2 — Sprint 3; 1.1 — Sprint 2; 1.0 — Sprint 1) |
| Fecha | 2026-10-16, aprobación de G09 (propuesta: 2026-10-15; v1.3: 2026-10-12; v1.2: 2026-10-11; v1.1: 2026-10-09; v1.0: 2026-09-26) |
| Estado | **v1.4 aprobada por G09 (2026-10-16)**, con el valor `origin_unavailable` en inglés. Entra en `develop` al mergear T-31.1; hasta entonces `develop` responde como la v1.3. Aprobación nominal pendiente |
| Equipos | Roadmap (Tema 10) y Motor de Desafíos |

Este documento es la fuente vigente del contrato funcional del Gate de Roadmap.
La especificación ejecutable se publica también en `/v3/api-docs` y
[`docs/api_doc/swagger.json`](../api_doc/swagger.json).

## Historial de versiones

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-09-26 | Contrato de Sprint 1: cinco motivos, orden de evaluación y degradación ante Accounting. |
| 1.1 | 2026-10-09 | T-44.3 (HU-44): se agrega el motivo `group_restricted` (§4 y §5), un `403` para la unidad cuya sección Courses no encuentra y el `503` cuando Courses no responde (§6). Cambio aditivo: no cambia la ruta, el envelope ni los motivos existentes. |
| 1.2 | 2026-10-11 | T6 (HU-48): el `data` del gate suma `challenge_id` y `attempt_type` (§3). Cambio aditivo: el Motor ignora los campos que no conoce; no cambia la ruta, el envelope, `eligible` ni `reason`. |
| 1.3 | 2026-10-12 | T-10.1 §3.6: se agrega el motivo `date_restricted` (§4 y §5) y el Gate evalúa las condiciones `DATE` de Courses. Cambio aditivo: solo con el flag `ROADMAP_BY_GROUP_ENABLED` encendido; no cambia la ruta, el envelope, `eligible` ni ninguno de los motivos existentes. |
| 1.4 | 2026-10-16 | **Aprobada por G09** (propuesta el 2026-10-15; T-31.1, HU-15 CA5, [[decisiones/DEC-020-gate-origen-no-disponible-en-vez-de-503\|DEC-020]]): si Accounting o Courses no responden sin dato vigente, el Gate responde `200` con `eligible=false` y `reason=origin_unavailable` en lugar del `503` (§6). **No es aditivo**: el Gate deja de devolver `503` por un origen caído. Además se documenta `unit_prerequisite_pending` (§4 y §5), que el Gate ya emitía desde los prerrequisitos entre unidades ([[decisiones/DEC-010-prerrequisitos-por-seccion-v25\|DEC-010]]) y faltaba en el acta. El valor se acordó en inglés (`origin_unavailable`, no `origen_no_disponible`) a pedido de G09, por consistencia con el resto del vocabulario. |

La v1.1 solo cambia el comportamiento con el flag `ROADMAP_BY_GROUP_ENABLED` encendido. Con el flag
apagado (default) el Gate responde exactamente como en la v1.0. La v1.2 es aditiva para todos los
consumidores: agrega dos campos al `data` y no altera la decisión funcional.

## 1. Objetivo y ownership

Motor consulta el Gate antes de crear un intento. Roadmap evalúa únicamente si el alumno puede
iniciar el nodo y no crea intentos ni modifica progreso.

Una respuesta `eligible=true` termina la participación de Roadmap en el inicio. El flujo posterior
es responsabilidad exclusiva de Motor y Accounting:

```text
Motor → ATTEMPT_INIT → Accounting
      → reserva vida/ítems
      → RESERVATION_CREATED o RESERVATION_REJECTED
```

Roadmap no reserva vidas o ítems, no participa de Hold/Commit/Release, no envía equipamiento a
Motor y no interviene en `challenges.reservations` ni `accounting.holds`. Esta acta no define ni
implementa los payloads o el transporte de ese flujo posterior.

## 2. Endpoint e identidad

```http
GET /api/roadmap/courses/{courseId}/students/{studentId}/nodes/{nodeId}/eligibility
```

- `courseId`, `studentId` y `nodeId` son UUID.
- `studentId` es un dato funcional del path; no viaja en `X-User-Id`.
- La llamada es servicio a servicio mediante API Gateway.
- Roadmap confía en la identidad de servicio validada e inyectada por Gateway y no parsea el JWT.
- El `serviceId`, scope y credenciales nominales de Motor siguen pendientes de confirmación; esta
  acta no los inventa.

## 3. Respuesta exitosa

El endpoint conserva el envelope global de Roadmap. Respuesta habilitada:

```json
{
  "data": {
    "eligible": true,
    "reason": null,
    "challenge_id": "3f2504e0-4f89-11d3-9a0c-0305e82c3301",
    "attempt_type": "NORMAL"
  },
  "message": null,
  "success": true,
  "timestamp": "2026-09-26T18:00:00Z"
}
```

Respuesta con bloqueo funcional:

```json
{
  "data": {
    "eligible": false,
    "reason": "no_lives",
    "challenge_id": "3f2504e0-4f89-11d3-9a0c-0305e82c3301",
    "attempt_type": "NORMAL"
  },
  "message": null,
  "success": true,
  "timestamp": "2026-09-26T18:00:00Z"
}
```

Los bloqueos funcionales responden HTTP 200. Cuando `eligible=true`, `reason` siempre es `null`.

### 3.1 Campos `challenge_id` y `attempt_type` (v1.2)

Además de `eligible` y `reason`, y con el mismo casing `snake_case`, el `data` incluye:

| Campo | Tipo | Descripción |
|---|---|---|
| `challenge_id` | UUID o `null` | Desafío del Motor asociado al nodo. Es `null` cuando el nodo no tiene desafío (por ejemplo, `CONTENT` o `UNIT`). |
| `attempt_type` | `NORMAL`, `LIVES` o `LLM` | Tipo de intento derivado de `node.livesPolicy`: `STANDARD → NORMAL`, `RECOVERY → LIVES`, `LLM → LLM`. |

Ambos campos acompañan a `eligible` tanto en las respuestas habilitadas como en los bloqueos funcionales.
Son **aditivos**: un consumidor que no los conozca los ignora y la decisión funcional (`eligible`,
`reason`) no cambia. `challenge_id` y `attempt_type` no reservan vidas ni crean intentos; solo informan
al Motor qué desafío y qué clase de intento corresponde al nodo consultado.

## 4. Vocabulario (v1.1)

`reason` admite exclusivamente:

| Valor | Condición |
|---|---|
| `not_enrolled` | El alumno no tiene matrícula activa en el curso-cohorte. |
| `course_archived` | El curso o roadmap está archivado. |
| `content_not_read` | Falta leer contenido obligatorio de la sección. |
| `prerequisite_pending` | No se cumplen los prerrequisitos AND/OR del nodo. |
| `no_lives` | Un nodo `STANDARD` no tiene vidas libres disponibles. |
| `group_restricted` | **v1.1.** La unidad del nodo está limitada a comisiones a las que el alumno no pertenece. Solo se emite con el flag `ROADMAP_BY_GROUP_ENABLED` encendido. |
| `date_restricted` | **v1.3.** La unidad del nodo tiene una condición `DATE` que no se cumple en el instante de la consulta (acta T-10.1 §3.6). Solo se emite con el flag `ROADMAP_BY_GROUP_ENABLED` encendido. |
| `unit_prerequisite_pending` | **v1.4 (documentación).** Falta completar una unidad requisito de la unidad del nodo (todos sus nodos obligatorios, [[decisiones/DEC-010-prerrequisitos-por-seccion-v25\|DEC-010]]). El Gate ya lo emitía; no estaba en el acta. |
| `origin_unavailable` | **v1.4.** Accounting o Courses no respondieron, o respondieron con un dato inválido, y no hay dato vigente (§6). Reemplaza al `503`. |

El vocabulario sigue siendo cerrado: Roadmap no emite ningún valor fuera de esta tabla. Como la v1.0
lo cerraba en cinco valores, cada ampliación se coordina con el consumidor (§9). El Motor ya reconoce
`date_restricted` como passthrough de texto (§9); la v1.3 lo incorpora al contrato activo.

Los valores históricos `recovery_pending` y `already_passed` quedan retirados del contrato activo.
Roadmap no sustituye ninguno de ellos por otra razón. Haber completado el nodo no agrega un
bloqueo del Gate: Motor es responsable del ciclo de vida de intentos y reintentos.

## 5. Orden y reglas funcionales

Roadmap devuelve el primer bloqueo aplicable en este orden:

1. `course_archived`;
2. `not_enrolled`;
3. `group_restricted` o `date_restricted` (v1.1/v1.3, restricción de la unidad, solo con el flag encendido);
4. `unit_prerequisite_pending` (unidad requisito incompleta);
5. `content_not_read`;
6. `prerequisite_pending`;
7. `no_lives`.

`origin_unavailable` (v1.4) no tiene un lugar fijo: aparece en el paso donde el origen falla.
Matrícula, comisiones y fechas consultan Courses (pasos 2 y 3) y las vidas consultan Accounting
(paso 7), así que un bloqueo funcional anterior a la consulta que falla gana sobre la caída.

La restricción de la unidad se evalúa antes que las condiciones de progreso, para no revelar lecturas
ni prerrequisitos de una unidad a la que el alumno no accede, y después de la matrícula: sin matrícula
activa la respuesta es `not_enrolled` y no se consultan comisiones ni fechas.

Regla de `group_restricted` y `date_restricted` (HU-44, T-44.3; T-10.1 §3.6):

- Se consideran **todas** las comisiones del alumno, no la que tenga elegida en el frontend: el
  Motor no envía comisión.
- Una unidad sin condiciones en su sección de Courses, o sin sección asociada, es general
  y no bloquea. Una cohorte sin comisiones se comporta como en la v1.0.
- La restricción de la **sección** se evalúa primero y la de la **actividad/nodo** después (acta
  T-10.1 §3.6). El nodo se mapea a `courseActivityId` por su `content_id`; un nodo sin actividad
  vinculada no suma una segunda restricción.
- Una unidad o actividad con condiciones `GROUP` exige pertenecer a alguna de esas comisiones; con
  operador `ALL`, a todas (acta T-10.1 §4). La regla es la de `GroupVisibilityRules`, la misma de la
  vista por comisión.
- Las condiciones `GROUP` y `DATE` se combinan con el **mismo operador** `ALL`/`ANY` de la unidad
  (acta T-10.1 §4): `ALL` exige cumplirlas todas y `ANY` alcanza con una.
- Una condición `DATE` se cumple con **apertura inclusiva y cierre exclusivo**, en la zona
  configurada (`app.clients.course-restrictions.date-zone`, default `America/Argentina/Buenos_Aires`,
  acta T-10.1 §3.6); un extremo ausente es abierto. Una fecha-hora **sin offset** se asume en esa
  zona. Un **cierre con fecha sola** abarca ese día completo: el fin exclusivo se corre al día
  siguiente. Una ventana **vacía o invertida** (`from >= until`) se informa como indisponibilidad
  (`503` hasta la v1.3; `origin_unavailable` desde la v1.4), nunca como un bloqueo permanente.
- La restricción `DATE` aplica también a la **lectura** de un nodo de contenido: un contenido fuera
  de su ventana no se puede leer antes de tiempo (mismo `date_restricted`).
- Cuando la unidad queda bloqueada, un incumplimiento `DATE` informa `date_restricted`; si ninguna
  condición `DATE` falla, informa `group_restricted`. Las condiciones `SECTION_COMPLETED` siguen sin
  evaluarse en el Gate.

La evaluación de prerrequisitos reutiliza `PrerequisiteService`; el controller no implementa
AND/OR. La lectura obligatoria reutiliza `SectionReadingProgressService`.

Para vidas, Roadmap consulta `InventoryClient` y trabaja con:

```text
freeLives = currentLives - reservedLives
```

- `STANDARD` con `freeLives <= 0`: `eligible=false`, `reason=no_lives`.
- `RECOVERY` no consulta vidas y no se bloquea solamente por falta de ellas.
- La elegibilidad no reserva ni consume vidas.

## 6. Degradación y errores reales

> [!info] v1.4 aprobada por G09 (2026-10-16)
> Hasta la v1.3, un origen caído respondía `503` Problem Details. La v1.4 lo reemplaza por un
> bloqueo con motivo. El código está en `feature/t-31-1-gate-origen-no-disponible`; mientras no se
> mergee, `develop` sigue respondiendo `503`.

Si Accounting o Courses fallan (o responden con un dato inválido) y no existe caché vigente, el
Gate responde un bloqueo:

```json
{
  "data": {
    "eligible": false,
    "reason": "origin_unavailable",
    "challenge_id": "3f2504e0-4f89-11d3-9a0c-0305e82c3301",
    "attempt_type": "NORMAL"
  },
  "message": null,
  "success": true,
  "timestamp": "2026-10-15T18:00:00Z"
}
```

Sigue siendo **fail-closed** ([[decisiones/DEC-003-gate-pull-identidad-de-servicio-fail-closed|DEC-003]]).
La indisponibilidad:

- no se convierte en `no_lives`, `not_enrolled` ni `group_restricted`;
- no devuelve `eligible=true`;
- no utiliza caché vencida para decidir el Gate.

Un nodo `RECOVERY` no consulta vidas: la caída de Accounting no lo bloquea.

También se conservan 401 para falta de identidad, 403 para principal o nodo no autorizado y 404
cuando el nodo no existe en el curso.

### 6.2 Cuenta ausente en Accounting (faltante de datos, no indisponibilidad)

Un `404` de Accounting en las consultas de vidas (`equip-summary`) significa que no existe la
cuenta del alumno en esa cohorte, no que el servicio de vidas esté caído. Roadmap lo informa como:

```http
HTTP/1.1 404 Not Found
Content-Type: application/problem+json
```

con código `inventory.account-not-found` y los IDs consultados (`courseId`, `studentId`) en el
`detail`. La cuenta ausente:

- no se convierte en `no_lives` (no se asume una disponibilidad);
- no devuelve `eligible=true` ni habilita la apertura;
- no usa caché: la cuenta debe crearse por el flujo previsto (inscripción/alta) antes de evaluar
  vidas.

Cualquier otra falla HTTP o de transporte sigue siendo la indisponibilidad de §6 (`503` hasta la v1.3, `origin_unavailable` desde la v1.4); un rechazo `4xx` de Accounting es un `502` ([[decisiones/DEC-015-4xx-de-accounting-no-es-indisponibilidad|DEC-015]]). El
consumidor (Motor) todavía define solo 403 y 503; su tratamiento de este `404` queda pendiente de
coordinación, igual que el resto de los pendientes de §9.

### 6.1 Comisiones (v1.1, solo con el flag encendido)

Para decidir `group_restricted`, Roadmap consulta a Courses la restricción de la sección del nodo
y la de su actividad (`content_id`, §3.4.1) y, solo si alguna de las dos tiene comisiones, las
comisiones del alumno. No consulta el resto del roadmap.

| Situación | Respuesta | Tipo |
|---|---|---|
| La unidad o la actividad es de comisiones a las que el alumno no pertenece | `200`, `eligible=false`, `reason=group_restricted` | Bloqueo funcional |
| La unidad tiene una sección asociada (o el nodo una actividad) que Courses no encuentra (inexistente o inactiva) | `403` Problem Details, código `node.unit-unresolved`, sin `reason` | Bloqueo funcional |
| Courses no responde las restricciones o las comisiones | `200`, `eligible=false`, `reason=origin_unavailable` (v1.4; `503` hasta la v1.3) | Indisponibilidad |

- El `403` de la unidad o actividad no resuelta no agrega un motivo al vocabulario: no se sabe si
  estaba restringida, así que no se informa `group_restricted` ni se concede acceso. Es el mismo
  tratamiento que el nodo no disponible.
- La caída de Courses sigue las mismas reglas que la de Accounting: no se convierte en
  `group_restricted`, no devuelve `eligible=true` y no usa datos viejos para decidir. Lo mismo para
  la matrícula: si el fallback contra Courses no responde, no se informa `not_enrolled`.
- No hay caché: cada evaluación de una unidad con sección asociada hace una llamada a Courses por su
  restricción y, si el nodo tiene `content_id`, otra por su actividad; una restricción con comisiones
  suma la lectura paginada de participantes de la cohorte.

## 7. Idempotencia y efectos

Repetir el GET con el mismo estado produce la misma decisión. La operación no escribe matrícula,
lecturas, nodos completados, desbloqueos ni movimientos de XP, y no crea intentos o reservas.

## 8. Contratos reemplazados

La v1.4 **no es aditiva**: reemplaza el `503` de §6 por el bloqueo
`origin_unavailable` y suma ese valor al vocabulario. No cambia la ruta, el envelope, el orden de
los motivos existentes ni los demás errores (`401`, `403`, `404`, `502`). También documenta
`unit_prerequisite_pending`, que el Gate ya emitía.

La v1.3 es **aditiva** sobre la v1.2: agrega `date_restricted` al vocabulario de §4 (pasa de seis a
siete valores) y activa la evaluación de las condiciones `DATE` de Courses. No retira ni reemplaza
ningún motivo, no cambia el orden existente y, con el flag `ROADMAP_BY_GROUP_ENABLED` apagado (default),
no cambia el comportamiento respecto de la v1.0.

La v1.1 reemplaza a la v1.0 en un solo punto: el vocabulario de §4 pasa de cinco a seis valores.

La v1.0 reemplazó, para Sprint 1, toda referencia anterior que:

- incluya `recovery_pending` o `already_passed` como razones activas;
- publique la respuesta sin el envelope global `data`;
- represente una caída de Accounting como un bloqueo funcional;
- afirme que Roadmap reserva o envía vidas o ítems para iniciar el intento.

El path no incorpora `/v1` ni `/v3`: la versión se registra en esta acta y en la especificación
OpenAPI, sin cambiar la ruta funcional acordada.

## 9. Aprobación

### Compatibilidad de la v1.1 con el consumidor

Verificado en el código de G09 (`tpi-engine-challenge`, rama `develop`, commit `3ee47b4`,
2026-10-09; cambio de su PR #127, pedido en `tpi-engine-challenge#124`):

- `RoadmapIneligibilityReason` incluye `GROUP_RESTRICTED("group_restricted")`.
- `RoadmapEligibilityResponse` conserva `reason` como texto: un motivo que no esté en su enum no
  rompe la lectura ni se pierde.
- Con `eligible=false`, el Motor rechaza el intento con `403` y reenvía el `reason` recibido.
- Un `403` de Roadmap se trata como alumno no elegible, sin motivo; un `503`, como Roadmap no
  disponible, y no se crea el intento.

Para la v1.3, el mismo enum del Motor ya incorpora `date_restricted` (`RoadmapIneligibilityReason`,
commits `3ee47b4`/`d07cdbb` de `tpi-engine-challenge`, `develop`, verificados en
[`motor-desafios-evento-cierre.md`](motor-desafios-evento-cierre.md) §"Motivos del gate"), y su
passthrough de texto lo trata como cualquier otro motivo: `403` con el `reason` recibido.

### Compatibilidad de la v1.4 con el consumidor (aprobada por G09, 2026-10-16)

Con `eligible=false`, el Motor ya rechaza el intento con `403 student-not-eligible` y reenvía el
`reason` como texto, así que `origin_unavailable` llega al alumno sin cambiar su lógica.

G09 respondió en su issue el 2026-10-16:

- **Aprueba** que, ante una dependencia de Roadmap caída o con respuesta inválida y sin caché
  vigente, el Gate responda `200` con `eligible=false` (fail-closed) en lugar de `503`, y que el
  Motor y su front devuelvan `403 student-not-eligible` con el `reason`.
- **Pidió** el valor en inglés, `origin_unavailable`, por consistencia con el resto del vocabulario
  y con el enum `GateReason.ORIGIN_UNAVAILABLE`. Roadmap lo cambió (la propuesta decía
  `origen_no_disponible`).
- **Va a cambiar de su lado**, cuando confirmemos el nombre:
  - `roadmap-eligibility.yaml`: suma `unit_prerequisite_pending` y `origin_unavailable` al enum de
    `reason`, y aclara que el `503` ya no aplica a dependencias de Roadmap caídas;
  - `RoadmapIneligibilityReason`: suma `UNIT_PREREQUISITE_PENDING` y `ORIGIN_UNAVAILABLE`;
  - `RoadmapEligibilityResponse`: `@JsonIgnoreProperties(ignoreUnknown = true)`, para tolerar
    `challenge_id` y `attempt_type` y cualquier campo nuevo de `data`.

Pendiente de coordinar con G09: su contrato `docs/contracts/roadmap-eligibility.yaml` ya lista los
siete valores de la v1.3 (verificado en `tpi-engine-challenge`, `develop`, `e95adac6`, 2026-10-15;
antes listaba los cinco de la v1.0, seguimiento `2026-P4-BE/tpi-engine-challenge#234`), pero le
faltan `unit_prerequisite_pending` y `origin_unavailable`, y todavía documenta el `503` por
dependencia caída. También falta su conformidad explícita con el `403` de la unidad no resuelta.

Las decisiones funcionales están registradas, pero el repositorio no contiene evidencia nominal
verificable de aprobación Roadmap ↔ Motor. La firma debe completarse antes de considerar el acta
formalmente aprobada; no se infieren responsables.

| Equipo | Responsable | Fecha | Aprobación |
|---|---|---|---|
| Roadmap (Tema 10) | Pendiente de registrar | Pendiente | Pendiente |
| Motor de Desafíos | Pendiente de registrar | Pendiente | Pendiente |
