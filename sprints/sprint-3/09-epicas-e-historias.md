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
> - **Reabrir**: la HU ya existe en Taiga y figura Done (o New) sin cumplir sus criterios; la nota tiene lo que falta.
> - **Nueva**: se carga en Taiga con ese código. Las nuevas siguen la numeración del equipo: HU desde **HU-57** y HT desde **HT-12**.
> - Debajo de la línea final de cada nota hay contexto del cerebro (código actual, dependencias, dudas) que no va a Taiga.
> - No confundir con `taiga/` (raíz), que se genera desde Taiga y no se edita.

## Épicas

| Épica | Historias | Puntos |
|---|---|---|
| [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2\|Deuda del Sprint 2]] | 15 | 63 |
| [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable\|Múltiples roadmaps por curso y grafo configurable]] | 13 | 76 |
| [[sprints/sprint-3/epicas/G10 — Correcciones de los profes\|Correcciones de los profes]] | 9 | 45 |
| [[sprints/sprint-3/epicas/G10 — Consistencia visual con la UI-KIT\|Consistencia visual con la UI-KIT]] | 1 | 21 |

**Total:** 38 historias (12 a reabrir y 26 nuevas), 205 puntos. Todo lo de la UI-KIT quedó en una sola HT (HT-26) el 2026-10-15.

## Deuda del Sprint 2

| HU | Título | En Taiga | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/HT-14 Sacar los IDs de mock del front\|HT-14]] | Sacar los IDs de mock del front | Nueva | 3 | Must | — | — |
| [[sprints/sprint-3/historias/HU-48 CA1 pendiente - pre-chequeo con el JWT del alumno\|HU-48]] | CA1 pendiente - pre-chequeo con el JWT del alumno | Reabrir | 3 | Must | — | — |
| [[sprints/sprint-3/historias/HU-20 Sin CA pendiente - editar y dar de baja insignias en el front\|HU-20]] | Sin CA pendiente - editar y dar de baja insignias en el front | Reabrir | 3 | Should | — | — |
| [[sprints/sprint-3/historias/HU-21 CA1 pendiente - 3 criterios que nunca se otorgan\|HU-21]] | CA1 pendiente - 3 criterios que nunca se otorgan | Reabrir | 5 | Should | — | [[sprints/sprint-3/08-dudas\|E2]] ✅, [[sprints/sprint-3/08-dudas\|E8]] ✅ |
| [[sprints/sprint-3/historias/HU-15 CA5 pendiente - motivo origen_no_disponible\|HU-15]] | CA5 pendiente - motivo origen_no_disponible | Reabrir | 3 | Should | — | [[sprints/sprint-3/08-dudas\|E9]] ✅ |
| [[sprints/sprint-3/historias/HU-16 CA3 pendiente - último dato de vidas si Accounting cae\|HU-16]] | CA3 pendiente - último dato de vidas si Accounting cae | Reabrir | 3 | Should | — | — |
| [[sprints/sprint-3/historias/HU-43 Sin CA pendiente - ícono solo en desafíos y exámenes\|HU-43]] | Sin CA pendiente - ícono solo en desafíos y exámenes | Reabrir | 1 | Could | — | — |
| [[sprints/sprint-3/historias/HU-46 CA1 y CA3 pendientes - Templo y visor embebido\|HU-46]] | CA1 y CA3 pendientes - Templo y visor embebido | Reabrir | 5 | Should | — | [[sprints/sprint-3/08-dudas\|P13]] ✅ |
| [[sprints/sprint-3/historias/HU-44 CA2 pendiente - selector de comisión en el front\|HU-44]] | CA2 pendiente - selector de comisión en el front | Reabrir | 5 | Must | — | [[sprints/sprint-3/08-dudas\|P5]] ✅ |
| [[sprints/sprint-3/historias/HU-45 Ranking de la cohorte y avance por comisión\|HU-45]] | Ranking de la cohorte y avance por comisión | Reabrir | 5 | Must | — | [[sprints/sprint-3/08-dudas\|E1]] ✅, [[sprints/sprint-3/08-dudas\|P10]] ✅, [[sprints/sprint-3/08-dudas\|P14]] ✅ |
| [[sprints/sprint-3/historias/HU-49 Aplicar en el roadmap las restricciones de sección y actividad que publica Courses\|HU-49]] | Aplicar en el roadmap las restricciones de sección y actividad que publica Courses | Reabrir | 8 | Should | [[sprints/sprint-3/historias/HU-67 Nodo examen con ventana horaria\|HU-67]] | [[sprints/sprint-3/08-dudas\|P9]] ✅, [[sprints/sprint-3/08-dudas\|G4]] ✅ |
| [[sprints/sprint-3/historias/HU-41 CA2 pendiente - reintentos y política de vidas\|HU-41]] | CA2 pendiente - reintentos y política de vidas | Reabrir | 3 | Must | — | — |
| [[sprints/sprint-3/historias/HU-01 CA8 pendiente - baja de desafío del Motor\|HU-01]] | CA8 pendiente - baja de desafío del Motor | Reabrir | 3 | Should | — | [[sprints/sprint-3/08-dudas\|G8]] ✅ |
| [[sprints/sprint-3/historias/HU-72 Cerrar el curso con el estado académico final\|HU-72]] | Cerrar el curso con el estado académico final | Nueva | 8 | Must | [[sprints/sprint-3/historias/HU-45 Ranking de la cohorte y avance por comisión\|HU-45]] | [[sprints/sprint-3/08-dudas\|P15]] ✅, [[sprints/sprint-3/08-dudas\|G14]] |
| [[sprints/sprint-3/historias/HU-73 Ver mi racha de días con actividad\|HU-73]] | Ver mi racha de días con actividad | Nueva | 5 | Should | — | [[sprints/sprint-3/08-dudas\|E12]] ✅ |

## Múltiples roadmaps por curso y grafo configurable

| HU | Título | En Taiga | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/HT-16 Validar la infra de Neo4j y modelar las relaciones\|HT-16]] | Validar la infra de Neo4j y modelar las relaciones | Nueva | 3 | Must | — | [[sprints/sprint-3/08-dudas\|G1]] ✅, [[sprints/sprint-3/08-dudas\|P1]] ✅, [[sprints/sprint-3/08-dudas\|P4]] ✅ |
| [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]] | Modelo 1 a N de curso a roadmaps | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-16 Validar la infra de Neo4j y modelar las relaciones\|HT-16]] | [[sprints/sprint-3/08-dudas\|P1]] ✅, [[sprints/sprint-3/08-dudas\|P2]] ✅, [[sprints/sprint-3/08-dudas\|P3]] ✅ |
| [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | Módulo graph en Neo4j y migración inicial | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-16 Validar la infra de Neo4j y modelar las relaciones\|HT-16]] | [[sprints/sprint-3/08-dudas\|P1]] ✅, [[sprints/sprint-3/08-dudas\|P4]] ✅, [[sprints/sprint-3/08-dudas\|P8]] ✅ |
| [[sprints/sprint-3/historias/HU-57 Habilitar y gestionar varios roadmaps por curso\|HU-57]] | Habilitar y gestionar varios roadmaps por curso | Nueva | 5 | Should | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]] | [[sprints/sprint-3/08-dudas\|P1]] ✅ |
| [[sprints/sprint-3/historias/HU-58 Dependencias entre secciones\|HU-58]] | Dependencias entre secciones | Nueva | 5 | Must | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]], [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | [[sprints/sprint-3/08-dudas\|P6]] ✅ |
| [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas\|HU-59]] | Dependencias entre nodos con reglas combinadas | Nueva | 5 | Should | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]], [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | [[sprints/sprint-3/08-dudas\|P7]] ✅ |
| [[sprints/sprint-3/historias/HU-60 Propiedades personalizadas en nodos y secciones\|HU-60]] | Propiedades personalizadas en nodos y secciones | Nueva | 3 | Could | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | [[sprints/sprint-3/08-dudas\|P8]] ✅ |
| [[sprints/sprint-3/historias/HU-61 El alumno elige qué roadmap recorrer\|HU-61]] | El alumno elige qué roadmap recorrer | Nueva | 5 | Should | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]] | [[sprints/sprint-3/08-dudas\|P1]] ✅, [[sprints/sprint-3/08-dudas\|P2]] ✅, [[sprints/sprint-3/08-dudas\|P5]] ✅ |
| [[sprints/sprint-3/historias/HU-62 Vista de grafo cómoda para el profesor\|HU-62]] | Vista de grafo cómoda para el profesor | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]], [[sprints/sprint-3/historias/HT-26 Adopción de la UI-KIT en el roadmap\|HT-26]] | [[sprints/sprint-3/08-dudas\|G13]] ✅ |
| [[sprints/sprint-3/historias/HU-63 Vista tipo Moodle con la UI-KIT\|HU-63]] | Vista tipo Moodle con la UI-KIT | Nueva | 8 | Should | [[sprints/sprint-3/historias/HT-26 Adopción de la UI-KIT en el roadmap\|HT-26]] | [[sprints/sprint-3/08-dudas\|P1]] ✅ |
| [[sprints/sprint-3/historias/HT-19 Contratos con Courses y el Motor para el modelo 1 a N\|HT-19]] | Contratos con Courses y el Motor para el modelo 1 a N | Nueva | 5 | Must | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]] | [[sprints/sprint-3/08-dudas\|P3]] ✅, [[sprints/sprint-3/08-dudas\|G4]] ✅, [[sprints/sprint-3/08-dudas\|G8]] ✅ |
| [[sprints/sprint-3/historias/HT-20 Gate y progreso con reglas combinadas y XP mínimo\|HT-20]] | Gate y progreso con reglas combinadas y XP mínimo | Nueva | 5 | Must | [[sprints/sprint-3/historias/HU-58 Dependencias entre secciones\|HU-58]], [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas\|HU-59]] | [[sprints/sprint-3/08-dudas\|P7]] ✅ |
| [[sprints/sprint-3/historias/HU-71 Clonar un roadmap con sus restricciones\|HU-71]] | Clonar un roadmap con sus restricciones | Nueva | 8 | Should | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]], [[sprints/sprint-3/historias/HU-57 Habilitar y gestionar varios roadmaps por curso\|HU-57]] | [[sprints/sprint-3/08-dudas\|G4]] ✅, [[sprints/sprint-3/08-dudas\|P17]] |

## Correcciones de los profes

| HU | Título | En Taiga | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/HU-64 Nodos de inicio y fin obligatorios\|HU-64]] | Nodos de inicio y fin obligatorios | Nueva | 5 | Must | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | — |
| [[sprints/sprint-3/historias/HU-65 Relaciones con tipo\|HU-65]] | Relaciones con tipo | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | [[sprints/sprint-3/08-dudas\|P4]] ✅ |
| [[sprints/sprint-3/historias/HU-66 Editor con arrastre y el curso como mapa\|HU-66]] | Editor con arrastre y el curso como mapa | Nueva | 8 | Should | [[sprints/sprint-3/historias/HU-62 Vista de grafo cómoda para el profesor\|HU-62]], [[sprints/sprint-3/historias/HU-65 Relaciones con tipo\|HU-65]] | [[sprints/sprint-3/08-dudas\|P1]] ✅ |
| [[sprints/sprint-3/historias/HU-67 Nodo examen con ventana horaria\|HU-67]] | Nodo examen con ventana horaria | Nueva | 5 | Must | — | [[sprints/sprint-3/08-dudas\|P9]] ✅ |
| [[sprints/sprint-3/historias/HU-68 Obligatoriedad visible en la lista de nodos\|HU-68]] | Obligatoriedad visible en la lista de nodos | Nueva | 2 | Should | — | — |
| [[sprints/sprint-3/historias/HU-69 Archibaldo - Enter, aspecto de Hernán y destello\|HU-69]] | Archibaldo: Enter, avatar personalizable y destello | Nueva | 5 | Could | — | [[sprints/sprint-3/08-dudas\|P11]] ✅ |
| [[sprints/sprint-3/historias/HT-21 Seed de demo curado\|HT-21]] | Seed de demo curado | Nueva | 5 | Must | [[sprints/sprint-3/historias/HU-64 Nodos de inicio y fin obligatorios\|HU-64]], [[sprints/sprint-3/historias/HU-65 Relaciones con tipo\|HU-65]], [[sprints/sprint-3/historias/HU-67 Nodo examen con ventana horaria\|HU-67]] | [[sprints/sprint-3/08-dudas\|G7]], [[sprints/sprint-3/08-dudas\|E4]] ✅ |
| [[sprints/sprint-3/historias/HT-22 Permisos en vez de roles\|HT-22]] | Permisos en vez de roles | Nueva | 5 | Should | — | [[sprints/sprint-3/08-dudas\|G2]], [[sprints/sprint-3/08-dudas\|G6]] ✅ |
| [[sprints/sprint-3/historias/HT-23 Documentación global del micro\|HT-23]] | Documentación global del micro | Nueva | 2 | Should | — | [[sprints/sprint-3/08-dudas\|E7]] ✅ |

## Consistencia visual con la UI-KIT

| HU | Título | En Taiga | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/HT-26 Adopción de la UI-KIT en el roadmap\|HT-26]] | Adopción de la UI-KIT en el roadmap | Nueva | 21 | Must | — | [[sprints/sprint-3/08-dudas\|G13]] ✅, [[sprints/sprint-3/08-dudas\|E12]] ✅ |

## Orden sugerido

1. **Semana 1:** toda la deuda del Sprint 2 y HT-16 (spike de Neo4j). Las dudas 🔴 de [[sprints/sprint-3/08-dudas|08]] (P1 a P4, G1) ya están respondidas (2026-10-15). En paralelo, lo que no depende de nada: HU-67, HU-68, HU-69, HT-22 (si G07 pasó el catálogo) y HT-23.
2. **Semana 2:** HT-17 y HT-18. Front: HT-26 (UI-KIT y componente de grafo), HU-62 y HU-63 sobre un mock de `/roadmaps/{id}/graph`. HU-64 y HU-65 sobre el módulo `graph`.
3. **Cierre:** HU-57 a HU-61, HT-19, HT-20, HU-66 y HT-21. Demo con un curso completo de inicio a fin.

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

> [!tip] Las que entraban sin HU ya tienen nota (HU-71, HU-72 y HU-73). Para nuevas, usar el siguiente número libre (HU-74, HT-30…) y revisar la capacidad (P12).
