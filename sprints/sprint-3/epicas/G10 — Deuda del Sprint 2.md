---
tags: [tpi, g10, sprint-3, epica]
estado: Propuesta
sprint: "G10 - Sprint 3"
historias: 16
puntos: 56
---

# Deuda del Sprint 2

> [!info] Épica del Sprint 3 · **16 historias** · **56 pts** · Estado: **Propuesta** (todavía no está en Taiga).

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
| [[sprints/sprint-3/historias/HT-12 Cerrar o mergear las ramas colgadas del back\|HT-12]] | Cerrar o mergear las ramas colgadas del back | Nueva | 2 | Must | — | [[sprints/sprint-3/08-dudas\|E5]] ✅ |
| [[sprints/sprint-3/historias/HT-13 Encender los flags en los entornos\|HT-13]] | Encender los flags en los entornos | Nueva | 2 | Must | — | [[sprints/sprint-3/08-dudas\|E6]] |
| [[sprints/sprint-3/historias/HT-14 Sacar los IDs de mock del front\|HT-14]] | Sacar los IDs de mock del front | Nueva | 3 | Must | — | — |
| [[sprints/sprint-3/historias/HU-48 Saber si puedo entrar a un desafío antes de abrirlo\|HU-48]] | Saber si puedo entrar a un desafío antes de abrirlo | Reabrir | 3 | Must | — | — |
| [[sprints/sprint-3/historias/HU-20 Definir el catálogo de insignias del curso\|HU-20]] | Definir el catálogo de insignias del curso | Reabrir | 3 | Should | — | — |
| [[sprints/sprint-3/historias/HU-21 Otorgar insignias automáticamente\|HU-21]] | Otorgar insignias automáticamente | Reabrir | 5 | Should | — | [[sprints/sprint-3/08-dudas\|E2]] ✅, [[sprints/sprint-3/08-dudas\|E8]] ✅ |
| [[sprints/sprint-3/historias/HU-15 Impedir la entrega en un nodo bloqueado (gate, vocabulario v3)\|HU-15]] | Impedir la entrega en un nodo bloqueado (gate, vocabulario v3) | Reabrir | 3 | Should | — | [[sprints/sprint-3/08-dudas\|E9]] ✅ |
| [[sprints/sprint-3/historias/HU-16 Integración real con Inventario para las vidas del gate\|HU-16]] | Integración real con Inventario para las vidas del gate | Reabrir | 3 | Should | — | — |
| [[sprints/sprint-3/historias/HU-43 Elegir el ícono de un desafío\|HU-43]] | Elegir el ícono de un desafío | Reabrir | 1 | Could | — | — |
| [[sprints/sprint-3/historias/HU-46 Ver en los nodos y en el Templo el material teórico de Courses\|HU-46]] | Ver en los nodos y en el Templo el material teórico de Courses | Reabrir | 5 | Should | — | [[sprints/sprint-3/08-dudas\|P13]] ✅ |
| [[sprints/sprint-3/historias/HU-44 Ver el roadmap de cada una de mis comisiones\|HU-44]] | Ver el roadmap de cada una de mis comisiones | Reabrir | 5 | Must | [[sprints/sprint-3/historias/HT-13 Encender los flags en los entornos\|HT-13]] | [[sprints/sprint-3/08-dudas\|P5]] ✅ |
| [[sprints/sprint-3/historias/HU-45 Ranking de la cohorte y avance por comisión\|HU-45]] | Ranking de la cohorte y avance por comisión | Reabrir | 5 | Must | [[sprints/sprint-3/historias/HT-13 Encender los flags en los entornos\|HT-13]] | [[sprints/sprint-3/08-dudas\|E1]] ✅, [[sprints/sprint-3/08-dudas\|P10]] ✅, [[sprints/sprint-3/08-dudas\|P14]] ✅ |
| [[sprints/sprint-3/historias/HU-49 Aplicar en el roadmap las restricciones de sección y actividad que publica Courses\|HU-49]] | Aplicar en el roadmap las restricciones de sección y actividad que publica Courses | Reabrir | 8 | Should | [[sprints/sprint-3/historias/HU-67 Nodo examen con ventana horaria\|HU-67]] | [[sprints/sprint-3/08-dudas\|P9]] ✅, [[sprints/sprint-3/08-dudas\|G4]] ✅ |
| [[sprints/sprint-3/historias/HU-41 Editar un nodo del roadmap de forma individual\|HU-41]] | Editar un nodo del roadmap de forma individual | Reabrir | 3 | Must | — | — |
| [[sprints/sprint-3/historias/HU-01 Crear nodos en el grafo (unidades, contenidos, desafíos, exámenes)\|HU-01]] | Crear nodos en el grafo (unidades, contenidos, desafíos, exámenes) | Reabrir | 3 | Should | — | [[sprints/sprint-3/08-dudas\|G8]] ✅ |
| [[sprints/sprint-3/historias/HT-15 Poner Taiga al día\|HT-15]] | Poner Taiga al día | Nueva | 2 | Must | — | [[sprints/sprint-3/08-dudas\|E10]] ✅, [[sprints/sprint-3/08-dudas\|E11]] ✅ |

---

## Origen (no va a Taiga)

[[sprints/sprint-3/02-pendientes|02-pendientes]], [[sprints/sprint-3/01-estado-actual|01-estado-actual]], [[deuda-tecnica|deuda técnica]]
