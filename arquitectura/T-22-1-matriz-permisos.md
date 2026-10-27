---
tags: [tpi, g10, roadmap, sprint-3, seguridad, permisos]
tarea: "T-22.1 (#9090)"
historia: "[[sprints/sprint-3/historias/HT-22 Permisos en vez de roles|HT-22]]"
estado: propuesta
actualizado: 2026-10-23
---

# T-22.1 — Matriz de permisos del micro

**Historia:** [[sprints/sprint-3/historias/HT-22 Permisos en vez de roles|HT-22]] · **Taiga:** #9090 · Cierra **DT-03** de [[deuda-tecnica]].

Copia de `tpi-roadmap/docs/T-22-1-MATRIZ-PERMISOS.md`. Si cambia, se actualizan las dos.

Lista cada endpoint de `tpi-roadmap` con el permiso que va a pedir y quién lo tiene hoy. Hoy se autoriza
por rol (`hasRole` / `hasAnyRole` en las constantes `CAN_*` de cada controller), más los chequeos de
dueño del curso (`requireOwner` y parecidos) y las reglas de servicio de `SecurityConfig`.

> **Estado: propuesta.** Los nombres se acuerdan con Users (G07), que es dueño del catálogo (T-22.2).
> Hasta entonces se sigue autorizando por rol ([[sprints/sprint-3/08-dudas|duda G6]]). Relevado sobre `develop` en `04c3d1ac`
> (2026-10-23): 25 controllers, 82 endpoints.

---

## 1. Cómo leer la matriz

- **Permiso propuesto:** lo que pediría el `@PreAuthorize` con `hasAuthority('roadmap.…')` (T-22.3).
- **ADMIN / GESTOR / PROFESSOR / STUDENT:** roles que pasan hoy el `@PreAuthorize`. **propio** quiere decir
  que el alumno pasa solo cuando consulta sus datos (`#studentId == authentication.principal`).
- **Servicio:** identidad técnica (`ServiceIdentity`) que deja el Gateway para las llamadas entre micros.
- **Alcance hoy:** lo que se chequea además del rol. El permiso **no lo reemplaza**: el chequeo de dueño del
  curso se mantiene (HT-22).
- ⚠️ marca un chequeo que falta o que no es igual al del resto (ver §3).

## 2. Catálogo de permisos propuesto

Convención: `roadmap.<recurso>.<acción>`, como pide la HT-22. Se reusan los tres scopes de servicio que
ya existen en `SecurityConfig` (`roadmap.progress.read`, `roadmap.health.read`,
`roadmap.restrictions.read`), así el usuario y el servicio piden el mismo nombre.

| Permiso | Qué permite |
|---|---|
| `roadmap.graph.read` | Ver el roadmap, el grafo y el detalle de nodos. El alumno ve lo de su comisión. |
| `roadmap.graph.edit` | Editar secciones, nodos, reglas, prerrequisitos, relaciones y tipos ocultos; sincronizar secciones; ver el historial de edición y la validación de estructura. |
| `roadmap.roadmaps.read` | Listar los roadmaps del curso. |
| `roadmap.roadmaps.manage` | Ajustes del curso; crear, renombrar, asignar comisiones, archivar y clonar roadmaps. |
| `roadmap.badges.read` | Ver las insignias de un alumno. |
| `roadmap.badges.manage` | Catálogo de insignias del curso (alta, edición y baja). |
| `roadmap.challenge-pool.read` | Pool de desafíos del curso y cursos de un desafío. |
| `roadmap.restrictions.read` | Ventana de fechas de un desafío (scope de servicio existente). |
| `roadmap.mentor.read` / `roadmap.mentor.edit` | Ver / cambiar el personaje guía del curso. |
| `roadmap.progress.read` | Progreso de otro alumno, de la cohorte o de una comisión; historial de XP y nivel de un alumno (scope de servicio existente). |
| `roadmap.health.read` | Salud de un alumno (scope de servicio existente). |
| `roadmap.ranking.read` | Ranking del curso o de un roadmap. La vista depende de quién pide. |
| `roadmap.learning.read` | Lo del propio alumno: materiales, avance de lectura, nivel, salud, inventario y elegibilidad. |
| `roadmap.learning.write` | Marcar un contenido como leído. |
| `roadmap.avatar.read` / `roadmap.avatar.edit` | Ver / guardar el avatar y la mascota propios. |
| `roadmap.gate.read` | Scope del servicio que consulta el gate (Motor), T-22.4. |
| `roadmap.maintenance.run` | Operaciones de plataforma: reconstruir y reconciliar el grafo, backfill de nodos frontera. |

### Rol → permisos, como queda hoy

| Permiso | Endpoints | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| `roadmap.avatar.edit` | 2 |  |  |  | ✔ |  |
| `roadmap.avatar.read` | 4 |  |  |  | ✔ |  |
| `roadmap.badges.manage` | 4 | ✔ |  | ✔ |  |  |
| `roadmap.badges.read` | 1 | ✔ |  | ✔ | propio |  |
| `roadmap.challenge-pool.read` | 2 | ✔ | ✔ | ✔ |  |  |
| `roadmap.gate.read` (scope) | 1 |  |  |  |  | ✔ |
| `roadmap.graph.edit` | 25 | ✔ | ✔ | ✔ |  |  |
| `roadmap.graph.read` | 7 | ✔ | ✔ | ✔ | ✔ |  |
| `roadmap.health.read` | 1 | ✔ |  | ✔ |  | ✔ |
| `roadmap.learning.read` | 9 |  |  |  | ✔ |  |
| `roadmap.learning.write` | 1 | ✔ |  |  | ✔ |  |
| `roadmap.maintenance.run` | 3 | ✔ |  |  |  |  |
| `roadmap.mentor.edit` | 1 | ✔ | ✔ | ✔ |  |  |
| `roadmap.mentor.read` | 1 | ✔ | ✔ | ✔ | ✔ |  |
| `roadmap.progress.read` | 8 | ✔ |  | ✔ | propio | ✔ |
| `roadmap.ranking.read` | 2 | ✔ | ✔ | ✔ | ✔ |  |
| `roadmap.restrictions.read` | 1 | ✔ |  | ✔ |  | ✔ |
| `roadmap.roadmaps.manage` | 7 | ✔ | ✔ | ✔ |  |  |
| `roadmap.roadmaps.read` | 1 | ✔ | ✔ | ✔ | ✔ |  |
| — (público) | 1 | ✔ | ✔ | ✔ | ✔ |  |

## 3. Hallazgos (para T-22.3, no se cambian en esta tarea)

1. **El GESTOR no recibe el mismo trato en todos lados.** Desde [[decisiones/DEC-009-gestores-editan-roadmaps|DEC-009]] pasa el chequeo de dueño como ADMIN
   en el grafo, el pool, el mentor, el sync, las relaciones, la validación, los roadmaps, la vista del grafo
   y el ranking. Pero **no** tiene acceso al catálogo de insignias (`BadgeCatalogController`), al nivel de un
   alumno (`LevelController`), a la salud de un alumno (`HealthController`) ni al progreso de la cohorte o de
   una comisión (`ProgressController`, `GroupProgressController`). Con permisos, esto pasa a ser una decisión
   de la matriz y no de cada `requireOwner`.
2. **Un profesor puede leer datos de cualquier curso**, porque en estos endpoints alcanza con el rol y no se
   chequea que sea dueño:
   - ~~progreso de un alumno (`/students/{studentId}/progress`, por curso y por roadmap)~~;
   - ~~historial de XP (`/students/{studentId}/xp-history`)~~;
   - ~~insignias de un alumno (`/students/{studentId}/badges`; el service solo exige que el alumno esté inscripto)~~;
   - ventana de un desafío (`/challenges/{challengeId}/window`);
   - roadmap y detalle de nodo (`GET /courses/{courseId}`, `GET /roadmaps/{roadmapId}`, `/nodes/{nodeId}`).

   ✅ **Resuelto (2026-10-25)** para progreso, XP e insignias: [tpi-roadmap#343](https://github.com/2026-P4-BE/tpi-roadmap/pull/343).
   Quedan pendientes la ventana del desafío y el roadmap/detalle de nodo; conviene sumarles el chequeo de dueño
   en T-22.3, o abrir un issue aparte si se prefiere no esperar.
3. **El gate acepta cualquier servicio.** `SecurityConfig` deja pasar a toda `ServiceIdentity` en
   `/students/{studentId}/nodes/{nodeId}/eligibility` sin mirar el scope (DT-01). Lo resuelve T-22.4 con
   `roadmap.gate.read`.
   ✅ **Resuelto (2026-10-25)** en `develop`: `402a4094`.
4. **`POST /nodes/{nodeId}/read` acepta ADMIN**, pero marca la lectura con el id de quien llama: un ADMIN se
   marca a sí mismo como alumno. Parece un resto; con permisos quedaría solo para el alumno
   (`roadmap.learning.write`).
5. **Los servicios solo entran a cuatro rutas:** gate, salud de un alumno, progreso de la cohorte y ventana
   de un desafío. El resto de `/api/roadmap/**` exige un usuario (`principal` de tipo `UUID`).
6. **Los chequeos de dueño están copiados en cada controller** (`requireOwner`, `requireEditor`,
   `requireViewer`, `requireCohortViewer`, `validated`), y por eso difieren. T-22.3 puede juntarlos en un solo
   componente.

## 4. Matriz por endpoint

Rutas relativas a `/api/roadmap`. Agrupadas por controller.

### BadgeCatalogController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/badges` | `roadmap.badges.manage` | ✔ |  | ✔ |  |  | Dueño del curso (ADMIN sin chequeo) |
| POST | `/courses/{courseId}/badges` | `roadmap.badges.manage` | ✔ |  | ✔ |  |  | Dueño del curso (ADMIN sin chequeo) |
| PUT | `/courses/{courseId}/badges/{badgeId}` | `roadmap.badges.manage` | ✔ |  | ✔ |  |  | Dueño del curso (ADMIN sin chequeo) |
| DELETE | `/courses/{courseId}/badges/{badgeId}` | `roadmap.badges.manage` | ✔ |  | ✔ |  |  | Dueño del curso (ADMIN sin chequeo) |

### BadgeController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/students/{studentId}/badges` | `roadmap.badges.read` | ✔ |  | ✔ | propio |  | El propio alumno, ADMIN o profesor dueño |

### BoundaryNodeAdminController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| POST | `/admin/boundary-nodes/backfill` | `roadmap.maintenance.run` | ✔ |  |  |  |  | Operación de plataforma |

### ChallengeCoursesController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/challenges/{challengeId}/courses` | `roadmap.challenge-pool.read` | ✔ | ✔ | ✔ |  |  | El profesor ve solo sus cursos; ADMIN y GESTOR todos |
| GET | `/challenges/{challengeId}/world` | `roadmap.graph.read` | ✔ | ✔ | ✔ | ✔ |  | Cualquier usuario con el rol |

### ChallengePoolController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/challenge-pool` | `roadmap.challenge-pool.read` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |

### ChallengeWindowController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseCohortId}/challenges/{challengeId}/window` | `roadmap.restrictions.read` | ✔ |  | ✔ |  | ✔ | Servicio con el scope, o usuario; sin chequeo de dueño ⚠️ |

### CourseMentorController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/mentor` | `roadmap.mentor.read` | ✔ | ✔ | ✔ | ✔ |  | Cualquier usuario con el rol |
| PUT | `/courses/{courseId}/mentor` | `roadmap.mentor.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |

### GateController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/students/{studentId}/nodes/{nodeId}/eligibility` | `roadmap.gate.read` (scope) |  |  |  |  | ✔ | Solo servicio con el scope; 403 sin él (T-22.4, `402a4094`) |
| GET | `/courses/{courseId}/nodes/{nodeId}/eligibility` | `roadmap.learning.read` |  |  |  | ✔ |  | El propio alumno (id del token) |

### GraphAdminController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| POST | `/admin/graph/rebuild` | `roadmap.maintenance.run` | ✔ |  |  |  |  | Operación de plataforma |
| POST | `/admin/graph/reconcile` | `roadmap.maintenance.run` | ✔ |  |  |  |  | Operación de plataforma |

### GraphController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}` | `roadmap.graph.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno: su comisión; staff sin chequeo de dueño ⚠️ |
| GET | `/roadmaps/{roadmapId}` | `roadmap.graph.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno: su comisión; staff sin chequeo de dueño ⚠️ |
| POST | `/courses/{courseId}/sections` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| POST | `/roadmaps/{roadmapId}/sections` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PUT | `/sections/{sectionId}` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/sections/{sectionId}` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| DELETE | `/sections/{sectionId}` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| POST | `/sections/{sectionId}/nodes` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PUT | `/nodes/{nodeId}` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/nodes/{nodeId}` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| DELETE | `/nodes/{nodeId}` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/nodes/{nodeId}/availability` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/nodes/{nodeId}/mandatory` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/nodes/{nodeId}/content` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/nodes/{nodeId}/prerequisite-mode` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/nodes/{nodeId}/rules` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/sections/{sectionId}/rules` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| GET | `/nodes/{nodeId}/edit-log` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| POST | `/nodes/{nodeId}/prerequisites` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |

### GraphViewController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/roadmaps/{roadmapId}/graph` | `roadmap.graph.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno: su comisión; staff: dueño (ADMIN y GESTOR sin chequeo) |
| GET | `/courses/{courseId}/graph` | `roadmap.graph.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno: su comisión; staff: dueño (ADMIN y GESTOR sin chequeo) |

### GroupProgressController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/groups/{groupId}/progress` | `roadmap.progress.read` | ✔ |  | ✔ |  |  | ADMIN o profesor dueño |

### HealthController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/students/me/health` | `roadmap.learning.read` |  |  |  | ✔ |  | El propio alumno (id del token) |
| GET | `/courses/{courseId}/students/{studentId}/health` | `roadmap.health.read` | ✔ |  | ✔ |  | ✔ | Servicio con el scope, ADMIN o profesor dueño (GESTOR no) |

### InventoryController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/inventory` | `roadmap.learning.read` |  |  |  | ✔ |  | El propio alumno (id del token) |

### LevelController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/students/me/level` | `roadmap.learning.read` |  |  |  | ✔ |  | El propio alumno (id del token) |
| GET | `/courses/{courseId}/students/{studentId}/level` | `roadmap.progress.read` | ✔ |  | ✔ |  |  | ADMIN o profesor dueño (GESTOR no) |
| GET | `/roadmaps/{roadmapId}/students/me/level` | `roadmap.learning.read` |  |  |  | ✔ |  | El propio alumno (id del token) |
| GET | `/roadmaps/{roadmapId}/students/{studentId}/level` | `roadmap.progress.read` | ✔ |  | ✔ |  |  | ADMIN o profesor dueño (GESTOR no) |

### NodeController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/nodes/{nodeId}` | `roadmap.graph.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno: lo que le toca ver; staff sin chequeo de dueño ⚠️ |
| GET | `/roadmaps/{roadmapId}/nodes/{nodeId}` | `roadmap.graph.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno: lo que le toca ver; staff sin chequeo de dueño ⚠️ |
| GET | `/courses/{courseId}/materials` | `roadmap.learning.read` |  |  |  | ✔ |  | El propio alumno, inscripto (403 student.not-enrolled) |
| GET | `/roadmaps/{roadmapId}/materials` | `roadmap.learning.read` |  |  |  | ✔ |  | El propio alumno, inscripto (403 student.not-enrolled) |

### PingController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/public/ping` | — (público) | ✔ | ✔ | ✔ | ✔ |  | Sin autenticación |

### ProgressController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| POST | `/nodes/{nodeId}/read` | `roadmap.learning.write` | ✔ |  |  | ✔ |  | El propio alumno |
| GET | `/courses/{courseId}/students/{studentId}/progress` | `roadmap.progress.read` | ✔ |  | ✔ | propio |  | El propio alumno, ADMIN o profesor dueño |
| GET | `/roadmaps/{roadmapId}/students/{studentId}/progress` | `roadmap.progress.read` | ✔ |  | ✔ | propio |  | El propio alumno, ADMIN o profesor dueño |
| GET | `/courses/{courseId}/progress` | `roadmap.progress.read` | ✔ |  | ✔ |  | ✔ | Servicio con el scope, ADMIN o profesor dueño |
| GET | `/roadmaps/{roadmapId}/progress` | `roadmap.progress.read` | ✔ |  | ✔ |  | ✔ | Servicio con el scope, ADMIN o profesor dueño |
| GET | `/courses/{courseId}/sections/{sectionId}/reading-progress` | `roadmap.learning.read` |  |  |  | ✔ |  | El propio alumno (id del token) |
| GET | `/roadmaps/{roadmapId}/sections/{sectionId}/reading-progress` | `roadmap.learning.read` |  |  |  | ✔ |  | El propio alumno (id del token) |

### RankingController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/ranking` | `roadmap.ranking.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno inscripto (vista anónima); profesor dueño; ADMIN y GESTOR todos |
| GET | `/roadmaps/{roadmapId}/ranking` | `roadmap.ranking.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno inscripto (vista anónima); profesor dueño; ADMIN y GESTOR todos |

### RoadmapManagementController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/settings` | `roadmap.roadmaps.manage` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PUT | `/courses/{courseId}/settings` | `roadmap.roadmaps.manage` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| GET | `/courses/{courseId}/roadmaps` | `roadmap.roadmaps.read` | ✔ | ✔ | ✔ | ✔ |  | Alumno inscripto; staff: dueño (ADMIN y GESTOR sin chequeo) |
| POST | `/courses/{courseId}/roadmaps` | `roadmap.roadmaps.manage` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PATCH | `/roadmaps/{roadmapId}` | `roadmap.roadmaps.manage` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PUT | `/roadmaps/{roadmapId}/groups` | `roadmap.roadmaps.manage` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| POST | `/roadmaps/{roadmapId}/archive` | `roadmap.roadmaps.manage` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| POST | `/roadmaps/{roadmapId}/clone` | `roadmap.roadmaps.manage` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |

### SectionSyncController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| POST | `/courses/{courseId}/sections/sync` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |

### StructureValidationController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/validation` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| GET | `/roadmaps/{roadmapId}/validation` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |

### StudentAvatarController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/students/me/avatar` | `roadmap.avatar.read` |  |  |  | ✔ |  | El propio alumno |
| PUT | `/students/me/avatar` | `roadmap.avatar.edit` |  |  |  | ✔ |  | El propio alumno |
| GET | `/courses/{courseId}/students/me/avatar` | `roadmap.avatar.read` |  |  |  | ✔ |  | El propio alumno |
| PUT | `/courses/{courseId}/students/me/avatar` | `roadmap.avatar.edit` |  |  |  | ✔ |  | El propio alumno |
| GET | `/courses/{courseId}/students/me/pet` | `roadmap.avatar.read` |  |  |  | ✔ |  | El propio alumno |
| GET | `/students/me/pet` | `roadmap.avatar.read` |  |  |  | ✔ |  | El propio alumno |

### TypedRelationController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/roadmaps/{roadmapId}/relations` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| POST | `/roadmaps/{roadmapId}/relations` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| DELETE | `/roadmaps/{roadmapId}/relations/{relationId}` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| GET | `/roadmaps/{roadmapId}/hidden-relation-types` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |
| PUT | `/roadmaps/{roadmapId}/hidden-relation-types` | `roadmap.graph.edit` | ✔ | ✔ | ✔ |  |  | Dueño del curso (ADMIN y GESTOR sin chequeo) |

### XpHistoryController

| Método | Ruta | Permiso propuesto | ADMIN | GESTOR | PROFESSOR | STUDENT | Servicio | Alcance hoy |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| GET | `/courses/{courseId}/students/{studentId}/xp-history` | `roadmap.progress.read` | ✔ |  | ✔ | propio |  | El propio alumno, ADMIN o profesor dueño |

## 5. Qué sigue

- **T-22.2:** mandar esta matriz a G07 y acordar los nombres y cómo llegan los permisos (token o headers del
  Gateway). El Gateway avisó que va a dejar de mandar `X-User-Roles` para mandar permisos.
- **T-22.3:** pasar cada `@PreAuthorize` a `hasAuthority('roadmap.…')` con esta tabla, juntar los chequeos de
  dueño y resolver los hallazgos 1, 2 y 4. Cada endpoint con su test de permitido y 403.
- **T-22.4:** ✅ hecho en `develop` (`402a4094`, 2026-10-25): el gate exige `roadmap.gate.read`.
- Si se agrega o cambia un endpoint antes de T-22.3, sumarlo a esta tabla.
