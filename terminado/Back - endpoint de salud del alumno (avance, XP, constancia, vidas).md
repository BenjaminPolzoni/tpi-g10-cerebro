---
tags: [tpi, g10, sprint-3, plan, back, notificaciones]
fecha: 2026-10-22
autor: Benja
estado: aprobado
repo: 2026-P4-BE/tpi-roadmap
taiga: sin asignar
orden: 2 de 4
rama: feature/student-health-endpoint
worktree: ~/orca/workspaces/tpi-roadmap/feature/student-health-endpoint
---

# Back — Endpoint de «salud del alumno» (avance, XP, constancia, vidas)

> [!info] Contexto
> Auditoría del 2026-10-22. Endpoint **síncrono** para que Notificaciones (G02) consulte, y para la vista de vida del usuario. Compone lo que ya existe; no reimplementa nada. Racha: [[sprints/sprint-3/historias/HU-73 Ver mi racha de días con actividad|HU-73]] (cierra [[deuda-tecnica#DT-13]]).

## 1. Estado actual (verificado en código)

Rutas de `Backend/tpi-roadmap/src/main/java/com/utn/tpi/roadmap/`.

| Dato | ¿Existe? | Dónde |
|---|---|---|
| XP | Sí, `xp_total` | `StudentProgress` (`ProgressController`) |
| Vidas | Sí, `current_lives`, `recovery_pending` (en vivo de Accounting) | `NodeProgressService.progressOf` (`inventory.fetchLives`) |
| Nivel | Sí | `GET .../level` (`LevelController`, DTO `StudentLevel`) |
| Avance % | **No como campo**; hay `nodes[].status` | contar `completed / total` |
| Racha | **Sí**: `current_streak`, `max_streak` en `StudentProgress` vía `StreakService`, detrás de `streakProperties.enabled()` (apagado devuelve 0/0) | `NodeProgressService.java:126` |
| Endpoint único de salud | No | — |

## 2. Decisiones (aprobadas 2026-10-22)

- **D1.** Un solo endpoint de lectura, sin tabla nueva, **por curso** (roadmap principal; sin `roadmap_id`).
- **D2.** Si Accounting no responde, `lives` va `null` y el endpoint responde 200.
- **D3.** Racha apagada por flag → `streak: null` (no `0/0`). Racha prendida → `{current, max}`.
- **D4.** Seguridad: servicio con scope nuevo `roadmap.health.read` (patrón `canReadCohortProgress` en `SecurityConfig`); ADMIN y profesor dueño de la cohorte, cualquier alumno; alumno solo `me`.
- **D5.** Notificaciones consume por **polling** de este endpoint.
- **D6.** Variante por cohorte (paginada) fuera de alcance.

## 3. Contrato

```
GET /api/roadmap/courses/{courseId}/students/{studentId}/health
GET /api/roadmap/courses/{courseId}/students/me/health        (alumno)
```

Respuesta 200 (snake_case):

```json
{
  "student_id": "uuid",
  "course_id": "uuid",
  "roadmap_id": "uuid",
  "progress": { "completed_nodes": 3, "total_nodes": 10, "progress_pct": 30.0 },
  "xp": { "total": 1250, "level": 4, "current_level_xp": 150, "next_level_xp": 400,
          "xp_to_next_level": 250, "max_level": false },
  "lives": { "current": 2, "recovery_pending": false },
  "streak": { "current": 5, "max": 9 },
  "generated_at": "2026-10-22T14:03:00Z"
}
```

- `lives` y `streak` pueden ser `null` (D2, D3). `next_level_xp` y `xp_to_next_level` son `null` en nivel máximo (como `StudentLevel`).
- Errores en Problem Details: `403 course.not-owner`, `404` alumno no matriculado, `404` curso sin roadmap.

## 4. Pasos

1. `HealthDtos` (`StudentHealth`) en `dtos/`, con `@JsonProperty` explícito.
2. `StudentHealthService`: reutiliza `NodeProgressService`/`StreakService`, `LevelService`, `XpScopeService` y `inventory.fetchLives` (capturar fallo → `null`). Sin queries nuevas.
3. `HealthController` con las dos rutas; `@PreAuthorize` como `ProgressController` y `requireCohortViewer` para personas.
4. `SecurityConfig`: matcher `GET /courses/*/students/*/health` con scope `roadmap.health.read`.
5. OpenAPI en `docs/contracts/` y nota en [[contratos]].
6. Tests: 3/10 nodos → 30 %; Accounting caído → `lives = null`; racha apagada → `streak = null`; alumno pidiendo otro id → 403.

## 4b. Ejecución

Worktree `feature/student-health-endpoint` desde `origin/develop` (`f7cfa2af`), PR a `develop`. Implementación delegada a Codex vía orquestación; sin push.

## 5. Coordinación

- [ ] Pedir el alta del scope `roadmap.health.read` a plataforma (ver `P-11-5-issues.md`); sin eso el Gateway da 400.
- [ ] Avisar a Notificaciones del contrato y dejar acta (P-09, `acuerdos/notificaciones-bus.md`).
- [ ] Verificar que el flag de racha esté prendido en el entorno de la demo.
- [ ] `COURSE_LEVEL_UP` y `PERFORMANCE_ZONE_CHANGED` figuran en `AGENTS.md` pero no se emiten; decidir implementar o sacar del doc.

## 6. Fuera de alcance

Front de «salud» y reemplazar el `7` fijo de `streak.component` (lo cubre HU-73).
