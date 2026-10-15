# Acta T-10.1 — Contrato de grupos Roadmap ↔ Courses

Estado: **ACORDADO e IMPLEMENTADO en Courses; pendiente de validación formal de ambos grupos.**

> **Ampliación H1 (2026-10-08), implementada en Courses.** Esta acta fija los scopes dedicados por
> endpoint (§6.2), el orden de actividades (§3.5), las decisiones de integración del lado de Roadmap
> (§3.6) y la restricción de actividad/nodo (§3.4.1).
>
> Courses **acepta los scopes dedicados** `course.groups.read` y `course.restrictions.read`,
> **expone** las restricciones de actividad/nodo (§3.4.1) y el lote de actividades incluye
> `order_index` y `course_section_id` (§3.5). Son los cambios del pedido `tpi-course#84`, ya
> implementados en Courses. Los scopes dedicados ya estaban emitidos en el registry y en el catálogo
> de scopes ([`tpi-system-compose#137`](https://github.com/2026-P4-BE/tpi-system-compose/issues/137),
> cerrado).

| | |
|---|---|
| Consumidor | Roadmap (G10) — `2026-P4-BE/tpi-roadmap` |
| Proveedor | Courses and Enrollment (G01) — `2026-P4-BE/tpi-course` |
| Fecha del acta | 2026-10-08 |
| Verificado contra | `tpi-course`, rama `develop`, commit `4b51350` (2026-10-08), posterior al PR #86; la ampliación H1 es según `tpi-course#84` y no se re-verificó en un commit de `tpi-course` |
| Seguimiento en Courses | Issue `2026-P4-BE/tpi-course#84` (implementado en Courses) |
| Contrato base | `docs/contracts/courses.md` (base path, Gateway, token de servicio, secciones) |

Cada afirmación de este documento tiene uno de dos orígenes, y se indica cuál:

- **Acordado con G01**: decisión funcional confirmada por G01.
- **Verificado en código**: comportamiento leído en `tpi-course` en el commit indicado. No se ejecutó
  la aplicación ni sus tests.
- **Implementado en Courses (H1)**: puntos marcados así reflejan los cambios de Courses para la
  ampliación H1 (`tpi-course#84`: scopes dedicados, restricciones de actividad/nodo, `order_index` y
  `course_section_id`); no se re-verificaron contra un commit de `tpi-course` en esta acta.

Rutas de `tpi-course` abreviadas: `J/` = `src/main/java/ar/edu/utn/frc/tup/p4/`,
`T/` = `src/test/java/ar/edu/utn/frc/tup/p4/`.

---

## 1. Decisiones acordadas con G01

1. Una matrícula puede pertenecer a **varios grupos activos a la vez**.
2. Roadmap trabaja con **`groups[]`**; no asume un único grupo por matrícula.
3. El identificador de grupo es un **UUID estable**: no cambia.
4. Roadmap obtiene los datos con los endpoints de §3.
5. **No hay evento Kafka** de cambio de grupo por ahora.
6. Roadmap obtiene el estado actual **consultando a Courses**.
7. Roadmap consume con principal de servicio, con los scopes por endpoint de §6.2.

Además, G01 mencionó la denominación "MS3" para el principal de servicio. No es verificable en código
y no forma parte del contrato técnico (ver §6.3).

Roadmap solo lee: nunca crea, modifica ni da de baja grupos, membresías o restricciones.

---

## 2. Modelo

### 2.1 Pertenencia múltiple

- La membresía vincula una **matrícula** (`enrollment_id`) con un grupo, no un alumno con un grupo.
- Una matrícula puede tener cero, una o varias membresías activas.
- `group_id` y `group_name` del participante están **deprecados** en el OpenAPI de Courses y solo se
  completan cuando la matrícula tiene exactamente un grupo. Roadmap no los usa.

Verificado en código:

- Índice único parcial `uq_cohort_group_member_active` sobre `(cohort_group_id, enrollment_id)`
  con `is_active = TRUE` (`V1__create_lms_schema.sql`): impide repetir el mismo par, no limita la
  cantidad de grupos por matrícula.
- `CohortParticipantService.assignParticipantGroup` agrega un grupo sin quitar los demás.
- Tests: `CohortParticipantServiceTest.assignParticipantGroup_preservesOtherActiveMemberships`,
  `participantListReturnsStudentOnceWithAllGroups`.

### 2.2 Identificador de grupo

| | |
|---|---|
| Campo | `id` |
| Tipo | UUID |
| Entidad / tabla | `J/entities/CohortGroup.java` / `cohort_group` |
| Alcance | Un grupo pertenece a una sola cohorte (`course_cohort_id`) |

Aparece como `id` en `CohortGroup` y en `participants[].groups[]`, y como `cohort_group_id` en las
condiciones de restricción.

Roadmap relaciona por `id`, nunca por `name`: el nombre es descriptivo.

Verificado en código: no existe endpoint ni lógica que modifique el `id`, renombre, borre o desactive
un grupo; solo existen el alta y el listado.

### 2.3 Identificadores de alumno

En el listado de participantes, para un alumno:

- `id` = identificador de la **matrícula** (`enrollmentId`);
- `user_id` = identificador del **alumno** (`studentId`).

Mapeo ya vigente: el `courseId` de Roadmap es el `courseCohortId` de Courses (`courses.md`).

---

## 3. Endpoints

Base path `/api/course`, siempre a través del Gateway. Los nombres de campo van en `snake_case`.

### 3.1 Grupos de la cohorte

`GET /api/course/course-cohorts/{courseCohortId}/groups`

- Path param: `courseCohortId` (UUID). Sin query params.
- `200`: array **sin paginar** con todos los grupos **activos** de la cohorte, ordenados por nombre.

```json
[
  { "id": "8b1f0c5e-2a4d-4e3b-9f1a-0c7d5e2a1b34", "course_cohort_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "name": "2W1" },
  { "id": "c2d9e7a1-5b6f-4c8d-a3e2-1f0b9d8c7a65", "course_cohort_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "name": "2W2" }
]
```

Scope de servicio: `course.groups.read` (H1, §6.2).

Código: `CourseCohortsApiController.getCourseCohortGroups`, `CohortGroupService.list`, `CohortGroupDto`.

### 3.2 Alumnos de la cohorte y sus grupos

`GET /api/course/course-cohorts/{courseCohortId}/participants?role=STUDENT&page={n}&size={m}`

| Parámetro | Tipo | Nota |
|---|---|---|
| `courseCohortId` | path, UUID | |
| `role` | query, opcional | `STUDENT` para traer solo alumnos. **El nombre es `role`**: cualquier otro nombre se ignora y la respuesta incluye también al cuerpo docente |
| `page` | query, opcional | Base 0, default 0 |
| `size` | query, opcional | Default 20, máximo 100 |
| `search` | query, opcional | No lo usa Roadmap |

`200`: página de participantes.

```json
{
  "content": [
    {
      "id": "e1a2b3c4-0000-4000-8000-000000000001",
      "user_id": "a9b8c7d6-0000-4000-8000-000000000002",
      "role": "STUDENT",
      "status": "VALIDATED",
      "groups": [
        { "id": "8b1f0c5e-2a4d-4e3b-9f1a-0c7d5e2a1b34", "course_cohort_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "name": "2W1" },
        { "id": "c2d9e7a1-5b6f-4c8d-a3e2-1f0b9d8c7a65", "course_cohort_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "name": "2W2" }
      ]
    },
    {
      "id": "e1a2b3c4-0000-4000-8000-000000000003",
      "user_id": "a9b8c7d6-0000-4000-8000-000000000004",
      "role": "STUDENT",
      "status": "VALIDATED",
      "groups": []
    }
  ],
  "page": 0,
  "size": 100,
  "total_elements": 2,
  "total_pages": 1
}
```

Campos que usa Roadmap:

| Campo | Significado |
|---|---|
| `content[].id` | `enrollmentId` |
| `content[].user_id` | `studentId` |
| `content[].status` | Estado de la matrícula: `PENDING`, `VALIDATED` o `REJECTED` |
| `content[].groups[]` | Grupos activos de la matrícula; `[]` si no tiene ninguno |
| `total_pages` | Para recorrer todas las páginas |

Notas verificadas en código:

- El listado incluye toda matrícula activa **sea cual sea su `status`**; no filtra por `VALIDATED`.
- El wrapper trae además `page_size` y `total`, duplicados de `size` y `total_elements`.
- Los ejemplos omiten campos que Roadmap no usa (`first_name`, `last_name`, `full_name`, `email`,
  `enrolled_datetime`, `last_connection_datetime`, `group_id`, `group_name`).

Scope de servicio: `course.enrollment.read`. Este endpoint **no** acepta `course.sections.read`.

Código: `CourseCohortsApi` (parámetros), `CohortParticipantService.getParticipants`,
`EnrollmentRepository.findCohortParticipants`, `CohortParticipantDto`, `CohortParticipantPageResponseDto`.

### 3.3 Secciones de la cohorte

`GET /api/course/course-cohorts/{courseCohortId}/sections`

Sin cambios respecto de `docs/contracts/courses.md` §7.7: con principal de servicio devuelve solo
secciones activas y visibles, paginadas. La respuesta no incluye restricciones.

Scope de servicio: `course.sections.read`.

### 3.4 Restricciones de una sección

`GET /api/course/course-sections/{courseSectionId}/restrictions`

- Path param: `courseSectionId` (UUID). Sin query params.
- `200`: configuración de restricciones de la sección.

```json
{
  "operator": "ANY",
  "on_unmet": "HIDDEN",
  "conditions": [
    { "type": "GROUP", "cohort_group_id": "8b1f0c5e-2a4d-4e3b-9f1a-0c7d5e2a1b34" },
    { "type": "GROUP", "cohort_group_id": "c2d9e7a1-5b6f-4c8d-a3e2-1f0b9d8c7a65" }
  ]
}
```

| Campo | Valores |
|---|---|
| `operator` | `ALL`, `ANY` |
| `on_unmet` | `HIDDEN`, `LOCKED` |
| `conditions[].type` | `DATE`, `GROUP`, `SECTION_COMPLETED` |
| `conditions[].cohort_group_id` | UUID del grupo; solo en condiciones `GROUP` |
| `conditions[].from`, `until` | Solo en condiciones `DATE` |
| `conditions[].required_section_id` | Solo en condiciones `SECTION_COMPLETED` |

- Máximo 10 condiciones por sección.
- Una sección sin configuración guardada responde el valor por defecto: `ALL`, `LOCKED`, `conditions: []`.
- La consulta es **por sección**. Se acuerda que Roadmap lista las secciones (§3.3) y consulta las
  restricciones de cada una; no se exige una lectura por lote.

Scope de servicio: `course.restrictions.read` (H1, §6.2).

Código: `CourseSectionsApiController.getSectionRestrictions`, `SectionRestrictionService.get`,
`SectionRestrictionMapper`, `SectionRestrictionConfigurationDto`, `RestrictionConditionDto`.

### 3.4.1 Restricciones de una actividad/nodo

`GET /api/course/course-activities/{courseActivityId}/restrictions`

> **Implementado en Courses.** Expuesto con principal de servicio y scope `course.restrictions.read`.
> El modelo de datos lo soporta —`content_restriction_set` (migración **V12**) admite el target
> `course_activity_id`— y la exposición REST ya está disponible (pedido `tpi-course#84`).

- Path param: `courseActivityId` (UUID). Sin query params.
- `200`: configuración de restricciones de la actividad, con el **mismo envelope** que §3.4
  (`operator`, `on_unmet`, `conditions[]`), evaluado por la misma lógica de restricciones.
- Exposición **por endpoint**, no por lote.

Scope de servicio: `course.restrictions.read` (H1, §6.2).

Código: mismo servicio de restricciones que §3.4 (`SectionRestrictionService.get`), sobre el
target `course_activity_id`.

### 3.5 Orden de actividades

> **Implementado en Courses.** El lote M2M de actividades incluye `order_index` y
> `course_section_id` por ítem, además de `id`, `title`, `type`, `publication_status`, `access_url` y
> `access_url_expires_at` (pedido `tpi-course#84`).

Integración de Roadmap:

- Cada actividad del lote trae `order_index` y `course_section_id`.
- Roadmap **sincroniza el orden de sus nodos** desde `order_index` (dentro de cada `course_section_id`).
- El orden de la sección se resuelve primero y el orden de la actividad/nodo después (ver §3.6).

Scope de servicio: `course.activities.read` (§6.2).

### 3.6 Notas de integración del lado de Roadmap

Estas notas describen cómo consume Roadmap; **no alteran el contrato de Courses** de §1–§5.

- **Modelo B (un roadmap por cohorte, vista por comisión).** Roadmap mantiene **un `roadmap` por
  cohorte** (`courseCohortId`). La "vista por comisión" es un **filtro** sobre ese roadmap: el alumno
  que pertenece a varias comisiones elige cuál ve. Roadmap no crea un roadmap por grupo.
- **Orden de sección y de nodo.** La restricción de **SECCIÓN** se evalúa primero y la de **NODO**
  después. El orden de nodos se sincroniza desde `order_index` / `course_section_id` de §3.5.
- **Regla (c) de prerrequisitos — implementada en Roadmap.** Un prerrequisito **no puede quedar
  fuera del scope de visibilidad del nodo que lo exige**: la validación es **transitiva** en el
  editor de Roadmap (`GraphValidator` combina el cierre transitivo de `PrerequisiteGraphService` con
  el alcance `NodeVisibilityScope` de la sección y la actividad; 409 `node.prerequisite-out-of-scope`)
  y se **re-valida en el sync** (`CourseSectionSyncService` da de baja lógica las aristas vigentes que
  quedaron fuera de alcance). Las condiciones `DATE` **no** restringen el scope de visibilidad; las de
  `GROUP` sí, con la semántica de `GroupVisibilityRules` (`ANY`/`ALL`). Con el flag
  `roadmap-by-group` apagado no hay alcance que validar; si Courses no responde, el editor no guarda
  la arista (503).
- **Restricciones por PULL.** Courses **expone la configuración** (solo lectura) de las restricciones de
  sección (§3.4), de actividad/nodo (§3.4.1) y **por lote** por cohorte; Roadmap las consulta
  por pull, no por evento.
- **Evaluación del lado de Roadmap (opción R).** Courses **no evalúa por alumno**: no expone ningún
  endpoint con `studentId`. Roadmap evalúa `DATE`/`GROUP`/`SECTION_COMPLETED` con **su propio progreso**
  de nodos y los **grupos del alumno** (obtenidos de §3.2), y aplica `HIDDEN`/`LOCKED`. Semántica: `DATE`
  con **apertura inclusiva y cierre exclusivo**; `operator` `ALL`/`ANY` sobre **todas** las condiciones
  de la sección/actividad.
- **Asignación de comisiones solo humana.** Solo `PROFESSOR`/`MANAGER` (Gestor) asignan el grupo de cada
  alumno; Roadmap **solo lee**, nunca asigna ni mueve comisiones. El principal de servicio es de solo lectura.

---

## 4. Reglas GROUP

Semántica real de Courses (`J/services/restrictions/SectionRestrictionEvaluator.evaluate`):

| Caso | Resultado |
|---|---|
| Sin configuración o `conditions: []` | No hay restricción: acceso concedido |
| `ANY` | Alcanza con cumplir una condición |
| `ALL` | Deben cumplirse todas las condiciones |
| Alumno sin grupos | No cumple ninguna condición `GROUP` |
| Alumno en varios grupos | Cada condición `GROUP` se evalúa por separado contra sus membresías activas |

- Una condición `GROUP` se cumple cuando la matrícula tiene una membresía activa en ese grupo y el
  grupo está activo (`CohortGroupMemberRepository.hasActiveMembershipInActiveGroup`).
- Una sección restringida a varios grupos se expresa con una condición `GROUP` por grupo.
- Courses evalúa restricciones solo para matrículas activas en estado `VALIDATED`.
- El operador se aplica sobre **todas** las condiciones de la sección, no solo sobre las `GROUP`.

Tests de Courses: `SectionRestrictionEvaluatorTest.groupRestrictionGrantsOnlyStudentsWithAnActiveMembership`,
`CourseSectionsApiControllerTest.savesAndReopensDateAndGroupRestrictions`,
`rejectsAGroupFromAnotherCohortAndReadOnlyWrites`.

---

## 5. Actualización ante cambios de grupo

- No existe evento de alta, cambio o baja de grupo en `courses.events`
  (`J/events/CourseEventTypes.java` no define ninguno).
- Roadmap obtiene el estado vigente volviendo a consultar §3.1 y §3.2.
- Courses no expone fecha de actualización, versión ni ETag para grupos o membresías. La columna
  `cohort_group_member.last_updated_datetime` existe en la base y no viaja en ningún DTO.
- El momento y la frecuencia de la consulta son decisión de Roadmap y se definen en la implementación.

Este mecanismo es el vigente "por ahora". Si Courses publica un evento más adelante, se incorpora con
una revisión de esta acta.

---

## 6. Autenticación técnica

### 6.1 Mecanismo

El mismo de `docs/contracts/courses.md` §7.7:

- Roadmap pide un token de servicio y llama a través del Gateway. Audience `course-service`.
- Courses no valida el token: confía en los headers que inyecta el Gateway
  (`J/security/GatewayAuthenticationFilter.java`, `J/security/IdentityHeaders.java`).

| Header | Valor |
|---|---|
| `X-Principal-Type` | `service` |
| `X-Service-Id` | identificador del servicio llamador |
| `X-Service-Scopes` | lista separada por comas; debe incluir `MS` y el scope del endpoint (§6.2) |

Courses convierte el valor `MS` en la authority `ROLE_MS` y deja cada scope como authority.

### 6.2 Scopes por endpoint

Tabla final H1 — un **scope dedicado por recurso**:

| Endpoint | Scope de servicio requerido |
|---|---|
| `GET .../groups` (§3.1) | `course.groups.read` |
| `GET .../participants` (§3.2) | `course.enrollment.read` |
| `GET .../sections` (§3.3) | `course.sections.read` |
| `GET .../restrictions` de sección (§3.4) | `course.restrictions.read` |
| `GET .../restrictions` de actividad/nodo (§3.4.1) | `course.restrictions.read` |
| lote M2M de actividades (§3.5) | `course.activities.read` |

En todos los casos se exige además la authority `MS`. Sin el scope del endpoint, Courses responde `403`.

Esta tabla reemplaza, para el consumo de Roadmap, los scopes genéricos previos
(`course.sections.read` y `course.enrollment.read`) como scope de §3.1 y §3.4 por los scopes
**dedicados**. Courses, de su lado, suma los dedicados **sin quitar** los genéricos que ya aceptaba,
así que las llamadas con `course.groups.read` o `course.restrictions.read` responden `200`.

`roadmap-service` declara en `tpi-integration.yml` los scopes H1 que consume (`course.groups.read`,
`course.enrollment.read`, `course.sections.read`, `course.restrictions.read` y `course.activities.read`).

### 6.3 Base del contrato técnico y denominación "MS3"

El contrato técnico se apoya únicamente en lo verificable en código:

| Elemento | Valor |
|---|---|
| Tipo de principal | `service` |
| Authority de servicio | `MS` (Courses la expone como `ROLE_MS`) |
| Audience | `course-service` |
| Scopes | `course.groups.read`, `course.enrollment.read`, `course.sections.read`, `course.restrictions.read` y `course.activities.read`, según el endpoint (§6.2, H1) |

G01 informó además la denominación "MS3" para el principal de servicio. El término no es verificable:
no aparece en `tpi-course` (ninguna rama), ni en el resto de los repositorios de la organización, ni
en `tpi-roadmap`. Esta acta lo registra solo como denominación informada por G01, no le asigna
significado y no depende de él.

---

## 7. Errores HTTP

Formato de error de Courses (`J/controllers/ApiExceptionHandler.java`, `J/configs/SecurityConfig.java`):

```json
{ "status": 403, "code": "FORBIDDEN", "message": "Access is denied" }
```

| Código | Cuándo | `message` |
|---|---|---|
| `200` | Consulta correcta | — |
| `400` | Path o query param inválido (por ejemplo, UUID mal formado) | `Invalid value for <param>: UUID expected` |
| `401` | Sin identidad válida | `Authentication is required` |
| `403` | Sin el rol o scope requerido | `Access is denied` |
| `404` | Cohorte inexistente o inactiva (§3.1, §3.2, §3.3) | `Course Cohort not found` |
| `404` | Sección inexistente o inactiva (§3.4) | `Course Section not found` |

`409` no aplica a estas lecturas.

---

## 8. Estado de implementación en Courses

| Punto | Estado |
|---|---|
| Pertenencia múltiple a grupos | Implementado |
| ID de grupo UUID estable | Implementado |
| DTOs y respuestas de §3 | Implementado |
| Semántica `ANY` / `ALL` / `GROUP` de §4 | Implementado |
| `GET .../sections` con principal de servicio | Implementado (previo al PR #86) |
| `GET .../groups` con principal de servicio | Implementado; acepta `course.groups.read` |
| `GET .../participants` con principal de servicio | Implementado (PR #86) |
| `GET .../restrictions` de sección con principal de servicio | Implementado; acepta `course.restrictions.read` |
| `GET .../restrictions` de actividad/nodo con principal de servicio | Implementado (§3.4.1) |
| Lote M2M de actividades con `order_index`/`course_section_id` | Implementado (§3.5) |
| Evento de cambio de grupo | No existe (acordado, §5) |

El PR #86 de `tpi-course` ("Feature/correciones roadmap") fue mergeado a `develop` el 2026-10-08
(commit de merge `4b51350`). `GET .../sections` ya aceptaba principal de servicio desde antes; el PR #86
habilitó los otros tres.

Evidencia, verificada en código:

| Endpoint | Autorización del método | Camino de servicio en la lógica |
|---|---|---|
| `groups` | `CourseCohortsApiController.getCourseCohortGroups`: `hasRole('MS') and (hasAuthority('course.groups.read') or hasAuthority('course.sections.read') or hasAuthority('course.enrollment.read'))` | `CohortGroupService.ensureCanManage` |
| `participants` | `CourseCohortsApiController.getCourseCohortParticipants`: `hasRole('MS') and hasAuthority('course.enrollment.read')` | `CohortParticipantService.ensureCanAccess` |
| `sections` | `CourseSectionsApiController.listCohortSections`: `hasRole('MS') and hasAuthority('course.sections.read')` | `CourseSectionService.listForService` |
| `restrictions` | `CourseSectionsApiController.getSectionRestrictions`: `hasRole('MS') and (hasAuthority('course.restrictions.read') or hasAuthority('course.sections.read'))` | `SectionRestrictionService.get` |

En los cuatro métodos se conserva la alternativa por rol de usuario que ya existía. En `groups`,
`participants` y `restrictions`, la lógica deja pasar al principal de servicio con el scope sin
resolver una membresía de usuario.

Tests de Courses en `T/controllers/CourseSectionsServicePrincipalTest.java` (`200` con scope, `403`
sin scope):

- `serviceWithScopeCanGetCohortGroups` (con cada scope aceptado), `serviceWithoutScopeCannotGetCohortGroups`;
- `serviceWithScopeCanGetCohortParticipants`, `serviceWithoutScopeCannotGetCohortParticipants`;
- `serviceWithScopeCanGetSectionRestrictions`, `serviceWithoutScopeCannotGetSectionRestrictions`.

La evidencia de arriba corresponde al commit `4b51350`, donde los cuatro endpoints ya aceptan principal
de servicio con los scopes genéricos. Con la ampliación H1 (§6.2), Courses acepta además los scopes
dedicados `course.groups.read` y `course.restrictions.read`, expone las restricciones de
actividad/nodo (§3.4.1) y el lote de actividades incluye `order_index` y `course_section_id` (§3.5);
son los cambios del pedido `tpi-course#84`. La integración de T-10.2 no está bloqueada por Courses.

---

## 9. Seguimiento en Courses

- **Issue `tpi-course#84`** — pedido de implementación de la ampliación H1: scopes dedicados
  (`course.groups.read`, `course.restrictions.read`), restricciones de actividad/nodo (§3.4.1) y
  `order_index`/`course_section_id` en el lote de actividades (§3.5). **Implementado en Courses.**
  La suposición de ese issue de **un único grupo activo por alumno y cohorte** queda descartada: el
  modelo de Courses es de pertenencia **múltiple** (§2.1) y esta acta no la adopta.
- **Issue `tpi-course#88`** — "Alinear contrato de grupos Roadmap ↔ Courses tras PR #86". A cerrar
  por esta ampliación.

### Observación técnica (no forma parte del contrato)

El test `CourseCohortParticipantsControllerTest.assignParticipantGroup_preservesOtherMembershipsAndIsIdempotent`
de Courses está con `@Disabled` y la leyenda "Pendiente de definir la regla con el equipo de grupos".
Se deja asentado solo como referencia: la regla de pertenencia múltiple quedó definida en §1 y el
estado de ese test es una decisión interna de G01.

---

## 10. Puntos abiertos de integración en Roadmap

No bloquean esta acta y se resuelven en la implementación funcional posterior de Roadmap. Esta acta
**no fija** el comportamiento de Roadmap en ninguno de los dos:

- Cómo trata Roadmap las condiciones `DATE` y `SECTION_COMPLETED` cuando están combinadas con
  condiciones `GROUP` bajo un mismo operador.
- Cómo traduce Roadmap `HIDDEN` y `LOCKED`.

---

## 11. Validación

El acta queda vigente cuando ambos grupos la aprueban.

| Grupo | Responsable | Fecha | Aprobación |
|---|---|---|---|
| G01 — Courses | | | ☐ |
| G10 — Roadmap | | | ☐ |

Cualquier cambio posterior a los endpoints, campos, reglas o autenticación descriptos acá requiere
una revisión de esta acta acordada por ambos grupos.
