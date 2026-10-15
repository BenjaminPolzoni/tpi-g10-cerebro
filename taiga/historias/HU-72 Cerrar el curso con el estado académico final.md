---
tags: [tpi, g10, taiga, hu]
codigo: HU-72
ref: 8620
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8632 Deuda del Sprint 2|EP-8632]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8620
---

# HU-72: Cerrar el curso con el estado académico final

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8620) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8632 Deuda del Sprint 2|EP-8632]] · Tareas cerradas: **0/5**

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

- [ ] #9222 T-72.1 Acordar con Courses dónde se guarda el estado final · New · Benjamin Polzoni
- [ ] #9223 T-72.2 Calcular los candidatos a promoción y a pérdida de regularidad · New · Benjamin Polzoni
- [ ] #9225 T-72.3 Pantalla de cierre del curso · New · Benjamin Polzoni
- [ ] #9226 T-72.4 Exportar el resumen por alumno · New · Benjamin Polzoni
- [ ] #9355 T-72.5 Wiki, OpenAPI y diagrama de secuencia · New · Quinteros Tomás
