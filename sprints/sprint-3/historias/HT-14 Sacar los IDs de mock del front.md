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

- [ ] **T-14.1 Usar el alumno logueado en el roadmap, el mundo y los intentos** · Front
    - **Qué:** sacar el respaldo `DEMO_STUDENT_ID` y tomar el id del alumno de la sesión. Si no hay sesión, mostrar un error en vez de seguir con el alumno de prueba.
    - **Dónde:** `roadmap.store.ts`, `hex-world-page`, `challenge-attempt.service`.
    - **Listo cuando:** con dos alumnos distintos cada uno ve su propio progreso, y sin sesión aparece el error (anunciado con `aria-live`). Hay un test de cada caso.
- [ ] **T-14.2 Usar el curso de la URL en el roadmap y el ranking** · Front
    - **Qué:** sacar `COURSE_SEED_ID` como curso por defecto y leer el curso de la ruta. Si la ruta no trae curso, error claro.
    - **Dónde:** `RoadmapStore` (`roadmap.store.ts`) y `ranking-panel`.
    - **Listo cuando:** dos cursos distintos muestran datos distintos, y hay un test sin curso en la ruta.
- [ ] **T-14.3 Resaltar la fila del alumno logueado en el detalle del ranking** · Front
    - **Qué:** reemplazar el mock `CURRENT_STUDENT_ID` por el alumno de la sesión para marcar «mi fila».
    - **Dónde:** `ranking-detail`.
    - **Listo cuando:** se resalta la fila del alumno logueado y no la de un alumno fijo. Hay un test.
- [ ] **T-14.4 Dejar el front sin ids de prueba** · Front
    - **Qué:** buscar `DEMO_STUDENT_ID`, `COURSE_SEED_ID` y `CURRENT_STUDENT_ID` en `src/app` y dejarlos solo en tests y mocks.
    - **Listo cuando:** la búsqueda da cero fuera de tests y mocks, y `npm run verify` pasa.

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
