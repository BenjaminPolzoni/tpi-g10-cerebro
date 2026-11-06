---
tags: [tpi, g10, sprint-4, plan, back, front, permisos, challenges]
fecha: 2026-11-05
autor: Benjamin Polzoni
estado: propuesta
repo: 2026-P4-BE/tpi-users, 2026-P4-BE/tpi-practical-challenge, 2026-P4-BE/tpi-theoristcal-challenge, 2026-P4-FE/2026-PIV-TPI-FE
rama: feature/gestor-admin-challenge-authoring
---

# Plan — Gestor y Admin crean, editan y quitan desafíos

Continúa el [[sprints/sprint-4/Planes/Benja/Front - pantallas de creacion unificadas en la vista de nodos|plan de pantallas de creación unificadas]] (hueco 7). Pedido de Benja, 2026-11-05: Profesor, Gestor y Admin tienen que poder **crear, editar y quitar** desafíos teóricos y prácticos desde las pantallas de creación. Hoy lo frenan las validaciones del back.

> [!info] Análisis sobre `develop` del 2026-11-05
> - tpi-practical-challenge `9f76b27`
> - tpi-theoristcal-challenge `3a97e9c`
> - tpi-users `develop`
> - tpi-engine-challenge `main 66fffd85`
>
> Las rutas son relativas a `src/main/java/ar/edu/utn/frc/tup/p4/`.

## Cómo se autoriza hoy (dos capas en cada micro)
1. **Anotación** `@RequirePermission(code, legacyRoles)`.
   - Con `AUTHZ_MODE=on` manda el **código de permiso** del snapshot. Los códigos salen de los paquetes de fábrica de tpi-users (`users/permissions/FactoryPack.java` y migraciones `V179`, `V184`, `V206`).
   - Con `off`/`shadow` mandan los `legacyRoles` del token.
2. **Servicio**: regla por **rol en la comisión** (Courses: PROFESSOR, PROFESSOR_READ_ONLY, GESTOR) y, a veces, una excepción para el ADMIN de plataforma.

## Diagnóstico por micro

| Micro | Capa 1 (anotación + paquete) | Capa 2 (servicio) | ¿Qué falta? |
|---|---|---|---|
| **tpi-engine-challenge** (Motor: el desafío en sí, alta, edición, estado/archivo) | `ChallengeController` POST, PUT y PATCH `/estado` con `legacyRoles={PROFESSOR,ADMIN,GESTOR}`. Los paquetes GESTOR, ADMIN y ORG_ADMIN ya tienen `engine-challenge.challenge.write`. | `challenges/service/ChallengeAccess.java`: escriben PROFESSOR y GESTOR de la comisión; **el admin pasa todas las reglas**. | **Nada.** Ya permite. |
| **tpi-theoristcal-challenge** (cuestionario: contenido y preguntas) | `ContentController` POST y PUT con `legacyRoles={PROFESSOR,GESTOR}`, **sin ADMIN**. `ItemController` (preguntas: POST, PUT, DELETE, impact, categories), `ItemFileImportController`, `ItemImportTemplateController` y `SavedRubricController` **solo PROFESSOR**. Paquetes: GESTOR y ADMIN **no tienen** `theoretical-challenge.content.write`, `.item.write` ni `.item.read`. | `services/ContentAccessGuard.java`: `requireWriter` llama a `requireNotAdmin()`, **"el administrador solo lee el contenido"** (decisión explícita del equipo). `CourseBankGuard` sí deja escribir al GESTOR de la comisión. | Anotaciones: sumar GESTOR y ADMIN. Paquetes: sumar los códigos. Servicio: decidir lo del admin. |
| **tpi-practical-challenge** (payload práctico: plantilla, variantes, provisión, revisión) | `controllers/PracticalChallengeController` POST, PUT/PATCH `/{id}` y `/variants`; `workspace/web/TemplateAuthoringController` (`template/sync`, `validation`); `ChallengeProvisioningController`; `TemplateSnapshotController`; `DetectedCompositionController`; `vpcr/controllers/ReviewChallengeController`. **Todos solo PROFESSOR.** Paquetes: GESTOR y ADMIN no tienen `practical-challenge.challenge.write` ni `.challenge-authoring.read`. | `services/ChallengeAccessPolicy.java`: `EDIT_ROLES={PROFESSOR,GESTOR}` de la comisión. **No hay excepción para el admin**: si no es miembro de la comisión, `canEdit` da `false`. | Anotaciones y paquetes, como en el teórico. Servicio: sumar la excepción para el admin. |
| **tpi-users** (paquetes de fábrica) | `GESTOR`, `ADMIN` y `ORG_ADMIN` solo tienen `engine-challenge.challenge.write` y `roadmap.graph.write` de esta familia. | — | Migración nueva que agregue los códigos a esos paquetes y actualice el `FactoryPack.java` y la matriz `factory-packs-compose-matrix-vNNN.json`. |
| **Front** | `core/services/permissions.service.ts:31` `authorChallenges: ['PROFESSOR']`, también `manageChallengeVariants` y `readChallengeVariants`. | `cohortProfessorGuard`. | Abrir esas capacidades a GESTOR y ADMIN cuando el back esté. |

> [!warning] Hallazgos a confirmar
> - `practical-challenge.challenge-authoring.write` (`ReviewChallengeController` PUT y `/ready`) **no aparece en ningún paquete**, ni siquiera en PROFESSOR. Con `AUTHZ_MODE=on` podría estar denegado para todos. **Hipótesis**: verificar en el catálogo de compose.
> - El GESTOR ya figura en los `legacyRoles` del `ContentController` teórico, pero su paquete no tiene `theoretical-challenge.content.write`. Con `on` hoy queda afuera aunque el servicio lo acepte.
> - **"GESTOR" tiene dos sentidos**: el rol de plataforma (paquete) y el rol en la comisión (Courses). El servicio mira el de la comisión. Un gestor de plataforma que no es miembro de la comisión sigue rechazado por la capa 2. Hay que decidir si el gestor de plataforma pasa como el admin o si se lo agrega como miembro GESTOR de la comisión.

## Qué significa "quitar"
- **Sacar el nodo del roadmap**: `roadmap.graph.write`. Ya lo tienen los tres roles.
- **Archivar o desactivar el desafío**: Motor `PATCH /{id}/estado`. Ya lo tienen los tres roles. El chequeo previo teórico `GET /by-challenge/{id}/deactivation-check` ya admite PROFESSOR, GESTOR y ADMIN.
- **Borrar una pregunta del banco**: `DELETE /items/{id}`, hoy solo PROFESSOR.

## Decisiones a tomar antes de mandar el agente
- **D1 — Admin en el teórico.** `requireNotAdmin()` es una regla deliberada del equipo dueño (G04). Propuesta: que el admin escriba el cuestionario pero **siga sin corregir ni asentar notas** (`requireCorrector` no se toca). Coordinarlo con el equipo dueño en la PR.
- **D2 — Admin en el práctico.** Sumar en `ChallengeAccessPolicy.canEdit` una excepción para el admin (mismo criterio que `ChallengeAccess` del Motor: "admins pass every rule") que respete la organización (`OrganizationAccess`).
- **D3 — Gestor sin membresía.** ¿El gestor de plataforma escribe en cualquier comisión de su organización, igual que el admin? ¿O solo donde es miembro GESTOR? Recomendación: **solo donde es miembro**, que ya funciona en la capa 2. Así el cambio queda en anotaciones y paquetes.
- **D4 — Corrección y notas** (corregir intentos, ajustes de nota, credenciales Git del docente): **fuera de alcance**, siguen solo PROFESSOR.

## Tareas

### tpi-users
- [ ] **U-01** Migración `V2xx__gestor_admin_challenge_authoring.sql` (revisar la versión libre en develop y en las PRs abiertas, ver memoria «Flyway en tpi-roadmap»). Agrega a `GESTOR`, `ADMIN` y `ORG_ADMIN`:
  - `practical-challenge.challenge.write`
  - `practical-challenge.challenge.read`
  - `practical-challenge.challenge-authoring.read`
  - `practical-challenge.challenge-authoring.write` (si existe en el catálogo)
  - `theoretical-challenge.content.write`
  - `theoretical-challenge.item.read`
  - `theoretical-challenge.item.write`
- [ ] **U-02** Actualizar `FactoryPack.java` (`gestorPermissions()` y `adminPermissions()`) y la matriz `src/test/resources/permission-catalog/factory-packs-compose-matrix-vNNN.json`. Correr `FactoryPackCatalogueMigrationTest`.
- [ ] **U-03** Si el catálogo de compose no tiene algún código, sumarlo en tpi-system-compose (skill `tpi-adopt-permissions`).

### tpi-theoristcal-challenge
- [ ] **T-01** `legacyRoles` con `PROFESSOR, GESTOR, ADMIN` en las escrituras y lecturas de autoría:
  - `ContentController` (POST, PUT, `points`).
  - `ChallengeHistoryController` (`restore`, `points/impact`).
  - `ItemController` (todo).
  - `ItemFileImportController`.
  - `ItemImportTemplateController`.
  - `SavedRubricController`.
  - Mantener solo PROFESSOR las de corrección (`AttemptController` 349/385) y las de marketplace.
- [ ] **T-02** `ContentAccessGuard.requireWriter`: dejar escribir al admin según D1, sin tocar `requireCorrector`.
- [ ] **T-03** Ver si la autoría de ítems (categorías, `authorId`) asume un profesor: `ItemCategoryService` usa `authorId` "el profesor". Comprobar que un gestor o admin no cree ítems huérfanos ni invisibles para el profesor de la comisión.
- [ ] **T-04** Tests de matriz (permitido o denegado) por rol: PROFESSOR, GESTOR miembro, GESTOR no miembro, ADMIN, PROFESSOR_READ_ONLY (denegado), STUDENT (denegado).

### tpi-practical-challenge
- [ ] **P-01** `legacyRoles` con `PROFESSOR, GESTOR, ADMIN` en la autoría:
  - `PracticalChallengeController` POST, PUT/PATCH y `variants`.
  - `TemplateAuthoringController` (`sync`, `validation`, lecturas de autoría).
  - `ChallengeProvisioningController` (`retry` y lectura).
  - `TemplateSnapshotController`.
  - `DetectedCompositionController`.
  - `ReviewChallengeController`.
  - Las lecturas de catálogo de autoría (`PracticalTechnologyCatalogController`, `LlmGradingRubricController`, `composition/web/*`) cuando hoy son solo PROFESSOR.
- [ ] **P-02** `ChallengeAccessPolicy`: excepción para el admin en `canEdit` y `canView`, dentro de su organización (D2). Revisar `authoring/application/AuthoringOperationService.requireEditor` y el alta (quién puede crear en una comisión).
- [ ] **P-03** Sin cambios: `TeacherGit*`, `GradeAdjustmentController`, corrección (D4).
- [ ] **P-04** Tests de matriz como T-04.

### Front (2026-PIV-TPI-FE), después del back
- [ ] **F-01** `core/services/permissions.service.ts`: `authorChallenges`, `manageChallengeVariants` y `readChallengeVariants` pasan a `['PROFESSOR','GESTOR','ADMIN']`. Actualizar los comentarios que dicen que el back los rechaza.
- [ ] **F-02** En la pantalla de desafío, con el back listo, «crear nuevo» se ofrece a los tres roles (cierra el hueco 7 del plan de front).
- [ ] **F-03** Verificar con la skill `tpi-verify-integration`: crear, editar y archivar un desafío teórico y uno práctico como GESTOR y como ADMIN por el gateway.

## Reglas para el agente
- Cuatro worktrees, uno por repo, con la rama `feature/gestor-admin-challenge-authoring` desde `develop`. El front de este plan va en el worktree del front.
- Skills: `tpi-adopt-permissions` (anotaciones, paquetes, la trampa del handler final), `tpi-merge-develop` si hay colisión de Flyway, `tpi-verify-integration` para la evidencia.
- No tocar las reglas de corrección ni de notas. No pushear sin pedirlo.
