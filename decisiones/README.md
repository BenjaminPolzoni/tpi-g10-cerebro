---
tags: [tpi, g10, decision, indice]
fecha: 2026-10-14
---

# Decisiones técnicas de G10 (Roadmap)

Registro de decisiones **ya tomadas** que se deducen del código, los contratos y el historial de `origin/develop` de `tpi-roadmap` (tip `57ff06a`, 2026-10-14). Cada nota cita archivos y commits en *Referencias*. Estructura: [[plantillas/decision]]. La fecha es la de la evidencia más temprana (commit, migración o acta).

> [!info] Alcance
> Solo hay decisiones con evidencia. Lo que no estaba claro quedó marcado como `[!question] Verificar` dentro de cada nota. Las contrapartes y contratos están en el [[acuerdos/README|índice de acuerdos]].

| DEC | Título | Fecha | Estado | Nota |
|---|---|---|---|---|
| DEC-001 | Wire Kafka y HTTP en snake_case (contratos-kafka v8), sin alias | 2026-10-12 | aceptada | [[decisiones/DEC-001-wire-kafka-v8-snake-case\|DEC-001]] |
| DEC-002 | Eventos salientes por outbox transaccional | 2026-09-26 | aceptada | [[decisiones/DEC-002-outbox-transaccional-eventos-salientes\|DEC-002]] |
| DEC-003 | Gate por pull con identidad de servicio, solo lectura y fail-closed | 2026-09-26 | aceptada | [[decisiones/DEC-003-gate-pull-identidad-de-servicio-fail-closed\|DEC-003]] |
| DEC-004 | Funcionalidad con dependencias externas, apagada por defecto (flags) | 2026-10-06 | aceptada | [[decisiones/DEC-004-flags-apagados-por-defecto\|DEC-004]] |
| DEC-005 | Baja lógica en todo y el progreso del alumno nunca se borra | 2026-09-24 | aceptada | [[decisiones/DEC-005-baja-logica-sin-borrar-progreso\|DEC-005]] |
| DEC-006 | Dos orígenes de insignias: sistema y curso | 2026-10-03 | aceptada | [[decisiones/DEC-006-insignias-sistema-y-curso\|DEC-006]] |
| DEC-007 | El anonimato del ranking se resuelve en el servidor | 2026-10-03 | aceptada | [[decisiones/DEC-007-anonimato-ranking-en-servidor\|DEC-007]] |
| DEC-008 | El perfil `integrated` no arranca con clientes en stub (HT-09) | 2026-10-03 | aceptada | [[decisiones/DEC-008-perfil-integrated-falla-con-stubs\|DEC-008]] |
| DEC-009 | Los gestores pueden editar el roadmap de cualquier curso | 2026-10-11 | aceptada | [[decisiones/DEC-009-gestores-editan-roadmaps\|DEC-009]] |
| DEC-010 | Prerrequisitos entre unidades (secciones), migración V25 | 2026-10-13 | aceptada | [[decisiones/DEC-010-prerrequisitos-por-seccion-v25\|DEC-010]] |
| DEC-011 | Se quita el umbral de XP de las secciones (V8): desbloqueo por prerrequisitos | 2026-09-21 | aceptada | [[decisiones/DEC-011-quitar-umbral-xp-seccion-v8\|DEC-011]] |
| DEC-012 | La curva de niveles viene de Backoffice (PAR-09) | 2026-09-24 | aceptada | [[decisiones/DEC-012-curva-de-niveles-desde-par-09\|DEC-012]] |
| DEC-013 | Roadmap no calcula XP: aplica el delta del Motor en un ledger idempotente | 2026-09-27 | aceptada | [[decisiones/DEC-013-roadmap-no-calcula-xp-ledger-idempotente\|DEC-013]] |
| DEC-014 | Comisiones: un roadmap por cohorte, pertenencia múltiple y evaluación en Roadmap | 2026-10-08 | aceptada | [[decisiones/DEC-014-comisiones-modelo-b-evaluacion-en-roadmap\|DEC-014]] |
| DEC-015 | Un 4xx de Accounting no es una indisponibilidad | 2026-10-13 | aceptada | [[decisiones/DEC-015-4xx-de-accounting-no-es-indisponibilidad\|DEC-015]] |

## Decisiones que conviene revisar pronto
> [!warning] Con deuda abierta
> - [[decisiones/DEC-004-flags-apagados-por-defecto\|DEC-004]]: los flags apagados esconden HU ya hechas en la demo; falta decidir cuándo cambian de default.
> - [[decisiones/DEC-015-4xx-de-accounting-no-es-indisponibilidad\|DEC-015]]: la rama `fix/account-not-found-gate` sigue sin mergear junto a #193.
> - [[decisiones/DEC-001-wire-kafka-v8-snake-case\|DEC-001]]: falta confirmar que los consumidores de `roadmap.events` leen v8.
> - [[decisiones/DEC-006-insignias-sistema-y-curso\|DEC-006]] y [[decisiones/DEC-012-curva-de-niveles-desde-par-09\|DEC-012]]: confirmar qué curva PAR-09 está activa (600/1800/4200 vs la de ejemplo de Backoffice).
