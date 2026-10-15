---
tags: [tpi, g10, sprint-3, historia, ht]
id: B03
tipo: HT
epica: "EP-S3-0"
capa: "Front"
esfuerzo: S
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# B03: Sacar los IDs de mock del front

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HT** · Capa: **Front** · Esfuerzo: **S** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como alumno quiero ver mis datos reales y no los de un alumno de prueba.

## Qué hay hoy

`DEMO_STUDENT_ID` se usa de respaldo en `roadmap.store.ts`, `hex-world-page` y `challenge-attempt.service`. `COURSE_SEED_ID` es el curso por defecto del store y del `ranking-panel`. `CURRENT_STUDENT_ID` (mock) en `ranking-detail`.

## Criterios de aceptación

- [ ] El alumno sale de la sesión y el curso de la ruta en todas esas pantallas.
- [ ] Sin sesión o sin curso se muestra un error, no un respaldo silencioso.
- [ ] No queda ninguna referencia a esas constantes fuera de tests y mocks.

## Depende de

Nada: se puede empezar ya.

## Dudas que la frenan

Ninguna.

## Deuda técnica que cierra

- [[deuda-tecnica|DT-09]]
