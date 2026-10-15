---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-45
estado: Propuesta
responsable: ""
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Must
en_taiga: true
---

# HU-45: Ranking de la cohorte y avance por comisión

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Ya existe en Taiga: [[taiga/historias/HU-45 Ranking de la cohorte y avance por comisión|HU-45]] (épica EP-5371). En el Sprint 3 se **reabre** con lo que falta.

[G10] — HU-45 — Ranking de la cohorte y avance por comisión
-----------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO / PROFESOR
*   **Quiero**: ver el ranking sin errores, por curso por defecto y filtrable por comisión, y como profesor ver el avance por comisión
*   **Para**: comparar el avance con el curso o la comisión

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Default: ranking por curso; la comisión es un filtro (P10). Orden por XP con desempate en cascada (HU-25); si van notas lo define P14. Corrección de los profes: hoy el ranking por grupo da error (sin reproducir, E1).
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): Anonimato de filas ajenas (DEC-007). El avance por comisión: ADMIN o PROFESSOR.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Filtro accesible con teclado.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Error del ranking por grupo reproducido y documentado.
*   [ ] **CA2**: El ranking muestra el del curso por defecto, con filtro opcional por comisión.
*   [ ] **CA3**: El profesor ve el avance por comisión (`GET /courses/{id}/groups/{gid}/progress`).
*   [ ] **CA4**: Test que cubre el caso que fallaba.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Ranking y avance por comisión

**Escenario 1**  

*   **Dado**: un curso con 2 comisiones
*   **Cuando**: el alumno abre el ranking
*   **Entonces**: ve el del curso completo

**Escenario 2**  

*   **Dado**: el mismo curso
*   **Cuando**: elige su comisión
*   **Entonces**: ve solo los de su comisión, sin datos personales ajenos

**Escenario 3**  

*   **Dado**: un profesor del curso
*   **Cuando**: abre el avance por comisión
*   **Entonces**: ve el progreso de cada comisión

* * *

Prototipo
---------

*   **Capturas**: Ranking con filtro; panel del profesor.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-select`, `generic-table`.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/ranking?group_id=… y GET /api/roadmap/courses/{courseId}/groups/{groupId}/progress.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 5
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 5 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Courses (comisiones).
*   Módulos afectados: `RankingController`, `RankingService`, `GroupProgressController`, `ranking-panel`.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Depende de HT-13 (flag).

## Tareas

- [ ] T-45.7 Reproducir el error (E1)
- [ ] T-45.8 Filtro por comisión en el back
- [ ] T-45.9 Filtro en el front
- [ ] T-45.10 Avance por comisión del profesor
- [ ] T-45.11 Tests

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

El back tiene ranking solo por curso y `GET /groups/{gid}/progress` aparte. El front no tiene filtro ni vista de avance por comisión. Los profes reportan que el ranking por grupo da error. HU-45 sigue en New.

### Depende de

- [[sprints/sprint-3/historias/HT-13 Encender los flags en los entornos|HT-13]] Encender los flags en los entornos

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E1]]
- [[sprints/sprint-3/08-dudas|P10]]
- [[sprints/sprint-3/08-dudas|P14]]
