---
tags: [tpi, g10, sprint-3, plan, fix, roadmap, front]
fecha: 2026-10-19
autor: Benja
estado: borrador
repo: 2026-P4-FE/2026-PIV-TPI-FE
---

# Fix · Front — Orden de nodos y restricciones dentro de una unidad

> [!info] Contexto
> Dentro de una sección/unidad, un nodo solo puede tener como restricción (prerrequisito) a los nodos que están **antes** que él:
> - el 1.º no puede tener ninguna restricción;
> - el 2.º solo puede elegir al 1.º;
> - el 3.º puede elegir al 1.º y al 2.º, y así sucesivamente.
>
> Ahora el orden se cambia con drag & drop. **Cada vez que cambia el orden**, hay que desvincular solo las restricciones que quedaron mal: las de nodos que ahora están delante del nodo que los requería, o en su mismo lugar. Así nada queda bloqueado para siempre.

## 1. Worktree

- **Carpeta:** `~/dev/TPI_2026/Frontend/2026-PIV-TPI-FE-fix-orden-restricciones`
- **Rama:** `fix/roadmap-orden-restricciones-nodos`, creada desde `origin/develop` en `366042f11` (2026-10-19). Se le sacó el upstream para que un `git push` no termine en `develop`. El primer push va con `-u origin fix/roadmap-orden-restricciones-nodos`.
- **Antes de empezar:** correr `npm ci`, porque la worktree no tiene `node_modules`.

## 2. Qué hay hoy (verificado en `develop`, `366042f11`)

### Lista de nodos y drag & drop
`features/roadmap/embeds/section-nodes/roadmap-section-nodes.component.{ts,html}`
- Es drag & drop nativo de HTML5 (`draggable`, `dragstart`/`dragover`/`drop`), no usa CDK.
- `onRowDrop()` llama a `store.moveActivityTo(sectionId, draggedId, targetId, before, …)`.
- Las flechas ↑/↓ llaman a `moveNode()`, que llama a `store.moveActivity()`, que a su vez termina en `moveActivityTo`.
- `course-map-page.component.ts:529` también llama a `store.moveActivity(...)`.
- **Conclusión: todos los reordenamientos pasan por `RoadmapStore.moveActivityTo`.** Ahí va el fix, una sola vez, y cubre a todos los que lo llaman.

### Candidatos a restricción
`domain/unlock-rules.ts`
- `nodesBefore(sections, nodeId)` devuelve los nodos que están antes en la misma unidad. Para el primero devuelve `[]`.
- `nodeRuleCandidates()` ofrece esos nodos **más** los prerrequisitos que ya estaban guardados aunque hoy estén después. A esos últimos los marca `misplaced: true`: siguen habilitados para que el profe los pueda sacar a mano.
- **La regla "solo los anteriores" ya se cumple al elegir.** Lo que falla es que al reordenar, las restricciones que quedaron hacia adelante **no se borran**: quedan como `misplaced`, y el alumno puede quedar bloqueado (A requiere a B, pero B está después de A).

### Reordenar en el store y el back
- `RoadmapStore.moveActivityTo` → `port.reorderActivity` → `PATCH /nodes/{id}` con `sort_order` → `reload()`.
- **El back no poda aristas al mover.** `GraphService.moveNode` (tpi-roadmap `develop` `fd799f3`) solo corre los `sort_order` de los nodos vecinos.
- `GraphValidator.requirePrerequisitesInScope` valida el alcance de comisión, no el orden. Por eso el fix puede hacerse **solo en el front**.

### Cómo se guardan las reglas
- **Regla plana:** aristas `connections` (origen → destino) más `prerequisiteMode` del nodo. Se guarda con `store.updateRules(nodeId, mode, ids)`, que llama a `port.updateRules`.
- **Regla con grupos (HU-59):** `node.rule`. Se lee con `combinedRuleOf(node)`, que la devuelve solo si tiene grupos, y se guarda con `store.updateRuleTree(nodeId, rule)`.
- Ya existe `withoutElement(rule, id)` en `domain/rule-tree.ts`: saca la hoja del nodo y los grupos que quedan vacíos. Un root vacío es válido y borra la regla.

## 3. Qué hay que cambiar

### 3.1 Dominio (función pura) — `domain/unlock-rules.ts`
Nueva función `prerequisitesBrokenByMove(activities, connections, movedId, targetId, before)`. Devuelve un `Map<destinoId, origenIds[]>`.
1. Simula el nuevo orden de la unidad con el mismo criterio que `reorderActivity`: el nodo movido queda antes o después del target.
2. Revisa **solo las aristas en las que participa el nodo movido** y donde los dos nodos son de esta unidad. Las aristas entre otros dos nodos no cambian de sentido con un solo movimiento, así que no se tocan (es el "desvincular solo los que pasaron a estar delante").
   - **Si el movido bajó:** sus requeridos siguen arriba. Se rompen las aristas `movido → X` donde X ahora quedó antes del movido, es decir, los nodos que lo requerían y que él pasó por encima.
   - **Si el movido subió:** se rompen las aristas `X → movido` donde X ahora quedó después, es decir, los que él requería y que pasó por encima.
   - Regla general, sin casos especiales: una arista `origen → destino` está rota si `index(origen) >= index(destino)` en el nuevo orden.
3. Las restricciones con nodos de **otra** unidad no se tocan: el orden entre unidades es una regla de las unidades, no de los nodos.

### 3.2 Store — `RoadmapStore.moveActivityTo`
- **Antes** del PATCH, calcula `broken = prerequisitesBrokenByMove(...)` con la sección y las `connections()` actuales.
- **Después** del PATCH, si `broken` no está vacío, por cada destino:
  - si `combinedRuleOf(node)` devuelve una regla, aplica `withoutElement` a cada origen roto y llama a `port.updateRuleTree`;
  - si no, llama a `port.updateRules(nodeId, prerequisiteModeOf(node), restantes)`.
- Todos los llamados al `port` van en un `forkJoin`. **Se hace un solo `reload()` y un solo toast** al final, en lugar de usar `store.updateRules`, que recarga y avisa por cada nodo.
- **Toast:** si se desvinculó algo, un mensaje nuevo `roadmapStore.orderSavedUnlinked` («Orden guardado. Se quitaron N restricciones que quedaban hacia adelante.»), en `assets/i18n/es.json` y en `en.json`. Si no, el `orderSaved` de siempre.
- **Si falla la poda:** el orden ya quedó guardado. Hace igual `reload()` y muestra un error (`roadmapStore.unlinkAfterMoveFailed`). Lo que quede aparece `misplaced` en el editor de reglas, como pasa hoy, y el profe lo puede sacar a mano.

### 3.3 Componentes
- `roadmap-section-nodes` y `course-map-page` no cambian: el fix está en el store.
- `nodeRuleCandidates` / `misplaced` **se dejan como están**: siguen sirviendo para los datos viejos que ya tienen aristas hacia adelante.

## 4. Tests (solo los del cambio)
- `domain/unlock-rules.spec.ts`, con la función nueva:
  - mover el 1.º al final rompe las aristas de los que lo requerían;
  - subir el 3.º al 1.º lugar rompe sus aristas a los nodos 1 y 2;
  - una arista con un nodo de otra unidad no se toca;
  - mover sin cruzar ninguna arista devuelve un mapa vacío;
  - una arista entre dos nodos que no se movieron no se toca.
- `data-access/roadmap/roadmap.store.spec.ts`:
  - después de `moveActivityTo`, llama a `updateRules` con lo que queda y hace un solo `reload`;
  - con una regla con grupos, llama a `updateRuleTree` con `withoutElement`;
  - si no se rompe nada, no llama a ninguna de las dos.
- Correr con `npx ng test --include='**/unlock-rules.spec.ts' --include='**/roadmap.store.spec.ts' --watch=false`.

## 5. Prueba manual
1. En una unidad con nodos A, B y C: B requiere a A, y C requiere a A y a B.
2. Arrastrar A al final, para que el orden quede B, C, A. Resultado esperado: B queda sin restricciones, a C le sacan la de A y le queda B, y A sigue sin restricciones.
3. Abrir las reglas de B: no aparece ningún candidato. Abrir las de C: aparece solo B.
4. Con las flechas ↑/↓ tiene que pasar lo mismo, porque usan el mismo camino.

## 6. Fuera de alcance
- Que el back pode las aristas al recibir un `sort_order`. Sería lo más sólido, pero no se pidió. Se puede sumar a [[deuda-tecnica]].
- Limpiar las aristas hacia adelante que ya están guardadas en datos viejos. El editor las sigue mostrando `misplaced`.
