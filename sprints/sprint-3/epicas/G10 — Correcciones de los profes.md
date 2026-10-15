---
tags: [tpi, g10, sprint-3, epica]
estado: Propuesta
sprint: "G10 - Sprint 3"
historias: 7
puntos: 31
---

# Correcciones de los profes

> [!info] Épica del Sprint 3 · **7 historias** · **31 pts** · Estado: **New** · En Taiga: [[taiga/epicas/EP-8631 Correcciones de los profes|EP-8631]].

[G10] — Correcciones de los profes
----------------------------------

* * *

Objetivo
--------

Resolver las correcciones que los profes marcaron como nuestras (2026-10-14).

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: Correcciones del documento de los profes (2026-10-14), solo las marcadas como nuestras.
*   Restricciones (legales/técnicas): Las que dependen de otros grupos (catálogo de permisos y usuarios demo de G07) se coordinan; no se implementa lo que es de ellos.

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] Cada corrección marcada como nuestra en [[sprints/sprint-3/07-correcciones-profes|07]] tiene su HU cerrada o una respuesta de los profes que la redefine.
*   [ ] La demo muestra un curso completo de inicio ("Bienvenidos") a fin ("Felicitaciones").
*   [ ] KPIs iniciales alcanzan: Correcciones nuestras resueltas: 11 de 11, o redefinidas con respuesta de los profes.
*   [ ] Sin regresiones críticas en: El ranking mantiene el anonimato (DEC-007). Migrar a permisos no deja ningún endpoint abierto.
*   [ ] Observabilidad y alertas configuradas: Errores del ranking por grupo; 403 por permisos mal asignados.
*   [ ] Documentación de uso y operación publicada: Documentación global del micro (HT-23).

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: Backoffice (permisos, dashboard), Users (usuarios demo), Courses.
*   Módulos afectados: Módulo graph, editor, ranking, mundo 3D, seguridad, seed.
*   Otros equipos: G06, G07, G01.
*   Impacto en datos / migraciones: START/END en roadmaps existentes; configuración de Archibaldo por curso; datos de demo.
*   Feature toggles / flags: Ninguno nuevo.

## Historias

| HU | Título | En Taiga | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/HU-64 Nodos de inicio y fin obligatorios\|HU-64]] | Nodos de inicio y fin obligatorios | Nueva | 5 | Must | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | — |
| [[sprints/sprint-3/historias/HU-65 Relaciones con tipo\|HU-65]] | Relaciones con tipo | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]], [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas\|HU-59]] | [[sprints/sprint-3/08-dudas\|P4]] ✅ |
| [[sprints/sprint-3/historias/HU-68 Obligatoriedad visible en la lista de nodos\|HU-68]] | Obligatoriedad visible en la lista de nodos | Nueva | 1 | Should | — | — |
| [[sprints/sprint-3/historias/HU-69 Archibaldo - Enter, avatar personalizable y destello\|HU-69]] | Archibaldo: Enter, avatar personalizable y destello | Nueva | 5 | Could | — | [[sprints/sprint-3/08-dudas\|P11]] ✅ |
| [[sprints/sprint-3/historias/HT-21 Seed de demo curado\|HT-21]] | Seed de demo curado | Nueva | 5 | Must | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]], [[sprints/sprint-3/historias/HU-57 Habilitar y gestionar varios roadmaps por curso\|HU-57]], [[sprints/sprint-3/historias/HU-58 Dependencias entre secciones\|HU-58]], [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas\|HU-59]], [[sprints/sprint-3/historias/HU-64 Nodos de inicio y fin obligatorios\|HU-64]], [[sprints/sprint-3/historias/HU-65 Relaciones con tipo\|HU-65]], [[sprints/sprint-3/historias/HU-49 Aplicar en el roadmap las restricciones de sección y actividad que publica Courses\|HU-49]], [[sprints/sprint-3/historias/HT-30 Insignias pendientes de HU-20 y HU-21\|HT-30]], G07 | [[sprints/sprint-3/08-dudas\|G7]], [[sprints/sprint-3/08-dudas\|E4]] ✅ |
| [[sprints/sprint-3/historias/HT-22 Permisos en vez de roles\|HT-22]] | Permisos en vez de roles | Nueva | 5 | Should | G07 (catálogo de permisos) | [[sprints/sprint-3/08-dudas\|G2]], [[sprints/sprint-3/08-dudas\|G6]] ✅ |
| [[sprints/sprint-3/historias/HT-23 Documentación global del micro\|HT-23]] | Documentación global del micro | Nueva | 2 | Should | — | [[sprints/sprint-3/08-dudas\|E7]] ✅ |

---

## Origen (no va a Taiga)

[[sprints/sprint-3/07-correcciones-profes|07-correcciones-profes]], [[sprints/sprint-3/fuentes/correcciones-profes-original|original de los profes]]
