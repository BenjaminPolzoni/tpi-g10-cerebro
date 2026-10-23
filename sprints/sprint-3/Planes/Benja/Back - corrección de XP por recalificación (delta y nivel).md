---
tags: [tpi, g10, sprint-3, plan, back, xp, nivel, integración]
fecha: 2026-10-22
autor: Benja
estado: borrador - bloqueado por decisiones
repo: 2026-P4-BE/tpi-roadmap
taiga: sin asignar
orden: 3 de 4 (requiere D1 con G09 y D2 con el equipo)
---

# Back — Corrección de XP cuando el Motor recalifica (delta y nivel)

> [!warning] Actualización (2026-10-23)
> G09 respondió D1 en la tpi-roadmap#312: Motor manda el **total del intento** (`target_experience`) en un evento nuevo, `CHALLENGE_RESULT_RECTIFIED`. El plan vigente está en [[Issue 312 Back - consumir CHALLENGE_RESULT_RECTIFIED (XP y progreso por rectificación)]], que también reemplaza la recomendación de D2 (ahora se acepta que la XP y el nivel bajen).

> [!info] Contexto
> Auditoría del 2026-10-22. Pregunta del equipo: si la diferencia de XP enviada por un desafío es negativa, ¿el alumno puede bajar de nivel? Hoy el caso **no está contemplado**: es accidentalmente imposible.

## 1. Estado actual (verificado en código)

Rutas de `Backend/tpi-roadmap/src/main/java/com/utn/tpi/roadmap/` (`BE/`).

- **Nivel** se calcula al leer, no se guarda: `services/LevelService.java:60-84`, mayor nivel con `xpRequired <= totalXp`. Si `total_xp` baja, el nivel baja solo.
- **Aplicación del XP**: `ProgressService.java:119-173`. Inserta en `xp_movement` y `StudentCourse.addXp` (`totalXp += earnedXp`, `models/StudentCourse.java:49-51`). **Sin `max`, sin clamp, sin check SQL.**
- **Idempotencia** solo por `event_id` (`uq_xp_movement_event_id`).
- **Reenvío del mismo nodo**: `ProgressService.java:137-140` lanza `node.already-passed` y descarta el evento. Por eso un delta negativo hoy nunca llega.
- **Camino de corrección**: `ATTEMPT_CORRECTED` (`RoadmapEventListener.java:344-374`), en el listener de `challenges.results`, **apagado** (`application.properties:272`, `enabled=false`) y marcado como deuda a borrar (`:144-151`).
- **Ledger**: `XpMovementEntity.java:20-22` declara «nunca se recalcula el XP histórico».
- **Contrato**: `ChallengeClosurePayload.java:108` dice que `resources.xp` es delta; `contratos/motor-desafios.md:205-211` (§4.5) lo deja como pregunta abierta.

## 2. Decisiones a tomar (bloquean el desarrollo)

| # | Pregunta | Con quién | Recomendación |
|---|---|---|---|
| D1 | ¿`resources.xp` es el **total del intento** o un **delta**? | G09 (Motor) | Total del intento: permite calcular el delta de forma determinista y es idempotente ante reenvíos |
| D2 | ¿El nivel puede **bajar**? | Equipo / profes | **No**: clampear a `max(delta, 0)` en recompensas; bajar de nivel por una corrección es mala experiencia y rompe insignias ya dadas |
| D3 | ¿Una recalificación puede **quitar** XP en absoluto? | Equipo / profes | Solo si D2 = sí. Si no, la corrección solo sube |

## 3. Plan (si D1 = total y D2 = no baja)

1. En `ProgressService.recordResult`, reemplazar el `already-passed` por: buscar el último `xp_movement` del par (alumno, nodo/desafío); `delta = nuevo - previo`.
2. Si `delta > 0`: insertar movimiento con el delta, `addXp(delta)`. Si `delta <= 0`: registrar el evento (idempotencia) y no tocar el XP.
3. No modificar `completed_node`, desbloqueos ni insignias (ver plan de recálculo de nota).
4. Decidir si se reactiva `ATTEMPT_CORRECTED` o se borra la deuda: con este cambio, el camino principal (`CHALLENGE_COMPLETED`) cubre el caso y se puede **eliminar** el listener apagado.
5. Actualizar `contratos/motor-desafios.md` §4.5 y [[acuerdos/motor-desafios-g09]] con la respuesta de D1.
6. Tests: (a) mismo nodo, XP 100 → 130: +30; (b) 100 → 80: sin cambio y nivel igual; (c) mismo `event_id` reenviado: idempotente; (d) cruce de nivel por la subida.

## 4. Fuera de alcance

Bajar el nivel. Si D2 = sí, hay que agregar: delta negativo permitido (con piso 0), nivel recalculado (ya lo hace `LevelService`), y decidir qué pasa con insignias y gates por XP mínimo ([[sprints/sprint-3/historias/HT-20 Gate y progreso con reglas combinadas y XP mínimo|HT-20]]) que dependan del XP perdido.
