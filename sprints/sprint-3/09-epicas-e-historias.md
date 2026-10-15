---
tags: [tpi, g10, sprint-3, epicas, historias]
fecha: 2026-10-15
estado: borrador
---

# 09 — Épicas e historias del Sprint 3

> [!info] Qué es esto
> Todas las historias y correcciones propuestas para el Sprint 3, organizadas como en Taiga: **épica → historia → criterios de aceptación**.
> - `epicas/`: una nota por épica, con objetivo, criterios a nivel épica y sus historias.
> - `historias/`: una nota por historia (HU, HT, spike o bug), con criterios de aceptación, dependencias, dudas que la frenan y deuda técnica que cierra.
> - **Todavía no están en Taiga.** Son la base para cargarlas (B12). Al cargar una, completar `taiga` y `responsable` en sus propiedades.
> - No confundir con `taiga/` (raíz del cerebro), que se genera desde Taiga y no se edita.

**IDs:** `B` = deuda del Sprint 2 · `M` = múltiples roadmaps y grafo · `C` = correcciones de los profes · `U` = UI-KIT.
**Estado de cada nota:** Propuesta → Cargada en Taiga → En curso → Hecha (propiedad `estado`).
**Formato:** cada nota sigue la plantilla de Taiga del equipo (Como/Quiero/Para, notas, CA, BDD, prototipo, estimación, dependencias y tareas), lista para copiar.

## Épicas

| Épica | Objetivo | Historias | Puntos |
|---|---|---|---|
| [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2\|EP-S3-0]] Deuda del Sprint 2 | Cerrar lo que figura Done en Taiga y no lo está, y la deuda que rompe la demo. | 12 | 49 pts |
| [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable\|EP-S3-1]] Múltiples roadmaps por curso y grafo configurable | Que un curso pueda tener uno o más roadmaps, con secciones y nodos relacionados por reglas configurables, guardados en Neo4j y editables desde dos vistas (Moodle y grafo). | 12 | 68 pts |
| [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes\|EP-S3-2]] Correcciones de los profes | Resolver las correcciones que los profes marcaron como nuestras (2026-10-14). | 11 | 52 pts |
| [[sprints/sprint-3/epicas/EP-S3-3 Consistencia visual con la UI-KIT\|EP-S3-3]] Consistencia visual con la UI-KIT | Que las pantallas del roadmap y del ranking usen la UI-KIT (`@2026-p4-fe/ui`) en vez de controles y colores propios, y aportar al kit el componente de grafo. | 6 | 27 pts |

**Total:** 41 historias, 196 pts (Fibonacci).

## EP-S3-0: Deuda del Sprint 2

| ID | Tipo | Título | Capa | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/B01 Cerrar o mergear las ramas colgadas del back\|B01]] | HT | Cerrar o mergear las ramas colgadas del back | Back | 2 | Must | — | [[sprints/sprint-3/08-dudas\|E5]] |
| [[sprints/sprint-3/historias/B02 Encender los flags en los entornos\|B02]] | HT | Encender los flags en los entornos | Infra | 2 | Must | — | [[sprints/sprint-3/08-dudas\|E6]] |
| [[sprints/sprint-3/historias/B03 Sacar los IDs de mock del front\|B03]] | HT | Sacar los IDs de mock del front | Front | 3 | Must | — | — |
| [[sprints/sprint-3/historias/B04 Pre-chequeo de elegibilidad para el alumno (HU-48)\|B04]] | HU | Pre-chequeo de elegibilidad para el alumno (HU-48) | Back | 3 | Must | — | — |
| [[sprints/sprint-3/historias/B05 Completar insignias (HU-20 y HU-21)\|B05]] | HU | Completar insignias (HU-20 y HU-21) | Back + Front | 5 | Should | — | [[sprints/sprint-3/08-dudas\|E2]] |
| [[sprints/sprint-3/historias/B06 Gate con origen no disponible y dato stale (HU-15 y HU-16)\|B06]] | HU | Gate con origen no disponible y dato stale (HU-15 y HU-16) | Back | 5 | Should | — | [[sprints/sprint-3/08-dudas\|E9]] |
| [[sprints/sprint-3/historias/B07 Validar el ícono según el tipo de nodo (HU-43)\|B07]] | HU | Validar el ícono según el tipo de nodo (HU-43) | Back | 1 | Could | — | — |
| [[sprints/sprint-3/historias/B08 Templo de materiales (HU-46)\|B08]] | HU | Templo de materiales (HU-46) | Front | 5 | Should | — | [[sprints/sprint-3/08-dudas\|P13]] |
| [[sprints/sprint-3/historias/B09 Comisiones en el front (HU-44 y HU-45)\|B09]] | HU | Comisiones en el front (HU-44 y HU-45) | Front (+ Back) | 8 | Must | [[sprints/sprint-3/historias/B02 Encender los flags en los entornos\|B02]] | [[sprints/sprint-3/08-dudas\|P5]] |
| [[sprints/sprint-3/historias/B10 Restricciones de Courses (HU-49)\|B10]] | HU | Restricciones de Courses (HU-49) | Back + Front | 8 | Should | [[sprints/sprint-3/historias/C04 Nodo examen con ventana horaria\|C04]] | [[sprints/sprint-3/08-dudas\|P9]], [[sprints/sprint-3/08-dudas\|G4]] |
| [[sprints/sprint-3/historias/B11 Reintentos y edición de nodos (HU-01 y HU-41)\|B11]] | HU | Reintentos y edición de nodos (HU-01 y HU-41) | Back | 5 | Must | — | — |
| [[sprints/sprint-3/historias/B12 Poner Taiga al día\|B12]] | HT | Poner Taiga al día | Taiga | 2 | Must | — | [[sprints/sprint-3/08-dudas\|E10]], [[sprints/sprint-3/08-dudas\|E11]] |

## EP-S3-1: Múltiples roadmaps por curso y grafo configurable

| ID | Tipo | Título | Capa | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/M01 Validar la infra de Neo4j y modelar las relaciones\|M01]] | Spike | Validar la infra de Neo4j y modelar las relaciones | Back + Infra | 3 | Must | — | [[sprints/sprint-3/08-dudas\|G1]], [[sprints/sprint-3/08-dudas\|P1]], [[sprints/sprint-3/08-dudas\|P4]] |
| [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps\|M02]] | HT | Modelo 1 a N de curso a roadmaps | Back | 8 | Must | [[sprints/sprint-3/historias/M01 Validar la infra de Neo4j y modelar las relaciones\|M01]] | [[sprints/sprint-3/08-dudas\|P1]], [[sprints/sprint-3/08-dudas\|P2]], [[sprints/sprint-3/08-dudas\|P3]] |
| [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial\|M03]] | HT | Módulo graph en Neo4j y migración inicial | Back | 8 | Must | [[sprints/sprint-3/historias/M01 Validar la infra de Neo4j y modelar las relaciones\|M01]] | [[sprints/sprint-3/08-dudas\|P1]], [[sprints/sprint-3/08-dudas\|P4]], [[sprints/sprint-3/08-dudas\|P8]] |
| [[sprints/sprint-3/historias/M04 Habilitar y gestionar varios roadmaps por curso\|M04]] | HU | Habilitar y gestionar varios roadmaps por curso | Back + Front | 5 | Should | [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps\|M02]] | [[sprints/sprint-3/08-dudas\|P1]] |
| [[sprints/sprint-3/historias/M05 Dependencias entre secciones\|M05]] | HU | Dependencias entre secciones | Back + Front | 5 | Must | [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps\|M02]], [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial\|M03]] | [[sprints/sprint-3/08-dudas\|P6]] |
| [[sprints/sprint-3/historias/M06 Dependencias entre nodos con reglas combinadas\|M06]] | HU | Dependencias entre nodos con reglas combinadas | Back + Front | 5 | Should | [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps\|M02]], [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial\|M03]] | [[sprints/sprint-3/08-dudas\|P7]] |
| [[sprints/sprint-3/historias/M07 Propiedades personalizadas en nodos y secciones\|M07]] | HU | Propiedades personalizadas en nodos y secciones | Back + Front | 3 | Could | [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial\|M03]] | [[sprints/sprint-3/08-dudas\|P8]] |
| [[sprints/sprint-3/historias/M08 El alumno elige qué roadmap recorrer\|M08]] | HU | El alumno elige qué roadmap recorrer | Back + Front | 5 | Should | [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps\|M02]] | [[sprints/sprint-3/08-dudas\|P1]], [[sprints/sprint-3/08-dudas\|P2]], [[sprints/sprint-3/08-dudas\|P5]] |
| [[sprints/sprint-3/historias/M09 Vista de grafo cómoda para el profesor\|M09]] | HU | Vista de grafo cómoda para el profesor | Front (+ Back) | 8 | Must | [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps\|M02]], [[sprints/sprint-3/historias/U06 Componente de grafo en la UI-KIT\|U06]] | [[sprints/sprint-3/08-dudas\|G13]] |
| [[sprints/sprint-3/historias/M10 Vista tipo Moodle con la UI-KIT\|M10]] | HU | Vista tipo Moodle con la UI-KIT | Front | 8 | Should | [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]], [[sprints/sprint-3/historias/U02 Controles y botones del roadmap con el kit\|U02]] | [[sprints/sprint-3/08-dudas\|P1]] |
| [[sprints/sprint-3/historias/M11 Contratos con Courses y el Motor para el modelo 1 a N\|M11]] | HT | Contratos con Courses y el Motor para el modelo 1 a N | Back | 5 | Must | [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps\|M02]] | [[sprints/sprint-3/08-dudas\|P3]], [[sprints/sprint-3/08-dudas\|G4]], [[sprints/sprint-3/08-dudas\|G8]] |
| [[sprints/sprint-3/historias/M12 Gate y progreso con reglas combinadas y XP mínimo\|M12]] | HT | Gate y progreso con reglas combinadas y XP mínimo | Back | 5 | Must | [[sprints/sprint-3/historias/M05 Dependencias entre secciones\|M05]], [[sprints/sprint-3/historias/M06 Dependencias entre nodos con reglas combinadas\|M06]] | [[sprints/sprint-3/08-dudas\|P7]] |

## EP-S3-2: Correcciones de los profes

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

## EP-S3-3: Consistencia visual con la UI-KIT

| ID | Tipo | Título | Capa | Pts | Prioridad | Depende de | Dudas |
|---|---|---|---|---|---|---|---|
| [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | HT | Subir la UI-KIT a 0.8.0 y cerrar sus TODOs | Front | 3 | Must | — | [[sprints/sprint-3/08-dudas\|G13]] |
| [[sprints/sprint-3/historias/U02 Controles y botones del roadmap con el kit\|U02]] | HT | Controles y botones del roadmap con el kit | Front | 3 | Should | [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | — |
| [[sprints/sprint-3/historias/U03 Colores y espaciado del roadmap con tokens\|U03]] | HT | Colores y espaciado del roadmap con tokens | Front | 5 | Could | [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | — |
| [[sprints/sprint-3/historias/U04 Overlays y componentes locales al kit\|U04]] | HT | Overlays y componentes locales al kit | Front | 5 | Should | [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | [[sprints/sprint-3/08-dudas\|E12]] |
| [[sprints/sprint-3/historias/U05 Ranking con componentes del kit\|U05]] | HT | Ranking con componentes del kit | Front | 3 | Should | [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | — |
| [[sprints/sprint-3/historias/U06 Componente de grafo en la UI-KIT\|U06]] | HU | Componente de grafo en la UI-KIT | UI-KIT | 8 | Must | [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs\|U01]] | [[sprints/sprint-3/08-dudas\|G13]] |

## Orden sugerido

1. **Semana 1:** EP-S3-0 completa (B01 a B12), M01 (spike) y U01. Conseguir las dudas 🔴 de [[sprints/sprint-3/08-dudas|08]] (P1 a P4, G1). En paralelo, lo que no depende de nada: C04, C05, C06, C07, C09 (si G06 pasó el catálogo), C10 y C11.
2. **Semana 2:** M02 y M03. Front: U02 a U06 y M09/M10 sobre un mock de `/roadmaps/{id}/graph`. C01 y C02 sobre el módulo `graph`.
3. **Cierre:** M04 a M08, M11, M12, C03 y C08. Demo con un curso completo de inicio a fin.

Detalle de dependencias y riesgos: [[sprints/sprint-3/06-backlog-sprint-3|06-backlog]].

## No entran en el Sprint 3

| Tema | Por qué | Dónde |
|---|---|---|
| Racha | La épica EP-592 no tiene HU ni RF en el PRD. El front muestra un valor fijo | E12 en [[sprints/sprint-3/08-dudas\|08]], DT-13 en [[deuda-tecnica]] (U04 lo saca o lo conecta) |
| Estado académico final | Diferido en EP-61 (HU-27/28) | P15 en [[sprints/sprint-3/08-dudas\|08]] |
| Multiple choice con boss fight | No está definido; el contenido es de G04/G09 | P16 en [[sprints/sprint-3/08-dudas\|08]] |
| Ranking por notas | Hoy es solo por XP y no recibimos notas | P14 en [[sprints/sprint-3/08-dudas\|08]] |
| Subsecciones | Depende de qué signifique "anidadas" | P6 en [[sprints/sprint-3/08-dudas\|08]] |

> [!tip] Si los profes responden y alguno entra, crear su nota en `historias/` con el siguiente ID de la épica que corresponda.
