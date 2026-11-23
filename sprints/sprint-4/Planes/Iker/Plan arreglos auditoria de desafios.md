# Plan de implementación: arreglos de la auditoría de desafíos

**Fecha:** 03/11/2026
**Base:** `2026-PIV-TPI-FE` develop @ `07945db12` y `tpi-roadmap` develop
**Acompaña a:** `auditoria-creacion-desafios.md`
**Autor:** Iker · **Actualizado:** 03/11/2026 (se quitó el PR 1 y se agregó el reparto entre 3 integrantes)

El trabajo se reparte en **7 PRs chicos** (6 en el FE y 1 en `tpi-roadmap`), cada uno con un solo objetivo. Se mantiene la numeración original: el **PR 1 se quitó** porque ya está resuelto.

**Convenciones:**

- Ramas `fix/...` que salgan de `develop` actualizado.
- Commits en inglés en el FE (`fix(roadmap): ...`) y en español en `tpi-roadmap`.
- Antes de abrir cada PR: `git pull origin develop`, `npm run lint` y los specs que se tocaron.
- En una PC de 8 GB, correr los specs de a uno y con `NODE_OPTIONS=--max-old-space-size=4096`.

**Fuera de este plan:** la generación de desafíos prácticos en cursos sin configuración de Git. Eso lo resuelve el microservicio de desafíos prácticos.

---

## Reparto y orden

| Integrante | PRs | Archivos principales |
|---|---|---|
| **Iker** | PR 2 back → PR 2 FE → PR 6.1 | `tpi-roadmap` (`GraphDtos`, `GraphService`), adapter HTTP, `RoadmapStore`, `hideNode()` |
| **Ludmila** | PR 3 → PR 5 | Página de alta (`livesPolicy`), `roadmap-section-nodes`, `graph-editor-page`, `dirty()` del drawer |
| **Benja** | PR 4 → PR 6.2 → PR 7 | Página de alta (`rulesContext`), `/challenges/:id`, `compose-quiz-page`, `pt.json`, chequeo de i18n |

**Arrancan ya, en paralelo:** Iker con el PR 2 back, Ludmila con el PR 3 y Benja con el PR 4.

**Después:**

- Iker: el PR 2 FE cuando se mergee el back, y luego el PR 6.1.
- Ludmila: el PR 5, apenas se mergee el PR 3.
- Benja: el PR 6.2 y luego el PR 7.

**Orden de merge en la página de alta:** PR 3 → PR 4 → PR 2 FE. Tocan zonas distintas (`livesPolicy` ~738, `rulesContext` ~650, guardado/`hideNode` ~1830+), pero conviene respetar ese orden y hacer pull de `develop` antes de mergear.

**Decisiones a cerrar en el grupo:** por qué la descripción está en 500 (PR 4) y el selector de nodos o desafíos (PR 7.4).

---

## PR 2 — Que el nodo nazca no disponible y con sus prerrequisitos (crítico, dos repos) · Iker

**Qué pasa hoy.** Al guardar, el nodo se crea **disponible y sin prerrequisitos**, y recién después tres llamadas más le ponen la regla, la IA y lo marcan no disponible:

1. `POST /roadmap/sections/{id}/nodes` → `available: true`, sin prerrequisitos
2. `PATCH /roadmap/nodes/{id}/rules`
3. `PATCH /roadmap/nodes/{id}/ai`
4. `PATCH /roadmap/nodes/{id}/availability` → `available: false`

En la prueba estuvo disponible 0,7 segundos. Si alguna de las llamadas 2 a 4 falla, queda iniciable para los alumnos con un desafío sin terminar.

> `available: false` no oculta el nodo: según `GraphService.updateAvailability` significa «visible pero no iniciable». El riesgo es que se pueda **iniciar**, no que se vea.

**Por qué pasa.** El backend **ya acepta** la regla (`rule`, `prerequisite_mode`, `prerequisite_node_ids`) y la IA (`ai_roles`) en el mismo `POST`, y las guarda en la misma operación (`doCreateNode`, con `hasInitialRules()`). Lo que no acepta es `available`:

- `NodeRequest` (en `GraphDtos.java`) no tiene ese campo y tiene `@ClosedSchema`, así que mandarlo puede dar 400.
- `GraphService.apply()` nunca lo setea.

Del lado del FE, el store manda la regla y la IA en llamadas aparte.

### Parte backend (`tpi-roadmap`)

Commit en español, por ejemplo `fix(nodos): permitir crear un nodo no disponible`.

1. En `GraphDtos.NodeRequest`, agregar `@JsonProperty("available") Boolean available`. Que `null` signifique `true`, así no cambia nada para quien no lo manda.
2. En `GraphService.apply()`, setearlo sólo en el alta, con `node.setAvailable(req.available() == null || req.available())`.
   - **Ojo:** verificar que la edición use su propio patch (el comentario cerca de la línea ~950 indica que sí) para no pisar la disponibilidad de un nodo existente.
3. Actualizar el Javadoc de `MotorChallengeDetail.isAssignable`, que hoy promete algo que no se hace («el nodo nace no disponible»).
4. Tests:
   - un test del service que cree un nodo con `available=false` y verifique que queda no disponible;
   - un escenario BDD «crear un nodo con un desafío en borrador lo deja no disponible».

### Parte FE (después de mergear el backend)

1. En el adapter HTTP del roadmap (`roadmap/data-access/roadmap-http/http-roadmap.adapter.ts`, `createNode`, y su mapper), mandar `available`, la regla y `ai_roles` dentro del `POST`.
2. En `RoadmapStore.addActivityAt`, si el alta ya llevó la regla y la IA, no repetir los `PATCH /rules` y `/ai`.
3. En `challenge-node-create-page.component.ts`, `hideNode()` deja de ser necesario cuando el nodo ya nace no disponible. Dos opciones:
   - borrarlo, junto con `nodeHidden` en `Progress`;
   - dejarlo como no-op si `created.available` ya es `false`.

**Tests:**

- Spec del adapter: el body del `POST` lleva `available: false` y la regla.
- Spec de la página: no hay llamada a `updateAvailability`.

**Prueba manual:** guardar un desafío nuevo y ver en la pestaña Red **un solo** `POST /nodes` que responda `available: false` y con la regla, sin `PATCH /availability` después.

---

## PR 3 — Vidas: guardar lo que se elige (alto, chico) · Ludmila

**Qué pasa hoy:**

- «No consume vida» se guarda como «Consume vida».
- La cantidad de vidas (de 1 a 5) no se guarda en ningún lado.

**Qué cambiar** en `src/app/features/roadmap/pages/challenge-node-create-page/challenge-node-create-page.component.ts`:

1. **`livesPolicy`** (línea ~737): mapear `NONE → 'LLM'`, `RECOVERY → 'RECOVERY'` y el resto a `'STANDARD'`. `LLM` es el nombre histórico del perfil que no consume vida; lo dice el Javadoc de `LivesPolicy` en `tpi-roadmap` (`exemptFromLivesCheck()`). El tipo del FE (`roadmap.models.ts:53`) ya incluye `'LLM'`.
2. **La cantidad de vidas**: el roadmap no tiene ese campo y el banco limita a 3 (PAR-12). Mientras no exista:
   - **ocultar** «Vidas que descuenta» y «Vidas que recupera», junto con su aviso;
   - en la revisión, mostrar sólo «Consume vida», «No consume vida» o «Recupera vida».
3. Corregir el comentario de `LivesMode` y la sección «Pending in the roadmap: lives per node» de `docs/roadmap/e02-challenge-source.md`, que hoy dicen que falta la política sin vida.

**Tests:**

- «No consume vida» manda `livesPolicy: 'LLM'`.
- El selector de cantidad no se muestra.

---

## PR 4 — Mismo rango de XP y mismo límite de descripción en el alta y en la edición (alto) · Benja

**Qué pasa hoy:**

- **XP:** el alta acepta de 0 a 1000; el editor pide de 250 a 500 para un desafío Medio. Un desafío creado con 100 XP no se puede volver a guardar en el editor.
- **Descripción:** el alta permite 20.000 caracteres; la pantalla `/challenges/:id` corta en 500.

**Por qué pasa:**

- **XP:** la página de alta pisa el rango a mano en `rulesContext` con `xpRange: { min: 0, max: MAX_XP }`, donde `MAX_XP = 1000`. El editor usa `xpRangeFor(PAR-01, dificultad)` desde `challenge-draft-form.ts:288`. El Motor acepta de 0 a 100.000.
- **Descripción:** la pantalla de edición usa `CHALLENGE_DESCRIPTION_MAX = 500` (`challenges/utils/challenge-authoring.util.ts:11`). El alta usa `DESCRIPTION_HTML_MAX_LENGTH = 20000` (`challenges/utils/challenge-html.util.ts:6`). El Motor acepta 20.000 (`ChallengeTextLimits.DESCRIPTION_MAX_LENGTH`).

**Qué cambiar:**

1. **XP en la página de alta:** sacar el `xpRange` fijo de `rulesContext` y dejar el que ya calcula `this.form.settingsContext()`, que usa `xpRangeFor`. El valor por defecto (`defaultXp`, el XP del curso) se puede mantener; lo que tiene que ser igual en las dos pantallas es el **rango**. Borrar la constante `MAX_XP` si queda sin uso.
2. **Texto de ayuda del XP:** el alta dice «XP máxima… parte proporcional» y el editor dice «XP fijas». Revisar `requestWithXp`: cuando el profesor escribe un valor, el alta no fuerza `xpSemantics`. Elegir una sola semántica y usar la misma clave de ayuda en las dos pantallas.
3. **Descripción:** en la pantalla de edición, usar el mismo límite que el alta y el Motor (20.000). Antes, consultar en el grupo por qué está en 500: puede venir de una decisión de diseño de esa pantalla.

**Tests:**

- En la página de alta, un desafío Medio con XP 100 queda inválido.
- En la pantalla de edición, se acepta una descripción de 600 caracteres.

---

## PR 5 — Detalles del drawer y de la lista de nodos (medio) · Ludmila

Son cuatro arreglos chicos, todos en `roadmap/`.

### 5.1 «Cambios sin guardar» al abrir el drawer sin tocar nada

El badge sale de `dirty()` (`entity-editor-dialog.component.ts`, línea ~2986), que compara `initialValues()` contra `currentValues()` campo por campo. Algún campo arranca distinto de cómo se cargó; por ejemplo `null` contra `''`, o fechas en otro formato.

**Cómo encontrarlo:**

1. En un spec, abrir el drawer con un nodo como el de la prueba: desafío teórico, sin fechas, `allowed_retries: null`, `uses_ai: false`.
2. Loguear qué posición del array difiere.
3. Normalizar ese campo igual en los dos lados.

### 5.2 Una regla OR se lee como AND

En `roadmap/embeds/section-nodes/roadmap-section-nodes.component.ts` (línea ~986) se arma «Requiere: Sección: X, Nodo: Y» sin mirar el modo. Si el modo es OR, unir con «o» o agregar «(cualquiera)». Ya existen las claves `rulesWizard.node.requiresAny` y `requiresAll` para reutilizar.

### 5.3 El desafío creado se busca sólo en los primeros 100

`reportLinkedChallenge` (`roadmap/pages/graph-editor-page/graph-editor-page.component.ts`, línea ~2122) usa `getOwnChallenges({ size: 100 })` y busca por id en esa página. Un profesor con más de 100 desafíos ve «no se encontró el desafío». Conviene pedir ese desafío solo:

- `getChallenge(id)` trae `status`, que es lo único que usa;
- el título ya viaja en el estado de vuelta, o se puede leer con `getChallengeResource`.

### 5.4 «Añadir → Desafío» no hace nada si el curso no cargó

En `addChallenge()` (`roadmap-section-nodes.component.ts`, línea ~1515), el `if (!cohortId) return;` es silencioso. Dos opciones:

- deshabilitar la opción del menú mientras `courseCohortId()` está vacío;
- mostrar un `feedback.error` («El curso todavía se está cargando…»).

**De paso:** en el mismo archivo de `reportLinkedChallenge` hay un JSDoc viejo pegado encima del suyo. Borrarlo.

---

## PR 6 — Avisos duplicados y vuelta del editor (medio)

### 6.1 Toasts dobles al guardar · Iker

- `RoadmapStore.addActivityAt` y `updateAvailability` muestran «nodo agregado» y «disponibilidad guardada», y la página de alta además muestra su propio aviso.
- Agregar al store una opción para que no muestre feedback (por ejemplo un parámetro `{ silent: true }`) y usarla desde la página de alta.
- Con el PR 2, la de disponibilidad desaparece sola.
- Revisar también el caso de error: hoy salen el toast del store y el mensaje de la página.

### 6.2 El editor de desafíos, abierto sin contexto, vuelve a «Mis cursos» · Benja

Al guardar en `/challenges/:id/edit` sin `returnUrl`, debería quedarse en el desafío o volver a la pantalla anterior, no ir a la lista de cursos. Buscar en el componente de esa ruta dónde se navega después del `PUT` y usar un `returnUrl` por defecto razonable.

---

## PR 7 — Rendimiento y limpieza (bajo, opcional) · Benja

1. **403 en la página del curso para el profesor.** Algo de la lista de nodos pide `engine-challenge/.../students/me/.../counted-attempt` aunque quien mira es profesor. Buscar quién lo llama (grep `counted-attempt`) y condicionarlo a que el usuario sea alumno del curso.
2. **`catalog/manage` se pide 6 veces.** Se pide una vez por sección. Subir la carga a un nivel que se comparta (el store o el componente padre) o cachearla con `shareReplay`.
3. **El compositor embebido carga correcciones.** `compose-quiz-page` con `embedded` igual pide correcciones pendientes y conflictos. Saltear esas cargas cuando `embedded()` es `true`.
4. **El selector «Seleccioná el desafío que desbloquea este»** también lista nodos de Contenido. Hay que decidir en el grupo entre:
   - renombrarlo («Seleccioná el nodo…»);
   - filtrar sólo desafíos.
5. **`pt.json`** tiene la clave `errorTitle` duplicada (líneas ~15719 y ~15721). Borrar una.
6. **El chequeo de i18n** no detecta claves usadas en templates que faltan en los JSON. Agregar esa validación. Al 03/11, `myQuiz.edit.backToCatalog` (`compose-quiz-page.component.html:107`) sigue faltando en `es.json`, `en.json` y `pt.json`.

---

## Prueba final de punta a punta

Cuando esté todo mergeado, en un curso de prueba y con una cuenta de profesor:

1. Crear un desafío teórico con «No consume vida».
   - El nodo nace no disponible, con `lives_policy: LLM`, en un solo `POST`.
2. Editar el desafío.
   - Un XP de 100 en un desafío Medio marca error; con 300, guarda.
3. Ponerle prerrequisitos «Unidad 1 O (otro nodo)».
   - El curso muestra que alcanza con cualquiera de los dos.
4. Abrir el drawer sin tocar nada.
   - No aparece «Cambios sin guardar».
