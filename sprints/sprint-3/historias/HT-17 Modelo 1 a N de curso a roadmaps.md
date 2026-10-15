---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-17
estado: Propuesta
responsable: ""
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Must
en_taiga: false
---

# HT-17: Modelo 1 a N de curso a roadmaps

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HT-17 — Modelo 1 a N de curso a roadmaps
------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: que un curso pueda tener varios roadmaps sin romper las rutas ni los datos actuales
*   **Para**: habilitar el pedido de los profes sin una migración a ciegas

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Se quita el UNIQUE de `roadmap.course_cohort_id`. Las rutas `/courses/{id}/...` siguen funcionando contra el roadmap principal del curso mientras el front migra a `/roadmaps/{id}/...`. XP, vidas, nivel y ranking pueden ser por curso o por roadmap: lo configura el profesor (P2). Las secciones también: de Courses o propias (P3). Ver DEC-017.
*   [ ] Validaciones: Un curso sin roadmaps devuelve 404 claro; con varios, las rutas viejas usan el principal.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): Mismas reglas de autorización que hoy.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: P1 confirmó los N roadmaps por curso: el alcance se mantiene (DEC-017).

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Migración que quita el UNIQUE y marca un roadmap principal por curso.
*   [ ] **CA2**: Rutas y DTOs con `roadmap_id`.
*   [ ] **CA3**: Las rutas `/courses/{id}/...` siguen respondiendo igual.
*   [ ] **CA4**: XP, vidas, nivel y ranking por curso o por roadmap, según lo configure el profesor.
*   [ ] **CA5**: Todos los tests existentes pasan.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Modelo 1 a N

**Escenario 1**  

*   **Dado**: un curso con un roadmap
*   **Cuando**: el front llama a `/courses/{id}/progress`
*   **Entonces**: responde igual que antes

**Escenario 2**  

*   **Dado**: un curso con 2 roadmaps
*   **Cuando**: se pide `/roadmaps/{id}/progress` de cada uno
*   **Entonces**: cada uno devuelve su progreso

**Escenario 3**  

*   **Dado**: un curso con 2 roadmaps
*   **Cuando**: se llama a la ruta vieja
*   **Entonces**: responde con el roadmap principal

* * *

Prototipo
---------

*   **Capturas**: No aplica.
*   **URL Figma**: No aplica.
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: Rutas nuevas `/api/roadmap/roadmaps/{roadmapId}/...` en el OpenAPI.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 8 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno nuevo.
*   Módulos afectados: Entidades, repositorios, controllers y DTOs de roadmap, progreso, ranking y nivel.
*   Otros equipos / aprobaciones: Front (migración de rutas).
*   Impacto en datos / migraciones: Migración: quitar UNIQUE, columna `is_primary`.
*   Riesgos y mitigación (opcional): Regresiones en todo el front; mitigación: mantener las rutas viejas hasta que el front migre.

## Tareas

- [ ] T-17.1 Migración y entidades
- [ ] T-17.2 Rutas `/roadmaps/{id}` y compatibilidad
- [ ] T-17.3 Ajuste por roadmap: XP, vidas, nivel y ranking por curso o por roadmap
- [ ] T-17.4 Tests de regresión

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

`roadmap.course_cohort_id` es UNIQUE (V1/V12) y todas las rutas son `/courses/{id}/...`. XP, vidas, nivel y ranking dependen de `student_course`, por curso.

### Depende de

- [[sprints/sprint-3/historias/HT-16 Validar la infra de Neo4j y modelar las relaciones|HT-16]] Validar la infra de Neo4j y modelar las relaciones

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P1]] Cada roadmap es un mapa distinto del mismo curso.
- ✅ [[sprints/sprint-3/08-dudas|P2]] XP, vidas, nivel y ranking: lo configura el profesor (por curso o por roadmap).
- ✅ [[sprints/sprint-3/08-dudas|P3]] Secciones de Courses o propias: lo configura el profesor.
