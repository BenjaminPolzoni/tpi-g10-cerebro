---
tags: [tpi, g10, decision, gate, motor, accounting, courses]
fecha: 2026-10-15
estado: propuesta  # pasa a aceptada cuando G09 apruebe el acta del gate v1.4
reemplaza: "DEC-003 (solo el 503 por origen caído)"
---

# DEC-020: La caída de un origen del gate es un motivo (`origen_no_disponible`), no un 503

## Contexto
Según [[decisiones/DEC-003-gate-pull-identidad-de-servicio-fail-closed|DEC-003]], si Accounting o Courses no respondían sin dato vigente, el gate devolvía `503` Problem Details. HU-15 CA5 pide que esa situación tenga un motivo, para que el Motor y el front la puedan mostrar en texto en lugar de un error técnico. La tarea es T-31.1 de [[sprints/sprint-3/historias/HT-31 Gate y vidas pendientes de HU-15, HU-16 y HU-48|HT-31]].

## Decisión
Si al evaluar el gate Accounting o Courses no responden y no hay caché vigente, el gate responde `200` con `eligible=false` y `reason=origen_no_disponible`, con el mismo `challenge_id` y `attempt_type` de siempre. Sigue siendo **fail-closed**: nunca habilita, nunca se convierte en `no_lives`, `not_enrolled` ni `group_restricted`, y nunca usa caché vencida.

Lo mismo vale para una respuesta inválida de Courses (por ejemplo, una ventana `DATE` vacía o invertida), que ya se trataba como indisponibilidad.

Se mantienen sin cambios:
- `404 inventory.account-not-found` (cuenta ausente, [[decisiones/DEC-015-4xx-de-accounting-no-es-indisponibilidad|DEC-015]]);
- `502` por un rechazo `4xx` de Accounting;
- `403 node.unit-unresolved` y `403 node.unavailable`;
- `404 node.not-found`.

Un bloqueo funcional anterior gana sobre la caída: las vidas se consultan al final, así que un `content_not_read` o un `prerequisite_pending` se informan aunque Accounting esté caído. Un nodo `RECOVERY` no consulta vidas, y la caída de Accounting no lo bloquea.

## Alternativas descartadas
- **Mantener el `503`** (DEC-003): el alumno ve un error técnico en lugar de un motivo, y no cumple HU-15 CA5.
- **Responder `no_lives` o `eligible=true`**: prohibido por el acta (no se transforma una falla en un bloqueo funcional ni se habilita con un dato faltante).
- **Nombre en inglés (`source_unavailable`)**: el resto del vocabulario está en inglés, pero la HU fija `origen_no_disponible`. Se puede renombrar antes de que G09 apruebe el acta.

## Consecuencias
- Positivas: el Motor ya reenvía el `reason` como texto con `eligible=false` (`403` + `reason`), así que muestra el motivo sin cambiar su código; el front lo puede mostrar en texto (HT-31 CA1).
- Negativas / deuda:
  - Cambia el contrato con G09: el gate deja de devolver `503`. **Bloquea el merge de T-31.1** hasta que G09 apruebe el acta v1.4.
  - `POST /nodes/{nodeId}/read` y el recorrido (`block_reason`) siguen respondiendo `503` ante la misma caída: este cambio es solo del gate.
  - El valor en castellano rompe la convención del resto del vocabulario.

## Referencias
- Código: `services/GateService` (atrapa el `ApiException` 503 de los clientes), `models/GateReason.ORIGIN_UNAVAILABLE`, `models/NodeBlockReason.ORIGIN_UNAVAILABLE`; rama `feature/t-31-1-gate-origen-no-disponible` de `tpi-roadmap`.
- Tests: `GateLivesAndEnrollmentTest` (Accounting caído y entrada vencida), `GateEnrollmentFallbackTest` y `GroupGateTest` (Courses caído), `gate_eligibility.feature`.
- Contrato: [[contratos/roadmap-motor-gate-v1|acta del gate]] §6 (v1.4).
- Relacionadas: [[decisiones/DEC-003-gate-pull-identidad-de-servicio-fail-closed|DEC-003]], [[decisiones/DEC-015-4xx-de-accounting-no-es-indisponibilidad|DEC-015]], [[acuerdos/motor-desafios-g09|Motor]].
