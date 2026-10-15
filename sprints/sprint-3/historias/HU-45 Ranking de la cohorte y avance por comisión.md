---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-45
estado: New
responsable: "Lorenzo Araujo"
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Must
en_taiga: true
ref: 5374
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5374
responsables_tareas: ["Lorenzo Araujo", "Quinteros Tomás", "Benjamin Polzoni"]
tareas_cerradas: "5/13"
---

# HU-45: Ranking de la cohorte y avance por comisión

> Cargada en Taiga: [[taiga/historias/HU-45 Ranking de la cohorte y avance por comisión|HU-45]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5374)) · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Benjamin Polzoni|Benjamin Polzoni]] (6), [[sprints/sprint-3/12-responsables#Lorenzo Araujo|Lorenzo Araujo]] (5), [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]] (2).

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **New** · Responsable de la historia: **[[sprints/sprint-3/12-responsables#Lorenzo Araujo|Lorenzo Araujo]]** · Tareas: **5/13** · Sprint: **G10 - Sprint 3**
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

*   [ ] Reglas de negocio: Default: ranking por curso; la comisión (= grupo) es un filtro (P10, confirmado). El profesor configura si el ranking ordena por XP o por notas (P14); las notas vienen del Motor de desafíos y falta acordar con G09 cómo llegan. El desempate en cascada (HU-25) se mantiene. Corrección de los profes: hoy el ranking por grupo da error (sin reproducir); se arregla en este sprint (E1).
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
*   [ ] **CA5**: El profesor elige si el ranking ordena por XP o por notas.

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
*   Otros equipos / aprobaciones: G09 (cómo llegan las notas del Motor; solo para CA5).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que G09 no defina a tiempo cómo llegan las notas; mitigación: pedirlo la semana 1 (T-45.12).

## Tareas

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **5/13**. Historia en Taiga: [[taiga/historias/HU-45 Ranking de la cohorte y avance por comisión|HU-45]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5374)

- [x] [#5421](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/5421) **T-45.1 Ranking de la cohorte con la XP compartida** · Closed · [[sprints/sprint-3/12-responsables#Lorenzo Araujo|Lorenzo Araujo]]
    - Tarea heredada del Sprint 2, ya cargada en Taiga.
- [x] [#5422](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/5422) **T-45.2 Parámetro de comisión en el avance (no en el ranking)** · Closed · [[sprints/sprint-3/12-responsables#Lorenzo Araujo|Lorenzo Araujo]]
    - Tarea heredada del Sprint 2, ya cargada en Taiga.
- [ ] [#5423](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/5423) **T-45.3 Selector de comisión (filtra avance, no ranking) en StaffRankingView, teacher-home-page y la vista del alumno** · In progress · [[sprints/sprint-3/12-responsables#Lorenzo Araujo|Lorenzo Araujo]]
    - Tarea heredada del Sprint 2, ya cargada en Taiga.
- [x] [#5424](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/5424) **T-45.4 Alumno en varias comisiones y alumno quitado de una** · Closed · [[sprints/sprint-3/12-responsables#Lorenzo Araujo|Lorenzo Araujo]]
    - Tarea heredada del Sprint 2, ya cargada en Taiga.
- [x] [#5425](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/5425) **T-45.5 BDD ranking de la cohorte** · Closed · [[sprints/sprint-3/12-responsables#Lorenzo Araujo|Lorenzo Araujo]]
    - Tarea heredada del Sprint 2, ya cargada en Taiga.
- [x] [#5426](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/5426) **T-45.6 Wiki, OpenAPI y diagrama de secuencia** · Closed · [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]]
    - Tarea heredada del Sprint 2, ya cargada en Taiga.
- [ ] [#9305](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9305) **T-45.7 Reproducir y arreglar el error del ranking por comisión** · Back + Front · New · [[sprints/sprint-3/12-responsables#Benjamin Polzoni|Benjamin Polzoni]]
    - **Qué:** reproducirlo en el entorno integrado con `ROADMAP_BY_GROUP_ENABLED=true`, anotar el pedido y la respuesta que fallan, arreglarlo (E1: se arregla este sprint).
    - **Listo cuando:** el caso que fallaba tiene un test y ya no falla.
- [ ] [#9306](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9306) **T-45.8 Ranking del curso con filtro opcional por comisión** · Back · New · [[sprints/sprint-3/12-responsables#Benjamin Polzoni|Benjamin Polzoni]]
    - **Qué:** por defecto se muestra el ranking del curso; un parámetro opcional de comisión lo filtra (la comisión es un filtro, P10). El anonimato no cambia (DEC-007).
    - **Dónde:** `RankingService`, `RankingController`.
    - **Listo cuando:** con y sin comisión devuelve lo esperado. Hay tests.
- [ ] [#9307](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9307) **T-45.9 Filtro por comisión en la pantalla del ranking** · Front · New · [[sprints/sprint-3/12-responsables#Benjamin Polzoni|Benjamin Polzoni]]
    - **Qué:** un `generic-select` con las comisiones en `ranking-panel`.
    - **Listo cuando:** el alumno cambia de comisión y el ranking se actualiza.
- [ ] [#9308](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9308) **T-45.10 Avance por comisión para el profesor** · Front · New · [[sprints/sprint-3/12-responsables#Benjamin Polzoni|Benjamin Polzoni]]
    - **Qué:** vista para el profesor con el avance de cada comisión, usando `GET /courses/{id}/groups/{gid}/progress` (`GroupProgressController`, ya existe).
    - **Listo cuando:** el profesor compara el avance de dos comisiones.
- [ ] [#9309](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9309) **T-45.11 Elegir si el ranking ordena por XP o por notas** · Back + Front · New · [[sprints/sprint-3/12-responsables#Benjamin Polzoni|Benjamin Polzoni]]
    - **Qué:** ajuste del profesor por roadmap (DEC-017). Con «notas», el orden usa la nota que manda el Motor (P14; acordar con G09 cómo llega). El desempate en cascada sigue igual.
    - **Listo cuando:** cambiar el ajuste cambia el orden y hay tests de los dos modos.
- [ ] [#9310](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9310) **T-45.12 Acordar con el Motor (G09) cómo llegan las notas** · Coordinación · New · [[sprints/sprint-3/12-responsables#Benjamin Polzoni|Benjamin Polzoni]]
    - **Qué:** definir con G09 si la nota llega en el evento de cierre del intento o por consulta, y con qué escala. T-45.11 no arranca hasta tenerlo.
    - **Listo cuando:** el acuerdo está en `acuerdos/motor-desafios-g09`.
- [ ] [#9345](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9345) **T-45.13 Wiki, OpenAPI y diagrama de secuencia** · New · [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]]
    - Tarea de documentación agregada en Taiga por el equipo; no estaba en la propuesta.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

El back tiene ranking solo por curso y `GET /groups/{gid}/progress` aparte. El front no tiene filtro ni vista de avance por comisión. Los profes reportan que el ranking por grupo da error. HU-45 sigue en New.

### Depende de

- Flag `ROADMAP_BY_GROUP_ENABLED` encendido en el entorno (para reproducir el error y para el filtro por comisión).
- G09 Motor: cómo llegan las notas (solo CA5 / T-45.11; bloqueante para esa tarea).

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|E1]] El error del ranking por grupo se arregla en este sprint.
- ✅ [[sprints/sprint-3/08-dudas|E3]] Ya debería estar hecho: corroborarlo.
- ✅ [[sprints/sprint-3/08-dudas|P10]] Sí: por curso por defecto; la comisión (= grupo) es un filtro.
- ✅ [[sprints/sprint-3/08-dudas|P14]] Lo configura el profesor: el ranking ordena por XP o por notas; las notas vienen del Motor de desafíos (G09).
