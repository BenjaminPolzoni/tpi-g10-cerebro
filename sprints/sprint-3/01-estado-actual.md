---
tags: [tpi, g10, sprint-3, auditoria, taiga]
fecha: 2026-10-14
estado: borrador
---

# 01 — Estado actual (Taiga vs código) al cierre del Sprint 2

> [!info] Alcance de la auditoría
> Auditoría del 2026-10-14 sobre `origin/develop`:
> - Back `2026-P4-BE/tpi-roadmap` en el tip `57ff06a`.
> - Front `2026-P4-FE/2026-PIV-TPI-FE` en el tip `8a770d50`.

> [!warning] Limitaciones
> No se corrieron los tests. El estado sale de leer el código, los tests y los commits.
> Los criterios de aceptación se cotejaron completos en parte de las HU. En las demás el estado se dedujo del código y de los títulos.

## Resumen

- En Taiga todas las HU de G10 están en **Done**, salvo **HU-45** y **HU-49** (New).
- En el código hay varias HU "Done" que **no están completas**. El detalle está en [02-pendientes.md](02-pendientes.md).
- El back está muy avanzado y tiene tests: suites BDD en `src/test/.../bdd/` y tests por feature.
- En el front casi todo usa HTTP real. Lo que todavía está en memoria es el banco de vidas, monedas y XP (`InMemoryBankAdapter` + localStorage).

Columnas:
- **Taiga**: estado de la HU en Taiga.
- **Back** / **Front**: qué tan implementada está la HU en el código de esa capa (`origin/develop`), contra sus criterios de aceptación.

Leyenda de Back y Front:
- ✅ **Completo**: cumple los criterios de aceptación en esa capa.
- ⚠️ **Parcial**: existe, pero le falta algo o tiene un bug. Qué falta está en *Nota principal*.
- ❌ **Falta**: la HU necesita esa capa y no hay nada hecho.
- N/A **No aplica**: la HU no tiene trabajo en esa capa (ej. consumir un evento de Kafka no tiene pantalla).

## Tabla por HU

| HU                                         | Taiga    | Back | Front | Nota principal                                                                                                                                                                                                                                     |
| ------------------------------------------ | -------- | ---- | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HU-01 Crear nodos en el grafo              | Done     | ⚠️   | ⚠️    | Back: falta el campo `reintentos_permitidos` y no hay consumidor de la baja de desafío del Motor (CA8). Front: `moveNode` devuelve 501, así que las posiciones no se guardan, y las aristas se escriben reescribiendo las reglas del nodo destino. |
| HU-03 Consumir resultado del Motor         | Done     | ✅    | N/A   | Idempotente por `eventId`. El outbox emite `NODE_COMPLETED` y `NODE_UNLOCKED`.                                                                                                                                                                     |
| HU-04 Vincular contenido a Courses         | Done     | ✅    | ⚠️    | Front: no se verificó el rechazo de material no publicado.                                                                                                                                                                                         |
| HU-05 Detalle de nodo                      | Done     | ✅    | ✅     | Un nodo bloqueado devuelve el detalle sin título.                                                                                                                                                                                                  |
| HU-06 Marcar como leído                    | Done     | ✅    | ✅     | `POST /nodes/{id}/read`                                                                                                                                                                                                                            |
| HU-11 Lectura obligatoria                  | Done     | ✅    | ⚠️    | Front: el flag se edita, pero no hay una UI propia de bloqueo por lectura.                                                                                                                                                                         |
| HU-13 Reglas AND/OR                        | Done     | ✅    | ✅     | Se agregó además la regla de prerrequisitos por sección (V25).                                                                                                                                                                                     |
| HU-14 Recorrido con bloqueos               | Done     | ✅    | ✅     | `block_reason` sale del mismo evaluador que el gate.                                                                                                                                                                                               |
| HU-15 Gate                                 | Done     | ⚠️   | ✅     | Back: no existe el motivo `origen_no_disponible` (devuelve 503). Front: usa `DEMO_STUDENT_ID` como respaldo.                                                                                                                                       |
| HU-16 Inventario real para las vidas       | Done     | ⚠️   | N/A   | El gate no usa "último dato 24 h + stale". La rama `fix/account-not-found-gate` está sin mergear; revisar contra #193, que ya está en develop.                                                                                                     |
| HU-17 Baja de sección de Courses           | Done     | ✅    | N/A   | Funciona solo con `SECTIONS_SYNC_ENABLED`, que está apagado por defecto.                                                                                                                                                                           |
| HU-18 Reordenamiento de secciones          | Done     | ✅    | N/A   | Ídem (flag apagado).                                                                                                                                                                                                                               |
| HU-19 Avance de lectura                    | Done     | ✅    | ✅     |                                                                                                                                                                                                                                                    |
| HU-20 Catálogo de insignias                | Done     | ⚠️   | ⚠️    | Back: hay 3 criterios del catálogo que nunca se otorgan. Front: no se puede editar ni dar de baja.                                                                                                                                                 |
| HU-21 Otorgar insignias                    | Done     | ⚠️   | N/A   | No se otorgan `SECTION_NO_LIVES_LOST`, `NODE_NO_RETRIES` ni `LIFE_RECOVERED`. El topic de salida ya es `roadmap.events` por defecto en develop (#134).                                                                                             |
| HU-22 Ver mis insignias                    | Done     | ✅    | ⚠️    | Hay un TODO en `ranking-detail.component.ts:190` (ui-kit#59, falta un modo solo lectura).                                                                                                                                                          |
| HU-24 Ranking del curso                    | Done     | ✅    | ⚠️    | Front: `ranking-panel` llama con `COURSE_SEED_ID` fijo y `ranking-detail` usa `CURRENT_STUDENT_ID` de mock.                                                                                                                                        |
| HU-25 Desempate en cascada                 | Done     | ✅    | ✅     |                                                                                                                                                                                                                                                    |
| HU-36/37 Sincronizar unidades con Courses  | Done     | ✅    | ✅     | Necesita el flag `SECTIONS_SYNC_ENABLED`.                                                                                                                                                                                                          |
| HU-38 Nivel en el curso                    | Done     | ✅    | ✅     | `level-curve.ts` está duplicado en `accounting` y en `roadmap/mocks`.                                                                                                                                                                              |
| HU-40 Ítems en el roadmap                  | Done     | ✅    | ✅     | Con `lastKnown` + `stale`.                                                                                                                                                                                                                         |
| HU-41 Editar nodo individual               | Done     | ⚠️   | ✅     | Falta el campo de reintentos. Un PUT sin `lives_policy` resetea el nodo a STANDARD (bug conocido).                                                                                                                                                 |
| HU-42 Leer material del nodo               | Done     | ✅    | ⚠️    | Falta verificar el visor embebido.                                                                                                                                                                                                                 |
| HU-43 Ícono del desafío                    | Done     | ⚠️   | ✅     | El back no restringe el ícono a nodos DESAFIO/EXAMEN.                                                                                                                                                                                              |
| HU-44 Roadmap por comisión                 | **Done** | ⚠️   | ❌     | El front no tiene selector de comisión. En el back está todo detrás de `ROADMAP_BY_GROUP_ENABLED=false`.                                                                                                                                           |
| HU-45 Ranking y avance por comisión        | New      | ⚠️   | ❌     | El back tiene `GET /groups/{gid}/progress`. En el front no hay nada.                                                                                                                                                                               |
| HU-46 Material en nodos y Templo           | Done     | ✅    | ⚠️    | Se borró la página Templo (`student/materials`).                                                                                                                                                                                                   |
| HU-47 Desafío del pool del Motor           | Done     | ✅    | ✅     | La rama `bypass-desafio-11-10` está sin mergear (es de demo).                                                                                                                                                                                      |
| HU-48 Saber si puedo entrar a un desafío   | **Done** | ❌    | ✅     | No hay un pre-chequeo que el alumno pueda llamar con su JWT: el gate es solo `ServiceIdentity`. `ProgressService.startChallenge` quedó como código muerto.                                                                                         |
| HU-49 Restricciones de Courses             | New      | ⚠️   | ❌     | Back: se aplica la restricción por fecha, pero falta HIDDEN vs LOCKED, el evento de cambio y el aviso. Front: no hay nada. Depende de G01.                                                                                                         |
| HU-50 Elegir bioma                         | Done     | ✅    | ✅     |                                                                                                                                                                                                                                                    |
| HU-51 Mundo Luna                           | Done     | N/A  | ⚠️    | Tiene menos archivos que los otros mundos. Revisar que esté completo.                                                                                                                                                                              |
| HU-52 a 56 Mundos                          | Done     | N/A  | ✅     |                                                                                                                                                                                                                                                    |
| HT-05 Migrar el front a nodos              | Done     | N/A  | ✅     | Siguen vivos el adapter in-memory, el seed y `COURSE_SEED_ID`.                                                                                                                                                                                     |
| HT-08 Optimizar GLB                        | Done     | N/A  | ⚠️    | Los GLB optimizados no están versionados (hay 219 GLB, unos 60 MB).                                                                                                                                                                                |
| HT-09 Sin simulaciones en el micro         | Done     | ✅    | N/A   | `IntegratedClientsValidator` hace fallar el arranque si queda algún stub.                                                                                                                                                                          |
| HT-10 Comisiones con identidad de servicio | Done     | ✅    | N/A   | No se confirmaron los scopes en la config.                                                                                                                                                                                                         |
| HT-11 Evento de cierre del Motor           | Done     | ✅    | N/A   | El código usa snake_case (contrato v8). **El texto de Taiga dice camelCase**: hay que actualizarlo.                                                                                                                                                |

## Ramas sin mergear a develop

**Back**

| Rama | Qué hacer |
|---|---|
| `fix/account-not-found-gate` | **Revisar.** Trata el 404 `ACCOUNT_NOT_FOUND` de Accounting en el gate (HU-15/16). develop ya trae #193 para Inventario: confirmar si es redundante o contradictoria. |
| `feature/t-21-7-roadmap-events-topic` | **Cerrar.** Redundante: develop ya tiene `roadmap.events` por defecto (#134). |
| `bypass-desafio-11-10` | Revisar. Trae un flag de demo que no debe llegar a producción. |
| `revert-130-feature/5390-ranking-rules-parity` | **No mergear.** Deja sin tests al ranking. |
| `release/2.0.0` | PR #210. Solo cambia versiones. |
| `feature/contracts-courses-m2m`, `feature/docs-contexto-agentes` | Solo documentación. |

**Front:** `fix/biome-avatar` y `fix/roadmap-editor-fixes`.

## Flags apagados por defecto que esconden funcionalidad

> [!danger] Con estos flags apagados, en la demo no funcionan cosas que ya están hechas.
> | Variable | Valor por defecto | HU afectadas |
> |---|---|---|
> | `SECTIONS_SYNC_ENABLED` | false | HU-17, 18, 36 |
> | `ROADMAP_BY_GROUP_ENABLED` | false | HU-44, 45 |

## Mocks o datos fijos en el front (develop)

- `DEMO_STUDENT_ID` como respaldo en:
  - `roadmap.store.ts:134`
  - `hex-world-page.component.ts:462`
  - `challenge-attempt.service.ts:74`
- `COURSE_SEED_ID`: curso por defecto de `RoadmapStore` y valor fijo en `ranking-panel`.
- `CURRENT_STUDENT_ID` (mock) en `ranking-detail.component.ts:485`.
- `BankDataPort` → `InMemoryBankAdapter`, con localStorage para vidas, monedas y XP.
- Avatar en localStorage (comentario "Phase 3 BFF"). `visit.service.ts` guarda el progreso de visitas en el navegador.
- Llamadas que devuelven 501 a propósito en `http-roadmap.adapter.ts`: `moveNode`, `listCourses`, `createCourse`, `removeCourse`, `getStudents`, `registerProgress`.

## Restos en el back

- `@DefaultValue("stub")` en las `*Properties` de `clients/`. No tiene efecto porque `application.properties` fuerza `http`, pero conviene limpiarlo.
- `ProgressService.startChallenge:113` no tiene callers.
- El listener legado `handleChallengeCompleted` (v1/v2) está apagado por defecto.
