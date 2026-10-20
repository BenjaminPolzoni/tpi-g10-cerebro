---
tags:
  - tpi
  - g10
actualizado: 2026-10-19
---

# Deuda técnica de G10 (roadmap-service)

> [!info] Qué va acá y qué no
> - **Acá:** problemas de **calidad interna** que no son una HU: código muerto, mocks que quedaron, seguridad floja, docs desactualizados, ramas colgadas, duplicados. Vive entre sprints: no se borra al cerrar un sprint.
> - **No va acá:** una HU marcada Done que no cumple sus criterios. Eso está en [[sprints/sprint-3/02-pendientes|02-pendientes]] y en el Bloque 0 del [[sprints/sprint-3/06-backlog-sprint-3|backlog]].
> - Cuando un ítem se toma en un sprint, completar la columna **Sprint**. Cuando se resuelve, pasarlo a [[#Resuelta]] con el PR.

**Impacto:** 🔴 riesgo de seguridad o rompe la demo · 🟠 confunde o frena al equipo · 🟢 limpieza.
**Esfuerzo:** S (≤1 día) · M (2-3 días) · L (≥4 días).

## Back

| # | Imp. | Deuda | Qué hacer | Esf. | Origen | Sprint |
|---|---|---|---|---|---|---|
| DT-01 | 🔴 | El **Gate** (`/eligibility`) acepta a cualquier servicio con token técnico: `SecurityConfig` exige `ServiceIdentity` pero no valida el scope `roadmap.gate.read` | Validar el scope como ya se hace con `roadmap.progress.read` en `/courses/*/progress` | S | [[arquitectura/cors-topics-rutas]] | Proponer con HT-22 |
| DT-02 | 🟠 | Autorización con **roles fijos** (`hasRole`/`hasAnyRole` en constantes por controller) y dos chequeos a mano (`RankingController`, `requireOwner`) | Migrar a permisos con el catálogo de G06. **Actualización (2026-10-17):** el Gateway va a dejar de mandar `X-User-Roles` y mandará permisos; sin el rol, todo chequeo por rol da 403 (ver [[sprints/sprint-3/historias/HT-22 Permisos en vez de roles\|HT-22]]). T-45.9 sumó `GESTOR` al ranking | M | [[sprints/sprint-3/07-correcciones-profes\|07]] | Sprint 3 (HT-22) |
| DT-03 | 🟠 | **No hay una matriz escrita de qué puede hacer cada rol** (ADMIN, GESTOR, PROFESSOR, STUDENT). Hoy hay que leer los controllers | Escribir la tabla rol → acciones. Es la base para HT-22 | S | Consulta del equipo (2026-10-15) | Sprint 3 (con HT-22/C10) |
| DT-05 | 🟢 | Listener **legado** de `challenges.results` (payloads v1/v2) y su flag `KAFKA_TOPIC_CHALLENGE_RESULT_ENABLED`, apagado | Borrar listener, payloads y flag | S | `application.properties` | |
| DT-07 | 🟠 | `TraceIdFilter` figura en `08-comunicacion-gateway.md` pero **no existe** en develop | Confirmar si se borró a propósito y actualizar el doc | S | E7 en [[sprints/sprint-3/08-dudas\|08]] | |
| DT-08 | 🟢 | Accounting publica `LIVES_EXHAUSTED`/`LIVES_AVAILABLE` y no hay consumidor | Decidir si hace falta; si no, sacarlo del acta | S | E8 en [[sprints/sprint-3/08-dudas\|08]] | |
| DT-09 | 🟢 | La **caché de respaldo del ranking** (T-45.7) vive en memoria: se pierde al reiniciar el micro y no se comparte entre instancias | Si se escala a varias instancias o hace falta sobrevivir reinicios, evaluar una caché compartida | M | [[decisiones/DEC-019-ranking-estado-de-datos-y-cache-de-respaldo\|DEC-019]] | |
| DT-22 | 🟠 | `OutboxPoller.publishPending()` tiene `@Transactional` y espera el ACK de Kafka adentro (`send().get()`): retiene la conexión de Hikari y las filas bloqueadas | Reclamar el lote en una transacción corta, enviar fuera y marcar el resultado en otra (como `tpi-sandbox`) | M | [[arquitectura/patrones-de-diseno\|patrones]] (2026-10-19) | |
| DT-23 | 🟠 | `COURSE_LEVEL_UP` y `PERFORMANCE_ZONE_CHANGED` figuran como publicados en `AGENTS.md` y [[arquitectura/contexto-integral]] pero no se emiten en ningún lado | Implementarlos o corregir los docs ([[decisiones/DEC-002-outbox-transaccional-eventos-salientes\|DEC-002]]) | M | [[arquitectura/patrones-de-diseno\|patrones]] (2026-10-19) | |
| DT-24 | 🟠 | `BadgeEvaluator.meets` manda `SECTION_NO_LIVES_LOST`, `NODE_NO_RETRIES` y `LIFE_RECOVERED` a `default -> false`: esas insignias nunca se otorgan | Implementar los criterios o sacarlos de `BadgeCriterion` | M | [[arquitectura/patrones-de-diseno\|patrones]] (2026-10-19) | |
| DT-25 | 🟢 | Módulo `graph/` (Neo4j) sin uso: ningún service lo llama y no hay proyector ([[decisiones/DEC-021-postgres-fuente-de-verdad-neo4j-proyeccion\|DEC-021]]) | Terminar el proyector o sacar el módulo hasta que haga falta | L | [[arquitectura/patrones-de-diseno\|patrones]] (2026-10-19) | |
| DT-26 | 🟠 | Clientes HTTP a Courses y Accounting sin circuit breaker: con el origen lento, cada request espera el timeout completo | Resilience4j como `CoursesCallGuard` de `tpi-theoristcal-challenge` | M | [[arquitectura/patrones-plataforma\|patrones plataforma]] (2026-10-19) | |

## Front

| # | Imp. | Deuda | Qué hacer | Esf. | Origen | Sprint |
|---|---|---|---|---|---|---|
| DT-10 | 🟠 | `BankDataPort` → `InMemoryBankAdapter`: vidas, monedas y XP salen de **localStorage** | Pasarlo a HTTP | M | [[sprints/sprint-3/01-estado-actual\|01]] | |
| DT-11 | 🟢 | Adapter in-memory y `seed.ts` dentro del árbol de producción | Moverlos a tests | S | [[sprints/sprint-3/02-pendientes\|02]] | |
| DT-12 | 🟢 | `level-curve.ts` **duplicado** en `accounting` y en `roadmap/mocks` | Dejar uno | S | [[sprints/sprint-3/01-estado-actual\|01]] | |
| DT-13 | 🟠 | **Racha falsa**: `streak.component` muestra un **7 fijo**, sin lógica (la épica EP-592 no tiene HU) | Se implementa la racha en [[sprints/sprint-3/historias/HU-73 Ver mi racha de días con actividad\|HU-73]] (E12 en [[sprints/sprint-3/08-dudas\|08]]) | S | Consulta del equipo (2026-10-15) | |
| DT-15 | 🟢 | Roadmap con **316 colores hardcodeados** y un puente de tokens `--color-*` propio | Pasar a los tokens del kit | L | [[sprints/sprint-3/05-ui-kit\|05]] | Sprint 3 (épica UI-KIT) |
| DT-16 | 🟢 | GLB optimizados **no versionados** (219 GLB, ~60 MB) | Versionarlos o documentar el pipeline (HT-08) | S | [[sprints/sprint-3/01-estado-actual\|01]] | |

## Repos, docs y Taiga

| # | Imp. | Deuda | Qué hacer | Esf. | Origen | Sprint |
|---|---|---|---|---|---|---|
| DT-17 | 🟠 | **Ramas colgadas** en el back: `feature/t-21-7-roadmap-events-topic` (redundante), `fix/account-not-found-gate` (revisar contra #193), `bypass-desafio-11-10` (flag de demo), `revert-130-…` (**no mergear**) | Cerrar o mergear cada una | S | [[sprints/sprint-3/01-estado-actual#Ramas sin mergear a develop\|01]] | Sprint 3 (Bloque 0, parcial) |
| DT-18 | 🟠 | **Contratos desactualizados**: `courses.md` §7.3 y el estándar de Kafka siguen en camelCase; el código lee snake_case (DEC-001) | Actualizar los docs | S | [[acuerdos/courses-g01]] | |
| DT-19 | 🟢 | **Taiga desactualizado**: 15/17 épicas en New con sus HU Done, HT-11 dice camelCase, HT-04/10/11 sin épica, HT-05 sin épica ni tag | Ordenarlo (HT-11, E10, E11) | S | [[taiga/README\|Taiga]] | Sprint 3 (Bloque 0) |
| DT-20 | 🟢 | Flags que esconden funcionalidad hecha: `SECTIONS_SYNC_ENABLED`, `ROADMAP_BY_GROUP_ENABLED` | Encenderlos en los entornos; después evaluar sacar el flag | S | [[decisiones/DEC-004-flags-apagados-por-defecto\|DEC-004]] | Sprint 3 (Bloque 0) |
| DT-21 | 🟢 | **Vault personal sin git**: `~/Documents/Obsidian Vault` no es repo y no tiene el plugin Obsidian Git. El cerebro del equipo sí está conectado desde `~/dev/TPI_2026/tpi-g10-cerebro` (origin en GitHub, `main`, plugin activo) | Para usar el cerebro: abrir esa carpeta como vault y activar Git (ver [[COMO-USAR#1. Clonar y abrir en Obsidian (una sola vez)\|COMO-USAR §1]]). Para otro vault: `git init`, agregar el remote y el plugin Obsidian Git | S | [[COMO-USAR]] | |

## Resuelta

| # | Deuda | Cómo se resolvió | PR / fecha |
|---|---|---|---|
| — | Outbox sin topic de salida | `roadmap.events` por defecto | #134 |
| DT-04 | `ProgressService.startChallenge` muerto | Borrado junto con el pre-chequeo del alumno (T-31.5) | BE#234, 2026-10-16 |
| DT-06 | `@DefaultValue("stub")` en properties de clientes | Perfiles `dev`/`prod` separados, clientes en `http` por defecto | BE#226, 2026-10-16 |
| DT-09 (front) | IDs de mock en rutas reales | Alumno y curso desde la sesión y la ruta (HT-14) | FE#607, 2026-10-16 |
| DT-14 | UI-KIT en 0.7.1 | `develop` usa `@2026-p4-fe/ui ^0.10.0` (verificado el 2026-10-18) | — |

> [!warning] Deuda nueva (2026-10-18)
> - **Migraciones fuera de orden:** BE#258 trae V39 con V45 ya en `develop`. Ver [[sprints/sprint-3/14-cambios-recientes#Alertas para el equipo|14 — Alertas]].
> - **Nombre del nodo desalineado:** back 2 caracteres (BE#271), front 3.
