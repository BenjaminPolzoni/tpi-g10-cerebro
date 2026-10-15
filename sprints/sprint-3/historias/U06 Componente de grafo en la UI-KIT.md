---
tags: [tpi, g10, sprint-3, historia, hu]
id: U06
tipo: HU
epica: "EP-S3-3"
capa: "UI-KIT"
esfuerzo: L
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [U01]
---

# U06: Componente de grafo en la UI-KIT

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-3 Consistencia visual con la UI-KIT|EP-S3-3]] · **HU** · Capa: **UI-KIT** · Esfuerzo: **L** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como front de cualquier grupo quiero un componente de grafo en el kit para no hacer uno propio.

## Qué hay hoy

El kit no tiene componente de grafo. La vista de grafo del roadmap es un SVG propio.

## Criterios de aceptación

- [ ] `generic-node-graph` en el kit con pan, zoom, minimapa, aristas, selección con teclado y foco.
- [ ] Envuelve `ngx-vflow` o `@foblex/flow` + `elkjs`, con tokens del kit.
- [ ] Acordado con el equipo del kit quién es dueño (G13).
- [ ] Publicado en una versión del kit y usado por M09.

## Depende de

- [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs|U01]] Subir la UI-KIT a 0.8.0 y cerrar sus TODOs

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G13]]
