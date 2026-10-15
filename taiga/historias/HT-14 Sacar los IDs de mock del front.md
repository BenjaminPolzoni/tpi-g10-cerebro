---
tags: [tpi, g10, taiga, ht]
codigo: HT-14
ref: 8598
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8632 Deuda del Sprint 2|EP-8632]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8598
---

# HT-14: Sacar los IDs de mock del front

> [!info] Generado desde Taiga (2026-10-15 16:54). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8598) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8632 Deuda del Sprint 2|EP-8632]] · Tareas cerradas: **0/5**

[G10] — HT-14 — Sacar los IDs de mock del front
-----------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: ver siempre mis datos y los de mi curso, nunca los de un alumno o curso de prueba
*   **Para**: confiar en lo que muestra el roadmap y el ranking

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El alumno sale de la sesión y el curso de la ruta. Sin sesión o sin curso se muestra un error; nunca un respaldo silencioso.
*   [ ] Validaciones: No quedan referencias a `DEMO_STUDENT_ID`, `COURSE_SEED_ID` ni `CURRENT_STUDENT_ID` fuera de tests y mocks.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): Un alumno no puede ver datos de otro por un id fijo en el código.
*   [ ] Accesibilidad (WCAG/teclado/lectores): El mensaje de error se anuncia (`aria-live`).
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: `roadmap.store.ts`, `hex-world-page` y `challenge-attempt.service` toman el alumno de la sesión.
*   [ ] **CA2**: `RoadmapStore` y `ranking-panel` toman el curso de la ruta.
*   [ ] **CA3**: `ranking-detail` usa el alumno de la sesión.
*   [ ] **CA4**: Sin sesión o sin curso se muestra un error claro.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Datos reales en lugar de mocks

**Escenario 1**  

*   **Dado**: un alumno logueado en el curso X
*   **Cuando**: abre el roadmap
*   **Entonces**: ve su progreso del curso X

**Escenario 2**  

*   **Dado**: un alumno logueado
*   **Cuando**: abre el detalle del ranking
*   **Entonces**: su fila resaltada es la suya

**Escenario 3**  

*   **Dado**: una sesión vencida
*   **Cuando**: se abre el roadmap
*   **Entonces**: se muestra un error y no los datos de un alumno de prueba

* * *

Prototipo
---------

*   **Capturas**: Roadmap, mundo hexagonal y ranking.
*   **URL Figma**: No aplica (sin cambio visual).
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: Sin cambios de API.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 3
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 3 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno nuevo.
*   Módulos afectados: `roadmap.store.ts`, `hex-world-page`, `challenge-attempt.service`, `ranking-panel`, `ranking-detail`.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Pantallas que dependían del respaldo fallan en desarrollo; mitigación: usar el proxy con headers de un alumno demo real.


## Tareas

- [ ] #8788 T-14.1 Usar el alumno logueado en el roadmap, el mundo y los intentos · New · Lorenzo Araujo
- [ ] #8804 T-14.2 Usar el curso de la URL en el roadmap y el ranking · New · Lorenzo Araujo
- [ ] #8805 T-14.3 Resaltar la fila del alumno logueado en el detalle del ranking · New · Lorenzo Araujo
- [ ] #8806 T-14.4 Dejar el front sin ids de prueba · New · Lorenzo Araujo
- [ ] #9334 T-14.5 Wiki con capturas y componentes usados · New · Quinteros Tomás
