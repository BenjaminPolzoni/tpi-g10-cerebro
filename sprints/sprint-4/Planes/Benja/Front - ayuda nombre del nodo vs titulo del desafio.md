---
tags: [tpi, g10, sprint-4, plan, front, roadmap, challenges, help-hint]
fecha: 2026-10-27
autor: Benjamin Polzoni
estado: en revisión - PR FE#1688
actualizado: 2026-10-27
repo: 2026-P4-FE/2026-PIV-TPI-FE
rama: fix/challenge-name-on-create
---

# Plan — Ayuda contextual: «Nombre del nodo» vs «Título del desafío»

> **Autor / responsable del plan:** Benjamin Polzoni (`412056-1w3-Polzoni-Benjamin`)  
> **Fecha:** 2026-10-27  
> **Estado:** textos aprobados por Benjamin el 2026-10-27; **ayuda no implementada todavía**.  
> **Rama / worktree (frontend):** `fix/challenge-name-on-create` en `~/orca/workspaces/2026-PIV-TPI-FE/fix-challenge-name-on-create` (sin commit).  
> **Objetivo:** que el profesor sepa qué título se le pide al crear un desafío desde un nodo del roadmap: el **nombre del nodo** (lo que ve el alumno en el mapa) no es el **título del desafío** (su nombre en el catálogo). Se agrega un botón «i» (`app-help-hint`) junto a cada campo.

## 1. Lo que ya está hecho en la rama (paso previo)

Implementado por un worker codex vía Orca el 2026-10-27. ESLint y Prettier pasan; `tsc` limpio pendiente (el worktree usa un `node_modules` enlazado del checkout principal, con versiones distintas a `develop`).

- **Etiquetas:** en el roadmap el campo se llama «Nombre del nodo» (editor del nodo y wizard); en `/challenges/new`, «Título del desafío». Ambos con `hint` de `GenericInput`.
- **Opción «El desafío se llama igual que el nodo»** (`GenericCheckbox`, marcada por defecto) al elegir «desafío nuevo». Se guarda en el borrador del nodo (`node-draft.storage.ts`, campo `challengeSameName`).
- **Flujo:** si está marcada, `openChallengeAuthoring` manda el nombre del nodo como query param `title` (recortado, máx. 100) → `readChallengeAuthoringContext` lo valida → `challenge-create-page` lo precompleta y lo **bloquea** (`titleLocked`) con el aviso «Se usa el nombre del nodo». Desmarcada = flujo de antes.
- Al volver, `assignCreatedChallenge` **nunca renombra el nodo**.
- **Regla E-13 actualizada** en `docs/roadmap/e02-challenge-source.md`: antes el nombre del nodo nunca pasaba al desafío; ahora pasa solo con la opción marcada.

> [!warning] Pantalla de otro grupo
> La pantalla de creación de desafíos es del equipo de Challenges y la skill `help-hint` dice no editar pantallas ajenas. Ya se tocó en el paso previo; queda por confirmar si se mantiene o se pasa como pedido a ese equipo.

## 2. Skill que se aplica

`docs/skills/help-hint/SKILL.md` (frontend). Reglas que importan acá:

- El texto final lo decide la persona: estos textos quedaron **aprobados por Benjamin, 2026-10-27**.
- De 1 a 3 pasos, una oración cada uno. El paso 1 es la definición.
- Popover (`app-help-hint`) y no tooltip, porque son varios pasos (justificarlo en la PR).
- Botón **al lado** del label o encabezado, nunca adentro. Espaciado con `--space-*`.
- `help-sources.ts` aparte del `help-topics.ts` (solo lo lee el spec, no viaja en el bundle).
- `ui-standardization` **no aplica** al roadmap (está excluido).

## 3. Textos aprobados

### 3.1 `roadmap.help.nodeName` — «Nombre del nodo»

Va junto al campo en `entity-editor-dialog` y en `node-creation-wizard`.

| Paso | Texto (es) | Fuente | Estado |
|---|---|---|---|
| 1 | El nombre del nodo es lo que ven tus estudiantes en el mapa del roadmap de este curso. | `roadmap-section-nodes.component.ts:498` (`titleOf` → `node.name`) | verificado en código |
| 2 | Cambiarlo solo afecta a este nodo: no renombra el desafío del catálogo. | `docs/roadmap/e02-challenge-source.md` (E-13) y `entityEditor.scopeBody` | verificado en doc |
| 3 | Si creás un desafío nuevo y dejás marcado «El desafío se llama igual que el nodo», este nombre se usa también como título del desafío. | `roadmap-section-nodes.component.ts` (`openChallengeAuthoring`, query param `title`) | verificado en código |

### 3.2 `challenges.help.challengeTitle` — «Título del desafío»

Va junto al campo en `challenge-rich-text-field`, con el envoltorio `challenges/ui/field-help/`.

| Paso | Texto (es) | Fuente | Estado |
|---|---|---|---|
| 1 | El título del desafío es su nombre en el catálogo de desafíos. | `challenge-definition-card` / `title` del Motor | verificado en código |
| 2 | Un mismo desafío puede usarse en varios nodos y cursos, y cada nodo tiene su propio nombre. | e02 («A challenge has its own title») + pool de desafíos existentes | inferido en parte, **aprobado igual** |
| 3 | Si venís desde un nodo con «se llama igual que el nodo», el título llega completo y bloqueado; para cambiarlo, desmarcá esa opción en el nodo. | `challenge-create-page.component.html` (`titleLocked`) | verificado en código |

Fuente de cada aprobación en `help-sources.ts`: `defined by Benjamin Polzoni, 2026-10-27`.

**Actualización (2026-10-27):** implementado por codex vía Orca; `check:fast` pasa. Para el título del desafío se usó `app-help-hint` directo (no `field-help`, cuyo servicio no tiene título). **Pendiente:** aprobar la versión en inglés (`en.json`) que redacte el worker.

## 4. Pasos de implementación

Se manda a implementar con `/orchestration` → worker **codex** en el mismo worktree.

- [x] **Roadmap:** crear `src/app/features/roadmap/help-topics.ts` y `help-sources.ts` desde las plantillas de `docs/skills/help-hint/templates/` (forma de `accounting/help-topics.ts`).
- [x] **Challenges:** sumar el tema `challengeTitle` a `challenges/help-topics.ts` y su `help-sources.ts`.
- [x] **i18n:** claves `roadmap.help.nodeName.title|step1..3` y `challenges.help.challengeTitle.title|step1..3` en `es.json` y `en.json`, solo aditivas.
- [x] **Botones:** `app-help-hint` junto al campo de nombre del nodo (editor + wizard) y junto al título del desafío (vía `field-help`). Patrón `title-row`, `flex-shrink: 0`, sin meterlo en el `<label>`/encabezado.
- [x] **Specs:** spec de topics (claves en ambos idiomas, 1–3 pasos, con fuente) y uno por componente (`aria-label` = `Ayuda: <tema>`, botón fuera del encabezado). Se escriben, **no se corren** mientras se programa.
- [x] **Validación del worker:** solo `npm run check:fast`. Sin commit ni push.

## 5. Antes de abrir la PR

- [ ] `npm run auth` en el worktree para tener `node_modules` propio y `tsc` limpio.
- [ ] Specs de lo cambiado + `npm run verify` (una vez, al final).
- [ ] `npm run ui:review:pr` y H-01 a H-10 de `docs/skills/ui-review/rules.md`, una línea por ítem en la PR.
- [ ] Ver la app real: oscuro/claro, arcade/sobrio, 320 px y zoom 200 %, es/en, teclado y `Esc`.
- [ ] PR con: definiciones + fuentes + quién las definió, la justificación popover vs tooltip y lo no verificado.
- [ ] Decidir lo de la pantalla de Challenges (ver aviso de §1).

## 6. Actualización (2026-10-27) — cambio de regla y PR

- **Regla final (pedida por Benjamin):** en un nodo de desafío el nombre del nodo es **siempre** el título del desafío. Se eliminó la casilla «se llama igual».
  - Desafío nuevo: el nombre del nodo llega prellenado y **editable** a `/challenges/new`; al volver, el nodo toma el título final.
  - Desafío existente: al elegirlo, el nombre del nodo pasa a ser su título y queda bloqueado.
- Selector «Desafío existente / nuevo» al 50/50 como el de vidas; título largo del desafío cortado con «…».
- Paso 3 de ambas ayudas reescrito para la regla nueva.
- **PR:** [FE#1688](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/1688), con verify y specs tocados en verde. Los 24 fallos de la suite completa también fallan en `develop`.
- **Pendiente:** issue al UI-KIT por `GenericSegmented` a ancho completo (hoy `::ng-deep`, UI-004), lector de pantalla y CI.
