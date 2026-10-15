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
> Nueva: todavía no está cargada en Taiga.

[G10] — HU-63 — Vista tipo Moodle con la UI-KIT
-----------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: una vista de lista tipo Moodle cómoda y sincronizada con la vista de grafo
*   **Para**: editar el curso en el formato que conozco

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Las dos vistas editan el mismo roadmap.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Reordenar también con teclado, no solo con drag-drop.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: `course-editor-page` refactorizada con componentes del kit.
*   [ ] **CA2**: Un cambio en una vista se ve en la otra sin recargar.
*   [ ] **CA3**: Reordenar secciones y nodos con drag-drop y con teclado.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Vista tipo Moodle

**Escenario 1**  

*   **Dado**: el profesor renombra una sección en la lista
*   **Cuando**: cambia a la vista de grafo
*   **Entonces**: ve el nombre nuevo

**Escenario 2**  

*   **Dado**: una lista de secciones
*   **Cuando**: el profesor arrastra la 3 arriba de la 2
*   **Entonces**: el orden se guarda

**Escenario 3**  

*   **Dado**: un profesor con teclado
*   **Cuando**: reordena con las flechas
*   **Entonces**: el orden se guarda

* * *

Prototipo
---------

*   **Capturas**: `course-editor-page`.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-course-outline`, `generic-disclosure`.
*   **Mock API / Swagger**: Endpoints existentes de secciones y nodos.

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
*   Módulos afectados: `course-editor-page`, `section-reorder-list`.
*   Otros equipos / aprobaciones: Equipo UI-KIT (lista reordenable).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Depende de HT-25 y HT-26.

## Tareas

- [ ] T-63.1 Refactor con el kit
- [ ] T-63.2 Sincronización con la vista de grafo
- [ ] T-63.3 Reordenar accesible

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Existe `course-editor-page` con controles propios.

### Depende de

- [[sprints/sprint-3/historias/HT-25 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs|HT-25]] Subir la UI-KIT a 0.8.0 y cerrar sus TODOs
- [[sprints/sprint-3/historias/HT-26 Controles y botones del roadmap con el kit|HT-26]] Controles y botones del roadmap con el kit

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P1]]
