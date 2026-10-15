---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-63
estado: Propuesta
responsable: ""
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Should
en_taiga: false
---

# HU-63: Vista tipo Moodle con la UI-KIT

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga. Creada el 2026-10-15 (se referenciaba sin nota). Absorbe lo que quedaba de HU-66: ver cada roadmap del curso como mapa desde el editor. Arrastrar nodos y crear relaciones arrastrando quedan en [[sprints/sprint-3/historias/HU-62 Vista de grafo cómoda para el profesor|HU-62]].

[G10] — HU-63 — Vista tipo Moodle con la UI-KIT
-----------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: editar el roadmap en una vista tipo Moodle (lista de secciones y nodos) hecha con la UI-KIT, sincronizada con la vista de grafo, y pasar de una a la otra en cada roadmap del curso
*   **Para**: editar el curso como en Moodle o como un mapa, según me convenga, y tener una alternativa en lista al grafo

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Las dos vistas editan el mismo roadmap: un cambio en una se ve en la otra sin recargar. Cada roadmap del curso es un mapa distinto (P1); el profesor elige el roadmap y la vista. La vista en lista es la alternativa accesible a la vista de grafo de HU-62.
*   [ ] Validaciones: Las mismas que el editor de grafo (HT-18, HU-64): no se guarda un roadmap inválido.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): Fluida con 150 nodos.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño del curso.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Toda la edición se hace con teclado; secciones y nodos con headings y listas que lee un lector de pantalla.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: `course-editor-page` (vista tipo Moodle) usa los componentes del kit: lista de secciones y nodos, acciones de crear, editar, mover y borrar.
*   [ ] **CA2**: Un cambio hecho en la vista Moodle se ve en la vista de grafo y al revés, sin recargar.
*   [ ] **CA3**: El profesor elige un roadmap del curso y cambia entre la vista Moodle y el mapa de ese roadmap.
*   [ ] **CA4**: Toda la edición de la vista Moodle se puede hacer con teclado.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Vista tipo Moodle

**Escenario 1**  

*   **Dado**: un roadmap con 3 secciones
*   **Cuando**: el profesor abre el editor en vista Moodle
*   **Entonces**: ve las secciones y sus nodos en lista, con los componentes del kit

**Escenario 2**  

*   **Dado**: el profesor agrega un nodo en la vista Moodle
*   **Cuando**: cambia a la vista de grafo
*   **Entonces**: el nodo nuevo aparece en el mapa

**Escenario 3**  

*   **Dado**: un curso con 2 roadmaps
*   **Cuando**: el profesor elige el segundo y pasa a la vista de mapa
*   **Entonces**: ve el mapa del segundo roadmap

* * *

Prototipo
---------

*   **Capturas**: Editor del curso en vista Moodle y cambio a mapa.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-button`, `generic-title`, `generic-select`, `generic-modal`.
*   **Mock API / Swagger**: GET /api/roadmap/roadmaps/{roadmapId}/graph (HT-18).

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 8 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: `course-editor-page`, `section-nodes`, store del editor, `course-map-page`.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que las dos vistas se desincronicen; mitigación: un solo store del roadmap para las dos.

## Tareas

- [ ] **T-63.1 Vista Moodle con los componentes del kit** · Front
    - **Qué:** rehacer `course-editor-page` y `section-nodes` con los componentes del kit (lista de secciones y nodos, acciones de crear, editar, mover y borrar), usando lo que deja HT-26.
    - **Listo cuando:** la vista no tiene controles crudos y `ui-review` no marca nada.
- [ ] **T-63.2 Un solo estado para la vista Moodle y la de grafo** · Front
    - **Qué:** las dos vistas leen y escriben el mismo store del roadmap (`/roadmaps/{id}/graph`), así un cambio en una se ve en la otra.
    - **Listo cuando:** agregar, editar o borrar un nodo en una vista se ve en la otra sin recargar. Hay test.
- [ ] **T-63.3 Elegir el roadmap y cambiar entre Moodle y mapa** · Front
    - **Qué:** en el editor, un selector de roadmap del curso y un cambio de vista entre Moodle y el mapa de HU-62 (P1).
    - **Listo cuando:** el profesor ve el mapa de cada roadmap desde el editor.
- [ ] **T-63.4 Editar la vista Moodle con teclado** · Front
    - **Qué:** foco visible, orden de tabulación lógico y acciones accesibles con teclado; es la alternativa en lista al grafo (HU-62).
    - **Listo cuando:** se puede editar un roadmap completo sin mouse.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

`course-editor-page` es una vista tipo Moodle con controles y botones propios. No hay selector de roadmap ni cambio a la vista de mapa.

### Depende de

- [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps|HT-17]] Modelo 1 a N de curso a roadmaps
- [[sprints/sprint-3/historias/HT-26 Adopción de la UI-KIT en el roadmap|HT-26]] Adopción de la UI-KIT en el roadmap
- [[sprints/sprint-3/historias/HU-62 Vista de grafo cómoda para el profesor|HU-62]] Vista de grafo cómoda para el profesor (para CA2 y CA3)

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P1]] Cada roadmap es un mapa distinto del mismo curso.
