---
tags: [tpi, g10, sprint-4, plan, front, roadmap, gate, resiliencia]
fecha: 2026-10-27
autor: Benjamin Polzoni
estado: borrador
repo: 2026-PIV-TPI-FE
base: origin/develop 6d4efb5b0 (2026-10-27)
antecedentes: HT-31 (T-31.1 origin_unavailable, T-31.4 vidas vencidas, T-31.6 pre-chequeo), HU-48, DEC-003 (fail-closed)
---

# Front · Mensajes y reintentos ante `origin_unavailable`

> [!info] Alcance
> Revisar qué ve el alumno cuando el gate responde `origin_unavailable` y cómo puede reintentar. Ese motivo significa que Accounting o Courses no respondieron y no hay un dato vigente. Hoy el front lo muestra como un bloqueo más, igual que "te falta un nodo", cuando en realidad es una **falla pasajera**. Es un cambio sólo de front: el back no cambia. Es una propuesta; todavía no hay código.

## 1. Qué hay hoy (verificado en `origin/develop`)

**Back (`tpi-roadmap`), para tener el contexto:**

- `GateService.evaluate` (`:90-103`) atrapa cualquier 503 de Accounting o Courses y lo convierte en un **200** con `eligible=false, reason=origin_unavailable`, nunca en un 503 (contrato `roadmap-motor-gate-v1` §4, v1.4).
- Las vidas pasan por la caché corta de `HttpInventoryClient`, de 30 s. Si Accounting se cae, el gate sigue habilitando hasta que esa caché vence, y desde ahí responde `origin_unavailable` (`GateStaleLivesTest`). La pantalla de inventario muestra igual el último dato, marcado como `stale`.
- El progreso (`NodeProgressService`) **no** atrapa el 503. Si Accounting o Courses no responden al leer el mapa, falla la lectura entera, y en el mapa casi nunca aparece un nodo con `origin_unavailable`. Marcar un material como leído con Courses caído responde **503**, no un motivo (`GroupGateTest:262`).

**Front (`2026-PIV-TPI-FE`):**

- El motivo **ya es parte del vocabulario**. Está en `GATE_REASONS` (`challenge-attempt.service.ts:47-60`), en `KNOWN_BLOCK_REASONS` (`roadmap-mapper.ts:701-714`) y en `labels.ts:102`, y tiene textos en es/en/pt: `attemptGate.origin_unavailable` y `roadmapLabels.blockReason.origin_unavailable`.
- **Pre-chequeo** (`evaluateGate`, `:~530`): consulta `/roadmap/courses/{id}/nodes/{nodeId}/eligibility` con un `timeout` de 3 s. Si el pre-chequeo **no se pudo consultar** (red, timeout), devuelve `null` y el intento se le pide igual al Motor, que vuelve a evaluar el gate. Pero si **sí respondió** con `origin_unavailable`, se trata como un bloqueo definitivo: `showBlocked`, un toast `info` con el texto "🔒 No pudimos verificar…", y en los desafíos prácticos se sale de la pantalla de preparación (`leavePreparing`). Al Motor no se le pide nada y no hay botón para reintentar.
- **Rechazo del Motor** (`403 student-not-eligible` con `reason`): se muestra igual. En un práctico, la falla aparece en la pantalla de preparación (`handoff.fail`), que **sí tiene reintentar**, y ese reintento repite sólo el pedido al Motor, que vuelve a evaluar el gate. En un teórico aparece un toast, sin reintentar.
- **Unidad bloqueada** (`unlock-rules.ts`, `byReason` `:~575`): `origin_unavailable` no tiene entrada y cae en `nextStep.generic`, que dice "Abrí las unidades anteriores y completá sus nodos obligatorios…". Para una caída es **un consejo equivocado**.
- **Mapa sin progreso:** el HUD ya ofrece reintentar cuando no se pudo leer el progreso (`roadmap.store.ts:363-390`). No hay reintentos automáticos en interceptores ni en `core`.

## 2. Problemas

1. **El pre-chequeo frena de más.** El pre-chequeo es una cortesía: la decisión real es la del Motor. Un `origin_unavailable` del pre-chequeo quiere decir "no pude verificar", igual que un timeout. Sin embargo, el timeout deja seguir y `origin_unavailable` corta.
2. **El tono es de bloqueo.** El candado 🔒 y el toast `info` le dicen al alumno que no tiene acceso. En realidad es una falla de un servicio y se arregla sola.
3. **No hay forma de reintentar** cuando el bloqueo viene del pre-chequeo, ni en teóricos ni en prácticos. El alumno tiene que adivinar que puede volver a hacer clic.
4. **La unidad bloqueada da un consejo equivocado** (`nextStep.generic`).
5. El texto dice "Probá en unos minutos", pero la caché de vidas se renueva cada 30 s y un parpadeo de Courses dura segundos. "En unos instantes" se ajusta más.

## 3. Decisiones (a confirmar)

| # | Decisión | Recomendación |
|---|---|---|
| D1 | ¿Qué hace el pre-chequeo con `origin_unavailable`? | Tratarlo **como un pre-chequeo no consultable**: devolver `null` y pedir el intento al Motor, que es el que decide. Si el Motor también rechaza con `origin_unavailable`, se usa el camino que ya existe para los rechazos del Motor (pantalla de preparación con reintentar en prácticos, toast en teóricos). No se consume vida, porque el Motor evalúa el gate antes de crear el intento. **Verificar** esto con el contrato §9 antes de cerrar la decisión. |
| D2 | ¿Reintento automático? | **No.** No sumar `retry` ni polling. Un intento consume vidas y la idempotencia del Motor no está garantizada (lo dice el comentario de `reattach`). Alcanza con los reintentos manuales que ya existen. |
| D3 | ¿Reintentar en teóricos? | **No por ahora.** `ToastService` no tiene acciones y sumarlas es cambiar `core`. El texto nuevo invita a volver a hacer clic. Si el equipo lo pide, se suma después como tarea propia. |
| D4 | Tono del mensaje | Una clave propia, `attemptGate.unavailable`, **sin 🔒**, mostrada con `toast.warning` en vez de `info`. Los demás motivos siguen con `blocked` y el candado. |
| D5 | Unidad bloqueada | Agregar `origin_unavailable: 'originUnavailable'` en `byReason` y el texto `worldsPage.unitLocked.nextStep.originUnavailable`. **No** sumarlo a `IN_UNIT_REASONS`: con fail-closed (DEC-003), la unidad sigue cerrada. |

**Textos propuestos** (`attemptGate.origin_unavailable`, `roadmapLabels.blockReason.origin_unavailable`, `nextStep.originUnavailable`):

| | es | en | pt |
|---|---|---|---|
| motivo | No pudimos verificar si podés entrar: un servicio no responde. Probá de nuevo en unos instantes. | We could not check whether you can enter: a service is not responding. Try again in a moment. | Não foi possível verificar se você pode entrar: um serviço não está respondendo. Tente novamente em instantes. |
| unidad | Un servicio no responde y no pudimos verificar tu acceso. Volvé a intentar en unos instantes. | A service is not responding and we could not check your access. Try again in a moment. | Um serviço não está respondendo e não conseguimos verificar seu acesso. Tente novamente em instantes. |

## 4. Pasos

1. **Verificación previa (T1):**
   - con Accounting y después Courses apagados en la variante `polzoni`, abrir un desafío teórico y uno práctico y anotar qué responde el Motor (`403 student-not-eligible` con `reason=origin_unavailable`, u otra cosa);
   - confirmar que no se crea el intento y que no se consume una vida;
   - ver qué muestra el front al marcar un material como leído con Courses caído (503): toast genérico, o nada.
2. `challenge-attempt.service.ts` (D1): dentro de `evaluateGate`, en el `map`, si `reason === 'origin_unavailable'` devolver `null`, con un comentario que explique que "no pude verificar" equivale a "no consultable". Así, `switchMap` sigue de largo hacia el Motor sin tocar nada más.
3. `challenge-attempt.service.ts` (D4): en `showBlocked` y `describeOpenFailure`, si el motivo es `origin_unavailable`, usar `toast.warning(this.i18n.t('attemptGate.unavailable', …))` y sacar el candado. El resto queda igual.
4. `unlock-rules.ts` (D5): sumar la entrada en `byReason`.
5. `es.json`, `en.json` y `pt.json`: los textos del §3, más la clave nueva `attemptGate.unavailable` (sin 🔒, por ejemplo `"{{ reason }}"`) y `nextStep.originUnavailable`.
6. Si en T1 marcar como leído con Courses caído no muestra nada, agregar un mensaje con `failureKey` → `unavailable`. **Sólo** si hace falta.

## 5. Tests (sólo los del cambio)

- `challenge-attempt.service.spec.ts`:
  - un pre-chequeo con `origin_unavailable` **sí** llama al Motor (hoy, en `:412`/`:455`, se espera que no lo llame; esos casos cambian);
  - un rechazo del Motor con `origin_unavailable` muestra `toast.warning` sin 🔒;
  - en un práctico, el rechazo queda en la pantalla de preparación con reintentar.
- `unlock-rules.spec.ts`: una unidad bloqueada por `origin_unavailable` usa `nextStep.originUnavailable`.
- Comando: `NODE_OPTIONS=--no-experimental-webstorage npx ng test --include='**/challenge-attempt.service.spec.ts' --include='**/unlock-rules.spec.ts' --watch=false`.

## 6. Riesgos

- **D1 depende de que el Motor sea fail-closed.** Si el Motor, ante `origin_unavailable`, creara el intento o consumiera una vida, D1 abriría un hueco. Por eso T1 va primero, y si falla se vuelve al comportamiento de hoy (bloquear desde el pre-chequeo), pero con el mensaje y el tono nuevos.
- Con D1, el clic de un alumno con un servicio caído ahora también le pega al Motor. Es un pedido más por clic y no reintenta solo, así que no se amplifica.
- Fuera de alcance: cambiar el progreso del back para que devuelva `origin_unavailable` por nodo en lugar de un 503 de toda la lectura, y sumar acciones a `ToastService`.
