# DT-01 · Scope `roadmap.gate.read` en el gate

Fecha: 2026-10-27 · Asignada: Santi · Rama: `feature/dt-01-gate-scope-d991d3` (desde `origin/develop`, fea2fece)

## Estado

La validación **ya estaba en `develop`** desde `402a4094` (Mateo, 2026-10-25, `fix(security): require roadmap.gate.read on eligibility`):

- `SecurityConfig.canReadGate`: solo `ServiceIdentity` cuyo `X-Service-Scopes` contiene `roadmap.gate.read` (comparación exacta, lista separada por comas).
- 401 y 403 salen como `problem+json` vía `ProblemJsonSecurityHandlers` (`code: FORBIDDEN`).
- Test existente: `GateControllerTest.serviceWithoutGateScopeIsForbidden`.

Lo que sumó esta rama: solo tests (`GateControllerTest`): scope de otro endpoint (`roadmap.progress.read`) → 403 problem+json; scopes parecidos (`roadmap.gate.readonly`, `roadmap.gate`, mayúsculas, prefijo) → 403; `roadmap.gate.read` junto a otros scopes → 200.

## Contrato (fuentes)

- [[microservicios/02-engine-challenge-service]]: el Motor (`engine-challenge-service`) pide `roadmap.gate.read`, audiencia `roadmap-service`.
- [[arquitectura/cors-topics-rutas]], [[acuerdos/users]] (el gate exige `roadmap.gate.read`, T-22.4).
- Llamadores del gate por servicio: solo el Motor. El alumno usa otra ruta (`/courses/{c}/nodes/{n}/eligibility`, pre-chequeo HU-48), que no cambia.

## Pendiente de confirmar

- [[acuerdos/motor-desafios-g09]] dice que el `serviceId` y el scope nominales del Motor siguen sin confirmar; la ficha del Motor y `tpi-integration.yml` ya muestran `roadmap.gate.read`. Si el registry real no lo da al token del Motor, el gate devuelve 403 en producción.
- `deuda-tecnica.md` sigue listando DT-01 como abierta y [[arquitectura/T-22-1-matriz-permisos]] dice «hoy no valida el scope»: están desactualizados respecto de `develop`.
- No se probó contra un Gateway real.
