---
tags: [tpi, g10, roadmap, sprint-3, seguridad, permisos]
tarea: "T-22.3 (#9092) · DT-02 / DT-03"
historia: "[[sprints/sprint-3/historias/HT-22 Permisos en vez de roles|HT-22]]"
estado: alineada con tpi-roadmap#294
actualizado: 2026-10-27
---

# T-22.1 — Matriz de permisos (versión alineada con #294)

**Historia:** [[sprints/sprint-3/historias/HT-22 Permisos en vez de roles|HT-22]] · **Taiga:** #9090 / #9092 · Cierra **DT-03** y apoya **DT-02** de [[deuda-tecnica]].

> [!info] Qué es esta nota
> Es una **copia** de [[arquitectura/T-22-1-matriz-permisos]] (la propuesta original, que se deja como estaba) con los **nombres y roles reales del código**. El catálogo no es el de 19 permisos de la propuesta: es el que implementa la PR draft [tpi-roadmap#294](https://github.com/2026-P4-BE/tpi-roadmap/pull/294) de Ramiro Ibazeta (Tema 01, `authz-starter 0.1.0`), que es el que se acordó con Users ([[acuerdos/users]]). Esta tabla sale de `src/test/resources/permission-matrix.csv` del repo: un test (`PermissionMatrixTest`) la compara con los controllers y falla si no coinciden.

> [!warning] Base
> Relevada sobre la rama de #294 (`7b2fbcb2`, 2026-10-27) más los cambios de esta tarea (rama `feature/dt-02-03-permisos-2806eb`, apilada sobre #294). `develop` todavía no tiene `@RequirePermission`. Con `authz.mode=off` (valor por defecto) cada `@RequirePermission` deja pasar por sus `legacyRoles`; esas son las columnas de rol de abajo.

## 1. Cómo leer la matriz

- **Permiso:** el código que pide `@RequirePermission` (en el controller o en `RoadmapAuthorizationService`).
- **ADMIN / GESTOR / PROFESSOR / STUDENT:** roles en `legacyRoles`, o sea los que pasan hoy con `authz.mode=off`. El header `X-User-Roles` sigue llegando (Users, tpi-users#215).
- **Servicio:** identidad técnica (`ServiceIdentity`) que entra por scope en `SecurityConfig`.
- **Alcance hoy:** lo que se chequea además del permiso. El permiso **no reemplaza** el chequeo de dueño del curso (HT-22).
- ⚠️ marca un chequeo que falta o que no es igual al del resto.

## 2. Catálogo de permisos (el de #294)

| Permiso | Qué permite |
|---|---|
| `roadmap.graph.read` | Ver el roadmap, el grafo, el detalle de nodos, los roadmaps del curso, el mentor y los ajustes; el staff ve además relaciones, tipos ocultos y el historial de edición. |
| `roadmap.graph.write` | Editar secciones, nodos, reglas, prerrequisitos, relaciones, mentor y ajustes; crear, renombrar, asignar comisiones, archivar y clonar roadmaps; sincronizar secciones; validar la estructura. |
| `roadmap.graph.rebuild` | Operaciones de plataforma (solo ADMIN): reconstruir y reconciliar el grafo, backfill de nodos frontera y reintento de eventos outbox. |
| `roadmap.badge.read` / `roadmap.badge.write` | Ver / administrar el catálogo de insignias del curso; staff que ve las insignias de un alumno. |
| `roadmap.challenge.read` | Pool de desafíos, cursos de un desafío y ventana de fechas de un desafío (staff). |
| `roadmap.progress.read` | Progreso, nivel, XP y línea de XP de otros alumnos o de la cohorte / comisión. |
| `roadmap.progress.self` | Lo propio del alumno: materiales, lectura, nivel, salud, inventario, elegibilidad, XP, avatar y mascota; marcar un contenido como leído. |
| `roadmap.ranking.read` | Ranking del curso o de un roadmap. La vista depende de quién pide. |
| `roadmap.gate.read` · `roadmap.restrictions.read` · `roadmap.health.read` | **Scopes de servicio** de `SecurityConfig` (Motor / Courses / Accounting). No son `@RequirePermission`. |

### Equivalencias con la propuesta original (19 permisos)

| Propuesta T-22.1 | #294 |
|---|---|
| `graph.read`, `roadmaps.read`, `mentor.read` | `graph.read` |
| `graph.edit`, `roadmaps.manage`, `mentor.edit` | `graph.write` |
| `maintenance.run` | `graph.rebuild` |
| `badges.read` / `badges.manage` | `badge.read` / `badge.write` |
| `challenge-pool.read` | `challenge.read` |
| `learning.read`, `learning.write`, `avatar.read`, `avatar.edit` | `progress.self` |
| `progress.read`, `ranking.read` | igual |
| `gate.read`, `restrictions.read`, `health.read` | igual (scopes de servicio) |

Users confirmó que no hace falta inventar `roadmap.learning.*` ni `roadmap.avatar.*` (tpi-users#215).

### Rol → permisos

✔ = todos los endpoints del permiso lo dejan pasar; **parcial** = solo algunos.

| Permiso | Endpoints | ADMIN | GESTOR | PROFESSOR | STUDENT |
|---|:-:|:-:|:-:|:-:|:-:|
| `roadmap.badge.read` | 2 | ✔ | ✔ | ✔ |  |
| `roadmap.badge.write` | 3 | ✔ | ✔ | ✔ |  |
| `roadmap.challenge.read` | 3 | ✔ | parcial | ✔ |  |
| `roadmap.graph.read` | 13 | ✔ | ✔ | ✔ | parcial |
| `roadmap.graph.rebuild` | 5 | ✔ |  |  |  |
| `roadmap.graph.write` | 34 | ✔ | ✔ | ✔ |  |
| `roadmap.progress.read` | 9 | ✔ | ✔ | ✔ | parcial |
| `roadmap.progress.self` | 18 | parcial |  |  | ✔ |
| `roadmap.ranking.read` | 2 | ✔ | ✔ | ✔ | ✔ |

Más los chequeos que los controllers piden desde el código (`RoadmapAuthorizationService`), que figuran al final de la matriz por endpoint.

## 3. Qué cambió respecto de la propuesta (roles)

Comparado endpoint por endpoint con la matriz original, estas son **todas** las diferencias de rol:

1. **GESTOR entra** (T-22.3 y [[acuerdos/users]]: la paridad no sale del catálogo de Compose, se pone en `legacyRoles`):
   - catálogo de insignias (`badge.read` / `badge.write`), progreso de la cohorte, `xp-history` y `xp-timeline`: ya venía en #294;
   - **progreso de un alumno** (`requireProgressRead`), **progreso de comisión** (`GroupProgressController`) y **nivel de un alumno** (`LevelController`): agregado en esta tarea. El chequeo de dueño también deja pasar a GESTOR como a ADMIN (`Roles.isPlatformStaff`); antes `CohortOwnershipGuard`, `GroupProgressController` y `LevelController` miraban solo `ADMIN`. Esto cierra una incoherencia de #294: `ProgressController` listaba GESTOR en `legacyRoles`, pero el guard le exigía ser dueño.
2. **`STUDENT` figura en `progress.read` de la cohorte** (`/courses/{id}/progress`, `/roadmaps/{id}/progress`). No es un permiso nuevo: en `develop` esos endpoints no tenían `@PreAuthorize` y dejaban pasar a cualquier usuario; el chequeo de dueño del service es el que corta. #294 lo dejó explícito con `LegacyPermissionParityTest`. La matriz original decía ADMIN / PROFESSOR, que no era del todo exacto.
3. **Endpoints nuevos** desde la propuesta: dashboard de cohorte, `ai-policy`, mover nodo, efectos de ítems, IA del nodo, PATCH de relación, `xp-history` propio, `xp-timeline` del alumno y el redrive del outbox.
4. **Outbox admin**: pasó de `hasRole('ADMIN')` a `@RequirePermission("roadmap.graph.rebuild", legacyRoles = ADMIN)`, **sin cambio de quién pasa**. Se reutilizó `graph.rebuild` para no inventar un código que no esté en el catálogo de Compose; si Users prefiere uno propio (`roadmap.outbox.retry`) es un cambio de una línea.

## 4. Hallazgos de la propuesta: estado

| # | Hallazgo | Estado |
|---|---|---|
| 1 | GESTOR sin el mismo trato en todos lados | ✅ Resuelto para insignias, progreso (cohorte, alumno, comisión) y nivel. **Pendiente:** salud de un alumno (`HealthController.requireViewer` mira `ADMIN` / `PROFESSOR` a mano) y la ventana del desafío (`requireChallengeRead`: ADMIN / PROFESSOR). No estaban en la lista de T-22.3: quedan igual hasta que se decida. |
| 2 | Profesor lee datos de cualquier curso | ✅ progreso, XP e insignias ([tpi-roadmap#343](https://github.com/2026-P4-BE/tpi-roadmap/pull/343)). Pendientes: ventana del desafío y roadmap / detalle de nodo (`graph.read` sin chequeo de dueño) |
| 3 | El gate aceptaba cualquier servicio | ✅ `402a4094` (T-22.4) |
| 4 | `POST /nodes/{id}/read` acepta ADMIN | Sigue: `markAsRead` tiene `legacyRoles = {STUDENT, ADMIN}` |
| 5 | Los servicios solo entran a cuatro rutas | Sin cambios |
| 6 | Chequeos de dueño copiados en cada controller | Sigue (ver §6) |

## 5. Matriz por endpoint

Rutas relativas a `/api/roadmap`. Agrupadas por controller. Los roles salen del CSV.


### BadgeCatalogController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| POST | `/courses/{courseId}/badges` | `roadmap.badge.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| DELETE | `/courses/{courseId}/badges/{badgeId}` | `roadmap.badge.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| GET | `/courses/{courseId}/badges` | `roadmap.badge.read` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PUT | `/courses/{courseId}/badges/{badgeId}` | `roadmap.badge.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |

### BadgeController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/students/{studentId}/badges` | `roadmap.progress.self` / `roadmap.badge.read` | ✔ | ✔ | ✔ | ✔ |  | El propio alumno; staff por `requireBadgeRead`. Profesor: dueño; ADMIN y GESTOR: cualquier cohorte |

### BoundaryNodeAdminController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| POST | `/admin/boundary-nodes/backfill` | `roadmap.graph.rebuild` | ✔ |  |  |  |  | Operación de plataforma |

### ChallengeCoursesController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/challenges/{challengeId}/courses` | `roadmap.challenge.read` | ✔ | ✔ | ✔ |  |  | El profesor ve solo sus cursos; ADMIN y GESTOR todos |
| GET | `/challenges/{challengeId}/world` | `roadmap.graph.read` | ✔ | ✔ | ✔ | ✔ |  | Cualquier usuario con el rol |

### ChallengePoolController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/challenge-pool` | `roadmap.challenge.read` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |

### ChallengeWindowController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseCohortId}/challenges/{challengeId}/window` | `roadmap.restrictions.read` (scope) / `roadmap.challenge.read` | ✔ |  | ✔ |  | ✔ | Servicio con el scope, o ADMIN/profesor por `requireChallengeRead`; sin chequeo de dueño ⚠️ |

### CohortDashboardController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/progress/summary` | `roadmap.progress.read` | ✔ | ✔ | ✔ |  |  | Resumen del dashboard de cohorte (nuevo) |
| GET | `/courses/{courseId}/xp-timeline` | `roadmap.progress.read` | ✔ | ✔ | ✔ |  |  | Línea de XP de la cohorte (nuevo) |

### CourseMentorController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/mentor` | `roadmap.graph.read` | ✔ | ✔ | ✔ | ✔ |  | Cualquier usuario con el rol |
| PUT | `/courses/{courseId}/mentor` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |

### GateController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/students/{studentId}/nodes/{nodeId}/eligibility` | `roadmap.gate.read` (scope) |  |  |  |  | ✔ | Solo servicio con el scope; 403 sin él (`SecurityConfig`, T-22.4) |
| GET | `/courses/{courseId}/nodes/{nodeId}/eligibility` | `roadmap.progress.self` |  |  |  | ✔ |  | El propio alumno (id del token) |

### GraphAdminController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| POST | `/admin/graph/rebuild` | `roadmap.graph.rebuild` | ✔ |  |  |  |  | Operación de plataforma |
| POST | `/admin/graph/reconcile` | `roadmap.graph.rebuild` | ✔ |  |  |  |  | Operación de plataforma |

### GraphController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| POST | `/nodes/{nodeId}/prerequisites` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| GET | `/courses/{courseId}/nodes/{nodeId}/ai-policy` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Política de IA del nodo; pide `graph.write` (nuevo) |
| POST | `/sections/{sectionId}/nodes` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| POST | `/courses/{courseId}/sections` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| POST | `/roadmaps/{roadmapId}/sections` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| DELETE | `/nodes/{nodeId}` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| DELETE | `/sections/{sectionId}` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| GET | `/nodes/{nodeId}/edit-log` | `roadmap.graph.read` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| GET | `/courses/{courseId}` | `roadmap.graph.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno: su comisión; staff sin chequeo de dueño ⚠️ |
| GET | `/roadmaps/{roadmapId}` | `roadmap.graph.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno: su comisión; staff sin chequeo de dueño ⚠️ |
| PATCH | `/nodes/{nodeId}/section` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Mover un nodo de unidad (nuevo) |
| PATCH | `/nodes/{nodeId}` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/sections/{sectionId}` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/nodes/{nodeId}/availability` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/nodes/{nodeId}/content` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/nodes/{nodeId}/allowed-item-effects` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Efectos de ítems permitidos (nuevo) |
| PATCH | `/nodes/{nodeId}/mandatory` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PUT | `/nodes/{nodeId}` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/nodes/{nodeId}/prerequisite-mode` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/nodes/{nodeId}/rules` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PUT | `/sections/{sectionId}` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/sections/{sectionId}/rules` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/nodes/{nodeId}/ai` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Marca el uso de IA (nuevo) |

### GraphViewController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/graph` | `roadmap.graph.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno: su comisión; staff: dueño (ADMIN y GESTOR sin chequeo) |
| GET | `/roadmaps/{roadmapId}/graph` | `roadmap.graph.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno: su comisión; staff: dueño (ADMIN y GESTOR sin chequeo) |

### GroupProgressController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/groups/{groupId}/progress` | `roadmap.progress.read` | ✔ | ✔ | ✔ |  |  | ADMIN, GESTOR o profesor dueño |

### HealthController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/students/me/health` | `roadmap.progress.self` |  |  |  | ✔ |  | El propio alumno (id del token) |
| GET | `/courses/{courseId}/students/{studentId}/health` | `roadmap.health.read` (scope) / dueño | ✔ |  | ✔ |  | ✔ | Servicio con el scope, ADMIN o profesor dueño (`hasRole` a mano); GESTOR no |

### InventoryController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/inventory` | `roadmap.progress.self` |  |  |  | ✔ |  | El propio alumno (id del token) |

### LevelController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/students/me/level` | `roadmap.progress.self` |  |  |  | ✔ |  | El propio alumno (id del token) |
| GET | `/roadmaps/{roadmapId}/students/me/level` | `roadmap.progress.self` |  |  |  | ✔ |  | El propio alumno (id del token) |
| GET | `/courses/{courseId}/students/{studentId}/level` | `roadmap.progress.read` | ✔ | ✔ | ✔ |  |  | ADMIN, GESTOR o profesor dueño |
| GET | `/roadmaps/{roadmapId}/students/{studentId}/level` | `roadmap.progress.read` | ✔ | ✔ | ✔ |  |  | ADMIN, GESTOR o profesor dueño |

### NodeController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/nodes/{nodeId}` | `roadmap.graph.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno: lo que le toca ver; staff sin chequeo de dueño ⚠️ |
| GET | `/roadmaps/{roadmapId}/nodes/{nodeId}` | `roadmap.graph.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno: lo que le toca ver; staff sin chequeo de dueño ⚠️ |
| GET | `/courses/{courseId}/materials` | `roadmap.progress.self` |  |  |  | ✔ |  | El propio alumno, inscripto (403 student.not-enrolled) |
| GET | `/roadmaps/{roadmapId}/materials` | `roadmap.progress.self` |  |  |  | ✔ |  | El propio alumno, inscripto (403 student.not-enrolled) |

### OutboxAdminController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| POST | `/admin/outbox/{eventId}/retry` | `roadmap.graph.rebuild` | ✔ |  |  |  |  | Operación de plataforma: reintento de un evento outbox (nuevo; antes `hasRole(ADMIN)`) |
| POST | `/admin/outbox/retry-failed` | `roadmap.graph.rebuild` | ✔ |  |  |  |  | Operación de plataforma: reintento de todos los eventos FAILED (nuevo; antes `hasRole(ADMIN)`) |

### PingController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/public/ping` | — (público) | ✔ | ✔ | ✔ | ✔ |  | Sin autenticación |

### ProgressController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/progress` | `roadmap.progress.read` | ✔ | ✔ | ✔ | ✔ | ✔ | Servicio con el scope, ADMIN, GESTOR o profesor dueño |
| GET | `/roadmaps/{roadmapId}/progress` | `roadmap.progress.read` | ✔ | ✔ | ✔ | ✔ | ✔ | Servicio con el scope, ADMIN, GESTOR o profesor dueño |
| POST | `/nodes/{nodeId}/read` | `roadmap.progress.self` | ✔ |  |  | ✔ |  | El propio alumno |
| GET | `/courses/{courseId}/students/{studentId}/progress` | `roadmap.progress.self` / `roadmap.progress.read` | ✔ | ✔ | ✔ | ✔ |  | El propio alumno; staff por `requireProgressRead`. Profesor: dueño; ADMIN y GESTOR: cualquier cohorte |
| GET | `/roadmaps/{roadmapId}/students/{studentId}/progress` | `roadmap.progress.self` / `roadmap.progress.read` | ✔ | ✔ | ✔ | ✔ |  | El propio alumno; staff por `requireProgressRead`. Profesor: dueño; ADMIN y GESTOR: cualquier cohorte |
| GET | `/courses/{courseId}/sections/{sectionId}/reading-progress` | `roadmap.progress.self` |  |  |  | ✔ |  | El propio alumno (id del token) |
| GET | `/roadmaps/{roadmapId}/sections/{sectionId}/reading-progress` | `roadmap.progress.self` |  |  |  | ✔ |  | El propio alumno (id del token) |

### RankingController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/ranking` | `roadmap.ranking.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno inscripto (vista anónima); profesor dueño; ADMIN y GESTOR todos |
| GET | `/roadmaps/{roadmapId}/ranking` | `roadmap.ranking.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno inscripto (vista anónima); profesor dueño; ADMIN y GESTOR todos |

### RoadmapManagementController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| POST | `/roadmaps/{roadmapId}/archive` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PUT | `/roadmaps/{roadmapId}/groups` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| POST | `/roadmaps/{roadmapId}/clone` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| POST | `/courses/{courseId}/roadmaps` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| GET | `/courses/{courseId}/roadmaps` | `roadmap.graph.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno inscripto; staff: dueño (ADMIN y GESTOR sin chequeo) |
| GET | `/courses/{courseId}/settings` | `roadmap.graph.read` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/roadmaps/{roadmapId}` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PUT | `/courses/{courseId}/settings` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |

### SectionSyncController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| POST | `/courses/{courseId}/sections/sync` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |

### StructureValidationController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/validation` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| GET | `/roadmaps/{roadmapId}/validation` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |

### StudentAvatarController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/students/me/avatar` | `roadmap.progress.self` |  |  |  | ✔ |  | El propio alumno |
| GET | `/students/me/avatar` | `roadmap.progress.self` |  |  |  | ✔ |  | El propio alumno |
| GET | `/courses/{courseId}/students/me/pet` | `roadmap.progress.self` |  |  |  | ✔ |  | El propio alumno |
| GET | `/students/me/pet` | `roadmap.progress.self` |  |  |  | ✔ |  | El propio alumno |
| PUT | `/courses/{courseId}/students/me/avatar` | `roadmap.progress.self` |  |  |  | ✔ |  | El propio alumno |
| PUT | `/students/me/avatar` | `roadmap.progress.self` |  |  |  | ✔ |  | El propio alumno |

### StudentDashboardController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/students/{studentId}/xp-timeline` | `roadmap.progress.self` / `roadmap.progress.read` | ✔ | ✔ | ✔ | ✔ |  | El propio alumno; staff por `requireTimelineRead`. Profesor: dueño; ADMIN y GESTOR: cualquier cohorte |

### TypedRelationController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| POST | `/roadmaps/{roadmapId}/relations` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| DELETE | `/roadmaps/{roadmapId}/relations/{relationId}` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| GET | `/roadmaps/{roadmapId}/hidden-relation-types` | `roadmap.graph.read` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| GET | `/roadmaps/{roadmapId}/relations` | `roadmap.graph.read` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PUT | `/roadmaps/{roadmapId}/hidden-relation-types` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/roadmaps/{roadmapId}/relations/{relationId}` | `roadmap.graph.write` | ✔ | ✔ | ✔ |  |  | Edición de una relación tipada (nuevo) |

### XpHistoryController

| Método | Ruta | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/students/{studentId}/xp-history` | `roadmap.progress.self` / `roadmap.progress.read` | ✔ | ✔ | ✔ | ✔ |  | El propio alumno; staff por `requireTimelineRead`. Profesor: dueño; ADMIN y GESTOR: cualquier cohorte |
| GET | `/courses/{courseId}/students/me/xp-history` | `roadmap.progress.self` |  |  |  | ✔ |  | El propio alumno (nuevo) |

### Chequeos desde el código (`RoadmapAuthorizationService`)

| Chequeo | Permiso | ADMIN | GESTOR | PROFESSOR | STUDENT |
|---|---|:-:|:-:|:-:|:-:|
| `requireBadgeRead` | `roadmap.badge.read` | ✔ | ✔ | ✔ |  |
| `requireChallengeRead` | `roadmap.challenge.read` | ✔ |  | ✔ |  |
| `requireProgressRead` | `roadmap.progress.read` | ✔ | ✔ | ✔ |  |
| `requireProgressSelf` | `roadmap.progress.self` |  |  |  | ✔ |
| `requireTimelineRead` | `roadmap.progress.read` | ✔ | ✔ | ✔ |  |

## 6. Qué queda para cerrar CA3 de HT-22 (sin `hasRole` a mano)

Siguen chequeos de rol dentro del código, no en anotaciones. Todos distinguen "profesor" de "staff" para aplicar el chequeo de dueño, y el `authz-starter 0.1.0` solo expone `@RequirePermission` (no una consulta "tiene permiso X" desde el código):

- `CohortOwnershipGuard.requireProfessorOwner` (`hasRole PROFESSOR`).
- `RankingController.rankingOf` (`hasRole PROFESSOR`).
- `HealthController.requireViewer` (`hasRole ADMIN` / `PROFESSOR`).

Con el starter hay dos caminos: pedirle a Users una consulta programática de permisos, o envolver cada uno en un método de `RoadmapAuthorizationService` con su `@RequirePermission` (como ya se hace con el resto) y atrapar el 403. Ninguno se resolvió acá: es decisión del dueño de #294.

## 7. Qué sigue

- Mergear #294 (hoy draft). Antes de prender `authz.mode=on` los permisos `roadmap.*` tienen que estar en el catálogo de Compose (`permissions.json`, `tpi-system-compose`); todavía no hay PR.
- Bug de CRLF en `.mvn/tpi-libs` (ver [[acuerdos/users]]): sin `.gitattributes` el `authz-starter` vendoreado no compila en Windows.
- Decidir los tres chequeos de la §6 y los dos pendientes del hallazgo 1.
- Si se agrega o cambia un endpoint, actualizar `permission-matrix.csv` (el test lo exige) y esta nota.
