---
tags: [tpi, g10, decision, ranking, privacidad]
fecha: 2026-10-03
estado: aceptada
reemplaza: ""
---

# DEC-007: El anonimato del ranking se resuelve en el servidor

## Contexto
RF-RNK-03: un alumno solo puede ver su propia identidad en el ranking; el profesor ve a todos. Las reglas de orden vivían en el front (`ranking.rules.ts`). Mostrar el nombre de otros alumnos al profesor requiere Users, que puede fallar.

## Decisión
`GET /api/roadmap/courses/{courseId}/ranking` devuelve una **vista según el rol** y el servidor decide qué se serializa:
- `STUDENT`: solo su fila lleva `student_id`; `top3`, `bottom3`, `cutoffs` y `list` llevan **solo `pseudonym`**, nunca el id de otro alumno. Sin matrícula activa: `403`.
- `STAFF` (ADMIN y profesor dueño): filas identificadas con puestos de corte; un profesor ajeno recibe `403`.
- Para el profesor, cada fila suma `profile` (nombre, legajo, avatar) cuando Users respondió; si no, `pseudonym` además de `student_id`.
- `cutoffs` es `null` con menos de 10 inscriptos. `lost_lives` es `null` (no disponible), nunca `0`. Los empates comparten posición (cascada: insignias, menos vidas perdidas, ejercicios).
Las reglas se portaron a Java (`RankingRules`) con paridad contra el front.

## Alternativas descartadas
- **Anonimizar en el front**: el id de otros alumnos viajaría al cliente (el commit exige que nunca ocurra).
- **Bloquear el ranking si Users cae**: se devuelve completo, con seudónimos.
- **Usar `student_course.lost_lives` para el desempate**: la auditoría concluyó que siempre vale 0; se lee del lote de Accounting.

## Consecuencias
- Positivas: privacidad garantizada en el borde; el front no puede filtrar por error.
- Negativas / deuda:
  - Dos formatos de respuesta (`oneOf`), más complejidad en el front.
  - Una sola cuenta faltante en Accounting apaga el desempate por vidas para todo su grupo empatado.
  - El front aún usa `COURSE_SEED_ID` y `CURRENT_STUDENT_ID` de mock en el ranking (auditoría Sprint 3).

## Referencias
- Código / PR / doc: `4edd27e` (2026-10-03), `aa0f437` (BDD anonimato), `41aa7ba` (`RankingRules`), `9fb41e6` (perfil de Users, 2026-10-10), `controllers/RankingController`, `services/RankingService`, `dtos/RankingDtos`.
- `tpi-roadmap/docs/ESTRUCTURA.md` (`RankingDtos`), `docs/T-25-2-FUENTE-VIDAS-PERDIDAS.md`.
- Relacionadas: [[acuerdos/users|Users]], [[acuerdos/accounting|Accounting]].
