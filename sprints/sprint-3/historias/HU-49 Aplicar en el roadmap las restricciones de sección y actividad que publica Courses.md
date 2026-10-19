---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-49
estado: New
responsable: "Sin asignar"
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Must
en_taiga: true
ref: 7211
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7211
responsables_tareas: ["Mateo Delgado Costa", "Franco Maximiliano Amarilla"]
tareas_cerradas: "0/6"
---

# HU-49: Aplicar en el roadmap las restricciones de sección y actividad que publica Courses

> Cargada en Taiga: [[taiga/historias/HU-49 Aplicar en el roadmap las restricciones de sección y actividad que publica Courses|HU-49]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7211)) · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Mateo Delgado Costa|Mateo Delgado Costa]] (5), [[sprints/sprint-3/12-responsables#Franco Maximiliano Amarilla|Franco Maximiliano Amarilla]] (1).

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **0/6** · Sprint: **G10 - Sprint 3**
> Ya existe en Taiga: [[taiga/historias/HU-49 Aplicar en el roadmap las restricciones de sección y actividad que publica Courses|HU-49]] (épica EP-4230). En el Sprint 3 se **reabre** con lo que falta. El 2026-10-15 absorbe HU-67 (examen con ventana horaria) y lo oculto/bloqueado de un roadmap entero que estaba en HU-61, y pasa a Must porque la demo (HT-21) lo necesita.

[G10] — HU-49 — Aplicar en el roadmap las restricciones de sección y actividad que publica Courses
--------------------------------------------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: saber por qué un nodo, una sección o un roadmap está oculto o bloqueado por fecha (incluida la ventana horaria de los exámenes), y que se actualice cuando Courses cambia la restricción
*   **Para**: no perderme una actividad habilitada ni intentar una que todavía no lo está

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Courses publica restricciones por sección y actividad. HIDDEN: el alumno no ve el nodo. LOCKED: lo ve bloqueado con la fecha. El gate ya evalúa `DATE_RESTRICTED`. La ventana horaria de un nodo `EXAM` es una restricción de fecha más que publica Courses (P9): el nodo no tiene campos propios. Lo oculto y lo bloqueado se aplica también a un roadmap entero.
*   [ ] Validaciones: Si llega un evento de cambio, se invalida la caché de restricciones del curso. Las fechas se guardan en UTC y se muestran en la zona horaria del curso.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): La fecha de habilitación en texto, no solo con un ícono.
*   [ ] Otros: Depende de G01 (evento de cambio). Con N roadmaps, el profesor define las restricciones de cada roadmap y se copian al clonarlo (G4). E3: puede que ya esté hecha; corroborarlo antes de empezar.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Un nodo HIDDEN no aparece al alumno.
*   [ ] **CA2**: Un nodo LOCKED aparece bloqueado con su fecha de habilitación.
*   [ ] **CA3**: Al llegar el evento de cambio de Courses, el estado se actualiza.
*   [ ] **CA4**: El front muestra el aviso con la fecha.
*   [ ] **CA5**: Un nodo examen fuera de su ventana horaria responde `DATE_RESTRICTED` y muestra «Se habilita el {fecha} a las {hora}», con tests de reloj simulado.
*   [ ] **CA6**: Un roadmap que Courses marca como oculto no aparece al alumno; uno bloqueado aparece con el motivo y la fecha.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Restricciones de Courses

**Escenario 1**  

*   **Dado**: un nodo con restricción HIDDEN
*   **Cuando**: el alumno abre el roadmap
*   **Entonces**: no lo ve

**Escenario 2**  

*   **Dado**: un nodo LOCKED hasta el 20/10
*   **Cuando**: el alumno lo abre el 18/10
*   **Entonces**: lo ve bloqueado con «se habilita el 20/10»

**Escenario 3**  

*   **Dado**: Courses cambia la fecha de un nodo
*   **Cuando**: llega el evento
*   **Entonces**: el roadmap muestra la fecha nueva

**Escenario 4**  

*   **Dado**: un examen habilitado de 18:00 a 20:00
*   **Cuando**: el alumno entra a las 17:59
*   **Entonces**: el gate responde `DATE_RESTRICTED` y el alumno ve «Se habilita hoy a las 18:00»

* * *

Prototipo
---------

*   **Capturas**: Nodo bloqueado por fecha y examen fuera de horario en el mapa.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-badge` para el estado.
*   **Mock API / Swagger**: Restricciones de Courses (`course.restrictions.read`) y evento de cambio a acordar.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 8 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Courses (restricciones y evento).
*   Módulos afectados: `CourseRestrictionsClient`, `GateEvaluator`, mapa del alumno.
*   Otros equipos / aprobaciones: G01 (bloqueante para el evento; publica las ventanas de examen, P9).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que G01 no publique el evento a tiempo; mitigación: leer por pull con caché corta. Zonas horarias en los exámenes; mitigación: guardar en UTC y mostrar en la del curso.

## Tareas

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **1/6**. Historia en Taiga: [[taiga/historias/HU-49 Aplicar en el roadmap las restricciones de sección y actividad que publica Courses|HU-49]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7211)

- [x] [#9311](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9311) **T-49.9 Corroborar qué ya está hecho** · Equipo · Done · [[sprints/sprint-3/12-responsables#Mateo Delgado Costa|Mateo Delgado Costa]]
    - **Qué:** según E3 puede estar hecho. Probar en develop restricciones de Courses ocultas, bloqueadas y por fecha, y actualizar esta HU con lo que falte antes de seguir.
    - **Listo cuando:** la HU dice exactamente qué falta.
    - **Resultado del análisis en develop:**
        - **Ya implementado en develop (backend `tpi-roadmap`):**
            - `HttpCourseRestrictionsClient`: Cliente HTTP operativo con token técnico que consulta restricciones de sección (`/api/courses/course-sections/{id}/restrictions`) y de actividad (`/api/courses/course-activities/{id}/restrictions`). Soporta parseo de condiciones `DATE` (fechas locales, offset y fechas solas con ventana inclusiva de apertura y exclusiva de cierre) y condiciones `GROUP`.
            - `UnitRestrictionRules`: Evaluación en memoria de operadores lógicos `ALL` y `ANY` combinando pertenencia a comisiones y ventanas temporales (`DateWindow.satisfiedAt(now)`).
            - `DateGateTest`: Suite de pruebas funcionales en el backend que verifica que ventanas vencidas y futuras bloquean con `date_restricted`, ventanas abiertas permiten (`eligible: true`), y POST a lectura de contenido fuera de fecha devuelve 403 Forbidden.
        - **Qué falta exactamente antes de continuar:**
            - **T-49.10 (Distinguir oculto de bloqueado):** En backend, Courses publica `on_unmet` (`HIDDEN` / `LOCKED`), pero `HttpCourseRestrictionsClient` no lo mapea y `SectionGroupRestriction` no lo almacena. `UnitRestrictionRules`, `GroupVisibilityRules` y `GroupUnitsService` deben distinguir si una restricción no cumplida oculta la entidad (`HIDDEN`) o la deja visible bloqueada con su fecha (`LOCKED`), aplicando tanto a nivel nodo, sección y roadmap completo. Faltan tests de ambos casos en los 3 niveles.
            - **T-49.11 (Actualizar el roadmap ante cambios de restricción):** Falta consumir el evento de cambio de restricciones de G01 o implementar caché corta con lectura por pull si G01 no lo publica. Registrar el acuerdo con G01.
            - **T-49.12 (Front: Mostrar al alumno lo bloqueado y cuándo se habilita):** En el front (`2026-PIV-TPI-FE`), el mapa 2D (`course-map-page`) y el mundo 3D (`hex-world-page`) no ocultan lo `HIDDEN`, no soportan `date_restricted` en `NodeBlockReason`, ni muestran el texto accesible «Se habilita el {fecha}» (o «Se habilita el {fecha} a las {hora}» en examen) para lectores de pantalla.
            - **T-49.13 (Aplicar al examen la ventana horaria de Courses):** Conectar la restricción de fecha de actividad de Courses con el nodo de examen `EXAM` (`boss`), validando antes y después de la ventana con `DATE_RESTRICTED` sin persistir fechas propias en el nodo (P9). Faltan tests con reloj simulado a las 17:59, 18:30 y 20:01.
- [ ] [#9312](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9312) **T-49.10 Distinguir oculto de bloqueado** · Back · New · [[sprints/sprint-3/12-responsables#Mateo Delgado Costa|Mateo Delgado Costa]]
    - **Qué:** con el `on_unmet` que publica Courses, `HIDDEN` saca el nodo, la sección o el roadmap de lo que ve el alumno y `LOCKED` lo deja visible bloqueado, con su fecha.
    - **Dónde:** `CourseRestrictionsClient`, `UnitRestrictionRules`, `GroupVisibilityRules`, `GroupUnitsService`.
    - **Listo cuando:** hay tests de los dos casos en nodo, sección y roadmap.
- [ ] [#9313](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9313) **T-49.11 Actualizar el roadmap cuando Courses cambia una restricción** · Back + Coordinación · New · [[sprints/sprint-3/12-responsables#Mateo Delgado Costa|Mateo Delgado Costa]]
    - **Qué:** si G01 publica un evento de cambio, consumirlo e invalidar la caché de restricciones; si no lo publica, usar caché corta con lectura por pull. Registrar el acuerdo con G01.
    - **Dónde:** `CoursesLifecycleEventListener`.
    - **Listo cuando:** un cambio en Courses se ve en el roadmap sin reiniciar nada.
- [ ] [#9314](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9314) **T-49.12 Mostrarle al alumno lo bloqueado y cuándo se habilita** · Front · New · [[sprints/sprint-3/12-responsables#Mateo Delgado Costa|Mateo Delgado Costa]]
    - **Qué:** el mapa del alumno no muestra lo oculto y en lo bloqueado dice «Se habilita el {fecha}» (en un examen, «Se habilita el {fecha} a las {hora}»), en texto.
    - **Listo cuando:** se ve en el mapa 2D y en el mundo, y lo lee un lector de pantalla.
- [ ] [#9315](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9315) **T-49.13 Aplicar al examen la ventana horaria que publica Courses** · Back · New · [[sprints/sprint-3/12-responsables#Mateo Delgado Costa|Mateo Delgado Costa]]
    - **Qué:** la restricción de fecha que Courses publica para la actividad (`CourseRestrictionsClient`) se aplica al nodo `EXAM` correspondiente, sin datos propios en el nodo (P9). Antes y después de la ventana el gate responde `DATE_RESTRICTED` (antes HU-67).
    - **Listo cuando:** hay tests con reloj simulado a las 17:59, 18:30 y 20:01.
- [ ] [#9346](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9346) **T-49.14 Wiki, OpenAPI y diagrama de secuencia** · New · [[sprints/sprint-3/12-responsables#Franco Maximiliano Amarilla|Franco Maximiliano Amarilla]]
    - Tarea de documentación agregada en Taiga por el equipo; no estaba en la propuesta.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

- **Backend (`tpi-roadmap` develop):**
  - El cliente HTTP `HttpCourseRestrictionsClient` y el evaluador `UnitRestrictionRules` evalúan fechas y comisiones.
  - El gate responde `date_restricted` para ventanas vencidas y futuras, y 403 Forbidden en lectura (`DateGateTest`).
  - **Falta:** `on_unmet` (`HIDDEN` vs `LOCKED`) en cliente, modelo y reglas de visibilidad (nodo, sección y roadmap); actualización reactiva por evento de Courses o caché corta; vincular ventana horaria al nodo `EXAM` sin fechas propias (tests a 17:59, 18:30, 20:01).
- **Frontend (`2026-PIV-TPI-FE` develop):**
  - No tiene soporte para `date_restricted` en `NodeBlockReason` ni textos de habilitación por fecha/hora en mapa 2D o mundo 3D.
  - La obligatoriedad en `detailsOf` de `roadmap-section-nodes` se mostraba únicamente para `theory`.

### Depende de

- G01 Courses: evento de cambio de restricciones (bloqueante para CA3) y ventanas de examen (P9). El resto se puede empezar ya.
- [[sprints/sprint-3/historias/HU-67 Nodo examen con ventana horaria|HU-67]] Nodo examen con ventana horaria (absorbida por T-49.13 según P9)

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P9]] La ventana horaria la publica Courses.
- ✅ [[sprints/sprint-3/08-dudas|G4]] Restricciones por roadmap, definidas por el profesor; se copian al clonar.
- ✅ [[sprints/sprint-3/08-dudas|E3]] Ya debería estar hecho: corroborado en develop (hecho el gate por fecha y cliente básico, falta `on_unmet`, evento/caché corta, visibilidad front y tests de examen).
