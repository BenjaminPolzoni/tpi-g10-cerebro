---
tags: [tpi, g10, acuerdo, inventario, vidas, gate]
fecha: 2026-09-26
grupos: [G10, Gxx]  # Inventario sale servido por Accounting (Tema 08); grupo a verificar
estado: vigente
contrato: "contratos/accounting-roadmap-v1.md"
---

# Acuerdo con Inventario (vidas e ítems): equip-summary, Gate y pantalla de inventario

> [!info] Fuentes
> - `contratos/accounting-roadmap-v1.md` §3.7, §5, §6.
> - `contratos/roadmap-motor-gate-v1.md` §5, §6, §6.2.
> - `terminado/T-35-1-ENDPOINT-INVENTARIO.md`, `terminado/T-15-4-MATRICULA-VIDAS-RECUPERACION.md`, `terminado/T-03-2-ACCOUNTING-CLIENT.md`.
> - Contrato general y eventos: [[acuerdos/accounting|Accounting]].

> [!question] Verificar
> En el código, "Inventario" es el puerto `InventoryClient`, que llama a `/api/accounting/...`. No hay otro servicio de inventario en los docs. Esta nota cubre solo **vidas e ítems del alumno**; confirmar el grupo responsable.

## Qué se acordó
- **Una sola llamada por alumno y curso** trae vidas, saldo e ítems: `equip-summary`. No hay batch de inventarios de varios alumnos.
- El Gate usa **vidas libres** `freeLives = currentLives - reservedLives`; solo bloquea con `no_lives` si el nodo es `STANDARD` y `freeLives <= 0`. Los nodos `RECOVERY` y `LLM` **no consultan** vidas (una llamada menos y la caída de Accounting no los bloquea).
- La pantalla de inventario (HU-35) es `STUDENT` y solo del propio alumno (`X-User-Id`, nunca de la URL). Sin matrícula activa: `403 student.not-enrolled`, sin consultar a Accounting.
- Ante una caída, la pantalla muestra el **último dato conocido** con aviso (`stale: true`, retención 24 h por defecto); el Gate **nunca** usa ese dato.
- **Cuenta ausente** en Accounting (`404 ACCOUNT_NOT_FOUND`) no es una caída: se informa como `404` Problem Details `inventory.account-not-found`, sin convertirlo en `no_lives` ni habilitar el intento.
- Roadmap no reserva ni consume ítems; equipar es del lado de Accounting.

## Quién lo acordó
- G10: equipo Roadmap.
- Otro grupo: equipo Accounting/Inventario (Tema 08), Gxx (verificar). Confirmado el 2026-10-15: Inventario y Accounting son el mismo equipo (G10). La aprobación nominal del acta v1.0 está pendiente.

## Contrato técnico
- **Endpoint:** `GET /api/accounting/courses/{courseId}/accounts/{studentId}/equip-summary` por Gateway.
- **Auth:** Bearer técnico, audience `accounting-service`, scope `accounting.account.read`.
- **Respuesta:** `currentLives`, `reservedLives`, `availableBalance`, `items[]` (`itemInstanceId`, `catalogItemId`, `itemName`, `itemType`, `itemEffect`, `applicableChallengeScope`, `status`, `maxCharges`, `remainingUses`). Vocabulario abierto: un valor nuevo no rompe la lectura. Un resumen incompleto (sin vidas, saldo o lista; ítem sin id/estado/contadores válidos) se trata como indisponibilidad: nunca se completa con datos inventados.
- **Lo que exponemos:** `GET /api/roadmap/courses/{courseId}/inventory` (`InventoryView`: vidas, `freeLives`, saldo, ítems, `stale`, `retrieved_at`, `notice`).
- **Timeouts y caché:** conexión y lectura 2 s; caché `(courseId, studentId)` TTL 30 s (default técnico, no contractual); sin retries locales.
- **Degradación del Gate:** 503 Problem Details (`trace_id`) si no hay caché vigente (en la v1.4 del acta del gate (aprobada por G09; entra con T-31.1) pasa a `200` con `reason=origin_unavailable`, [[decisiones/DEC-020-gate-origen-no-disponible-en-vez-de-503|DEC-020]]); 404 `inventory.account-not-found` si la cuenta no existe; 502 si Accounting rechaza la consulta (4xx no transitorio). Ver [[decisiones/DEC-015-4xx-de-accounting-no-es-indisponibilidad|DEC-015]].
- **Proyección informativa:** `student_course.recovery_pending` (V24) sale de los eventos `LIFE_CREDITED`/`LIFE_DEBITED`; no decide nada del Gate.

## Impacto en nuestro código
- `clients/inventory/InventoryClient` (puerto), `HttpInventoryClient`, `InventoryConfig` (siempre HTTP, sin modo stub desde T-09.5), `InventoryProperties`.
- `controllers/InventoryController`, `services/InventoryService` (último dato conocido), `dtos/InventoryDtos`.
- `services/GateEvaluator` (política de vidas por `LivesPolicy`), `controllers/GateController` (mapeo de 404/502/503), `RecoveryPendingService`.
- Tests: `InventoryHttpScenario` (Accounting guionado por HTTP), `InventoryIntegratedE2ETest` (T-09.6), BDD de inventario (T-40.2).

## Pendiente / próximos pasos
- [ ] **404 `ACCOUNT_NOT_FOUND`:** en `origin/develop` ya está el PR #193 (2026-10-12, `d48542b`: 404 propio `inventory.account-not-found`). La rama `origin/fix/account-not-found-gate` (`6c0dac5`) **sigue sin mergear** y propone otro tratamiento (bloquear con `not_enrolled`). La auditoría de Sprint 3 la lista como "mergear"; con #193 en develop parece **redundante o contradictoria**.
- [ ] Coordinar con G09 el tratamiento del `404` del gate (su cliente solo define `403`/`503`). Ver [[acuerdos/motor-desafios-g09|Motor]].
- [ ] Motivo funcional dedicado para "cuenta no aprovisionada" (hoy es un 404 fuera del vocabulario cerrado del Gate).
- [ ] Alta de la cuenta del alumno al inscribirse: la crea el flujo de inscripción/alta, no Roadmap (se asume; verificar quién la dispara).
- [ ] Gate: falta "último dato 24 h + stale" y el motivo `origin_unavailable` (auditoría Sprint 3).

> [!warning] Riesgos
> - Un alumno inscripto sin cuenta en Accounting no puede abrir desafíos `STANDARD` ni ver el inventario (404) hasta que se cree la cuenta.
> - Si Accounting cambia a una ruta distinta de `lives-availability`, el contrato escrito y el cliente divergen: hoy el Gate depende de `equip-summary`, que es más pesado.

> [!question] Verificar
> Confirmar en el entorno integrado si `fix/account-not-found-gate` debe cerrarse como obsoleta y si el 404 de #193 llega bien al front.

## Historial
- 2026-09-26: acta v1.0 y cliente HTTP (T-03.2); `equip-summary` para la pantalla (T-35.1).
- 2026-10-07: caché vencida reportada como 503 en el Gate (T-16.3).
- 2026-10-09: se eliminan los dobles de ítems/vidas; Inventory siempre HTTP (T-09.5).
- 2026-10-10: el Gate lee vidas de `equip-summary` (HU-16).
- 2026-10-12: cuenta ausente = 404 (PR #193).
- 2026-10-13: 4xx de Accounting distinto de 404 = 502, no 503/500 (PR #199).
- 2026-10-14: nota creada desde `origin/develop` (`57ff06a`).
- 2026-10-15: Inventario y Accounting son el mismo equipo (G10 en [[sprints/sprint-3/08-dudas|08-dudas]]); `fix/account-not-found-gate` ya está hecho (E5).
