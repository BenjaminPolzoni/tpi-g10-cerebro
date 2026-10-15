---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-73
estado: Propuesta
responsable: ""
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Should
en_taiga: false
---

# HU-73: Ver mi racha de días con actividad

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga. Es la primera HU de [[taiga/epicas/EP-592 Racha|EP-592 Racha]], que entra en el Sprint 3 por E12 (2026-10-15).

[G10] — HU-73 — Ver mi racha de días con actividad
--------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: ver mi racha de días seguidos con actividad resuelta y mi racha máxima en el curso
*   **Para**: tener un incentivo para estudiar con constancia

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Un día cuenta si el alumno completó un nodo o leyó un contenido obligatorio. La racha es por curso-cohorte y el corte del día usa la zona horaria del curso, no la del navegador. Dos actividades el mismo día cuentan como un día. Sin comodines: un día sin actividad corta la racha. La racha vigente se deriva del registro diario; la máxima se guarda. Es cosmética: no habilita ni bloquea nada.
*   [ ] Validaciones: Registrar la actividad es idempotente por alumno, curso y día.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): La racha responde en menos de 200 ms y llega en la misma carga que el progreso, sin una llamada extra.
*   [ ] Seguridad (roles, permisos, datos sensibles): El alumno ve solo su racha.
*   [ ] Accesibilidad (WCAG/teclado/lectores): El número de la racha se lee como texto, no solo como ícono.
*   [ ] Otros: Detrás de un flag porque no tiene RF en el PRD (P-07). Reemplaza el 7 fijo del front (DT-13). La racha es criterio de una insignia (CA6).

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Un alumno con actividad tres días seguidos ve racha 3.
*   [ ] **CA2**: Si se saltea un día, al volver ve racha 1 y máxima 3.
*   [ ] **CA3**: Dos actividades el mismo día cuentan como un día.
*   [ ] **CA4**: El HUD muestra la racha real con `generic-streak-flame` y desaparece el valor fijo.
*   [ ] **CA5**: Registrar la actividad no cambia ningún desbloqueo ni ninguna lectura.
*   [ ] **CA6**: Al llegar a la racha configurada para la insignia (por ejemplo, 50 días), el alumno recibe la insignia de racha una sola vez.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Racha

**Escenario 1**  

*   **Dado**: un alumno que completó un nodo hoy, ayer y anteayer
*   **Cuando**: abre su progreso
*   **Entonces**: ve racha 3

**Escenario 2**  

*   **Dado**: un alumno con racha 3 que no tuvo actividad ayer
*   **Cuando**: completa un nodo hoy
*   **Entonces**: ve racha 1 y máxima 3

**Escenario 3**  

*   **Dado**: un alumno que completó dos nodos hoy
*   **Cuando**: abre su progreso
*   **Entonces**: hoy cuenta como un solo día

* * *

Prototipo
---------

*   **Capturas**: HUD de progreso del alumno con la llama de racha.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-streak-flame`.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/progress con `current_streak` y `max_streak`.

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

*   Servicios involucrados: Ninguno externo.
*   Módulos afectados: Registro de actividad diaria, progreso del alumno, HUD de racha (`streak.component`), evaluador de insignias.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Tabla nueva `actividad_diaria` (alumno, curso-cohorte, día) con clave única por los tres, y campo `racha_maxima` por alumno y curso-cohorte. Sin datos históricos que migrar.
*   Riesgos y mitigación (opcional): Un corte horario mal tomado sumaría más de un día por día real; mitigación: tests con reloj simulado en la zona horaria del curso.

## Tareas

- [ ] **T-73.1 Registrar los días con actividad** · Back
    - **Qué:** migración con `actividad_diaria` (alumno, curso-cohorte, día; únicos los tres) y `racha_maxima`. Se registra al completar un nodo o leer un contenido obligatorio, con el día según la zona horaria del curso.
    - **Dónde:** `ProgressService`, `ContentReadingWriter`.
    - **Listo cuando:** dos actividades el mismo día dejan un solo registro. Hay test.
- [ ] **T-73.2 Calcular la racha y devolverla con el progreso** · Back
    - **Qué:** `current_streak` y `max_streak` en la respuesta del progreso, detrás de un flag de racha.
    - **Listo cuando:** responde en menos de 200 ms y hay tests con reloj simulado (3 días seguidos, un día salteado).
- [ ] **T-73.3 Mostrar la racha real en el HUD** · Front
    - **Qué:** `streak.component` usa `generic-streak-flame` con el dato real y se saca el 7 fijo (DT-13).
    - **Listo cuando:** la llama muestra la racha del alumno logueado.
- [ ] **T-73.4 Insignia por racha** · Back
    - **Qué:** criterio de insignia por racha (por ejemplo, 50 días) evaluado en `BadgeEvaluator`.
    - **Listo cuando:** se otorga una vez al llegar a la racha. Hay test.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

`streak.component` muestra un 7 fijo, sin lógica (DT-13). EP-592 no tenía ninguna HU.

### Depende de

- [[sprints/sprint-3/historias/HT-26 Adopción de la UI-KIT en el roadmap|HT-26]] Adopción de la UI-KIT en el roadmap (`generic-streak-flame`, para T-73.3). El back (T-73.1, T-73.2 y T-73.4) se puede empezar ya.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|E12]] Racha es nueva para el Sprint 3.
