---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-57
estado: New
responsable: "Sin asignar"
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Should
en_taiga: true
ref: 8607
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8607
responsables_tareas: ["Baltasar Rodriguez Teruel", "Quinteros Tomás"]
tareas_cerradas: "0/4"
---

# HU-57: Habilitar y gestionar varios roadmaps por curso

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **0/4** · Sprint: **G10 - Sprint 3**
> Cargada en Taiga: [[taiga/historias/HU-57 Habilitar y gestionar varios roadmaps por curso|HU-57]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8607)) · Épica en Taiga: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Baltasar Rodriguez Teruel|Baltasar Rodriguez Teruel]] (3), [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]] (1).

[G10] — HU-57 — Habilitar y gestionar varios roadmaps por curso
---------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: GESTOR / PROFESOR
*   **Quiero**: habilitar varios roadmaps en un curso y crearlos, renombrarlos y archivarlos
*   **Para**: organizar el curso en recorridos distintos

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Flag por curso `multiple_roadmaps_allowed`. Con el flag apagado no se puede crear un segundo roadmap. Archivar es baja lógica y conserva el progreso.
*   [ ] Validaciones: Nombre obligatorio y único dentro del curso.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño del curso.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Pantalla con componentes del kit.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor dueño o el gestor activa varios roadmaps en un curso.
*   [ ] **CA2**: Con el flag apagado, crear un segundo roadmap devuelve 409.
*   [ ] **CA3**: Crear, renombrar y archivar un roadmap.
*   [ ] **CA4**: Archivar no borra el progreso de los alumnos.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Varios roadmaps por curso

**Escenario 1**  

*   **Dado**: un curso con el flag apagado
*   **Cuando**: el profesor intenta crear un segundo roadmap
*   **Entonces**: recibe un error claro

**Escenario 2**  

*   **Dado**: un curso con el flag encendido
*   **Cuando**: el profesor crea «Roadmap práctico»
*   **Entonces**: aparece en la lista del curso

**Escenario 3**  

*   **Dado**: un roadmap con alumnos avanzados
*   **Cuando**: el profesor lo archiva
*   **Entonces**: deja de verse y el progreso se conserva

* * *

Prototipo
---------

*   **Capturas**: Lista de roadmaps del curso.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-table`, `generic-modal`.
*   **Mock API / Swagger**: POST/PATCH /api/roadmap/courses/{courseId}/roadmaps.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 5
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 5 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: Controller y servicio de roadmaps, pantalla del profesor.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Columna `multiple_roadmaps_allowed`.
*   Riesgos y mitigación (opcional): Ninguno abierto (P1 respondida el 2026-10-15).

## Tareas

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **0/4**. Historia en Taiga: [[taiga/historias/HU-57 Habilitar y gestionar varios roadmaps por curso|HU-57]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8607)

- [ ] [#9148](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9148) **T-57.1 Habilitar varios roadmaps en un curso** · Back · New · [[sprints/sprint-3/12-responsables#Baltasar Rodriguez Teruel|Baltasar Rodriguez Teruel]]
    - **Qué:** columna `multiple_roadmaps_allowed` por curso (migración) y acción para que el profesor dueño o el gestor la active. Con el ajuste apagado, crear un segundo roadmap devuelve 409.
    - **Listo cuando:** hay tests con el ajuste prendido y apagado.
- [ ] [#9149](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9149) **T-57.2 Crear, renombrar y archivar roadmaps** · Back · New · [[sprints/sprint-3/12-responsables#Baltasar Rodriguez Teruel|Baltasar Rodriguez Teruel]]
    - **Qué:** nombre obligatorio y único dentro del curso; archivar es baja lógica y conserva el progreso (DEC-005).
    - **Listo cuando:** un roadmap archivado no lo ve el alumno, su progreso sigue en la base y hay tests.
- [ ] [#9150](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9150) **T-57.3 Pantalla de roadmaps del curso para el profesor** · Front · New · [[sprints/sprint-3/12-responsables#Baltasar Rodriguez Teruel|Baltasar Rodriguez Teruel]]
    - **Qué:** lista de roadmaps con crear, renombrar, archivar y el interruptor de «varios roadmaps», con componentes del kit. Acá también va la acción «Clonar» (HU-71) y la asignación a grupos (HU-61).
    - **Listo cuando:** el profesor maneja los roadmaps del curso sin salir de la pantalla.
- [ ] [#9347](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9347) **T-57.4 Wiki, OpenAPI y diagrama de secuencia** · New · [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]]
    - Tarea de documentación agregada en Taiga por el equipo; no estaba en la propuesta.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Un curso tiene un único roadmap.

### Depende de

- [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps|HT-17]] Modelo 1 a N de curso a roadmaps

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P1]] Cada roadmap es un mapa distinto del mismo curso (DEC-017).
