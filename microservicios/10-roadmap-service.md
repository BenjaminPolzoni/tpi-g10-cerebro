# Microservicio: Roadmap Service (`tpi-roadmap`)

> **Ficha Técnica Canónica y Manual de Arquitectura**  
> Tema: **Tema 10 — Roadmap Gamificado y Progresión de Aprendizaje**  
> Equipo Responsable: **Grupo 10 (G10)**  
> Repositorio: `2026-P4-BE/tpi-roadmap` (Local: `D:\Dev\IdeaProjects\Progra4\tpi-roadmap`)  
> Estado: **Release v2.0.0 / Migraciones Flyway V1..V26**

---

## 1. Identidad y Red

| Parámetro | Valor |
|---|---|
| **Nombre de Aplicación (Eureka)** | `roadmap-service` |
| **Prefijo en API Gateway** | `/api/roadmap/**` (preservado sin reescritura) |
| **Puerto por Defecto** | `8010` |
| **Puerto de Gestión (Management/Actuator)** | `8011` (`management.server.port`) |
| **Rutas Públicas** | `${app.api.public-path}/**` (`/api/roadmap/public/**`, swagger y healthchecks) |
| **Rutas Privadas** | `${app.api.private-path}/**` (`/api/roadmap/**`) |
| **Consumer Group Kafka** | `tema-10-roadmap-service-group` |
| **Producer Kafka** | `tema-10-roadmap-service` |
| **Base de Datos** | PostgreSQL (H2 en tests unitarios con compatibilidad Postgres) |

---

## 2. Dominio y Funcionalidades Implementadas (v2.0.0)

### 2.1 Grafo de Roadmap y Progresión (`GraphController`, `NodeController`)
- **Jerarquía:** Unidades/Secciones (`Section`) y Nodos de actividad (`Node`).
- **Prerrequisitos de Nodo:** Soporta evaluación en modo `ALL` (debe completar todos los predecesores) o `ANY` (al menos uno).
- **Prerrequisitos de Unidad (`section_prerequisite`, V25):** Permite bloquear secciones completas hasta que se finalicen unidades anteriores.
- **Metadatos Visuales y 3D:**
  - Biomas de sección (`section_biome`, V22): Claves visuales (`FOREST`, `DESERT`, `VOLCANO`, `CYBER`, `OCEAN`).
  - Iconos de nodo (`node_icon_key`, V20): Representación en el canvas.
  - Campos del editor gráfico (`node_editor_fields`, V23): Coordenadas espaciales `(x, y, z)` para layout personalizado.
- **Lectura de Contenidos Formativos (`content_reading`, V4):** Registro de lectura obligatoria antes de habilitar el desafío asociado.

### 2.2 Gate de Elegibilidad Síncrono (`GateController`)
- Expuesto en: `GET /api/roadmap/courses/{courseId}/students/{studentId}/nodes/{nodeId}/eligibility`.
- **Reglas de Evaluación (en orden):**
  1. **Matrícula:** Alumno matriculado y activo en Courses (`course-service`).
  2. **Estado del Curso:** Curso no archivado ni en modo sólo lectura.
  3. **Prerrequisitos de Unidad:** Unidades precedentes obligatorias completadas (V25).
  4. **Prerrequisitos de Nodo:** Nodos predecesores completados según modo `ALL` o `ANY`.
  5. **Lecturas Previas:** Contenidos teóricos obligatorios leídos (`content_reading`).
  6. **Comisión / Grupo:** Restricción de grupo escolar cumplida si aplica (HU-44).
  7. **Vidas Disponibles:** $\text{freeLives} > 0$ en `accounting-service`.  
     *Excepción:* Nodos de tipo `RECOVERY` (recuperación de vidas) y `LLM` **no consultan vidas**.

### 2.3 Ledger de XP Propio (`XpHistoryController`)
- **Roadmap NO calcula XP (DEC-013):** Consume el evento `CHALLENGE_COMPLETED` desde `challenges.events`.
- Registra el movimiento en `xp_movement` (V10) de forma estrictamente append-only.
- Idempotencia garantizada por índice único sobre `event_id`.

### 2.4 Ranking Dinámico y Desempate en Cascada (`RankingController`)
- Cálculo en vivo del XP acumulado por cohorte.
- **Zonas Percentiles:** P90 (oro), MIDDLE (azul), P10 (naranja), activas dinámicamente **únicamente si la cohorte tiene $\ge 10$ alumnos**.
- **Desempate en Cascada (`RF-RNK-11`):**
  1. Mayor cantidad de insignias obtenidas.
  2. Menor cantidad de vidas perdidas históricamente (consultado a `accounting-service` en lote).
  3. Mayor cantidad de ejercicios completados.

- **Disponibilidad (T-45.7, [[decisiones/DEC-019-ranking-estado-de-datos-y-cache-de-respaldo|DEC-019]]):**
  - **Accounting o Backoffice caídos:** el ranking sale degradado (vidas perdidas o nivel nulos, mismo orden por XP) y la respuesta lo indica con `data_status=DEGRADED`.
  - **Users caído (vista del profesor):** si a alguna fila le falta el perfil (sale con seudónimo), también `data_status=DEGRADED`. El cliente no distingue "no lo tiene" de "no respondió" (T-45.7, revisión del PR #231).
  - **Fallo al armar el ranking después de autorizar** (por ejemplo, la base): se sirve el último ranking cacheado en memoria con `data_status=STALE` y su `generated_at`. Sin caché, `503 ranking.unavailable`.
  - **Autorización:** la validación de dueño (Courses o token técnico) y la de matrícula fallan cerrado (`503`). La caché nunca las saltea.
  - **Causa del 503:** el token técnico tiene su código (`courses.ownership-token-unavailable`), distinto de Courses caído (`courses.ownership-unavailable`).

### 2.5 Insignias y Niveles (`BadgeController`, `BadgeCatalogController`, `LevelController`)
- Insignias del sistema precargadas (V17) y otorgamiento automático (`badge_award`, V16).
- Curva oficial de 10 a 200 niveles sincronizada desde Backoffice (`PAR-09`) con caché Caffeine y actualización reactiva por Kafka.

### 2.6 Personalización 3D del Avatar (`StudentAvatarController`)
- Almacenamiento de modelo, colores y accesorios 3D por curso (`student_avatar`, V26), con validación de payload y baja lógica.

### 2.7 Sincronización con Secciones de Courses (`SectionSyncController`)
- Toggle `SECTIONS_SYNC_ENABLED` (HU-36): Sincronización unidireccional de títulos, orden y visibilidad de secciones desde Courses.

### 2.8 Roadmap por Comisión (`GroupProgressController`)
- Toggle `ROADMAP_BY_GROUP_ENABLED` (HU-44): Avance segmentado por comisiones escolares.

### 2.9 Catálogo y Pool de Desafíos (`ChallengePoolController`)
- Acceso al catálogo de desafíos sin filtrado restrictivo de autor para administradores y gestores.

### 2.10 Transactional Outbox (`outbox_event`, V15)
- Publicación confiable a `roadmap.events` de los eventos `NODE_COMPLETED`, `NODE_UNLOCKED`, `BADGE_AWARDED` y `ROADMAP_MANDATORY_AVAILABILITY_CHANGED` (wire snake_case, key `student_id`). `COURSE_LEVEL_UP` y `PERFORMANCE_ZONE_CHANGED` están declarados pero todavía no se emiten.

---

## 3. Matriz de Endpoints REST de Roadmap

| Método | Endpoint | Roles Permitidos | Propósito |
|---|---|---|---|
| `GET` | `/api/roadmap/courses/{courseId}/graph` | `STUDENT,PROFESSOR,MANAGER,ADMIN` | Obtener árbol completo de unidades y nodos con estado. |
| `POST` | `/api/roadmap/courses/{courseId}/nodes` | `PROFESSOR,MANAGER,ADMIN` | Crear nuevo nodo en el grafo. |
| `PUT` | `/api/roadmap/courses/{courseId}/nodes/{id}` | `PROFESSOR,MANAGER,ADMIN` | Actualizar configuración y prerrequisitos del nodo. |
| `DELETE`| `/api/roadmap/courses/{courseId}/nodes/{id}` | `PROFESSOR,MANAGER,ADMIN` | Baja lógica de nodo (valida dependencias huérfanas). |
| `GET` | `/api/roadmap/courses/{courseId}/students/{studentId}/nodes/{nodeId}/eligibility` | M2M (`engine-challenge-service`), UI | Gate de elegibilidad para iniciar intento. |
| `GET` | `/api/roadmap/courses/{courseId}/rankings` | `STUDENT,PROFESSOR,MANAGER,ADMIN` | Tabla de posiciones y zonas percentiles. |
| `GET` | `/api/roadmap/courses/{courseId}/levels` | Todos | Curva y umbrales de niveles PAR-09. |
| `GET` | `/api/roadmap/courses/{courseId}/students/{studentId}/xp/history` | Propio alumno o docente | Historial de movimientos del ledger de XP. |
| `GET` | `/api/roadmap/courses/{courseId}/inventory` | `STUDENT` | BFF de inventario, vidas e ítems equipados (HU-35). |
| `GET` | `/api/roadmap/courses/{courseId}/students/{studentId}/avatar` | Todos | Obtener avatar 3D del alumno (V26). |
| `PUT` | `/api/roadmap/courses/{courseId}/students/{studentId}/avatar` | Propio alumno | Guardar configuración 3D del avatar (V26). |
| `GET` | `/api/roadmap/courses/{courseId}/challenges/pool` | `PROFESSOR,MANAGER,ADMIN` | Pool de desafíos disponibles para asignar. |

---

## 4. Historial de Migraciones Flyway (V1 .. V26)

| Versión | Descripción |
|---|---|
| **V1** | Esquema inicial: `roadmap`, `section`, `node`, `prerequisite`. |
| **V2** | Soporte de tipos de nodo: `CHALLENGE`, `READING`, `MILESTONE`. |
| **V3** | Modos de prerrequisito: regla de evaluación `ALL` o `ANY`. |
| **V4** | Tabla `content_reading`: registro de lecturas formativas previas obligatorias. |
| **V5** | Metadatos de orden y visibilidad en secciones. |
| **V6** | Índices de rendimiento sobre `course_id` y `student_id`. |
| **V7** | Soporte de cohortes y aislamiento de roadmap por cohorte. |
| **V8** | Restricciones de archivado de curso (`archived`). |
| **V9** | Campos de auditoría `created_at`, `updated_at`, `created_by`. |
| **V10** | Tabla `xp_movement`: ledger append-only con índice único sobre `event_id`. |
| **V11** | Estados de progreso del alumno en nodos (`student_node_progress`). |
| **V12** | Soporte para desafíos de recuperación de vida (`RECOVERY`). |
| **V13** | Campos de puntuación máxima y ponderación en nodos. |
| **V14** | Vínculo explícito de contenidos de Courses (`content_id`). |
| **V15** | Tabla `outbox_event` para publicación transaccional a Kafka. |
| **V16** | Tabla `badge_award`: asignación de insignias a estudiantes. |
| **V17** | Precarga de catálogo de insignias del sistema. |
| **V18** | Índices compuestos para optimización de cálculo de ranking en vivo. |
| **V19** | Soporte de soft-delete en nodos y secciones (`deleted_at`). |
| **V20** | Metadato visual `node_icon_key` en nodos. |
| **V21** | Historial de transiciones de zonas percentiles (`performance_zone_history`). |
| **V22** | Metadato visual `section_biome` en secciones. |
| **V23** | Coordenadas espaciales `(x, y, z)` para editor gráfico (`node_editor_fields`). |
| **V24** | Flag `recovery_pending` en progreso del estudiante. |
| **V25** | Tabla `section_prerequisite`: prerrequisitos entre unidades/secciones. |
| **V26** | Tabla `student_avatar`: personalización de modelo y accesorios 3D del alumno. |

---

## 5. Convenciones de Calidad y Tests

- **Testing:** JUnit 5 con mocks (`Mockito`), base H2 en memoria con compatibilidad Postgres y soporte de Testcontainers.
- **Quality Gates Mandatorios:** `mvn verify` corre Checkstyle, PMD y CPD sin advertencias permitidas.
- **Idempotencia y Transaccionalidad:** Toda mutación de progreso y outbox se ejecuta dentro de `@Transactional`.
