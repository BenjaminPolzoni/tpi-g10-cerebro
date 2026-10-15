---
tags: [tpi, g10, sprint-3, epica]
id: EP-S3-0
estado: Propuesta
historias: 12
puntos: 49
---

# EP-S3-0: Deuda del Sprint 2

> [!info] Épica propuesta del Sprint 3. **12 historias**, **49 pts**. Todavía no está en Taiga.
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Objetivo* hasta *Dependencias / Impactos*.

**[G10] — Deuda del Sprint 2**

* * *

## Objetivo

Cerrar lo que figura Done en Taiga y no lo está, y la deuda que rompe la demo. Va primero: varias HU de las otras épicas se apoyan en esto.

* * *

## Suposiciones y Restricciones

- Suposiciones: Las HU listadas figuran Done (o New) en Taiga; el detalle de qué les falta sale de la auditoría del 2026-10-14 sobre `origin/develop`.
- Restricciones (legales/técnicas): No se agregan funciones nuevas: solo se completa lo comprometido en el Sprint 2 y se limpia la deuda que rompe la demo.

* * *

## Criterios de Aceptación a nivel Épico

- [ ] Ninguna HU de G10 figura Done en Taiga sin cumplir sus criterios en el código.
- [ ] La demo corre con los flags encendidos y sin IDs de mock.
- [ ] No quedan ramas del back sin decidir (mergear o cerrar).
- [ ] KPIs iniciales: HU en Done que no cumplen sus CA (ver 01-estado-actual): 0 al cierre del sprint.
- [ ] Sin regresiones críticas: Ninguna HU que hoy funciona deja de funcionar al encender los flags o sacar los mocks.
- [ ] Observabilidad y alertas: Logs del gate con el motivo de cada bloqueo; alerta si `origen_no_disponible` supera el 5 % de las consultas.
- [ ] Documentación publicada: Taiga actualizado; `01-estado-actual` y `02-pendientes` del cerebro marcados como resueltos.

* * *

## Dependencias / Impactos

- Servicios / APIs: Courses, Accounting, Motor, Backoffice, plataforma.
- Módulos afectados: Gate, insignias, nodos, comisiones, roadmap del alumno, ranking.
- Otros equipos: G01 (restricciones), G09 (gate), plataforma (flags).
- Impacto en datos / migraciones: Columna de reintentos en nodos (B11).
- Feature toggles / flags: `SECTIONS_SYNC_ENABLED` y `ROADMAP_BY_GROUP_ENABLED` se encienden en mesh y demo.

---

## Historias

| ID | Tipo | Título | Capa | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/B01 Cerrar o mergear las ramas colgadas del back\|B01]] | HT | Cerrar o mergear las ramas colgadas del back | Back | 2 | Must | — | [[sprints/sprint-3/08-dudas\|E5]] |
| [[sprints/sprint-3/historias/B02 Encender los flags en los entornos\|B02]] | HT | Encender los flags en los entornos | Infra | 2 | Must | — | [[sprints/sprint-3/08-dudas\|E6]] |
| [[sprints/sprint-3/historias/B03 Sacar los IDs de mock del front\|B03]] | HT | Sacar los IDs de mock del front | Front | 3 | Must | — | — |
| [[sprints/sprint-3/historias/B04 Pre-chequeo de elegibilidad para el alumno (HU-48)\|B04]] | HU | Pre-chequeo de elegibilidad para el alumno (HU-48) | Back | 3 | Must | — | — |
| [[sprints/sprint-3/historias/B05 Completar insignias (HU-20 y HU-21)\|B05]] | HU | Completar insignias (HU-20 y HU-21) | Back + Front | 5 | Should | — | [[sprints/sprint-3/08-dudas\|E2]] |
| [[sprints/sprint-3/historias/B06 Gate con origen no disponible y dato stale (HU-15 y HU-16)\|B06]] | HU | Gate con origen no disponible y dato stale (HU-15 y HU-16) | Back | 5 | Should | — | [[sprints/sprint-3/08-dudas\|E9]] |
| [[sprints/sprint-3/historias/B07 Validar el ícono según el tipo de nodo (HU-43)\|B07]] | HU | Validar el ícono según el tipo de nodo (HU-43) | Back | 1 | Could | — | — |
| [[sprints/sprint-3/historias/B08 Templo de materiales (HU-46)\|B08]] | HU | Templo de materiales (HU-46) | Front | 5 | Should | — | [[sprints/sprint-3/08-dudas\|P13]] |
| [[sprints/sprint-3/historias/B09 Comisiones en el front (HU-44 y HU-45)\|B09]] | HU | Comisiones en el front (HU-44 y HU-45) | Front (+ Back) | 8 | Must | [[sprints/sprint-3/historias/B02 Encender los flags en los entornos\|B02]] | [[sprints/sprint-3/08-dudas\|P5]] |
| [[sprints/sprint-3/historias/B10 Restricciones de Courses (HU-49)\|B10]] | HU | Restricciones de Courses (HU-49) | Back + Front | 8 | Should | [[sprints/sprint-3/historias/C04 Nodo examen con ventana horaria\|C04]] | [[sprints/sprint-3/08-dudas\|P9]], [[sprints/sprint-3/08-dudas\|G4]] |
| [[sprints/sprint-3/historias/B11 Reintentos y edición de nodos (HU-01 y HU-41)\|B11]] | HU | Reintentos y edición de nodos (HU-01 y HU-41) | Back | 5 | Must | — | — |
| [[sprints/sprint-3/historias/B12 Poner Taiga al día\|B12]] | HT | Poner Taiga al día | Taiga | 2 | Must | — | [[sprints/sprint-3/08-dudas\|E10]], [[sprints/sprint-3/08-dudas\|E11]] |

## Origen

[[sprints/sprint-3/02-pendientes|02-pendientes]], [[sprints/sprint-3/01-estado-actual|01-estado-actual]], [[deuda-tecnica|deuda técnica]]
