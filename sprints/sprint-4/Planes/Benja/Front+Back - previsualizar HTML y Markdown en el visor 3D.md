---
tags: [tpi, g10, sprint-4, plan, front, back, visor-3d, html, markdown, pdf]
fecha: 2026-10-26
autor: Benjamin Polzoni
estado: plan listo - pendiente de implementación (solo Front; Back condicional)
repo: 2026-P4-FE/2026-PIV-TPI-FE (tpi-roadmap solo si falla el supuesto de permisos)
---

# Front + Back — Previsualizar HTML, Markdown y PDF en el visor 3D

> [!important] Objetivo
> En el mundo 3D, el alumno abre el material del nodo (`.html`, `.md`, `.pdf`) **dentro del visor (drawer) del roadmap**, sin descargar nada ni abrir otra pestaña. Es lo mismo que ya hace la vista simple (`/courses/:id/files/:contentId` y `/courses/:id/general/pages/:contentId`). Descargar queda, si acaso, como acción secundaria.
>
> Antecedente: [[sprints/sprint-3/Planes/Benja/Front+Back - previsualizar HTML y Markdown en el visor 3D|plan de Sprint 3]] (hipótesis). Esta nota lo reemplaza con el diagnóstico sobre el código de `origin/develop` (FE `8fe1b354f`+, roadmap `develop`).

## Diagnóstico (código leído, 2026-10-26)

### Por qué la vista simple funciona

- Sabe **qué es** el archivo por los metadatos de Courses: `CourseContent.contentType` / `fileName` → `contentPreviewKindOf()` (`courses/data-access/content-preview.ts`) e `isHtmlPage()` (`courses/data-access/html-page.ts`).
- **Lee el archivo con `fetch`** (`credentials: 'omit'`), sin navegar a él: `loadContentPreview()` arma un blob `application/pdf` para el PDF, texto para Markdown/CSV/txt; el HTML se lee con `CourseHtmlPageService.read()` y se muestra con `renderHtmlPage()` en `HtmlPageFrameComponent` (sandbox, sin scripts).
- Un `fetch` **nunca dispara una descarga**, aunque Storage responda `Content-Disposition: attachment`.

### Por qué el 3D descarga "algo raro"

Único punto de entrada: `roadmap/ui/material-access/material-access.component.ts`, que usa `hex-world-page` con `d.material` del detalle de nodo (`GET /courses/{id}/nodes/{nodeId}`).

1. **Clasifica por la extensión del *pathname* de la URL firmada** (`embeddedViewerOf()` en `roadmap/domain/material-access.ts`). La URL de Storage es una clave opaca: casi nunca termina en `.html`, `.md` ni `.pdf`. Entonces `viewer()` queda `undefined` → `mode()` = `'download'` → `<a download>` baja un archivo con el nombre de la clave y sin extensión. Esa es la "descarga rara".
2. **No existe la rama Markdown** en el visor 3D (`EmbeddedViewer = 'pdf' | 'video' | 'image' | 'html'`).
3. **El PDF depende de un *probe* de `Content-Disposition`** (`probeMaterialDisposition`): si Roadmap trae la URL firmada `attachment`, `mode()` = `'download'` aunque el visor ya lea los bytes con `fetch` + blob, es decir, aunque no haga falta. El *probe* sobra.
4. **Exige el mismo origen** (`/_s3`) para todo. Con `fetch` + blob/srcdoc no hay iframe apuntando a Storage, así que solo importa CORS, y la vista simple demuestra que el `fetch` a esas URLs ya anda.

### Back: no hace falta tocarlo

- `NodeDetailDto.Material` (roadmap) trae `contentId`, `type`, `status`, `accessUrl` y `accessUrlExpiresAt`. Le faltan MIME y nombre (el `Item` de `HttpCoursesMaterialClient` tampoco los lee), pero **el Front ya tiene `contentId` y `courseCohortId` (`aid()`)**: con eso obtiene `contentType`/`fileName` de Courses (`CourseContentService.listContents(cohort, undefined, includeSections=true)`), como hace la vista simple.
- La `accessUrl` de Roadmap sirve tal cual para el `fetch`: la disposición deja de importar.
- Las rutas de la vista simple (`files/:contentId`, `general/pages/:contentId`) no tienen `cohortProfessorGuard` y los alumnos ya listan contenidos de Courses. **Supuesto a verificar en la tarea 1.**

## Plan

### T1 — Verificar el supuesto (15 min, sin código)

- [ ] Como alumno matriculado, en el 3D, abrir un nodo `COURSE` con `.html`, otro con `.md` y otro con `.pdf`. En DevTools, comprobar que `GET /course/course-cohorts/{aid}/contents?include_sections=true` responde 200 y trae ese `contentId` con `content_type`/`file_name`, y que `fetch(accessUrl, {credentials:'omit'})` responde 200 (CORS OK). No pegar URLs firmadas en ningún lado.
- [ ] Si falla el listado por permisos → ir a **T5 (Back)**. Si no, el cambio es **solo Front**.

### T2 — Front: clasificar con metadatos de Courses (`material-access`)

Archivos: `roadmap/ui/material-access/material-access.component.ts`, `roadmap/domain/material-access.ts`, `hex-world-page.component.html`.

- [ ] Nuevo `input` `courseCohortId` en `MaterialAccessComponent`. `hex-world-page` le pasa `aid()`.
- [ ] Buscar el `CourseContent` del material con `CourseContentService.listContents(() => material ? cohortId : undefined, () => undefined, () => true)` y elegir el ítem con `id === material.contentId`.
- [ ] Tipo de visor (`kind`):
  - `isHtmlPage(content)` → `'html'` (rama existente: `loadMaterialHtml` + `renderHtmlPage` + `app-html-page-frame`).
  - si no, `contentPreviewKindOf(content)` → `'pdf' | 'markdown' | 'text' | 'table' | 'image' | 'video' | 'none'`.
  - Sin `CourseContent` (lista con error o ítem ausente), dejar `embeddedViewerOf(url)` como compatibilidad (mocks y URLs con extensión).
- [ ] `mode()`: material `FILE` con `kind !== 'none'` → `'view'`, sin importar el origen ni la disposición. `LINK` u otro tipo → `'external'`, como hoy. `'none'` (Word/Excel/PPT) → `'download'`, como hoy.
- [ ] **Eliminar** el `resource` `disposition`, el input `probe` y `probeMaterialDisposition` (más sus tests): el visor lee con `fetch`, así que la disposición no importa. Revisar con `grep` que no tengan otros usos.

### T3 — Front: renderizar con el visor de la vista simple

- [ ] Reemplazar el `@switch` de pdf/video/image del drawer por `<app-content-preview [preview]="preview.value()" [fileName]="m.title">` (`courses/ui/content-preview`), alimentado por un `resource` que, con el drawer abierto, llama `inject(CONTENT_PREVIEW_LOADER)(kind, accessUrl, abortSignal)`. Así entran **Markdown, txt y CSV gratis**, con el mismo renderer saneado (`renderMarkdown`) de la vista simple.
- [ ] Mantener `keepObjectUrl` para liberar el blob del PDF (el `ContentPreview` `pdf` trae `objectUrl`). Borrar el `resource` `pdf`, `frameUrl` y `loadMaterialPdf` si quedan sin uso.
- [ ] HTML: queda con su rama actual (`htmlPage` + `HtmlPageFrameComponent`), disparada por el nuevo `kind`.
- [ ] Estados: carga (skeleton/spinner), error con mensaje (`materialAccess.*Failed`, agregar `markdownFailed` o uno genérico `viewFailed` en i18n es/en). La URL vencida sigue con `renewalRequested`, igual que hoy.
- [ ] Acción secundaria: dejar "Abrir en pestaña nueva" **solo** para `image`/`video` (el navegador no descarga esos tipos). Para `pdf`/`markdown`/`html` no ofrecer el link crudo, porque con disposición `attachment` descargaría.

### T4 — Tests (solo los pertinentes)

- [ ] `material-access.component.spec.ts`: con `CourseContent` de tipo `text/html`, `text/markdown` (y `.md` con MIME vacío) y `application/pdf`, y una URL **sin extensión**: aparece "Ver"; al abrir se renderiza el frame HTML, el markdown o el PDF (loader fake). Ningún `<a download>`.
- [ ] Con `.docx` → "Descargar". `LINK` → nueva pestaña. Lista de Courses con error → *fallback* por extensión.
- [ ] URL vencida → `renewalRequested`, sin abrir el visor.
- [ ] Borrar los tests del *probe*. Correr solo `material-access*.spec.ts` y `content-preview*.spec.ts`, no la suite completa. Push del FE con `NODE_OPTIONS=--no-experimental-webstorage`.

### T5 — Back (condicional: solo si T1 muestra que el alumno no puede listar contenidos)

- [ ] Courses → Roadmap: leer `file_name`/`content_type` en `HttpCoursesMaterialClient.Item` (si Courses los expone en el endpoint de materiales; si no, pedírselo al equipo de Courses) y propagarlos en `CourseMaterial` → `NodeDetailDto.Material` como campos opcionales `fileName`/`contentType`. Agregar test del cliente y del detalle de nodo.
- [ ] Front: `NodeMaterial` suma `fileName?`/`contentType?`. T2 los usa en lugar del listado de Courses (`contentPreviewKindOf({type:'FILE', fileName, contentType, ...})`).

### T6 — Validación de cierre

- [ ] E2E manual: el profesor sube un `.html` (Código HTML), un `.md` y un `.pdf` en la vista simple y los vincula a nodos `COURSE`. El alumno los abre en el 3D: los tres se ven en el drawer y **no hay ninguna descarga ni pestaña nueva** (pestaña Descargas vacía).
- [ ] Un HTML con `<script>alert(1)</script>` y `onerror=` no ejecuta nada (sandbox). Un Markdown con `[x](javascript:...)` no queda como link activo.
- [ ] Regresión: imagen y video siguen andando, `.docx` descarga, `LINK` abre en pestaña nueva, nodo bloqueado sin material, URL vencida que se renueva.

## Fuera de alcance

- Nodos `OWN` (material propio del roadmap): ruta distinta. Investigarlo aparte si aparece el mismo síntoma.
- Ejecutar scripts del HTML del profesor: el sandbox sin scripts se mantiene a propósito.

## Ramas (Orca)

| Parte | Rama | Worktree |
|---|---|---|
| Front | `BenjaminPolzoni/html-content-3d-viewer-front` | `~/orca/workspaces/2026-PIV-TPI-FE/html-content-3d-viewer-front` |
| Roadmap back (solo T5) | `BenjaminPolzoni/html-content-3d-viewer-back` | `~/orca/workspaces/tpi-roadmap/html-content-3d-viewer-back` |
