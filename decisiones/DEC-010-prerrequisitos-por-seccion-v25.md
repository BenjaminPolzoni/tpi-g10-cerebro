---
tags: [tpi, g10, decision, grafo, prerrequisitos]
fecha: 2026-10-13
estado: aceptada
reemplaza: ""
---

# DEC-010: Prerrequisitos entre unidades (secciones), migración V25

## Contexto
El desbloqueo se definía solo entre nodos (AND/OR, V5/V7). Los profesores necesitan que una unidad exija completar otras unidades antes de entrar. Ver también el pedido de relaciones configurables entre secciones y nodos del Sprint 3.

## Decisión
`section_prerequisite` (V25) modela una arista entre dos unidades del mismo roadmap. La unidad prerrequisito está **completa** cuando todos sus nodos obligatorios fueron superados. Cada unidad elige cómo combinar sus requisitos con `prerequisite_mode` (`AND` por defecto o `OR`), igual que los nodos. Misma baja lógica que `node_prerequisite`, unicidad `(section_id, prerequisite_section_id)`, y servicios propios (`SectionPrerequisiteEditor`, `SectionPrerequisiteGraphService`, `SectionPrerequisiteService`, `SectionPrerequisiteReader`) para validar ciclos y evaluar. Las unidades existentes quedan en `AND`.

## Alternativas descartadas
- **Reglas de unidad por umbral de XP**: ya descartado en [[decisiones/DEC-011-quitar-umbral-xp-seccion-v8|DEC-011]].
- No hay otras alternativas documentadas; se eligió una tabla propia con las mismas convenciones que `node_prerequisite` (V5).

## Consecuencias
- Positivas: unidades encadenables con la misma semántica AND/OR del editor de nodos.
- Negativas / deuda:
  - Convive con la regla (c) (alcance de visibilidad por comisión de HU-17/36), que limita qué prerrequisitos de nodo son válidos.
  - Entró a `develop` el 2026-10-13; no se verificó cómo lo usa el front.
  - Se solapa con la épica de múltiples roadmaps y relaciones configurables.

## Referencias
- Código / PR / doc: `V25__section_prerequisite.sql`, `6f39416` (2026-10-13), PR #204 (`feature/unit-prerequisites`), `365bf7e` (tests y estilo).
- `tpi-g10-cerebro/sprints/sprint-3/01-estado-actual.md` (HU-13) y `03-requerimientos-profes.md`.
- Relacionadas: [[acuerdos/courses-g01|Courses]], [[decisiones/DEC-014-comisiones-modelo-b-evaluacion-en-roadmap|DEC-014]].
