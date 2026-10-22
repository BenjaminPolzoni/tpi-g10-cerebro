---
tags: [tpi, g10, sprint-3, plan, back, notificaciones]
fecha: 2026-10-22
autor: Benja
estado: borrador
repo: 2026-P4-BE/tpi-roadmap
taiga: sin asignar
orden: 2 de 4 (la racha depende de HU-73)
---

# Back — Endpoint de «salud del alumno» (avance, XP, constancia, vidas)

> [!info] Contexto
> Auditoría del 2026-10-22. Se pidió un endpoint de progreso del alumno que sirva para notificaciones y para la salud del alumno. La racha ya tiene HU: [[sprints/sprint-3/historias/HU-73 Ver mi racha de días con actividad|HU-73]] (cierra [[deuda-tecnica#DT-13]]). Este plan **compone** lo que ya existe y consume la racha de HU-73; no la reimplementa.

## 1. Estado actual (verificado en código)

Rutas de `Backend/tpi-roadmap/src/main/java/com/utn/tpi/roadmap/` (`BE/`).

| Dato | ¿Existe? | Dónde |
|---|---|---|
| XP | Sí, `xp_total` | `GET /courses/{id}/students/{sid}/progress` (`ProgressController`, DTO `StudentProgress`) |
| Vidas | Sí, `current_lives` (en vivo de Accounting) | mismo endpoint, `NodeProgressService.java:110` |
| Nivel | Sí | `GET .../level` (`LevelController`) |
| Avance % | **No como campo**; hay `nodes[].status` | se cuenta `completed / total` |
| Constancia | **Solo se persiste** `daily_activity` (V29); sin cálculo ni endpoint | `ActivityDayService.java:18` («el cálculo vive en T-73.2») |
| Endpoint único de salud | No | — |
| Notificaciones | No hay código; Roadmap ya publica `NODE_COMPLETED`, `NODE_UNLOCKED`, `BADGE_AWARDED` en `roadmap.events` | acta pendiente: `acuerdos/notificaciones-bus.md` |

## 2. Decisiones

- **D1.** Un solo endpoint de lectura, sin tabla nueva: `GET /courses/{courseId}/students/{studentId}/health`, más `.../me`.
- **D2.** Devuelve `completed_nodes`, `total_nodes`, `progress_pct`, `xp_total`, `level`, `current_lives`, `streak_days`, `max_streak`.
- **D3.** `streak_days` y `max_streak` salen de lo que entregue HU-73 (T-73.2). Hasta que esté, el campo va `null` y el resto funciona. No duplicar la query de racha.
- **D4.** Si Accounting no responde, `current_lives` va `null` y el endpoint no falla (misma tolerancia que `progress`).
- **D5.** Alumno: solo `me`. Servicio y profesor del curso: cualquier alumno. Mismo esquema de permisos que `ProgressController`.
- **D6.** Variante por cohorte (paginada) **fuera de alcance**; se agrega cuando Notificaciones la pida.

## 3. Pasos

1. `HealthDtos` (`StudentHealth`) en `BE/dtos/`.
2. `StudentHealthService`: reutiliza `NodeProgressService` (conteo de completados), `LevelService`, `XpScopeService` y el cliente de vidas. Sin queries nuevas salvo la racha (HU-73).
3. `HealthController` con las dos rutas y la validación de acceso copiada de `ProgressController`.
4. OpenAPI/contrato en `tpi-roadmap/docs/contracts/` y nota en [[contratos]].
5. Test: servicio con alumno de 3/10 nodos, XP y vidas → 30 %; caso con Accounting caído → `current_lives = null`.

## 4. Coordinación

- [ ] Confirmar con Notificaciones si quieren **polling** de este endpoint o **eventos** (hoy el bus ya cubre nodos/insignias; les faltaría vidas y racha). Ver `acuerdos/notificaciones-bus.md`.
- [ ] Verificar el estado de T-73.2 con Lautaro/Franco antes de empezar el paso 2.
- [ ] `COURSE_LEVEL_UP` y `PERFORMANCE_ZONE_CHANGED` figuran en `AGENTS.md` pero no se emiten en `BE/`; decidir si se implementan o se sacan del doc.

## 5. Fuera de alcance

Front de «salud» (pantalla del profesor) y reemplazar el `7` fijo de `streak.component`; este último lo cubre HU-73.
