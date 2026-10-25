# Contrato Roadmap ↔ Courses and Enrollment

Estado: **CONFIRMADO Y VERIFICADO** con el repositorio `2026-P4-BE/tpi-course` (rama `develop` y PRs #31, #36, #41).
Base: `agent.md` §2.2, §3.0, §3.5 y §10.5; `docs/ESTRUCTURA.md` (`clients/courses`).

Resuelve: el gate de habilitación (`not_enrolled`, `course_archived`), el poblado real de `student_course` vía eventos de Kafka, y la validación de permisos de profesor (`HttpCohortOwnershipClient`).

> Mapeo de identificadores: **nuestro `courseId` = su `courseCohortId`**. Roadmap trabaja siempre
> a nivel cohorte, nunca a nivel `courseBase`. Conviene dejarlo escrito antes de integrar.

---

## 1. Lo que ya está implementado de nuestro lado

| Pieza | Dónde | Nota |
|---|---|---|
| Cliente de material por lote | `clients/courses/CoursesMaterialClient` + `HttpCoursesMaterialClient` | `GET /api/course/course-cohorts/{id}/activities?sectionIds=...` con token de servicio (`course.activities.read`). Lo usan el detalle del nodo y la validación del vínculo (HU-04, T-04.2) |
| `CourseMaterial` (`contentId`, `title`, `type`, `status`, `accessUrl`) | `clients/courses/CourseMaterial.java` | `PUBLISHED` / `DRAFT` / `NOT_AVAILABLE`; solo lo publicado se vincula a un nodo (HU-04 CA2) |
| Todo va por el Gateway | `app.clients.courses.base-url=${GATEWAY_URL}` | Nunca micro a micro directo (`agent.md` §4.1) |

---

## 2. Lo que el spec ya resuelve

No hace falta discutirlo, lo damos por acordado:

| Qué | Dónde en el spec | Para qué nos sirve |
|---|---|---|
| `CohortStatus: DRAFT / ACTIVE / ARCHIVED` | `schemas/CohortStatus` | Es nuestro `Roadmap.archived`: archivado → roadmap y ranking **solo lectura** (RF-CUR-09) |
| `FinalAcademicStatus: PROMOTED / REGULAR / NOT_REGULAR / DROPPED_OUT` | `schemas/EnrollmentResponse` | **Cierra la frontera de `agent.md` §10.5**: el estado académico final es de Courses, no nuestro. Coincide con RF-RNK-10 |
| `EnrollmentStatus: PENDING / VALIDATED / REJECTED` | `schemas/EnrollmentStatus` | "Inscripto y activo" = `VALIDATED` + `active: true`. A confirmar (§3.1) |
| `studentNumber` (legajo) | `CreateEnrollmentRequest` | Lo necesita el resumen exportable por alumno (RF-RNK-13) |
| `professorRole: MANAGER / PROFESSOR / PROFESSOR_READ_ONLY` | `CourseCohortItemResponse` | `PROFESSOR_READ_ONLY` parece ser el **PROFESOR AYUDANTE** de nuestro pendiente #8 |
| Identidad de servicio soportada | `GatewayPrincipalType` + `GatewayServiceId` + `GatewayServiceScopes` | Es el camino que usamos para llamarlos: `X-Principal-Type: service` |
| Baja lógica idempotente | `/course-base/{id}/activate` y `/deactivate` | Coherente con RF-NFR-01 |

---

## 3. Huecos: lo que necesitamos y el spec no tiene

### 3.1 🔴 No hay ninguna lectura de enrollments

Hay `POST /enrollments`, `approve-exception` y `reject`. **No existe un solo `GET`.**

Roadmap necesita responder *"¿el alumno X está matriculado y activo en el cohorte Y?"* en dos
lugares distintos:

- el motivo **`not_enrolled`** del gate `/eligibility` que nos pide el Motor;
- la precondición de `ProgressService.recordResult`: un resultado de un alumno no matriculado se
  descarta como `NonRetryableEventException`.

**Pedimos**: `GET /enrollments?courseCohortId={uuid}&studentId={uuid}` (o
`GET /course-cohorts/{id}/enrollments` paginado), accesible con identidad de **servicio**.

1. ¿Lo pueden exponer? ¿Con qué forma?
2. "Inscripto y activo", ¿es `status = VALIDATED` **y** `active = true`? ¿Qué significa `active`
   cuando el `status` ya es `REJECTED`?

### 3.2 🔴 No hay `GET /course-cohorts/{id}`

`/course-cohorts/me` está scopeado al profesor autenticado (`X-User-Id`). Como servicio no tenemos
forma de leer el `status` de un cohorte → **no podemos evaluar `course_archived`**, ni saber cuándo
el roadmap pasa a solo lectura.

3. ¿Pueden exponer `GET /course-cohorts/{id}` para principal de tipo `service`?

### 3.3 🔴 No existe el catálogo de contenidos

Nuestro cliente pide metadatos de materiales **por lote** (`contentId` → `title`, `type`, `status`)
para dos cosas: validar que un material esté `PUBLISHED` antes de vincularlo a un nodo (HU-04 CA2)
y evaluar el motivo **`content_not_read`** del gate (HU-11). En este spec **no hay ni un endpoint
de contenidos o materiales**.

4. ¿Los materiales son de Courses y todavía no están construidos, o son de **otro grupo**? Esta es
   la pregunta que más nos cambia el plan: si son de otro grupo, el cliente
   `clients/courses/` está mal ubicado.
5. Si son suyos: ¿aceptan un endpoint por lote? Propuesta:
   `POST /api/course/contents/batch` con `{ "contentIds": ["uuid", ...] }` → lista de
   `{ contentId, title, type, status }`. Por lote y no de a uno porque una unidad puede tener
   decenas de materiales y no queremos N llamadas por pantalla.

### 3.4 🔴 No hay eventos

El spec es REST puro. Roadmap necesita **consumir** dos hechos del bus:

| Evento | Para qué | Payload mínimo que necesitamos |
|---|---|---|
| Inscripción validada | Crear la fila de `student_course` (hoy la pueblan los eventos de inscripción; sin ellos el micro no tendría ni un alumno) | `courseCohortId`, `studentId`, `studentNumber`, `status` |
| Cohorte archivado | Pasar el roadmap y el ranking a solo lectura (RF-CUR-09) | `courseCohortId`, `status` |

6. ¿Publican esos eventos? Si no, ¿los pueden agregar? El envelope es el de 6 campos (contratos-kafka v8, snake_case)
   del bus y el topic lo asigna Notificaciones (ver `docs/contracts/bus-notificaciones.md`).
7. Si no hay eventos, la alternativa es que **nosotros** consultemos por REST en cada operación.
   Funciona, pero nos deja sin saber de una baja hasta que el alumno intente algo.

### 3.5 🟠 Nadie escribe `finalAcademicStatus`

Aparece en `EnrollmentResponse` pero **no hay endpoint que lo setee**. El PRD dice que el estado
final lo confirma **manualmente el profe al archivar**, y que nosotros le mostramos el listado de
candidatos P90/P10 con sus condiciones (`agent.md` §3.5).

8. ¿Cómo es el flujo? ¿El profe lo confirma en la UI de Courses y ustedes lo persisten? ¿Nos piden
   los candidatos por REST, o se los publicamos por evento?

---

## 4. Contradicciones a resolver

| # | Qué dice el spec | Qué dice nuestra convención | Impacto |
|---|---|---|---|
| 9 | Base path **`/api/course`** (singular) | Nuestro cliente apunta a `/api/courses` (plural) | Es consistente con `agent.md` §4.2 si su `spring.application.name` es `course-service`. **Confirmarlo y corregir nuestro lado.** Es un cambio de una línea en `application.properties` |
| 10 | `ErrorResponse { status, code, message }` | **Problem Details RFC 7807 con `traceId`** (`agent.md` §4.5) | Uno de los dos está fuera de convención. Afecta cómo parseamos sus errores y cómo se correlacionan las trazas |
| 11 | `X-User-Roles` descrito como *"GESTOR o PROFESOR"* (español), pero el enum del body es `MANAGER / PROFESSOR / PROFESSOR_READ_ONLY` (inglés) | El contrato del Gateway fija `ADMIN`, `MANAGER`, `PROFESSOR`, `STUDENT`. **`GESTOR` no existe** | Inconsistencia dentro del propio spec. Hay que unificar antes de que alguien codee contra el texto |
| 12 | Scope **`MS`** ("mapped to the ROLE_MS authority") | `scope=<destino>.<recurso>.<acción>`, p. ej. `course.enrollments.read` (`agent.md` §4.4) | Si pedimos el token técnico con scope granular, nos van a rechazar. Definir cuál rige |
| 13 | `CookieAuth: fu_at` (cookie HttpOnly) | *"Nunca mandar el JWT de persona, cookies de sesión ni headers sensibles del cliente"* micro a micro (`agent.md` §4.4) | Para nosotros no aplica (vamos por service identity). Confirmar que la cookie es **solo** para el navegador |
| 14 | El cohorte tiene `isActive: boolean` **y** `status: ARCHIVED` | Nosotros tenemos un solo flag `Roadmap.archived` | ¿Cuál define que el roadmap pasa a solo lectura? ¿Pueden coexistir `isActive: true` + `status: ARCHIVED`? |
| 15 | `/course-cohorts/me` declara `X-User-Id` como parámetro `required` del request | El Gateway **inyecta y reemplaza** ese header; el cliente nunca lo manda (`agent.md` §4.4) | Documentarlo como parámetro invita a que alguien lo mande a mano. Sugerencia: moverlo a `securitySchemes`, como ya está |

---

## 5. Fuera de este contrato

- Roles de PROFESOR / PROFESOR AYUDANTE en `X-User-Roles`: es de **Users** (pendiente #8), aunque
  `PROFESSOR_READ_ONLY` de acá es un buen insumo.
- Topic y envelope de los eventos: es de **Notificaciones**
  (`docs/contracts/bus-notificaciones.md`).
- Vidas del alumno: es de **Inventario**.
- Institutions, course bases, códigos de invitación y el flujo de aprobación por excepción: son
  suyos íntegramente. Roadmap no los toca ni los replica.

---

## 6. Qué cerramos con cada respuesta

Tabla para Courses: qué queda habilitado de nuestro lado según qué contesten.

| Si responden | Cerramos | Si no responden |
|---|---|---|
| **P1-2** — lectura de enrollments | El motivo **`not_enrolled`** del gate y la validación real de `recordResult`. Es lo que más nos frena | El gate no puede saber si el alumno está matriculado |
| **P3** — `GET /course-cohorts/{id}` | El motivo **`course_archived`** y el paso a solo lectura (RF-CUR-09) | Un curso archivado sigue aceptando progreso |
| **P4-5** — catálogo de contenidos | El motivo **`content_not_read`** (HU-11) y la validación de vincular solo material `PUBLISHED` (HU-04 CA2). Reemplazamos el doble por el cliente real | `clients/courses/` se queda con el doble para siempre. HU-04 y HU-11 no se pueden integrar |
| **P6-7** — eventos de inscripción y archivado | **Poblar `student_course` con datos reales**. Hoy lo llenan los eventos de inscripción de `courses.events` | En producción Roadmap **no tiene ni un alumno**. Es el bloqueante más serio de los cuatro |
| **P8** — flujo del estado final | El **cierre de curso**: punto **#6 del DoD del MVP** y el resumen exportable (RF-RNK-13) | Calculamos los candidatos P90/P10 pero no hay dónde depositarlos |
| **P9-15** — contradicciones | Integración sin sorpresas: path, formato de error, roles, scopes | Se descubren en el entorno integrado, que es el peor momento |

### Lo que Courses gana

- Roadmap es quien calcula el **XP, el nivel y el ranking por cohorte**. El resumen exportable de
  RF-RNK-13 (legajo, nombre, estado final, XP, insignias) necesita datos de los dos: ustedes ponen
  legajo y estado final, nosotros XP y posición.
- Con **P8** cerrado les podemos entregar los **candidatos a promoción y a pérdida de regularidad**
  (P90/P10 con sus condiciones) para que el profe confirme el estado final con información real.

### Lo mínimo para no frenarnos

**P1 y P6.** Una lectura de enrollments y un evento de inscripción. Con eso Roadmap deja de
depender de la semilla y el gate empieza a funcionar con datos reales.

### Lo que NO depende de ustedes

El grafo del roadmap, los prerrequisitos AND/OR, el ledger de XP, los niveles y el ranking son
dominio nuestro. Están construidos y no esperan a este contrato.

---

## 7. Resolución técnica verificada en el repositorio de Courses (`2026-P4-BE/tpi-course`)

Tras inspeccionar directamente la implementación en `tpi-course` (rama `develop` y PRs #31, #36, #41), se confirmaron los contratos reales:

### 7.1 Base Path y Gateway Routing
- **Base path**: `/api/course` (singular). Configurado en `app.clients.courses.batch-path` y `app.clients.courses.membership-path`.
- Enrutamiento vía API Gateway mediante `${app.api.private-path}` y headers `X-Principal-Type`, `X-User-Id`, `X-User-Roles`.

### 7.2 Validación de Pertenencia y Permisos de Profesor (`HttpCohortOwnershipClient`)
- **Endpoint**: `GET /api/course/course-cohorts/{courseCohortId}/membership`
- **Headers**:
  - `X-Principal-Type: user`
  - `X-User-Id: {professorId}`
  - `X-User-Roles: PROFESSOR`
- **Respuesta**: `200 OK` con `CohortMembershipResponseDto`:
  ```json
  {
    "courseCohortId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "role": "PROFESSOR",
    "canRead": true,
    "canWrite": true
  }
  ```
  Si el profesor no pertenece a la cohorte, Courses responde `403 FORBIDDEN` (o `404 NOT_FOUND` si la cohorte no existe).
- **Implementación en Roadmap**:
  - `HttpCohortOwnershipClient` invoca dicho endpoint. Si `response != null && response.canWrite() == true`, valida la pertenencia y edición.
  - Se cachea con Caffeine (TTL corto, máx. 500 entradas) para no sobrecargar las consultas repetitivas de edición del roadmap.

### 7.3 Sincronización Asíncrona de Matrículas y Cierre de Cohorte (`CoursesEventListener`)
- **Topic**: `courses.events` (configurable vía `app.kafka.topics.courses=${KAFKA_TOPIC_COURSES:courses.events}`).
- **Eventos consumidos**:
  1. `STUDENT_ENROLLED`:
     - Payload (snake_case, v8): `{ enrollment_id, course_cohort_id, student_id, validation_type, enrolled_at }`. Roadmap lee `course_cohort_id` y `student_id`
     - Acción: upsert idempotente en `student_course` (`active = true`, inicializa vidas y XP si es nuevo).
  2. `STUDENT_UNENROLLED`:
     - Payload (snake_case, v8): `{ enrollment_id, course_cohort_id, student_id, reason, performed_by_user_id, unenrolled_at }`. Roadmap lee `course_cohort_id` y `student_id`
     - Acción: marca `active = false` en `student_course` para la cohorte indicada.
  3. `COURSE_COHORT_ARCHIVED`:
     - Payload (snake_case, v8): `{ course_cohort_id, course_base_id, archived_at }`. Roadmap lee `course_cohort_id`
     - Acción: marca `RoadmapEntity.archived = true` en **todos los roadmaps de la cohorte**, pasando el curso y el ranking a solo lectura. Con la cohorte archivada, los cambios de gestión de roadmaps responden `409 course.archived`.

### 7.4 Mapeo y Creación del Roadmap
- **Relación de Identificadores**: El identificador de curso en Roadmap (`courseId`) corresponde exactamente al `courseCohortId` de Courses.
- **Creación On-Demand**: Courses no envía un payload para autogenerar el grafo del roadmap. El roadmap se instancia en Roadmap cuando el profesor a cargo da de alta la primera sección (`POST /api/roadmap/courses/{courseCohortId}/sections`) o crea el primer roadmap (`POST /api/roadmap/courses/{courseCohortId}/roadmaps`).
- **Varios roadmaps por curso (HT-17, HU-57)**: un curso (`courseCohortId`) puede tener **varios roadmaps**; cada uno es un mapa distinto del mismo curso (DEC-017). El primero que se crea queda como **principal** (`is_primary`) y siempre hay uno solo. Las rutas `/api/roadmap/courses/{courseCohortId}/...` resuelven el roadmap principal y las rutas `/api/roadmap/roadmaps/{roadmapId}/...` el roadmap pedido, autorizado contra el curso al que pertenece. Crear más de uno exige que el profesor active `multiple_roadmaps_allowed` en los ajustes del curso (`409 roadmap.multiple-not-allowed` si no).
- **Origen de las unidades (HT-19, T-19.3)**: cada roadmap tiene `section_source`: `COURSE` (por defecto: sus unidades espejan las secciones de Courses) u `OWN` (unidades propias, no se sincronizan). La sincronización de secciones solo toca los roadmaps `COURSE` que no están archivados. *Hoy no hay un endpoint para cambiar `section_source`: todos los roadmaps quedan en `COURSE`.*
- **Validación previa**: Antes de crear o editar cualquier sección o nodo, Roadmap verifica mediante `HttpCohortOwnershipClient` que el profesor posea `canWrite: true` en Courses para dicha cohorte.
- **Mapeo de Nodos**:
  - `THEORY`: vincula lecturas/materiales de Courses mediante `contentId`.
  - `PRACTICE`: vincula desafíos evaluados por el Motor mediante `challengeId`.
- **Evento de Activación emitido por Courses (`COURSE_COHORT_ACTIVATED`)**:
  - Payload (snake_case, v8): `{ course_cohort_id, course_base_id, institution_id, start_date, end_date }`. Roadmap **no reacciona** a este evento (lo ignora).

### 7.5 Tabla de Verificación de Integración Campo por Campo

| Componente | Contrato en `tpi-course` | Implementación en `tpi-roadmap` | Estado |
|---|---|---|---|
| **Base Path** | `/api/course` (singular) | `/api/course` (`application.properties`) | ✅ Verificado 100% |
| **Headers Gateway** | `X-Principal-Type`, `X-User-Id`, `X-User-Roles` | `HttpCohortOwnershipClient` inyecta los 3 headers | ✅ Verificado 100% |
| **Endpoint Membresía** | `GET /api/course/course-cohorts/{id}/membership` | `HttpCohortOwnershipClient` con caché Caffeine | ✅ Verificado 100% |
| **Respuesta Membresía** | `CohortMembershipResponseDto { courseCohortId, role, canRead, canWrite }` | `MembershipResponse { courseCohortId, role, canRead, canWrite }` | ✅ Verificado 100% |
| **Topic Kafka** | `courses.events` | `${app.kafka.topics.courses:courses.events}` | ✅ Verificado 100% |
| **Envelope Kafka** | `EventEnvelope<T> { event_id, event_type, event_version, timestamp, producer, payload }` (snake_case, v8) | `EventEnvelope<T> { event_id, event_type, event_version, timestamp, producer, payload, unknownFields }`; `event_version` debe ser 1, si no va a la DLT | ✅ Verificado 100% |
| **Payload `STUDENT_ENROLLED`** | `{ enrollment_id, course_cohort_id, student_id, validation_type, enrolled_at }` | `StudentEnrolledPayload` (mismos campos y tipos) | ✅ Verificado y mergeado en `develop` (PR #36) |
| **Payload `STUDENT_UNENROLLED`**| `{ enrollment_id, course_cohort_id, student_id, reason, performed_by_user_id, unenrolled_at }` | `StudentUnenrolledPayload` (mismos campos y tipos) | ✅ Verificado 100% |
| **Payload `COURSE_COHORT_ARCHIVED`**| `{ course_cohort_id, course_base_id, archived_at }` | `CourseCohortArchivedPayload` (mismos campos y tipos) | ✅ Verificado 100% |
| **Consulta Matrículas Alumno**| `GET /api/course/enrollments/me` | `StudentCohortEnrollmentDto` | ✅ Mergeado en `develop` (PR #41) |
| **Lote de material** | `GET /course-cohorts/{id}/activities?sectionIds=` para principal de servicio con `course.activities.read` | `HttpCoursesMaterialClient` en `mode=http`; valida el vínculo de un nodo por la sección de la unidad (T-04.2) | ✅ Implementado; el lote incluye `order_index` y `course_section_id` (§7.9) |
| **Catálogo de Contenidos** | Tabla `course_activity` en BD; controller no expuesto aún en `develop` | `CoursesCatalogClient` mockeado (`catalog-mode=stub`) | 🟡 Mockeado en memoria (Fase actual) |
| **Listado de Secciones (servicio)** | `GET /course-cohorts/{id}/sections`: `ROLE_MS` + `course.sections.read`; activas y visibles | `HttpCourseSectionsClient` (M2M, validación del catálogo completo), audience `course-service` | 🟡 Implementado; el scope debe estar habilitado en el entorno integrado |
| **Flujo Cierre de Curso** | `finalAcademicStatus` en DTO; sin endpoint de confirmación | Postergado para fases posteriores | ⏸️ Postergado para otra fase |

### 7.6 Acuerdos y Decisiones para las Siguientes Fases
1. **Flujo de Cierre de Curso (`finalAcademicStatus` / P90-P10 / RF-RNK-10 / RF-RNK-13)**:
   - Se pospone formalmente para una fase posterior.
   - En la fase actual, Roadmap congela el curso y ranking al recibir `COURSE_COHORT_ARCHIVED`, sin enviar notas finales a Courses hasta que se defina el contrato definitivo.
2. **Carga y Catálogo de Contenidos**:
   - Courses expone el material por lote de secciones (P-11.6) y permite subir archivos a una sección; los enlaces y videos llegan con su contenido de cohorte.
   - En Roadmap no queda ningún cliente de material simulado fuera de los tests: el vínculo de un nodo (HU-04, T-04.2) y el detalle del nodo (HU-42) leen el lote real con `CoursesMaterialClient`. El perfil integrado no arranca con `app.clients.course-materials.mode=stub`.
   - **Pendiente**: definir si el material de cohorte sin sección puede vincularse (hoy no: el lote se pide por secciones).

Con esta arquitectura reactiva y desacoplada, Roadmap no requiere polling ni llamadas síncronas bloqueantes para validar alumnos matriculados, eliminando por completo la dependencia en producción de datos sembrados.

### 7.7 Lectura de secciones con identidad de servicio (M2M, no "como alumno")

**Decisión:** Roadmap lee `GET /api/course/course-cohorts/{courseCohortId}/sections` con **token de servicio** (client_credentials), no simulando un alumno.

**Por qué no "como alumno":**
- El token de persona viaja en la cookie `fu_at` (HttpOnly), que solo maneja el navegador; el Gateway rechaza (401 `not-authenticated`) un token de persona enviado en `Authorization` (DEC-03).
- El contrato prohíbe micro-a-micro mandar JWT de persona / cookies (`agent.md §4.4`). `agent.md §4.4`; convención #13 del §4 de este doc.
- Un servicio no tiene `X-User-Id` de persona: el Gateway inyecta `X-Service-Id`/`X-Service-Scopes` desde el JWT y borra los headers de identidad entrantes.
- Roadmap llama en contextos sin request de usuario (sync, jobs, `CoursesLifecycleEventListener`); no hay cookie ni sesión.
- No existe `on_behalf_of`: el Gateway no lo genera (si viniera en el token, solo lo registra en logs).

**Vista acordada para el servicio:** solo secciones **activas y no ocultas** (`isActive=true ∧ isVisible=true`), equivalente a la vista de alumno. **No** las ocultas que ve `GESTOR`/`PROFESSOR`. El servicio no consulta membresía ni matrícula (no tiene usuario).

**Dónde se filtra (decisión):** el filtrado de las secciones ocultas es responsabilidad de **Courses**, no de Roadmap. El listado con principal `service` devuelve únicamente secciones activas y visibles; Roadmap consume esa lista **tal cual** y **no** re-filtra por visibilidad. Si Courses agrega campos como `is_visible`, Roadmap los ignora (binding tolerante a campos desconocidos): no forman parte del contrato del consumidor. Un filtro cliente-side sobre `is_visible` queda fuera de este contrato.

**Scope:** `course.sections.read` → audience `course-service` (`<segment>.<recurso>.<acción>`). Se da de alta en `ScopeCatalog.java` de `tpi-users` y en el cliente `roadmap-service`; el registro ya lo lleva en `tpi-integration.yml`/registry (`needs`). Trámite **P-11.5** (`docs/T-01-7-EUREKA-GATEWAY.md`). El scope `course.activities.read` ya está emitido y Courses expone el listado de actividades; el lote incluye `order_index` y `course_section_id` (§7.9).

**Estado de la implementación en Roadmap:**
- `HttpCourseSectionsClient` lee por servicio y recorre todas las páginas (`totalPages`), valida que los metadatos sean completos y estables, que no haya IDs repetidos ni páginas faltantes, y falla explícitamente si se excede el tope `max-pages` (default 100); ordena por `orderIndex`; `pageSize` máx 50, timeout 2s. `CourseSectionsProperties` exige `tokenAudience` y `tokenScope` cuando `mode=http`.
- Defaults de la app: `COURSES_SECTIONS_CLIENT_MODE=http`, `COURSES_TOKEN_AUDIENCE=course-service`, `COURSES_SECTIONS_TOKEN_SCOPE=course.sections.read`.
- El cliente se selecciona en `mode=stub|http`; en el perfil integrado se exige HTTP. El modo HTTP requiere registrar `course.sections.read` en Gateway/Users/registry antes de usarlo en un entorno compartido.

**Implementación de Courses:** el listado acepta `X-Principal-Type: service` con `hasRole('MS') and hasAuthority('course.sections.read')` y **devuelve solo secciones activas y visibles**: es la fuente del filtrado de ocultas (§7.7, arriba). El camino de usuario no cambia; `403` si falta el scope.

**Grupos y restricciones por sección (T-10.1):** el contrato de lectura de grupos, participantes con `groups[]` y restricciones `GROUP`, con sus scopes de servicio por endpoint, está en [`courses-grupos-t-10-1.md`](courses-grupos-t-10-1.md).

### 7.8 Reconciliación manual de secciones Courses→Roadmap

- Roadmap expone `POST /api/roadmap/courses/{courseId}/sections/sync` solo cuando `app.sections.sync-enabled=true` (default `false`). La reconciliación se aplica a **todos los roadmaps del curso con `section_source = COURSE` que no están archivados**; los de unidades propias (`OWN`) no se tocan. Si el curso todavía no tiene ningún roadmap y Courses tiene secciones, se crea el principal; si no tiene roadmaps y Courses no devuelve secciones, responde `404 roadmap.not-found`; si tiene roadmaps pero todos son `OWN`, no hay nada que sincronizar.
- Puede ejecutarlo un ADMIN o el profesor dueño de la cohorte. Un roadmap archivado responde `409`; Courses se consulta antes de abrir la transacción local y una respuesta incompleta/indisponible no modifica el grafo.
- Las secciones ya vinculadas se reconcilian por UUID Courses: altas, renombres y posiciones actualizan únicamente la entidad sección; nodos, aristas y progreso se conservan. `orderIndex` de Courses es cero-based y se traduce a `sortOrder` uno-based.
- HU-17: cuando una sección desaparece del catálogo activo (o se inactiva), Roadmap da de baja lógica la unidad, sus nodos y sus aristas (RF-NFR-01), sin borrar el progreso ya alcanzado (`completed_node`, `content_reading`, `xp_movement`, G10-E1). Si Courses vuelve a publicar la sección, la unidad se reactiva con sus nodos en lugar de crear una nueva. Una lista vacía de secciones no da de baja nada (guard T-36.7).
- Para roadmaps antiguos, una unidad sin UUID se vincula solo si coinciden exactamente el nombre normalizado y la posición con una sección activa de Courses. Si hay más de una coincidencia, se responde `409` y se exige revisión; no se asignan IDs por aproximación.
- La lectura M2M requiere registrar `course.sections.read` en Gateway/Users/registry (P-11.5) antes de habilitar la llamada HTTP en un entorno compartido.
- Cada sincronización registra actor, cohorte, hora, conteos de altas/vínculos/renombres/orden y fallos; los logs no incluyen tokens. Los rechazos HTTP 401 consecutivos de Courses emiten alerta al llegar a `app.sync.courses.token-rejection-alert-threshold` (default `3`) dentro de 15 minutos; una lectura completa exitosa reinicia la ventana.

### 7.9 Comisiones (grupos) y restricciones legibles por servicio (M2M)

Este apartado **no duplica** el contrato de lectura de comisiones y restricciones. La fuente de endpoints,
campos, semántica y errores es el acta **T-10.1**
[`courses-grupos-t-10-1.md`](courses-grupos-t-10-1.md) (§3 y §6.2). Acá solo se registran la decisión y
los scopes.

**Decisión:** Roadmap lee comisiones y restricciones con **token de servicio** (client_credentials) por
**pull (M2M)**, nunca con JWT de persona ni cookie `fu_at` (mismo criterio que §7.7). No se espera un
evento del bus.

**Decisión de producto (08/10, HU-44/HT-10):** **un alumno puede pertenecer a varias comisiones a la
vez**. Reemplaza **P-29/D-02** y deja **obsoleto** el punto 4 de P-11.7 (`tpi-course` [#59](https://github.com/2026-P4-BE/tpi-course/issues/59), «un grupo activo por alumno y cohorte»); ver la nota de obsolescencia en [`docs/P-11-5-issues.md`](../P-11-5-issues.md). Roadmap maneja **0..N** comisiones por alumno.

**Scopes H1** (tabla final en el acta §6.2): `course.groups.read` (grupos/comisiones),
`course.enrollment.read` (participantes con su `groups[]`), `course.sections.read` (secciones),
`course.restrictions.read` (restricciones de sección **y** de actividad/nodo) y `course.activities.read`
(orden/material de actividades), todos con audience `course-service`. La sincronización de unidades
consume `course.activities.read` para leer `order_index`/`course_section_id` y reflejar el orden en el
`sort_order` de los nodos vinculados por `content_id`/`challenge_id` (acta §3.5; best-effort, no bloquea
la sincronización).

**Estado de los scopes.** Los cinco scopes H1 están emitidos en el registry y en el catálogo de
scopes —`offers` de `course-service` y `needs` de `roadmap-service` en `registry/services.yml`, con
`USERS_SCOPE_CATALOG` regenerado
([`tpi-system-compose#137`](https://github.com/2026-P4-BE/tpi-system-compose/issues/137), cerrado)— y
Courses **acepta los scopes dedicados** `course.groups.read` y `course.restrictions.read`, además de
los genéricos que ya aceptaba. `course.activities.read` ya se consume para el lote de material y el
lote M2M de actividades incluye `order_index` y `course_section_id` (`tpi-course`
[#84](https://github.com/2026-P4-BE/tpi-course/issues/84), implementado).

**Restricciones de actividad/nodo.** El endpoint
`GET /api/course/course-activities/{courseActivityId}/restrictions` está implementado con el scope
`course.restrictions.read`, con el mismo envelope que las restricciones de sección (acta §3.4.1). El
modelo de datos ya soportaba el target (`content_restriction_set`, migración V12).
