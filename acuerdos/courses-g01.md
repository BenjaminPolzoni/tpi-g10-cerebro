---
tags: [tpi, g10, acuerdo, courses, g01]
fecha: 2026-10-08
grupos: [G10, G01]
estado: vigente  # acta T-10.1 implementada en Courses; validación formal de ambos grupos pendiente
contrato: "tpi-roadmap/docs/contracts/courses-grupos-t-10-1.md"
---

# Acuerdo con Courses (G01): cohortes, secciones, comisiones y restricciones

> [!info] Fuentes
> - `tpi-roadmap/docs/contracts/courses.md` ([GitHub](https://github.com/2026-P4-BE/tpi-roadmap/blob/develop/docs/contracts/courses.md)): base path, M2M, secciones, sync, scopes.
> - `tpi-roadmap/docs/contracts/courses-grupos-t-10-1.md` ([GitHub](https://github.com/2026-P4-BE/tpi-roadmap/blob/develop/docs/contracts/courses-grupos-t-10-1.md)): acta T-10.1 (comisiones y restricciones, ampliación H1).
> - `tpi-roadmap/docs/contracts/contrato-cursos.txt` ([GitHub](https://github.com/2026-P4-BE/tpi-roadmap/blob/develop/docs/contracts/contrato-cursos.txt)): OpenAPI original de Courses (histórico; documenta `CookieAuth fu_at`).
> - Repo de la contraparte: `2026-P4-BE/tpi-course` (issues #57, #58, #59, #84, #88).

## Qué se acordó
- **`courseId` de Roadmap = `courseCohortId` de Courses.** Roadmap trabaja siempre a nivel cohorte, nunca a nivel `courseBase`.
- Roadmap **solo lee** de Courses: nunca crea ni asigna grupos, membresías ni restricciones. Solo `PROFESSOR`/`MANAGER` asignan comisión.
- Todo va **por el API Gateway**, con **token de servicio** (`client_credentials`), nunca con JWT de persona ni cookie `fu_at`.
- **Un alumno puede pertenecer a varias comisiones a la vez** (decisión de producto del 2026-10-08, HU-44/HT-10). Reemplaza P-29/D-02 y deja obsoleto el punto 4 de `tpi-course#59`. Roadmap maneja 0..N comisiones por alumno. Ver [[decisiones/DEC-014-comisiones-modelo-b-evaluacion-en-roadmap|DEC-014]].
- El ID de comisión es un **UUID estable**; Roadmap relaciona por `id`, nunca por `name`.
- **No hay evento Kafka de cambio de grupo** por ahora: Roadmap consulta el estado vigente por pull.
- Las restricciones de sección y de actividad/nodo se **leen por pull** y **Roadmap las evalúa** con su propio progreso y los grupos del alumno ("opción R"). Courses no evalúa por alumno.
- El filtrado de secciones ocultas es responsabilidad de **Courses**: el listado con principal de servicio devuelve solo secciones `isActive ∧ isVisible`. Roadmap las consume tal cual.
- Courses acepta los scopes dedicados `course.groups.read` y `course.restrictions.read` además de los genéricos (`tpi-course#84`, implementado).

## Quién lo acordó
- G10: equipo Roadmap (docs y código en `tpi-roadmap`).
- G01: equipo Courses and Enrollment (`tpi-course`). Informaron además la denominación "MS3" para el principal de servicio; **no es verificable en código** y el acta no depende de ella.
- Aprobación formal: la tabla de validación del acta (§11) está **vacía** para ambos grupos (sin responsable ni fecha).

## Contrato técnico

Base path de Courses: `/api/course` (singular), siempre vía Gateway. Audience de los tokens: `course-service`. Headers que llegan a Courses: `X-Principal-Type: service`, `X-Service-Id`, `X-Service-Scopes` (incluye `MS` más el scope del endpoint). Sin scope: `403`.

### Lo que consumimos (REST, Roadmap → Courses)

| Método y ruta | Scope | Para qué | Cliente en Roadmap |
|---|---|---|---|
| `GET /api/course/course-cohorts/{courseCohortId}/sections` | `course.sections.read` | Unidades/secciones activas y visibles (paginado, `pageSize` máx 50). Sync HU-36/17 | `HttpCourseSectionsClient` |
| `GET /api/course/course-cohorts/{courseCohortId}/groups` | `course.groups.read` | Comisiones activas (array sin paginar) | `HttpCourseGroupsClient` |
| `GET /api/course/course-cohorts/{courseCohortId}/participants?role=STUDENT&page=&size=` | `course.enrollment.read` | Alumnos con su `groups[]`; también fallback de matrícula del gate (HU-48) | `HttpCourseGroupsClient`, `HttpCourseParticipantsClient` |
| `GET /api/course/course-sections/{courseSectionId}/restrictions` | `course.restrictions.read` | Restricciones de sección | `HttpCourseRestrictionsClient` |
| `GET /api/course/course-activities/{courseActivityId}/restrictions` | `course.restrictions.read` | Restricciones de actividad/nodo (§3.4.1) | `HttpCourseRestrictionsClient` |
| `GET /api/course/course-cohorts/{courseCohortId}/activities?sectionIds=...` | `course.activities.read` | Material por lote; incluye `order_index` y `course_section_id` | `HttpCoursesMaterialClient` |
| `GET /api/course/course-cohorts/{courseCohortId}/teaching-memberships/{userId}` | `course.teaching-membership.read` | Pertenencia docente M2M (HU-47) | `HttpCohortOwnershipClient` |

> [!note] Dónde viven los defaults
> Rutas, scopes, timeouts (2 s) y caches están en `application.properties` (`app.clients.course-*`). Los cinco scopes H1 están declarados como `needs` de `roadmap-service` en `tpi-integration.yml`.

### Formato
- Grupos, participantes y restricciones van en `snake_case` (`course_cohort_id`, `user_id`, `total_pages`, `on_unmet`, `cohort_group_id`); el lote de material también se lee en snake_case (`418744e`, 2026-10-06).
- El listado de **secciones** viaja en camelCase (`totalPages`, `orderIndex`, `isActive`); Roadmap fija esos nombres con `@JsonProperty` (`9dee26e`, 2026-10-05).
- Errores de Courses: `{ "status", "code", "message" }` (no es Problem Details). Códigos: 400 UUID inválido, 401, 403, 404 (`Course Cohort not found` / `Course Section not found`).
- Restricciones: `{ operator: ALL|ANY, on_unmet: HIDDEN|LOCKED, conditions[] }`. `conditions[].type`: `DATE` (`from`, `until`), `GROUP` (`cohort_group_id`), `SECTION_COMPLETED` (`required_section_id`). Máximo 10 condiciones. Sin configuración: `ALL`, `LOCKED`, `[]`.
- Semántica `DATE`: apertura inclusiva, cierre exclusivo, zona `America/Argentina/Buenos_Aires` (`app.clients.course-restrictions.date-zone`).

### Eventos (Kafka `courses.events`, Courses → Roadmap)
| `event_type` | Efecto en Roadmap |
|---|---|
| `STUDENT_ENROLLED` | Upsert idempotente de `student_course` (activo; inicializa XP/vidas si es nuevo) |
| `STUDENT_UNENROLLED` | `student_course.active = false` |
| `COURSE_COHORT_ARCHIVED` | `roadmap.archived = true` (roadmap y ranking en solo lectura, RF-CUR-09) |
| `COURSE_COHORT_ACTIVATED` | Roadmap no reacciona |

Courses escribe el wire v8 en snake_case (`KafkaEventWire`, verificado en `docs/T-191-KAFKA-V8-CUTOVER.md`). Ver [[acuerdos/notificaciones-bus|bus de eventos]] y [[decisiones/DEC-001-wire-kafka-v8-snake-case|DEC-001]].

> [!question] Verificar
> `courses.md` §7.3 todavía muestra los payloads en camelCase (`courseCohortId`, `enrolledAt`). Tras #191 Roadmap lee solo snake_case. Confirmar con un evento real de G01. **G5 (2026-10-15): todo en snake_case.**

### Lo que exponemos a Courses
Nada específico. El front de Courses no nos consume por contrato. Roadmap expone el sync manual `POST /api/roadmap/courses/{courseId}/sections/sync` (ADMIN, GESTOR o profesor dueño) **solo con `SECTIONS_SYNC_ENABLED=true`**.

## Impacto en nuestro código
- `com.utn.tpi.roadmap.clients.courses.*`: un cliente HTTP por endpoint, con `Properties`, `Config` (modo `http`/`stub`) y excepción `*UnavailableException` (503 Problem Details).
- `CourseSectionSyncService`, `CourseSectionsReconciliationService`: sync de unidades; baja lógica y reactivación; guard contra lista vacía (T-36.7); regla (c).
- `services/groups/*`: `GroupVisibilityRules`, `GroupUnitsService`, `GroupAccessService`, `UnitRestrictionRules`, `NodeVisibilityScope`, `GroupProgressService`.
- `GateEvaluator` / `GateService`: motivos `group_restricted` y `date_restricted` (ver [[acuerdos/motor-desafios-g09|Motor]]).
- `GraphValidator` + `PrerequisiteGraphService`: regla (c), 409 `node.prerequisite-out-of-scope`.
- `events/CoursesLifecycleEventListener`: `courses.events`.
- `EnrollmentResolver` / `CourseCohortSyncService`: matrícula, con fallback pull de participantes.

## Pendiente / próximos pasos
- [ ] **HU-49 (restricciones de Courses): bloqueada por G01.** El back aplica `DATE` y `GROUP`, pero falta traducir `HIDDEN` vs `LOCKED`, el evento de cambio y el aviso. El acta §10 deja "cómo traduce Roadmap `HIDDEN` y `LOCKED`" como punto abierto.
- [ ] Definir con G01 un **evento de cambio de grupo/restricción** (hoy no existe; solo pull).
- [ ] Firma formal del acta T-10.1 (G01 y G10).
- [ ] Cerrar `tpi-course#88` ("Alinear contrato de grupos tras PR #86").
- [ ] Cierre de curso / `finalAcademicStatus` (P90/P10, RF-RNK-10/13): **postergado**; hoy solo se congela el roadmap al archivar. **P15 (2026-10-15): entra en el Sprint 3.**
- [ ] Definir si el material de cohorte **sin sección** puede vincularse (hoy no: el lote se pide por secciones).
- [ ] Condiciones `SECTION_COMPLETED`: no se evalúan en el Gate.
- [ ] Encender `SECTIONS_SYNC_ENABLED` y `ROADMAP_BY_GROUP_ENABLED` en los entornos de la demo. Ver [[decisiones/DEC-004-flags-apagados-por-defecto|DEC-004]].

> [!warning] Riesgos
> - Con `ROADMAP_BY_GROUP_ENABLED=false` (default) el gate no emite `group_restricted`/`date_restricted` y HU-44/45 no se ven.
> - Cada evaluación de una unidad con restricciones hace llamadas a Courses (sin caché en el gate); si Courses no responde, el gate devuelve `503`, nunca `eligible=true`.
> - El front no tiene selector de comisión (HU-44) según la auditoría de Sprint 3.

> [!question] Verificar
> Roles: Courses describe `X-User-Roles` como "GESTOR o PROFESOR" en español y el enum del body como `MANAGER/PROFESSOR/PROFESSOR_READ_ONLY`. Roadmap usa `GESTOR` desde #188. **G6 (2026-10-15):** no va a haber roles sino permisos; mientras tanto vale `PROFESSOR`/`GESTOR`.

## Historial
- 2026-09-24: primer contrato `courses.md` (eventos de matrícula, membresía docente, material).
- 2026-10-04: lectura M2M de secciones (`course.sections.read`, P-11.5).
- 2026-10-06: sync de secciones Courses a Roadmap (HU-36), flag apagado por defecto.
- 2026-10-08: acta T-10.1 (grupos y restricciones) + ampliación H1 (scopes dedicados, restricciones de actividad, `order_index`).
- 2026-10-10: baja y reactivación de unidades en el sync (HU-17); restricción de actividad/nodo por comisión (HU-44).
- 2026-10-12: Gate evalúa `DATE` y emite `date_restricted` (gate v1.3).
- 2026-10-14: nota creada desde `origin/develop` (`57ff06a`).
- 2026-10-15: respuestas en [[sprints/sprint-3/08-dudas|08-dudas]]: eventos en snake_case (G5); el profesor elige por roadmap secciones de Courses o propias (P3) y define las restricciones de cada roadmap, que se copian al clonarlo (G4); la ventana horaria de los exámenes la publica Courses (P9).
