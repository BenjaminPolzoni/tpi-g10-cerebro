---
tags: [tpi, g10, taiga, hu]
codigo: HU-73
ref: 8621
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8632 Deuda del Sprint 2|EP-8632]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8621
---

# HU-73: Ver mi racha de días con actividad

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8621) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8632 Deuda del Sprint 2|EP-8632]] · Tareas cerradas: **0/5**

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

- [ ] #9227 T-73.1 Registrar los días con actividad · New · Lautaro Jesus Diego
- [ ] #9228 T-73.2 Calcular la racha y devolverla con el progreso · New · Lautaro Jesus Diego
- [ ] #9229 T-73.3 Mostrar la racha real en el HUD · New · Lautaro Jesus Diego
- [ ] #9230 T-73.4 Insignia por racha · New · Lautaro Jesus Diego
- [ ] #9356 T-73.5 Wiki, OpenAPI y diagrama de secuencia · New · Franco Maximiliano Amarilla
