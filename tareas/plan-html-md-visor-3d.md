# Plan — HTML y Markdown de la vista simplificada en el visor 3D

> **Autor / responsable del plan:** Benjamin Polzoni (`412056-1w3-Polzoni-Benjamin`)  
> **Fecha:** 2026-10-26  
> **Estado:** propuesto; **no implementado ni validado de extremo a extremo**.  
> **Objetivo:** que los archivos `.html` y `.md` cargados por un profesor en la vista simplificada/sobria se **previsualicen dentro del visor de contenido del mundo 3D**, siguiendo el patrón del visor de PDF. La acción primaria debe ser **ver**, no descargar el archivo ni abrir otra pestaña. Un botón secundario de descarga puede mantenerse, pero nunca debe ser necesario para leer el material.

## 1. Diagnóstico: no son dos cargas equivalentes

La revisión corresponde a `origin/develop` del frontend y del servicio Roadmap, no al checkout principal del frontend (`feature/roadmap-ghost-phantoms`), que no incluye este flujo. La vista simplificada ya permite importar HTML y Markdown mediante `entity-editor-dialog.component.ts` (aprox. líneas 1057–1129). El HTML pasa por `course-html-page.service.ts` (aprox. líneas 38–72): se sube y confirma como contenido `FILE` con `text/html`, vinculado por `contentId` a la sección. Markdown se importa como archivo `FILE` `.md`. **No se trata de `SectionSettings.content.html/Markdown`**, que es el cuerpo de una sección y sigue otro flujo.

El recorrido de publicación del HTML es `POST /course/course-cohorts/{cohortId}/contents` con `type=FILE`, `courseSectionId`, `fileName`, `contentType=text/html` y tamaño → `PUT` a URL de carga firmada → `POST /course/course-contents/{contentId}/confirm`. El editor guarda el `content.id` devuelto y el adaptador Roadmap crea el nodo en `POST /sections/{sectionId}/nodes`, seguido de `PATCH /nodes/{nodeId}/content` con ese `contentId`. Esta unión debe verificarse con la misma identidad de contenido en el caso E2E.

El mundo 3D **ya posee una rama de visor HTML**, por lo que no corresponde diseñarlo desde cero: `roadmap/domain/material-access.ts` (aprox. 43–77) clasifica HTML solo cuando la URL es del mismo origen y su *pathname* termina en `.html`; no clasifica Markdown. `material-access.component.ts` (aprox. 182–198 y 305–318) ya tiene `renderHtmlPage`/`HtmlPageFrameComponent` para obtener el texto y mostrarlo dentro del visor. `hex-world-page.component.html` (aprox. 391–406) pasa el `NodeMaterial` al visor. En la rama HTML la petición `fetch` no depende de `Content-Disposition`; PDF ya crea un `Blob`/URL de objeto para evitar que una respuesta `attachment` fuerce la descarga. Por lo tanto, que hoy el HTML termine en descarga indica que **la URL real probablemente no está entrando en la rama HTML**, pero la causa exacta sigue sin probarse (origen, ruta opaca, extensión, clasificación u otro fallo). Los tests existentes usan URL simulada y **no demuestran** que la URL real producida por Courses satisfaga detección, autorización y lectura desde el navegador.

Roadmap guarda `contentId` y expone al frontend materiales con `type`, `status`, `accessUrl` y expiración en `NodeDetailDto.Material`, pero **no aporta MIME ni nombre de archivo**. Para nodos **COURSE** asociados a una sección, `GraphValidator.java` (aprox. 261–265) y `NodeDetailService.java` (aprox. 141–147) consultan la ruta de actividades, y `HttpCoursesMaterialClient.materialOf.java` (aprox. 133–137) conserva la URL recibida. En nodos **OWN**, sin sección, se consulta otra ruta de contenidos de comisión y `HttpCoursesMaterialClient.java` (aprox. 90–115) descarta `accessUrl`/expiración. **Esto último no es la causa demostrada de un fallo del flujo COURSE normal** y no debe mezclarse con el objetivo principal.

El repositorio fuente de Courses no está disponible localmente en estas worktrees. Su contrato real de `accessUrl`, descarga y permisos debe confirmarse con el equipo/servicio antes de cerrar el diseño. El frontend ya dispone de `GET /course/course-contents/{id}/download-url?disposition=attachment`; `CourseHtmlPageService.render` obtiene esa URL y después hace `fetch` del texto con `credentials: omit`. También existe `SectionMarkdownComponent`/su renderer de vista previa, reutilizable para el Markdown del alumno con los ajustes de seguridad y contexto necesarios. El visor 3D, en cambio, consume `Roadmap material.accessUrl`, detecta mismo origen y extensión en el *pathname* (ignora la query firmada), y hace `fetch` con `credentials: omit`. Evaluar si se puede compartir la resolución del frontend sin cambiar el DTO de Roadmap. `disposition=attachment` no demuestra por sí mismo un problema para `fetch`; los riesgos por comprobar son URL nula, vencida, 403, origen cruzado, CORS u *opaque path* sin extensión.

## 2. Contrato funcional propuesto

1. **Identidad estable:** el material publicado conserva `contentId`, tipo de archivo/MIME y relación con la sección. No inferir identidad ni seguridad de un nombre de archivo.
2. **Disponibilidad:** el alumno matriculado ve el material solo si el nodo está desbloqueado/publicado, mediante el detalle autorizado de Roadmap; no saltar `NodeDetailService` ni las reglas de Courses.
3. **Resolución:** para HTML y Markdown, el frontend obtiene una URL vigente con el contrato aprobado (`NodeDetailDto.Material.accessUrl` o `GET /course/course-contents/{id}/download-url`). Evitar que la extensión de una URL firmada sea el único discriminador: decidir, según la URL real, si hace falta agregar `mimeType`/`fileName` opcionales al contrato Courses → Roadmap → FE. No agregar un cambio de backend especulativo.
4. **Presentación:** HTML y Markdown se ven **dentro del panel/visor de contenido del mundo 3D**, como el PDF, con estados de carga, vencimiento, error y reintento. La acción principal nunca es la descarga; esta puede ofrecerse de manera secundaria. PDF, imágenes, video y enlaces conservan su comportamiento.
5. **Seguridad:** HTML de usuario es contenido no confiable. Mantener o reforzar sanitización, `iframe` con sandbox restrictivo, CSP aplicable, sin scripts ni navegación superior, `credentials: omit` al recuperar el archivo cuando corresponda y sin ejecutar HTML arbitrario en el origen de la app. Validar el origen/host permitido de la descarga sin romper URL firmadas legítimas. No usar `bypassSecurityTrustHtml` para el documento sin aislamiento.
6. **Markdown:** `.md` es alcance **P0 obligatorio**. Recuperar su texto, renderizarlo de forma segura en el visor existente y reutilizar el renderer de vista previa de `SectionMarkdownComponent` cuando corresponda; no tratar Markdown como HTML crudo. Definir la misma política para `.markdown` y cubrir enlaces e imágenes relativas.

## 3. Trabajo por fases y responsables

### Fase 0 — Reproducir el contrato real (Front + Courses + Roadmap)

- [ ] Crear en entorno integrado una sección COURSE con un `.html` y un `.md` desde la vista sobria; publicar y abrir los nodos correspondientes con usuario alumno matriculado. Confirmar el síntoma actual: el visor ofrece descarga como acción principal en vez de previsualización.
- [ ] Capturar, sin registrar tokens ni firmas, forma del `contentId`, respuesta del detalle de Roadmap, `type/status/accessUrl/expiresAt`, URL de Courses, método de autenticación, `Content-Type`, `Content-Disposition`, CORS y redirecciones. Verificar origen, extensión en *pathname*, query firmada, ruta sin extensión, vencimiento y viabilidad de `fetch` desde navegador tanto para HTML como Markdown.
- [ ] Confirmar con Courses el contrato `GET /course/course-contents/{id}/download-url` y si la URL requiere renovar firma. Validar que el archivo confirmado como `text/html` aparece en la ruta `/activities` de la sección.
- [ ] Documentar exactamente dónde falla hoy el flujo real antes de cambiar código: publicación, proyección, URL, clasificador del visor, fetch o aislamiento.

**Salida:** traza reproducible y decisión de contrato FE–Roadmap–Courses, sin exponer URLs firmadas en Obsidian.

### Fase 1 — Frontend: previsualizar HTML y Markdown en 3D (P0)

- [ ] En la capa de acceso a materiales, clasificar `.html`, `.htm`, `.md` y `.markdown` aun cuando la URL sea firmada, tenga query u origen distinto. Priorizar tipo/MIME o nombre de archivo confiable cuando estén disponibles; conservar detección por extensión solo como compatibilidad segura. Si el DTO no aporta metadatos, evaluar resolución por `contentId` mediante Courses y comprobar respuesta real antes de pedir campos nuevos al backend.
- [ ] Reutilizar la lógica de carga/render de `CourseHtmlPageService` donde tenga sentido, sin acoplar el visor 3D al editor del profesor. Definir un adaptador/servicio compartido si evita duplicar obtención, renovación y errores.
- [ ] Alimentar el visor actual (`material-access.component`) desde `hex-world-page` sin alterar la navegación del mundo 3D. Para HTML, aprovechar `renderHtmlPage`/`HtmlPageFrameComponent`; para Markdown, hacer `fetch` del texto y render seguro en el mismo panel/drawer, reutilizando el renderer de `SectionMarkdownComponent` si procede. Evitar que un `Content-Disposition: attachment` lance la descarga como resultado de la acción primaria. Manejar URL vencida y renovación, ausencia de permisos, archivo no disponible, `Content-Type` incorrecto, redirección, CORS y fallo de red con mensaje y reintento controlado.
- [ ] Revisar las garantías de `iframe` sandbox/sanitización/CSP y la liberación de URLs objeto. **No incrustar la URL firmada de HTML crudo directamente en un `iframe`, ni relajar el sandbox, habilitar scripts o credenciales** para “hacer funcionar” una prueba. Aplicar sanitización y política de enlaces al Markdown.
- [ ] Añadir pruebas unitarias/de componente para `.html`, `.htm`, `.md`, `.markdown`, URL con query, URL firmada sin extensión y de otro origen, ruta `contentId`/URL, render embebido, `attachment`, XSS, errores y regresiones de otros tipos.

**Salida:** HTML y Markdown publicados visibles dentro del visor 3D para el flujo COURSE, sin descarga forzada, con pruebas locales.

### Fase 2 — Backend únicamente según evidencia de Fase 0 (P0 condicional)

- [ ] Si Roadmap `/activities` ya devuelve `contentId` y URL utilizable, **no modificar backend** por costumbre. Mantener sus controles de matrícula, publicación y desbloqueo.
- [ ] Si la proyección pierde el vínculo o la URL, corregir mapeo/DTO en `tpi-roadmap`, con test de cliente Courses y de `NodeDetailService`. Coordinar con Courses cualquier cambio en respuesta/MIME o endpoint; su repo no está en las worktrees creadas.
- [ ] Si la URL real no permite identificar confiablemente HTML y Markdown, agregar `mimeType`/`fileName` opcionales y retrocompatibles al contrato, con pruebas para materiales antiguos y despliegue coordinado Courses → Roadmap → FE. No usar la extensión de la URL firmada como contrato estable.
- [ ] Verificar autorización en backend para `download-url` y que una URL firmada no habilite un material bloqueado por acceso directo.

**Salida:** contrato consistente y cubierto por tests; cambio de backend solo si una falla real lo exige.

### Fase 3 — Variante OWN (P1, fuera del bloqueo P0)

- [ ] Confirmar si el profesor debe publicar HTML de la vista sobria en nodos **OWN** además de COURSE. OWN sin sección utiliza contenidos de comisión y hoy el cliente Roadmap no propaga URL/expiración en esa ruta; estudiar primero cómo asociar un `contentId` de sección. No aplicar el arreglo de OWN como condición para el caso COURSE.

**Salida:** alcance explícito y, si se aprueba, pruebas adicionales sin degradar P0.

### Fase 4 — Validación integrada y entrega

- [ ] E2E con profesor que importa/publica `.html` y `.md` en vista sobria y alumno que abre los **mismos `contentId`** desde sus nodos COURSE en 3D; comprobar visualmente que ambos aparecen *dentro* del visor, sin descarga ni pestaña nueva como requisito para leer.
- [ ] Repetir para `.htm`, `.markdown`, URL con query, URL firmada sin extensión y de otro origen, URL recién emitida y vencida/renovada, respuesta `attachment`, alumno no matriculado, nodo bloqueado, archivo eliminado/no confirmado, HTML con script, Markdown malicioso, URL externa y PDF/imagen/video.
- [ ] Registrar evidencias sin tokens, URLs firmadas ni contenido sensible; anotar commits/PR de FE, Roadmap y Courses si hubo cambios, y el orden de despliegue.

## 4. Criterios de aceptación

- [ ] Un `.html`/`.htm` y un `.md`/`.markdown` importados desde la vista simplificada, confirmados y publicados en una sección COURSE se **previsualizan dentro del visor de contenido del mundo 3D** por un alumno autorizado. Ninguno exige descargar el archivo para leerlo; la descarga, si existe, es una acción secundaria explícita.
- [ ] El HTML y Markdown renderizados corresponden a sus `contentId` publicados; una URL temporal vencida tiene renovación o error explícito, nunca una pantalla vacía indefinida.
- [ ] Nodo bloqueado/alumno no autorizado no entrega contenido; HTML malicioso no ejecuta scripts, no navega la app y no accede a cookies/credenciales.
- [ ] El visor de PDF, imagen, video y enlace externo no presenta regresiones.
- [ ] Markdown se muestra como contenido legible y seguro en el mismo panel/drawer del visor 3D; enlaces/imágenes relativas, archivo vacío y contenido malicioso tienen comportamiento probado.
- [ ] Existe al menos una prueba integrada con backend real o entorno de integración; los mocks de URL no bastan como cierre.

## 5. Worktrees preparadas y preguntas abiertas

| Equipo | Worktree Orca | Rama | Estado |
|---|---|---|---|
| Frontend | `/Users/benjaminpolzoni/orca/workspaces/2026-PIV-TPI-FE/html-content-3d-viewer-front` | `BenjaminPolzoni/html-content-3d-viewer-front` | Creada desde `origin/develop`; sin implementación de este plan. |
| Backend Roadmap | `/Users/benjaminpolzoni/orca/workspaces/tpi-roadmap/html-content-3d-viewer-back` | `BenjaminPolzoni/html-content-3d-viewer-back` | Creada desde `origin/develop`; cambio condicional a la evidencia. |

**Por resolver antes de implementar:** (1) contrato real de Courses, origen/CORS y expiración de la URL; (2) si hacen falta metadatos opcionales para clasificar HTML/Markdown; (3) si OWN forma parte del requerimiento posterior; (4) responsable de cambios en Courses si fueran necesarios. **El visor embebido de `.md` y `.html` no es opcional.** Ninguna worktree implica que ya exista una solución ni que el flujo haya pasado E2E.
