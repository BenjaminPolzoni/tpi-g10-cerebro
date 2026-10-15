# T-15.1 — Endpoint de Gate con vocabulario v3

## Contrato publicado

Motor consulta a Roadmap antes de crear un intento:

```http
GET /api/roadmap/courses/{courseId}/students/{studentId}/nodes/{nodeId}/eligibility
```

La operación es de solo lectura e idempotente. Roadmap no crea ni administra intentos.

Respuesta habilitada:

```json
{"data": {"eligible": true, "reason": null}, "message": null, "success": true, "timestamp": "..."}
```

Respuesta bloqueada:

```json
{"data": {"eligible": false, "reason": "prerequisite_pending"}, "message": null, "success": true, "timestamp": "..."}
```

Vocabulario v3 cerrado: `not_enrolled`, `course_archived`, `content_not_read`,
`prerequisite_pending`, `no_lives`.

Los bloqueos funcionales devuelven 200. Los errores reales conservan las convenciones existentes:
401/403 para identidad, 404 para nodo inexistente y Problem Details.

## Identidad

La llamada es servicio a servicio a través del Gateway. Roadmap confía en:

- `X-Principal-Type: service`
- `X-Service-Id`
- `X-Service-Scopes`

Roadmap no parsea el JWT. `studentId` es un dato funcional del path; no viaja en `X-User-Id`.
`on_behalf_of` no genera un header para Roadmap y `X-Delegated-User` se rechaza.

No hay todavía un `serviceId` o scope formalmente acordado para Motor. Por eso T-15.1 autoriza
identidad de tipo servicio y conserva ID/scopes como datos opacos, sin inventar nombres.

## Reutilización y orden

El controller solo adapta HTTP. `GateService` reutiliza:

1. el nodo y su curso para validar pertenencia y existencia;
2. el estado archivado del roadmap;
3. la matrícula activa de `StudentCourseRepository`;
4. `SectionReadingProgressService` para lectura obligatoria;
5. `PrerequisiteService.isSatisfied` para AND/OR;
6. `InventoryClient` como puerto desacoplado de vidas.

Un nodo marcado no disponible conserva el 403 existente. Un desafío de recuperación conserva la
regla existente: puede iniciarse sin vidas. No se escriben lecturas, desbloqueos, XP ni intentos.

## Límite con T-15.2

El contrato vigente de Accounting para el Gate es:

```http
GET /api/accounting/courses/{courseId}/accounts/{studentId}/lives-availability
```

```json
{"currentLives": 2, "reservedLives": 1}
```

T-15.1 consume el puerto `InventoryClient`. T-03.2 implementa el cliente HTTP y adapta
`currentLives`/`reservedLives`; el Gate calcula sus vidas libres. La caché vigente
puede respaldar el Gate; sin ella, una falla de Accounting es indisponibilidad explícita, nunca
`no_lives` ni habilitación por defecto. El TTL corto y configurable se define en T-03.2 sin fijar
un valor en el contrato. Ver `docs/contracts/accounting-roadmap-v1.md`.

El contrato anterior `GET /api/bank/courses/{courseId}/students/{studentId}/lives` queda
**obsoleto y reemplazado** por el acta Accounting ↔ Roadmap v1.

T-15.5 retiró del contrato activo los valores históricos `recovery_pending` y `already_passed`.
El contrato vigente y su aprobación se registran en
[`contracts/roadmap-motor-gate-v1.md`](contracts/roadmap-motor-gate-v1.md).

## Versionado

El repositorio no versiona endpoints de negocio agregando `/v3`. `/v3/api-docs` es la ruta de la
especificación OpenAPI y `info.version` toma la versión del artefacto Maven. El “v3” de T-15.1 se
materializa en el vocabulario cerrado documentado en el schema, no cambia el path acordado.
