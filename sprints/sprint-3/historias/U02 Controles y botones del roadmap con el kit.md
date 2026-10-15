---
tags: [tpi, g10, sprint-3, historia, ht]
id: U02
tipo: HT
epica: "EP-S3-3"
capa: "Front"
esfuerzo: S
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [U01]
---

# U02: Controles y botones del roadmap con el kit

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-3 Consistencia visual con la UI-KIT|EP-S3-3]] · **HT** · Capa: **Front** · Esfuerzo: **S** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como usuario quiero formularios y botones consistentes con el resto de la plataforma.

## Qué hay hoy

`entity-editor-dialog`, `badges-catalog-page` y `avatar-panel` usan `<input>`, `<select>` y `<button>` crudos. Hay botones y headings sueltos en `course-editor-page`, `section-nodes`, `course-map-page`, `hex-world-page` y `feedback-toast`.

## Criterios de aceptación

- [ ] Esas pantallas usan `generic-input`, `generic-select`, `generic-textarea` y `genericButton`.
- [ ] Sin `::ng-deep` nuevos.

## Depende de

- [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs|U01]] Subir la UI-KIT a 0.8.0 y cerrar sus TODOs

## Dudas que la frenan

Ninguna.
