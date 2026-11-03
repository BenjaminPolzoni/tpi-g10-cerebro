---
tags: [tpi, g10, sprint-4, plan, front, courses, roadmap, performance]
fecha: 2026-11-02
autor: Benjamin Polzoni
estado: implementado (falta medir como alumno)
repo: 2026-PIV-TPI-FE
rama: feature/simple-view-mark-read
base: 9f9947114 (2026-11-02)
---

# Front · Carga más rápida de la vista simple del curso

> [!info] Alcance
> La pestaña **General** del curso (vista simple del alumno) tarda varios segundos en abrir. Medido el 2026-11-02 en el front local (`127.0.0.1:8000`, sesión de profe, imagen previa a `9f9947114`): **cada pedido tarda ~200 ms en el servidor, pero los últimos esperan ~2,8 s en cola en el navegador**. El edge sirve por HTTP/1.1 (6 conexiones por host) y la página dispara ~60 pedidos. Este plan baja la cantidad de pedidos que compiten con lo que el alumno necesita para ver el curso y corta los escalones encadenados del arranque. Sólo front; lo que necesita back o infra queda listado al final.

## Medición base

| Tramo (ms) | Qué pasa |
|---|---|
| 0 – 1143 | sesión → membresía → curso (encadenados) |
| 1144 – 1780 | `participants` ×2 (635 ms); secciones y roadmap **recién salen al terminar** |
| 1780 – 2200 | secciones (349), roadmap (402), grupos, parámetros, en paralelo |
| 2135 – 5200 | `/contents` ×23 (una por tarjeta), `/restrictions` ×11, `engine-challenge/.../nodes/:id/...` ×20, `market/catalog/manage` ×4 |

Un `/contents` típico: cola 2738 ms · servidor 212 ms · descarga 3 ms.

Verificado: `GET /course/course-cohorts/:id/contents?include_sections=true` devuelve sólo el contenido del curso (1 ítem), no el de las secciones. Juntar `/contents` en un pedido **no** es posible sin cambiar Cursos.

## Ya hecho en la rama

- `9f9947114` el alumno abre el roadmap apenas conoce el curso, en paralelo con las secciones (antes lo abría cada tarjeta al montarse).
- `5c4053706` / `2cf0076e1` pantalla de carga única (avatar corriendo) que espera roadmap + progreso + archivos de las tarjetas abiertas (`SectionLoadTracker`).

## Tareas

### T-1 · Pedidos secundarios después de mostrar el curso

Los intentos contados de cada desafío (`NodeFeedbackService.countedAttempt`, uno por desafío desbloqueado, en `section-resources-container.component.ts` → `loadCountedAttemptsEffect`) no son parte de lo que el alumno necesita para ver la unidad, pero compiten en la cola con `/contents`, roadmap y progreso.

- `SectionLoadTracker` (`cohort-general-page/section-load-tracker.ts`) suma una señal `settled` (empieza en `false`) y un `markSettled()`.
- `CohortGeneralPageComponent`: cuando `studentWaiting()` pasa a `false` por primera vez, llama `markSettled()`. Para quien no es alumno se marca de entrada (no hay pantalla de carga que esperar).
- `SectionResourcesContainerComponent.loadCountedAttemptsEffect` no dispara pedidos hasta que `tracker?.settled() ?? true`.
- Resultado esperado: el estado del desafío aparece con la pantalla; la nota del intento contado (p. ej. «67/10») se completa un instante después. Es la única diferencia visible y es aceptada.

### T-2 · Guard de encuestas pendientes una sola vez por navegación

`pendingSurveyGuard` está como `canActivate` **y** `canActivateChild` de `:cohortId` (`courses.routes.ts`). Para un alumno cada uno llama a `SurveysService.refreshPendingSurveys()`, y los guards corren en serie antes de que la página monte.

- Confirmar en el código cuántas veces se dispara en una entrada a `/courses/:id/general` (leer `refreshPendingSurveys`).
- Si son dos: reutilizar el pedido en curso y su respuesta durante unos segundos (p. ej. `shareReplay` con vencimiento corto en `SurveysService`, o cachear el resultado por navegación). Una encuesta nueva debe seguir detectándose en la próxima navegación.
- Si ya es uno, no tocar y anotarlo en el reporte.

### T-3 · Escalón `participants` antes de secciones y roadmap

En la medición del profe, `sections`/`roadmaps`/roadmap salen en el ms 1780, justo cuando termina `participants` (1144–1779), aunque el curso ya estaba cargado en el ms 1143.

- Encontrar qué hace esperar a `CohortGeneralPageComponent` (layout `cohort-layout-page`, guards de la ruta `general`, `UserCapabilitiesService`, `CohortContextFacade`, o la página que no monta hasta tener algo).
- Si la causa es de front y el arreglo es chico (no esperar algo que la página no usa para pedir secciones/roadmap), arreglarlo. Si no, documentar la causa en el reporte sin cambiar código.

## Avance (2026-11-03)

- T-1 `879390751`: intentos contados recién cuando el curso ya se muestra.
- T-2 `e5052e142`: era doble; las encuestas pendientes se piden una vez por navegación.
- T-3 `fa7565b0b`: `getCohortByIdProgressively` emite el curso base al instante y el enriquecido (equipo docente) después; el layout ya no espera a `participants`. `getCohortById` no cambió para el resto.
- Pendiente: rebuild + medición como alumno contra la tabla base.

## Restricciones

- Leer `AGENTS.md` antes de tocar código. Signals, sin `NgModule`, sin `@Input/@Output`, OnPush.
- Rama actual `feature/simple-view-mark-read`, sin ramas ni PRs nuevos.
- **No correr tests ni `npm run verify`.** Validar con `npx ngc -p tsconfig.app.json --noEmit` (sin errores) y eslint/prettier de los archivos tocados.
- Un commit por tarea con `git commit -- <rutas>`; el pre-commit corre (no usar `--no-verify`).
- No cambiar textos visibles salvo que una tarea lo pida; si agregás claves i18n, en es/en/pt.

## Aceptación

- T-1, T-2 y T-3 commiteadas (o T-2/T-3 justificadas como "sin cambio" en el reporte).
- Reporte final con: archivos tocados, causa encontrada en T-3, y si T-2 era doble.
- Validación posterior (Benja): rebuild del front local y nueva medición como **alumno** con la Performance API, comparando contra la tabla base.

## Fuera de este plan (back / infra)

| Qué | Dónde | Efecto |
|---|---|---|
| HTTP/2 en el nginx del edge | compose de la plataforma | elimina la cola de 6 conexiones; el mayor impacto |
| `/contents` de todas las secciones en un pedido (`include_sections` hoy ignora las secciones) | Cursos | 23 → 1 pedido |
| Intentos contados en lote por curso | engine-challenge | N → 1 pedido |
| Restricciones de todas las secciones en un pedido | Cursos | 11 → 1 pedido |
