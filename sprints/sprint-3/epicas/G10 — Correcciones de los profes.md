---
tags: [tpi, g10, sprint-3, epica]
estado: Propuesta
sprint: "G10 - Sprint 3"
historias: 10
puntos: 44
---

# Correcciones de los profes

> [!info] Épica del Sprint 3 · **9 historias** · **44 pts** · Estado: **Propuesta** (todavía no está en Taiga).

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
*   Impacto en datos / migraciones: START/END en roadmaps existentes; ventana horaria en exámenes; datos de demo.
*   Feature toggles / flags: Ninguno nuevo.

## Historias

| HU | Título | En Taiga | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/HU-64 Nodos de inicio y fin obligatorios\|HU-64]] | Nodos de inicio y fin obligatorios | Nueva | 5 | Must | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | — |
| [[sprints/sprint-3/historias/HU-65 Relaciones con tipo\|HU-65]] | Relaciones con tipo | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | [[sprints/sprint-3/08-dudas\|P4]] ✅ |
| [[sprints/sprint-3/historias/HU-66 Editor con arrastre y el curso como mapa\|HU-66]] | Editor con arrastre y el curso como mapa | Nueva | 8 | Should | [[sprints/sprint-3/historias/HU-62 Vista de grafo cómoda para el profesor\|HU-62]], [[sprints/sprint-3/historias/HU-65 Relaciones con tipo\|HU-65]] | [[sprints/sprint-3/08-dudas\|P1]] ✅ |
| [[sprints/sprint-3/historias/HU-67 Nodo examen con ventana horaria\|HU-67]] | Nodo examen con ventana horaria | Nueva | 5 | Must | — | [[sprints/sprint-3/08-dudas\|P9]] ✅ |
| [[sprints/sprint-3/historias/HU-68 Obligatoriedad visible en la lista de nodos\|HU-68]] | Obligatoriedad visible en la lista de nodos | Nueva | 1 | Should | — | — |
| [[sprints/sprint-3/historias/HU-69 Archibaldo - Enter, aspecto de Hernán y destello\|HU-69]] | Archibaldo: Enter, avatar personalizable y destello | Nueva | 5 | Could | — | [[sprints/sprint-3/08-dudas\|P11]] ✅ |
| [[sprints/sprint-3/historias/HT-21 Seed de demo curado\|HT-21]] | Seed de demo curado | Nueva | 5 | Must | [[sprints/sprint-3/historias/HU-64 Nodos de inicio y fin obligatorios\|HU-64]], [[sprints/sprint-3/historias/HU-65 Relaciones con tipo\|HU-65]], [[sprints/sprint-3/historias/HU-67 Nodo examen con ventana horaria\|HU-67]] | [[sprints/sprint-3/08-dudas\|G7]], [[sprints/sprint-3/08-dudas\|E4]] ✅ |
| [[sprints/sprint-3/historias/HT-22 Permisos en vez de roles\|HT-22]] | Permisos en vez de roles | Nueva | 5 | Should | — | [[sprints/sprint-3/08-dudas\|G2]], [[sprints/sprint-3/08-dudas\|G6]] ✅ |
| [[sprints/sprint-3/historias/HT-23 Documentación global del micro\|HT-23]] | Documentación global del micro | Nueva | 2 | Should | — | [[sprints/sprint-3/08-dudas\|E7]] ✅ |

---

## Origen (no va a Taiga)

[[sprints/sprint-3/07-correcciones-profes|07-correcciones-profes]], [[sprints/sprint-3/fuentes/correcciones-profes-original|original de los profes]]
