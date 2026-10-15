---
tags: [tpi, g10, sprint-3, historia, hu]
id: C04
tipo: HU
epica: "EP-S3-2"
capa: "Back + Front"
esfuerzo: M
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# C04: Nodo examen con ventana horaria

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes|EP-S3-2]] · **HU** · Capa: **Back + Front** · Esfuerzo: **M** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como profesor quiero que un nodo examen (parcial) solo esté habilitado en una ventana horaria.

## Qué hay hoy

El gate evalúa `DATE_RESTRICTED` con ventanas que publica Courses (HU-49). El nodo no tiene ventana propia.

## Criterios de aceptación

- [ ] Campos `available_from` y `available_until` en nodos `EXAM`.
- [ ] Fuera de la ventana el gate responde `DATE_RESTRICTED`.
- [ ] El alumno ve cuándo se habilita.
- [ ] Si Courses también publica una ventana, gana la más restrictiva (o lo que defina P9).

## Depende de

Nada: se puede empezar ya.

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P9]]
