---
tags: [tpi, g10, sprint-3, plan, back, decision]
fecha: 2026-10-22
autor: Benja
estado: borrador - decisión de producto
repo: 2026-P4-BE/tpi-roadmap
taiga: sin asignar
orden: 4 de 4 (depende de la corrección de XP)
---

# Back — Qué pasa con el progreso cuando se recalcula una nota

> [!info] Contexto
> Auditoría del 2026-10-22. Pregunta del equipo: ¿un recálculo de nota puede **volver atrás** el progreso? Hoy no: todo es monótono. Este plan deja la política escrita y define el alcance mínimo, sin construir rollback sin que lo pidan.

## 1. Estado actual (verificado en código)

Rutas de `Backend/tpi-roadmap/src/main/java/com/utn/tpi/roadmap/` (`BE/`).

| Elemento | Comportamiento hoy | Evidencia |
|---|---|---|
| Nodo completado | Solo se inserta, nunca se borra | `ProgressService.java:153-158`; no hay `delete` en `BE/` |
| Desbloqueos | Solo se agregan | `prerequisites.recordUnlocksAfter`, `ProgressService.java:165` |
| Insignias | Se otorgan una vez, nunca se quitan (ni las dadas de baja se re-otorgan) | `BadgeEvaluator.awardEarned`, `:43-58` |
| Estado `completed` del nodo | Sale de `completed_node` o `content_reading`, sin recálculo | `NodeProgressService.java:148-161` |
| `CHALLENGE_ABORTED` / `ATTEMPT_CANCELED` | Solo loguean | `RoadmapEventListener.java:253-256`, `:376-393` |
| `CHALLENGE_ARCHIVED` | Marca `challengeUnavailable`, no toca progreso | `:263-280` |

## 2. Propuesta de política (a validar con profes y equipo)

1. **El progreso es monótono**: completado, desbloqueos e insignias no se revocan por un recálculo de nota.
2. **El XP se corrige solo hacia arriba** (ver [[Back - corrección de XP por recalificación (delta y nivel)]]).
3. **La nota en sí** (para el ranking «por notas», [[T-45.11 Back+Front - ranking por XP o por notas]]) sí se actualiza: es un dato de lectura, no de progreso.
4. Una nota que baja de «aprobada» a «reprobada» **no** descompleta el nodo; queda para revisión manual del profesor.

## 3. Pasos

1. Presentar la política a los profes (ficha en [[sprints/sprint-3/08-dudas]], nueva duda).
2. Dejar la decisión en `decisiones/` como ADR corto: «Progreso monótono; solo XP se corrige hacia arriba».
3. Documentarlo en `contratos/motor-desafios.md` para que G09 sepa que un `passed=false` posterior no revierte nada.
4. Cubrir con un test de regresión: nodo completado + evento posterior `passed=false` → `completed_node` intacto, desbloqueos intactos, insignias intactas.

## 4. Si los profes piden revocación (no se hace sin pedido)

Trabajo grande, en este orden:
1. `completed_node` con baja lógica (columna `revoked_at`), y que `NodeProgressService` la respete.
2. Recalcular desbloqueos derivados del nodo revocado (grafo y `recordUnlocksAfter` inverso) y manejar a los alumnos que ya avanzaron sobre ellos.
3. Revocar o suspender insignias (hoy el evaluador asume que son permanentes).
4. Evento nuevo `NODE_REVOKED` en `roadmap.events` y acta con Notificaciones.
5. Decidir XP: devolver el delta al ledger como movimiento negativo.

Impacto alto en datos de alumnos reales; requiere migración y aprobación explícita.
