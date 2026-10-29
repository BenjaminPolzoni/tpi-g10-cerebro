---
tags: [tpi, g10, sprint-4, plan, back, front, roadmap, auditoria, deuda]
fecha: 2026-10-28
autor: Benjamin Polzoni
estado: borrador
repo: 2026-P4-BE/tpi-roadmap, 2026-PIV-TPI-FE
base: BE origin/develop 90d305bd (2026-10-28)
antecedentes: AUDITORIA-develop-2026-10-28 (pestaña «Endpoints sin uso», servicio tpi-roadmap), HU-13, HU-41, HU-65, #310, #332, #349
---

# Back+Front · Endpoints sin uso del roadmap

> [!info] Alcance
> La auditoría del 2026-10-28 marca **9 endpoints de `tpi-roadmap` como «Huérfano»**: ningún front, micro, desktop ni infra los llama. En este plan se explica de dónde salió cada uno y se decide si **se borra**, **se conecta** o **se mantiene**. Es una propuesta y todavía no hay código.

## 1. Qué hay hoy, endpoint por endpoint

| ID | Endpoint | De dónde sale | Por qué nadie lo llama | Veredicto |
|---|---|---|---|---|
| B4-122 | `POST /admin/outbox/retry-failed` | Outbox en dos fases con DLT y redrive (`ab97301c`). Devuelve todos los eventos `FAILED` a `PENDING` para que el poller los reintente. Lo hermana `POST /admin/outbox/{eventId}/retry`. | Es una **herramienta de operación**: la usa un ADMIN a mano (Swagger o curl) cuando Kafka estuvo caído. No necesita UI. | **Mantener** |
| B4-113 | `GET /roadmaps/{id}/hidden-relation-types` | T-65.6 (HU-65 CA3), `43d81b57`. | Sobra: la vista del grafo del profesor ya trae `layout.hiddenTypes`, que el FE lee en `graph-view.mapper.ts`. Al alumno no se lo manda (`4a2197b1`). | **Borrar** |
| B4-114 | `PUT /roadmaps/{id}/hidden-relation-types` | T-65.6 (HU-65 CA3). Reemplaza los tipos ocultos. Ocultar `REQUIRES` solo cambia el dibujo, no el desbloqueo. | Falta el control del front (T-65.2): el FE **filtra** con `hiddenTypes` pero no tiene ningún botón que lo cambie. | **Conectar** |
| B4-118 | `PATCH /nodes/{id}/prerequisite-mode` | HU-13 D-01: cambiar AND/OR del nodo. | **Lo reemplazó `PATCH /nodes/{id}/rules`** (T-13.1 y el árbol de HU-59), que guarda modo y prerrequisitos juntos. En el FE solo queda el DTO muerto (`backend-roadmap.dto.ts:246`). | **Borrar** |
| B4-117 | `GET /courses/{id}/nodes/{id}/ai-policy` | Issue **#332** (abierta, pedida por Motor), `ec9e8f15`. Da `ai_allowed` efectivo: la cohorte con `ai_enabled` y el nodo con `uses_ai`. | El editor de nodos usa solo el flag de la cohorte (`aiAllowed = aiEnabled()`), que es correcto ahí porque está editando `uses_ai`. El consumidor que falta es la **creación de desafío desde un nodo** (Motor), que todavía no la consulta. | **Conectar** (lo consume Motor) |
| B4-119 | `GET /nodes/{id}/edit-log` | HU-41 CA6 (T-41.4, HT-32): autor, fecha, campos cambiados y alumnos afectados. Tabla `node_edit_log` (V18). | El back se hizo, pero el front nunca tuvo la vista de historial. | **Conectar** |
| B4-108 | `GET /courses/{id}/students/{id}/xp-timeline` | Issue **#310** (cerrada en el back), `f427dff3`: serie semanal de XP del alumno. | El FE solo usa la de la cohorte (`/courses/{id}/xp-timeline`, en `cohort-dashboard.service.ts`). Faltó el gráfico en «Mi progreso» y en el progreso que ve el staff. | **Conectar** |
| B4-123 | `GET /courses/{id}/students/me/xp-history` | Issue **#349** (abierta, la pide Accounting T08), PR #352. Saca el historial de XP del perfil `dev`. | La auditoría corrió con #352 recién mergeado. El consumidor es la **pantalla de inventario** de Accounting, que está pendiente. | **Mantener** (consumidor en camino) |
| B4-124 | `GET /courses/{id}/students/{id}/xp-history` | Igual que B4-123, para el staff. | Igual. | **Mantener** |

> [!warning] El clon local de `tpi-roadmap` está atrás
> El `develop` local todavía tiene `XpHistoryController` con `@Profile("dev")` y sin `/me`. Antes de tocar nada, hacer `pull`.

## 2. Decisiones a confirmar

| # | Decisión | Recomendación |
|---|---|---|
| D1 | ¿El outbox lleva UI en el backoffice? | **No.** Se documenta en el runbook y en la auditoría queda «Mantener: operativo». |
| D2 | ¿Se borra el `GET hidden-relation-types` o se deja para que el PUT tenga par REST? | **Borrar.** Lo cubre `layout.hiddenTypes` y un endpoint menos es menos superficie. Si se prefiere el par REST, cambiar a «Mantener». |
| D3 | ¿Dónde va el control para ocultar tipos? | En la leyenda de relaciones del mapa del profesor (`course-map-page`): un interruptor por tipo que hace el PUT y recarga el grafo. |
| D4 | ¿Quién conecta `ai-policy`? | El equipo de Motor o el dueño de la creación de desafíos en el FE. Nosotros comentamos en #332 que el back está listo. |
| D5 | ¿Dónde se ve el log de edición? | Una pestaña «Historial» en `entity-editor-dialog`, que solo se carga al abrirla. |
| D6 | ¿Dónde va la serie personal de XP? | En `student-progress-page` (el alumno) y en `staff-student-progress-page` (el staff), reusando `CohortXpTimelineComponent` con otra fuente. |

## 3. Pasos: borrar (BE + FE)

1. **`PATCH /nodes/{id}/prerequisite-mode`**
   - BE: quitar `GraphController.updatePrerequisiteMode` y `GraphDtos.PrerequisiteModeRequest`. Quitar `GraphService.updatePrerequisiteMode` (las 2 sobrecargas) solo si nada fuera del controlador lo usa. Si algún test lo usa como atajo, pasar ese test a `PATCH /nodes/{id}/rules`.
   - Tests que llaman la ruta y hay que migrar a `/rules`: `NodeUnlockRetroactivityTest`, `RoadmapFlowTest`, `UnlockRuleTreeTest`, `UnlockRuleReadTest` y `GraphControllerTest`. En `SpringDocConfigTest`, sacar la ruta de la lista esperada.
   - FE: borrar el DTO del body en `backend-roadmap.dto.ts:246`.
2. **`GET /roadmaps/{id}/hidden-relation-types`** (si se confirma D2)
   - BE: quitar `TypedRelationController.hiddenTypes`. El servicio `relations.hiddenTypes` sigue, porque lo usa el armado de `layout`.
   - Tests: los escenarios BDD de T-65.5/T-65.6 que leen con GET pasan a leer `layout.hiddenTypes` del `GET /roadmaps/{id}/graph`.

## 4. Pasos: conectar (FE)

1. **Tipos ocultos (B4-114).** Agregar `setHiddenRelationTypes(roadmapId, types)` en `http-roadmap.adapter.ts`, que hace el PUT con `hidden_types`. En `course-map-page`, cada tipo de la leyenda tiene un interruptor: al cambiarlo se hace el PUT y se recarga `graphView`. Con `REQUIRES` oculto se muestra el aviso «solo cambia el dibujo, no el desbloqueo».
2. **Log de edición (B4-119).** Agregar `getNodeEditLog(nodeId)` en el adapter y una pestaña «Historial» en `entity-editor-dialog`, con autor, fecha, campos y cantidad de alumnos afectados, la más reciente primero. Si el nodo es nuevo, la pestaña no aparece.
3. **Serie personal de XP (B4-108).** Agregar `studentXpTimeline(courseId, studentId, from?, to?)` en el servicio de progreso. En `student-progress-page` y `staff-student-progress-page`, mostrar `CohortXpTimelineComponent`, o una versión que reciba los puntos por input si hoy los pide adentro. Cuando no hay datos, se muestra el estado vacío de NO_DATA.
4. **`ai-policy` (B4-117).** No lo tocamos nosotros: comentar en #332 la ruta, la respuesta y que el 503 nunca concede IA.

## 5. Pasos: mantener y documentar

1. **Outbox (B4-122):** agregar al runbook del roadmap cuándo usar `retry-failed` o `/{eventId}/retry`, después de revisar la DLT, y con qué rol.
2. **xp-history (B4-123/124):** comentar en #349 que está en `develop` y que se cierra cuando Accounting lo consuma.
3. En la planilla, completar «Estado» y «Comentarios» de las 9 filas con el veredicto de este plan.

## 6. Tests (solo los del cambio)

- BE: los 6 tests de §3.1 migrados a `/rules`, más el escenario de T-65.6 que lee `layout.hiddenTypes`. Correr solo esas clases.
- FE: specs del adapter para los métodos nuevos, de `course-map-page` (el interruptor hace el PUT y recarga), de `entity-editor-dialog` (la pestaña carga el log) y de las 2 páginas de progreso (gráfico y NO_DATA). Al pushear, usar `NODE_OPTIONS=--no-experimental-webstorage`.

## 7. Orden y dependencias

1. Las decisiones D1–D6.
2. Las bajas del BE (§3), en un PR chico que no depende de nada.
3. Las 3 conexiones del FE (§4), en PRs separados que pueden ir en paralelo.
4. Los comentarios en #332/#349 y la planilla (§5).

## 8. Riesgos

- **Borrar `prerequisite-mode`** puede romper a un cliente externo que la auditoría no vio. La búsqueda cubrió FE, micros, desktop, sandbox e infra, y Swagger no es un cliente. Riesgo bajo.
- **`hidden-relation-types` y Neo4j:** `hiddenRelationTypes` también se copia a `:Roadmap`, y el PUT ya pasa por Postgres → `graph_sync_pending` (DEC-021). Con el interruptor no cambia nada de eso.
- **Serie de XP del alumno:** exige matrícula activa, así que un alumno dado de baja recibe 4xx y el front tiene que mostrar un vacío, no un error.
