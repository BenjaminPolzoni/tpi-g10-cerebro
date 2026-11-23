---
tags: [presentacion, roadmap]
---

# Roles y permisos: quién hace qué

## Lo que decimos

«Antes de entrar al editor, veamos quién usa el recorrido. El docente responsable organiza mapas, configura el camino y consulta el seguimiento de su cohorte. El alumno encuentra los mapas habilitados para su cursada, recorre actividades y consulta su progreso y ranking. Gestión y administración tienen herramientas de alcance institucional, siempre dentro de la organización y de los permisos asignados. Administración también dispone de operaciones de mantenimiento; no por eso presentamos cada pantalla docente como su pantalla de inicio.

La clave es que **el nombre del rol no alcanza por sí solo**. La cuenta recibe permisos efectivos desde los packs y asignaciones; además, la operación se valida contra la organización y, cuando corresponde, contra el curso, la matrícula y la comisión. En modo de transición pueden seguir decidiendo los roles anteriores. Así, un docente con permiso de edición no edita automáticamente cualquier curso, y un alumno no accede a una cursada ajena por conocer una dirección.

> [!info]- Detalle técnico: permiso y pertenencia
> `@RequirePermission` protege la escritura del grafo y luego se verifica dueño; la lista de mapas exige matrícula y filtra por comisión para alumno. Ver `_presentacion-src/tpi-roadmap/src/main/java/com/utn/tpi/roadmap/controllers/GraphController.java:174-178` y `RoadmapManagementController.java:121-135`.

En el ingreso, Users autentica y emite la credencial; Gateway la valida y transmite identidad y organización confiables a Roadmap. Roadmap comprueba el permiso y las reglas del recurso. En el navegador, un snapshot de capacidades adapta menús y protege rutas, pero la decisión de seguridad se vuelve a tomar en el servidor. Cuando se comunican servicios, usan identidad técnica y scopes específicos, no una cuenta de alumno o docente.

> [!info]- Detalle técnico: identidad y modos
> Gateway limpia headers reservados y agrega identidad validada: `_presentacion-src/tpi-api-gateway/src/main/java/ar/edu/utn/frc/tup/p4/apigateway/filters/IdentityPropagationFilter.java:60-99`. Roadmap usa `AUTHZ_MODE`, `off` por defecto: `_presentacion-src/tpi-roadmap/src/main/resources/application.properties:16`; modos y despliegue: `_presentacion-src/tpi-roadmap/docs/identity-permissions-rollout.md:26`. `editRoadmap` usa el permiso de escritura: `_presentacion-src/fe/src/app/core/services/permissions.service.ts:142-144`, `:626`.

Para la demo usamos cuatro cuentas preparadas: docente dueño, alumno inscripto, gestor y administrador. Mostramos lo que cada una tiene habilitado, no prometemos que todas tengan los mismos permisos en cualquier instalación. El cierre académico sigue siendo responsabilidad de Courses; Roadmap aporta información de seguimiento. Más detalle y límites en [[A4-Limites-conocidos]] y [[A6-Preguntas-dificiles]].»

### Mapa de capacidades

Lectura orientativa de roles legacy y packs de fábrica; **✓ condicionado** a permisos efectivos, organización y controles de dominio, no es garantía de acceso en toda configuración. `P` = PROFESSOR/docente, `S` = STUDENT/alumno, `G` = GESTOR, `A` = ADMIN. Guion operativo en [[A1-Guion-de-demo]].

| Capacidad | Permiso de persona | P | S | G | A |
|---|---|:---:|:---:|:---:|:---:|
| Listar mapas y ver grafo | `roadmap.course-roadmaps.read`, `roadmap.graph.read` | ✓ dueño | ✓ matrícula/comisión | ✓ | ✓ |
| Crear, configurar y mostrar/ocultar mapas | `roadmap.course-roadmaps.write` | ✓ dueño | — | ✓ | ✓ |
| Editar grafo y reglas | `roadmap.graph.write` | ✓ dueño | — | ✓ | ✓ |
| Ranking de curso o mapa | `roadmap.ranking.read` | ✓ dueño, vista staff | ✓ propia/configurada | ✓ staff | ✓ staff |
| Dashboard de cohorte | `roadmap.dashboard.read` | ✓ dueño | — | ✓ | ✓ |
| Mi progreso (vista del alumno logueado: gate, nivel, inventario, cofres, calendario) | `roadmap.student-progress.read` | — | ✓ | — | — |
| Progreso de la cohorte, alumno por alumno (`GET /courses/{id}/progress`, `/roadmaps/{id}/progress`) | `roadmap.cohort-progress.read` + ser dueño o tener `roadmap.cohort-admin.read` | ✓ dueño | ✗ (pasa el permiso, cae en el control de dueño) | ✗ (ídem: no es dueño ni tiene `cohort-admin.read`) | ✓ |
| Detalle por alumno (avance por comisión, salud y nivel de un alumno) | `roadmap.students-progress.read` | ✓ dueño | — | ✗ no está en su pack de fábrica | ✓ |

> [!info]- Detalle técnico: por qué el gestor no ve el progreso por alumno
> Los cuatro packs de fábrica tienen `roadmap.cohort-progress.read` (`tpi-users/.../FactoryPack.java`), pero `ProgressController.cohortProgressOf` (`ProgressController.java:240-245`) llama además a `CohortOwnershipGuard.requireCohortViewer`, que solo deja pasar a servicios, al dueño de la cohorte o a quien tenga `roadmap.cohort-admin.read` (`CohortOwnershipGuard.java`, `RoadmapAuthorizationService.java:156-157`). Ese permiso solo está en el pack ADMIN. Para que el gestor lo vea alcanza con asignarle `roadmap.cohort-admin.read` y `roadmap.students-progress.read` en Users, sin tocar código.
| Mantenimiento técnico | `roadmap.maintenance.write` | — | — | — | ✓ |
| Cierre académico | No se confirma permiso de cierre en Roadmap | — | — | — | — |

> [!info]- Detalle técnico: alcance de la tabla
> Matriz legacy y packs: `_presentacion-src/tpi-roadmap/docs/T-22-1-MATRIZ-PERMISOS.md:10-40` y `_presentacion-src/tpi-users/src/main/java/ar/edu/utn/frc/tup/p4/usersservice/users/permissions/FactoryPack.java:176-182`, `:351-361`, `:494-505`, `:704-719`. Hay controles adicionales y excepciones por endpoint: [[07-roles-y-permisos]]. La publicación de desafíos corresponde al Motor, no equivale a mostrar un mapa.

> [!info]- Detalle técnico: qué es «mantenimiento técnico» (`roadmap.maintenance.write`)
> Son 5 endpoints de operación, bajo `/admin/...` en la ruta privada, solo para ADMIN (legacy) o quien tenga el permiso. No tienen pantalla en el front: se usan para reparar datos, no en el uso diario.
> - `POST /admin/graph/rebuild`: reconstruye Neo4j entero copiando todos los roadmaps desde Postgres, incluidos los dados de baja (`GraphAdminController.java:38-39`).
> - `POST /admin/graph/reconcile`: compara Neo4j con Postgres y marca en `graph_sync_pending` los roadmaps que difieren para que se reproyecten (`GraphAdminController.java:54-55`).
> - `POST /admin/outbox/{eventId}/retry`: vuelve a PENDING un evento Kafka del outbox que quedó FAILED y limpia su error y backoff (`OutboxAdminController.java:40-41`).
> - `POST /admin/outbox/retry-failed`: lo mismo para todos los eventos FAILED (`OutboxAdminController.java:59-60`).
> - `POST /admin/boundary-nodes/backfill`: agrega START («Bienvenidos») y END («Felicitaciones») a las unidades viejas que no los tienen (`BoundaryNodeAdminController.java:34-35`).

### Cómo se otorga un permiso en Roadmap

1. **Catálogo:** Roadmap define los códigos `roadmap.*`, que se sincronizan con Users.
2. **Asignación:** Users asigna los permisos a cada cuenta mediante *packs* (de fábrica o asignados), no por el nombre del rol, y emite el JWT al iniciar sesión.
3. **Gateway:** valida el token, borra los headers de identidad que traiga el cliente e inyecta en Roadmap la identidad y la organización verificadas.
4. **Roadmap, en dos capas:**
   - `@RequirePermission` en cada endpoint exige el código de permiso. Modos de `AUTHZ_MODE`: `off` (deciden los roles legacy), `shadow` (deciden los roles legacy y se registran las diferencias con el permiso nuevo) y `on` (decide solo el permiso).
   - Control del recurso: organización coincidente, docente dueño de la cohorte, alumno inscripto y filtrado por su comisión.
5. **Front:** el snapshot de capacidades muestra menús y protege rutas; es comodidad, el back vuelve a validar.
6. **Servicios (M2M):** token técnico con scopes propios, nunca los permisos de una persona.

> [!warning] Antes de la demo
> `AUTHZ_MODE` viene en `off` por defecto (`_presentacion-src/tpi-roadmap/src/main/resources/application.properties:16`): si el ambiente no lo cambió, deciden los roles legacy y no los permisos. Confirmar el modo del ambiente y contarlo en consecuencia.

```mermaid
flowchart LR
 U[Cuenta] --> L[Users: login y JWT]
 L --> G[Gateway: valida token, limpia e inyecta identidad y organización]
 G --> R[Roadmap: organización y permiso o rol legacy]
 R --> D[Curso: dueño, matrícula y comisión según operación]
 D --> V[Respuesta autorizada]
 L --> F[Front: snapshot de capacidades, menú y guard]
 F --> G
 M[Servicio: token técnico y scope] --> G
```

## Qué se ve en pantalla

Mostrar el ingreso y la organización de cada cuenta preparada. Docente: lista y editor de su cohorte; alumno: mapas de su comisión, progreso y ranking; gestor: lista/dashboard que su cuenta efectivamente permita; admin: acceso institucional o mantenimiento solo si está ensayado. No efectuar cambios destructivos ni cierre real.

## Preguntas probables

**¿El docente puede editar cualquier curso?** No: además del permiso, las escrituras comprobadas exigen dueño salvo el bypass de staff aplicable.

**¿Se puede ocultar un botón y considerar protegido el dato?** No: el front facilita navegación; el backend valida por separado.

**¿Un servicio tiene los permisos del alumno?** No: se identifica como servicio y usa scopes explícitos en rutas que lo admiten.

**¿Ya probamos las cuatro cuentas integradas?** No en este trabajo; hay que verificar organización, packs, modo y datos antes de la demo.
