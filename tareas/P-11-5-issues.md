# Issues — integración Roadmap ↔ Courses (M2M)

Plan P-11.5 (lectura de secciones) + P-11.6/7 (material y grupos). Issues **abiertas** (label `enhancement`).

| # | Repo | Título | URL |
|---|---|---|---|
| A | `tpi-users` | ScopeCatalog: agregar course.sections.read | https://github.com/2026-P4-BE/tpi-users/issues/89 |
| B | `tpi-course` | P-11.B: aceptar principal service en GET /sections | https://github.com/2026-P4-BE/tpi-course/issues/57 |
| C | `tpi-roadmap` | Habilitar lectura real de secciones (M2M) y multi-página | https://github.com/2026-P4-BE/tpi-roadmap/issues/108 |
| D | `tpi-system-compose` | Onboarding: agregar scope course.sections.read a roadmap-service | https://github.com/2026-P4-BE/tpi-system-compose/issues/92 |
| E | `tpi-course` | P-11.6: catálogo de actividades/material por servicio (por lote) | https://github.com/2026-P4-BE/tpi-course/issues/58 |
| F | `tpi-course` | P-11.7: grupos de cohorte y membresía alumno-grupo por servicio | https://github.com/2026-P4-BE/tpi-course/issues/59 |

Orden de desbloqueo:
- **P-11.5 (secciones)**: A + D habilitan el token; B habilita la lectura; C conecta Roadmap. Bloquea HT-07 → HU-36/17/18/37.
- **P-11.6 (material)**: E. Bloquea HU-04, HU-42, HU-46.
- **P-11.7 (grupos)**: F. Bloquea HT-10, HU-44, HU-45.

---

## Issue A — `tpi-users` (Tema 01 / Identity)

`https://github.com/2026-P4-BE/tpi-users/issues/89`

**Título:** `ScopeCatalog: agregar course.sections.read (audience course-service)`

**Labels (si existen):** `scope-catalog`, `P-11`

**Body:**

### Contexto
Roadmap (G10) necesita leer las secciones de una cohorte en Courses (Tema 02)
con identidad de servicio (M2M), no con token de persona. El cliente técnico
`roadmap-service` ya existe y ya tiene scopes (`course.enrollment.read`,
`accounting.account.read`). Falta dar de alta el scope nuevo.

### Pedido
1. Agregar al catálogo la entrada: `course.sections.read` → audience `course-service`.
2. Actualizar el scope del cliente `roadmap-service` en
   `service_clients` / `service_client_scopes` para incluir `course.sections.read`.
3. Regenerar `USERS_SCOPE_CATALOG`.

### Restricciones
- Un scope mapea a una sola audience (`<segment>.<recurso>.<acción>`).
- Sin esta entrada, la emisión de token responde `400 validation`.
- Secret solo por Vault; nunca en texto ni en el issue.

### Criterio de aceptación
- `POST /api/users/public/auth/token` con `client_id=roadmap-service`,
  `scope=course.sections.read`, `audience=course-service` devuelve `access_token`.
- El token contra otra audience responde `403 invalid-audience`.

### Deadline
Oct 10

---

## Issue B — `tpi-course` (Tema 02 / G01)

`https://github.com/2026-P4-BE/tpi-course/issues/57`

**Título:** `P-11.B: aceptar principal service en GET /sections con scope course.sections.read`

**Body:**

### Contexto
Roadmap (G10) lee `GET /api/course/course-cohorts/{courseCohortId}/sections`.
Hoy el controller exige rol humano (`@PreAuthorize("hasAnyRole('GESTOR','PROFESSOR','STUDENT')")`)
y `HttpCourseSectionsClient` de Roadmap queda en modo `stub` por eso.

### Pedido
1. Permitir `X-Principal-Type: service` en ese endpoint con
   `@PreAuthorize("hasRole('MS') and hasAuthority('course.sections.read')")`,
   sin romper el camino de usuario existente.
2. Nueva rama en `SectionAccessPolicy` para principal **service**:
   devuelve únicamente secciones **activas** (`isActive=true`) **y no ocultas**
   (`isVisible=true`), equivalente a la vista de alumno. NO reutilizar el camino
   docente/Gestor (que sí ve ocultas). No consultar membresía ni matrícula de
   usuario (un servicio no tiene).
3. Devolver `403` si falta el scope; `401` si no hay identidad.

### Criterio de aceptación
- Token de servicio con `course.sections.read` → 200, solo activas y visibles.
- Token de servicio sin el scope → 403.
- Token de persona sin relación con la cohorte → 403 (comportamiento actual intacto).
- Cohorte inexistente/inactiva → 404 `"Course Cohort not found"`.

### Deadline
Oct 10

---

## Issue C — `tpi-roadmap` (G10)

`https://github.com/2026-P4-BE/tpi-roadmap/issues/108`

**Título:** `Habilitar lectura real de secciones de Courses (M2M) y soporte multi-página`

**Body:**

### Contexto
La infra ya existe y quedó lista: `HttpCourseSectionsClient` + `TechnicalTokenProvider` +
`CourseSectionsProperties` (`mode` stub|http; en `http` exige `tokenAudience`/`tokenScope`).
La app ya arranca en `COURSES_SECTIONS_CLIENT_MODE=http`; falta que Users/Courses/plataforma entreguen (A/B/D).

### Pedido
1. Agregar `course.sections.read` a `tpi-integration.yml` (`needs`) y al onboarding
   del registry hasta que se refleje.
2. Corregir `HttpCourseSectionsClient`: hoy lee solo `page=0&size=50`. Iterar
   `totalPages` para no perder secciones cuando la cohorte supera 50.
3. Tests contra `stub` + test del paginado multi-página (mapeo `id/title/orderIndex`,
   filtro `isActive`, orden por `orderIndex`, traducción 404 → NOT_FOUND).
4. Al confirmar scope y cliente: `COURSES_SECTIONS_CLIENT_MODE=http`,
   `COURSES_TOKEN_AUDIENCE=course-service`, `COURSES_SECTIONS_TOKEN_SCOPE=course.sections.read`.

### Criterio de aceptación
- `mvn verify` en verde.
- Con >50 secciones, el cliente devuelve la lista completa.
- Con scope emitido, `GET` real contra Courses por Gateway devuelve activas y visibles.

### Dependencias
- A (tpi-users), B (tpi-course). Nada de http con valores inventados.

---

## Issue D — `tpi-system-compose` (Onboarding)

`https://github.com/2026-P4-BE/tpi-system-compose/issues/92`

**Título:** `Onboarding: agregar scope course.sections.read a roadmap-service`

**Body:**

### Contexto
El cliente técnico `roadmap-service` ya está registrado en el registry y ya tiene
scopes (`course.enrollment.read`, `accounting.account.read`). Roadmap (G10)
necesita además leer las secciones de una cohorte en Courses con token de
servicio (M2M). El scope lo emite Users; el registro del `needs` vive acá.

### Pedido
1. Sumar `course.sections.read` a `needs:` de `roadmap-service` en `registry/services.yml`.
2. Regenerar `registry/generated/` (`USERS_SCOPE_CATALOG`, `clients.txt`, `micros.yml`,
   `platform.env`) con `scripts/render-registry.sh`.
3. Verificar que `USERS_SCOPE_CATALOG` incluya `course.sections.read:course-service`.

### Criterio de aceptación
- `registry/generated/platform.env` contiene `course.sections.read:course-service`.
- `registry/generated/clients.txt` lista `roadmap-service` con el scope nuevo.
- El onboarding/render queda consistente (sin diffs inesperados).

### Dependencia
- Issue de `tpi-users` para dar de alta el scope en `ScopeCatalog.java` y en el cliente (P-11.5).
  Sin esa alta, la emisión de token responde `400 validation`.

### Deadline
Oct 10

---

## Issue E — `tpi-course` (Tema 02 / G01) — P-11.6 material

`https://github.com/2026-P4-BE/tpi-course/issues/58`

**Título:** `P-11.6: catálogo de actividades/material legible por servicio (por lote)`

**Body:**

### Contexto
Roadmap (G10) necesita leer el material teórico de una sección para las HUs HU-04 (vincular nodo a material publicado), HU-42 (abrir/leer material de un nodo) y HU-46 (material teórico en nodos/Templo). Hoy la tabla `course_activity` existe en `tpi_course`, pero **no hay endpoint REST** que la exponga y el `activity_type` sólo se crea `QUIZ`; no hay `FILE`/`LINK` ni URL de acceso. Roadmap guarda solo `content_id` y **nunca** sube ni almacena archivos.

### Pedido
1. Exponer lectura por **lote** de actividades/materiales de una sección/cohorte con token de servicio (M2M), no una llamada por material.
2. Devolver por cada ítem: id estable, `title`, `type` (`FILE`|`LINK`|`GITHUB_REPO`|`QUIZ`), estado de publicación (`PUBLISHED`/`DRAFT`/no disponible), y una **URL de acceso al archivo** (firmada y con vencimiento, provista por Courses).
3. Habilitar la carga/almacenamiento del material en la plataforma Garage y los tipos `FILE` y `LINK` (hoy sólo `QUIZ`).
4. Scope de servicio nuevo (propuesta: `course.activities.read` → `course-service`).

### Restricciones
- El material vive en Garage; Roadmap no lo guarda ni lo sube.
- Un material despublicado o dado de baja debe informarse como "no disponible" sin romper las lecturas ya registradas en Roadmap.
- Sin datos sensibles (soluciones/tests) en el payload.

### Criterio de aceptación
- Una sección con material publicado devuelve por lote id, `title`, `type`, estado y URL de acceso, con token de servicio.
- Material despublicado → estado "no disponible".
- 403 si falta el scope; 404 si la sección/cohorte no existe.

### Dependencia
- HT-07 (`course.sections.read`) para la lectura base de secciones.

### Deadline
Oct 17

Relacionado: `tpi-roadmap` HU-04 (#734), HU-42 (#4248), HU-46 (#5375); P-11.5/6 en `docs/T-01-7-EUREKA-GATEWAY.md`.

---

## Issue F — `tpi-course` (Tema 02 / G01) — P-11.7 grupos

`https://github.com/2026-P4-BE/tpi-course/issues/59`

> **Actualización 08/10 (HU-44/HT-10):** la decisión de producto reemplaza P-29/D-02: un alumno **puede** pertenecer a **varias** comisiones. El punto 4 (garantizar un grupo activo por alumno y cohorte) queda **obsoleto**. El pedido se resolvió en [tpi-course#84](https://github.com/2026-P4-BE/tpi-course/issues/84) (implementado), que además sumó las restricciones de actividad/nodo y el orden de actividades.

**Título:** `P-11.7: grupos de cohorte y membresía alumno-grupo legibles por servicio`

**Body:**

### Contexto
Roadmap (G10) necesita conocer el grupo de cada alumno y qué grupos alcanza una sección para las HUs HU-44 (ver sólo las unidades de mi grupo), HU-45 (ranking y avance por grupo) y HT-10. Courses ya modela los grupos (`cohort_group` y `cohort_group_member` desde V1; restricción `GROUP` por sección desde V12), pero **ningún endpoint los expone**, así que HT-10/HU-44/HU-45 no tienen fuente de datos. Roadmap guarda `cohort_group_id` como UUID sin FK y nunca da de alta grupos.

### Pedido
1. Exponer los **grupos de una cohorte** y la **membresía alumno-grupo** con token de servicio (M2M).
2. Los **grupos de cada matrícula** se leen en el listado de participantes (paginado, con `groups[]` por matrícula); no se requiere una llamada por alumno.
3. Definir si el **cambio de grupo** se comunica por evento o por consulta (a acordar en el acta).
4. ~~Corregir la restricción de unicidad: garantizar un grupo activo por alumno y cohorte.~~ **Obsoleto (08/10):** un alumno puede estar en varias comisiones; ver actualización arriba.
5. Scope de servicio `course.groups.read` → `course-service` (implementado).

### Restricciones
- Solo PROFESSOR/GESTOR administran grupos en Courses; Roadmap sólo lee.
- Un alumno puede pertenecer a **varias** comisiones a la vez (decisión 08/10, reemplaza D-02/P-29).
- Roadmap nunca da de alta ni modifica grupos.

### Criterio de aceptación
- Dado un alumno en 2W1 y 2W2, la consulta devuelve ambas comisiones.
- Cuando un gestor le cambia la comisión, Roadmap obtiene el estado vigente por consulta (no hay evento de cambio, §5 del acta).
- Las restricciones de sección (condiciones `GROUP`) se leen por sección, no por lote.
- 403 si falta el scope; sin exposición de datos cross-cohorte.

### Dependencia
- HT-07 (`course.sections.read`) y visibilidad por grupo (P-29, reemplazada por la decisión 08/10).

### Deadline
Oct 17

Relacionado: `tpi-roadmap` HT-10 (#5372), HU-44 (#5373), HU-45 (#5374); P-11.5/6/7 en `docs/T-01-7-EUREKA-GATEWAY.md`.
