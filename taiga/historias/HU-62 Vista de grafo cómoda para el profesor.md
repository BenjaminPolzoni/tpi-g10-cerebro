---
tags: [tpi, g10, taiga, hu]
codigo: HU-62
ref: 8612
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8612
---

# HU-62: Vista de grafo cómoda para el profesor

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8612) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Tareas cerradas: **0/6**

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

- [ ] #9165 T-62.1 Vista de grafo con el componente del kit · New · Mateo Delgado Costa
- [ ] #9166 T-62.2 Guardar las posiciones de los nodos · New · Mateo Delgado Costa
- [ ] #9167 T-62.3 Crear y borrar relaciones arrastrando · New · Mateo Delgado Costa
- [ ] #9168 T-62.4 Usar el grafo con teclado · New · Mateo Delgado Costa
- [ ] #9316 T-62.5 Elegir qué roadmap del curso ver como mapa · New · Mateo Delgado Costa
- [ ] #9351 T-62.6 Wiki con capturas y componentes usados · New · Franco Maximiliano Amarilla
