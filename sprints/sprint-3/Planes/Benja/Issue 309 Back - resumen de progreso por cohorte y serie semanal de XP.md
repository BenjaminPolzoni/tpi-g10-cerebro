---
tags: [tpi, g10, sprint-3, plan, resolver-issue, back, dashboards, backoffice, xp, progreso, concluido]
fecha: 2026-10-23
autor: Benja
estado: concluido
repo: 2026-P4-BE/tpi-roadmap
issue: https://github.com/2026-P4-BE/tpi-roadmap/issues/309
taiga: sin tarea en Taiga
---

# Issue #309 — Resumen de progreso por cohorte y serie semanal de XP

> [!success] Plan concluido (PR 1) — 23/10
> - **PR:** [#325](https://github.com/2026-P4-BE/tpi-roadmap/pull/325) hacia `develop`, con 3 commits en `feature/309-resumen-cohorte-xp-timeline` (`741295a5`, `d81db9db`, `513ec18c`). Suite completa: 2942 tests, 0 fallas.
> - Los records son `XpStats` y `StreakStats`, para no pisar los schemas `Xp` y `Streak` de `HealthDtos` en el OpenAPI.
> - **Implementado:** B1–B6, aplicando las recomendaciones D1–D6. Lo hizo codex por Orca y Claude lo revisó. `enabled`, `blocked` y `blocked_reasons` van en `null` (PR 2 pendiente de D1).
> - **Agregado fuera del plan:** el bean `Clock` en `common/config/ClockConfig.java`, para que el reloj se pueda inyectar en los servicios del dashboard.
> - **Verificado:** `CohortSummaryServiceTest` (11), `XpTimelineServiceTest` (5), `CohortDashboardControllerTest` (7), `StreakServiceTest` (14) y `SnakeCaseContractTest` (3) en verde. `mvn verify` (Checkstyle, PMD y CPD) en verde.
> - **Issue #309:** respondida con la sección 6 y cerrada (23/10). Falta asignar revisor y mergear #325.
> - **Actualización (2026-10-23):** #325 mergeado en `develop` (`642bd935`). SantiFenoglio primero pidió cambios y después aprobó. Revisión posterior al merge:
>   - **Comisión:** con `group_id` se filtran los alumnos, pero el % y `by_node` se siguen calculando sobre **todos** los nodos de los roadmaps COURSE. No usa las secciones que ve la comisión, como sí hace `GroupProgressService.sectionsOf`. Con unidades restringidas por comisión, el % sale más bajo de lo real.
>   - **Activos:** solo cuentan los movimientos con `countedInCourse = true`, así que un alumno que solo se mueve en un roadmap en modo ROADMAP no figura como activo.
>   - **Fix de los dos puntos anteriores:** PR [#326](https://github.com/2026-P4-BE/tpi-roadmap/pull/326) (`fix/309-dashboard-comision-activos`), con revisión pedida a SantiFenoglio.
>   - Los tests del controller llaman al método directo, así que no prueban `@PreAuthorize`, el binding de `from`/`to` ni `SecurityConfig`. Verifiqué aparte que `from=2026-08-01` se parsea bien.

> [!info] Contexto
> **Backoffice** abrió el issue #309 el 22/10. Lo creó Paz; el seguimiento lo lleva **Joaquín**. Es parte del plan de dashboards de Backoffice (referencia interna **R1**; el plan y los borradores están en [tpi-backoffice#244](https://github.com/2026-P4-BE/tpi-backoffice/pull/244), en `docs/Contracts/dashboards/`).
>
> **Lo que pasa hoy:** el único dato de cohorte es `GET /courses/{id}/progress`, que trae páginas de 50 alumnos con todos sus nodos. El dashboard tendría que bajarlas todas y sumar en el navegador.
>
> **Lo que piden:** dos endpoints nuevos, **solo con agregados** (sin identidades). Los usan el profesor dueño de la cohorte, ADMIN y GESTOR.
>
> La issue **no se cierra** hasta que los endpoints estén mergeados en `develop`.

Es **solo Back**. Lo hacemos en dos PR:

- **PR 1:** el resumen con los datos baratos, más la serie semanal.
- **PR 2:** los datos que salen del Gate (bloqueados y motivos). Este PR depende de D1.

## Worktree

| Repo | Ruta | Rama | Base |
|---|---|---|---|
| Back | `~/dev/TPI_2026/Backend/tpi-roadmap-dashboards-cohorte` | `feature/309-resumen-cohorte-xp-timeline` | `origin/develop` `9f2660a5` (#319). Sin upstream: el primer push lleva `-u origin feature/309-...` |

## 1. Contrato pedido

`GET {private}/courses/{courseId}/progress/summary?group_id=` (`group_id` es opcional):

```json
{
  "course_id": "uuid", "roadmap_id": "uuid", "generated_at": "2026-10-21T20:00:00Z",
  "status": "AVAILABLE",
  "total_enrolled": 40, "active_last_7_days": 28,
  "xp": { "total": 18400, "average": 460, "median": 430, "p10": 90, "p90": 880 },
  "nodes": { "completed_pct_average": 54.2, "by_status": { "completed": 520, "enabled": 180, "blocked": 300 } },
  "streak": { "average_current": 2.1, "max": 14 },
  "students_without_lives": 3,
  "blocked_reasons": { "no_lives": 3, "content_not_read": 10, "prerequisite_pending": 22 },
  "by_node": [{ "node_id": "uuid", "completed": 31, "blocked": 4 }]
}
```

`GET {private}/courses/{courseId}/xp-timeline?granularity=week&from=2026-08-01&to=2026-10-21`
→ `{ "points": [{ "period": "2026-W41", "xp_total": 2100, "active_students": 26 }] }`

**Criterios de aceptación:**
- no devuelve nodos por alumno ni identidades;
- `by_node` permite ver el cuello de botella;
- la regla de `active_last_7_days` queda documentada;
- una cohorte sin movimientos da `status: NO_DATA` y valores `null`;
- un PROFESSOR que no es dueño recibe 403.

**Reglas comunes del plan de Backoffice:**
- un dato que no se puede calcular va `null`, nunca `0`;
- con menos alumnos que el mínimo (PAR-18), los valores van `null` con `status: INSUFFICIENT_SAMPLE`;
- campos en `snake_case`, con `generated_at`;
- una sola consulta liviana por endpoint;
- acotado a `X-Organization-Id`;
- los nombres de campo son una propuesta y se pueden negociar.

## 2. Estado actual (verificado en `origin/develop` `9f2660a5` el 23/10)

| Dato pedido | De dónde sale | Hallazgo |
|---|---|---|
| `total_enrolled` | `student_course` (`active = true`) | `StudentCourseRepository.findByCourseCohortIdAndActiveTrueOrderByStudentIdAsc`. Es la misma base que usan el ranking y `GroupProgressService`. |
| `xp.*` (alcance de curso) | `student_course.total_xp` | El alcance de curso es `total_xp`, según `XpScopeService.xpOf` y `XpScope.isCourse()`. **Los percentiles se calculan en Java**: los tests corren en **H2** (`src/test/resources/application.properties:44`, `MODE=PostgreSQL`), y `percentile_cont` y `date_trunc` no son portables. Con cohortes de decenas o cientos de alumnos, ordenar la lista en memoria no cuesta nada. |
| ¿La XP baja? (pregunta 2) | `xp_movement` | **Hoy no baja.** El ledger es de solo inserción (`@SQLRestriction("deleted_at IS NULL")`). `ATTEMPT_CORRECTED` agrega un movimiento nuevo con su XP (`RoadmapEventListener.java:365-396`). `ATTEMPT_CANCELED` solo valida y deja un log (`:399-415`). Si en el futuro se corrige por delta (ver [[Back - corrección de XP por recalificación (delta y nivel)\|plan de corrección por delta]]), la serie va a mostrar la semana de la corrección con un `xp_total` menor, incluso negativo. No se reescriben las semanas pasadas. |
| `active_last_7_days` (pregunta 1) | `daily_activity` (V29) + `xp_movement.recorded_at` | `daily_activity` registra un día solo cuando el alumno **aprueba un nodo** (`ProgressService.java:~156-163`) o **lee un contenido obligatorio** (`:~295-298`). Un intento desaprobado deja `xp_movement`, pero **no** marca actividad. El issue define activo como "movimiento de XP **o** lectura", así que la regla es la **unión**: tener una fila en `daily_activity` en los últimos 7 días, o un `xp_movement` con `recorded_at` en ese rango. Las lecturas no obligatorias no cuentan. |
| `streak.*` | `daily_activity` + `student_course.max_streak` | La racha actual se calcula en `StreakService.view` (`:74`): la cadena que termina hoy o, si hoy todavía no hay actividad, la que termina ayer, en la zona `StudentZone.ID`. Hacerlo por alumno es N consultas. **Mejor:** una sola consulta con los días de la cohorte y reusar `runEnding` (hoy es privado: abrirlo a nivel de paquete o agregar `currentOf(Set<LocalDate>, LocalDate)`). La racha máxima sale de `max_streak`. |
| Nodos completados | `completed_node` **y** `content_reading` | **Ojo:** para un nodo `CONTENT`, "completado" significa **leído** (`content_reading`), no `completed_node` (`NodeProgressService.isCompleted`, `:~210`). Hay que unir las dos tablas. Los nodos que cuentan son los `available` de los roadmaps del alcance; `NodeRepository.countAvailableBySection` (`:95`) es el precedente. Los nodos START y END no se completan (`type.isBoundary()`) y se excluyen. |
| `students_without_lives` | `student_course.recovery_pending` | Es la proyección local de "no tiene vidas libres" que mantiene `AccountingEventsListener` con `LIFE_CREDITED` y `LIFE_DEBITED` (V24). Es informativa, pero alcanza para un número agregado. **No usar `student_course.lives`**: solo se escribe al crear la matrícula (`CourseCohortSyncService.java:108`) y está desactualizada. |
| `by_status.enabled/blocked`, `blocked_reasons`, `by_node.blocked` | **Gate**, que calcula en el momento | El estado "habilitado" o "bloqueado" **no está guardado**. `NodeProgressService.viewOf` y `blockReasonOf` (`:~190-235`) evalúan el Gate por alumno y nodo, y la `GateEvaluator.Context` pide las vidas a Inventory/Accounting **una vez por alumno**. Para la cohorte serían N llamadas remotas y N×nodos evaluaciones. Va al PR 2 (ver D1). |
| Comisión (`group_id`) | `GroupUnitsService.contextOf(courseCohortId).groupsByStudent()` | Ya resuelve qué alumnos son de la comisión (lo usa `GroupProgressService.progressOf`). Si `group_id` no es de la cohorte, da 404 `group.not-found`. Consulta a Courses: si Courses falla, 503 (mismo comportamiento que T-45.2). |
| Roles y dueño | `RankingController.rankingOf` (`:140`) | Es el patrón con GESTOR: `Roles.isPlatformStaff` (ADMIN o GESTOR) pasa; PROFESSOR pasa solo si `CohortOwnershipClient.isOwner`, si no, 403 `course.not-owner`; STUDENT no tiene acceso. `GroupProgressController` **no** incluye GESTOR: no copiar ese. |
| Seguridad por ruta | `SecurityConfig.java:62-72` | `/courses/*/progress` tiene un matcher propio (service token o persona). `/courses/*/progress/summary` **no** lo matchea: cae en `privatePath/**`, que exige una persona (`principal instanceof UUID`). Eso está bien si Backoffice llama con el token del usuario a través del Gateway. **Confirmarlo** (D5). |
| Organización | No existe en `develop` | `X-Organization-Id` y `CourseOrganizationGuard` viven en la rama **sin mergear** `feature/tema-01-identity-permissions-adoption`. No bloquea: cuando entre, se agrega el guard en los endpoints nuevos (ver D4). |
| Varios roadmaps (HU-57) | `XpScopeService.cohortXpOf(XpScope.ofCourse(id))` | Para el alcance de curso devuelve los roadmaps COURSE de la cohorte. Los nodos de `by_node` y el % salen **de esos roadmaps**, igual que en el ranking. El `roadmap_id` de la respuesta es el principal (`RoadmapResolver.ofCourse`). Los roadmaps en modo ROADMAP quedan fuera del resumen de curso. |
| Índices | `xp_movement` | Solo existe `idx_xp_movement_roadmap_student` (V44). La serie y la regla de activos filtran por `course_cohort_id` + `recorded_at`. Ver B4. |

## 3. Plan Back — PR 1 (rama `feature/309-resumen-cohorte-xp-timeline`)

Seguir el estilo de `RankingController`/`RankingService` y `GroupProgressController`/`GroupProgressService`:
- Javadoc en español en cada miembro;
- `@Operation` y `@ApiResponses` completos;
- DTOs como `record` en `dtos/`, con `@JsonProperty`/naming snake_case como los DTOs vecinos (mirar `GroupProgressDtos` y `RankingDtos`);
- Checkstyle y PMD en verde.

### B1. Controller `CohortDashboardController` (nuevo, en `controllers/`)
- `@RequestMapping("${app.api.private-path}")`, `@Tag(name = "Dashboard de cohorte")`.
- `GET /courses/{courseId}/progress/summary` con `@RequestParam(name = "group_id", required = false) UUID groupId`.
- `GET /courses/{courseId}/xp-timeline` con:
  - `granularity` (default `week`; **solo** se acepta `week`, otro valor da 400 `timeline.granularity-unsupported`);
  - `from` y `to` (`LocalDate`, ISO);
  - defaults: `to` = hoy en `StudentZone.ID`, `from` = `to - 12 semanas`;
  - `from > to` o un rango de más de 53 semanas da 400 `timeline.range-invalid`.
- `@PreAuthorize("hasAnyRole(ADMIN, GESTOR, COURSE_PROFESSOR)")`, y en el cuerpo la misma lógica que `RankingController.rankingOf`: si es staff de plataforma pasa; si es PROFESSOR, chequear `isOwner` y, si no es dueño, 403.
- Mensajes nuevos (`timeline.*`) en los `messages*.properties`, igual que los existentes.

### B2. Servicio `CohortSummaryService` (nuevo, en `services/dashboard/`)
`@Transactional(readOnly = true) CohortSummaryView summaryOf(UUID courseCohortId, UUID groupId)`:
1. `RoadmapRef ref = roadmaps.ofCourse(courseCohortId)`. Si no tiene roadmap principal, 404, igual que las otras rutas por curso.
2. Matrículas activas. Si viene `groupId`, filtrar por `groupUnits.contextOf(courseCohortId).groupsByStudent()` (y 404 si la comisión no es de la cohorte; copiar la búsqueda de `GroupProgressService:~45`).
3. Con `n = 0`, o sin ningún movimiento de XP ni actividad: devolver `status: NO_DATA`, con `total_enrolled` real y todo lo demás `null`.
4. Con `n < minSample` (B5): `status: INSUFFICIENT_SAMPLE`. Se mantienen `total_enrolled`, los conteos de `by_node` y `nodes.by_status.completed` (son conteos, no identifican a nadie: **ver D3**). Promedios, percentiles, racha y `active_last_7_days` van `null`.
5. Si no, `status: AVAILABLE`, con:
   - `xp`: lista de `total_xp` ordenada → `total` (suma), `average` (redondeado a 1 decimal), `median`, `p10` y `p90`, por **nearest-rank** (método simple y determinista; documentarlo en `@Schema`).
   - `active_last_7_days`: unión de dos consultas nuevas, ambas **por cohorte** y **desde una fecha**:
     - `DailyActivityRepository`: `select distinct d.studentId ... where courseCohortId = :c and activityDay >= :since`;
     - `XpMovementRepository`: `select distinct m.studentId ... where courseCohortId = :c and recordedAt >= :since`;
     - después, intersecar con los alumnos del paso 2.
   - `nodes`:
     - una consulta de completados por `(nodeId, count)` para los roadmaps del alcance, uniendo `completed_node` (nodos no CONTENT) y `content_reading` (nodos CONTENT). Puede ser una consulta JPQL por tabla y sumar en Java;
     - restringir los conteos a los alumnos del paso 2 (`studentId in :ids`); con comisión, a esos alumnos;
     - `completed_pct_average` = promedio por alumno de completados / nodos disponibles no boundary, en % con 1 decimal. Necesita el conteo por alumno: `CompletedNodeRepository.countCompletedByStudent` es el precedente (nativo, `roadmapIds`), más las lecturas;
     - `by_status.completed` = suma; `enabled` y `blocked` van `null` en el PR 1 (D1).
   - `by_node`: `[{ node_id, completed, blocked: null }]` para **todos** los nodos disponibles no boundary del alcance, incluidos los que tienen `completed = 0`. Orden estable: sección y después la posición del nodo (como en el grafo). Si no hay orden simple, ordenar por `node_id`.
   - `streak`:
     - una consulta `daily_activity` de la cohorte con `activityDay >= hoy - 400 días` (alcanza para la racha actual);
     - agrupar por alumno y aplicar `runEnding` igual que `StreakService.view`;
     - `average_current` con 1 decimal; `max` = máximo de `max_streak` de las matrículas.
   - `students_without_lives`: conteo de `recovery_pending = true` entre los alumnos del paso 2.
   - `blocked_reasons`: `null` en el PR 1 (D1).
6. `generated_at = Instant.now(clock)`, `course_id`, `roadmap_id` (el principal).

> [!warning] Nada de identidades
> El DTO no tiene `student_id` en ningún lado. Hay que agregar un test que serialice la respuesta y verifique que no aparece `student`.

### B3. Servicio `XpTimelineService` (nuevo, mismo paquete)
`XpTimelineView timelineOf(UUID courseCohortId, LocalDate from, LocalDate to)`:
- Una consulta: `select m.studentId, m.recordedAt, m.xp from XpMovementEntity m where m.courseCohortId = :c and m.countedInCourse = true and m.recordedAt >= :fromInstant and m.recordedAt < :toExclusive`. `countedInCourse` mantiene la serie consistente con `total_xp` (T-17.3). Convertir `from` y `to` con `StudentZone.ID`.
- Otra: `daily_activity` de la cohorte en el rango, con `(studentId, activityDay)`.
- En Java, agrupar por semana ISO (`IsoFields.WEEK_BASED_YEAR` y `WEEK_OF_WEEK_BASED_YEAR`, formato `"%d-W%02d"`):
  - `xp_total` = suma de la semana;
  - `active_students` = alumnos distintos con movimiento **o** actividad en la semana (la misma regla que B2).
- **Emitir todas las semanas del rango**, también las vacías:
  - si en el rango no hay ningún dato, la respuesta es `status: NO_DATA` con `points` vacío;
  - si hay datos, las semanas sin movimientos van con `xp_total: 0` y `active_students: 0`. Ahí `0` es un dato real, no la falta de dato.
- Agregar al sobre `course_id`, `generated_at`, `granularity`, `from`, `to` y `status`.
- Con matrícula activa por debajo de `minSample`: `status: INSUFFICIENT_SAMPLE`, `active_students: null` y `xp_total` se mantiene. Ver D3.

### B4. Índice (migración nueva `V63__xp_movement_course_recorded_idx.sql`)
- `CREATE INDEX idx_xp_movement_course_recorded ON xp_movement (course_cohort_id, recorded_at);`
- SQL común a PostgreSQL y H2. **Verificar el número de versión libre** contra `develop` al momento del PR, porque otras ramas pueden tomar V63.
- `daily_activity` ya tiene `ix_daily_activity_student_cohort`, pero empieza por `student_id`. Si el plan de ejecución lo pide, sumar `(course_cohort_id, activity_day)` en la misma migración. Con cohortes chicas no hace falta (YAGNI): agregarlo solo si se ve lento.

### B5. Mínimo de muestra
- Property `app.dashboards.min-sample` (default `5`) en `application.properties`, con `@ConfigurationProperties` o `@Value` según cómo esté hecho `StreakProperties`.
- **No** se lee PAR-18 de Backoffice: hoy no existe en el catálogo (`acuerdos/backoffice.md` lista PAR-01, 08, 09, 12 y 13). Cuando Backoffice lo publique, se agrega en `HttpParCatalogClient`, como pasó con PAR-12.

### B6. Documentación
- `@Operation` con la **regla de activos** escrita tal cual la define B2 (criterio de aceptación), la de percentiles (nearest-rank) y la de semanas (ISO, zona `StudentZone.ID`).
- Si el repo tiene un README de endpoints o `docs/` de contratos, sumar los dos endpoints ahí (buscar dónde quedó documentado `/courses/{id}/progress`).

### Tests PR 1 (solo los pertinentes, sin la suite completa)
- `CohortSummaryServiceTest`, con H2 y datos sembrados:
  - `NO_DATA` (cohorte sin movimientos), `INSUFFICIENT_SAMPLE` (n < 5) y `AVAILABLE`;
  - percentiles con una lista conocida;
  - un CONTENT leído cuenta como completado;
  - `recovery_pending` cuenta;
  - activo por un intento desaprobado (`xp_movement` sin `daily_activity`);
  - el filtro por comisión (mock de `GroupUnitsService`).
- `XpTimelineServiceTest`: semanas vacías intermedias, borde de semana en `StudentZone`, `countedInCourse = false` excluido, rango inválido.
- `CohortDashboardControllerTest` (WebMvc, como `RankingControllerTest`):
  - ADMIN y GESTOR dan 200; PROFESSOR dueño da 200; PROFESSOR ajeno da 403; STUDENT da 403;
  - `granularity=day` da 400;
  - el JSON está en snake_case y sin `student_id`.
- Correr: `./mvnw -q test -Dtest='CohortSummaryServiceTest,XpTimelineServiceTest,CohortDashboardControllerTest,StreakServiceTest'`, más Checkstyle y PMD.

## 4. Plan Back — PR 2 (bloqueados y motivos; depende de D1)
- Reusar `NodeProgressService.progressFor(ref, studentId)` para cada alumno de la cohorte **en el servidor** (sin paginar por HTTP) y agregar:
  - `by_status.enabled/blocked`;
  - `blocked_reasons` (contar `NodeBlockReason` y emitir **todas** las claves del enum en snake_case, no solo las 3 del ejemplo);
  - `by_node.blocked`.
- Costo: N llamadas de vidas (una por alumno, por la `Context` lazy) más N×nodos evaluaciones. **Cachear el resumen** con Caffeine, que ya se usa en el repo (`RankingFallbackCache` y la caché de PAR). Clave `(courseCohortId, groupId)`, TTL corto (60 a 120 s, en una property). `generated_at` es el del cálculo cacheado, así el dashboard sabe cuán viejo es el dato.
- Si falla Accounting o Inventory al pedir vidas, esos campos van `null` y `status` queda en `AVAILABLE`. Evaluar sumar un `data_status: DEGRADED` como el ranking (`RankingDataStatus`).
- Tests: un `*CallBudgetTest`, como `GroupAccessCallBudgetTest`, que fije cuántas llamadas remotas hace el resumen para N alumnos.

## 5. Decisiones abiertas

| # | Pregunta | Recomendación |
|---|---|---|
| D1 | ¿Calculamos `enabled`/`blocked`/`blocked_reasons` evaluando el Gate por alumno (caro) o los dejamos `null`? | El PR 1 sale con `null`. `by_node.completed` ya muestra el cuello de botella: el nodo donde cae la cantidad de completados. El PR 2 con caché, solo si Backoffice confirma que lo va a usar. |
| D2 | ¿`students_without_lives` desde `recovery_pending` (proyección por eventos) o consultando Accounting? | Usar la proyección: es local, barata y alcanza para un agregado. Decírselo a Backoffice en la respuesta. |
| D3 | ¿Con muestra chica se ocultan también los conteos (`by_node`, `total_enrolled`)? | No: los conteos no identifican a nadie. Solo se ocultan promedios, percentiles y activos. Confirmar con Joaquín. |
| D4 | Organización (`X-Organization-Id`) | Dejarlo para cuando se mergee `tema-01-identity-permissions-adoption`. Ahí se aplica `CourseOrganizationGuard` en los dos endpoints. Avisarlo en la issue. |
| D5 | ¿Backoffice llama con el token del usuario (Gateway) o con un token técnico? | Si es técnico, sumar los dos paths al matcher de `SecurityConfig.java:62`, con `canReadCohortProgress`. |
| D6 | ¿Hace falta la variante `/roadmaps/{roadmapId}/progress/summary` para los roadmaps en modo ROADMAP? | No por ahora (YAGNI). Se agrega si el dashboard la pide. |

## 6. Respuesta para la issue (borrador para pegar)

> Lo tomamos desde G10 (Roadmap).
> 1. **Activo en 7 días** = un día con actividad registrada (aprobó un nodo o leyó un contenido obligatorio) **o** un movimiento de XP (incluye intentos desaprobados). Las lecturas no obligatorias no cuentan.
> 2. **La XP hoy no baja**: el ledger es de solo inserción y una recalificación suma un movimiento nuevo. Si a futuro se corrige por delta, la serie lo va a mostrar en la semana de la corrección, sin reescribir las semanas anteriores.
> 3. **Primera entrega:** `summary` con XP, percentiles, activos, racha, alumnos sin vidas, % de avance y completados por nodo, más `xp-timeline` semanal. **Segunda entrega:** `enabled`/`blocked`/`blocked_reasons` por nodo. Requieren evaluar el Gate por alumno, así que saldrán cacheados unos minutos.
> 4. `students_without_lives` sale de nuestra proyección de eventos de Accounting (`recovery_pending`).
> 5. Muestra mínima: 5 por property hasta que exista PAR-18. Organización: cuando entre la integración multi-organización.
> ¿Algo más?: `by_node` incluye todos los nodos, también los que tienen 0 completados. Si les sirve, podemos sumar el tiempo medio hasta completar cada nodo (`completed_node.completed_at` contra la habilitación), en una iteración aparte.

## 7. Fuera de alcance
- Lo que pide Backoffice a otros micros.
- `granularity` distinta de `week`.
- El resumen por roadmap en modo ROADMAP (D6).
- Leer PAR-18 (todavía no existe).

## 8. Orden de trabajo recomendado
1. Responder la issue con la sección 6 y esperar D1, D3 y D5 de Joaquín. **No hace falta esperar para empezar el PR 1.**
2. PR 1: B4 → B2 → B3 → B1 → B5 → B6 → tests pertinentes → PR contra `develop` con `Closes` solo si D1 se resuelve como "no hace falta"; si no, `Refs #309`.
3. PR 2, si D1 lo pide.

## 9. Cierre
- [ ] PR 1 mergeado ([#325](https://github.com/2026-P4-BE/tpi-roadmap/pull/325) abierto)
- [ ] PR 2 mergeado, o D1 descartado
- [ ] Backoffice confirma el contrato en la issue (respuesta publicada; quedó pendiente D5, qué token usa Backoffice)
- [x] Issue #309 cerrada
