---
tags: [tpi, g10, sprint-3, historia, hu]
id: B09
tipo: HU
epica: "EP-S3-0"
capa: "Front (+ Back)"
esfuerzo: L
estado: Propuesta
responsable: ""
taiga: "HU-44, HU-45"
depende: [B02]
---

# B09: Comisiones en el front (HU-44 y HU-45)

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HU** · Capa: **Front (+ Back)** · Esfuerzo: **L** · Taiga: [[taiga/historias/HU-44 Ver el roadmap de cada una de mis comisiones|HU-44]], [[taiga/historias/HU-45 Ranking de la cohorte y avance por comisión|HU-45]]
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como alumno quiero ver el roadmap de cada una de mis comisiones, y como profesor quiero ver el avance por comisión.

## Qué hay hoy

El back está hecho detrás de `ROADMAP_BY_GROUP_ENABLED`. El front no tiene selector de comisión ni vista de avance por comisión. HU-45 sigue en New.

## Criterios de aceptación

- [ ] Selector de comisión en el roadmap del alumno cuando tiene más de una.
- [ ] El motivo `group_restricted` se muestra con un texto claro.
- [ ] El profesor ve el avance por comisión (`GET /courses/{id}/groups/{gid}/progress`).
- [ ] HU-44 y HU-45 pasan a Done en Taiga con los criterios cumplidos.

## Depende de

- [[sprints/sprint-3/historias/B02 Encender los flags en los entornos|B02]] Encender los flags en los entornos

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P5]]
