---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-57
estado: Propuesta
responsable: ""
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Should
en_taiga: false
---

# HU-57: Habilitar y gestionar varios roadmaps por curso

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

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
*   [ ] Seguridad (roles, permisos, datos sensibles): GESTOR, ADMIN o PROFESSOR dueño del curso.
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
*   Riesgos y mitigación (opcional): Depende de P1.

## Tareas

- [ ] T-57.1 Flag por curso
- [ ] T-57.2 ABM de roadmaps
- [ ] T-57.3 Pantalla del profesor
- [ ] T-57.4 Tests

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Un curso tiene un único roadmap.

### Depende de

- [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps|HT-17]] Modelo 1 a N de curso a roadmaps

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P1]]
