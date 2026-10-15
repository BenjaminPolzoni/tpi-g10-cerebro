---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-72
estado: New
responsable: "Sin asignar"
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Should
en_taiga: true
ref: 8620
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8620
responsables_tareas: ["Benjamin Polzoni", "Quinteros Tomás"]
tareas_cerradas: "0/5"
---

# HU-72: Cerrar el curso con el estado académico final

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **0/5** · Sprint: **G10 - Sprint 3**
> Cargada en Taiga: [[taiga/historias/HU-72 Cerrar el curso con el estado académico final|HU-72]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8620)) · Épica en Taiga: [[epicas/EP-8632 Deuda del Sprint 2|EP-8632]] · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Benjamin Polzoni|Benjamin Polzoni]] (4), [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]] (1). Retoma el cierre académico que [[taiga/epicas/EP-61 Ranking y cierre académico|EP-61]] había diferido (HU-27/28). Entra en el Sprint 3 por P15 (2026-10-15). Pasa a Should el 2026-10-15 mientras G14 (dónde se guarda el estado final) no tenga respuesta.

[G10] — HU-72 — Cerrar el curso con el estado académico final
-------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: ver los candidatos a promoción y a pérdida de regularidad con sus condiciones, confirmar el estado final de cada alumno al cerrar el curso y exportar el resumen
*   **Para**: cerrar la cursada con los datos del roadmap y no a mano

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El estado final lo confirma manualmente el profesor: promocionado, regular, no regular o abandonó (`PROMOTED`, `REGULAR`, `NOT_REGULAR`, `DROPPED_OUT`). Roadmap le muestra los candidatos P90/P10 con sus condiciones (RF-RNK-10). El estado final es de Courses (`finalAcademicStatus`); Roadmap aporta XP, posición, insignias y candidatos. Resumen exportable por alumno: legajo, nombre, estado final, XP e insignias (RF-RNK-13).
*   [ ] Validaciones: Los cortes P90/P10 solo se calculan con 10 o más inscriptos (RF-RNK-09). No se confirma un estado fuera de los cuatro valores.
*   [ ] Datos obligatorios: Estado final de cada alumno matriculado antes de cerrar.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño del curso. El alumno solo ve su propio estado final. El resumen tiene legajos: no se expone a alumnos.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Tabla de candidatos con `generic-table`, estados con texto y no solo color.
*   [ ] Otros: Si el ranking es por roadmap (P2), definir con qué ranking se calculan los candidatos de un curso con varios roadmaps.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor ve los candidatos P90/P10 con las condiciones de cada uno.
*   [ ] **CA2**: El profesor confirma el estado final de cada alumno y queda guardado donde se acuerde con G01 (G14).
*   [ ] **CA3**: El profesor exporta el resumen por alumno: legajo, nombre, estado final, XP e insignias.
*   [ ] **CA4**: Con menos de 10 inscriptos no se muestran cortes P90/P10.
*   [ ] **CA5**: Después del cierre, el roadmap y el ranking quedan en solo lectura.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Cierre de curso

**Escenario 1**  

*   **Dado**: un curso de 24 alumnos al final de la cursada
*   **Cuando**: el profesor abre el cierre
*   **Entonces**: ve los candidatos P90 y P10 con sus condiciones

**Escenario 2**  

*   **Dado**: el profesor confirmó el estado final de todos los alumnos
*   **Cuando**: exporta el resumen
*   **Entonces**: obtiene una fila por alumno con legajo, nombre, estado final, XP e insignias

**Escenario 3**  

*   **Dado**: un curso de 7 alumnos
*   **Cuando**: el profesor abre el cierre
*   **Entonces**: ve a todos los alumnos sin zonas P90/P10

* * *

Prototipo
---------

*   **Capturas**: Pantalla de cierre del curso del profesor.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-table`, `generic-select`, `generic-badge`, `generic-button`.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/closure/candidates y GET /api/roadmap/courses/{courseId}/closure/summary (CSV).

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

*   Servicios involucrados: Courses (estado final y archivado), Users (legajo y nombre), Accounting (vidas perdidas, para las condiciones de promoción).
*   Módulos afectados: Ranking (percentiles y cascada), insignias, pantalla del profesor.
*   Otros equipos / aprobaciones: G01 (bloqueante: hoy nadie escribe `finalAcademicStatus`), G07.
*   Impacto en datos / migraciones: Si Courses guarda el estado final, sin migración. Si no, tabla de estado final en Roadmap (como preveía EP-61).
*   Riesgos y mitigación (opcional): Que G01 no exponga cómo guardar el estado; mitigación: proponer el endpoint por escrito en la semana 1 (G14).

## Tareas

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **0/5**. Historia en Taiga: [[taiga/historias/HU-72 Cerrar el curso con el estado académico final|HU-72]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8620)

- [ ] [#9222](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9222) **T-72.1 Acordar con Courses dónde se guarda el estado final** · Coordinación · New · [[sprints/sprint-3/12-responsables#Benjamin Polzoni|Benjamin Polzoni]]
    - **Qué:** resolver G14 con G01: el estado final (`finalAcademicStatus`) lo guarda Courses (endpoint o evento) o Roadmap.
    - **Listo cuando:** el acuerdo está en `acuerdos/courses-g01`.
- [ ] [#9223](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9223) **T-72.2 Calcular los candidatos a promoción y a pérdida de regularidad** · Back · New · [[sprints/sprint-3/12-responsables#Benjamin Polzoni|Benjamin Polzoni]]
    - **Qué:** endpoint de candidatos P90/P10 con sus condiciones (vidas perdidas, obligatorios aprobados), usando las zonas que ya calcula `RankingService`. Solo con 10 o más inscriptos.
    - **Listo cuando:** un curso de 24 da candidatos y uno de 7 no. Hay tests.
- [ ] [#9225](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9225) **T-72.3 Pantalla de cierre del curso** · Front · New · [[sprints/sprint-3/12-responsables#Benjamin Polzoni|Benjamin Polzoni]]
    - **Qué:** tabla con los candidatos y sus condiciones, un selector de estado final por alumno (promocionado, regular, no regular, abandonó) y confirmar. Después, el roadmap y el ranking quedan en solo lectura.
    - **Listo cuando:** el profesor cierra un curso de punta a punta.
- [ ] [#9226](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9226) **T-72.4 Exportar el resumen por alumno** · Back + Front · New · [[sprints/sprint-3/12-responsables#Benjamin Polzoni|Benjamin Polzoni]]
    - **Qué:** archivo con legajo, nombre, estado final, XP e insignias de cada alumno (el legajo sale de Users o Courses).
    - **Listo cuando:** el archivo se descarga con una fila por alumno.
- [ ] [#9355](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9355) **T-72.5 Wiki, OpenAPI y diagrama de secuencia** · New · [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]]
    - Tarea de documentación agregada en Taiga por el equipo; no estaba en la propuesta.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

El ranking ya calcula las zonas P90/P10 y la cascada de desempate. Al recibir `COURSE_COHORT_ARCHIVED`, Roadmap congela el roadmap y el ranking. El flujo de cierre se había postergado (`courses.md` §7.6): `finalAcademicStatus` aparece en el DTO de Courses pero no hay endpoint que lo escriba.

### Depende de

- [[sprints/sprint-3/historias/HU-45 Ranking de la cohorte y avance por comisión|HU-45]] Ranking de la cohorte y avance por comisión

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P15]] El estado académico final entra en el Sprint 3.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G14]] ¿Dónde se guarda el estado final que confirma el profesor: en Courses (endpoint o evento) o en Roadmap?
