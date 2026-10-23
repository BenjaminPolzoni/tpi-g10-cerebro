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
- Mostrarlo **solo si la torre es un desafío práctico real** (`activity.type === 'practical-challenge' && activity.challengeId`). D2 resuelto: los teóricos no lo llevan, porque el alumno ya los puede releer y ver sin límite.
- `hex-world-page.component.ts`: método `viewAttempts(t)`:
  1. `audio.playClick()`
  2. guardar la pose con `saveReturnPosition(...)`, igual que en `openChallenge`, para que al volver el barco y el personaje queden en la torre
  3. `router.navigate(['/attempts'])`
  
  **No toca `challengeAttempts`.**
- Repetir queda **tal cual** (punto 2 del issue).
- i18n `es.json` / `en.json`, bloque `hexWorld`: `"viewAttempts": "Ver mis intentos"` / `"View my attempts"`.

### F2. El diálogo respeta la misma decisión que la torre (punto 3)
- `npc-dialogue.ts`, rama `ctx.challenge === 'practical' && ctx.passed` (hoy solo tiene «Chau»): sumar la opción `{ id: 'attempts', label: t(i18n, 'viewAttempts') }`. El teórico superado queda como está (D2).
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

### F6. Popup «Ver feedback» con el resumen de Motor
Solo para un **práctico real superado**. Consume **solo Motor** (sección 5.1) y nunca llama a Prácticos ni a `ChallengeAttemptService`.

**Relación con F1/F2:** si F6 entra en el mismo PR, el botón de la torre pasa a ser **«Ver feedback»** (abre el popup) y «Ver mis intentos» queda como link dentro del popup. La opción del diálogo (F2) también abre el popup. Si F6 va en otro PR, F1 queda como está hasta entonces.

**1. Data: `data-access/challenge-attempt/node-feedback.service.ts`** (al lado de `challenge-attempt`, con `HttpGenericService.get`, mismo patrón que `my-attempts.service.ts`)
- Tipos en el mismo archivo, en snake_case tal como llegan (solo los campos que se usan):
  - `NodeCountedAttempt { state, counted_attempt_id, counted_score, verdict, attempts_left }`
  - `AttemptFeedbackSummary { feedback_state, summary_items: { severity, message, code, file, line }[] }`
- `countedAttempt(courseId, nodeId, challengeId)` → `GET /engine-challenge/courses/{courseId}/students/me/nodes/{nodeId}/challenges/{challengeId}/counted-attempt`
- `summary(attemptId)` → `GET /engine-challenge/attempts/{attemptId}/summary`, con el header `Accept-Language: i18n.lang()` puesto en esta llamada. El `acceptLanguageInterceptor` de core solo cubre `/tutor/` y **no se toca**, porque core es compartido.
- Ningún POST.

**2. Página: `hex-world-page.component.ts`**
- Signal `feedback = signal<{ tower; status: 'loading' | 'ready' | 'error'; counted?; summary? } | null>(null)`.
- `viewFeedback(t)`:
  1. pone `loading`
  2. llama a `countedAttempt(...)`
  3. si `state === 'COUNTED'` y hay `counted_attempt_id`, llama a `summary(id)`
  4. pone `ready`
  
  Ante cualquier error pone `error`. **Nunca cae a abrir un intento.**
- `closeFeedback()` pone `null`.
- `openReview()`: guarda la pose (`saveReturnPosition`) y navega a `/attempts/{counted_attempt_id}/review`. `viewAttempts()` (F1) sigue para el link «Ver todos mis intentos».

**3. Template: un bloque nuevo `@else if (feedback(); as fb)`** con `<aside class="hud-panel hud-panel-center">`, mismo patrón que el panel `challenge()`, sin modal nuevo.
- `loading` → `generic-skeleton`.
- `error` → `generic-callout` con `hexWorld.feedback.error` + botón «Reintentar lectura» (vuelve a llamar a `viewFeedback`, **no** abre un intento) + «Cerrar».
- `ready`, según `counted.state`:
  - `COUNTED` → nota (`counted_score`) y veredicto (`PASSED`/`FAILED`), y abajo según `summary.feedback_state`:
    - `AVAILABLE` → hasta 3 hallazgos (`severity` + `message`, con `file:line` si viene). `message` ya llega en el idioma pedido.
    - `WITHHELD_BY_POLICY` → «La devolución se publica cuando cierre el desafío».
    - `NOT_CORRECTED` → «Todavía no está corregido».
    - `TEMPORARILY_UNAVAILABLE` → «La devolución no está disponible ahora» (la nota sí se muestra).
    - `NO_HISTORICAL_REFERENCE` → «Resultado no disponible».
    - `NOT_PRACTICAL` → no debería pasar; mismo texto que el anterior.
  - `IN_PROGRESS` → «Tenés un intento en curso».
  - `PENDING_CORRECTION` → «Tu entrega está esperando la corrección».
  - `NO_RESULT` → «El intento cerró sin resultado».
  - `NO_ATTEMPTS` y `NO_HISTORICAL_REFERENCE` → «Resultado no disponible».
- Acciones: «Ver revisión completa» (solo con `COUNTED`), «Ver todos mis intentos» y «Cerrar».

**4. «Repetir» según Motor (F6b, opcional)**
- Al acercarse a una torre práctica superada, pedir `countedAttempt` una vez (cachearlo por nodo en un `Map` de la página) y ocultar «Repetir» si `attempts_left === 0`.
- Cuando G09 agregue la opción «repetible sin límite» (5.2.1), usar ese dato en lugar de `attempts_left`.

**5. i18n `es`/`en`:** bloque `hexWorld.feedback.*` con `title`, `score`, `verdict.PASSED`, `verdict.FAILED`, `state.<cada feedback_state y cada estado del nodo>`, `error`, `retryRead`, `fullReview`, `allAttempts` y `close`.

**6. Tests**
- `node-feedback.service.spec.ts` (con `HttpTestingController`): las dos URLs, el header `Accept-Language` en `summary` y que no haya ningún POST.
- `hex-world-page.component.spec.ts`:
  - si la lectura falla, se muestra el error y `ChallengeAttemptService.open` **no** se llama
  - `COUNTED` + `AVAILABLE` → se ven 3 hallazgos
  - `NO_HISTORICAL_REFERENCE` → «resultado no disponible»
- Prueba manual: hace falta que el Motor del entorno donde se pruebe tenga el `develop` del 19/10 o posterior (PR #321 y #322).

### Tests front (solo los pertinentes)
- `npc-dialogue.spec.ts`: torre superada con desafío real → aparece la opción `attempts`. Torre local → no aparece.
- `hex-world-page.component.spec.ts`: `viewAttempts` navega a `/attempts` y **no** llama a `ChallengeAttemptService.open` (spy). Repetir sigue llamando a `open`.
- Si se hace F3: el spec de `roadmap-section-nodes` para un nodo completado.
- Correr con `NODE_OPTIONS=--no-experimental-webstorage` (Node 25).

## 3. Plan Back (rama `BenjaminPolzoni/issue-270-feedback-alumno`)

### B1. No descartar el cierre de un nodo ya superado (punto 4)
- `ProgressService.recordResult`: **sacar el `throw`** de `node.already-passed`. Se mantiene `alreadyPassed` para la guarda que ya existe (`result.passed() && !alreadyPassed`). Así el movimiento se registra y solo se omiten el completado, `NODE_COMPLETED`, el desbloqueo por prerrequisito y el día de actividad.
- XP según **D1 (resuelto el 23/10)**:
  - **Reintento de un nodo desaprobado** (no está en `completed_nodes`): **da XP**, como hoy. No se toca.
  - **Repetición de un nodo ya aprobado** (`alreadyPassed`): **no da XP**. El movimiento se guarda con `xp = 0` (queda la traza del intento), no suma a `total_xp` y no dispara `recordXpUnlocks`. Roadmap lo fuerza aunque Motor mande XP. Dejarlo explícito en el javadoc.
- Limpieza: si `node.already-passed` queda sin uso, quitarlo de `RoadmapErrorCode`, `ErrorCatalog` (`:150`), `messages.properties` (`:55`) y `docs/api_doc/swagger.json`.

### Tests back
- `ChallengeResultListenerTest` (ya cubre `recordResult` y `completedNodes`): un segundo evento aprobado sobre un nodo ya completado → hay movimiento con su `event_id`, sigue habiendo **un solo** completado, **no** hay un segundo `NODE_COMPLETED` en el outbox y el XP queda según D1.
- Correr solo esa clase.

## 4. Decisiones abiertas

| # | Decisión | Default si nadie responde |
|---|---|---|
| D1 | ¿Repetir da XP? | **Resuelto (23/10):** el reintento de un nodo desaprobado da XP; la repetición de un nodo aprobado no da XP |
| D2 | ¿«Ver mis intentos» también en los teóricos? | **Resuelto (23/10):** no. El teórico ya se puede releer y ver sin límite |
| D3 | Fechas para responder en el issue | Pendiente (Benja) |

## 5. Motor (G09): qué ya está y qué falta pedir

> [!warning] Actualización 23/10
> G09 ya cerró el issue de G05 (`tpi-engine-challenge#316`, cerrado el 19/10) y **mergeó en `develop`** los PR #318, #321, #322 y #325. Gran parte de lo que el hilo del #270 daba como «bloqueado por Motor» **ya existe**.

### 5.1 Ya disponible en Motor: para qué lo usamos

| Endpoint / dato | Para qué en Roadmap |
|---|---|
| `GET /courses/{courseId}/students/me/nodes/{nodeId}/challenges/{challengeId}/counted-attempt` (#321) → `state`, `counted_attempt_id`, `counted_score`, `verdict`, `attempts_used`, `attempts_left` | Saber **qué intento representa el nodo**. Con `counted_attempt_id` enlazamos directo a `/attempts/:id/review` (sin pasar por `/attempts`). Con `attempts_left = 0` dejamos de ofrecer «Repetir». `NO_HISTORICAL_REFERENCE` → «resultado no disponible». `IN_PROGRESS` / `PENDING_CORRECTION` → estados visibles en la torre. |
| `GET /attempts/{attemptId}/summary` (#322) → resultado + hasta 3 hallazgos + `feedback_state` | El **popup definitivo** de «Ver feedback», con un texto ES/EN por cada `feedback_state` (`AVAILABLE`, `WITHHELD_BY_POLICY`, `NOT_CORRECTED`, `NO_HISTORICAL_REFERENCE`, `TEMPORARILY_UNAVAILABLE`, `NOT_PRACTICAL`). |
| `GET /attempts/{attemptId}/review` (#322) | Destino del enlace «Revisar» (es la misma pantalla de G05). Ya no hace falta `?challengeId=`. |
| `counted_score` como nombre único (#325) | El nombre de la nota en el popup. |
| Reenvío de `Accept-Language` a Prácticos (#322) | Que el feedback llegue en el idioma de la UI. **Falta que el front lo mande** (core del front, no es de Motor). |

➡️ Con esto el popup ya **no está bloqueado**: está detallado en **F6**.

### 5.2 Lo que todavía hay que pedirle a G09

1. **Opción del profesor «repetible sin límite una vez aprobado».** No existe: `ChallengeSettings` solo tiene `retries`/`cooldownMinutes`, y `attempts_left = 1 + retries − usados`.
   - **Para qué:** mostrar «Repetir» en un nodo aprobado aunque `attempts_left = 0`, y que Motor no rechace con `attempts-exhausted`.
   - **Qué pedir:** la opción en la configuración del desafío y un dato en `counted-attempt` que diga si se puede repetir (por ejemplo, `can_repeat`), así Roadmap no deduce nada.
2. **Que la repetición después de aprobar no cambie la nota ni consuma reintentos.**
   - **Para qué:** con la regla `LAST`, una repetición peor bajaría la nota que cuenta, y en ese caso repetir sería un castigo. Tampoco tiene que gastar intentos `NORMAL`.
3. **Que la repetición después de aprobar no premie desde Motor.** Que mande `xp = 0` y sin monedas, o que el evento `CHALLENGE_COMPLETED` la marque (por ejemplo, `result.post_pass_repeat`).
   - **Para qué:** Roadmap ya fuerza XP 0 con `alreadyPassed` (B1), pero las **monedas** las acredita Contabilidad con el evento de Motor. Si Motor no lo marca, el alumno cobra monedas cada vez que repite.
4. **Confirmar los slugs de rechazo:** `attempts-exhausted` y `attempt-cooldown-active` (ya mapeados en `failureKey`).
   - **Para qué:** que el mensaje de «Repetir» rechazado sea claro (criterio de aceptación del #270).
5. ~~Confirmar la ruta por el gateway de `counted-attempt`.~~ **Verificado (23/10):** el controller usa `${app.api.private-path}`, así que desde el front es `/engine-challenge/courses/.../counted-attempt`, igual que `/engine-challenge/attempts/me`.

## 6. Fuera de alcance
- `Accept-Language` desde el front (core del front, lo coordina quien lo mantiene).
- Retirar las torres con quiz local (lo decide el grupo).

## 7. Orden de trabajo recomendado
1. **Back (B1) primero.** Es chico (sacar el `throw`, XP 0 si `alreadyPassed`, un test) y no depende de nadie. Además es el único **bug que hoy pierde datos**: cada cierre sobre un nodo aprobado se descarta entero. Sale en un PR corto y se revisa mientras se hace el front.
2. **Front** en este orden: F1 → F2 → F5 → F6 (+ F6b) → F3 → F4. F1/F2 son la base, F6 se monta encima, y F3/F4 tienen más incertidumbre (F3 requiere verificar si el alumno ve la lista; F4 puede romper lo offline).
3. El front **no depende** del back: el popup y los botones leen de Motor. Los dos PR se pueden mergear en cualquier orden.

## 8. Cierre
- PR del front y PR del back por separado, cada uno con `Refs 2026-P4-BE/tpi-roadmap#270`.
- Comentar en el #270 con las fechas (D3) y avisar cuando esté en `develop`, como pidió G05.
- Checklist de aceptación del issue:
  - [ ] Acceso a la revisión, separado de Repetir (F1, F3)
  - [ ] Ninguna acción de feedback hace el POST (tests de F1 y F2)
  - [ ] Todos los puntos de entrada respetan la misma decisión (F1, F2, F3)
  - [ ] ES/EN
  - [ ] Rechazo claro (F5)
