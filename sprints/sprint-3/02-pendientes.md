---
tags: [tpi, g10, sprint-3, pendientes, deuda]
fecha: 2026-10-14
estado: borrador
---

# 02 — Pendientes que deberían estar resueltos para el Sprint 3

Son HU que figuran **Done** en Taiga pero no cumplen sus criterios de aceptación en el código, más la deuda que bloquea la demo. Se ordenan por impacto.

## P0: rompen la demo o el flujo principal

> [!danger] Resolver en la primera semana
> | # | Tema | Capa | Acción |
> |---|---|---|---|
> | 1 | ~~Outbox sin topic~~ **Corregido:** develop ya publica en `roadmap.events` por defecto (#134) | Back | Cerrar la rama redundante `feature/t-21-7-roadmap-events-topic` |
> | 2 | 404 `ACCOUNT_NOT_FOUND` de Accounting tomado como caída en el gate | Back | develop ya trae #193 (404 de Inventario). Revisar si `fix/account-not-found-gate` sigue haciendo falta o contradice #193, y mergear o cerrar |
> | 3 | Flags apagados (`SECTIONS_SYNC_ENABLED`, `ROADMAP_BY_GROUP_ENABLED`) | Infra | Encenderlos en los entornos de la mesh y de la demo |
> | 4 | IDs de mock en rutas reales (`DEMO_STUDENT_ID`, `COURSE_SEED_ID`, `CURRENT_STUDENT_ID`) | Front | Tomar el alumno y el curso de la sesión y de la ruta. Sin usuario, error en vez de un respaldo silencioso |

## P1: HU marcadas Done que no lo están

| HU | Falta | Capa |
|---|---|---|
| HU-44 | Selector de comisión en el roadmap y manejo del motivo `group_restricted` | Front |
| HU-48 | Endpoint de pre-chequeo para el alumno (JWT, sin `studentId` en el path). Borrar `startChallenge` | Back |
| HU-46 | Página Templo (material agrupado por unidad), o redefinir el CA con el PO | Front |
| HU-01 / HU-41 | Campo `reintentos_permitidos` (0..PAR-13). Corregir el PUT que resetea `lives_policy`. Consumir la baja de desafío del Motor (CA8) | Back |
| HU-01 | Guardar las posiciones del grafo (`moveNode` devuelve 501) | Front + Back |
| HU-20 / HU-21 | Implementar o quitar del catálogo `SECTION_NO_LIVES_LOST`, `NODE_NO_RETRIES` y `LIFE_RECOVERED`. Edición y baja de insignias en el front | Back + Front |
| HU-15 / HU-16 | Motivo `origen_no_disponible`. Último dato de 24 h con `stale` en el gate | Back |
| HU-43 | Validar que el ícono solo aplique a DESAFIO/EXAMEN | Back |
| HU-22 | Modo solo lectura de `GenericBadgeShowcase` (ui-kit#59) | Front + UI-KIT |
| HT-11 | Actualizar el texto de Taiga a snake_case v8 | Taiga |

## P2: HU en New (comprometidas)

| HU | Estado |
|---|---|
| HU-45 Ranking y avance por comisión | El back está mayormente hecho. El front no tiene nada |
| HU-49 Restricciones de Courses | El back aplica la fecha. Falta HIDDEN/LOCKED, el evento de cambio y el aviso. El front no tiene nada. Bloqueada por G01 |

## P3: limpieza

- Front: sacar el adapter in-memory y el seed del árbol de producción (dejarlos solo para tests). Unificar `level-curve.ts`. Pasar `BankDataPort` a HTTP.
- Back: borrar los `@DefaultValue("stub")` y el listener legado v1/v2.
- HT-08: versionar los GLB optimizados o documentar el pipeline.
- HU-51: revisar que el mundo Luna esté completo.

> [!tip] Solapamiento con la épica nueva
> Varios de estos puntos (HU-01/41, posiciones del grafo, HU-44/45) **se solapan con la épica de múltiples roadmaps** ([03](03-requerimientos-profes.md)). Conviene resolverlos dentro de ella y no por separado.
