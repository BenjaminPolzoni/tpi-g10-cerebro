---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-14
estado: Propuesta
responsable: ""
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 3
prioridad: Must
en_taiga: false
---

# HT-14: Sacar los IDs de mock del front

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

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

- [ ] T-14.1 Reemplazar `DEMO_STUDENT_ID` por el alumno de la sesión
- [ ] T-14.2 Reemplazar `COURSE_SEED_ID` por el curso de la ruta
- [ ] T-14.3 Reemplazar `CURRENT_STUDENT_ID` en `ranking-detail`
- [ ] T-14.4 Tests de las pantallas sin sesión

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

`DEMO_STUDENT_ID` se usa de respaldo en `roadmap.store.ts`, `hex-world-page` y `challenge-attempt.service`. `COURSE_SEED_ID` es el curso por defecto del store y del `ranking-panel`. `CURRENT_STUDENT_ID` (mock) en `ranking-detail`.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

Ninguna.

### Deuda técnica que cierra

- [[deuda-tecnica|DT-09]]
