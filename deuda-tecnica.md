---
tags: [tpi, g10, deuda-tecnica]
actualizado: 2026-10-15
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
| DT-01 | 🔴 | El **Gate** (`/eligibility`) acepta a cualquier servicio con token técnico: `SecurityConfig` exige `ServiceIdentity` pero no valida el scope `roadmap.gate.read` | Validar el scope como ya se hace con `roadmap.progress.read` en `/courses/*/progress` | S | [[arquitectura/cors-topics-rutas]] | Proponer con C9 |
| DT-02 | 🟠 | Autorización con **roles fijos** (`hasRole`/`hasAnyRole` en constantes por controller) y dos chequeos a mano (`RankingController`, `requireOwner`) | Migrar a permisos con el catálogo de G06 | M | [[sprints/sprint-3/07-correcciones-profes\|07]] | Sprint 3 (C9) |
| DT-03 | 🟠 | **No hay una matriz escrita de qué puede hacer cada rol** (ADMIN, GESTOR, PROFESSOR, STUDENT). Hoy hay que leer los controllers | Escribir la tabla rol → acciones. Es la base para C9 | S | Consulta del equipo (2026-10-15) | Sprint 3 (con C9/C10) |
| DT-04 | 🟢 | `ProgressService.startChallenge` es **código muerto** | Borrarlo al hacer el pre-chequeo de HU-48 | S | [[sprints/sprint-3/02-pendientes\|02]] | Sprint 3 (Bloque 0) |
| DT-05 | 🟢 | Listener **legado** de `challenges.results` (payloads v1/v2) y su flag `KAFKA_TOPIC_CHALLENGE_RESULT_ENABLED`, apagado | Borrar listener, payloads y flag | S | `application.properties` | |
| DT-06 | 🟢 | Quedan `@DefaultValue("stub")` en properties de clientes | Borrarlos (HT-09 ya prohíbe stubs en el arranque) | S | [[sprints/sprint-3/02-pendientes\|02]] | |
| DT-07 | 🟠 | `TraceIdFilter` figura en `08-comunicacion-gateway.md` pero **no existe** en develop | Confirmar si se borró a propósito y actualizar el doc | S | E7 en [[sprints/sprint-3/08-dudas\|08]] | |
| DT-08 | 🟢 | Accounting publica `LIVES_EXHAUSTED`/`LIVES_AVAILABLE` y no hay consumidor | Decidir si hace falta; si no, sacarlo del acta | S | E8 en [[sprints/sprint-3/08-dudas\|08]] | |

## Front

| # | Imp. | Deuda | Qué hacer | Esf. | Origen | Sprint |
|---|---|---|---|---|---|---|
| DT-09 | 🔴 | **IDs de mock en rutas reales**: `DEMO_STUDENT_ID`, `COURSE_SEED_ID`, `CURRENT_STUDENT_ID` | Tomar alumno y curso de la sesión y de la ruta; sin usuario, error | S | [[sprints/sprint-3/02-pendientes\|02]] | Sprint 3 (Bloque 0) |
| DT-10 | 🟠 | `BankDataPort` → `InMemoryBankAdapter`: vidas, monedas y XP salen de **localStorage** | Pasarlo a HTTP | M | [[sprints/sprint-3/01-estado-actual\|01]] | |
| DT-11 | 🟢 | Adapter in-memory y `seed.ts` dentro del árbol de producción | Moverlos a tests | S | [[sprints/sprint-3/02-pendientes\|02]] | |
| DT-12 | 🟢 | `level-curve.ts` **duplicado** en `accounting` y en `roadmap/mocks` | Dejar uno | S | [[sprints/sprint-3/01-estado-actual\|01]] | |
| DT-13 | 🟠 | **Racha falsa**: `streak.component` muestra un **7 fijo**, sin lógica (la épica EP-592 no tiene HU) | Sacarlo de la UI o implementar la épica (E12 en [[sprints/sprint-3/08-dudas\|08]]) | S | Consulta del equipo (2026-10-15) | |
| DT-14 | 🟠 | UI-KIT en **0.7.1** (última 0.8.0): 9 TODOs esperando el bump | Subir a 0.8.0 y cerrar los TODOs | M | [[sprints/sprint-3/05-ui-kit\|05]] | Sprint 3 (épica UI-KIT) |
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
