# Plan — HTML y Markdown de la vista simplificada en el visor 3D

> **Autor / responsable del plan:** Benjamin Polzoni (`412056-1w3-Polzoni-Benjamin`)  
> **Fecha:** 2026-10-26  
> **Estado:** propuesto; **no implementado ni validado de extremo a extremo**.  
> **Objetivo:** que el material `.html` cargado por un profesor en la vista simplificada/sobria de un curso se vea dentro del visor de contenido del mundo 3D del alumno, sin abrir otra pestaña. Mantener una ruta explícita para `.md`.

## 1. Diagnóstico: no son dos cargas equivalentes

La revisión corresponde a `origin/develop` del frontend y del servicio Roadmap, no al checkout principal del frontend (`feature/roadmap-ghost-phantoms`), que no incluye este flujo. La vista simplificada ya permite importar HTML y Markdown mediante `entity-editor-dialog.component.ts` (aprox. líneas 1057–1129). El HTML pasa por `course-html-page.service.ts` (aprox. líneas 38–72): se sube y confirma como contenido `FILE` con `text/html`, vinculado por `contentId` a la sección. Markdown se importa como archivo `FILE` `.md`. **No se trata de `SectionSettings.content.html/Markdown`**, que es el cuerpo de una sección y sigue otro flujo.

El recorrido de publicación del HTML es `POST /course/course-cohorts/{cohortId}/contents` con `type=FILE`, `courseSectionId`, `fileName`, `contentType=text/html` y tamaño → `PUT` a URL de carga firmada → `POST /course/course-contents/{contentId}/confirm`. El editor guarda el `content.id` devuelto y el adaptador Roadmap crea el nodo en `POST /sections/{sectionId}/nodes`, seguido de `PATCH /nodes/{nodeId}/content` con ese `contentId`. Esta unión debe verificarse con la misma identidad de contenido en el caso E2E.

El mundo 3D **ya posee una rama de visor HTML**, por lo que no corresponde diseñarlo desde cero: `roadmap/domain/material-access.ts` (aprox. 43–77) reconoce una URL `.html` del mismo origen; `material-access.component.ts` (aprox. 182–198 y 305–318) obtiene el texto y lo muestra en un `iframe` seguro; `hex-world-page.component.html` (aprox. 391–406) pasa el `NodeMaterial` al visor. Esto solo prueba capacidad por inspección; los tests existentes usan URL simulada y **no demuestran** que la URL real producida por Courses satisfaga la detección, autorización y descarga.

Roadmap guarda `contentId` y expone al frontend materiales con `type`, `status`, `accessUrl` y expiración en `NodeDetailDto.Material`. Para nodos **COURSE** asociados a una sección, `GraphValidator.java` (aprox. 261–265) y `NodeDetailService.java` (aprox. 141–147) consultan la ruta de actividades, y `HttpCoursesMaterialClient.materialOf.java` (aprox. 133–137) conserva la URL recibida. En nodos **OWN**, sin sección, se consulta otra ruta de contenidos de comisión y `HttpCoursesMaterialClient.java` (aprox. 90–115) descarta `accessUrl`/expiración. **Esto último no es la causa demostrada de un fallo del flujo COURSE normal** y no debe mezclarse con el objetivo principal.

El repositorio fuente de Courses no está disponible localmente en estas worktrees. Su contrato real de `accessUrl`, descarga y permisos debe confirmarse con el equipo/servicio antes de cerrar el diseño. El frontend ya dispone de `GET /course/course-contents/{id}/download-url?disposition=attachment`; `CourseHtmlPageService.render` obtiene esa URL y después hace `fetch` del texto con `credentials: omit`. El visor 3D, en cambio, consume `Roadmap material.accessUrl`, detecta mismo origen y extensión en el *pathname* (ignora la query firmada), y hace `fetch` con `credentials: omit`. Evaluar si se puede compartir la resolución del frontend sin cambiar el DTO de Roadmap. `disposition=attachment` no demuestra por sí mismo un problema para `fetch`; los riesgos por comprobar son URL nula, vencida, 403, origen cruzado u *opaque path* sin `.html`.

## 2. Contrato funcional propuesto

1. **Identidad estable:** el material publicado conserva `contentId`, tipo de archivo/MIME y relación con la sección. No inferir identidad ni seguridad de un nombre de archivo.
2. **Disponibilidad:** el alumno matriculado ve el material solo si el nodo está desbloqueado/publicado, mediante el detalle autorizado de Roadmap; no saltar `NodeDetailService` ni las reglas de Courses.
3. **Resolución:** para HTML, el frontend obtiene una URL vigente con el contrato aprobado (`NodeDetailDto.Material.accessUrl` o `GET /course/course-contents/{id}/download-url`). Evitar que la extensión de una URL firmada sea el único discriminador: usar metadatos confiables si la prueba real demuestra que hace falta. No agregar un cambio de backend especulativo.
4. **Presentación:** el HTML se ve **dentro del panel/visor del mundo 3D**, con estados de carga, vencimiento, error y reintento. PDF, imágenes, video y enlaces conservan su comportamiento.
5. **Seguridad:** HTML de usuario es contenido no confiable. Mantener o reforzar sanitización, `iframe` con sandbox restrictivo, CSP aplicable, sin scripts ni navegación superior, `credentials: omit` al recuperar el archivo cuando corresponda y sin ejecutar HTML arbitrario en el origen de la app. Validar el origen/host permitido de la descarga sin romper URL firmadas legítimas. No usar `bypassSecurityTrustHtml` para el documento sin aislamiento.
6. **Markdown:** acordar si `.md` entra en el mismo alcance de visualización embebida. Si sí, convertir Markdown a HTML sanitizado y aislarlo en el mismo mecanismo; no tratarlo como HTML crudo ni dejarlo pasar por un `iframe` sin política. Si no, documentar claramente que se descarga/abre externamente.

## 3. Trabajo por fases y responsables

### Fase 0 — Reproducir el contrato real (Front + Courses + Roadmap)

- [ ] Crear en entorno integrado una sección COURSE con un `.html` y un `.md` desde la vista sobria; publicar y abrir el mismo nodo con usuario alumno matriculado.
- [ ] Capturar, sin registrar tokens ni firmas, forma del `contentId`, respuesta del detalle de Roadmap, `type/status/accessUrl/expiresAt`, URL de Courses, método de autenticación, `Content-Type`, `Content-Disposition`, CORS y redirecciones. Verificar si `accessUrl` es de mismo origen, termina en `.html`, expira y se puede hacer `fetch` desde navegador.
- [ ] Confirmar con Courses el contrato `GET /course/course-contents/{id}/download-url` y si la URL requiere renovar firma. Validar que el archivo confirmado como `text/html` aparece en la ruta `/activities` de la sección.
- [ ] Documentar exactamente dónde falla hoy el flujo real antes de cambiar código: publicación, proyección, URL, clasificador del visor, fetch o aislamiento.

**Salida:** traza reproducible y decisión de contrato FE–Roadmap–Courses, sin exponer URLs firmadas en Obsidian.

### Fase 1 — Frontend: resolver y renderizar HTML en 3D (P0)

- [ ] En la capa de acceso a materiales, priorizar un tipo/MIME confiable para detectar HTML; conservar detección por extensión solo como compatibilidad cuando sea segura. Si el DTO no aporta metadatos, resolver por `contentId` usando el endpoint existente de Courses y comprobar respuesta real antes de pedir campo nuevo en backend.
- [ ] Reutilizar la lógica de carga/render de `CourseHtmlPageService` donde tenga sentido, sin acoplar el visor 3D al editor del profesor. Definir un adaptador/servicio compartido si evita duplicar obtención, renovación y errores.
- [ ] Alimentar el visor actual (`material-access.component`) desde `hex-world-page` sin alterar la navegación del mundo 3D. Manejar URL vencida, ausencia de permisos, archivo no disponible, `Content-Type` incorrecto, redirección y fallo de red con mensaje y reintento controlado.
- [ ] Revisar las garantías de `iframe` sandbox/sanitización/CSP y la liberación de URLs objeto. No habilitar scripts ni credenciales para “hacer funcionar” un HTML de prueba.
- [ ] Añadir pruebas unitarias/de componente para clasificación HTML, ruta `contentId`/URL, render embebido, rechazo de origen inseguro, errores y regresiones de otros tipos.

**Salida:** HTML publicado visible dentro del visor 3D para el flujo COURSE, con pruebas locales.

### Fase 2 — Backend únicamente según evidencia de Fase 0 (P0 condicional)

- [ ] Si Roadmap `/activities` ya devuelve `contentId` y URL utilizable, **no modificar backend** por costumbre. Mantener sus controles de matrícula, publicación y desbloqueo.
- [ ] Si la proyección pierde el vínculo o la URL, corregir mapeo/DTO en `tpi-roadmap`, con test de cliente Courses y de `NodeDetailService`. Coordinar con Courses cualquier cambio en respuesta/MIME o endpoint; su repo no está en las worktrees creadas.
- [ ] Si se añade `mimeType`/`fileName` al contrato, hacerlo opcional y retrocompatible, con pruebas para materiales antiguos y despliegue coordinado Courses → Roadmap → FE. No usar la extensión de la URL firmada como contrato estable.
- [ ] Verificar autorización en backend para `download-url` y que una URL firmada no habilite un material bloqueado por acceso directo.

**Salida:** contrato consistente y cubierto por tests; cambio de backend solo si una falla real lo exige.

### Fase 3 — Markdown y variante OWN (P1, decisión de alcance)

- [ ] Si el requisito incluye `.md` en el visor, definir renderer Markdown seguro, estilo legible y manejo de enlaces/imágenes relativas; cubrir Markdown malicioso y archivos vacíos. El visor actual no ofrece esta rama embebida.
- [ ] Confirmar si el profesor debe publicar HTML de la vista sobria en nodos **OWN** además de COURSE. OWN sin sección utiliza contenidos de comisión y hoy el cliente Roadmap no propaga URL/expiración en esa ruta; estudiar primero cómo asociar un `contentId` de sección. No aplicar el arreglo de OWN como condición para el caso COURSE.

**Salida:** alcance explícito y, si se aprueba, pruebas adicionales sin degradar P0.

### Fase 4 — Validación integrada y entrega

- [ ] E2E con profesor que importa/publica HTML en vista sobria y alumno que abre el **mismo `contentId`** desde el nodo COURSE en 3D; comprobar visualmente que aparece *dentro* del visor, no pestaña nueva.
- [ ] Repetir para URL firmada recién emitida y vencida/renovada, alumno no matriculado, nodo bloqueado, archivo eliminado/no confirmado, HTML con script, URL externa, PDF/imagen/video y, si se incluye, `.md`.
- [ ] Registrar evidencias sin tokens, URLs firmadas ni contenido sensible; anotar commits/PR de FE, Roadmap y Courses si hubo cambios, y el orden de despliegue.

## 4. Criterios de aceptación

- [ ] Un HTML importado desde la vista simplificada, confirmado y publicado en una sección COURSE se abre por un alumno autorizado **en el visor del mundo 3D** del nodo correspondiente.
- [ ] El HTML renderizado coincide con el `contentId` publicado; una URL temporal vencida tiene recuperación o error explícito, nunca una pantalla vacía indefinida.
- [ ] Nodo bloqueado/alumno no autorizado no entrega contenido; HTML malicioso no ejecuta scripts, no navega la app y no accede a cookies/credenciales.
- [ ] El visor de PDF, imagen, video y enlace externo no presenta regresiones.
- [ ] El comportamiento de `.md` queda probado y documentado según la decisión de alcance: visor seguro o descarga/apertura externa explícita.
- [ ] Existe al menos una prueba integrada con backend real o entorno de integración; los mocks de URL no bastan como cierre.

## 5. Worktrees preparadas y preguntas abiertas

| Equipo | Worktree Orca | Rama | Estado |
|---|---|---|---|
| Frontend | `/Users/benjaminpolzoni/orca/workspaces/2026-PIV-TPI-FE/html-content-3d-viewer-front` | `BenjaminPolzoni/html-content-3d-viewer-front` | Creada desde `origin/develop`; sin implementación de este plan. |
| Backend Roadmap | `/Users/benjaminpolzoni/orca/workspaces/tpi-roadmap/html-content-3d-viewer-back` | `BenjaminPolzoni/html-content-3d-viewer-back` | Creada desde `origin/develop`; cambio condicional a la evidencia. |

**Por resolver antes de implementar:** (1) contrato real de Courses y expiración de la URL; (2) alcance de `.md` embebido; (3) si OWN forma parte del requerimiento; (4) responsable de cambios en Courses si fueran necesarios. Ninguna worktree implica que ya exista una solución ni que el flujo haya pasado E2E.
