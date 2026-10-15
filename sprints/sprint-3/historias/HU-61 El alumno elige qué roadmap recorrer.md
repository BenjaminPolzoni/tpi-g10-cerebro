---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-61
estado: Propuesta
responsable: ""
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Should
en_taiga: false
---

# HU-61: El alumno elige qué roadmap recorrer

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HU-61 — El alumno elige qué roadmap recorrer
----------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: elegir qué roadmap del curso recorrer y ver mi progreso en cada uno
*   **Para**: seguir el recorrido que me corresponde

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Qué roadmaps ve el alumno lo configura el profesor: todos o por comisión (P5). XP, nivel y ranking por curso o por roadmap, según lo configure el profesor (P2). Ver DEC-017.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): Solo roadmaps no archivados del curso donde está matriculado.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Selector accesible.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Si el curso tiene varios roadmaps visibles, el alumno elige uno.
*   [ ] **CA2**: El progreso de cada roadmap se ve por separado.
*   [ ] **CA3**: XP, nivel y ranking se muestran por curso o por roadmap, según la configuración del profesor.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Elegir roadmap

**Escenario 1**  

*   **Dado**: un curso con 2 roadmaps visibles
*   **Cuando**: el alumno abre el curso
*   **Entonces**: elige cuál recorrer

**Escenario 2**  

*   **Dado**: un alumno con avance en ambos
*   **Cuando**: cambia de roadmap
*   **Entonces**: ve el progreso de cada uno

**Escenario 3**  

*   **Dado**: un roadmap archivado
*   **Cuando**: el alumno abre el curso
*   **Entonces**: no aparece

* * *

Prototipo
---------

*   **Capturas**: Selector de roadmap del alumno.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-segmented` o `generic-select`.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/roadmaps.

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
*   Módulos afectados: Roadmap del alumno, `RoadmapStore`.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Dos ajustes que configura el profesor (P2 y P5); hay que probar las combinaciones.

## Tareas

- [ ] T-61.1 Endpoint de roadmaps visibles
- [ ] T-61.2 Selector en el front
- [ ] T-61.3 Tests

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

El alumno ve un único roadmap por curso.

### Depende de

- [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps|HT-17]] Modelo 1 a N de curso a roadmaps

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P1]] Cada roadmap es un mapa distinto del mismo curso.
- ✅ [[sprints/sprint-3/08-dudas|P2]] XP, vidas, nivel y ranking: lo configura el profesor (por curso o por roadmap).
- ✅ [[sprints/sprint-3/08-dudas|P5]] Lo configura el profesor: todos los roadmaps o por comisión.
