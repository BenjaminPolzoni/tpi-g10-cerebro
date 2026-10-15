---
tags: [tpi, g10, sprint-3, epica]
id: EP-S3-0
estado: Propuesta
historias: 12
---

# EP-S3-0: Deuda del Sprint 2

> [!info] Épica propuesta del Sprint 3. **12 ítems** (5 S · 5 M · 2 L). Todavía no está en Taiga.

## Objetivo

Cerrar lo que figura Done en Taiga y no lo está, y la deuda que rompe la demo. Va primero: varias HU de las otras épicas se apoyan en esto.

## Criterios de aceptación a nivel épica

- [ ] Ninguna HU de G10 figura Done en Taiga sin cumplir sus criterios en el código.
- [ ] La demo corre con los flags encendidos y sin IDs de mock.
- [ ] No quedan ramas del back sin decidir (mergear o cerrar).

## Historias

| ID | Tipo | Título | Capa | Esf. | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/B01 Cerrar o mergear las ramas colgadas del back\|B01]] | HT | Cerrar o mergear las ramas colgadas del back | Back | S | — | [[sprints/sprint-3/08-dudas\|E5]] |
| [[sprints/sprint-3/historias/B02 Encender los flags en los entornos\|B02]] | HT | Encender los flags en los entornos | Infra | S | — | [[sprints/sprint-3/08-dudas\|E6]] |
| [[sprints/sprint-3/historias/B03 Sacar los IDs de mock del front\|B03]] | HT | Sacar los IDs de mock del front | Front | S | — | — |
| [[sprints/sprint-3/historias/B04 Pre-chequeo de elegibilidad para el alumno (HU-48)\|B04]] | HU | Pre-chequeo de elegibilidad para el alumno (HU-48) | Back | M | — | — |
| [[sprints/sprint-3/historias/B05 Completar insignias (HU-20 y HU-21)\|B05]] | HU | Completar insignias (HU-20 y HU-21) | Back + Front | M | — | [[sprints/sprint-3/08-dudas\|E2]] |
| [[sprints/sprint-3/historias/B06 Gate con origen no disponible y dato stale (HU-15 y HU-16)\|B06]] | HU | Gate con origen no disponible y dato stale (HU-15 y HU-16) | Back | M | — | [[sprints/sprint-3/08-dudas\|E9]] |
| [[sprints/sprint-3/historias/B07 Validar el ícono según el tipo de nodo (HU-43)\|B07]] | HU | Validar el ícono según el tipo de nodo (HU-43) | Back | S | — | — |
| [[sprints/sprint-3/historias/B08 Templo de materiales (HU-46)\|B08]] | HU | Templo de materiales (HU-46) | Front | M | — | [[sprints/sprint-3/08-dudas\|P13]] |
| [[sprints/sprint-3/historias/B09 Comisiones en el front (HU-44 y HU-45)\|B09]] | HU | Comisiones en el front (HU-44 y HU-45) | Front (+ Back) | L | [[sprints/sprint-3/historias/B02 Encender los flags en los entornos\|B02]] | [[sprints/sprint-3/08-dudas\|P5]] |
| [[sprints/sprint-3/historias/B10 Restricciones de Courses (HU-49)\|B10]] | HU | Restricciones de Courses (HU-49) | Back + Front | L | [[sprints/sprint-3/historias/C04 Nodo examen con ventana horaria\|C04]] | [[sprints/sprint-3/08-dudas\|P9]], [[sprints/sprint-3/08-dudas\|G4]] |
| [[sprints/sprint-3/historias/B11 Reintentos y edición de nodos (HU-01 y HU-41)\|B11]] | HU | Reintentos y edición de nodos (HU-01 y HU-41) | Back | M | — | — |
| [[sprints/sprint-3/historias/B12 Poner Taiga al día\|B12]] | HT | Poner Taiga al día | Taiga | S | — | [[sprints/sprint-3/08-dudas\|E10]], [[sprints/sprint-3/08-dudas\|E11]] |

## Origen

[[sprints/sprint-3/02-pendientes|02-pendientes]], [[sprints/sprint-3/01-estado-actual|01-estado-actual]], [[deuda-tecnica|deuda técnica]]
