---
tags: [tpi, g10, decision, gate, motor, accounting, courses]
fecha: 2026-10-15
estado: aceptada  # G09 aprobó el acta del gate v1.4 el 2026-10-16, con el valor en inglés
reemplaza: "DEC-003 (solo el 503 por origen caído)"
---

# DEC-020: La caída de un origen del gate es un motivo (`origin_unavailable`), no un 503

## Contexto
Según [[decisiones/DEC-003-gate-pull-identidad-de-servicio-fail-closed|DEC-003]], si Accounting o Courses no respondían sin dato vigente, el gate devolvía `503` Problem Details. HU-15 CA5 pide que esa situación tenga un motivo, para que el Motor y el front la puedan mostrar en texto en lugar de un error técnico. La tarea es T-31.1 de [[sprints/sprint-3/historias/HT-31 Gate y vidas pendientes de HU-15, HU-16 y HU-48|HT-31]].

## Decisión
Si al evaluar el gate Accounting o Courses no responden y no hay caché vigente, el gate responde `200` con `eligible=false` y `reason=origin_unavailable`, con el mismo `challenge_id` y `attempt_type` de siempre. Sigue siendo **fail-closed**: nunca habilita, nunca se convierte en `no_lives`, `not_enrolled` ni `group_restricted`, y nunca usa caché vencida.

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
- **Valor en castellano (`origen_no_disponible`, como lo escribió la HU)**: G09 pidió, al aprobar el acta, que el valor siga la convención del resto del vocabulario y del enum (`GateReason.ORIGIN_UNAVAILABLE`), todo en inglés. Quedó `origin_unavailable`.

## Consecuencias
- Positivas: el Motor ya reenvía el `reason` como texto con `eligible=false` (`403 student-not-eligible` + `reason`), así que muestra el motivo sin cambiar su lógica; el front de Roadmap lo muestra en texto (HT-31 CA1, T-31.2).
- Aprobación de G09 (2026-10-16, en su issue): acepta el `200` fail-closed en lugar del `503` y el `403 student-not-eligible` con el `reason`, y pidió el valor en inglés. De su lado suman `unit_prerequisite_pending` y `origin_unavailable` a `roadmap-eligibility.yaml` y a `RoadmapIneligibilityReason`, aclaran que el `503` ya no aplica a dependencias caídas de Roadmap, y agregan `@JsonIgnoreProperties(ignoreUnknown = true)` a `RoadmapEligibilityResponse`.
- Negativas / deuda:
  - Cambia el contrato con G09: el gate deja de devolver `503` (aprobado; G09 publica su contrato cuando confirmemos el nombre).
  - `POST /nodes/{nodeId}/read` y el recorrido (`block_reason`) siguen respondiendo `503` ante la misma caída: este cambio es solo del gate.

## Referencias
- Código: `services/GateService` (atrapa el `ApiException` 503 de los clientes), `models/GateReason.ORIGIN_UNAVAILABLE`, `models/NodeBlockReason.ORIGIN_UNAVAILABLE`; rama `feature/t-31-1-gate-origen-no-disponible` de `tpi-roadmap`.
- Tests: `GateLivesAndEnrollmentTest` (Accounting caído y entrada vencida), `GateEnrollmentFallbackTest` y `GroupGateTest` (Courses caído), `gate_eligibility.feature`, `group_access.feature`.
- Front (T-31.2): `ChallengeAttemptService` muestra el `reason` del `403` del Motor; textos `attemptGate.origin_unavailable` y `roadmapLabels.blockReason.origin_unavailable`; rama `feature/t-31-2-motivo-origen-no-disponible` de `2026-PIV-TPI-FE`.
- Contrato: [[contratos/roadmap-motor-gate-v1|acta del gate]] §6 (v1.4).
- Relacionadas: [[decisiones/DEC-003-gate-pull-identidad-de-servicio-fail-closed|DEC-003]], [[decisiones/DEC-015-4xx-de-accounting-no-es-indisponibilidad|DEC-015]], [[acuerdos/motor-desafios-g09|Motor]].
