---
tags: [tpi, g10, sprint-4, plan, front, courses, roadmap, reglas]
fecha: 2026-11-08
autor: Benjamin Polzoni
estado: en curso
repo: 2026-P4-FE/2026-PIV-TPI-FE
rama: BenjaminPolzoni/RamaDeAjusteDeVisibilidad
---

# Plan — Reglas de acceso de sección en la vista simplificada

## Qué se pide
Desde la vista simplificada (contenido del curso, `cohort-general-page`), el drawer "Editar <sección>"
tiene que dejar armar las reglas de acceso de la sección igual que en la vista de nodos:

- la sección 2 depende de la sección 1 (una o varias secciones/subsecciones);
- hace falta un mínimo de XP;
- hay que completar uno o varios nodos;
- cualquier combinación (todas juntas = AND, alguna = OR, grupos).

Hoy no deja. Back no cambia: `PUT` del árbol de reglas de sección ya acepta `minXp` y hojas tipadas
(`RoadmapStore.saveUnitRules` → `updateSectionRuleTree`).

## Diagnóstico (código)
Archivo: `src/app/features/courses/pages/cohort-general-page/section-editor-drawer.component.{ts,html}`.

1. **La unidad no se resuelve por id.** `unit` llama `store.unitOfCourseSection(section().title)` sin el
   id. Si el nombre de la unidad del roadmap no coincide exacto con el título del curso (o hay dos con
   el mismo nombre) devuelve `undefined` y la pestaña muestra "no sincronizada": no se puede marcar
   nada. `general-subsection-card` y `roadmap-section-nodes` ya pasan el id.
2. **No hay campo de XP.** El draft tiene `minXpText` pero el drawer no lo expone; el editor de nodos
   (`requirements-picker-page`) sí (`setDraftMinXp`, `invalidMinXpGroupIds`).
3. **La regla guardada no se ve fuera del modo selección.** El picker recibe
   `[selected]="selecting() ? ruleLeafIds() : []"`, así que al abrir la pestaña parece vacía.

## Tareas
- [x] R-01 `unit`: `this.store.unitOfCourseSection(this.section().title, this.section().id)`.
- [x] R-02 Picker: `[selected]="ruleLeafIds()"` siempre (sigue siendo solo lectura si no se selecciona).
- [x] R-03 Campo "XP mínimo" en la pestaña Reglas (debajo del panel de reglas), `GenericInput`
      `type="number"`, valor `currentRuleDraft().minXpText`, al cambiar
      `writeRuleDraft(setDraftMinXp(draft, 0, text))` (iniciando el draft con `startRulePicking` sin
      forzar el modo selección si no hace falta). Reusar las claves i18n del editor de nodos
      (`graphEditor.unlock.xpAria`, `graphEditor.unlock.xpPlaceholder`, `requirementsPicker.xpHint`,
      `requirementsPicker.xpInvalid`). Error si `invalidMinXpGroupIds(draft).length > 0`.
- [x] R-04 `save()`: si hay XP inválido, no guardar y mostrar `requirementsPicker.xpInvalid` en
      `saveError`.
- [x] R-05 `ruleSummary` ya incluye el XP (`requirementSummary` con `xp`): verificar que se ve.
- [x] R-06 `ruleTree()`: con XP > 0 y sin hojas tiene que mandar `{ op: 'AND', minXp, operands: [] }`
      (verificar que `draftToRule` + `needsRuleTree` lo producen; `minXp` fuerza árbol).
- [x] R-07 Specs en `section-editor-drawer.component.spec.ts`: unidad resuelta por id con nombre
      distinto; guardar solo XP manda árbol con `minXp`; XP inválido bloquea el guardado.

## Fuera de alcance
- Cambios de back.
- Rediseñar la pestaña o mover las reglas a una página aparte.
