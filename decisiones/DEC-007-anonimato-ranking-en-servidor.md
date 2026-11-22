---
tags: [tpi, g10, decision, ranking, privacidad]
fecha: 2026-10-03
estado: aceptada
reemplaza: ""
---

# DEC-007: El anonimato del ranking se resuelve en el servidor

## Contexto
RF-RNK-03 definía el anonimato de todas las filas ajenas. El acuerdo de [Roadmap #427](https://github.com/2026-P4-BE/tpi-roadmap/pull/427) incorporó la elección de la vista por curso. La regla de identidad se define para cada vista en esta decisión. Los perfiles dependen de Users.

## Decisión
`GET /api/roadmap/courses/{courseId}/ranking` devuelve una **vista según el rol** y el servidor decide qué se serializa:
- `STUDENT`: Roadmap aplica la vista elegida por el profesor. Por defecto se usa **Compacta**. La fila propia conserva su identidad en ambas vistas. Sin matrícula activa, la API devuelve `403`.
  - **Compacta (`COMPACT`)**: incluye la fila propia y hasta dos puestos cercanos. En las filas de compañeros, Roadmap omite `student_id` y `profile`, y conserva un seudónimo de respaldo. El front difumina la celda de identidad con un marcador genérico.
  - **Completa (`FULL`)**: habilita toda la clasificación y devuelve el nombre y la foto de perfil de los compañeros cuando Users entrega el perfil. Si falta un perfil, devuelve un seudónimo. El legajo se reserva al staff. Los ajustes ignoran `NAME` en `full_hidden_fields`.
  - La apariencia guardada del personaje 3D puede mostrarse en ambas vistas. Los cortes P90 y P10 se informan sin identidad. El alumno no puede optar por quedar fuera de las filas visibles.
- `STAFF` (ADMIN y profesor dueño): filas identificadas con puestos de corte; un profesor ajeno recibe `403`.
- Para el profesor, cada fila suma `profile` (nombre, legajo, avatar) cuando Users respondió; si no, `pseudonym` además de `student_id`.
- `cutoffs` es `null` con menos de 10 inscriptos. `lost_lives` es `null` (no disponible), nunca `0`. Los empates comparten posición (cascada: insignias, menos vidas perdidas, ejercicios).
Las reglas se portaron a Java (`RankingRules`) con paridad contra el front.

## Alternativas descartadas
- **Anonimizar solo en el front en la vista compacta**: los datos que deben ocultarse viajarían al cliente.
- **Bloquear el ranking si Users cae**: se devuelve completo, con seudónimos.
- **Usar `student_course.lost_lives` para el desempate**: la auditoría concluyó que siempre vale 0; se lee del lote de Accounting.

## Consecuencias
- Positivas: Roadmap limita los datos de identidad antes de entregar la vista compacta al front.
- Negativas / deuda:
  - Dos formatos de respuesta (`oneOf`), más complejidad en el front.
  - Una sola cuenta faltante en Accounting apaga el desempate por vidas para todo su grupo empatado.
  - El front aún usa `COURSE_SEED_ID` y `CURRENT_STUDENT_ID` de mock en el ranking (auditoría Sprint 3).

## Referencias
- [Cambio de visibilidad #10](https://github.com/BenjaminPolzoni/tpi-g10-cerebro/pull/10), [Roadmap #514](https://github.com/2026-P4-BE/tpi-roadmap/pull/514) y [Frontend #3042](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/3042).
- Código / PR / doc: `4edd27e` (2026-10-03), `aa0f437` (BDD anonimato), `41aa7ba` (`RankingRules`), `9fb41e6` (perfil de Users, 2026-10-10), `controllers/RankingController`, `services/RankingService`, `dtos/RankingDtos`.
- `tpi-roadmap/docs/ESTRUCTURA.md` (`RankingDtos`), `docs/T-25-2-FUENTE-VIDAS-PERDIDAS.md`.
- Relacionadas: [[acuerdos/users|Users]], [[acuerdos/accounting|Accounting]].
