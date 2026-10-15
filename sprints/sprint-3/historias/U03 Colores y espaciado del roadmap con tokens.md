---
tags: [tpi, g10, sprint-3, historia, ht]
id: U03
tipo: HT
epica: "EP-S3-3"
capa: "Front"
esfuerzo: M
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [U01]
---

# U03: Colores y espaciado del roadmap con tokens

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-3 Consistencia visual con la UI-KIT|EP-S3-3]] · **HT** · Capa: **Front** · Esfuerzo: **M** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como equipo quiero que el roadmap use los tokens del kit para que el tema (claro/oscuro) funcione igual que en el resto.

## Qué hay hoy

316 colores hardcodeados y un puente de tokens `--color-*` propio.

## Criterios de aceptación

- [ ] Se borra el puente `--color-*`.
- [ ] Colores, espaciado y tipografía con tokens del kit (salvo `engine/` y arte).
- [ ] Regla de `stylelint` contra hex/rgb literales en las carpetas de G10.

## Depende de

- [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs|U01]] Subir la UI-KIT a 0.8.0 y cerrar sus TODOs

## Dudas que la frenan

Ninguna.

## Deuda técnica que cierra

- [[deuda-tecnica|DT-15]]
