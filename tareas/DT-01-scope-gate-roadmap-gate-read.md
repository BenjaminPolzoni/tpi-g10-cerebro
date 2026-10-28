# DT-01 · Scope `roadmap.gate.read` en el gate

Fecha: 2026-10-27 · Asignada: Santi · Estado: **cerrada en código; falta una llamada real (punto 2 o 3 abajo)**

## Qué pasó

La validación **ya estaba en `develop`** desde `402a4094` (Mateo, 2026-10-25, `fix(security): require roadmap.gate.read on eligibility`):

- `SecurityConfig.canReadGate`: solo una `ServiceIdentity` cuyo `X-Service-Scopes` contiene `roadmap.gate.read` (comparación exacta, lista separada por comas).
- 401 y 403 salen como `problem+json` (`ProblemJsonSecurityHandlers`, `code: FORBIDDEN`).

Esta tarea sumó solo tests en `GateControllerTest` ([tpi-roadmap#356](https://github.com/2026-P4-BE/tpi-roadmap/pull/356), rama `feature/dt-01-gate-scope-d991d3`, commit `dca67455`): scope de otro endpoint → 403 problem+json; scopes parecidos (`roadmap.gate.readonly`, `roadmap.gate`, mayúsculas, prefijo) → 403; `roadmap.gate.read` junto a otros → 200.

Aparte, `mvn verify` estaba rojo en `develop` por `ErrorCatalogTest` (faltaba `xp-history.sort-unknown` de #352). Se arregla en la misma PR #356 (commit `e7211694`).

## Evidencia del contrato (verificada el 2026-10-27, solo lectura)

| Qué | Dónde | Dice |
|---|---|---|
| El Motor pide el scope | `tpi-engine-challenge`, `GatewayRoadmapEligibilityClient` + `application.properties` | `app.roadmap.service-id=roadmap-service`, `app.roadmap.scope=roadmap.gate.read` |
| Contrato del Motor | `tpi-engine-challenge/docs/contracts/roadmap-eligibility.yaml` | «Service token with audience roadmap-service and registered scope roadmap.gate.read» |
| Identidad lo tiene dado de alta | `tpi-system-compose/registry/generated/clients.txt` | `engine-challenge-service g09 …,roadmap.gate.read,…` |
| Roadmap lo ofrece | `tpi-roadmap/tpi-integration.yml` | `offers: roadmap.gate.read` |
| El Gateway lo pasa así | `tpi-api-gateway/docs/GATEWAY-REFERENCE.md` | `X-Service-Scopes`: roles primero (`MS`), después los scopes, separados por coma sin espacio |

Falta lo único que no se puede ver leyendo código: que **un token real del Motor, a través del Gateway, llegue a Roadmap con el scope** y el gate responda 200.

## Punto 2 — Pedirle a G09 una llamada real (recomendado)

Mensaje para mandar a G09 (Motor de Desafíos):

> Hola G09. En `tpi-roadmap` `develop` el gate (`GET /api/roadmap/courses/{courseId}/students/{studentId}/nodes/{nodeId}/eligibility`) ahora **exige** el scope `roadmap.gate.read` en el token de servicio (antes aceptaba a cualquier servicio). Sin el scope responde `403` problem+json.
>
> Por el código del Motor y el registry (`clients.txt`) ustedes ya piden `roadmap.gate.read` con audience `roadmap-service`, así que debería seguir andando. ¿Pueden hacer **una llamada real** al gate desde su entorno de dev (mesh) contra Roadmap con un `courseId`, `studentId` y `nodeId` válidos y pegarnos el status y el cuerpo?
>
> - `200` con `data.eligible` → todo bien, cerramos DT-01.
> - `403` → avisennos antes de que llegue a producción y miramos qué scopes llegan en `X-Service-Scopes`.
>
> No hace falta que nos manden ningún secreto ni token. Gracias.

Qué hacer con la respuesta: si es `200`, marcar «verificado» acá y listo. Si es `403`, revisar con Identidad (G07) qué scopes tiene el cliente `engine-challenge-service` en el entorno desplegado (no solo en el registry).

## Punto 3 — Alternativa: probarlo nosotros en la malla

Requiere cosas que **no tenemos**; hay que pedirlas:

1. A Identidad (G07): una `TS_AUTHKEY` reusable con `tag:microservicio` para levantar Roadmap en la malla.
2. Un cliente de servicio con el scope: el cliente de Roadmap **no** ofrece `roadmap.gate.read` (lo ofrece, no lo pide). Para obtener un token de prueba hace falta el secreto de `engine-challenge-service` (Vault, grupo 09), o que Identidad registre un cliente de prueba con ese scope. **El secreto nunca va por chat ni al repo.**

Pasos, una vez con las credenciales:

```bash
cd .tpi/platform
# TS_AUTHKEY y APP_CLIENT_SECRET en el entorno (no en archivos versionados)
./up.sh mesh
./verify.sh mesh
```

Después, con el script de `tpi-system-compose` (`skills/integrate-micro-gateway/scripts/test-round-trip.sh`), pedir un token `client_credentials` con `audience=roadmap-service` y `scope=roadmap.gate.read`, y llamar al gate por el Gateway (`{gateway}/api/roadmap/...`, nunca por el puerto 8010). Esperado: 200 con el scope, 403 problem+json sin él.

Es más trabajo y depende de otros grupos; el punto 2 da la misma respuesta con una sola llamada.

## Resumen para el cierre

- DT-01 resuelta en código por `402a4094`; tests de borde en `dca67455`.
- Contrato verificado leyendo los repos del Motor, del registry y del Gateway.
- Pendiente solo la confirmación en vivo (punto 2 o 3).
- Vault actualizado: `deuda-tecnica.md` (DT-01 pasó a «Resuelta»), matriz T-22.1, `acuerdos/plataforma-gateway-kafka.md` y `acuerdos/motor-desafios-g09.md`.
