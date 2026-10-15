---
tags: [tpi, g10, taiga, epica]
ref: 8632
estado: "New"
responsable: "Sin asignar"
avance: "0/9"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/8632
---

# EP-8632: Deuda del Sprint 2

> [!info] Generado desde Taiga (2026-10-15 16:56). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/8632) · Estado: **New** · Responsable: **Sin asignar** · HU cerradas: **0/9**

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

| HU | Estado | Responsable | Sprint | Tareas |
|---|---|---|---|---|
| [[historias/HU-45 Ranking de la cohorte y avance por comisión\|HU-45]] Ranking de la cohorte y avance por comisión | New | Lorenzo Araujo | G10 - Sprint 03 | 5/13 |
| [[historias/HU-49 Aplicar en el roadmap las restricciones de sección y actividad que publica Courses\|HU-49]] Aplicar en el roadmap las restricciones de sección y actividad que publica Courses | New | Sin asignar | G10 - Sprint 03 | 0/6 |
| [[historias/HT-14 Sacar los IDs de mock del front\|HT-14]] Sacar los IDs de mock del front | New | Sin asignar | G10 - Sprint 03 | 0/5 |
| [[historias/HU-72 Cerrar el curso con el estado académico final\|HU-72]] Cerrar el curso con el estado académico final | New | Sin asignar | G10 - Sprint 03 | 0/5 |
| [[historias/HU-73 Ver mi racha de días con actividad\|HU-73]] Ver mi racha de días con actividad | New | Sin asignar | G10 - Sprint 03 | 0/5 |
| [[historias/HT-30 Insignias pendientes de HU-20 y HU-21\|HT-30]] Insignias pendientes de HU-20 y HU-21 | New | Sin asignar | G10 - Sprint 03 | 0/6 |
| [[historias/HT-31 Gate y vidas pendientes de HU-15, HU-16 y HU-48\|HT-31]] Gate y vidas pendientes de HU-15, HU-16 y HU-48 | New | Sin asignar | G10 - Sprint 03 | 0/7 |
| [[historias/HT-32 Nodos y editor pendientes de HU-01, HU-41 y HU-43\|HT-32]] Nodos y editor pendientes de HU-01, HU-41 y HU-43 | New | Sin asignar | G10 - Sprint 03 | 0/6 |
| [[historias/HT-33 Comisión y material pendientes de HU-44 y HU-46\|HT-33]] Comisión y material pendientes de HU-44 y HU-46 | New | Sin asignar | G10 - Sprint 03 | 0/6 |
