---
tags: [tpi, g10, acuerdo, accounting, tema-08, kafka]
fecha: 2026-09-26
grupos: [G10, Gxx]  # Accounting = Tema 08; número de grupo no aparece en los docs (verificar)
estado: vigente  # acordado funcionalmente; firma nominal pendiente
contrato: "contratos/accounting-roadmap-v1.md"
---

# Acuerdo con Accounting (Tema 08, Gxx verificar): vidas, ledger y eventos

> [!info] Fuentes
> - `contratos/accounting-roadmap-v1.md`: acta v1.0, fuente vigente del contrato funcional.
> - `contratos/Contrato de Integración_ Accounting (Tema 08).pdf`: PDF de Accounting.
> - `tareas/T-03-2-ACCOUNTING-CLIENT.md`, `tareas/T-15-2-ACCOUNTING-GATE-LEDGER.md`, `tareas/T-25-2-FUENTE-VIDAS-PERDIDAS.md`, `tareas/T-35-1-ENDPOINT-INVENTARIO.md`.
> - Repos de la contraparte: `2026-P4-BE/tpi-accounting` (issue #227).
> - Nota hermana, centrada en el consumo de vidas e ítems: [[acuerdos/inventario|Inventario]].

> [!question] Verificar
> En los docs, "Inventario" y "Accounting" son el mismo servicio (`InventoryClient` llama a `/api/accounting/...`). Se separan en dos notas por pedido, pero conviene confirmar si el equipo que da Inventario es el mismo que Accounting y qué número de grupo tienen.

## Qué se acordó
- **Accounting es la fuente de verdad** de vidas, saldo e inventario; aplica el techo de vidas y administra el estado de los ítems.
- **Roadmap no envía vidas ni ítems a Motor** para iniciar un desafío. El `ChallengeStart` heredado (con vidas y XP) es una brecha conocida, no se usa para integrar.
- Roadmap conserva el **Gate**, calcula `freeLives = currentLives - reservedLives`, muestra el inventario y solicita el equipamiento (`ITEM_EQUIP_REQUESTED`).
- Todo REST pasa **por Gateway**; `app.api.private-path` de Accounting = `/api/accounting`; `courseId`/`studentId` son UUID.
- **Degradación:** sin caché vigente, una falla de Accounting es indisponibilidad (`503`; en la v1.4 del acta del gate (aprobada por G09; entra con T-31.1) pasa a `200` con `reason=origin_unavailable`, [[decisiones/DEC-020-gate-origen-no-disponible-en-vez-de-503|DEC-020]]); nunca `no_lives` ni `eligible=true`; nunca caché vencida para decidir el Gate. Para **visualización** de inventario sí se puede mostrar el último dato conocido marcado como desactualizado.
- El **techo de vidas** viene de Backoffice (PAR-12 `initialLives`/`maxLives`), no de Accounting. Ver [[acuerdos/backoffice|Backoffice]].
- Contratos **reemplazados** por el acta v1.0: `GET /api/bank/courses/{courseId}/students/{studentId}/lives`; `GET /api/wallet/inventory/lives` y `POST .../lives/batch`; eventos `EXHAUSTED-LIVES`/`VIDAS-AGOTADAS`; enums `BOOST_XP`, `ABSORB_FAILURE`, `XP_MULTIPLIER`, `NO_EXAMS`.

## Quién lo acordó
- G10: equipo Roadmap (Tema 10).
- Otro grupo: equipo Accounting (Tema 08), número de grupo: Gxx (verificar). Inventario es el mismo equipo (G10, 2026-10-15).
- Aprobación nominal: **pendiente**. El acta aclara que no hay evidencia versionada de nombres o firmas y que no se inventan responsables.

## Contrato técnico

### Auth
- Token técnico por Gateway: `POST /api/users/public/auth/token` (`client_credentials`), **audience `accounting-service`**, **scope `accounting.account.read`** (defaults en `application.properties`; confirmados, T-40.1).
- Los scopes `vidas.read` e `inventario.read` fueron una propuesta nuestra y **no se usan**.
- Headers de correlación `traceparent` y `X-Request-Id` se propagan a Accounting (`CorrelationPropagationInterceptor`, `b16f026`).
- Secretos por Vault, nunca en repo ni chat.

### HTTP (Roadmap → Accounting), prefijo `/api/accounting`
| Método y ruta | Estado en Roadmap |
|---|---|
| `GET /courses/{courseId}/accounts/{studentId}/equip-summary` | **En uso.** Vidas (`currentLives`, `reservedLives`), saldo e ítems. Lo usan el Gate (HU-16, `0ff6fe5`, 2026-10-10) y la pantalla de inventario (HU-35) |
| `GET /courses/{courseId}/accounts` | **En uso** para el desempate del ranking por vidas perdidas (`totalLivesLost`, T-25.2). Una llamada por curso, caché 30 s |
| `GET /courses/{courseId}/accounts/{studentId}/lives-availability` | Acordado en §3.1, **ruta reservada**: Accounting no la implementó; el Gate usa `equip-summary`. Queda configurada, sin dependencia activa |
| `GET .../coins-earned`, `.../lives-progress`, `.../progress-batch`, `.../public-detail` | Acordados (§3.2 a §3.6); sin cliente en el código de `origin/develop` |

### Kafka
| Topic | `event_type` | Dirección | Estado |
|---|---|---|---|
| `accounting.events` | `LIFE_CREDITED`, `LIFE_DEBITED` | Accounting → Roadmap | **Consumido** (`AccountingEventsListener`). Proyecta `student_course.recovery_pending = !hasLives()` releyendo vidas; informativo, no alimenta el Gate |
| `accounting.ledger.events` | `LIVES_EXHAUSTED`, `LIVES_AVAILABLE` | Accounting → Roadmap | Acordado en el acta §4; **sin consumidor en el código** (verificar) |
| `accounting.inventory.commands` | `ITEM_EQUIP_REQUESTED` / `ITEM_EQUIP_RESULT` | Roadmap ↔ Accounting | Acordado en el acta §5; **sin productor ni consumidor en el código**. `bus-notificaciones.md` lo ubica en `accounting.holds.events` (**discrepancia**) |

Equipar/desequipar es la transición reversible `AVAILABLE ⇄ EQUIPPED`; no genera asiento de ledger, no consume ni reserva.

> [!warning] Deuda de contrato (escalada)
> El payload de `LIFE_*` que emite Accounting está en **camelCase** mientras el sobre es snake_case v8. Roadmap lo lee con `@JsonProperty` camelCase + `@JsonAlias` snake_case como puente hasta que Accounting migre (`tpi-accounting#227`). Es la única excepción al [[decisiones/DEC-001-wire-kafka-v8-snake-case|wire v8 sin alias]].

### Formato HTTP
- `equip-summary` y `/accounts` llegan en camelCase en el acta; la lectura tolera snake_case (`a36868b`, `9041bae`, 2026-10-06/11). Vocabulario abierto: `itemType`, `itemEffect`, `applicableChallengeScope` y `status` viajan como texto.
- Errores de Accounting: `ErrorApi` con `error`, `message`, `path`, `request_id` (leídos en `AccountingErrors`).

### Tratamiento de errores (Roadmap)
| Respuesta de Accounting | Qué hace Roadmap |
|---|---|
| `404` con `error` o `code` = `ACCOUNT_NOT_FOUND` | `404 inventory.account-not-found` (faltante de datos, no caída) |
| `401`, `403`, otro `4xx` no transitorio | `502` Problem Details `inventory-request-rejected` (Gate e inventario); en ranking, criterio neutro |
| `408`, `429`, `5xx`, timeout, token no disponible | `503` indisponibilidad |
| Vidas perdidas no disponibles (ranking) | `lost_lives: null`, nunca `0`; un faltante en un grupo empatado apaga el criterio para ese grupo |

Ver [[decisiones/DEC-015-4xx-de-accounting-no-es-indisponibilidad|DEC-015]].

## Impacto en nuestro código
- `clients/inventory/*`: `InventoryClient`, `HttpInventoryClient`, `InventoryConfig`, `InventoryProperties` (TTL 30 s, `last-known-retention` 24 h), `StudentLives`, `EquipSummary`, `InventoryItem`, excepciones `InventoryUnavailableException`, `InventoryAccountNotFoundException`, `InventoryRequestRejectedException`.
- `clients/accounting/*`: `HttpLostLivesClient` (ranking), `LostLivesRejectedException`.
- `clients/AccountingErrors`, `clients/auth/HttpTechnicalTokenProvider`.
- `events/lives/AccountingEventsListener`, `LifeMovementPayload`, `services/RecoveryPendingService`; migración `V24`.
- `services/GateEvaluator`, `services/InventoryService`, `services/RankingService` (desempate `LOST_LIVES`).

## Pendiente / próximos pasos
- [ ] Firma nominal del acta v1.0 (ambos equipos).
- [ ] Accounting debe migrar el payload de `LIFE_*` a snake_case (`tpi-accounting#227`).
- [ ] **E8 (2026-10-15): sí, se consumen** `LIVES_EXHAUSTED`/`LIVES_AVAILABLE` (para `LIFE_RECOVERED`, HU-21). Queda decidir y se implementa `ITEM_EQUIP_*`, o se retiran del acta. Alinear el topic con `bus-notificaciones.md`.
- [ ] Verificar contra el **Accounting real** la fuente de vidas perdidas (T-25.2 "falta verificarla").
- [ ] Gate: falta el motivo `origin_unavailable` y el "último dato 24 h + stale" en el Gate (auditoría Sprint 3, HU-15/16).
- [ ] Confirmar si `lives-availability` se implementará o se elimina del acta.
- [ ] El `ChallengeStart` heredado (vidas y XP) debe retirarse.

> [!warning] Riesgos
> Un solo alumno sin cuenta en Accounting apaga el desempate por vidas perdidas para todo su grupo empatado. Un Accounting caído deja el Gate en `503` (sin caché vigente) y los desafíos `STANDARD` no se pueden abrir; `RECOVERY` y `LLM` no consultan vidas.

## Historial
- 2026-09-26: acta v1.0 (T-03.1) y cliente HTTP con caché (T-03.2).
- 2026-10-10: el Gate lee vidas de `equip-summary` (HU-16); vidas perdidas para desempate (T-25.2).
- 2026-10-12: cuenta ausente = 404 (`#193`); propagación de `traceparent`/`X-Request-Id`.
- 2026-10-13: consumo de `LIFE_*` y `recovery_pending` (PR #195, V24); un 4xx deja de ser indisponibilidad (#199, #200).
- 2026-10-14: nota creada desde `origin/develop` (`57ff06a`).
- 2026-10-15: respuestas en [[sprints/sprint-3/08-dudas|08-dudas]]: Accounting e Inventario son el mismo equipo (G10); hay que consumir `LIVES_EXHAUSTED`/`LIVES_AVAILABLE` (E8). Con N roadmaps, XP y vidas pueden ser por curso o por roadmap según el profesor (P2).
