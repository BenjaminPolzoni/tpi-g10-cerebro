---
tags: [tpi, g10, sprint-4, plan, back, front, permisos, roadmap]
fecha: 2026-11-05
autor: Benjamin Polzoni
estado: propuesta
actualizado: 2026-11-05
repo: 2026-P4-FE/2026-PIV-TPI-FE, 2026-P4-BE/tpi-roadmap
rama: BenjaminPolzoni/unified-node-creation-pages (front) · BenjaminPolzoni/gestor-admin-roadmap-authoring (back)
---

# Plan — Gestor y Admin arman el roadmap con desafíos (solo roadmap)

Continúa el [[sprints/sprint-4/Planes/Benja/Front - pantallas de creacion unificadas en la vista de nodos|plan de pantallas de creación unificadas]] (hueco 7).

> [!warning] Alcance: solo el roadmap (decisión de Benja, 2026-11-05)
> Se tocan **solo** el front (`2026-PIV-TPI-FE`, feature roadmap) y el back del roadmap (`tpi-roadmap`). **No se cambia ningún repo de otro grupo**: tpi-users, tpi-practical-challenge, tpi-theoristcal-challenge, tpi-engine-challenge ni tpi-course.

## Qué permite hoy el back del roadmap (`tpi-roadmap` develop `f382db61`, 2026-11-05)
- **Escritura del grafo** (crear, editar, mover y quitar nodos, unidades y reglas): `GraphController` con `roadmap.graph.write`, `legacyRoles={ADMIN,GESTOR,PROFESSOR}`. Los paquetes de PROFESSOR, GESTOR y ADMIN tienen ese código.
- **Pool de desafíos asignables**: `ChallengePoolController` y `ChallengeCoursesController` con `roadmap.challenge-pool.read` para los tres roles.
- **Dueño del curso**: `GraphViewController.requireEditor` y `RoadmapLayoutController.requireEditor` dejan pasar al *platform staff* (ADMIN o GESTOR, `common/security/Roles.isPlatformStaff`). Al profesor solo lo dejan pasar en sus comisiones (`CohortOwnershipClient.isOwner`).
- **Asignar un desafío a un nodo**: `services/GraphValidator.usableBy`. El staff de plataforma asigna **cualquier desafío publicado**. El profesor, solo los que él escribió.

**Conclusión:** para crear contenido, asignar desafíos existentes y quitar nodos, **el back del roadmap ya permite a Gestor y Admin**. No hace falta un cambio de back salvo que la verificación (B-01) muestre otra cosa.

## Lo que no se puede hacer desde el roadmap
- **Escribir un desafío nuevo** (las preguntas del teórico, la plantilla y las variantes del práctico) lo validan los servicios de otros grupos. Según el relevamiento del 2026-11-05, hoy solo aceptan PROFESSOR. El Motor ya acepta a los tres.
- Consecuencia en el front: **Gestor y Admin asignan un desafío existente y crean contenido teórico**. «Crear desafío nuevo» se ofrece solo a quien tiene `authorChallenges`, que hoy es PROFESSOR, como está.
- Si se quiere que Gestor y Admin también escriban el desafío, se **pide a esos grupos** con un issue en su repo. No lo cambiamos nosotros.
- **Hipótesis a verificar:** la subida de archivos de una lectura pasa por Courses (`CourseContentService`), de otro grupo. Hay que confirmar que acepta a Gestor y Admin. Si no, se muestra el error y se pide a ese grupo.

## Tareas

### Front (worktree `~/orca/workspaces/2026-PIV-TPI-FE/unified-node-creation-pages`)
- [ ] **F-01 Entrada a las pantallas.**
  - Las rutas `content/new`, `challenge/new` y `subsection/new` de `features/courses/courses.routes.ts` usan `permissionGuard('editRoadmap')` en lugar de `authorChallenges` en el `canMatch`.
  - Para esas rutas, `cohortProfessorGuard` deja pasar a quien tenga `editRoadmap` aunque no sea miembro de la comisión, como hace el back con el staff.
  - Verificar con la skill `tpi-front-permissions`.
- [ ] **F-02 Pantalla de desafío por capacidad.** En `ChallengeNodeCreatePageComponent`:
  - «Asignar desafío existente» del pool: para todos los que tienen `editRoadmap`.
  - «Crear desafío nuevo»: solo con `authorChallenges`.
  - Sin `authorChallenges`, la pantalla abre directo en «asignar existente», sin el botón de crear.
- [ ] **F-03 Escritura en la pantalla.** `facade.canWrite` y `isAdmin` deben quedar en `true` para Gestor y Admin sin membresía, para que el formulario no quede en solo lectura.
- [ ] **F-04 Mensajes de error claros.** Si un servicio externo responde 403 (subida de archivos o Motor), la pantalla lo dice con `GenericCallout tone="danger"` y no pierde el formulario.

### Back (worktree `~/orca/workspaces/tpi-roadmap/gestor-admin-roadmap-authoring`)
- [ ] **B-01 Verificación, sin código.** Por el gateway, como GESTOR y como ADMIN no miembros de la comisión:
  - Crear un nodo de contenido.
  - Crear un nodo desafío con un desafío publicado de otro autor.
  - Editarlo y quitarlo.
  - Leer el pool.
  - Usar el roadmap secundario y el filtro de comisión (`?roadmap=&group=`).
  - Skill `tpi-verify-integration`.
  - Si algo responde 403 en `tpi-roadmap`, se corrige ahí.
- [ ] **B-02 (solo si B-01 falla)** Ajustar el `requireEditor` o la regla de `tpi-roadmap` que falle, con un test de matriz: PROFESSOR dueño, PROFESSOR no dueño, GESTOR, ADMIN y STUDENT denegado.

> [!note] Hallazgo aparte (no pedido)
> `GraphValidator.usableBy` no deja que un profesor asigne un desafío escrito por **otro profesor de la misma comisión**: solo los suyos. No entra en este plan; anotarlo si aparece.

## Reglas para el agente
- Solo `2026-PIV-TPI-FE` (feature roadmap y las rutas de creación en courses) y `tpi-roadmap`.
- Sin tests mientras se programa; tests y verify solo antes de la PR. Una sola rama por repo. No pushear sin pedirlo.
