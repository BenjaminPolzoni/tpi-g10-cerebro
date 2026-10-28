# Implementación para coordinar bien (back `tpi-roadmap`)

Change: [[proposal|editor-grafo-unificado]] · Fuente: [[design]] (§ Contrato con el back), [[tasks]] (T-16). Creada 2026-10-28.

El front (rama `BenjaminPolzoni/fix-vista-y-uso-del-roadmap-en-el-mapa-de-nodos`) no necesita endpoints nuevos: usa los que ya existen. Lo de acá es lo que hay que **confirmar o completar en el back** para que el editor no dependa de suposiciones. Se hace después o se deja a medio; el front no se bloquea por esto salvo donde se indica.

Back localizado: `~/dev/TPI_2026/Backend/tpi-roadmap`.

## 1. Bloqueantes suaves (el front los usa ya; confirmar antes de la PR)

- [ ] **Reglas de sección para subsecciones** — `PATCH /sections/{id}/rules` con una sección hija (`parentSectionId != null`) en todos los entornos (local, mesh, prod). Lo usa T-05b/T-06d. Pregunta abierta del [[design]].
- [ ] **Hoja `NODE` en regla de sección** — `PATCH /sections/{id}/rules` con `{rule}` (árbol) que contenga una hoja tipada `NODE` de un nodo externo. Verificar `RuleLeafEligibility.requireEligibleForSection` (`:73-85`) y que el flat `prerequisiteSectionIds` no la acepte. Lo usa T-05b.
- [ ] **Bloqueo del alumno con hojas `NODE` en reglas de sección** — el progreso del alumno (`GET .../students/{id}/progress`, `unit_prerequisite_pending`) debe bloquear una unidad/subsección cuya regla `{rule}` exige un NODO no completado. El front (`domain/unlock-rules.ts`: `unitLockOf`/`pendingUnitPrerequisites`) hoy solo mira `prerequisiteSectionIds` y XP y depende del back para esto. Detectado en T-14 (2026-10-28).
- [ ] **Códigos de error estables** — que cada rechazo de la tabla del design salga con `code` de dominio (no solo `detail`): `node.prerequisite-cycle`, `node.prerequisite-duplicate`, `node.prerequisite-out-of-scope`, `section.prerequisite-cycle`, `section.prerequisite-containment`, `section.too-deep`, `rule.*`, `course.archived`, `node.section-invalid`, `node.order-conflict`. El front traduce por código.

## 2. Verificaciones T-16 (gaps posibles → backlog back)

| Punto | Dónde mirar | Qué esperar | Estado |
|---|---|---|---|
| `minXp` fraccionario / no entero | `RuleDto.java`, `RuleTreeValidator.java` | `400 rule.*` estable | verificar |
| Hoja a nodo/sección eliminado u oculto | `GraphService` (reglas), equivalentes de sección | `400 node.prerequisite-invalid` / `409 ...out-of-scope`; mismo trato para secciones | verificar |
| Concurrencia (dos profes editando) | mutaciones de `GraphService` | versión/lock o `409` inequívoco; hoy el front solo relee al volver el foco | verificar |
| Profundidad de árbol de reglas = 5 | config de `rule.too-deep` | máximo 5 en todos los entornos | verificar |
| Mover contenido con `contentId` | `GraphService.java:655-665`, `GraphValidator.java:244-291` | rechazo con código accionable si el destino no es elegible | implementado, confirmar código |

Si algún punto no tiene control en el back: abrir tarea back con status/código estable + test. Ninguna regla puede quedar protegida solo por el front.

## 3. Fuera de este change (historias aparte, empiezan por el back)

- **F9 — Tipos de relación creados por el profesor** y relaciones informativas en el editor (`recommends`, `belongs_to`, `part_of`, `related_to`). Hoy el editor no las toca (Enmienda 1).
- **Posición manual de los marcos** (punto 11 del backlog): requiere persistir layout por sección.
- **Endpoint transaccional crear nodo + regla**: hoy son dos llamadas (`POST .../nodes` y `PATCH .../rules`) y el front reporta fallo parcial. Si molesta en la práctica, un endpoint atómico lo resuelve.

## 4. Coordinación

- El front llama siempre por `RoadmapStore` → `HttpRoadmapAdapter` (`/api/roadmap/...`). No cambia contratos.
- Si el back cambia algún código de error o shape de `{rule}`, avisar antes: rompe la traducción de mensajes y T-05b.
- Al cerrar los puntos de §1 y §2, marcar aquí y en `state.yaml`.
