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

## Iteración 2 — validar nodos y mensajes claros (2026-11-08)
Feedback del usuario sobre la iteración 1: el drawer deja elegir nodos de la propia sección (y de
secciones que dependen de ella), el back lo rechaza con un mensaje genérico ("No se pudo guardar la
configuración de la sección") y el XP quedó abajo de todo. Criterio acordado: **se permite cualquier
elemento mientras no cierre un ciclo**, aunque esté más adelante en el mapa (casos en
[[preguntas-y-respuestas/01 - Reglas de acceso de una seccion]]).

**Solo front.** El back (tpi-roadmap) ya valida exactamente este modelo
(`RuleLeafEligibility.requireEligibleForSection`, `SubsectionGuard`, `DependencyGraphService` con
pasos ENTER/COMPLETE) y no tiene orden implícito. El front ya tiene la misma lógica en
`roadmap/domain/prerequisite-policy.ts`; el drawer solo la aplica a las secciones de primer nivel y
marca todos los nodos (y subsecciones) como `blocked: false`.

**Regla dura: solo componentes de `@2026-p4-fe/ui` y tokens `--tpi-*`.**

- [ ] R-08 `ruleOptions` (drawer): validar **cada** elemento (secciones de cualquier nivel y nodos)
      con `prerequisitePolicy(this.store.sections(), [])` contra
      `{ kind: 'section', id: unit.id }`. `blocked = !verdict.allowed && !savedLeaf` (un elemento ya
      guardado sigue elegible para poder quitarlo). Quitar el fallback que ofrecía todas las
      secciones sin bloquear cuando no había candidatos. La propia unidad sigue mostrándose con sus
      nodos, todos bloqueados.
- [ ] R-09 `PrerequisiteOption` gana `reason?: string` (texto ya traducido). `prerequisite-picker`
      muestra `row.reason` en la nota de la fila y en su `aria-label` cuando existe; si no, el texto
      actual `requirementsPicker.tree.blocked`. Las filas bloqueadas siguen `disabled` (no se
      pueden clickear). Sin cambios de comportamiento para el editor de nodos (no pasa `reason`).
- [ ] R-10 Textos del motivo (claves nuevas `sectionDrawer.rules.blocked.*`, en es/en/pt), según el
      primer motivo del veredicto:
      - `containment` en un **nodo** → "No podés elegir un nodo de esta misma sección."
      - `containment` en una **sección** → "No se puede elegir: contiene a esta sección o está dentro de ella."
      - `self` → "Es esta misma sección."
      - `cycle` → "No se puede elegir: ya depende de esta sección y cerraría un ciclo."
      - otro (`optional`, `boundary`, `recovery`) → "No se puede elegir: " + `prerequisitePolicy.reason.<motivo>`.
- [ ] R-11 XP mínimo **arriba**: mover el `generic-input` del XP justo debajo del texto de
      introducción de la pestaña Reglas, antes de los botones de selección y del árbol.
- [ ] R-12 Panel de la regla: `requirementOperandRows(..., kindOf)` con `'node'` para nodos y
      `'unit'` para secciones (hoy dice "Unidad" en todos).
- [ ] R-13 Error al guardar reglas: `saveRules` llama `saveUnitRules(..., { inlineError: true })` y
      el error que muestra el pie es `roadmapErrorMessage(err, t('roadmapStore.unitRulesFailed'), i18n)`
      (no el genérico de la configuración de la sección). En `roadmap-error-message.ts` mapear
      `rule.self-reference` → `ROADMAP_RULE_SELF_REFERENCE`, `rule.optional-prerequisite` →
      `ROADMAP_RULE_OPTIONAL_PREREQUISITE`, `section.prerequisite-containment` →
      `ROADMAP_SECTION_PREREQUISITE_CONTAINMENT`, con textos en `errors.byCode` (es/en/pt):
      - SELF_REFERENCE: "La regla exige un elemento de esta misma sección. Quitalo y guardá de nuevo."
      - OPTIONAL_PREREQUISITE: "La regla exige un nodo opcional, que el alumno puede saltear. Quitalo y guardá de nuevo."
      - CONTAINMENT: "Una sección no puede exigir a la que la contiene ni a una de sus subsecciones."
- [ ] R-14 Specs del drawer: nodo de la propia sección bloqueado con su motivo; nodo de una sección
      posterior que no depende de esta → elegible (caso 5); nodo de una sección que depende de esta
      → bloqueado por ciclo (caso 4); el XP se renderiza antes del picker; error 400
      `rule.self-reference` muestra el texto nuevo.

## Fuera de alcance
- Cambios de back.
- Rediseñar la pestaña o mover las reglas a una página aparte.
