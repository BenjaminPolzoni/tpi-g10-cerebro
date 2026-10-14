---
tags: [tpi, g10, taiga, hu]
codigo: HU-47
ref: 7196
estado: "Done"
responsable: "Mateo Delgado Costa"
epica: "[G10] — Edición del roadmap por el profesor"
sprint: "Backlog"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7196
---

# HU-47: Asignar a un nodo un desafío de mi pool del Motor

> [!info] Generado desde Taiga (2026-10-14 18:47). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7196) · Estado: **Done** · Responsable: **Mateo Delgado Costa** · Sprint: **Backlog**

[G10] — HU-47 — Asignar a un nodo un desafío de mi pool del Motor
-----------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR dueño del curso
*   **Quiero**: asignar a cada nodo de desafío uno de los desafíos que yo creé y publiqué en el Motor, eligiéndolo de una lista
*   **Para**: armar el roadmap con mis propios desafíos sin tipear identificadores ni ubicar desafíos en borrador, archivados, ajenos o de otro tipo

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El pool lo trae siempre el Motor: Roadmap lo consulta con token técnico (challenges.catalog.read) y se queda con los desafíos PUBLISHED cuyo author_id es el profesor autenticado (el UUID que Courses reconoce como dueño del curso). Un nodo THEORETICAL_CHALLENGE solo admite desafíos THEORETICAL y uno PRACTICAL_CHALLENGE solo PRACTICAL. Al guardar, el back vuelve a validar el desafío contra el Motor. Si el Motor no responde no se asigna nada. Roadmap guarda solo la referencia (challenge_id), nunca el enunciado. Las secciones vienen de Courses (HU-36, HU-37) y el contenido teórico de los nodos CONTENT lo publica Courses (HU-04, HU-46): ambos quedan fuera de esta historia.
*   [ ] Validaciones: Desafío existente, PUBLISHED, con author_id igual al profesor y de tipo compatible con el nodo; nodo de una sección activa del curso-cohorte.
*   [ ] Datos obligatorios: courseCohortId, nodeId y challenge_id.
*   [ ] Performance (tiempos, volumen, límites): El pool responde en menos de 1 s con hasta 300 desafíos publicados en el sistema (3 páginas de 100). El guardado, en menos de 300 ms más la consulta al Motor.
*   [ ] Seguridad (roles, permisos, datos sensibles): Solo el PROFESSOR dueño del curso, validado contra Courses (403 sin cambios si no lo es). El Motor se consulta con token técnico por el API Gateway.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Selector operable por teclado, con título, tipo y dificultad en texto; errores junto al campo anunciados con aria-live.
*   [ ] Otros: Reemplaza el input de UUID libre de entity-editor-dialog. Hoy requireKnownChallenge solo verifica que el desafío exista (acepta archivados y no cruza el tipo) y, con el Motor caído, guarda sin validar: se corrige acá. El filtro por autor se hace en Roadmap hasta que G09 exponga author_id como filtro (T-47.7). Decisión del 08/10: la asignación desafío → nodo es de Roadmap.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El selector muestra solo mis desafíos publicados del tipo del nodo.
*   [ ] **CA2**: Asignar un desafío archivado o en borrador se rechaza (409) y el nodo no cambia.
*   [ ] **CA3**: Asignar un desafío de otro profesor se rechaza (403) y el nodo no cambia.
*   [ ] **CA4**: Asignar un desafío de otro tipo se rechaza (400) y el nodo no cambia.
*   [ ] **CA5**: Con el Motor sin responder se informa «catálogo del Motor no disponible» (503) y no se guarda nada.
*   [ ] **CA6**: Un profesor que no es dueño del curso recibe 403 sin efectos.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Asignación de desafíos del pool del profesor

**Escenario 1**  

*   **Dado**: un nodo THEORETICAL_CHALLENGE y un profesor con desafíos teóricos y prácticos publicados
*   **Cuando**: abre el selector del nodo
*   **Entonces**: ve solo sus desafíos teóricos publicados

**Escenario 2**  

*   **Dado**: un desafío publicado de otro profesor
*   **Cuando**: intenta asignarlo al nodo por la API
*   **Entonces**: se rechaza por permiso y el nodo conserva su desafío

**Escenario 3**  

*   **Dado**: un desafío propio archivado en el Motor
*   **Cuando**: intenta asignarlo
*   **Entonces**: se rechaza porque no está publicado y nada cambia

**Escenario 4**  

*   **Dado**: el Motor sin responder
*   **Cuando**: el profesor abre el selector o guarda el nodo
*   **Entonces**: ve «catálogo del Motor no disponible» y no se guarda nada

* * *
Prototipo
---------

*   **Capturas**: entity-editor-dialog (course-builder-page y course-map-page) con selector de desafíos en lugar del campo de UUID.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/challenge-pool?type=THEORETICAL_CHALLENGE|PRACTICAL_CHALLENGE; PUT y PATCH /api/roadmap/nodes/{nodeId} (challenge_id). Consumidos del Motor: GET /api/engine-challenge/challenges?status=PUBLISHED&page={n}&size=100 y GET /api/engine-challenge/challenges/{challengeId}.

* * *
Estimación / Prioridad
----------------------

*   **Puntos (Fibonacci)**: 5
*   **Prioridad (MoSCoW / Numérica)**: Must

* * *
Dependencias / Impactos
-----------------------

*   Servicios involucrados: Motor de Desafíos (G09), Courses (dueño del curso, G01), API Gateway.
*   Módulos afectados: MotorCatalogClient, HttpMotorCatalogClient, GraphValidator, GraphController, entity-editor-dialog.
*   Otros equipos / aprobaciones: G09: filtro author_id (opcional, T-47.7) y aviso de desafío archivado (opcional, T-47.8). G01: alinear US2198 (T-47.9).
*   Impacto en datos / migraciones: Sin migración: node.challenge_id ya existe.
*   Riesgos y mitigación (opcional): El catálogo global crece y el pool recorre muchas páginas; mitigación: tope de páginas configurable y el filtro author_id pedido a G09.

## Tareas

- [ ] #7197 T-47.1 Cliente del Motor: pool de desafíos del profesor · New · Sin asignar
- [ ] #7198 T-47.2 Endpoint del pool: GET /courses/{courseId}/challenge-pool · New · Sin asignar
- [ ] #7199 T-47.3 Revalidar el desafío al asignarlo (publicado, propio y del tipo del nodo) · New · Sin asignar
- [ ] #7200 T-47.4 Selector de desafíos en el editor de nodos · New · Sin asignar
- [ ] #7201 T-47.5 BDD y contract test del catálogo del Motor · New · Sin asignar
- [ ] #7202 T-47.6 Wiki, OpenAPI y diagrama de secuencia · New · Sin asignar
- [ ] #7203 T-47.7 Pedido a G09: filtro author_id en GET /challenges para token de servicio (opcional) · New · Sin asignar
- [ ] #7204 T-47.8 Pedido a G09: aviso de desafío archivado (opcional, HU-01 CA8) · New · Sin asignar
- [ ] #7205 T-47.9 Pedido a G01: alinear US2198 con la asignación de desafíos en Roadmap · New · Sin asignar
- [x] #8154 [Backend] Endpoint GET challenge-pool (pool del Motor del profesor) · Closed · Mateo Delgado Costa
- [x] #8155 [Backend] Endurecer validacion de desafio al crear/editar nodo · Closed · Mateo Delgado Costa
- [x] #8156 [Front] Selector de desafios (GenericSelect) en el editor de nodos · Closed · Mateo Delgado Costa
- [x] #8157 [Test] Cobertura HU-47 (unit + wire + BDD CA1-CA6) · Closed · Mateo Delgado Costa
- [x] #8158 [Backend] Ownership real: proyeccion cohort_professor desde eventos de Courses · Closed · Mateo Delgado Costa
