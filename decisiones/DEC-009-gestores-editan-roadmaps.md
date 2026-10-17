---
tags: [tpi, g10, decision, seguridad, roles]
fecha: 2026-10-11
estado: aceptada
reemplaza: ""
---

# DEC-009: Los gestores pueden editar el roadmap de cualquier curso

## Contexto
La regla de edición era "ADMIN o profesor a cargo". Un usuario con rol `GESTOR` (rol de Users para la gestión de la plataforma) recibía `403` al intentar editar el grafo, el pool de desafíos o el sync de un curso.

## Decisión
`Roles.GESTOR` se suma a `ADMIN` en `CAN_EDIT` de `GraphController`, `ChallengePoolController` y `SectionSyncController`, y **omite la verificación de pertenencia al curso** (`requireOwner`), igual que ADMIN. El profesor sigue limitado a sus cohortes (pertenencia docente M2M con Courses).

## Alternativas descartadas
- **Mantener solo ADMIN + profesor dueño**: era el estado previo; dejaba al gestor sin poder operar.
- **Exigir pertenencia también al gestor**: no tiene docencia asignada por cohorte.

## Consecuencias
- Positivas: el gestor opera cualquier curso (editor, pool, sync).
- Negativas / deuda:
  - Alcance amplio: gestor equivale a ADMIN en edición; el pool dejó de filtrar por autor para admin y gestor (`1dbdd81`).
  - El vocabulario de roles debe alinearse con Courses (`MANAGER`, "GESTOR o PROFESOR") y Users.
  - El rol `GESTOR` ya existía en Users; Courses documenta un vocabulario distinto, así que conviene fijar un solo catálogo de roles.
- **Actualización (2026-10-17):** en T-45.9 el gestor también ve el **ranking** de cualquier cohorte como ADMIN (vista de staff con todas las comisiones), vía `Roles.isPlatformStaff` en `RankingController`. Cuando el Gateway pase a mandar permisos en vez de roles, esto se migra con [[sprints/sprint-3/historias/HT-22 Permisos en vez de roles|HT-22]].

## Referencias
- Código / PR / doc: `d64b097` (PR #188, 2026-10-11), `common/security/Roles`, `GraphController`, `ChallengePoolController`, `SectionSyncController`; tests `GraphEditorScenariosTest`, `ChallengePoolControllerTest`, `SectionSyncControllerTest`.
- `tpi-roadmap/docs/contracts/reporte-users-contratos-y-endpoints.md` (roles).
- Relacionadas: [[acuerdos/users|Users]], [[acuerdos/courses-g01|Courses]].
