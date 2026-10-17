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
| DEC-016 | Neo4j para la estructura del roadmap (pedido de los profes) | 2026-10-14 | aceptada | [[decisiones/DEC-016-neo4j-para-la-estructura-del-roadmap\|DEC-016]] |
| DEC-017 | N roadmaps por curso, con el alcance configurable por el profesor | 2026-10-15 | aceptada | [[decisiones/DEC-017-n-roadmaps-por-curso-configurables\|DEC-017]] |
| DEC-018 | Catálogo cerrado de relaciones y de tipos de nodo | 2026-10-15 | aceptada | [[decisiones/DEC-018-catalogo-de-relaciones-y-tipos-de-nodo\|DEC-018]] |
| DEC-019 | El ranking avisa el estado de sus datos, tiene caché de respaldo y la autorización falla cerrado | 2026-10-15 | aceptada | [[decisiones/DEC-019-ranking-estado-de-datos-y-cache-de-respaldo\|DEC-019]] |
| DEC-020 | La caída de un origen del gate es un motivo (`origin_unavailable`), no un 503 | 2026-10-15 | aceptada | [[decisiones/DEC-020-gate-origen-no-disponible-en-vez-de-503\|DEC-020]] |
| DEC-021 | Postgres es la fuente de verdad de la estructura y Neo4j es una proyección | 2026-10-17 | aceptada | [[decisiones/DEC-021-postgres-fuente-de-verdad-neo4j-proyeccion\|DEC-021]] |

## Decisiones que conviene revisar pronto
> [!warning] Con deuda abierta
> - [[decisiones/DEC-021-postgres-fuente-de-verdad-neo4j-proyeccion\|DEC-021]]: toda escritura de estructura va a Postgres y Neo4j se proyecta desde ahí. Cambia T-18.2, T-18.3, T-18.6 y suma T-65.5. Todo dato nuevo del grafo se agrega primero en Postgres.
> - [[decisiones/DEC-004-flags-apagados-por-defecto\|DEC-004]]: los flags apagados esconden HU ya hechas en la demo; falta decidir cuándo cambian de default.
> - [[decisiones/DEC-001-wire-kafka-v8-snake-case\|DEC-001]]: falta confirmar que los consumidores de `roadmap.events` leen v8.
> - [[decisiones/DEC-006-insignias-sistema-y-curso\|DEC-006]] y [[decisiones/DEC-012-curva-de-niveles-desde-par-09\|DEC-012]]: la curva PAR-09 activa es la de Backoffice (E4, 2026-10-15); actualizar el seed y lo que asuma 600/1800/4200.
> - [[decisiones/DEC-016-neo4j-para-la-estructura-del-roadmap\|DEC-016]]: Neo4j lo sumamos nosotros a la plataforma (G1); falta validar la infra. Los tipos de relación ya están definidos ([[decisiones/DEC-018-catalogo-de-relaciones-y-tipos-de-nodo\|DEC-018]]).
> - [[decisiones/DEC-015-4xx-de-accounting-no-es-indisponibilidad\|DEC-015]]: `fix/account-not-found-gate` ya está hecho (E5, 2026-10-15).
> - [[decisiones/DEC-019-ranking-estado-de-datos-y-cache-de-respaldo\|DEC-019]]: implementación en curso (T-45.7, `fix/t-45-7-error-ranking`). El `503` de dueño sigue siendo un error y la caché se pierde al reiniciar.
> - [[decisiones/DEC-020-gate-origen-no-disponible-en-vez-de-503\|DEC-020]]: aprobada por G09 el 2026-10-16 (acta del gate v1.4, valor `origin_unavailable`); reemplaza el `503` de [[decisiones/DEC-003-gate-pull-identidad-de-servicio-fail-closed\|DEC-003]] cuando se mergee T-31.1. Falta que G09 publique su `roadmap-eligibility.yaml` y su enum.
