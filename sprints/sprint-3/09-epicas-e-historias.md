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
| [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2\|Deuda del Sprint 2]] | 16 | 56 |
| [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable\|Múltiples roadmaps por curso y grafo configurable]] | 12 | 68 |
| [[sprints/sprint-3/epicas/G10 — Correcciones de los profes\|Correcciones de los profes]] | 10 | 47 |
| [[sprints/sprint-3/epicas/G10 — Consistencia visual con la UI-KIT\|Consistencia visual con la UI-KIT]] | 6 | 27 |

**Total:** 44 historias (12 a reabrir y 32 nuevas), 198 puntos.

## Deuda del Sprint 2

| HU | Título | En Taiga | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/HT-12 Cerrar o mergear las ramas colgadas del back\|HT-12]] | Cerrar o mergear las ramas colgadas del back | Nueva | 2 | Must | — | [[sprints/sprint-3/08-dudas\|E5]] |
| [[sprints/sprint-3/historias/HT-13 Encender los flags en los entornos\|HT-13]] | Encender los flags en los entornos | Nueva | 2 | Must | — | [[sprints/sprint-3/08-dudas\|E6]] |
| [[sprints/sprint-3/historias/HT-14 Sacar los IDs de mock del front\|HT-14]] | Sacar los IDs de mock del front | Nueva | 3 | Must | — | — |
| [[sprints/sprint-3/historias/HU-48 Saber si puedo entrar a un desafío antes de abrirlo\|HU-48]] | Saber si puedo entrar a un desafío antes de abrirlo | Reabrir | 3 | Must | — | — |
| [[sprints/sprint-3/historias/HU-20 Definir el catálogo de insignias del curso\|HU-20]] | Definir el catálogo de insignias del curso | Reabrir | 3 | Should | — | — |
| [[sprints/sprint-3/historias/HU-21 Otorgar insignias automáticamente\|HU-21]] | Otorgar insignias automáticamente | Reabrir | 5 | Should | — | [[sprints/sprint-3/08-dudas\|E2]], [[sprints/sprint-3/08-dudas\|E8]] |
| [[sprints/sprint-3/historias/HU-15 Impedir la entrega en un nodo bloqueado (gate, vocabulario v3)\|HU-15]] | Impedir la entrega en un nodo bloqueado (gate, vocabulario v3) | Reabrir | 3 | Should | — | [[sprints/sprint-3/08-dudas\|E9]] |
| [[sprints/sprint-3/historias/HU-16 Integración real con Inventario para las vidas del gate\|HU-16]] | Integración real con Inventario para las vidas del gate | Reabrir | 3 | Should | — | — |
| [[sprints/sprint-3/historias/HU-43 Elegir el ícono de un desafío\|HU-43]] | Elegir el ícono de un desafío | Reabrir | 1 | Could | — | — |
| [[sprints/sprint-3/historias/HU-46 Ver en los nodos y en el Templo el material teórico de Courses\|HU-46]] | Ver en los nodos y en el Templo el material teórico de Courses | Reabrir | 5 | Should | — | [[sprints/sprint-3/08-dudas\|P13]] |
| [[sprints/sprint-3/historias/HU-44 Ver el roadmap de cada una de mis comisiones\|HU-44]] | Ver el roadmap de cada una de mis comisiones | Reabrir | 5 | Must | [[sprints/sprint-3/historias/HT-13 Encender los flags en los entornos\|HT-13]] | [[sprints/sprint-3/08-dudas\|P5]] |
| [[sprints/sprint-3/historias/HU-45 Ranking de la cohorte y avance por comisión\|HU-45]] | Ranking de la cohorte y avance por comisión | Reabrir | 5 | Must | [[sprints/sprint-3/historias/HT-13 Encender los flags en los entornos\|HT-13]] | [[sprints/sprint-3/08-dudas\|E1]], [[sprints/sprint-3/08-dudas\|P10]], [[sprints/sprint-3/08-dudas\|P14]] |
| [[sprints/sprint-3/historias/HU-49 Aplicar en el roadmap las restricciones de sección y actividad que publica Courses\|HU-49]] | Aplicar en el roadmap las restricciones de sección y actividad que publica Courses | Reabrir | 8 | Should | [[sprints/sprint-3/historias/HU-67 Nodo examen con ventana horaria\|HU-67]] | [[sprints/sprint-3/08-dudas\|P9]], [[sprints/sprint-3/08-dudas\|G4]] |
| [[sprints/sprint-3/historias/HU-41 Editar un nodo del roadmap de forma individual\|HU-41]] | Editar un nodo del roadmap de forma individual | Reabrir | 3 | Must | — | — |
| [[sprints/sprint-3/historias/HU-01 Crear nodos en el grafo (unidades, contenidos, desafíos, exámenes)\|HU-01]] | Crear nodos en el grafo (unidades, contenidos, desafíos, exámenes) | Reabrir | 3 | Should | — | [[sprints/sprint-3/08-dudas\|G8]] |
| [[sprints/sprint-3/historias/HT-15 Poner Taiga al día\|HT-15]] | Poner Taiga al día | Nueva | 2 | Must | — | [[sprints/sprint-3/08-dudas\|E10]], [[sprints/sprint-3/08-dudas\|E11]] |

## Múltiples roadmaps por curso y grafo configurable

| HU | Título | En Taiga | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/HT-16 Validar la infra de Neo4j y modelar las relaciones\|HT-16]] | Validar la infra de Neo4j y modelar las relaciones | Nueva | 3 | Must | — | [[sprints/sprint-3/08-dudas\|G1]], [[sprints/sprint-3/08-dudas\|P1]], [[sprints/sprint-3/08-dudas\|P4]] |
| [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]] | Modelo 1 a N de curso a roadmaps | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-16 Validar la infra de Neo4j y modelar las relaciones\|HT-16]] | [[sprints/sprint-3/08-dudas\|P1]], [[sprints/sprint-3/08-dudas\|P2]], [[sprints/sprint-3/08-dudas\|P3]] |
| [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | Módulo graph en Neo4j y migración inicial | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-16 Validar la infra de Neo4j y modelar las relaciones\|HT-16]] | [[sprints/sprint-3/08-dudas\|P1]], [[sprints/sprint-3/08-dudas\|P4]], [[sprints/sprint-3/08-dudas\|P8]] |
| [[sprints/sprint-3/historias/HU-57 Habilitar y gestionar varios roadmaps por curso\|HU-57]] | Habilitar y gestionar varios roadmaps por curso | Nueva | 5 | Should | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]] | [[sprints/sprint-3/08-dudas\|P1]] |
| [[sprints/sprint-3/historias/HU-58 Dependencias entre secciones\|HU-58]] | Dependencias entre secciones | Nueva | 5 | Must | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]], [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | [[sprints/sprint-3/08-dudas\|P6]] |
| [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas\|HU-59]] | Dependencias entre nodos con reglas combinadas | Nueva | 5 | Should | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]], [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | [[sprints/sprint-3/08-dudas\|P7]] |
| [[sprints/sprint-3/historias/HU-60 Propiedades personalizadas en nodos y secciones\|HU-60]] | Propiedades personalizadas en nodos y secciones | Nueva | 3 | Could | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | [[sprints/sprint-3/08-dudas\|P8]] |
| [[sprints/sprint-3/historias/HU-61 El alumno elige qué roadmap recorrer\|HU-61]] | El alumno elige qué roadmap recorrer | Nueva | 5 | Should | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]] | [[sprints/sprint-3/08-dudas\|P1]], [[sprints/sprint-3/08-dudas\|P2]], [[sprints/sprint-3/08-dudas\|P5]] |
| [[sprints/sprint-3/historias/HU-62 Vista de grafo cómoda para el profesor\|HU-62]] | Vista de grafo cómoda para el profesor | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]], [[sprints/sprint-3/historias/HU-70 Componente de grafo en la UI-KIT\|HU-70]] | [[sprints/sprint-3/08-dudas\|G13]] |
| [[sprints/sprint-3/historias/HU-63 Vista tipo Moodle con la UI-KIT\|HU-63]] | Vista tipo Moodle con la UI-KIT | Nueva | 8 | Should | [[sprints/sprint-3/historias/HT-25 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|HT-25]], [[sprints/sprint-3/historias/HT-26 Controles y botones del roadmap con el kit\|HT-26]] | [[sprints/sprint-3/08-dudas\|P1]] |
| [[sprints/sprint-3/historias/HT-19 Contratos con Courses y el Motor para el modelo 1 a N\|HT-19]] | Contratos con Courses y el Motor para el modelo 1 a N | Nueva | 5 | Must | [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps\|HT-17]] | [[sprints/sprint-3/08-dudas\|P3]], [[sprints/sprint-3/08-dudas\|G4]], [[sprints/sprint-3/08-dudas\|G8]] |
| [[sprints/sprint-3/historias/HT-20 Gate y progreso con reglas combinadas y XP mínimo\|HT-20]] | Gate y progreso con reglas combinadas y XP mínimo | Nueva | 5 | Must | [[sprints/sprint-3/historias/HU-58 Dependencias entre secciones\|HU-58]], [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas\|HU-59]] | [[sprints/sprint-3/08-dudas\|P7]] |

## Correcciones de los profes

| HU | Título | En Taiga | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/HU-64 Nodos de inicio y fin obligatorios\|HU-64]] | Nodos de inicio y fin obligatorios | Nueva | 5 | Must | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | — |
| [[sprints/sprint-3/historias/HU-65 Relaciones con tipo\|HU-65]] | Relaciones con tipo | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial\|HT-18]] | [[sprints/sprint-3/08-dudas\|P4]] |
| [[sprints/sprint-3/historias/HU-66 Editor con arrastre y el curso como mapa\|HU-66]] | Editor con arrastre y el curso como mapa | Nueva | 8 | Should | [[sprints/sprint-3/historias/HU-62 Vista de grafo cómoda para el profesor\|HU-62]], [[sprints/sprint-3/historias/HU-65 Relaciones con tipo\|HU-65]] | [[sprints/sprint-3/08-dudas\|P1]] |
| [[sprints/sprint-3/historias/HU-67 Nodo examen con ventana horaria\|HU-67]] | Nodo examen con ventana horaria | Nueva | 5 | Must | — | [[sprints/sprint-3/08-dudas\|P9]] |
| [[sprints/sprint-3/historias/HU-68 Obligatoriedad visible en la lista de nodos\|HU-68]] | Obligatoriedad visible en la lista de nodos | Nueva | 2 | Should | — | — |
| [[sprints/sprint-3/historias/HU-69 Archibaldo - Enter, aspecto de Hernán y destello\|HU-69]] | Archibaldo: Enter, aspecto de Hernán y destello | Nueva | 5 | Could | — | [[sprints/sprint-3/08-dudas\|P11]] |
| [[sprints/sprint-3/historias/HT-21 Seed de demo curado\|HT-21]] | Seed de demo curado | Nueva | 5 | Must | [[sprints/sprint-3/historias/HU-64 Nodos de inicio y fin obligatorios\|HU-64]], [[sprints/sprint-3/historias/HU-65 Relaciones con tipo\|HU-65]], [[sprints/sprint-3/historias/HU-67 Nodo examen con ventana horaria\|HU-67]] | [[sprints/sprint-3/08-dudas\|G7]], [[sprints/sprint-3/08-dudas\|E4]] |
| [[sprints/sprint-3/historias/HT-22 Permisos en vez de roles\|HT-22]] | Permisos en vez de roles | Nueva | 5 | Should | — | [[sprints/sprint-3/08-dudas\|G2]], [[sprints/sprint-3/08-dudas\|G6]] |
| [[sprints/sprint-3/historias/HT-23 Documentación global del micro\|HT-23]] | Documentación global del micro | Nueva | 2 | Should | — | [[sprints/sprint-3/08-dudas\|E7]] |
| [[sprints/sprint-3/historias/HT-24 Datos para el dashboard de G06\|HT-24]] | Datos para el dashboard de G06 | Nueva | 2 | Should | — | [[sprints/sprint-3/08-dudas\|G3]] |

## Consistencia visual con la UI-KIT

| HU | Título | En Taiga | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/HT-25 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|HT-25]] | Subir la UI-KIT a 0.8.0 y cerrar sus TODOs | Nueva | 3 | Must | — | [[sprints/sprint-3/08-dudas\|G13]] |
| [[sprints/sprint-3/historias/HT-26 Controles y botones del roadmap con el kit\|HT-26]] | Controles y botones del roadmap con el kit | Nueva | 3 | Should | [[sprints/sprint-3/historias/HT-25 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|HT-25]] | — |
| [[sprints/sprint-3/historias/HT-27 Colores y espaciado del roadmap con tokens\|HT-27]] | Colores y espaciado del roadmap con tokens | Nueva | 5 | Could | [[sprints/sprint-3/historias/HT-25 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|HT-25]] | — |
| [[sprints/sprint-3/historias/HT-28 Overlays y componentes locales al kit\|HT-28]] | Overlays y componentes locales al kit | Nueva | 5 | Should | [[sprints/sprint-3/historias/HT-25 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|HT-25]] | [[sprints/sprint-3/08-dudas\|E12]] |
| [[sprints/sprint-3/historias/HT-29 Ranking con componentes del kit\|HT-29]] | Ranking con componentes del kit | Nueva | 3 | Should | [[sprints/sprint-3/historias/HT-25 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|HT-25]] | — |
| [[sprints/sprint-3/historias/HU-70 Componente de grafo en la UI-KIT\|HU-70]] | Componente de grafo en la UI-KIT | Nueva | 8 | Must | [[sprints/sprint-3/historias/HT-25 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|HT-25]] | [[sprints/sprint-3/08-dudas\|G13]] |

## Orden sugerido

1. **Semana 1:** toda la deuda del Sprint 2, HT-16 (spike de Neo4j) y HT-25 (UI-KIT 0.8.0). Conseguir las dudas 🔴 de [[sprints/sprint-3/08-dudas|08]] (P1 a P4, G1). En paralelo, lo que no depende de nada: HU-67, HU-68, HU-69, HT-22 (si G06 pasó el catálogo), HT-23 y HT-24.
2. **Semana 2:** HT-17 y HT-18. Front: HT-26 a HT-29, HU-70, HU-62 y HU-63 sobre un mock de `/roadmaps/{id}/graph`. HU-64 y HU-65 sobre el módulo `graph`.
3. **Cierre:** HU-57 a HU-61, HT-19, HT-20, HU-66 y HT-21. Demo con un curso completo de inicio a fin.

Dependencias y riesgos: [[sprints/sprint-3/06-backlog-sprint-3|06-backlog]].

## No entran en el Sprint 3

| Tema | Por qué | Dónde |
|---|---|---|
| Racha | La épica EP-592 no tiene HU ni RF en el PRD. El front muestra un valor fijo | E12 en [[sprints/sprint-3/08-dudas\|08]], DT-13 en [[deuda-tecnica]] (HT-28 lo saca o lo conecta) |
| Estado académico final | Diferido en EP-61 (HU-27/28) | P15 en [[sprints/sprint-3/08-dudas\|08]] |
| Multiple choice con boss fight | No está definido; el contenido es de G04/G09 | P16 en [[sprints/sprint-3/08-dudas\|08]] |
| Ranking por notas | Hoy es solo por XP y no recibimos notas | P14 en [[sprints/sprint-3/08-dudas\|08]] |
| Subsecciones | Depende de qué signifique "anidadas" | P6 en [[sprints/sprint-3/08-dudas\|08]] |

> [!tip] Si los profes responden y alguno entra, crear su nota en `historias/` con el siguiente número libre (HU-71, HT-30…).
