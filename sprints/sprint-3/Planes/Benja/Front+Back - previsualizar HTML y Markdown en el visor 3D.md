---
tags: [tpi, g10, sprint-3, plan, front, back, visor-3d, html, markdown]
fecha: 2026-10-26
autor: Benjamin Polzoni
estado: propuesto - pendiente de implementación y validación integrada
repo: 2026-P4-FE/2026-PIV-TPI-FE, 2026-P4-BE/tpi-roadmap
taiga: sin asignar
---

# Front + Back — Previsualizar HTML y Markdown en el visor de contenido 3D

> [!important] Pedido de Benjamin Polzoni
> El profesor puede cargar `.html` y `.md` desde la vista simplificada/sobria. El alumno debe **leer ambos dentro del visor de contenido del mundo 3D**, como ya ocurre con PDF. **Ver** es la acción principal; descargar, si se mantiene, es una opción secundaria explícita. No alcanza con ofrecer el archivo para descarga ni con abrir otra pestaña.

## Diagnóstico y alcance

- En `origin/develop` del Front, la vista sobria importa HTML y Markdown como contenidos `FILE` asociados a una sección y un `contentId` (`entity-editor-dialog.component.ts`; HTML vía `course-html-page.service.ts`). No es el mismo flujo que el cuerpo `SectionSettings.content`.
- El mundo 3D ya contiene una rama de previsualización HTML (`roadmap/domain/material-access.ts` y `roadmap/ui/material-access/material-access.component.ts`), pero el clasificador requiere URL del mismo origen cuyo *pathname* termine en `.html`/`.htm`. Markdown no tiene una rama equivalente. El síntoma observado por Benjamin es **descarga en vez de previsualización**. Que el HTML real no entre en el clasificador es una **hipótesis**, no una causa confirmada: hay que inspeccionar la URL y la respuesta reales.
- Roadmap conserva el `contentId`; para nodos `COURSE` de una sección obtiene las actividades y conserva la URL de material de Courses. El DTO de material expone `type`, `status`, `accessUrl` y vencimiento, no MIME ni nombre de archivo. La ruta de nodos `OWN` es distinta y su posible pérdida de URL **no demuestra** el fallo del caso `COURSE`.
- El contrato real de URLs, permisos, `Content-Type`, `Content-Disposition` y CORS de Courses aún debe verificarse. No se debe atribuir la descarga solo a `Content-Disposition: attachment`: una lectura con `fetch` puede evitar la navegación de descarga.

## Plan de ejecución

### 1. Reproducir y fijar el contrato (Front + Roadmap + Courses)

- [ ] Cargar/publicar un `.html` y un `.md` desde la vista sobria; enlazar cada `contentId` a su nodo `COURSE`; abrirlos como alumno matriculado en el 3D.
- [ ] Registrar, **sin guardar firmas ni tokens**, el detalle autorizado de Roadmap y la forma de las URLs entregadas por Courses: origen, extensión del *pathname*, query, MIME, disposición, expiración, redirecciones, CORS y resultado de `fetch`.
- [ ] Localizar el punto exacto de la descarga: vínculo/publicación, proyección Roadmap, clasificación FE, obtención del texto o render. Definir con Courses cómo renovar una URL expirada.

### 2. Front: previsualización embebida obligatoria

- [ ] Clasificar `.html`/`.htm` y `.md`/`.markdown` con metadatos confiables cuando existan; no depender solo de la extensión de una URL firmada/opaca. Mantener compatibilidad para URLs antiguas.
- [ ] Para HTML, usar la rama de previsualización ya existente y corregir el punto de fallo demostrado por la fase 1. Para Markdown, obtener el texto y renderizarlo **dentro del mismo panel/drawer del visor 3D**, reutilizando el renderer seguro de Markdown si resulta apropiado.
- [ ] Mantener estados de carga, error, permiso denegado, URL vencida y reintento; que un `attachment` no fuerce descarga como acción principal. Dejar el botón de descargar como secundario, si se conserva.
- [ ] Mantener el HTML de autor no confiable aislado: sanitización y `iframe` restrictivo; no habilitar scripts, credenciales ni navegación superior para hacer pasar la prueba. Sanitizar Markdown y definir enlaces/imágenes relativas.
- [ ] Pruebas de clasificador y componente para extensiones, URL firmada/opaca/de otro origen, respuesta `attachment`, XSS, errores y regresiones PDF/imagen/video/enlace.

### 3. Back: **solo si la evidencia lo exige**

- [ ] Si la ruta `COURSE` ya entrega `contentId` y URL utilizable, **no cambiar Roadmap**. Conservar controles de publicación, matrícula y desbloqueo.
- [ ] Si Roadmap pierde URL o vínculo, corregir mapeo/DTO y probar cliente Courses + detalle de nodo.
- [ ] Si no existe un discriminador estable, coordinar `mimeType`/`fileName` opcionales y retrocompatibles entre Courses → Roadmap → Front; probar materiales existentes. Confirmar también autorización del endpoint de URL de descarga.
- [ ] Tratar `OWN` como investigación posterior, no como bloqueo de la previsualización `COURSE`.

### 4. Validación de cierre

- [ ] E2E integrado: profesor publica los dos archivos y alumno autorizado abre **los mismos `contentId`** dentro del visor 3D; ninguno requiere descarga o pestaña nueva para leerse.
- [ ] Cubrir URL expirada, archivo faltante, alumno no autorizado, nodo bloqueado, HTML/Markdown malicioso y regresión de PDF. Registrar evidencia sin URLs firmadas.

## Ramas preparadas en Orca

| Parte | Rama | Worktree |
|---|---|---|
| Front | `BenjaminPolzoni/html-content-3d-viewer-front` | `/Users/benjaminpolzoni/orca/workspaces/2026-PIV-TPI-FE/html-content-3d-viewer-front` |
| Roadmap back (condicional) | `BenjaminPolzoni/html-content-3d-viewer-back` | `/Users/benjaminpolzoni/orca/workspaces/tpi-roadmap/html-content-3d-viewer-back` |

Ambas parten de `origin/develop`; este plan **no implementa código**. Para el análisis extendido y la lista completa de pruebas, ver [[tareas/plan-html-md-visor-3d|plan técnico previo]].
