---
tags: [tpi, g10, sprint-3, historia, ht]
id: U01
tipo: HT
epica: "EP-S3-3"
capa: "Front"
esfuerzo: S
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# U01: Subir la UI-KIT a 0.8.0 y cerrar sus TODOs

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-3 Consistencia visual con la UI-KIT|EP-S3-3]] · **HT** · Capa: **Front** · Esfuerzo: **S** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como equipo quiero el front en la última versión del kit para destrabar los TODOs que esperaban cambios del kit.

## Qué hay hoy

El front está en ^0.7.1. La rama `feature/ui-lib-0-8-0` no está mergeada. Hay 9 TODOs que se destraban con 0.8.0 (incluye ui-kit#59 de HU-22).

## Criterios de aceptación

- [ ] Bump a 0.8.0 mergeado, con `npm run verify` y los tests visuales en verde.
- [ ] TODOs #59, #53, #51, #83/#84/#85 y `::ng-deep` de pagination cerrados.
- [ ] HU-22: insignias en modo solo lectura en `ranking-detail`.

## Depende de

Nada: se puede empezar ya.

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G13]]

## Deuda técnica que cierra

- [[deuda-tecnica|DT-14]]
