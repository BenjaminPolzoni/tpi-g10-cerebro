---
tags: [tpi, g10, decision, ranking, errores, disponibilidad]
fecha: 2026-10-15
estado: aceptada
reemplaza: ""
---

# DEC-019: El ranking avisa el estado de sus datos, tiene caché de respaldo y la autorización falla cerrado

## Contexto
Los profes reportaron un error al ver el ranking (T-45.7, [[sprints/sprint-3/historias/HU-45 Ranking de la cohorte y avance por comisión|HU-45]]). En la variante del 2026-10-15 encontramos dos causas:

- **Token técnico:** con el secret viejo de `roadmap-service`, Users respondía `401` al pedir el token técnico. `HttpCohortOwnershipClient` lo convertía en la misma `OwnershipUnavailableException` que cuando Courses no responde. El resultado era un `503` con «Courses no responde», que apunta al servicio equivocado.
- **Curso de mock:** el front pedía el ranking de `COURSE_SEED_ID`, que no es un curso real. Ver [[sprints/sprint-3/Planes/Benja/HT-14 Front - quitar IDs de mock|HT-14]].

Además, si Accounting o Backoffice no responden, el ranking ya se degradaba en silencio (vidas perdidas o nivel nulos), sin avisarle al usuario.

## Decisión

### Errores
- **Token técnico:** si falla el token técnico de Users, se responde `503` con el código propio `courses.ownership-token-unavailable`.
- **Courses caído:** conserva `courses.ownership-unavailable`.
- **Formato:** todos los errores en `application/problem+json` (RFC 9457), con el mensaje en `messages.properties`.

### Autorización
- **Fail-closed:** la validación de dueño (Courses o token) y la de matrícula del alumno fallan cerrado. Si no se pueden hacer, `503`.
- **Sin atajos por caché:** la caché nunca saltea la autorización.

### Logs
- **Rechazos 403:** `INFO` en `not-owner` y `student.not-enrolled`, con `courseCohortId` y `userId`, sin datos personales.
- **503:** ya tienen `WARN`.

### Estado de los datos
Las respuestas del ranking (`StaffRankingView`, `StudentRankingView`) suman dos campos:

- **`data_status`:**
  - `FRESH`: armado completo.
  - `DEGRADED`: faltó Accounting o Backoffice; el ranking sale con XP al día y vidas o nivel nulos, sin cambiar el orden.
  - `STALE`: servido desde la caché.
- **`generated_at`:** instante en que se armó la vista.

### Caché de respaldo
- **Dónde:** el último ranking armado vive en memoria (Caffeine). La vista del profesor se guarda por `courseCohortId`; la del alumno, por `(courseCohortId, studentId)`.
- **Configuración:** TTL y tamaño por property con variable de entorno (por ejemplo `RANKING_FALLBACK_CACHE_TTL`, 24 h por defecto).
- **Cuándo se usa:** **solo** si armar el ranking falla **después** de pasar la autorización (por ejemplo, la base). Se devuelve con `data_status=STALE` y su `generated_at` original, y se deja un `WARN`.
- **Sin caché:** `503 ranking.unavailable`.

## Alternativas descartadas
- **Servir el ranking cacheado si no se puede validar al dueño**, recordando la última validación positiva: un profe dado de baja podría ver datos mientras dure la caché. Se prioriza la seguridad (misma línea que [[decisiones/DEC-003-gate-pull-identidad-de-servicio-fail-closed|DEC-003]]).
- **Servir el ranking cacheado completo cuando cae Accounting o Backoffice:** se prefiere el XP al día con aviso de dato faltante.
- **Caché en una tabla de la base:** sobrevive a reinicios, pero suma una entidad y una migración (RF-NFR-01). No se justifica para un respaldo.
- **Mantener un solo `503` para token y Courses:** era el estado previo y llevó a diagnosticar mal el error.

## Consecuencias
- **Positivas:**
  - El diagnóstico distingue el token técnico de Courses caído.
  - El usuario sabe cuándo los datos están incompletos o viejos.
  - Una caída de la base después de autorizar ya no deja la pantalla vacía.
- **Negativas / deuda:**
  - El `503` de dueño que vieron los profes **sigue siendo un error**. Solo lo amortigua la caché corta de validaciones positivas que ya tiene `HttpCohortOwnershipClient`.
  - La caché se pierde al reiniciar el micro y no se comparte entre instancias ([[deuda-tecnica#Back|DT-09]]).
  - El front tiene que mostrar el aviso de `DEGRADED`/`STALE` y los `503` nuevos ([[sprints/sprint-3/Planes/Benja/T-45.7 Front - estados de error del ranking|T-45.7 Front]]).

## Referencias
- **Código / PR / doc:**
  - `RankingService`, `RankingController`, `RankingDtos`.
  - `clients/courses/HttpCohortOwnershipClient`, `OwnershipUnavailableException`.
  - `clients/auth/TechnicalTokenUnavailableException`.
  - `tpi-roadmap/docs/T-45-7-ERROR-RANKING.md`.
  - Rama `fix/t-45-7-error-ranking`. **Implementación en curso; completar con el PR.**
- **Plan:** [[sprints/sprint-3/Planes/Benja/13-plan-T-45-7|13 — Plan T-45.7]] y [[sprints/sprint-3/Planes/Benja/T-45.7 Back - error del ranking|T-45.7 Back]] (§5 y §6).
- **Relacionadas:**
  - [[decisiones/DEC-003-gate-pull-identidad-de-servicio-fail-closed|DEC-003]]
  - [[decisiones/DEC-007-anonimato-ranking-en-servidor|DEC-007]]
  - [[decisiones/DEC-015-4xx-de-accounting-no-es-indisponibilidad|DEC-015]]
  - [[acuerdos/users|Users]]
  - [[acuerdos/courses-g01|Courses]]
