# Acta del contrato Roadmap ↔ Accounting

| Dato | Valor |
|---|---|
| Tarea | T-03.1 — Acta del contrato de vidas e ítems con Inventario/Accounting |
| Versión | 1.0 |
| Fecha | 2026-09-26 |
| Estado | **Acordado funcionalmente; firma nominal pendiente** |
| Equipos | Roadmap (Tema 10) y Accounting (Tema 08) |

Este documento es la fuente vigente del contrato funcional entre Roadmap y Accounting. La
implementación del cliente HTTP, la caché y su configuración corresponde a T-03.2 y queda fuera
del alcance de esta acta.

## 1. Objetivo y decisiones transversales

El contrato permite a Roadmap:

- consultar disponibilidad de vidas para el Gate;
- obtener históricos de vidas y monedas necesarios para ranking y desempate;
- mostrar en una llamada las vidas, el saldo y todos los ítems de un estudiante;
- recibir transiciones de disponibilidad de vidas;
- solicitar el equipamiento de ítems y correlacionar la respuesta de Accounting.

Decisiones cerradas:

- `app.api.private-path` de Accounting vale `/api/accounting`.
- Todas las llamadas síncronas Roadmap → Accounting pasan por API Gateway.
- `courseId` y `studentId` son UUID en paths y payloads.
- Los ejemplos anteriores como `crs-14` y `stu-8821` eran solamente ilustrativos y no definen
  el tipo del contrato.
- En T-03.1, “ítems por lote” significa obtener todos los ítems de **un estudiante** en una sola
  llamada mediante `equip-summary`. No se requiere un batch de inventarios de varios estudiantes.
- Esta acta no define scopes, credenciales ni nombres de clientes técnicos.

## 2. Ownership

Accounting es la fuente de verdad de vidas, saldo e inventario. Aplica el techo de vidas en las
operaciones que correspondan y administra el cambio de estado de los ítems.

Roadmap:

- conserva el Gate de habilitación;
- calcula vidas libres a partir de la respuesta de Accounting;
- consulta y muestra el inventario;
- maneja la selección del alumno y solicita el equipamiento de ítems;
- usa la información histórica acordada para ranking y desempate.

> **Decisión de ownership:** Roadmap **no envía vidas ni ítems a Motor para iniciar un
> desafío**. Esa responsabilidad corresponde a Accounting. Motor no debe depender de un
> “contexto de inicio” de Roadmap que contenga esos datos.

## 3. Contrato HTTP

Todos los endpoints de esta sección utilizan el prefijo privado `/api/accounting` y se consumen
por API Gateway.

### 3.1 Disponibilidad liviana de vidas para el Gate

```http
GET /api/accounting/courses/{courseId}/accounts/{studentId}/lives-availability
```

```json
{
  "currentLives": 2,
  "reservedLives": 1
}
```

Roadmap calcula:

```text
freeLives = currentLives - reservedLives
```

Este es el endpoint que debe utilizar el Gate. Un desafío sujeto a vidas puede continuar por
esta validación solamente cuando `freeLives > 0`. Si `freeLives = 0`, aplica el bloqueo funcional
`no_lives` conforme a las reglas del Gate. Las excepciones de dominio ya acordadas, como las
políticas de recuperación, no se redefinen en esta acta.

### 3.2 Monedas ganadas históricamente por estudiante

```http
GET /api/accounting/courses/{courseId}/accounts/{studentId}/coins-earned
```

```json
{
  "totalCoinsEarned": 1250.00
}
```

`totalCoinsEarned` tiene tipo conceptual `BigDecimal`.

### 3.3 Progreso histórico de vidas por estudiante

```http
GET /api/accounting/courses/{courseId}/accounts/{studentId}/lives-progress
```

```json
{
  "totalLivesEarned": 8,
  "currentLives": 2,
  "totalLivesLost": 1,
  "neverLostALife": false
}
```

### 3.4 Lote de progreso de vidas y monedas por curso

```http
GET /api/accounting/courses/{courseId}/accounts/progress-batch
```

```json
{
  "students": [
    {
      "studentId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "totalCoinsEarned": 1250.00,
      "totalLivesEarned": 8,
      "neverLostALife": false
    },
    {
      "studentId": "8b1e2c4a-1234-4a1b-9c3d-abcdef123456",
      "totalCoinsEarned": 900.00,
      "totalLivesEarned": 5,
      "neverLostALife": true
    }
  ]
}
```

### 3.5 Lote de vidas para desempate del ranking

```http
GET /api/accounting/courses/{courseId}/accounts
```

```json
[
  {
    "studentId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "totalLivesLost": 2,
    "neverLostALife": false
  },
  {
    "studentId": "8b1e2c4a-1234-4a1b-9c3d-abcdef123456",
    "totalLivesLost": 0,
    "neverLostALife": true
  }
]
```

Este lote evita N consultas individuales y alimenta los datos económicos/históricos que
Roadmap necesita para ranking y desempate.

### 3.6 Detalle público de un estudiante

```http
GET /api/accounting/courses/{courseId}/accounts/{studentId}/public-detail
```

```json
{
  "totalBalance": 850.00,
  "currentLives": 2,
  "totalLivesLost": 1,
  "neverLostALife": false
}
```

Este endpoint expone el detalle permitido de otro estudiante dentro del ranking. No autoriza a
Roadmap a exponer datos personales.

### 3.7 Resumen de vidas, saldo e inventario

```http
GET /api/accounting/courses/{courseId}/accounts/{studentId}/equip-summary
```

```json
{
  "currentLives": 3,
  "reservedLives": 1,
  "availableBalance": 850.00,
  "items": [
    {
      "itemInstanceId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "catalogItemId": "SHIELD-001",
      "itemName": "Escudo x2",
      "itemType": "SHIELD",
      "itemEffect": "LIFE_PROTECTION",
      "applicableChallengeScope": "ALL",
      "status": "EQUIPPED",
      "maxCharges": 2,
      "remainingUses": 2
    },
    {
      "itemInstanceId": "8b1e2c4a-1234-4a1b-9c3d-abcdef123456",
      "catalogItemId": "BOOST-007",
      "itemName": "Doble puntos",
      "itemType": "BOOST",
      "itemEffect": "SCORE_MULTIPLIER",
      "applicableChallengeScope": "PRACTICAL_ONLY",
      "status": "CONSUMED",
      "maxCharges": 1,
      "remainingUses": 0
    }
  ]
}
```

La colección `items` representa el listado completo de ítems del estudiante para ese curso en
una sola llamada. El vocabulario vigente mostrado por este contrato incluye `SHIELD`, `BOOST`,
`LIFE_PROTECTION`, `SCORE_MULTIPLIER`, `ALL`, `PRACTICAL_ONLY`, `EQUIPPED` y `CONSUMED`.

## 4. Eventos de vidas

Ambos eventos son publicados por Accounting en `accounting.ledger.events` y usan el envelope:

```json
{
  "event_id": "...",
  "event_type": "...",
  "timestamp": "ISO-8601 UTC",
  "producer": "...",
  "payload": {}
}
```

### 4.1 `LIVES_EXHAUSTED`

Representa la transición `freeLives > 0` → `freeLives = 0`.

```json
{
  "event_id": "123e4567-e89b-12d3-a456-426614174000",
  "event_type": "LIVES_EXHAUSTED",
  "timestamp": "2026-09-25T18:00:00Z",
  "producer": "tema-08-accounting",
  "payload": {
    "course_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "student_id": "8b1e2c4a-1234-4a1b-9c3d-abcdef123456",
    "current_lives": 0,
    "reserved_lives": 0
  }
}
```

### 4.2 `LIVES_AVAILABLE`

Representa la transición `freeLives = 0` → `freeLives > 0`.

```json
{
  "event_id": "123e4567-e89b-12d3-a456-426614174001",
  "event_type": "LIVES_AVAILABLE",
  "timestamp": "2026-09-25T18:10:00Z",
  "producer": "tema-08-accounting",
  "payload": {
    "course_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "student_id": "8b1e2c4a-1234-4a1b-9c3d-abcdef123456",
    "current_lives": 1,
    "reserved_lives": 0
  }
}
```

### 4.3 Movimientos de vidas en `accounting.events` (proyección `recovery_pending`)

Además del ledger de transiciones, Accounting publica los movimientos de vidas
`LIFE_CREDITED` (acredita) y `LIFE_DEBITED` (descuenta) en el topic
`accounting.events`, con el sobre estándar del bus en snake_case
(`event_id`, `event_type`, `event_version: 1`). Roadmap los consume en
`AccountingEventsListener` para proyectar un booleano local,
`student_course.recovery_pending`, que solo indica "el alumno no tiene vidas
libres" al momento del último movimiento.

```json
{
  "studentId": "8b1e2c4a-1234-4a1b-9c3d-abcdef123456",
  "courseId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "currentLives": 0,
  "movementType": "DEBIT",
  "livesAwarded": 1,
  "sourceReferenceId": "11111111-1111-1111-1111-111111111111"
}
```

- La proyección es **absoluta** e idempotente: ante cada movimiento, Roadmap
  relee `StudentLives` (`InventoryClient.fetchLives`) y escribe
  `recovery_pending = !lives.hasLives()`; no depende del orden de los eventos.
- Es **informativa**: **no** alimenta la decisión del Gate ni la elegibilidad,
  que siguen consultando `lives-availability`/`equip-summary` en el momento del
  pedido. Un `recovery_pending = true` no bloquea por sí solo.
- Si Accounting no responde (o no conoce la cuenta), Roadmap conserva el valor
  previo y registra un WARN; el evento se confirma igual (no va a la DLT).
- **Deuda de contrato (escalación):** el payload real que emite Accounting hoy
  está en camelCase, mientras el sobre y el resto del bus ya son snake_case.
  Roadmap lo lee con `@JsonProperty` camelCase más `@JsonAlias` snake_case como
  puente hasta que Accounting migre el payload (issue
  [tpi-accounting#227](https://github.com/2026-P4-BE/tpi-accounting/issues/227)).


## 5. Flujo de equipamiento

Antes de iniciar un desafío, Roadmap puede consultar `equip-summary` para mostrar al alumno sus
vidas e inventario. Roadmap maneja su selección, pero Accounting administra el estado.

Equipar o desequipar es la transición reversible `AVAILABLE` ⇄ `EQUIPPED`, siempre que el ítem no
esté reservado. Equipar:

- no genera un asiento de ledger;
- no consume el ítem;
- no lo reserva para un intento;
- cambia su estado de inventario en Accounting.

### 5.1 `ITEM_EQUIP_REQUESTED`

Roadmap publica en `accounting.inventory.commands`:

```json
{
  "event_id": "123e4567-e89b-12d3-a456-426614174010",
  "event_type": "ITEM_EQUIP_REQUESTED",
  "timestamp": "2026-09-19T23:00:00Z",
  "producer": "tema-10-roadmap",
  "payload": {
    "student_id": "8b1e2c4a-1234-4a1b-9c3d-abcdef123456",
    "course_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "item_instance_ids": [
      "11111111-1111-1111-1111-111111111111",
      "22222222-2222-2222-2222-222222222222"
    ]
  }
}
```

La solicitud requiere una respuesta de Accounting.

### 5.2 `ITEM_EQUIP_RESULT`

Accounting publica en `accounting.inventory.commands`:

```json
{
  "event_id": "123e4567-e89b-12d3-a456-426614174011",
  "event_type": "ITEM_EQUIP_RESULT",
  "timestamp": "2026-09-19T23:00:01Z",
  "producer": "tema-08-accounting",
  "payload": {
    "correlation_id": "123e4567-e89b-12d3-a456-426614174010",
    "student_id": "8b1e2c4a-1234-4a1b-9c3d-abcdef123456",
    "course_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "equipped": [
      "11111111-1111-1111-1111-111111111111"
    ],
    "rejected": [
      {
        "item_instance_id": "22222222-2222-2222-2222-222222222222",
        "reason": "ITEM_NOT_AVAILABLE"
      }
    ]
  }
}
```

`correlationId` referencia el `event_id` de `ITEM_EQUIP_REQUESTED`.

## 6. Política de degradación

### 6.1 Vidas utilizadas por el Gate

Ante una respuesta correcta, Roadmap usa `currentLives`, `reservedLives` y calcula `freeLives`.
Ante timeout, HTTP 5xx, 503 del Gateway o indisponibilidad equivalente:

- si existe caché **vigente**, puede utilizarla;
- sin caché vigente, la dependencia se considera no disponible;
- no se utiliza caché vencida para decidir el Gate;
- no se asume `currentLives = 0` ni se transforma la falla en `no_lives`;
- no se devuelve `eligible = true` por defecto;
- el Gate degrada explícitamente, previsiblemente mediante HTTP 503 y Problem Details.

El TTL debe ser corto y configurable. Esta acta no fija un valor numérico: T-03.2 debe
definirlo y configurarlo sin convertirlo en una constante de dominio.

### 6.2 Inventario para visualización

Ante una falla de Accounting, la lectura visual del inventario puede mostrar el último dato
conocido, indicando expresamente que está desactualizado. La falla no bloquea la lectura de la
pantalla. Esta política no se aplica a la decisión de vidas del Gate.

## 7. Techo de vidas

El techo no se obtiene de los endpoints de Accounting de esta acta. La fuente del parámetro es
Backoffice/PAR-12 (`initialLives`, `maxLives`), según
[`backoffice-par.md`](backoffice-par.md). Accounting/Inventario aplica ese techo en las
operaciones correspondientes. Roadmap no debe inventar un endpoint de Accounting para obtenerlo.

## 8. Contratos reemplazados

Desde la versión 1.0 quedan **obsoletos y reemplazados**:

- `GET /api/bank/courses/{courseId}/students/{studentId}/lives`;
- las propuestas `GET /api/wallet/inventory/lives` y `POST /api/wallet/inventory/lives/batch`;
- los nombres de evento `EXHAUSTED-LIVES` y `VIDAS-AGOTADAS`;
- las afirmaciones de que Roadmap envía vidas o el ítem activo a Motor al iniciar;
- los enums anteriores `BOOST_XP`, `ABSORB_FAILURE`, `XP_MULTIPLIER` y `NO_EXAMS`.

Las referencias históricas pueden conservarse si están marcadas como obsoletas y enlazan a esta
acta. No son una fuente vigente para T-03.2, T-15.2 ni el flujo de equipamiento.

### 8.1 Brecha conocida en la implementación actual

El endpoint heredado de inicio de Roadmap todavía devuelve un DTO `ChallengeStart` que incluye
vidas y XP. Esta forma no modifica el ownership acordado y no debe usarse para integrar Roadmap
con Motor. Su retiro o adaptación corresponde a una tarea de implementación posterior; T-03.1 no
modifica código productivo.

## 9. Límites de esta acta

Esta tarea no implementa:

- el cliente HTTP, adaptadores ni DTOs Java;
- caché, TTL numérico, timeouts o reintentos;
- controllers;
- listeners o publicadores de eventos;
- scopes, credenciales ni adquisición del token técnico;
- el flujo funcional de HU-35.

Esos puntos deben respetar este contrato cuando se implementen en sus tareas correspondientes.

> **Seguimiento técnico (fuera del acta, P-11):** para llamar a Accounting por
> Gateway, Roadmap pide token con `audience: accounting-service` (serviceId del
> micro). Los scopes los define el dueño del recurso y se dan de alta en el
> catálogo `ScopeCatalog` de Users antes de usarse: `course.enrollment.read` y
> `accounting.account.read` existen como `offers`; `vidas.read` e
> `inventario.read` son propuesta nuestra pendiente de confirmación por
> Accounting. Secret por Vault, nunca por chat
> (`docs/T-01-7-EUREKA-GATEWAY.md`).

## 10. Aprobación

El contrato funcional fue acordado entre los equipos. No hay evidencia versionada de nombres o
firmas, por lo que la aprobación nominal permanece pendiente y debe completarse sin inventar
responsables.

| Equipo | Responsable | Fecha | Aprobación |
|---|---|---|---|
| Roadmap (Tema 10) | Pendiente de registrar | Pendiente | Pendiente |
| Accounting (Tema 08) | Pendiente de registrar | Pendiente | Pendiente |
