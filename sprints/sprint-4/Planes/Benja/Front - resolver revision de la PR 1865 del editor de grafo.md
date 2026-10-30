---
tags: [tpi, g10, sprint-4, plan, front, roadmap, editor-grafo, revision-pr]
fecha: 2026-10-30
autor: Benjamin Polzoni
estado: propuesta - sin implementar
repo: 2026-P4-FE/2026-PIV-TPI-FE (FE#1865, rama feature/graph-editor-unified-iteration-2)
---

# Front — Resolver la revisión de la PR #1865 (editor de grafo)

> [!important] Objetivo
> Los 3 comentarios P2 de `412016-camacho` (estado `CHANGES_REQUESTED`) quedan resueltos sin tocar el contrato con el back ni el resto del editor. Los tres vienen de lo mismo: la PR ya permite reglas **nodo ⇄ sección** (una sección requiere un nodo, un nodo requiere una sección) y tres puntos todavía asumen "solo nodos". Copilot no revisó (sin cuota): no hay nada que atender de su parte.

## Los comentarios

| # | Archivo (en la PR) | Problema | Riesgo si se ignora |
|---|---|---|---|
| 1 | `domain/graph-editor-projection.ts:176` + `domain/requirement-picker.ts` | `savedDraftOf` → `draftFromRule` deja cada hoja en `itemId` y pierde `elementType`; `canvasVerdictOf(canvas,'node')` solo conoce candidatos nodo | Una regla válida con hoja SECTION aparece como inválida en «Desbloqueo» y `save` la rechaza; `draftToRule` además la guardaría sin tipo |
| 2 | `pages/graph-editor-page/graph-editor-page.component.ts:1118` (`nodeDependents`) | Filtra `targetKind !== 'section'`; si el único dependiente es una sección la lista queda vacía y `deleteNode()` corre sin confirmación | Borrado silencioso de un nodo que una sección requiere (rompe la regla de la sección) |
| 3 | `graph-editor-page.component.html:287,302` y `ui/learning-map-canvas/learning-map-minimap.component.html:34` | 3 `<button>` nativos nuevos (`edge-toggle` ×2, `minimap-toggle`) | Falla `check:fast` / `check-ui-kit-usage`; el reviewer pidió no subir el baseline |

## Plan

### 1. Hojas SECTION en el borrador (comentario 1) — lo más delicado

Principio: el cambio es **aditivo y opcional**, para no romper la pantalla `requirements-picker-page` que usa las mismas funciones y hoy trabaja con hojas sin tipo (heredan el del dueño).

1. `RequirementLeafDraft` gana `elementType?: 'NODE' | 'SECTION'` (ausente = hereda del dueño, como hoy).
2. `draftFromRule`: copiar `elementType` de la hoja al crear la hoja del borrador (hoy lo descarta en `requirementLeaf(operand.elementId)`).
3. `draftToRule`: emitir `elementType` en la hoja solo si el borrador lo trae. Sin tipo → salida idéntica a la actual (los specs existentes no cambian).
4. Veredicto en el editor (`graph-editor-page.component.ts` ~3399): armar `verdictOf` uniendo el mapa de candidatos nodo con el de candidatos sección (el de `canvasVerdictOf(canvas,'section')` o la misma regla que ya usa la conexión nodo←sección al dibujar, ~línea 4074 — **verificar cuál es la fuente de verdad**). Se mantiene `invalidDraftLeafIds(draft, verdictOf)` por id: no cambia firma. Supuesto a dejar en un test: los ids de nodo y sección no colisionan (UUID).
5. Revisar que `nameOf(id)` y `requirementGroupViews` resuelvan el nombre de una hoja sección (si no, se vería el id crudo).
6. `savedNodeRuleOf` (graph-editor-projection) ya conserva el árbol cuando hay hoja sección: no se toca.
7. Orden en `draftToRule(draft, orderOf)`: confirmar que `orderOf` devuelve algo estable para ids de sección (hoy `order.get(id) ?? 0`, ~3795); con `0` el orden entre hojas sección queda por orden del borrador (sort estable) → aceptable.

Test de regresión pedido: regla mixta (nodo E exige sección `u1` + un nodo) creada desde el canvas → abrir «Desbloqueo» → `invalidLeafIds` vacío → agregar/quitar otra hoja → guardar → el payload conserva `elementType: 'SECTION'` en `u1`. Más un spec de `draftFromRule`/`draftToRule` (round-trip con y sin tipo) en `requirement-picker.spec.ts`.

### 2. Dependientes de tipo sección al borrar (comentario 2)

1. `nodeDependents` pasa a devolver `{ id, name, kind: 'node' | 'section' }`: relaciones `requires` con `sourceId === id` y `sourceKind === 'node'` (se mantiene excluir `sourceKind === 'section'`, que no es "este nodo"), con `targetKind` node **o** section; el nombre sale de `nodesById` o del mapa de secciones.
2. El borrado inmediato (`nodeAction` delete, ~1196) queda **solo** con `nodeDependents().length === 0`.
3. Modal de borrado (`html` ~1013): listar ambos tipos, con una marca de tipo (texto, no solo color) y claves i18n nuevas en todos los idiomas existentes (es/en/pt; glosario en `docs/i18n-pt-glossary.md`). Reutilizar `courseMap.deleteDependents*`; solo agregar lo que falte para "sección".
4. `editNodeDependents` (~1284) hoy encadena rutas `requirements?owner=node`. Para dependientes sección **verificar** si `requirements?owner=section` edita reglas cuyas hojas son nodos (el canvas `'section'` solo mapea unidades → probablemente no). Si no: para sección cerrar el modal y seleccionar la sección en el editor (`pickCandidate({kind:'section'})` / `selectedUnitId`) para editar su regla ahí, sin navegar al picker. Decidir tras leer ese código; no inventar ruta nueva.
5. Test: F requerido solo por una sección → `nodeAction(delete)` abre el diálogo y **no** llama `deleteNode`; con un nodo y una sección dependientes, la lista muestra ambos; sin dependientes sigue borrando directo.

### 3. Botones nativos → UI kit (comentario 3)

1. `edge-toggle` ×2 y `minimap-toggle`: `<button type="button" genericIconButton …>` (`GenericIconButton`, selector `button[genericIconButton]`, input `size`). Conservar `aria-label`, `title`, `aria-expanded`, `aria-controls`, `(click)` y el glifo (`‹ › ✕ ▦`, `aria-hidden`).
2. Importar `GenericIconButton` en los dos componentes (`imports`). En el CSS dejar solo posicionamiento (`.edge-toggle*`, `.minimap-toggle` en `graph-editor-page.component.css:166` y `learning-map-minimap.component.css:16`); quitar fondo/borde/hover/foco propios que el kit ya da, con tokens `--tpi-*` si algo queda.
3. **No** correr `npm run check:ui-kit:update` ni tocar el baseline (pedido explícito del reviewer).
4. Nota: en esta rama hoy `node scripts/harness/check-ui-kit-usage.mjs` da `OK` (83 controles *por debajo* del baseline). Entonces el fallo del reviewer sale de `check:fast` completo o de un baseline por archivo frente a `develop`: correr primero `npm run check:fast`, leer el mensaje exacto y arreglar eso.

## Orden y verificación

1. Comentario 3 (mecánico) → 2 (acotado) → 1 (modelo de datos, el de más riesgo; al final con todo lo demás estable).
2. Una sola rama (la actual); un commit por comentario; **`git commit -- <rutas>`**, porque el working tree tiene trabajo sin commitear ajeno a esto (`roadmap-layout.store*`, `edge-custom-route`, canvas…) que no debe entrar.
3. Sin tests mientras se programa. Antes de empujar: specs de roadmap tocados + `npm run verify` (ojo con flakes conocidos: clipboard, teardown, `isolate:false`; re-correr aislado antes de culpar el cambio).
4. Aceptación: commit + levantar la imagen; comprobar a mano la regla mixta en «Desbloqueo» y el borrado de un nodo requerido solo por una sección.

## Fuera de alcance / a confirmar

- Responder o resolver los hilos en GitHub y volver a pedir revisión: **acción externa, se hace solo cuando lo pidas**, después del push.
- Si el back no acepta `elementType` en hojas dentro de reglas de nodo, el punto 1 se bloquea: la PR ya lo envía hoy (la proyección lo lee), así que se asume que sí; confirmar con una regla real antes de cerrar.
