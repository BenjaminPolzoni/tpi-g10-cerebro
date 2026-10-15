---
tags: [tpi, g10, sprint-3, epica]
estado: Propuesta
sprint: "G10 - Sprint 3"
historias: 9
puntos: 61
---

# Deuda del Sprint 2

> [!info] Épica del Sprint 3 · **9 historias** · **61 pts** · Estado: **New** · En Taiga: [[taiga/epicas/EP-8632 Deuda del Sprint 2|EP-8632]].

[G10] — Deuda del Sprint 2
--------------------------

* * *

Objetivo
--------

Cerrar lo que figura Done en Taiga y no lo está, y la deuda que rompe la demo. Va primero: varias HU de las otras épicas se apoyan en esto.

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: Las HU listadas figuran Done (o New) en Taiga; el detalle de qué les falta sale de la auditoría del 2026-10-14 sobre `origin/develop`.
*   Restricciones (legales/técnicas): No se agregan funciones nuevas: solo se completa lo comprometido en el Sprint 2 y se limpia la deuda que rompe la demo.

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] Ninguna HU de G10 figura Done en Taiga sin cumplir sus criterios en el código.
*   [ ] La demo corre con los flags encendidos y sin IDs de mock.
*   [ ] No quedan ramas del back sin decidir (mergear o cerrar).
*   [ ] KPIs iniciales alcanzan: HU en Done que no cumplen sus CA (ver 01-estado-actual): 0 al cierre del sprint.
*   [ ] Sin regresiones críticas en: Ninguna HU que hoy funciona deja de funcionar al encender los flags o sacar los mocks.
*   [ ] Observabilidad y alertas configuradas: Logs del gate con el motivo de cada bloqueo; alerta si `origen_no_disponible` supera el 5 % de las consultas.
*   [ ] Documentación de uso y operación publicada: Taiga actualizado; `01-estado-actual` y `02-pendientes` del cerebro marcados como resueltos.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: Courses, Accounting, Motor, Backoffice, plataforma.
*   Módulos afectados: Gate, insignias, nodos, comisiones, roadmap del alumno, ranking.
*   Otros equipos: G01 (restricciones), G09 (gate), plataforma (flags).
*   Impacto en datos / migraciones: Columna de reintentos en nodos (HU-41 y HU-01).
*   Feature toggles / flags: `SECTIONS_SYNC_ENABLED` y `ROADMAP_BY_GROUP_ENABLED` se encienden en mesh y demo.

## Historias

| HU | Título | En Taiga | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/HT-14 Sacar los IDs de mock del front\|HT-14]] | Sacar los IDs de mock del front | Nueva | 3 | Must | — | — |
| [[sprints/sprint-3/historias/HT-30 Insignias pendientes de HU-20 y HU-21\|HT-30]] | Insignias pendientes de HU-20 y HU-21 | Nueva | 8 | Must ⭐ 1 | — | [[sprints/sprint-3/08-dudas\|E2]] ✅, [[sprints/sprint-3/08-dudas\|E8]] ✅ |
| [[sprints/sprint-3/historias/HT-31 Gate y vidas pendientes de HU-15, HU-16 y HU-48\|HT-31]] | Gate y vidas pendientes de HU-15, HU-16 y HU-48 | Nueva | 8 | Must ⭐ 1 | G09 (acta del gate) | [[sprints/sprint-3/08-dudas\|E9]] ✅ |
| [[sprints/sprint-3/historias/HT-32 Nodos y editor pendientes de HU-01, HU-41 y HU-43\|HT-32]] | Nodos y editor pendientes de HU-01, HU-41 y HU-43 | Nueva | 8 | Must ⭐ 1 | — | [[sprints/sprint-3/08-dudas\|G8]] ✅ |
| [[sprints/sprint-3/historias/HT-33 Comisión y material pendientes de HU-44 y HU-46\|HT-33]] | Comisión y material pendientes de HU-44 y HU-46 | Nueva | 8 | Must ⭐ 1 | — | [[sprints/sprint-3/08-dudas\|P5]] ✅, [[sprints/sprint-3/08-dudas\|P13]] ✅ |
| [[sprints/sprint-3/historias/HU-45 Ranking de la cohorte y avance por comisión\|HU-45]] | Ranking de la cohorte y avance por comisión | Reabrir | 5 | Must | Flag `ROADMAP_BY_GROUP_ENABLED`; G09 (solo CA5) | [[sprints/sprint-3/08-dudas\|E1]] ✅, [[sprints/sprint-3/08-dudas\|P10]] ✅, [[sprints/sprint-3/08-dudas\|P14]] ✅ |
| [[sprints/sprint-3/historias/HU-49 Aplicar en el roadmap las restricciones de sección y actividad que publica Courses\|HU-49]] | Aplicar en el roadmap las restricciones de sección y actividad que publica Courses | Reabrir | 8 | Must | G01 (evento y ventanas de examen) | [[sprints/sprint-3/08-dudas\|P9]] ✅, [[sprints/sprint-3/08-dudas\|G4]] ✅, [[sprints/sprint-3/08-dudas\|E3]] ✅ |
| [[sprints/sprint-3/historias/HU-72 Cerrar el curso con el estado académico final\|HU-72]] | Cerrar el curso con el estado académico final | Nueva | 8 | Should | [[sprints/sprint-3/historias/HU-45 Ranking de la cohorte y avance por comisión\|HU-45]] | [[sprints/sprint-3/08-dudas\|P15]] ✅, [[sprints/sprint-3/08-dudas\|G14]] |
| [[sprints/sprint-3/historias/HU-73 Ver mi racha de días con actividad\|HU-73]] | Ver mi racha de días con actividad | Nueva | 5 | Should | [[sprints/sprint-3/historias/HT-26 Adopción de la UI-KIT en el roadmap\|HT-26]] | [[sprints/sprint-3/08-dudas\|E12]] ✅ |

---

## Origen (no va a Taiga)

[[sprints/sprint-3/02-pendientes|02-pendientes]], [[sprints/sprint-3/01-estado-actual|01-estado-actual]], [[deuda-tecnica|deuda técnica]]
