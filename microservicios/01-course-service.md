# Microservicio: Course Service (`tpi-course`)

> **Ficha Técnica Canónica y Contrato de Integración**  
> Tema: **Tema 01 — Cursos, Cohortes y Secciones**  
> Equipo Responsable: **Grupo 01 (G01)**  
> Repositorio: `2026-P4-BE/tpi-course` (Local: `D:\Dev\IdeaProjects\Progra4\tpi-course`)  
> Estado: **Vigente (v2.0.0)**

---

## 1. Identidad y Red

| Parámetro | Valor |
|---|---|
| **Nombre de Aplicación (Eureka)** | `course-service` |
| **Prefijo en API Gateway** | `/api/course/**` (sin reescritura de prefijo) |
| **Puerto por Defecto** | `8086` |
| **Puerto de Gestión (Management/Actuator)** | `8087` (`management.server.port`) |
| **Rutas Públicas** | `${app.api.public-path}/**` (`/api/course/public/**`, healthchecks y OpenAPI) |
| **Rutas Privadas** | `${app.api.private-path}/**` (`/api/course/**`) |
| **Base de Datos** | PostgreSQL (migraciones Flyway `db/migration`) |
| **Audience M2M** | `course-service` |

---

## 2. Dominio y Responsabilidades

### Qué Hace Course Service (Fuente de Verdad)
- **Gestión Académica Base:** Cursos base (`CourseBase`), cohortes (`CourseCohort`), materias, instituciones y docentes.
- **Estructura Formativa:** Secciones formativas (`Section`), submódulos y contenidos/actividades base del curso.
- **Matrículas y Membresías:** Alta, baja y estado de inscripción del alumno (`Enrollment`: `ACTIVE`, `INACTIVE`, `COMPLETED`, `DROPPED`).
- **Comisiones / Grupos Escolares:** Creación y gestión de comisiones (`Group`), asignación de alumnos a comisiones y pertenencias docentes.
- **Restricciones de Visibilidad:** Condición de visibilidad y activación de secciones (`isActive ∧ isVisible`).

### Qué NO Hace Course Service
- **NO evalúa la progresión gamificada ni el grafo de aprendizaje:** La condicionalidad de prerequisitos entre nodos y unidades es exclusiva de `roadmap-service`.
- **NO evalúa restricciones por alumno individualmente:** Courses expone las reglas y asignaciones; Roadmap es quien las evalúa en tiempo real contra el progreso del alumno (Acuerdo T-10.1 / DEC-014).
- **NO gestiona vidas, XP ni inventarios.**

---

## 3. Acuerdos y Decisiones de Integración con Roadmap

### 3.1 Identificador de Curso (`courseId` = `courseCohortId`)
- **Regla Fundamental:** El `courseId` utilizado en Roadmap siempre corresponde unívocamente al `courseCohortId` de Courses (instancia de cursado específica). Roadmap **nunca** opera sobre `courseBaseId`.

### 3.2 Comisiones / Grupos (HU-44 / DEC-014 / Acta T-10.1)
- **Multi-comisión:** Un alumno puede pertenecer a **0..N comisiones** simultáneamente dentro de la misma cohorte (reemplaza restricciones históricas de una única comisión).
- **Modelo de Evaluación Descentralizado ("Opción R"):** Courses solo provee las asignaciones y restricciones de la cohorte. Roadmap evalúa si el alumno puede acceder a un nodo según sus comisiones activas.
- **Identificador Estable:** Toda referencia a comisiones se realiza mediante UUID (`id`), nunca por nombre o etiqueta visual.

### 3.3 Sincronización de Unidades con Secciones de Courses (HU-36)
- Roadmap puede anclar sus unidades (`Section`) a las secciones académicas de Courses mediante `course_section_id`.
- Cuando el toggle `SECTIONS_SYNC_ENABLED=true` está activo, Roadmap sincroniza el orden, título y visibilidad de las unidades basándose en Courses (`SectionSyncClient`).

---

## 4. Endpoints REST Consumidos por Roadmap

Todas las llamadas salientes desde Roadmap hacia `course-service` se realizan a través del API Gateway (`${app.gateway.url}/api/course/...`) utilizando un token de servicio M2M con `grant_type=client_credentials`.

### 4.1 Consulta de Secciones de una Cohorte
- **Método y URL:** `GET /api/course/cohorts/{cohortId}/sections`
- **Scope Requerido:** `course.sections.read`
- **Headers:**  
  `Authorization: Bearer <m2m_token>`  
  `X-Service-Id: roadmap-service`
- **Respuesta Exitosa (200 OK):**
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "name": "Unidad 1: Introducción a la Programación",
    "order": 1,
    "is_active": true,
    "is_visible": true,
    "created_at": "2026-03-01T10:00:00Z"
  }
]
```

### 4.2 Verificación de Matrícula del Alumno (Gate de Elegibilidad)
- **Método y URL:** `GET /api/course/cohorts/{cohortId}/students/{studentId}/enrollment`
- **Scope Requerido:** `course.enrollment.read`
- **Respuesta Exitosa (200 OK):**
```json
{
  "student_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "cohort_id": "e2a1b3c4-d5e6-7f8a-9b0c-1d2e3f4a5b6c",
  "status": "ACTIVE",
  "enrolled_at": "2026-03-01T12:00:00Z"
}
```
- **Errores Típicos:**  
  - `404 Not Found`: Alumno no matriculado en la cohorte (`enrollment.not-found`).  
  - `403 Forbidden`: Matrícula suspendida o cursado archivado.

### 4.3 Consulta de Comisiones del Alumno en la Cohorte (HU-44)
- **Método y URL:** `GET /api/course/cohorts/{cohortId}/students/{studentId}/groups`
- **Scope Requerido:** `course.groups.read`
- **Respuesta Exitosa (200 OK):**
```json
[
  {
    "id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
    "name": "Comisión 4K1",
    "shift": "MORNING",
    "is_active": true
  }
]
```

### 4.4 Consulta de Todas las Comisiones de una Cohorte (Docentes/Managers)
- **Método y URL:** `GET /api/course/cohorts/{cohortId}/groups`
- **Scope Requerido:** `course.groups.read`

---

## 5. Eventos Kafka

- **Tópico Principal:** `courses.events`
- **Formato:** Envelope estándar v8 (`snake_case`, 5 campos)

### Eventos Producidos por Courses:
1. **`STUDENT_ENROLLED`:**
   - Emitido cuando un alumno se matricula a una cohorte.
   - Clave del mensaje (`Key`): `courseId` o `studentId`.
   - Payload:
```json
{
  "event_id": "4a7bb0f1-1234-5678-90ab-cdef12345678",
  "event_type": "STUDENT_ENROLLED",
  "timestamp": "2026-10-15T08:30:00.000Z",
  "producer": "course-service",
  "payload": {
    "course_id": "e2a1b3c4-d5e6-7f8a-9b0c-1d2e3f4a5b6c",
    "student_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "enrolled_at": "2026-10-15T08:30:00.000Z"
  }
}
```
2. **`COURSE_ARCHIVED` / `COHORT_CLOSED`:**
   - Informa el cierre del cursado; consumido por Roadmap para marcar el árbol en sólo lectura.

---

## 6. Seguridad y Scopes M2M

| Scope | Destinado a | Propósito |
|---|---|---|
| `course.sections.read` | `roadmap-service` | Sincronización de secciones y verificación de árbol. |
| `course.enrollment.read` | `roadmap-service`, `engine-challenge-service` | Validación de matrícula activa en Gate de elegibilidad. |
| `course.groups.read` | `roadmap-service` | Obtención de membresías a comisiones para HU-44. |
| `course.teaching-membership.read` | `roadmap-service` | Validación de permisos docentes para asignación de nodos. |

---

## 7. Clientes y Adaptadores en `tpi-roadmap`
- Clientes HTTP: `com.utn.tpi.roadmap.clients.CoursesClient`, `com.utn.tpi.roadmap.clients.SectionSyncClient`, `com.utn.tpi.roadmap.clients.GroupProgressClient`.
- Manejo de caídas: Si Courses no responde (503 / Timeout), el Gate responde `503 Service Unavailable` fail-closed (no asume matrícula activa). En la v1.4 del acta del gate (aprobada por G09; entra con T-31.1) pasa a `200` con `reason=origin_unavailable` ([[decisiones/DEC-020-gate-origen-no-disponible-en-vez-de-503|DEC-020]]).
