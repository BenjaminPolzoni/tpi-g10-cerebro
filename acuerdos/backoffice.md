---
tags: [tpi, g10, acuerdo, backoffice, tema-12, par, kafka]
fecha: 2026-09-24
grupos: [G10, Gxx]  # Backoffice = Tema 12; número de grupo no aparece en los docs (verificar)
estado: vigente  # REST + evento recibidos; faltan confirmaciones del payload v8
contrato: "tpi-roadmap/docs/contracts/backoffice-par.md"
---

# Acuerdo con Backoffice (Tema 12, Gxx verificar): parámetros PAR y eventos

> [!info] Fuentes
> - `tpi-roadmap/docs/contracts/backoffice-par.md` ([GitHub](https://github.com/2026-P4-BE/tpi-roadmap/blob/develop/docs/contracts/backoffice-par.md)): estado vigente del lado de Roadmap.
> - `tpi-roadmap/docs/contracts/CONTRATO_T10_BACKOFFICE.md` ([GitHub](https://github.com/2026-P4-BE/tpi-roadmap/blob/develop/docs/contracts/CONTRATO_T10_BACKOFFICE.md)): contrato original que **envió Backoffice** (2026-09-26). Parte quedó desactualizada (ver tabla de diferencias).
> - Contrato de eventos propios hacia Backoffice: `tpi-roadmap/docs/contracts/roadmap-events-v1.md` ([GitHub](https://github.com/2026-P4-BE/tpi-roadmap/blob/develop/docs/contracts/roadmap-events-v1.md)).
> - Repo de la contraparte: `2026-P4-BE/tpi-backoffice` (PR/issue #208 de `tpi-roadmap`).

## Qué se acordó
- **Los valores PAR los posee Backoffice; nunca constantes de código.** Solo rigen **hacia adelante** (no retroactivos, RF-CFG-06).
- Roadmap trae los parámetros **por REST al arrancar** (cold start: lista completa) y los cachea; el evento `GLOBAL_CONFIGURATION_CHANGED` invalida la caché.
- Parámetros que consumimos:
  | PAR | Concepto | Uso en Roadmap |
  |---|---|---|
  | `PAR-01` | XP base por dificultad `{easy:100, medium:250, hard:500}` | Cliente y properties adoptan las claves del contrato `easy/medium/hard` (el código usaba `basic/medium/advanced`) |
  | `PAR-09` | Curva de niveles (hasta **200 niveles** desde `#177`/`6399cf7`, 2026-10-11) | Nivel del alumno a partir del `total_xp` (`LevelService`). Ver [[decisiones/DEC-012-curva-de-niveles-desde-par-09\|DEC-012]] |
  | `PAR-12` | Vidas iniciales y techo `{initialLives, maxLives}` | `ParCatalogClient.lives()`; Accounting aplica el techo |
  | `PAR-08` | XP por defecto de desbloqueo (500) | **Fuera de alcance por decisión**: el desbloqueo es por prerrequisitos. Ver [[decisiones/DEC-011-quitar-umbral-xp-seccion-v8\|DEC-011]] |
  | `PAR-13` | Reintentos | **No está en el contrato**; sin dueño ni lector: se define su fuente antes de usarlo |
- Roadmap **publica** `NODE_COMPLETED`, `NODE_UNLOCKED`, `BADGE_AWARDED` en `roadmap.events` para el panel docente de Backoffice (issue `tpi-roadmap#134`) y expone una lectura paginada de arranque en frío.

## Quién lo acordó
- G10: equipo Roadmap.
- Otro grupo: equipo Backoffice (Tema 12), Gxx (verificar). Para `roadmap-events-v1.md` la fila de Backoffice en la tabla de firmas está **pendiente**; Roadmap firmó el 2026-10-11 ("schema y endpoint implementados").

## Contrato técnico

### REST (Roadmap → Backoffice)
| Método y ruta | Uso |
|---|---|
| `GET /api/backoffice/parameters` | Cold start: lista completa vigente |
| `GET /api/backoffice/parameters/{key}` | Consulta puntual (p. ej. `PAR-09`) |

Respuesta: `{ "key": "PAR-01", "value": {...}, "version": 1 }` (`ParameterResponseDto<T>`, `ignoreUnknown`).

- **Auth:** Bearer técnico de Roadmap, audience `backoffice-service`, scope `backoffice.parameters.read` (Backoffice exige la authority sin `SCOPE_`). El Gateway descarta los `X-User-*` de un micro.
- **Caché:** Caffeine, TTL 5 min, máx 50 entradas (`BACKOFFICE_PAR_CACHE_TTL`, `BACKOFFICE_PAR_CACHE_MAX_SIZE`). Cliente: `HttpParCatalogClient` (`ParCatalogClient`).

> [!warning] Diferencias con el contrato original de Backoffice
> | Tema | `CONTRATO_T10_BACKOFFICE.md` (reemplazado en estos puntos) | Vigente en Roadmap |
> |---|---|---|
> | Ruta | `/api/administration/parameters` | `/api/backoffice/parameters` (la que enruta el Gateway; `/api/administration/**` no) |
> | Auth | headers `X-User-Roles: MS` + `X-User-Id` | token de servicio con scope, headers de usuario descartados |
> | Payload del evento | `eventType`, `paramKey` en camelCase | snake_case v8: `param_key` |
> | Curva PAR-09 | 10 niveles | hasta 200 niveles |
> | PAR-08 | consumible | fuera de alcance |

### Kafka (Backoffice → Roadmap)
- Topic `administration.events` (DLT `administration.events.DLT`), key = `param_key`, `event_type = GLOBAL_CONFIGURATION_CHANGED`, `producer` esperado `tema-12-backoffice-service` (**a confirmar**).
- Sobre y payload en **snake_case v8**, sin alias. `ParRefreshListener` lee solo `param_key` (obligatorio) y `version` (para el log). Un `paramKey` camelCase se ignora y se confirma; un sobre camelCase va a la DLT y no invalida la caché (queda el TTL de 5 min). Backoffice publica `payload.param_key` desde su **2.0.0** (`#208`, 2026-10-14).
- Resto del payload según el contrato recibido, con nombres v8 **a confirmar por Backoffice**: `value`, `previous_version`, `description`, `updated_at`, `updated_by` (el DTO de Backoffice usa `previous_version` y `actor_id`, ver `T-191-KAFKA-V8-CUTOVER.md`).

### Kafka (Roadmap → Backoffice): `roadmap.events` v1
- Topic `roadmap.events` (DLT `roadmap.events.DLT`), producer `tema-10-roadmap-service`, key = `studentId`, at-least-once, idempotencia por `eventId`, publicado por outbox cada ~3 s.
- `NODE_COMPLETED {courseId, studentId, nodeId, challengeId, sectionId}`, `NODE_UNLOCKED {courseId, studentId, nodeId}`, `BADGE_AWARDED {courseId, studentId, badgeId}`. `courseId` = `courseCohortId`. El XP **no viaja**.
- Declarados y aún **sin emisión**: `COURSE_LEVEL_UP`, `PERFORMANCE_ZONE_CHANGED`.
- Lectura de arranque en frío: `GET /api/roadmap/courses/{courseId}/progress?page=0&size=50` (máx 200). Autoriza servicio con scope **`roadmap.progress.read`** (audience `roadmap-service`; ofrecido en el registry, `tpi-system-compose` PR #193) o usuario ADMIN/PROFESSOR. Solo matrículas activas, orden estable por `student_id`.

## Impacto en nuestro código
- `clients/backoffice/*`: `HttpParCatalogClient`, `ParCatalogClient`, `ParCatalogConfig`, `ParCatalogProperties`, `ParLevelCurve`, `ParLevel`, `ParBaseXp`, `ParLives`, `ParUnavailableException`.
- `events/ParRefreshListener` (invalidación por evento).
- `services/LevelService`, `controllers/LevelController` (`/students/{id|me}/level`).
- `events/outbox/*` (`OutboxService`, `OutboxPoller`), `BadgeEventService`, `controllers/ProgressController` (lectura `roadmap.progress.read`), `common/security/SecurityConfig`.

## Pendiente / próximos pasos
- [ ] Backoffice confirma `producer = tema-12-backoffice-service` y los nombres v8 del resto del payload.
- [ ] Definir la fuente de **PAR-13** (reintentos permitidos); relacionado con el campo `reintentos_permitidos` pendiente de HU-01/41.
- [ ] Backoffice firma `roadmap-events-v1.md` y confirma que consume v8 (**pendiente de confirmar** también para Gamificación, Accounting y Notificaciones antes del corte, según `T-191`).
- [ ] Emitir `COURSE_LEVEL_UP` y `PERFORMANCE_ZONE_CHANGED` (hoy solo declarados; las zonas existen con >= 10 inscriptos).
- [ ] Limpiar el contrato original `CONTRATO_T10_BACKOFFICE.md` o marcarlo como histórico.

> [!warning] Riesgos
> - Backoffice sin publicar de verdad `GLOBAL_CONFIGURATION_CHANGED`: la caché solo se refresca por TTL (5 min).
> - Con Backoffice caído en el cold start, el cliente lanza `ParUnavailableException` (verificar qué casos de uso la propagan, p. ej. el nivel del alumno).

> [!question] Verificar
> El contrato original exigía que Roadmap mandara headers `X-User-Roles: MS`; confirmar que Backoffice ya no depende de ello (`backoffice-par.md` dice "Confirmado por plataforma, revisión de la #77").

## Historial
- 2026-09-24: cliente REST con caché e invalidación por evento.
- 2026-09-26: contrato recibido de Backoffice (`CONTRATO_T10_BACKOFFICE.md`).
- 2026-10-11: PAR-09 admite hasta 200 niveles (`#177`); `roadmap.events` v1 y progreso agregado (`#134`).
- 2026-10-12: wire v8 snake_case (PR #191).
- 2026-10-14: Backoffice publica `param_key` (`#208`, PR #209); nota creada desde `origin/develop` (`57ff06a`).
