---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-17
estado: New
responsable: "Sin asignar"
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Must
en_taiga: true
ref: 8600
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8600
responsables_tareas: ["Baltasar Rodriguez Teruel", "Quinteros Tomás"]
tareas_cerradas: "0/4"
---

# HT-17: Modelo 1 a N de curso a roadmaps

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **0/4** · Sprint: **G10 - Sprint 3**
> Cargada en Taiga: [[taiga/historias/HT-17 Modelo 1 a N de curso a roadmaps|HT-17]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8600)) · Épica en Taiga: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Baltasar Rodriguez Teruel|Baltasar Rodriguez Teruel]] (3), [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]] (1).

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

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **0/4**. Historia en Taiga: [[taiga/historias/HT-17 Modelo 1 a N de curso a roadmaps|HT-17]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8600)

- [ ] [#8918](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/8918) **T-17.1 Permitir varios roadmaps por curso en la base** · Back · New · [[sprints/sprint-3/12-responsables#Baltasar Rodriguez Teruel|Baltasar Rodriguez Teruel]]
    - **Qué:** migración Flyway (la siguiente a V26) que quita el UNIQUE de `roadmap.course_cohort_id` y agrega `is_primary`; el roadmap actual de cada curso queda como principal. Ajustar entidad y repositorio para buscar por id de roadmap y por «principal del curso».
    - **Listo cuando:** la migración corre sobre una base con datos sin perder nada y cada curso tiene exactamente un roadmap principal.
- [ ] [#8924](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/8924) **T-17.2 Rutas por roadmap sin romper las rutas por curso** · Back · New · [[sprints/sprint-3/12-responsables#Baltasar Rodriguez Teruel|Baltasar Rodriguez Teruel]]
    - **Qué:** exponer `/roadmaps/{roadmapId}/...` y sumar `roadmap_id` a los DTOs. Las rutas actuales `/courses/{courseId}/...` siguen funcionando y resuelven el roadmap principal.
    - **Dónde:** `GraphController`, `NodeController`, `ProgressController`, `LevelController`, `RankingController` y sus DTOs.
    - **Listo cuando:** el front actual anda sin cambios, las rutas nuevas responden lo mismo para el roadmap principal y toda la suite existente pasa.
- [ ] [#8925](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/8925) **T-17.3 Elegir por roadmap si XP, vidas, nivel y ranking son del curso o del roadmap** · Back · New · [[sprints/sprint-3/12-responsables#Baltasar Rodriguez Teruel|Baltasar Rodriguez Teruel]]
    - **Qué:** guardar en cada roadmap si esos datos se comparten con todo el curso o son propios (P2, DEC-017), y hacer que el ledger de XP, `LevelService` y `RankingService` respeten esa elección.
    - **Listo cuando:** con dos roadmaps en un curso, en modo «por curso» el XP se acumula en un solo total y en modo «por roadmap» cada uno tiene el suyo. Hay tests de los dos modos.
- [ ] [#9335](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9335) **T-17.4 Wiki, OpenAPI y diagrama de secuencia** · New · [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]]
    - Tarea de documentación agregada en Taiga por el equipo; no estaba en la propuesta.

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
