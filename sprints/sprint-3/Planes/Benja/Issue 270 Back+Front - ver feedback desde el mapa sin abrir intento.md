---
tags: [tpi, g10, sprint-3, plan, resolver-issue, front, back, mapa, feedback]
fecha: 2026-10-22
autor: Benja
estado: borrador
repo: 2026-P4-FE/2026-PIV-TPI-FE + 2026-P4-BE/tpi-roadmap
issue: https://github.com/2026-P4-BE/tpi-roadmap/issues/270
taiga: sin tarea en Taiga
---

# Issue #270 — Feedback del alumno: revisión desde el mapa sin abrir un intento

> [!info] Contexto
> G05 (Brizuela) abrió el issue #270 en `tpi-roadmap` el 18/10 a partir del acuerdo de feedback al alumno entre G05, G09 y G10. Iker respondió en nombre de G10 qué tomamos (puntos 1 a 4) y qué queda bloqueado por Motor (G09). G05 aceptó y pidió las **fechas**, que quedaron en blanco. Este plan cubre **solo lo que ya asumimos**. El popup definitivo con el resumen de Motor queda afuera hasta que G09 publique el contrato.
>
> Regla de oro del acuerdo: **"Ver feedback" / "Ver mis intentos" nunca abre un intento** (no pasa por `ChallengeAttemptService.open` ni por el `POST /intentos`).

Es **Back + Front**: el front lleva los puntos 1 a 3 y el back el punto 4. Son independientes y van en PR separados.

## Worktrees

| Repo | Ruta | Rama | Base |
|---|---|---|---|
| Front | `~/dev/TPI_2026/Frontend/2026-PIV-TPI-FE-issue-270` | `feature/issue-270-feedback-alumno` | `origin/develop` `a286d97f9` (sin upstream, sin `node_modules`) |
| Back | `~/orca/workspaces/tpi-roadmap/issue-270-feedback-alumno` (ya existía, de Orca) | `BenjaminPolzoni/issue-270-feedback-alumno` | `origin/develop` `ce95104e` |

## 1. Estado actual (verificado en `develop` el 22/10)

| Qué | Dónde | Hallazgo |
|---|---|---|
| Torre superada | `hex-world-page.component.html:~546-552` | Solo muestra «Torre superada» + **Repetir** → `openChallenge(t, true)` → si es un desafío real, `challengeAttempts.open` (gate + `POST /intentos`). No hay acción de feedback. |
| `openChallenge` | `hex-world-page.component.ts:1443` | Guarda la pose (`saveReturnPosition`, `:1473`) y abre el intento real, o el quiz local si la torre no tiene `challengeId`. |
| Diálogo con el personaje | `domain/npc/npc-dialogue.ts:261-280` | Práctico superado: solo «Chau», no abre nada. Teórico superado: la opción `go` con la etiqueta «Reintentar» → `departTo` (`hex-world-page.component.ts:1571`) → `openChallenge(tower, true)`. **Es una elección explícita** (equivale a Repetir), pero no ofrece «Ver mis intentos». |
| Teclado | — | La E solo abre el diálogo o el mercado; no abre torres (ya se lo corregimos a G05). |
| Lista de nodos embebida | `embeds/section-nodes/roadmap-section-nodes.component.html:~84-91` → `section-resources-container.component.ts:107` | El título de un nodo con `challengeId` emite `openChallenge` → `attempts.open(...)`. **No sabe si el nodo está completado**: un nodo superado abre un intento nuevo con un clic sobre el título. |
| Rechazo de Motor | `data-access/challenge-attempt/challenge-attempt.service.ts:95-98` (`failureKey`) | Ya mapea `attempts-exhausted` → exhausted y `attempt-cooldown-active` → cooldown, más 503 y genérico. **Falta que Motor confirme los slugs**: si cambian, solo se toca `failureKey`. |
| «Superado» | `hex-world-page.component.ts:686-692`, `mergeWithCompleted` `:1644` | Une las marcas locales (`VisitService`) con `store.completedNodeIds()` para **todas** las torres. Si una torre real cae al quiz local (por ejemplo, porque `activityOf` todavía no cargó), queda marcada como superada sin el back. |
| Ruta de intentos | `app.routes.ts:101` → `features/challenges/attempts.routes.ts` | `/attempts` (mis intentos, con «Revisar» en prácticos corregidos) y `/attempts/:attemptId/review`. |
| Back: cierre sobre nodo ya superado | `tpi-roadmap/.../services/ProgressService.java:~141-144` | `if (alreadyPassed) throw new NonRetryableEventException("node.already-passed")` **antes** de `insertMovement`, así que un intento posterior se descarta entero (movimiento, XP, insignias). El bloque de completado ya tiene la guarda `result.passed() && !alreadyPassed`. |
| Gate | `GateController` | No rechaza nodos completados, así que «Repetir» llega a Motor y Motor decide. OK. |

## 2. Plan Front (rama `feature/issue-270-feedback-alumno`)

### F1. «Ver mis intentos» en la torre superada
- `hex-world-page.component.html`, rama `@else` (torre superada): agregar al lado de Repetir un botón `variant="secondary"` con `{{ 'hexWorld.viewAttempts' | t }}` → `viewAttempts(nearTower()!)`.
- Mostrarlo **solo si la torre es un desafío real** (`activityOf(id)?.challengeId`). Una torre local no tiene intentos en Motor (ver D2 para prácticos y teóricos).
- `hex-world-page.component.ts`: método `viewAttempts(t)`:
  1. `audio.playClick()`
  2. guardar la pose con `saveReturnPosition(...)`, igual que en `openChallenge`, para que al volver el barco y el personaje queden en la torre
  3. `router.navigate(['/attempts'])`
  
  **No toca `challengeAttempts`.**
- Repetir queda **tal cual** (punto 2 del issue).
- i18n `es.json` / `en.json`, bloque `hexWorld`: `"viewAttempts": "Ver mis intentos"` / `"View my attempts"`.

### F2. El diálogo respeta la misma decisión que la torre (punto 3)
- `npc-dialogue.ts`, ramas `ctx.passed` (práctico y teórico): sumar la opción `{ id: 'attempts', label: t(i18n, 'viewAttempts') }`, solo si el desafío es real (sumar `ctx.realChallenge` o equivalente al contexto que ya se arma).
- `NpcAction`: agregar `'attempts'`.
- `hex-world-page.component.ts` `onTalkChoice`: `id === 'attempts'` → `closeTalk()` + `viewAttempts(tower)`.
- `go` («Reintentar») sigue yendo a `departTo` → `openChallenge(tower, true)`. Ya es una elección explícita y equivale a Repetir.
- i18n del diálogo, `es` y `en`: clave `viewAttempts`, en el mismo bloque donde están `retry` y `toQuiz`.

### F3. Lista de nodos embebida (`roadmap-section-nodes`)
- **Verificar primero** si el alumno la ve. Si es solo del docente, no hay nada que hacer y se anota.
- Si el alumno la ve: pasarle los completados (`RoadmapStore.completedNodeIds()` o un input `completedIds`). Para un nodo completado con `challengeId`, el título deja de abrir el intento y se muestran dos acciones explícitas: **Repetir** (emite `openChallenge`, como hoy) y **Ver mis intentos** (`router.navigate(['/attempts'])`).

### F4. «Superado» de una torre real solo desde el back (si no complica lo offline)
- En `passedIds`, ignorar las marcas locales de las torres cuya actividad tiene `challengeId`. Para ellas cuenta solo `store.completedNodeIds()`. Las torres de quiz local siguen usando `VisitService` y la isla se sigue jugando offline.
- Si rompe el modo offline, sacarlo a un PR aparte (lo dijimos así en el issue).

### F5. Rechazo de Motor al repetir
- Ya está. Solo queda **confirmar los slugs** con G09 (`attempts-exhausted`, `attempt-cooldown-active`) y ajustar `failureKey` si son distintos. Verificar que las claves de i18n de exhausted/cooldown existan en `es` y en `en`.

### Tests front (solo los pertinentes)
- `npc-dialogue.spec.ts`: torre superada con desafío real → aparece la opción `attempts`. Torre local → no aparece.
- `hex-world-page.component.spec.ts`: `viewAttempts` navega a `/attempts` y **no** llama a `ChallengeAttemptService.open` (spy). Repetir sigue llamando a `open`.
- Si se hace F3: el spec de `roadmap-section-nodes` para un nodo completado.
- Correr con `NODE_OPTIONS=--no-experimental-webstorage` (Node 25).

## 3. Plan Back (rama `BenjaminPolzoni/issue-270-feedback-alumno`)

### B1. No descartar el cierre de un nodo ya superado (punto 4)
- `ProgressService.recordResult`: **sacar el `throw`** de `node.already-passed`. Se mantiene `alreadyPassed` para la guarda que ya existe (`result.passed() && !alreadyPassed`). Así el movimiento se registra y solo se omiten el completado, `NODE_COMPLETED`, el desbloqueo por prerrequisito y el día de actividad.
- XP del reintento según **D1**:
  - (Recomendado, propuesta de G05) Se usa el `result.xp()` que manda Motor, porque Motor aplica la regla de nota que cuenta y la penalización por reintento.
  - Si el grupo decide que repetir no da XP: cuando `alreadyPassed`, guardar el movimiento con `xp = 0` y no sumar a `total_xp`. Dejarlo explícito en el javadoc.
- Limpieza: si `node.already-passed` queda sin uso, quitarlo de `RoadmapErrorCode`, `ErrorCatalog` (`:150`), `messages.properties` (`:55`) y `docs/api_doc/swagger.json`.

### Tests back
- `ChallengeResultListenerTest` (ya cubre `recordResult` y `completedNodes`): un segundo evento aprobado sobre un nodo ya completado → hay movimiento con su `event_id`, sigue habiendo **un solo** completado, **no** hay un segundo `NODE_COMPLETED` en el outbox y el XP queda según D1.
- Correr solo esa clase.

## 4. Decisiones abiertas

| # | Decisión | Default si nadie responde |
|---|---|---|
| D1 | ¿Repetir un nodo superado da XP? (G05 propone que lo decida Motor) | Usar `result.xp()` de Motor |
| D2 | ¿«Ver mis intentos» también en las torres teóricas o solo en las prácticas? (Iker se comprometió a los prácticos; `/attempts` lista los dos) | Mostrarlo en cualquier desafío real |
| D3 | Fechas para responder en el issue (puntos 1 a 3 y punto 4) | Definirlas antes de responder |

## 5. Fuera de alcance (bloqueado por Motor / G09)
- Popup con el resumen de Motor: nota que cuenta, veredicto, hasta tres hallazgos y los estados de `feedback_state`.
- Mostrar «Repetir» solo cuando `attempts_left > 0` (G05 confirma que Motor ya expone `attempts_left`; falta el resumen por nodo).
- Enlace directo a `/attempts/:attemptId/review?challengeId=` (Roadmap no guarda el `attemptId`).
- `Accept-Language` (core del front, lo coordina quien lo mantiene).
- Retirar las torres con quiz local (lo decide el grupo).

## 6. Cierre
- PR del front y PR del back por separado, cada uno con `Refs 2026-P4-BE/tpi-roadmap#270`.
- Comentar en el #270 con las fechas (D3) y avisar cuando esté en `develop`, como pidió G05.
- Checklist de aceptación del issue:
  - [ ] Acceso a la revisión, separado de Repetir (F1, F3)
  - [ ] Ninguna acción de feedback hace el POST (tests de F1 y F2)
  - [ ] Todos los puntos de entrada respetan la misma decisión (F1, F2, F3)
  - [ ] ES/EN
  - [ ] Rechazo claro (F5)
