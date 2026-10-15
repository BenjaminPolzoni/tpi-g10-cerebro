---
tags: [tpi, g10, sprint-3, historia, ht]
id: U04
tipo: HT
epica: "EP-S3-3"
capa: "Front"
esfuerzo: M
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [U01]
---

# U04: Overlays y componentes locales al kit

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-3 Consistencia visual con la UI-KIT|EP-S3-3]] · **HT** · Capa: **Front** · Esfuerzo: **M** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como usuario quiero diálogos y componentes accesibles y consistentes.

## Qué hay hoy

`npc-dialogue` y `shop-interior` tienen su propio `role="dialog"`. `lives`, `streak`, `role-switch`, `inventory-item-card` y `level-hud` son componentes propios.

## Criterios de aceptación

- [ ] `npc-dialogue` y `shop-interior` con `generic-modal`/`generic-drawer`.
- [ ] `lives` → `generic-progress [hearts]`, `level-hud` → `generic-xp-bar`, `inventory-item-card` → `generic-item-tile`, `role-switch` → `generic-segmented`.
- [ ] `streak`: se saca de la UI o se pasa a `generic-streak-flame` con datos reales (DT-13, E12).

## Depende de

- [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs|U01]] Subir la UI-KIT a 0.8.0 y cerrar sus TODOs

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E12]]

## Deuda técnica que cierra

- [[deuda-tecnica|DT-13]]
