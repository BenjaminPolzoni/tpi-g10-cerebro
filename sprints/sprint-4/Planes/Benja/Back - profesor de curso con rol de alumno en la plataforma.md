---
tags: [tpi, g10, sprint-4, plan, back, roadmap, permisos]
fecha: 2026-11-06
autor: Benjamin Polzoni
estado: propuesta
repo: 2026-P4-BE/tpi-roadmap
rama: (a crear desde origin/develop f382db61)
---

# Plan — Profesor de un curso que en la plataforma es alumno

## Problema (visto el 2026-11-06)
Un usuario con rol de plataforma **STUDENT** figura como **Profesor** en la membresía de un curso (`tpi-course`). Al entrar al curso:
- El **front** decide por la membresía del curso y le muestra la vista de profesor.
- El **back** (`tpi-roadmap`) decide por los permisos del token y lo trata como **alumno**. Busca en qué comisiones está como alumno, no encuentra ninguna y responde **403 `ROADMAP_NOT_VISIBLE`** («Este roadmap no está habilitado para tu comisión») en `GET /api/roadmap/courses/{id}`.

Resultado: el resto de la página carga, pero el mapa y los nodos del curso quedan vacíos. Le pasa, por ejemplo, a un ayudante que en la plataforma es alumno.

## Estado actual (relevado en `origin/develop` f382db61)
- **`security/StudentViewer.idOf`** decide si quien consulta es «solo alumno»:
  - Es alumno si tiene el permiso de alumno (`isStudentSelf`).
  - No es alumno si es staff de plataforma (`isPlatformStaff`) o tiene `roadmap.graph.write` (`isGraphEditor`).
  - **No mira la membresía del curso.**
- **Dónde se usa (12 lugares):**
  - `RoadmapResolver.ofCourse` (:85), donde nace el 403;
  - `RoadmapResolver.ofRoadmap` (:118);
  - `GraphController.roadmapFor` (:148);
  - `GraphViewController` (:93);
  - `RoadmapLayoutController` (:60);
  - `RoadmapLayoutService` (:73);
  - `RoadmapManagementController` (:130);
  - `CohortChallengesController` (:83);
  - `ProgressController` (:156, :177);
  - `StudentDashboardController` (:71, :77).
- **Cómo se ve la comisión del alumno.** `RoadmapResolver.ofCourse` se queda con los roadmaps que `management.visibleTo` (por comisión, `RoadmapVisibilityService.groupsOf` → `groupsByStudent`) deja ver. Si no queda ninguno, tira 403 `roadmap.not-visible` (:97).
- **El back ya sabe preguntar por la membresía docente.** `CohortOwnershipClient.isOwner(userId, cohortId)` (`HttpCohortOwnershipClient`, :109) llama a Courses `GET .../teaching-memberships/{userId}` con token técnico. 200 confirma la membresía y 403/404 la niegan. Tiene caché Caffeine y recuerda las fallas. Ya lo usan `requireOwner` y `CohortOwnershipGuard`.
- **Escrituras.** `@RequirePermission("roadmap.graph.write", legacyRoles = ADMIN, GESTOR, PROFESSOR)` rechaza a un STUDENT de plataforma antes de mirar el curso. En el front, el editor de grafo también pide `editRoadmap`, así que hoy ese usuario no llega a editar.

## Propuesta
**Solo lectura:** quien es docente de **ese** curso según Courses ve el roadmap como lo ve el staff, aunque su rol de plataforma sea STUDENT. Es decir, ve el roadmap completo sin filtrar por comisión y no le pide estar inscripto. Las escrituras no cambian.

- `StudentViewer` suma una variante con curso: `idOf(authentication, access, courseCohortId, ownership)`.
- Esa variante devuelve vacío («no es alumno») cuando el usuario tiene el permiso de alumno pero `ownership.isOwner(userId, courseCohortId)` dice que es docente del curso.
- Solo consulta Courses cuando el usuario ya pasó como alumno, así que staff y servicios no pagan la llamada.
- Los alumnos reales hacen una consulta por curso, y queda en caché.
- **Si Courses no responde:** se lo trata como alumno (comportamiento de hoy) y se registra un warning. No se abre acceso con una consulta caída.

## Tareas
- [ ] **P-01 Test que reproduce el 403.** Un usuario STUDENT de plataforma, docente del curso según Courses y sin comisión, pide `GET /courses/{id}` → hoy 403 `roadmap.not-visible`. El test tiene que fallar antes del cambio.
- [ ] **P-02 `StudentViewer` con curso.** Agregar la variante con `courseCohortId` y `CohortOwnershipClient`, con la regla de la propuesta. La firma vieja queda solo para los casos sin curso.
- [ ] **P-03 Lecturas del roadmap.** Usar la variante en `RoadmapResolver.ofCourse` y `ofRoadmap`, `GraphController.roadmapFor`, `GraphViewController`, `RoadmapLayoutController` y `RoadmapLayoutService`, y `RoadmapManagementController` (listado de roadmaps).
- [ ] **P-04 Revisar el resto de los usos.** En `ProgressController`, `StudentDashboardController` y `CohortChallengesController`, ver uno por uno si hay que cambiar algo. En el progreso propio del alumno lo correcto es seguir tratándolo como alumno: no se cambia sin motivo.
- [ ] **P-05 Falla de Courses.** Si `isOwner` tira `OwnershipUnavailableException`, se lo trata como alumno, se loguea un warning y hay un test.
- [ ] **P-06 Verificación.** `./mvnw verify`, y además probarlo en el entorno compartido con el usuario del caso (alumno en la plataforma, profesor en el curso): el mapa del curso carga y no hay 403.

## Fuera de alcance
- **Que ese usuario pueda editar** el roadmap. Hace falta que los permisos de escritura miren la membresía del curso y no solo el rol de plataforma. Eso toca el catálogo de permisos y `authz-starter`, que no son nuestros: si se quiere, se abre un issue para quien los mantiene.
- **El front:** sigue mostrando la vista de profesor según la membresía y no necesita cambios para leer.

## Preguntas abiertas
1. ¿Está bien que un docente del curso con rol de alumno en la plataforma vea el roadmap **completo**, sin filtrar por comisión, como lo ve un profesor? ¿O debería ver solo lo de las comisiones donde da clase?
2. ¿Hay que confirmar con el equipo de Courses que `teaching-memberships` responde 200 también para «Profesor de solo lectura» (ReadOnlyProfessor)?
