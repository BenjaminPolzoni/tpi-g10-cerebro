---
tags: [tpi, g10, sprint-3, epicas, historias]
fecha: 2026-10-15
estado: borrador
---

# 09 — Épicas e historias del Sprint 3

> [!info] Qué es esto
> Las historias del Sprint 3 con el **formato de la wiki de Taiga** (`template-hist-usuario` y `template-epicas`), listas para copiar y pegar.
> - `epicas/`: una nota por épica.
> - `historias/`: una nota por historia, con el código de Taiga (`HU-NN` / `HT-NN`).
> - **Reabrir**: la HU ya existe en Taiga y figura Done (o New) sin cumplir sus criterios; la nota tiene lo que falta. Los CA pendientes de HU cerradas van como tareas de HT-30 a HT-33 (una por tema), que referencian la HU original; solo se reabren HU-45 y HU-49, que suman alcance nuevo.
> - **Nueva**: se carga en Taiga con ese código. Las nuevas siguen la numeración del equipo: HU desde **HU-57** y HT desde **HT-12**.
> - Debajo de la línea final de cada nota hay contexto del cerebro (código actual, dependencias, dudas) que no va a Taiga.
> - No confundir con `taiga/` (raíz), que se genera desde Taiga y no se edita.

## Épicas

| Épica | Historias | Puntos |
|---|---|---|
| [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2\|Deuda del Sprint 2]] | 9 | 61 |
| [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable\|Múltiples roadmaps por curso y grafo configurable]] | 11 | 65 |
| [[sprints/sprint-3/epicas/G10 — Correcciones de los profes\|Correcciones de los profes]] | 7 | 31 |
| [[sprints/sprint-3/epicas/G10 — Consistencia visual con la UI-KIT\|Consistencia visual con la UI-KIT]] | 2 | 16 |

**Total:** 29 historias (2 a reabrir y 27 nuevas), 173 puntos. Ninguna supera 8 puntos (máximo por historia). El 2026-10-15 los CA pendientes de 10 HU cerradas quedaron en cuatro HT por tema (HT-30 a HT-33) y la UI-KIT en dos (HT-26 pantallas y HT-34 componente de grafo).

> [!note] Revisión del 2026-10-15
> Aplicada la revisión de HU: HU-60 eliminada (su validación pasó a HT-18), HU-66 fusionada en HU-62, HU-67 fusionada en HU-49, HU-63 descartada (la vista tipo Moodle ya no existe: la edición en lista está en «Contenido del curso» de Courses), solapamientos resueltos (reglas en HU-59, XP mínimo en HU-58, oculto/bloqueado en HU-49, comisión en HT-33), permisos unificados y prioridades corregidas (HU-49 y HU-59 a Must, HU-72 a Should).

## Deuda del Sprint 2

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

## Múltiples roadmaps por curso y grafo configurable

| HU | Título | En Taiga | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/HT-16 Validar la infra de Neo4j y modelar las relaciones\|HT-16]] | Validar la infra de Neo4j y modelar las relaciones | Nueva | 3 | Must | — | [[sprints/sprint-3/08-dudas\|G1]] ✅, [[sprints/sprint-3/08-dudas\|P1]] ✅, [[sprints/sprint-3/08-dudas\|P4]] ✅ |
| [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]] | Modelo 1 a N de curso a roadmaps | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-16 Validar la infra de Neo4j y modelar las relaciones\|HT-16]] | [[sprints/sprint-3/08-dudas\|P1]] ✅, [[sprints/sprint-3/08-dudas\|P2]] ✅, [[sprints/sprint-3/08-dudas\|P3]] ✅ |
| [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | Módulo graph en Neo4j y migración inicial | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-16 Validar la infra de Neo4j y modelar las relaciones\|HT-16]] | [[sprints/sprint-3/08-dudas\|P1]] ✅, [[sprints/sprint-3/08-dudas\|P4]] ✅, [[sprints/sprint-3/08-dudas\|P8]] ✅ |
| [[sprints/sprint-3/historias/HU-57 Habilitar y gestionar varios roadmaps por curso\|HU-57]] | Habilitar y gestionar varios roadmaps por curso | Nueva | 5 | Should | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]] | [[sprints/sprint-3/08-dudas\|P1]] ✅ |
| [[sprints/sprint-3/historias/HU-58 Dependencias entre secciones\|HU-58]] | Dependencias entre secciones | Nueva | 5 | Must | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]], [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]], [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas\|HU-59]] | [[sprints/sprint-3/08-dudas\|P6]] ✅ |
| [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas\|HU-59]] | Dependencias entre nodos con reglas combinadas | Nueva | 5 | Must | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]], [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | [[sprints/sprint-3/08-dudas\|P7]] ✅ |
| [[sprints/sprint-3/historias/HU-61 Roadmaps por grupo del curso y restricciones de visualización\|HU-61]] | Roadmaps por grupo del curso y restricciones de visualización | Nueva | 5 | Should | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]] | [[sprints/sprint-3/08-dudas\|P1]] ✅, [[sprints/sprint-3/08-dudas\|P2]] ✅, [[sprints/sprint-3/08-dudas\|P5]] ✅ |
| [[sprints/sprint-3/historias/HU-62 Vista de grafo cómoda para el profesor\|HU-62]] | Vista de grafo cómoda para el profesor | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]], [[sprints/sprint-3/historias/HT-34 Componente de grafo en la UI-KIT\|HT-34]], [[sprints/sprint-3/historias/HU-65 Relaciones con tipo\|HU-65]] | [[sprints/sprint-3/08-dudas\|G13]] ✅ |
| [[sprints/sprint-3/historias/HT-19 Contratos con Courses y el Motor para el modelo 1 a N\|HT-19]] | Contratos con Courses y el Motor para el modelo 1 a N | Nueva | 5 | Must | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]] | [[sprints/sprint-3/08-dudas\|P3]] ✅, [[sprints/sprint-3/08-dudas\|G4]] ✅, [[sprints/sprint-3/08-dudas\|G8]] ✅ |
| [[sprints/sprint-3/historias/HT-20 Gate y progreso con reglas combinadas y XP mínimo\|HT-20]] | Gate y progreso con reglas combinadas y XP mínimo | Nueva | 5 | Must | [[sprints/sprint-3/historias/HU-58 Dependencias entre secciones\|HU-58]], [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas\|HU-59]] | [[sprints/sprint-3/08-dudas\|P7]] ✅ |
| [[sprints/sprint-3/historias/HU-71 Clonar un roadmap con sus restricciones\|HU-71]] | Clonar un roadmap con sus restricciones | Nueva | 8 | Should | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]], [[sprints/sprint-3/historias/HU-57 Habilitar y gestionar varios roadmaps por curso\|HU-57]] | [[sprints/sprint-3/08-dudas\|G4]] ✅, [[sprints/sprint-3/08-dudas\|P17]] |

## Correcciones de los profes

| HU | Título | En Taiga | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/HU-64 Nodos de inicio y fin obligatorios\|HU-64]] | Nodos de inicio y fin obligatorios | Nueva | 5 | Must | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | — |
| [[sprints/sprint-3/historias/HU-65 Relaciones con tipo\|HU-65]] | Relaciones con tipo | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]], [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas\|HU-59]] | [[sprints/sprint-3/08-dudas\|P4]] ✅ |
| [[sprints/sprint-3/historias/HU-68 Obligatoriedad visible en la lista de nodos\|HU-68]] | Obligatoriedad visible en la lista de nodos | Nueva | 1 | Should | — | — |
| [[sprints/sprint-3/historias/HU-69 Archibaldo - Enter, avatar personalizable y destello\|HU-69]] | Archibaldo: Enter, avatar personalizable y destello | Nueva | 5 | Could | — | [[sprints/sprint-3/08-dudas\|P11]] ✅ |
| [[sprints/sprint-3/historias/HT-21 Seed de demo curado\|HT-21]] | Seed de demo curado | Nueva | 5 | Must | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]], [[sprints/sprint-3/historias/HU-57 Habilitar y gestionar varios roadmaps por curso\|HU-57]], [[sprints/sprint-3/historias/HU-58 Dependencias entre secciones\|HU-58]], [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas\|HU-59]], [[sprints/sprint-3/historias/HU-64 Nodos de inicio y fin obligatorios\|HU-64]], [[sprints/sprint-3/historias/HU-65 Relaciones con tipo\|HU-65]], [[sprints/sprint-3/historias/HU-49 Aplicar en el roadmap las restricciones de sección y actividad que publica Courses\|HU-49]], [[sprints/sprint-3/historias/HT-30 Insignias pendientes de HU-20 y HU-21\|HT-30]], G07 | [[sprints/sprint-3/08-dudas\|G7]], [[sprints/sprint-3/08-dudas\|E4]] ✅ |
| [[sprints/sprint-3/historias/HT-22 Permisos en vez de roles\|HT-22]] | Permisos en vez de roles | Nueva | 5 | Should | G07 (catálogo de permisos) | [[sprints/sprint-3/08-dudas\|G2]], [[sprints/sprint-3/08-dudas\|G6]] ✅ |
| [[sprints/sprint-3/historias/HT-23 Documentación global del micro\|HT-23]] | Documentación global del micro | Nueva | 2 | Should | — | [[sprints/sprint-3/08-dudas\|E7]] ✅ |

## Consistencia visual con la UI-KIT

| HU | Título | En Taiga | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/HT-26 Adopción de la UI-KIT en el roadmap\|HT-26]] | Adopción de la UI-KIT en el roadmap | Nueva | 8 | Must ⭐ 1 | — | [[sprints/sprint-3/08-dudas\|G13]] ✅, [[sprints/sprint-3/08-dudas\|E12]] ✅ |
| [[sprints/sprint-3/historias/HT-34 Componente de grafo en la UI-KIT\|HT-34]] | Componente de grafo en la UI-KIT | Nueva | 8 | Must ⭐ 1 | — | [[sprints/sprint-3/08-dudas\|G13]] ✅ |

## Orden sugerido

0. **Prioridad 1 (desde el día 1):** [[sprints/sprint-3/historias/HT-30 Insignias pendientes de HU-20 y HU-21|HT-30]] a HT-33 (criterios pendientes de HU cerradas, empezando por las insignias de HT-30) y [[sprints/sprint-3/historias/HT-26 Adopción de la UI-KIT en el roadmap|HT-26]] (UI-KIT) y [[sprints/sprint-3/historias/HT-34 Componente de grafo en la UI-KIT|HT-34]] (componente de grafo). Van antes que el resto.
1. **Semana 1:** el resto de la deuda del Sprint 2 y HT-16 (spike de Neo4j). Las dudas 🔴 de [[sprints/sprint-3/08-dudas|08]] (P1 a P4, G1) ya están respondidas (2026-10-15). En paralelo, lo que no depende de nada: HU-68, HU-69, HT-22 (si G07 pasó el catálogo) y HT-23.
2. **Semana 2:** HT-17 y HT-18. Front: HU-62 (con el componente de grafo de HT-34) sobre un mock de `/roadmaps/{id}/graph`. HU-64 y HU-65 sobre el módulo `graph`, y HU-49 (restricciones y examen).
3. **Cierre:** HU-57 a HU-59, HU-61, HT-19, HT-20 y HT-21. Demo con un curso completo de inicio a fin.

Dependencias y riesgos: [[sprints/sprint-3/06-backlog-sprint-3|06-backlog]].

## Entran por las respuestas del 2026-10-15

| Tema | Respuesta | Dónde |
|---|---|---|
| Racha | E12: es nueva para el Sprint 3. Hoy el front muestra un valor fijo | [[sprints/sprint-3/historias/HU-73 Ver mi racha de días con actividad\|HU-73]]. DT-13 en [[deuda-tecnica]] |
| Estado académico final | P15: entra en el Sprint 3 (antes diferido en EP-61, HU-27/28) | [[sprints/sprint-3/historias/HU-72 Cerrar el curso con el estado académico final\|HU-72]] |
| Clonar un roadmap con sus restricciones | G4: el profesor clona un roadmap para otro grupo o curso, con `node_id` nuevos (G8) | [[sprints/sprint-3/historias/HU-71 Clonar un roadmap con sus restricciones\|HU-71]] |
| Ranking por notas | P14: el profesor configura si el ranking ordena por XP o por notas; las notas vienen del Motor de desafíos | [[sprints/sprint-3/historias/HU-45 Ranking de la cohorte y avance por comisión\|HU-45]] |
| Subsecciones | P6: dependencias entre subsecciones | [[sprints/sprint-3/historias/HU-58 Dependencias entre secciones\|HU-58]] |

## No entran en el Sprint 3

| Tema | Por qué | Dónde |
|---|---|---|
| Multiple choice con boss fight | P16: es de Desafíos teóricos (G04/G09), no nuestro | [[sprints/sprint-3/08-dudas\|08]] |

> [!tip] Las que entraban sin HU ya tienen nota (HU-71, HU-72 y HU-73). Para nuevas, usar el siguiente número libre (HU-74, HT-35…), con un máximo de 8 puntos por historia, y revisar la capacidad (P12).
