---
tags: [tpi, g10, taiga, hu]
codigo: HU-48
ref: 7206
estado: "Done"
responsable: "Mateo Delgado Costa"
epica: "[G10] — Progreso y desbloqueo"
sprint: "Backlog"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7206
---

# HU-48: Saber si puedo entrar a un desafío antes de abrirlo

> [!info] Generado desde Taiga (2026-10-14 18:47). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7206) · Estado: **Done** · Responsable: **Mateo Delgado Costa** · Sprint: **Backlog**

[G10] — HU-48 — Saber si puedo entrar a un desafío antes de abrirlo
-------------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: que al elegir un desafío del roadmap se valide si puedo entrar y, si puedo, se abra el intento en el Motor en la misma pestaña
*   **Para**: saber qué me falta en lugar de chocar con un error genérico del Motor

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El chequeo previo usa el mismo GateService que consulta el Motor y devuelve el mismo vocabulario (not_enrolled, course_archived, content_not_read, prerequisite_pending, no_lives, …). Si está habilitado, el front llama POST /api/engine-challenge/challenges/{challengeId}/intentos con {course_id, node_id, attempt_type} y navega en la misma pestaña. attempt_type sale de la política de vidas del nodo: STANDARD → NORMAL, RECOVERY → RECOVERY, LLM → LLM. El Motor vuelve a consultar el gate del lado del servidor: el chequeo previo mejora la experiencia, no reemplaza el control. Roadmap no crea intentos (acta roadmap-motor-gate-v1).
*   [ ] Validaciones: Nodo de desafío del curso-cohorte; alumno tomado del token.
*   [ ] Datos obligatorios: courseCohortId y nodeId; el alumno sale del token.
*   [ ] Performance (tiempos, volumen, límites): P95 por debajo de 200 ms, igual que el gate de HU-15.
*   [ ] Seguridad (roles, permisos, datos sensibles): Rol STUDENT con matrícula activa; el studentId nunca viaja en el path.
*   [ ] Accesibilidad (WCAG/teclado/lectores): El motivo se muestra en texto y se anuncia con aria-live; el botón queda deshabilitado mientras se abre el intento.
*   [ ] Otros: Reemplaza POST /courses/{courseId}/nodes/{nodeId}/start, que duplica el gate a medias (no evalúa content_not_read y toma las vidas de student_course en lugar de Inventario) y no tiene consumidores. Unifica startChallengeAttempt, hoy copiado en hex-world-page y section-map-page con attempt_type NORMAL fijo. Decisión del 08/10: el intento lo abre el front contra el Motor en la misma pestaña.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Un alumno sin la lectura obligatoria ve «contenido no leído» y no se llama al Motor.
*   [ ] **CA2**: Un nodo habilitado abre el intento en la misma pestaña con el attempt_type de su política de vidas.
*   [ ] **CA3**: Un nodo de recuperación abre con attempt_type RECOVERY aunque el alumno tenga 0 vidas.
*   [ ] **CA4**: El endpoint POST …/start deja de existir y el OpenAPI lo refleja.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Chequeo previo y apertura del intento

**Escenario 1**  

*   **Dado**: un desafío con contenido obligatorio sin leer
*   **Cuando**: el alumno lo elige en el roadmap
*   **Entonces**: ve «contenido no leído» y no se abre ningún intento

**Escenario 2**  

*   **Dado**: un desafío habilitado con política STANDARD
*   **Cuando**: el alumno lo elige
*   **Entonces**: se abre el intento NORMAL en el Motor en la misma pestaña

**Escenario 3**  

*   **Dado**: un desafío de recuperación y un alumno con 0 vidas
*   **Cuando**: el alumno lo elige
*   **Entonces**: se abre el intento con attempt_type RECOVERY

* * *
Prototipo
---------

*   **Capturas**: Torre del mundo hexagonal (hex-world-page) y desafío del mapa de sección (section-map-page) con el motivo de bloqueo en texto.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/nodes/{nodeId}/eligibility → {eligible, reason, challenge_id, attempt_type}. Consumido por el front: POST /api/engine-challenge/challenges/{challengeId}/intentos.

* * *
Estimación / Prioridad
----------------------

*   **Puntos (Fibonacci)**: 3
*   **Prioridad (MoSCoW / Numérica)**: Must

* * *
Dependencias / Impactos
-----------------------

*   Servicios involucrados: Motor de Desafíos (apertura), Accounting (vidas vía gate), API Gateway.
*   Módulos afectados: ProgressController, ProgressService, GateService, hex-world-page, section-map-page.
*   Otros equipos / aprobaciones: Ninguno bloqueante.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que el chequeo previo y el del Motor difieran; mitigación: ambos usan GateService.

## Tareas

- [ ] #7207 T-48.1 Elegibilidad para el alumno sobre GateService · New · Sin asignar
- [ ] #7208 T-48.2 Front: chequeo previo y apertura en la misma pestaña · New · Sin asignar
- [ ] #7209 T-48.3 BDD del chequeo previo · New · Sin asignar
- [ ] #7210 T-48.4 Wiki, OpenAPI y diagrama de secuencia · New · Sin asignar
- [x] #8159 [Backend] Extender eligibility a {challenge_id, attempt_type} y retirar POST /start · Closed · Mateo Delgado Costa
- [x] #8160 [Front] Chequeo previo del gate + apertura de intento en el Motor · Closed · Mateo Delgado Costa
- [x] #8161 [Test] Cobertura HU-48 (BDD CA1-CA4) · Closed · Mateo Delgado Costa
- [x] #8162 [Backend] Matricula real del alumno desde Courses (evento + fallback) · Closed · Mateo Delgado Costa
