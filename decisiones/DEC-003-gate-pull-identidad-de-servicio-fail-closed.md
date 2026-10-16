---
tags: [tpi, g10, decision, gate, motor, seguridad]
fecha: 2026-09-26
estado: aceptada
reemplaza: ""
---

# DEC-003: Gate por pull con identidad de servicio, de solo lectura y fail-closed

> [!warning] Parte en revisión
> El `503` por Accounting o Courses caídos queda reemplazado por el bloqueo `origen_no_disponible`
> en [[decisiones/DEC-020-gate-origen-no-disponible-en-vez-de-503|DEC-020]] (propuesta, T-31.1),
> cuando G09 apruebe el acta del gate v1.4. El resto de esta decisión sigue vigente.

## Contexto
Motor necesita saber si un alumno puede iniciar un nodo antes de crear el intento. G09 había implementado un contrato distinto (POST con autorización firmada) y pidió definir el gate porque, con la ruta vacía, toda apertura respondía 503. Roadmap además debe depender de Accounting (vidas) y Courses (comisiones), que pueden caer.

## Decisión
El gate es `GET /api/roadmap/courses/{courseId}/students/{studentId}/nodes/{nodeId}/eligibility`: **solo lectura e idempotente**, llamado servicio a servicio por Gateway con **identidad de servicio** (no se parsea el JWT; `studentId` va en el path). Responde con el primer bloqueo de un **vocabulario cerrado** y orden fijo (`course_archived`, `not_enrolled`, `group_restricted`|`date_restricted`, `content_not_read`, `prerequisite_pending`, `no_lives`). Los bloqueos funcionales son `200`. Si Accounting o Courses no responden sin dato vigente, el gate **falla cerrado**: `503` Problem Details, nunca `no_lives` ni `eligible=true`, y jamás caché vencida. Los cambios de contrato son **aditivos** y versionados (v1.1 `group_restricted`, v1.2 `challenge_id` y `attempt_type`, v1.3 `date_restricted`).

## Alternativas descartadas
- **POST con autorización firmada y `autorizacion_id`** (propuesta de G09, `respuesta-motor-a-roadmap-v2.md` §4): se mantuvo el GET `{eligible, reason}`; G09 lo consume como `403` + `reason` con `eligible=false`.
- **Tratar la caída como `no_lives` o habilitar por defecto**: prohibido por el acta (no se transforma una falla en un bloqueo funcional).
- **Razones `recovery_pending` y `already_passed`**: retiradas; completar un nodo no bloquea, el ciclo de intentos es del Motor.
- **Versionar la ruta (`/v1`, `/v3`)**: no; la versión vive en el acta y en OpenAPI.

## Consecuencias
- Positivas: contrato estable, trazable, sin efectos laterales; el mismo `GateEvaluator` alimenta `block_reason` del recorrido.
- Negativas / deuda:
  - Motor aún define solo `403`/`503`; el `404 inventory.account-not-found` y el `403 node.unit-unresolved` no están coordinados.
  - `serviceId` y scope nominales de Motor siguen sin confirmar: hoy cualquier servicio puede llamar el gate.
  - El alumno no puede pre-chequear con su JWT (HU-48 pendiente) y se retiró `/start`.
  - Con el flag de comisiones activo cada evaluación hace llamadas a Courses sin caché.

## Referencias
- Código / PR / doc: `controllers/GateController`, `services/GateService`, `services/GateEvaluator`, `models/GateReason`, `common/security/SecurityConfig`; `96fcff5` (2026-10-02), `548411d` (HU-48, 2026-10-11), `8b5578f` (DATE, 2026-10-12).
- [[contratos/roadmap-motor-gate-v1|Acta del gate]], [[tareas/T-15-1-GATE-V3|T-15.1]] y [[contratos/respuesta-motor-a-roadmap-v2|respuesta de G09 v2]] (antes en `tpi-roadmap/docs/`, movidas al cerebro en `e292333`).
- Relacionadas: [[acuerdos/motor-desafios-g09|Motor]], [[acuerdos/inventario|Inventario]], [[decisiones/DEC-015-4xx-de-accounting-no-es-indisponibilidad|DEC-015]], [[decisiones/DEC-020-gate-origen-no-disponible-en-vez-de-503|DEC-020]].
