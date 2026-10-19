---
tags: [tpi, g10, sprint-3, prs, cambios]
fecha: 2026-10-18
estado: vigente
---

# 14 — Cambios recientes: PRs de G10 del 14 al 18 de octubre

> [!info] Alcance
> - PRs de los integrantes de G10 mergeados a `develop` entre el **2026-10-14 (después de la release 2.0.0)** y el **2026-10-18 23:40**, más los que siguen abiertos.
> - Back `2026-P4-BE/tpi-roadmap` (tip `f5ed143`) y front `2026-P4-FE/2026-PIV-TPI-FE` (tip `79d0be13`). Del front solo se cuentan los PRs de G10.
> - Sale de leer la descripción de cada PR y de chequear `develop`. No se corrieron tests.
> - `BE#n` = PR del back, `FE#n` = PR del front.

## Resumen

1. **Varios roadmaps por curso ya están en el back**: modelo 1 a N, rutas por roadmap, gestión (crear, renombrar, principal, archivar) y XP/ranking por curso o por roadmap. Falta el clonado (BE#266, abierto).
2. **Reglas combinadas AND/OR completas en back y front** (`A y (B o C)`), con un solo evaluador para el gate y el alumno. El XP mínimo dentro de las reglas está en BE#268 (abierto).
3. **Neo4j**: compose, Spring Data, esquema versionado y módulo `graph` mergeados, pero **ningún servicio lo usa todavía**. Las relaciones con tipo (DEC-018) se guardan en **Postgres** (V38), según [[decisiones/DEC-021-postgres-fuente-de-verdad-neo4j-proyeccion|DEC-021]].
4. **Se cerraron varios pendientes del Sprint 2** (ver [[#Qué cerró de los pendientes del Sprint 2]]): gate con `origin_unavailable`, ícono solo en desafíos, baja de desafío del Motor, IDs de mock, selector de comisión en el ranking, `startChallenge` y los `stub` por defecto.
5. **Contrato común de errores** (RFC 9457, BE#227): todas las respuestas de error traen `code`, `params` y `errors[]`. Toda clave nueva de `messages.properties` tiene que estar en `ErrorCatalog` (lo controla un test desde BE#251).

## Back (tpi-roadmap)

### Varios roadmaps por curso (HT-17, HU-57)

| PR | Autor | Qué hace |
|---|---|---|
| [BE#215](https://github.com/2026-P4-BE/tpi-roadmap/pull/215) | Baltasar | T-17.1: varios roadmaps por cohorte con uno **principal** (`is_primary`, índice único parcial). V27 |
| [BE#217](https://github.com/2026-P4-BE/tpi-roadmap/pull/217) | Baltasar | T-19.4: el resultado del Motor suma en el roadmap **del nodo** (`id_node`), con caída al principal por `challenge_id` |
| [BE#218](https://github.com/2026-P4-BE/tpi-roadmap/pull/218) | Baltasar | T-17.2: rutas `/roadmaps/{roadmapId}/...` al lado de las de curso, vía `RoadmapResolver` |
| [BE#223](https://github.com/2026-P4-BE/tpi-roadmap/pull/223) | Baltasar | T-17.3, T-57.1, T-57.2: crear, listar, renombrar, elegir principal y archivar roadmaps (`multiple_roadmaps_allowed`). `progress_scope` `COURSE`/`ROADMAP` para XP, nivel, progreso y ranking, no retroactivo. V44 y V45 |

### Reglas de desbloqueo (HU-58, HU-59, HT-20)

| PR | Autor | Qué hace |
|---|---|---|
| [BE#224](https://github.com/2026-P4-BE/tpi-roadmap/pull/224) | Santino | T-59.1: reglas como **árbol AND/OR anidado** detrás de `RuleTreeStore` (hoy `JpaRuleTreeStore`). V28 |
| [BE#238](https://github.com/2026-P4-BE/tpi-roadmap/pull/238) | Santino | T-59.1: `GET /courses/{id}` y `GET /roadmaps/{id}` traen `rule` en cada nodo y sección. Una regla plana se lee como grupo de un nivel |
| [BE#247](https://github.com/2026-P4-BE/tpi-roadmap/pull/247) | Santino | T-20.1: **un solo evaluador** (`GateEvaluator.unlockBlock`) para gate, detalle, material y lectura |
| [BE#248](https://github.com/2026-P4-BE/tpi-roadmap/pull/248) | Santino | T-20.3: BDD del ejemplo de los profes (secciones 1 a 5) y de `A y (B o C)` |

### Grafo, Neo4j y relaciones con tipo (HT-16, HT-18, HU-65)

| PR | Autor | Qué hace |
|---|---|---|
| [BE#220](https://github.com/2026-P4-BE/tpi-roadmap/pull/220) | Iker | T-16.4: `docs/T-16-4-MODELO-GRAFO.md`, el modelo de la estructura en Neo4j |
| [BE#222](https://github.com/2026-P4-BE/tpi-roadmap/pull/222) | Iker | Neo4j `5.26-community` en `docker/docker-compose.yml` y `docker/neo4j/verificar-neo4j.sh` |
| [BE#237](https://github.com/2026-P4-BE/tpi-roadmap/pull/237) | Iker | Spring Data Neo4j + test de integración con Testcontainers. `NEO4J_HEALTH_ENABLED=false` |
| [BE#241](https://github.com/2026-P4-BE/tpi-roadmap/pull/241) | Iker | Módulo `graph` completo y esquema versionado con `neo4j-migrations`, solo con `NEO4J_MIGRATIONS_ENABLED=true` |
| [BE#246](https://github.com/2026-P4-BE/tpi-roadmap/pull/246) | Iker | Catálogo cerrado `RelationType` (DEC-018): **solo `requires` afecta el desbloqueo** |
| [BE#260](https://github.com/2026-P4-BE/tpi-roadmap/pull/260) | Iker | T-65.5: `node_relation`, `section_relation` y `roadmap_hidden_relation_type` en Postgres (V38) + API `/roadmaps/{roadmapId}/relations`. `requires` sigue en `node_prerequisite`/`section_prerequisite` |

### Gate, vidas y Motor (HT-31, HT-32)

| PR | Autor | Qué hace |
|---|---|---|
| [BE#234](https://github.com/2026-P4-BE/tpi-roadmap/pull/234) | Camacho | T-31.x: el gate responde `200` con `reason=origin_unavailable` en vez de `503` ([[decisiones/DEC-020-gate-origen-no-disponible-en-vez-de-503\|DEC-020]]). Se borró `ProgressService.startChallenge` |
| [BE#242](https://github.com/2026-P4-BE/tpi-roadmap/pull/242) | Iker | El gate informa `is_mandatory` (pedido del Motor, HU39 de ellos, #235) |
| [BE#245](https://github.com/2026-P4-BE/tpi-roadmap/pull/245) | Iker | Un nodo `RECOVERY` solo se ofrece con 0 vidas: motivo nuevo `lives_available` (RF-REC-04) |
| [BE#253](https://github.com/2026-P4-BE/tpi-roadmap/pull/253) | Camacho | T-32.1: consume `CHALLENGE_ARCHIVED` del Motor y marca `node.challenge_unavailable` (V30), separado de `available`. Motivo `challenge_unavailable` |
| [BE#263](https://github.com/2026-P4-BE/tpi-roadmap/pull/263) | Mateo | El gate publica `course_cohort_id` (#259), para que Prácticos cree el workspace en la organización correcta |
| [BE#225](https://github.com/2026-P4-BE/tpi-roadmap/pull/225) | Mateo | `GET /api/roadmap/challenges/{challengeId}/courses` (#216) para el Motor y el front |
| [BE#212](https://github.com/2026-P4-BE/tpi-roadmap/pull/212) | Mateo | ADMIN/GESTOR pueden asignar cualquier desafío publicado |

### Nodos y editor (HU-01, HU-41, HU-43)

| PR | Autor | Qué hace |
|---|---|---|
| [BE#250](https://github.com/2026-P4-BE/tpi-roadmap/pull/250) | Ludmila | T-32.5: `icon_key` solo en desafíos y exámenes (`NodeType.acceptsIcon()`), 400 `node.icon-requires-challenge` |
| [BE#265](https://github.com/2026-P4-BE/tpi-roadmap/pull/265) | Camacho | Los mensajes `error.node.challenge-*` ya no dicen «El nodo null…» en el alta |
| [BE#271](https://github.com/2026-P4-BE/tpi-roadmap/pull/271) | Ludmila | Corrección del 18/10: el nombre del **nodo** acepta 2 caracteres (`NODE_NAME_MIN_LENGTH`). Las **secciones siguen en 3** |

### Ranking (HU-45)

| PR | Autor | Qué hace |
|---|---|---|
| [BE#231](https://github.com/2026-P4-BE/tpi-roadmap/pull/231) | Benjamin | T-45.7: `data_status` (`FRESH`/`DEGRADED`/`STALE`), `generated_at`, caché de respaldo y 503 propio para el token técnico ([[decisiones/DEC-019-ranking-estado-de-datos-y-cache-de-respaldo\|DEC-019]]) |
| [BE#249](https://github.com/2026-P4-BE/tpi-roadmap/pull/249) | Benjamin | T-45.8: `group_id` opcional, recalcula puestos y cortes P90/P10 dentro de la comisión |
| [BE#251](https://github.com/2026-P4-BE/tpi-roadmap/pull/251) | Benjamin | Cataloga `ranking.unavailable`, el token técnico y `node.icon-requires-challenge`. Test `ErrorCatalogTest.everyMessageKeyIsInTheCatalog` |
| [BE#261](https://github.com/2026-P4-BE/tpi-roadmap/pull/261) | Benjamin | T-45.9: `available_groups` en el ranking y acceso del GESTOR |

### Sync con Courses (HU-17, HU-18, HU-36)

| PR | Autor | Qué hace |
|---|---|---|
| [BE#262](https://github.com/2026-P4-BE/tpi-roadmap/pull/262) | Mateo | Solo las **secciones raíz** de Courses son unidades. Antes las subsecciones hacían fallar el sync con 400 (`order_index` repetido) |
| [BE#264](https://github.com/2026-P4-BE/tpi-roadmap/pull/264) | Mateo | Una sección oculta en Courses queda como unidad **oculta** (`visible`), no dada de baja. V43 |
| [BE#228](https://github.com/2026-P4-BE/tpi-roadmap/pull/228) | Mateo | `HttpLostLivesClient` soporta la respuesta paginada de Accounting y la vieja (#221) |

### Plataforma, errores y config

| PR | Autor | Qué hace |
|---|---|---|
| [BE#227](https://github.com/2026-P4-BE/tpi-roadmap/pull/227) | Mateo | Contrato común de errores RFC 7807/9457: `code`, `params`, `errors[]`, `trace_id` (#214) |
| [BE#226](https://github.com/2026-P4-BE/tpi-roadmap/pull/226) | Mateo | Perfiles `dev` y `prod` separados: en prod no hay fallbacks a `localhost`, ni Swagger, ni `stub` por defecto (#219) |
| [BE#213](https://github.com/2026-P4-BE/tpi-roadmap/pull/213) | Mateo | AGENTS.md actualizado y docs movidos al cerebro (`microservicios/`) |

### Funcionalidades nuevas

| PR | Autor | Qué hace |
|---|---|---|
| [BE#240](https://github.com/2026-P4-BE/tpi-roadmap/pull/240) | Lautaro | T-73.1: tabla `daily_activity` (V29) para la racha. Solo registro, sin endpoint |
| [BE#254](https://github.com/2026-P4-BE/tpi-roadmap/pull/254) | Ludmila | T-69.2: `GET/PUT /courses/{courseId}/mentor`, personaje guía por curso («Hernán» por defecto). V33 |
| [BE#256](https://github.com/2026-P4-BE/tpi-roadmap/pull/256) | Stefano | HU-74 (pedido de G04, Modo Arcade): `GET /challenges/{challengeId}/world` y `GET .../students/me/pet` |

### Abiertos en el back

| PR | Autor | Qué falta saber |
|---|---|---|
| [BE#266](https://github.com/2026-P4-BE/tpi-roadmap/pull/266) | Baltasar | T-71.1/71.2: clonar roadmap con estructura, reglas y relaciones con tipo, sin progreso, en una transacción ([[sprints/sprint-3/historias/HU-71 Clonar un roadmap con sus restricciones\|HU-71]]) |
| [BE#268](https://github.com/2026-P4-BE/tpi-roadmap/pull/268) | Santino | T-58.1/T-20.2: `min_xp` dentro del árbol de reglas, evaluado con el XP del ámbito (`XpScopeService`). Saca `rule.min-xp-not-enforced` |
| [BE#255](https://github.com/2026-P4-BE/tpi-roadmap/pull/255) | Lautaro | T-73.2: racha en el progreso, flag `app.features.streak` apagado. Migración V46 |
| [BE#258](https://github.com/2026-P4-BE/tpi-roadmap/pull/258) | Lautaro | T-73.1: baja lógica de `daily_activity`. **Ver la alerta de migraciones** |

## Front (2026-PIV-TPI-FE, solo G10)

### Ranking y comisiones (HU-45, HU-44)

| PR | Autor | Qué hace |
|---|---|---|
| [FE#607](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/607) | Benjamin | HT-14: fuera `DEMO_STUDENT_ID`, `COURSE_SEED_ID` y `CURRENT_STUDENT_ID` del código de producción |
| [FE#615](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/615) | Ludmila | HT-26/T-26.5: `ranking-detail` en un `generic-drawer`, tablas nuevas del alumno y del profe, condiciones de promoción. Se borraron `ranking-panel` y las tablas viejas. Sale la racha fija |
| [FE#647](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/647) | Benjamin | T-45.7: un mensaje por cada error del ranking y aviso de datos `DEGRADED`/`STALE` |
| [FE#709](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/709) | Benjamin | T-45.9: selector «Comisión» en `/ranking/:courseId` (`?group=`), y acceso al ranking desde cada tarjeta de curso |
| [FE#739](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/739) | Benjamin | T-45.10: tabla «Comparar comisiones» en `/roadmap/teacher/progress/:id` |

### Editor de roadmap, reglas y nodos

| PR | Autor | Qué hace |
|---|---|---|
| [FE#691](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/691) | Santino | T-59.2: el asistente de reglas arma grupos AND/OR anidados (un nivel). Una regla plana se sigue guardando plana |
| [FE#727](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/727) | Mateo | Un prerrequisito que quedó después de su nodo (por un movimiento) aparece `blocked` |
| [FE#726](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/726) | Mateo | Editor de nodo por secciones; parámetros por curso del desafío (dificultad, XP base, reintentos, monedas, ítems, ventana de fechas, tiempo, examen) y combobox con búsqueda del pool |
| [FE#693](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/693) | Mateo | Las flechas ↑/↓ mueven el nodo dentro de su sección (antes usaban la lista global) |
| [FE#729](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/729) | Camacho | Toasts sin apilarse, desafío obligatorio para guardar un nodo desafío, nombre de 3 a 80, errores del back en español (`RoadmapApiError` con `code`, `errors[]`, `traceId`) |
| [FE#757](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/757) | Lorenzo | T-32.2: insignia «Desafío dado de baja» y aviso en el editor; el mapa abre con la disponibilidad real y la guarda por su endpoint |
| [FE#672](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/672) | Camacho | T-32.1: el alumno lee el motivo `challenge_unavailable` |
| [FE#624](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/624) | Camacho | T-31.2: el alumno ve el motivo del gate cuando el Motor rechaza el intento (`origin_unavailable`, `date_restricted`) en un solo toast |
| [FE#578](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/578) | Iker | Si el gate no responde, el `attempt_type` sale de la política de vidas del nodo (`RECOVERY → LIVES`) |

### Courses, unidades y sync

| PR | Autor | Qué hace |
|---|---|---|
| [FE#584](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/584) | Mateo | Modo Aventura desde cada tarjeta de curso; asistente de unidad completo (bioma, XP, posición, prerrequisitos) |
| [FE#721](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/721) | Mateo | Un sync rechazado con 400 muestra «materia inconsistente» sin reintento y loguea el `trace_id` |
| [FE#724](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/724) | Mateo | Rediseño de «Contenido del curso» del profe; reglas de unidad en el menú de la tarjeta; espeja `visible` de Courses |
| [FE#641](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/641) | Mateo | El mundo muestra el avatar editado dentro del curso; subsecciones anidadas hasta 5 niveles |
| [FE#626](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/626) | Ludmila | `no_lives` y `content_not_read` bloquean el intento, no la entrada a la unidad; la niebla se abre por prerrequisitos |
| [FE#658](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/658) | Ludmila | T-33.4: material en el panel de lectura; acepta URLs `http` de Garage; descarga, visor o enlace según cómo firma Courses |

### Insignias (HU-20, HU-22)

| PR | Autor | Qué hace |
|---|---|---|
| [FE#707](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/707) | Camacho | Catálogo de insignias y ranking con títulos y cards del kit |
| [FE#750](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/750) | Ludmila | Corrección del 18/10: cada insignia ganada dice su motivo y fecha; pantalla «Mis insignias» del alumno (`badge-showcase.ts` compartido) |

> [!warning] La edición de insignias del profe (T-30.1, [FE#743](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/743), Lorenzo) se **cerró sin mergear**.

### UI-KIT (HT-26)

| PR | Autor | Qué hace |
|---|---|---|
| [FE#665](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/665) | Ludmila | T-26.6: nombres de color actuales del kit y `var(--space-N)` (sin cambio visual) |
| [FE#704](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/704) | Lorenzo | T-26.2: `generic-title` y `genericButton` en las pantallas del roadmap |
| [FE#712](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/712) | Ludmila | Botones en la fila de pestañas del editor; Escape o clic en el mar cierra el cuadro de la isla |

### Personaje guía, mundos y Harbor

| PR | Autor | Qué hace |
|---|---|---|
| [FE#682](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/682) | Ludmila | T-69.1: charla con Enter y Tab |
| [FE#689](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/689) | Ludmila | T-69.2: pestaña «Personaje guía» (`?tab=guia`), nombre y aspecto por curso |
| FE#571 a FE#576, [FE#603](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/603), [FE#612](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/612) | Stefano | **Harbor** (`/harbor/:cohortId`): muelle 3D, editor de avatar modular, barra de cursos, vista «3D» en Mis Cursos |
| [FE#645](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/645), [FE#661](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/661), [FE#694](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/694) | Stefano | Tablero 3D a pantalla completa; «Mi Personaje» sin iframe (canvas Three.js nativo) y su arreglo de cámara |
| [FE#669](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/669), [FE#708](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/708) | Stefano | Aro guía del personaje, atmósfera día/atardecer/noche y rediseño low-poly de las islas del archipiélago |

### Mantenimiento de develop

- [FE#611](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/611) (Benjamin), revertido por [FE#614](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/614) y rehecho en [FE#618](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/618) (Mateo): compilación del chat (`PENDING_REVIEW`) y presupuesto de estilos de 4 kB.
- [FE#687](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/687) y [FE#690](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/690) (Lautaro): `.mailmap` para corregir un email sin `@` (solo afecta herramientas locales, no GitHub).

## Qué cerró de los pendientes del Sprint 2

Cruce con [[02-pendientes]] y [[01-estado-actual]]:

| Pendiente | Estado al 2026-10-18 |
|---|---|
| HU-15 `origen_no_disponible` | ✅ BE#234 (`origin_unavailable`, en inglés a pedido de G09) + FE#624 |
| HU-48 pre-chequeo del alumno | ✅ BE#234 (T-31.5): `GET /courses/{courseId}/nodes/{nodeId}/eligibility` con el JWT del alumno, y se borró `startChallenge` |
| HU-01 CA8 baja de desafío del Motor | ✅ BE#253 + FE#672 + FE#757 |
| HU-43 ícono solo en DESAFIO/EXAMEN | ✅ BE#250 |
| HU-44/45 selector de comisión | ✅ En el ranking (FE#709) y comparación del profe (FE#739). Sigue detrás de `ROADMAP_BY_GROUP_ENABLED` |
| IDs de mock en el front (P0-4) | ✅ FE#607 |
| `@DefaultValue("stub")` | ✅ BE#226 (no quedan en `src/main`) |
| UI-KIT 0.7.1 | ✅ `develop` usa `@2026-p4-fe/ui ^0.10.0` |
| HU-22 «Mis insignias» | ✅ FE#750 |
| HU-21 insignias que nunca se otorgan | ❌ `NODE_NO_RETRIES`, `LIFE_RECOVERED` y `SECTION_NO_LIVES_LOST` siguen solo en `BadgeCriterion` y V17 |
| HU-20 edición/baja de insignias en el front | ❌ FE#743 cerrado sin mergear |
| HU-01 posiciones del grafo | ❌ `moveNode` sigue devolviendo 501 (`node.position-local-only`) |
| HU-01/41 reintentos del nodo | ⚠️ El front ya pide «reintentos permitidos» (FE#726). **Hipótesis:** el back no tiene la columna; no se encontró migración |
| Ramas colgadas del back | ❌ Siguen `fix/account-not-found-gate`, `feature/t-21-7-roadmap-events-topic`, `bypass-desafio-11-10` y `revert-130-…` |
| `BankDataPort` en memoria | ❌ `InMemoryBankAdapter` sigue en `roadmap.providers.ts` |

## Alertas para el equipo

> [!danger] Migraciones de Flyway
> - En `develop` las últimas son **V43, V44 y V45** (hay huecos: V31, V32, V34-V37, V39-V42 no existen). Para una migración nueva, usar **V46 o más** y mirar las ramas abiertas: BE#255 ya toma V46.
> - **BE#258 trae V39** (`daily_activity_deleted_at`). Flyway no aplica fuera de orden por defecto (`outOfOrder=false`): en una base que ya tiene V45 la validación falla con «resolved migration not applied». Renumerar antes de mergear.
> - BE#264 se describió como V39 pero entró como **V43**. Si un PR dice un número, confirmarlo en el diff.

> [!warning] Otras
> - **Nombre del nodo:** el back acepta 2 caracteres desde BE#271 (corrección del 18/10), pero FE#729 valida de 3 a 80 en el front. `NAME_MIN_LENGTH = 3` en `entity-editor-dialog.component.ts:63` y `roadmap-error-message.ts:22`. El PR de Ludmila que lo bajaba a 2 ([FE#758](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/758)) se cerró sin mergear el 2026-10-18.
> - **Neo4j sigue apagado:** módulo y esquema están, pero las lecturas y escrituras siguen en Postgres (DEC-021). Las relaciones con tipo (V38) también.
> - **Contrato de errores:** toda clave nueva de `messages.properties` va también en `ErrorCatalog` y `RoadmapErrorCode`, o el test de BE#251 falla.
> - **Flags apagados:** `ROADMAP_BY_GROUP_ENABLED` (comisiones), `SECTIONS_SYNC_ENABLED`, `NEO4J_MIGRATIONS_ENABLED`, `app.features.streak` (BE#255).
