---
tags: [tpi, g10, decision, accounting, errores]
fecha: 2026-10-13
estado: aceptada
reemplaza: ""
---

# DEC-015: Un 4xx de Accounting no es una indisponibilidad

## Contexto
`HttpInventoryClient` atrapaba toda `RestClientException` y lanzaba `InventoryUnavailableException`: un `404 ACCOUNT_NOT_FOUND` (alumno sin cuenta) o un `401/403` (token técnico sin scope) terminaban como `503` o `500`, igual que una caída real. El alumno no podía abrir el desafío y el diagnóstico apuntaba al lugar equivocado.

## Decisión
Se clasifica la respuesta de Accounting:
- **`404` con `ACCOUNT_NOT_FOUND`** (en `error` o, por tolerancia, `code`): `404 inventory.account-not-found`. Es un faltante de datos: no se vuelve `no_lives` ni habilita el intento.
- **Otro `4xx` no transitorio** (`401`, `403`, etc.): `502` Problem Details `inventory-request-rejected`; el `error` y el `request_id` de Accounting quedan en el log, no en el mensaje.
- **`408`, `429`, `5xx`, timeout o token no disponible**: `503` indisponibilidad.
- En consultas de recuperación se conserva `recovery_pending` si Accounting rechaza la consulta; en el ranking, un rechazo deja el criterio de vidas perdidas neutro y se recuerda con tipo propio dentro de la ventana de falla.
Se propagan `traceparent` y `X-Request-Id` a Accounting.

## Alternativas descartadas
- **Bloquear con `not_enrolled` ante cuenta ausente** (rama `fix/account-not-found-gate`, `6c0dac5`): usa "el motivo existente más cercano" porque no hay uno para cuenta no aprovisionada; sigue sin mergear.
- **Todo error de Accounting como `503`**: era el estado previo.

## Consecuencias
- Positivas: el diagnóstico distingue falta de cuenta, credenciales mal y caída real.
- Negativas / deuda:
  - Motor define solo `403` y `503`: su tratamiento del `404` y `502` del gate queda por coordinar.
  - Falta un motivo funcional dedicado para "cuenta no aprovisionada".
  - La rama `fix/account-not-found-gate` debería cerrarse o reconciliarse.

## Referencias
- Código / PR / doc: PR #193 (`d48542b`, 2026-10-12), PR #199 (`1a8b0b9`, `9efdcd6`, `cd47297`, 2026-10-13), PR #200 (`85d9b38`, `c9f4d17`), `clients/AccountingErrors`, `InventoryAccountNotFoundException`, `InventoryRequestRejectedException`, `LostLivesRejectedException`.
- `tpi-roadmap/docs/contracts/roadmap-motor-gate-v1.md` §6.2, `docs/contracts/accounting-roadmap-v1.md` §6.
- Relacionadas: [[acuerdos/inventario|Inventario]], [[acuerdos/accounting|Accounting]], [[decisiones/DEC-003-gate-pull-identidad-de-servicio-fail-closed|DEC-003]].
