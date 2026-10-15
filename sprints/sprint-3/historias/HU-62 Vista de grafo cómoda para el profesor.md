---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-62
estado: Propuesta
responsable: ""
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Must
en_taiga: false
---

# HU-62: Vista de grafo cómoda para el profesor

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga. Desde el 2026-10-15 es la única dueña de guardar posiciones y crear relaciones arrastrando (HU-66 se eliminó) y de elegir qué roadmap del curso se ve como mapa (antes en HU-63, descartada).

[G10] — HU-62 — Vista de grafo cómoda para el profesor
------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: ver y editar el roadmap como un grafo cómodo, con acomodo automático y posiciones guardadas
*   **Para**: entender y modificar las relaciones del curso de un vistazo

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Las posiciones se guardan (hoy `moveNode` devuelve 501). Crear y borrar aristas arrastrando.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): Fluido con 150 nodos.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Navegación con teclado entre nodos, foco visible y, como alternativa en lista, la lista de nodos de cada sección en «Contenido del curso» (`roadmap-section-nodes`).
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Acomodo automático (`elkjs`), zoom, pan y minimapa.
*   [ ] **CA2**: Las posiciones se guardan y se recuperan.
*   [ ] **CA3**: Crear y borrar aristas arrastrando, eligiendo el tipo de relación (HU-65).
*   [ ] **CA4**: Usa el componente de grafo del kit (HT-34).
*   [ ] **CA5**: Se puede usar con teclado.
*   [ ] **CA6**: En un curso con varios roadmaps, el profesor elige cuál ver como mapa (cada roadmap es un mapa distinto, P1).

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Vista de grafo

**Escenario 1**  

*   **Dado**: un roadmap nuevo
*   **Cuando**: el profesor abre la vista de grafo
*   **Entonces**: los nodos aparecen acomodados automáticamente

**Escenario 2**  

*   **Dado**: el profesor mueve un nodo
*   **Cuando**: recarga la página
*   **Entonces**: el nodo sigue donde lo dejó

**Escenario 3**  

*   **Dado**: dos nodos
*   **Cuando**: el profesor arrastra de uno al otro
*   **Entonces**: se crea la relación

**Escenario 4**  

*   **Dado**: un curso con 2 roadmaps
*   **Cuando**: el profesor elige el segundo en el mapa
*   **Entonces**: ve el mapa del segundo roadmap

* * *

Prototipo
---------

*   **Capturas**: Vista de grafo del editor.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-node-graph` (HT-34).
*   **Mock API / Swagger**: GET /api/roadmap/roadmaps/{roadmapId}/graph y PATCH de posiciones.

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

*   Servicios involucrados: Ninguno.
*   Módulos afectados: `course-map-page`, endpoint `/graph`.
*   Otros equipos / aprobaciones: Equipo UI-KIT (HT-34).
*   Impacto en datos / migraciones: Posiciones en Neo4j.
*   Riesgos y mitigación (opcional): Depende del componente de grafo de HT-34; mitigación: arrancar sobre la librería directa y migrar al kit.

## Tareas

- [ ] **T-62.1 Vista de grafo con el componente del kit** · Front
    - **Qué:** `course-map-page` usa `generic-node-graph` (HT-34) con acomodo automático (`elkjs`), zoom, pan y minimapa. Si el componente todavía no está, arrancar con la librería directa y cambiar después.
    - **Listo cuando:** se mueve fluido con 150 nodos.
- [ ] **T-62.2 Guardar las posiciones de los nodos** · Back + Front
    - **Qué:** endpoint para guardar la posición de cada nodo en el grafo; el front deja de dar error al mover nodos (`moveNode` del store).
    - **Listo cuando:** se mueve un nodo, se recarga la página y queda donde se dejó.
- [ ] **T-62.3 Crear y borrar relaciones arrastrando** · Front
    - **Qué:** arrastrar de un nodo a otro crea la relación (eligiendo su tipo, HU-65); se borra desde la arista.
    - **Listo cuando:** el profesor arma las relaciones de una unidad sin usar formularios.
- [ ] **T-62.4 Usar el grafo con teclado** · Front
    - **Qué:** moverse entre nodos con teclado, foco visible y un enlace a la lista de nodos de la sección en «Contenido del curso» como alternativa.
    - **Listo cuando:** se puede revisar y editar el grafo sin mouse.
- [ ] **T-62.5 Elegir qué roadmap del curso ver como mapa** · Front
    - **Qué:** en `course-editor-page` (hoy solo el mapa), un selector con los roadmaps del curso (HU-57) que cambia el mapa que se muestra (P1).
    - **Listo cuando:** en un curso con dos roadmaps, el profesor ve el mapa de cada uno.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

La vista de grafo existe pero es incómoda. Desde el 13/10 (`31d31510`) `course-editor-page` solo muestra el mapa: la edición en lista está en «Contenido del curso» de Courses. `moveNode` devuelve 501: las posiciones no se guardan.

### Depende de

- [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps|HT-17]] Modelo 1 a N de curso a roadmaps
- [[sprints/sprint-3/historias/HT-34 Componente de grafo en la UI-KIT|HT-34]] Componente de grafo en la UI-KIT
- [[sprints/sprint-3/historias/HU-65 Relaciones con tipo|HU-65]] Relaciones con tipo (para elegir el tipo al crear una arista, T-62.3)

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|G13]] El componente de grafo es nuestro (G10).
