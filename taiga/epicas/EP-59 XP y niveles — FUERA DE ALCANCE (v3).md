---
tags: [tpi, g10, taiga, epica]
ref: 59
estado: "New"
responsable: "Baltasar Rodriguez Teruel"
avance: "0/0"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/59
---

# EP-59: XP y niveles — FUERA DE ALCANCE (v3)

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/59) · Estado: **New** · Responsable: **Baltasar Rodriguez Teruel** · HU cerradas: **0/0**

[G10] — XP y niveles — FUERA DE ALCANCE (v3)
--------------------------------------------

* * *

Objetivo
--------

Esta épica pertenece al alcance anterior y **no forma parte del alcance v3**. Su contenido fue absorbido por **[G10] — Progreso y desbloqueo**, y su premisa central quedó invalidada: Roadmap ya no calcula XP.

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: la decisión vigente es la contraria a la que sostenía esta épica. El Motor de Desafíos envía xpOtorgado **ya calculado**, con el bonus de ítem si aplica, y Roadmap sólo lo suma al ledger propio xp\_movement. Roadmap no calcula ni emite XP. Los eventos se consumen con idempotencia por eventId y esRepeticion=true se descarta conservando la primera solución (REQ-MOT-03).
*   Restricciones (legales/técnicas): no abrir historias contra esta épica. El trabajo de ledger, idempotencia y niveles se planifica y se estima dentro de Progreso y desbloqueo. Se conserva sin borrar por RF-NFR-01 (baja lógica) y para mantener la trazabilidad de las decisiones del Sprint 1.

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] No aplica: no hay flujo propio. El flujo de XP se verifica en los criterios de Progreso y desbloqueo.
*   [ ] KPIs iniciales: no aplica.
*   [ ] Sin regresiones críticas: no aplica, la épica no tiene código asociado.
*   [ ] Observabilidad y alertas: cubiertas por Progreso y desbloqueo (contadores de eventos consumidos, deduplicados y enviados a DLQ).
*   [ ] Documentación publicada: la decisión de que el Motor calcula el XP está documentada en G10-CONTRATOS-v3 y en la descripción de Progreso y desbloqueo.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: ninguno propio. Ver Progreso y desbloqueo.
*   Módulos afectados: ninguno propio. El ledger xp\_movement pertenece a Progreso y desbloqueo.
*   Otros equipos: ninguno propio. El esquema del evento se acuerda con Grupo 09 dentro de Progreso y desbloqueo.
*   Impacto en datos / migraciones: ninguno. La tabla xp\_movement se crea en Progreso y desbloqueo.
*   Feature toggles / flags: no aplica.


## Historias

_Sin historias de G10._
