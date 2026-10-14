---
tags: [tpi, g10, decision, xp, ledger, motor]
fecha: 2026-09-27
estado: aceptada
reemplaza: ""
---

# DEC-013: Roadmap no calcula XP: aplica el delta del Motor en un ledger idempotente

## Contexto
La primera respuesta de G09 (v2) decía que el Motor "no manda XP, monedas ni vidas" y proponía enviar insumos crudos (`approvalThreshold`, `maxAttempts`, timestamps) para que Roadmap calculara. El 2026-09-27 G09 revirtió: calcula y manda `coins`, `xp`, `add_live`, `subtract_live` y `active_item`, con los parámetros de Backoffice congelados al abrir el intento.

## Decisión
Roadmap **no calcula XP ni maneja el ciclo de vida del desafío**: evalúa su gate y registra el resultado ya calculado. `resources.xp` se aplica **tal cual**, como delta, en `xp_movement` (append-only, `event_id` único `uq_xp_movement_event_id`, sin `UPDATE` ni recálculo). `CHALLENGE_ABORTED` nunca mueve recursos. `add_live`, `subtract_live` y `active_item` no se procesan: son de Accounting. `student_course.lives`/`lost_lives` son un espejo en desuso que ninguna decisión de negocio puede leer.

## Alternativas descartadas
- **Calcular XP en Roadmap con PAR-01 y los insumos del Motor**: se descartó cuando G09 pasó a mandar el resultado calculado.
- **Procesar `subtract_live` para el histórico de "nunca perdió una vida"**: lo hace Accounting; el ranking lee el lote de Accounting.

## Consecuencias
- Positivas: una sola fuente del cálculo; idempotencia ante duplicados; ledger auditable.
- Negativas / deuda:
  - Una re-corrección manual con otro `event_id` **suma XP otra vez** (según `motor-desafios.md` §8, no cubierto por el contrato vigente).
  - Si el Motor cambia su fórmula, el ledger histórico no se corrige (RF-CFG-06).
  - `active_item` llega vacío y `late` en `false` por ahora.

## Referencias
- Código / PR / doc: `services/ProgressService.recordResult`, `XpMovementEntity`, `V10__name_xp_movement_event_id_unique.sql`, `events/ChallengeClosurePayload`; PR #191.
- `tpi-roadmap/docs/contracts/motor-desafios-evento-cierre.md`, `docs/contracts/respuesta-motor-a-roadmap-v2.md` §2, `README.md` (sección roadmap-service), `docs/T-25-2-FUENTE-VIDAS-PERDIDAS.md`.
- Relacionadas: [[acuerdos/motor-desafios-g09|Motor]], [[decisiones/DEC-005-baja-logica-sin-borrar-progreso|DEC-005]].
