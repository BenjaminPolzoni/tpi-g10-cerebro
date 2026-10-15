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
> Nueva: todavía no está cargada en Taiga.

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
*   [ ] Accesibilidad (WCAG/teclado/lectores): Navegación con teclado entre nodos, foco visible y alternativa en lista (HU-63).
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Acomodo automático (`elkjs`), zoom, pan y minimapa.
*   [ ] **CA2**: Las posiciones se guardan y se recuperan.
*   [ ] **CA3**: Crear y borrar aristas arrastrando.
*   [ ] **CA4**: Usa el componente de grafo del kit (HT-26).
*   [ ] **CA5**: Se puede usar con teclado.

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

* * *

Prototipo
---------

*   **Capturas**: Vista de grafo del editor.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-node-graph` (HT-26).
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
*   Otros equipos / aprobaciones: Equipo UI-KIT (HT-26).
*   Impacto en datos / migraciones: Posiciones en Neo4j.
*   Riesgos y mitigación (opcional): Depende del componente de grafo de HT-26; mitigación: arrancar sobre la librería directa y migrar al kit.

## Tareas

- [ ] T-62.1 Integrar el componente de grafo
- [ ] T-62.2 Guardar posiciones (reemplazar el 501)
- [ ] T-62.3 Aristas arrastrando
- [ ] T-62.4 Teclado y accesibilidad

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

La vista de grafo existe pero es incómoda. `moveNode` devuelve 501: las posiciones no se guardan.

### Depende de

- [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps|HT-17]] Modelo 1 a N de curso a roadmaps
- [[sprints/sprint-3/historias/HT-26 Adopción de la UI-KIT en el roadmap|HT-26]] Adopción de la UI-KIT en el roadmap (componente de grafo)

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|G13]] El componente de grafo es nuestro (G10).
