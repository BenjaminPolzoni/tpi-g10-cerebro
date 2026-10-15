---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-66
estado: Eliminada
responsable: ""
epica: "Correcciones de los profes"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Should
en_taiga: false
---

# HU-66: Editor con arrastre y el curso como mapa

> [!danger] Fusionada el 2026-10-15 (revisión de HU): arrastrar nodos y crear relaciones arrastrando ya estaban en HU-62 (CA2 y CA3); ver cada roadmap como mapa pasó a HU-63 (CA3). **Borrar esta nota.**

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Correcciones de los profes|Correcciones de los profes]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HU-66 — Editor con arrastre y el curso como mapa
--------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: arrastrar nodos, crear relaciones arrastrando y ver el curso como un mapa
*   **Para**: editar el curso de forma visual, como en Google Maps

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Las posiciones se guardan. Al crear una relación se elige su tipo (HU-65). Cada roadmap es un mapa distinto del mismo curso (P1).
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Alternativa con teclado para mover y relacionar.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Arrastrar nodos y guardar su posición.
*   [ ] **CA2**: Crear una relación arrastrando y eligiendo su tipo.
*   [ ] **CA3**: El editor muestra cada roadmap del curso como un mapa.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Editor como mapa

**Escenario 1**  

*   **Dado**: el editor abierto
*   **Cuando**: el profesor arrastra un nodo
*   **Entonces**: la posición se guarda

**Escenario 2**  

*   **Dado**: dos nodos
*   **Cuando**: arrastra de uno al otro y elige `REQUIRES`
*   **Entonces**: se crea la relación

**Escenario 3**  

*   **Dado**: un curso completo
*   **Cuando**: el profesor abre el editor
*   **Entonces**: lo ve como un mapa navegable

* * *

Prototipo
---------

*   **Capturas**: Editor del curso.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-node-graph`.
*   **Mock API / Swagger**: Endpoints de HU-62 y HU-65.

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
*   Módulos afectados: `course-editor-page`, vista de grafo.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Depende de HU-62 y HU-65.

## Tareas

- [ ] **T-66.1 Arrastrar nodos en el editor y que queden ahí** · Front
    - **Qué:** arrastre en `course-editor-page` usando el guardado de posiciones de HU-62.
    - **Listo cuando:** la posición se mantiene al recargar.
- [ ] **T-66.2 Crear una relación arrastrando y elegir su tipo** · Front
    - **Qué:** arrastrar de un nodo a otro abre la elección del tipo (HU-65).
    - **Listo cuando:** la relación queda creada con el tipo elegido.
- [ ] **T-66.3 Ver cada roadmap del curso como un mapa** · Front
    - **Qué:** en el editor, cambiar entre la vista tipo Moodle y el mapa de cada roadmap del curso (P1).
    - **Listo cuando:** el profesor ve el mapa de cada roadmap desde el editor.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

`course-editor-page` es una vista tipo Moodle. Las posiciones no se guardan.

### Depende de

- [[sprints/sprint-3/historias/HU-62 Vista de grafo cómoda para el profesor|HU-62]] Vista de grafo cómoda para el profesor
- [[sprints/sprint-3/historias/HU-65 Relaciones con tipo|HU-65]] Relaciones con tipo

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P1]] Cada roadmap es un mapa distinto del mismo curso.
