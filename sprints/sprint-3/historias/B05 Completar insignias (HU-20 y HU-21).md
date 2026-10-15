---
tags: [tpi, g10, sprint-3, historia, hu]
id: B05
tipo: HU
epica: "EP-S3-0"
capa: "Back + Front"
esfuerzo: M
estado: Propuesta
responsable: ""
taiga: "HU-20, HU-21"
depende: []
---

# B05: Completar insignias (HU-20 y HU-21)

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HU** · Capa: **Back + Front** · Esfuerzo: **M** · Taiga: [[taiga/historias/HU-20 Definir el catálogo de insignias del curso|HU-20]], [[taiga/historias/HU-21 Otorgar insignias automáticamente|HU-21]]
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como alumno quiero que todas las insignias del catálogo se puedan ganar, y como profesor quiero editar y dar de baja las insignias de mi curso.

## Qué hay hoy

Tres criterios del catálogo nunca se otorgan: `SECTION_NO_LIVES_LOST`, `NODE_NO_RETRIES` y `LIFE_RECOVERED`. El front no permite editar ni dar de baja insignias.

## Criterios de aceptación

- [ ] Cada uno de los tres criterios se implementa con su test, o se quita del catálogo (decisión E2).
- [ ] El profesor edita nombre, descripción e ícono de una insignia de su curso desde el front.
- [ ] El profesor da de baja una insignia sin borrar las ya otorgadas (baja lógica, DEC-005).

## Depende de

Nada: se puede empezar ya.

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E2]]
