---
tags: [tpi, g10, sprint-3, epica]
id: EP-S3-2
estado: Propuesta
historias: 11
puntos: 52
---

# EP-S3-2: Correcciones de los profes

> [!info] Épica propuesta del Sprint 3. **11 historias**, **52 pts**. Todavía no está en Taiga.
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Objetivo* hasta *Dependencias / Impactos*.

**[G10] — Correcciones de los profes**

* * *

## Objetivo

Resolver las correcciones que los profes marcaron como nuestras (2026-10-14).

* * *

## Suposiciones y Restricciones

- Suposiciones: Correcciones del documento de los profes (2026-10-14), solo las marcadas como nuestras.
- Restricciones (legales/técnicas): Las que dependen de otros grupos (permisos de G06, usuarios demo de G07) se coordinan; no se implementa lo que es de ellos.

* * *

## Criterios de Aceptación a nivel Épico

- [ ] Cada corrección marcada como nuestra en [[sprints/sprint-3/07-correcciones-profes|07]] tiene su HU cerrada o una respuesta de los profes que la redefine.
- [ ] La demo muestra un curso completo de inicio ("Bienvenidos") a fin ("Felicitaciones").
- [ ] KPIs iniciales: Correcciones nuestras resueltas: 11 de 11, o redefinidas con respuesta de los profes.
- [ ] Sin regresiones críticas: El ranking mantiene el anonimato (DEC-007). Migrar a permisos no deja ningún endpoint abierto.
- [ ] Observabilidad y alertas: Errores del ranking por grupo; 403 por permisos mal asignados.
- [ ] Documentación publicada: Documentación global del micro (C10) y acuerdo con G06 (C11).

* * *

## Dependencias / Impactos

- Servicios / APIs: Backoffice (permisos, dashboard), Users (usuarios demo), Courses.
- Módulos afectados: Módulo graph, editor, ranking, mundo 3D, seguridad, seed.
- Otros equipos: G06, G07, G01.
- Impacto en datos / migraciones: START/END en roadmaps existentes; ventana horaria en exámenes; datos de demo.
- Feature toggles / flags: Ninguno nuevo.

---

## Historias

| ID | Tipo | Título | Capa | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/C01 Nodos de inicio y fin obligatorios\|C01]] | HU | Nodos de inicio y fin obligatorios | Back + Front | 5 | Must | [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial\|M03]] | — |
| [[sprints/sprint-3/historias/C02 Relaciones con tipo\|C02]] | HU | Relaciones con tipo | Back + Front | 8 | Must | [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial\|M03]] | [[sprints/sprint-3/08-dudas\|P4]] |
| [[sprints/sprint-3/historias/C03 Editor con arrastre y el curso como mapa\|C03]] | HU | Editor con arrastre y el curso como mapa | Front | 8 | Should | [[sprints/sprint-3/historias/M09 Vista de grafo cómoda para el profesor\|M09]], [[sprints/sprint-3/historias/C02 Relaciones con tipo\|C02]] | [[sprints/sprint-3/08-dudas\|P1]] |
| [[sprints/sprint-3/historias/C04 Nodo examen con ventana horaria\|C04]] | HU | Nodo examen con ventana horaria | Back + Front | 5 | Must | — | [[sprints/sprint-3/08-dudas\|P9]] |
| [[sprints/sprint-3/historias/C05 Obligatoriedad visible en la lista de nodos\|C05]] | HU | Obligatoriedad visible en la lista de nodos | Front | 2 | Should | — | — |
| [[sprints/sprint-3/historias/C06 Ranking por grupo con error\|C06]] | Bug | Ranking por grupo con error | Back + Front | 5 | Must | [[sprints/sprint-3/historias/B02 Encender los flags en los entornos\|B02]] | [[sprints/sprint-3/08-dudas\|E1]], [[sprints/sprint-3/08-dudas\|P10]], [[sprints/sprint-3/08-dudas\|P14]] |
| [[sprints/sprint-3/historias/C07 Archibaldo - Enter, aspecto de Hernán y destello\|C07]] | HU | Archibaldo: Enter, aspecto de Hernán y destello | Front (3D) | 5 | Could | — | [[sprints/sprint-3/08-dudas\|P11]] |
| [[sprints/sprint-3/historias/C08 Seed de demo curado\|C08]] | HT | Seed de demo curado | Back | 5 | Must | [[sprints/sprint-3/historias/C01 Nodos de inicio y fin obligatorios\|C01]], [[sprints/sprint-3/historias/C02 Relaciones con tipo\|C02]], [[sprints/sprint-3/historias/C04 Nodo examen con ventana horaria\|C04]] | [[sprints/sprint-3/08-dudas\|G7]], [[sprints/sprint-3/08-dudas\|E4]] |
| [[sprints/sprint-3/historias/C09 Permisos en vez de roles\|C09]] | HT | Permisos en vez de roles | Back | 5 | Should | — | [[sprints/sprint-3/08-dudas\|G2]], [[sprints/sprint-3/08-dudas\|G6]] |
| [[sprints/sprint-3/historias/C10 Documentación global del micro\|C10]] | HT | Documentación global del micro | Docs | 2 | Should | — | [[sprints/sprint-3/08-dudas\|E7]] |
| [[sprints/sprint-3/historias/C11 Datos para el dashboard de G06\|C11]] | HT | Datos para el dashboard de G06 | Back + acuerdo | 2 | Should | — | [[sprints/sprint-3/08-dudas\|G3]] |

## Origen

[[sprints/sprint-3/07-correcciones-profes|07-correcciones-profes]], [[sprints/sprint-3/fuentes/correcciones-profes-original|original de los profes]]
