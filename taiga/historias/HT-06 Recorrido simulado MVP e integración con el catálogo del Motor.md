---
tags: [tpi, g10, taiga, ht]
codigo: HT-06
ref: 3735
estado: "Done"
responsable: "Iker Alonso"
epica: "[G10] — Esqueleto del servicio Roadmap — TRANSVERSAL (v3)"
sprint: "G10 - Sprint 1"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/3735
---

# HT-06: Recorrido simulado MVP e integración con el catálogo del Motor

> [!info] Generado desde Taiga (2026-10-14 18:47). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/3735) · Estado: **Done** · Responsable: **Iker Alonso** · Sprint: **G10 - Sprint 1**

[G10] — HT-06 — Recorrido simulado MVP e integración con el catálogo del Motor
------------------------------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: inicializar con una sola llamada el recorrido de un curso-cohorte real (secciones de Courses o unidades estándar, y nodos con desafíos publicados reales del Motor), y alinear nuestro cliente del Motor con sus rutas definitivas
*   **Para**: que una cohorte nueva (ej. `0c5bffcc-5fab-4338-9ef5-e15631eb8bd6`) cargue de inmediato en `/roadmap/teacher/build/:cohortId` y `/roadmap/play/:cohortId` sin responder `404 roadmap.not-found` y sin que el profesor tenga que pegar UUIDs del Motor a mano

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Para un `courseCohortId` se importan las secciones de Courses (`GET /api/course/course-cohorts/{cohortId}/sections`); si no hay, se generan 2 unidades estándar ("Unidad 1: Fundamentos" y "Unidad 2: Programación Estructurada"). Cada unidad recibe la secuencia pedagógica: Nodo 1 Teoría/Lectura (desbloqueado), Nodo 2 Desafío de práctica (challengeId real del Motor, prerrequisito Nodo 1) y Nodo 3 Desafío de práctica o Boss (challengeId real del Motor, prerrequisito Nodo 2). Si el Motor está caído o no tiene publicados, se usa un conjunto determinista representativo. Si el alumno demo o consultante no está en `student_course`, se lo matricula con 3 vidas y 0 XP.
*   [ ] Validaciones: El grafo generado es acíclico (se reutiliza la validación de HU-13, no se reescribe). Todo challengeId asignado existe en el Motor (`GET /api/engine-challenge/challenges/{challengeId}` → 200). La regeneración sobre una cohorte que ya tiene roadmap no duplica unidades ni nodos.
*   [ ] Datos obligatorios: `courseCohortId`; por nodo de desafío, `challengeId` y tipo (`theoretical-challenge` / `practical-challenge`).
*   [ ] Performance (tiempos, volumen, límites): La inicialización completa responde en menos de 2 s con el Motor disponible; las llamadas al Motor usan el timeout del cliente (2 s) y degradan sin bloquear.
*   [ ] Seguridad (roles, permisos, datos sensibles): Al Motor siempre con token técnico con scope `challenges.catalog.read`, nunca con el JWT de una persona. `POST init-mvp` solo para PROFESSOR o ADMIN. El auto-init en el GET queda detrás de `app.simulation.auto-init-on-get` y apagado fuera de dev/demo.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Sin pantalla propia.
*   [ ] Otros: Pedido al Motor (tpi-engine-challenge): (1) aceptar `hasAuthority('challenges.catalog.read')` en `GET /api/engine-challenge/challenges`; (2) con `status=PUBLISHED` o token de servicio, devolver los publicados de todo el sistema y no filtrar por `authorId`. El alumno nunca habla con los repositorios de desafíos: inicia el intento en el Motor (`POST /api/engine-challenge/challenges/{challengeId}/intentos` con `{ courseId, nodeId, attemptType: "NORMAL" }`), el Motor consulta nuestro gate de elegibilidad y al terminar publica `ATTEMPT_CORRECTED` en Kafka. Dependencias: Motor (scope y pool), Courses (secciones), Gateway y frontend 2026-PIV-TPI-FE. Reemplaza la ruta vieja `?challengeId=` usada en T-01.8 (HU-01). Riesgo: el Motor no habilita el scope a tiempo; mitigación, conjunto determinista de desafíos y pedido por escrito el día 1.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: `HttpMotorCatalogClient` consulta `GET /api/engine-challenge/challenges/{challengeId}` y el pool en `GET /api/engine-challenge/challenges?status=PUBLISHED`, con token técnico de scope `challenges.catalog.read`.
*   [ ] **CA2**: `POST /api/roadmap/courses/{courseCohortId}/init-mvp` genera un roadmap acíclico con unidades y nodos de teoría y desafío, y los nodos de desafío tienen challengeId reales del Motor.
*   [ ] **CA3**: Con `app.simulation.auto-init-on-get=true`, `GET /api/roadmap/courses/{courseCohortId}` de una cohorte sin roadmap responde 200 con el grafo generado en lugar de 404.
*   [ ] **CA4**: Con el Motor caído o sin publicados, la inicialización termina igual usando el conjunto determinista, sin error 5xx.
*   [ ] **CA5**: `GET /api/roadmap/courses/{courseId}/students/{studentId}/nodes/{nodeId}/eligibility` sigue respondiendo `{"data": {"eligible": true, "reason": null}}` para un nodo desbloqueado (regresión del gate).

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Inicialización del recorrido simulado MVP de un curso-cohorte

**Escenario 1**

*   **Dado**: la cohorte `0c5bffcc-5fab-4338-9ef5-e15631eb8bd6` sin roadmap, con secciones en Courses y desafíos publicados en el Motor
*   **Cuando**: el profesor llama a `POST /api/roadmap/courses/{courseCohortId}/init-mvp`
*   **Entonces**: se crea una unidad por sección con Teoría → Práctica → Práctica/Boss, cada desafío con un challengeId real y el primer nodo desbloqueado

**Escenario 2**

*   **Dado**: una cohorte sin secciones en Courses y el Motor sin responder
*   **Cuando**: se inicializa el recorrido
*   **Entonces**: se generan "Unidad 1: Fundamentos" y "Unidad 2: Programación Estructurada" con el conjunto determinista de desafíos y la respuesta es exitosa

**Escenario 3**

*   **Dado**: `app.simulation.auto-init-on-get=true` y una cohorte sin roadmap
*   **Cuando**: el alumno abre `/roadmap/play/{cohortId}`
*   **Entonces**: `GET /api/roadmap/courses/{courseCohortId}` responde 200 con el grafo, el alumno queda matriculado con 3 vidas y 0 XP y ve el nodo inicial desbloqueado

**Escenario 4**

*   **Dado**: una cohorte que ya tiene roadmap generado
*   **Cuando**: se vuelve a llamar a `init-mvp`
*   **Entonces**: no se duplican unidades ni nodos

* * *
Prototipo
---------

*   **Capturas**: No aplica: historia técnica sin pantalla propia. Se valida sobre `/roadmap/teacher/build/:cohortId` y `/roadmap/play/:cohortId` existentes.
*   **URL Figma**: No aplica.
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: `POST /api/roadmap/courses/{courseCohortId}/init-mvp`; `GET /api/roadmap/courses/{courseCohortId}` (auto-init opcional). Consumidos del Motor: `GET /api/engine-challenge/challenges/{challengeId}` y `GET /api/engine-challenge/challenges?status=PUBLISHED`. Consumido de Courses: `GET /api/course/course-cohorts/{cohortId}/sections`.


## Tareas

- [x] #3736 T-06.1 — Solicitud al Motor: scope challenges.catalog.read y pool de publicados · Closed · Iker Alonso
- [x] #3737 T-06.2 — Cliente del Motor: consulta de desafío por ID con path variable · Closed · Iker Alonso
- [x] #3738 T-06.3 — Cliente del Motor: pool de desafíos publicados · Closed · Iker Alonso
- [x] #3739 T-06.4 — Servicio de recorrido simulado (RoadmapSimulationService) · Closed · Iker Alonso
- [x] #3741 T-06.5 — Endpoint init-mvp y auto-init en la consulta del roadmap · Closed · Iker Alonso
- [x] #3742 T-06.6 — Tests de integración y regresión del gate · Closed · Iker Alonso
- [x] #3743 T-06.7 — Prueba end-to-end con el curso real · Closed · Iker Alonso
- [x] #3744 T-06.8 — Wiki: secuencia de inicialización del recorrido MVP · Closed · Iker Alonso
