# Tareas: editor unificado del grafo del roadmap

FE: `src/app/features/roadmap/`; i18n: `src/assets/i18n/{es,en}.json`. 2xx confirma. Por lote: TypeScript compila, commit y app revisada. Pruebas: lote final.

## Lotes ordenados

### Lote 1 — Extraer página (primero; sin cambio funcional)
- [ ] **T-01** Crear `pages/graph-editor-page/graph-editor-session.ts`, `domain/graph-editor-projection.ts`; modificar `graph-editor-page.component.ts` para delegar estado/comandos. **Dep.:** —. **Req.:** R2–R11, REPO-01–09. **Acept.:** conducta intacta; página coordina. **i18n es/en:** —.

### Lote 2 — Ruta única (paralelo con Lote 3 tras T-01)
- [ ] **T-02** Modificar `roadmap.routes.ts`, `pages/course-editor-page/course-editor-page.component.{ts,html}`; borrar `pages/course-map-page/**`, `ui/map-unit-list/**`; limpiar claves huérfanas en `es.json`/`en.json`. **Dep.:** T-01. **Req.:** R1. **Acept.:** `/map` monta Graph + guard, `/graph` redirige, sin pestaña/imports legacy. **i18n:** conservar usadas; borrar huérfanas.

### Lote 3 — Marcos y movimientos (paralelo con Lote 2)
- [ ] **T-03** Modificar `domain/map-layout/{map-layout.ts,dagre-layout.engine.ts,region-packing.ts}`, `ui/learning-map-canvas/learning-map-canvas.component.{ts,html,css}`: jerarquía, colapso, vacíos, drop al marco sin reparentar; movimiento no pierde reglas. **Dep.:** T-01. **Req.:** R3, R6, REPO-04–06. **Acept.:** colapso preserva reglas. **i18n:** `graphEditor.frame.*`, `graphEditor.emptySection.*` es/en.

### Lote 4 — Router real obstacle-aware
- [ ] **T-04** Modificar `domain/map-layout/edge-router.ts` y `ui/learning-map-canvas/learning-map-canvas.component.{ts,html,css}`: rutas ortogonales anidadas evitan obstáculos/marcos; stubs, curvas, costo de giro, paralelas, punta, resaltado y recálculo. **Dep.:** T-03. **Req.:** R12. **Acept.:** sin cruces ni fugas. Mockup A* 10 px, giro 25, paralela 7, stub 16 px: solo referencia. **i18n:** `graphEditor.edge.*` es/en.

### Lote 5 — Conexiones y persistencia
- [ ] **T-05** Modificar `ui/learning-map-canvas/*`, `pages/graph-editor-page/{graph-editor-page.component.ts,graph-editor-session.ts}`: puertos/flecha fantasma; «B requiere A», sin selector/informativas; hoja `NODE` a sección; atajos C/Enter/Esc. **Dep.:** T-03. **Req.:** R2, R10–R11, REPO-01/02/07/08. **Acept.:** request backend siempre decide. **i18n:** `graphEditor.connect.*` es/en.
- [ ] **T-06** Modificar `pages/graph-editor-page/graph-editor-session.ts`, `roadmap.store.ts` solo si falta método, diccionarios es/en: `saveRules`/`saveUnitRules`, saving pesimista, sin doble submit, reload/rollback/reintento, fallo parcial. **Dep.:** T-05. **Req.:** R5, R11, REPO-01–03/07–09. **Acept.:** 2xx confirma; error revierte; foco/conflicto relee; fallo parcial conserva nodo. **i18n:** `graphEditor.save.*` y mensajes accionables en ambos idiomas.

### Lote 6 — Asistente, árbol, overview y formas
- [ ] **T-07** Modificar `ui/node-creation-wizard/*`, `pages/graph-editor-page/*`; crear `ui/graph-structure-tree/*`, `ui/graph-overview-panel/*`. Wizard en panel derecho con selector de sección; usa `addSection`/`addZone`/`addActivity`; overview sin selección: conteos, «Para revisar» (vacíos/sin reglas), atajos; inspector seleccionado: requisitos/dependientes/quitar. **Dep.:** T-01/T-05. **Req.:** R4, R7, R10. **Acept.:** árbol expande ancestros/centra. **i18n:** `graphEditor.{tree,overview,wizard}.*` es/en.
- [ ] **T-08** Modificar `ui/learning-map-canvas/*`, `domain/map-layout/map-layout.ts`: tarjeta/círculo; preferencia `localStorage` try/catch (default tarjeta). **Dep.:** T-03. **Req.:** R8, R12. **Acept.:** misma info; recalcula router. **i18n:** —.

### Lote 7 — General/alumno (paralelo tras T-06)
- [ ] **T-09** Modificar `embeds/section-nodes/roadmap-section-nodes.component.{ts,html,css}`, diccionarios es/en: chip requisitos y «Conexiones». **Dep.:** T-06. **Req.:** R9. **Acept.:** General refleja «Requiere»; alumno mantiene bloqueo/filtro. **i18n:** `roadmap.sectionNodes.{requirements,connections}.*` es/en.

### Lote 8 — Verificación backend y pruebas finales
- [ ] **T-10** Verificar en `tpi-roadmap` `RuleTreeValidator.java`, `RuleLeafEligibility.java`, `RuleDto.java`, mutaciones `GraphService.java`: `minXp` fraccionario, referencias eliminadas/ocultas (nodo/sección), hoja `NODE`→sección y concurrencia. **Dep.:** T-06. **Req.:** R2, R5, R11. **Acept.:** evidencia o propuesta backend, nunca preflight FE. **i18n:** —.
- [ ] **T-11** Crear `domain/map-layout/edge-router.spec.ts` y specs de layout/canvas/página/rutas/store/wizard/`section-nodes`; cubrir R1–R12, intersección obstáculos, teclado/ARIA, rollback/parcial. **Dep.:** T-02–T-10. **Req.:** R1–R12, REPO-01–09. **Acept.:** escenarios cubiertos. **i18n:** validar par es/en.

## Paralelismo / revisión

Crítico: **T-01→T-03→T-04→T-05→T-06→T-07/T-09→T-11**. Paralelos: T-02 || T-03; T-09 || T-10 tras T-06; T-08 va tras T-05 por archivos compartidos. Sin solapar archivos.

- [ ] Trazabilidad: R1 T-02; R2 T-05/06/10; R3 T-03; R4 T-07; R5 T-06/10; R6 T-03; R7 T-07; R8 T-08; R9 T-09; R10 T-05/07/11; R11 T-05/06/10/11; R12 T-04/08/11.
- [ ] REPO-01–03/07–09: T-05/06/11; REPO-04–06: T-03/08/11. R1–R12/REPO-01–09 cubiertos.
