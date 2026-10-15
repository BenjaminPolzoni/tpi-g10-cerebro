---
tags: [tpi, g10, sprint-3, historia, hu]
id: B10
tipo: HU
epica: "EP-S3-0"
capa: "Back + Front"
esfuerzo: L
estado: Propuesta
responsable: ""
taiga: "HU-49"
depende: [C04]
---

# B10: Restricciones de Courses (HU-49)

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HU** · Capa: **Back + Front** · Esfuerzo: **L** · Taiga: [[taiga/historias/HU-49 Aplicar en el roadmap las restricciones de sección y actividad que publica Courses|HU-49]]
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como alumno quiero saber por qué un nodo está oculto o bloqueado por fecha, y que se actualice si Courses cambia la restricción.

## Qué hay hoy

El gate aplica la restricción por fecha. Falta distinguir oculto (HIDDEN) de bloqueado (LOCKED), consumir el evento de cambio y avisar. El front no tiene nada. Depende de G01.

## Criterios de aceptación

- [ ] Un nodo HIDDEN no aparece al alumno. Uno LOCKED aparece bloqueado con su fecha.
- [ ] Al llegar el evento de cambio de restricción de Courses, el estado se actualiza sin recargar a mano.
- [ ] El alumno ve un aviso con la fecha de habilitación.

## Depende de

- [[sprints/sprint-3/historias/C04 Nodo examen con ventana horaria|C04]] Nodo examen con ventana horaria

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P9]]
- [[sprints/sprint-3/08-dudas|G4]]
