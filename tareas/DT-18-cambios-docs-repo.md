---
tags: [tpi, g10, tarea, deuda-tecnica, kafka, docs-repo]
fecha: 2026-10-27
estado: pendiente-de-aplicar
---

# DT-18 — Cambios propuestos a los docs del repo `tpi-roadmap`

No se commitearon al repo (decisión del equipo: los docs de tareas van al vault). Es el diff exacto de `README.md`, `AGENTS.md`, `.agents/agent.md` y `docs/faq-notifications-bus.md` contra `develop` (`fea2fece`). Para aplicarlo: copiar el bloque a un archivo `dt18.patch` y correr `git apply --ignore-whitespace dt18.patch` en una rama desde `develop`. Hallazgos y contexto: [[tareas/DT-18-hallazgos-kafka-snake-case]].

```diff
diff --git a/.agents/agent.md b/.agents/agent.md
index db275bd7..656a2f8d 100644
--- a/.agents/agent.md
+++ b/.agents/agent.md
@@ -136,7 +136,7 @@ En el bus Kafka el Tema 10 figura como **"Ranking / XP"**: consume resultados de
 | **Progreso / historial del alumno** | RF-CUR-01, KPI-06/07 | **Implementado.** Registro de lecturas (`content_reading`, V4), nodos completados (`completed_node`), desbloqueos (`node_unlock`, V9/V11). |
 | **Gate de Elegibilidad** | §3.0, cerebro: `contratos/roadmap-motor-gate-v1.md` | **Implementado.** `GateController` valida matrícula en Courses, curso no archivado, prerrequisitos, lecturas obligatorias y vidas libres > 0 en Accounting. |
 | **XP: registro y acumulación** | RF-CFG-06, RF-NIV-05, RF-REC-01 | **Implementado.** Recibimos XP calculado vía Kafka `challenges.events`. |
-| **Ledger de XP propio** | `xp_movement` append-only | **Implementado.** `xp_movement` (V10) con índice único por `eventId`, inmutable e idempotente. Accounting no conoce el XP; Roadmap es la fuente única. |
+| **Ledger de XP propio** | `xp_movement` append-only | **Implementado.** `xp_movement` (V10) con índice único por `event_id`, inmutable e idempotente. Accounting no conoce el XP; Roadmap es la fuente única. |
 | **Vidas: consulta en Gate y desempate** | RF-RNK-05/11/12 | **Implementado.** Consulta en vivo a Accounting (`equip-summary` / `lives-availability`). Histórico de vidas perdidas para desempate consultado por lote a Accounting (`/accounts`). |
 | **Niveles** | RF-NIV-01..05, PAR-09 | **Implementado.** Curva oficial de 10 niveles (PAR-09 de Backoffice con caché y actualización reactiva por Kafka) + niveles custom por curso. |
 | **Ranking y percentiles** | RF-RNK-01..12 | **Implementado.** Ranking por cohorte, percentiles P90 / MIDDLE / P10 (umbral ≥ 10 alumnos) y cascada de desempate completa (`RF-RNK-11`). |
@@ -198,12 +198,12 @@ En la misma transacción que modifica el negocio, se inserta en `outbox_event` (
 por alumno, para que un fallo de Courses no revierta el XP ni la matrícula. El `OutboxPoller` publica periódicamente a `roadmap.events`:
 - `NODE_COMPLETED`: Estudiante completó un nodo de desafío.
 - `NODE_UNLOCKED`: Nodo desbloqueado por cumplimiento de prerrequisitos.
-- `COURSE_LEVEL_UP`: Alumno alcanzó un nuevo nivel en el curso.
 - `BADGE_AWARDED`: Alumno obtuvo una insignia.
-- `PERFORMANCE_ZONE_CHANGED`: Cambio de zona percentil (P90 / MIDDLE / P10).
 - `ROADMAP_MANDATORY_AVAILABILITY_CHANGED`: Cambio en los contadores de desafíos obligatorios/opcionales disponibles
   para el alumno (#252). Payload snake_case, key `student_id`, deduplicado por `(course_cohort_id, student_id)`.
 
+Declarados en el catálogo pero **sin emisión en el código** (verificado contra `OutboxService` y sus llamadores en DT-18, 2026-10-27): `COURSE_LEVEL_UP` (alumno alcanzó un nuevo nivel) y `PERFORMANCE_ZONE_CHANGED` (cambio de zona percentil P90 / MIDDLE / P10). Todos los eventos propios llevan `producer = tema-10-roadmap-service`. Contrato completo: `tpi-g10-cerebro/contratos/roadmap-events-v1.md` y `roadmap-service.asyncapi.yaml`.
+
 ---
 
 ## 4. Guía Operativa Docker: Backend y Frontend (Local y Mesh)
@@ -345,10 +345,10 @@ Todo error HTTP se emite con `Content-Type: application/problem+json` incluyendo
 ```json
 {
   "event_id": "550e8400-e29b-41d4-a716-446655440000",
-  "event_type": "CHALLENGE_COMPLETED",
+  "event_type": "NODE_COMPLETED",
   "event_version": 1,
   "timestamp": "2026-10-15T08:30:00.000Z",
-  "producer": "roadmap-service",
+  "producer": "tema-10-roadmap-service",
   "payload": { }
 }
 ```
@@ -356,16 +356,16 @@ Todo error HTTP se emite con `Content-Type: application/problem+json` incluyendo
 - `event_type`: SNAKE_CASE en inglés, en pasado (`NODE_COMPLETED`, `COURSE_LEVEL_UP`).
 - `event_version`: entero obligatorio, hoy `1`; el bus rechaza el sobre sin él.
 - `timestamp`: UTC ISO 8601.
-- `producer`: `roadmap-service` (en properties: `tema-10-roadmap-service`).
+- `producer`: `tema-10-roadmap-service` (propiedad `app.kafka.producer`).
 
 ### 6.2 Matriz de Tópicos
 | Topic | Dirección | Clave | Eventos Principales |
 |---|---|---|---|
-| `challenges.events` | Consumo | `userId` | `CHALLENGE_COMPLETED`, `CHALLENGE_ABORTED` |
-| `accounting.events` | Consumo | `studentId` | `LIFE_CREDITED`, `LIFE_DEBITED` |
-| `administration.events`| Consumo | `param_key` | `GLOBAL_CONFIGURATION_CHANGED` (PAR-09) |
-| `courses.events` | Consumo | `courseId` | Ciclo de vida y matriculaciones |
-| `roadmap.events` | Publicación (Outbox) | `studentId` | `NODE_COMPLETED`, `NODE_UNLOCKED`, `COURSE_LEVEL_UP`, `BADGE_AWARDED`, `PERFORMANCE_ZONE_CHANGED`, `ROADMAP_MANDATORY_AVAILABILITY_CHANGED` |
+| `challenges.events` | Consumo | `id_user` | `CHALLENGE_COMPLETED`, `CHALLENGE_ABORTED`, `CHALLENGE_ARCHIVED`, `CHALLENGE_RESULT_RECTIFIED` |
+| `accounting.events` | Consumo | `student_id` | `LIFE_CREDITED`, `LIFE_DEBITED` |
+| `administration.events`| Consumo | `param_key` | `GLOBAL_CONFIGURATION_CHANGED` (PAR-09), `PARAMETER_DEFINITION_CREATED` |
+| `courses.events` | Consumo | `course_cohort_id` / `student_id` (según el agregado) | `STUDENT_ENROLLED`, `STUDENT_UNENROLLED`, `COURSE_COHORT_ARCHIVED` |
+| `roadmap.events` | Publicación (Outbox) | `student_id` | `NODE_COMPLETED`, `NODE_UNLOCKED`, `BADGE_AWARDED`, `ROADMAP_MANDATORY_AVAILABILITY_CHANGED` |
 
 ---
 
diff --git a/AGENTS.md b/AGENTS.md
index 55d308af..fd67c39c 100644
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -134,7 +134,7 @@ El repositorio [**`tpi-g10-cerebro`**](file:///D:/Dev/IdeaProjects/Progra4/tpi-g
 9. **Pool de Desafíos (`ChallengePoolController`):**
    - Catálogo de desafíos disponibles para asignar al roadmap sin filtro restrictivo de autor para administradores y gestores.
 10. **Transactional Outbox (`outbox_event`, V15):**
-    - Publicación confiable a `roadmap.events` de los eventos `NODE_COMPLETED`, `NODE_UNLOCKED`, `COURSE_LEVEL_UP`, `BADGE_AWARDED` y `PERFORMANCE_ZONE_CHANGED`.
+    - Publicación confiable a `roadmap.events` (wire `snake_case`, key `student_id`) de los eventos `NODE_COMPLETED`, `NODE_UNLOCKED`, `BADGE_AWARDED` y `ROADMAP_MANDATORY_AVAILABILITY_CHANGED`. `COURSE_LEVEL_UP` y `PERFORMANCE_ZONE_CHANGED` están declarados en el catálogo pero el código todavía no los emite.
 11. **Múltiples Roadmaps por Curso (T-17.1, V27):**
     - Soporte de múltiples roadmaps por cohorte con un roadmap principal (`roadmap.is_primary`). Las rutas por curso resuelven el roadmap principal.
 
diff --git a/README.md b/README.md
index 4c9b7c19..2283a49a 100644
--- a/README.md
+++ b/README.md
@@ -119,9 +119,9 @@ El ranking suma `course_average` y `course_average_status` (#310), calculados so
 
 Errores en Problem Details (RFC 7807) con `traceId`; textos en `messages.properties`.
 
-### Consumidor y Productor Kafka (contratos-kafka v3)
+### Consumidor y Productor Kafka (contratos-kafka v8+)
 
-La fuente de verdad para la integración asíncrona es la skill oficial `contratos-kafka` (v8) del Skill Hub
+La fuente de verdad para la integración asíncrona es la skill oficial `contratos-kafka` (v8 en adelante; hoy v12) del Skill Hub
 (mantenida por Social y Notificaciones). Reemplaza cualquier estándar previo o documento local. Todo mensaje
 viaja en texto plano JSON (con `StringSerializer` y `StringDeserializer`) y en **snake_case** (sobre y payload),
 respetando estrictamente el sobre canónico obligatorio de 6 campos:
@@ -141,17 +141,20 @@ respetando estrictamente el sobre canónico obligatorio de 6 campos:
   estrictamente el entero `1` (ausente, decimal o texto `"1"` derivan a DLT). Un sobre en camelCase va a la DLT:
   v8 admite un único nombre por campo.
 - **Consumo por dominios**:
-  - `challenges.events`: `CHALLENGE_COMPLETED` y `CHALLENGE_ABORTED` (dominio Desafíos / Tema 03).
+  - `challenges.events`: `CHALLENGE_COMPLETED`, `CHALLENGE_ABORTED`, `CHALLENGE_ARCHIVED` y `CHALLENGE_RESULT_RECTIFIED` (dominio Desafíos / Tema 03; key `id_user`; se filtra por `producer = tema-03-challenges-service`).
+  - `accounting.events`: `LIFE_CREDITED` y `LIFE_DEBITED` (dominio Contabilidad / Tema 08); el payload de Accounting sigue en camelCase y se acepta con alias de lectura hasta `tpi-accounting#227`.
   - `courses.events`: `STUDENT_ENROLLED`, `STUDENT_UNENROLLED` y `COURSE_COHORT_ARCHIVED` (dominio Cursos / Tema 02).
-  - `administration.events`: `PAR_STATUS_CHANGED` (dominio Administración / Tema 12).
+  - `administration.events`: `GLOBAL_CONFIGURATION_CHANGED` y `PARAMETER_DEFINITION_CREATED` (dominio Administración / Tema 12; key `param_key`).
   - `challenges.results` (**retirado**): el listener del formato anterior v1/v2 queda apagado por defecto
     (`app.kafka.topics.challenge-result.enabled=false`); se borra en el próximo sprint.
 - **Consumer Group**: `tema-10-roadmap-service-group` configurado en properties y listeners con `ack-mode: manual`.
 - **Resiliencia y DLT**: 3 reintentos con intervalo fijo de 2000 ms (`FixedBackOff`). Los errores no reintentables
   (`NonRetryableEventException`) o eventos que agotan reintentos son derivados a la DLT del dominio emisor
   (`<dominio>.events.DLT`).
-- **Productor / Outbox**: Publicación de eventos de progreso en el grafo (`NODE_COMPLETED` y `NODE_UNLOCKED`)
-  con clave de agregado `student_id` y productor `tema-10-roadmap-service`. Brecha declarada (P-09): tópico de Roadmap
+- **Productor / Outbox**: Publicación de eventos de progreso (`NODE_COMPLETED`, `NODE_UNLOCKED` y `BADGE_AWARDED`)
+  con clave de agregado `student_id` y productor `tema-10-roadmap-service`. `COURSE_LEVEL_UP` y
+  `PERFORMANCE_ZONE_CHANGED` están declarados pero el código todavía no los emite. Payloads en
+  `tpi-g10-cerebro/contratos/roadmap-events-v1.md`. Brecha declarada (P-09): tópico de Roadmap
   en el broker compartido pendiente de asignación por Tema 11. Cutover a v8: ver
   `tpi-g10-cerebro/tareas/T-191-KAFKA-V8-CUTOVER.md`.
 - **Disponibilidad obligatoria (#252)**: `ROADMAP_MANDATORY_AVAILABILITY_CHANGED` en `roadmap.events`, key
@@ -221,7 +224,7 @@ docker compose -f docker/docker-compose.yml up -d postgres
   para el topic real, la DLQ y la key del mensaje (P-09); hoy los defaults son una propuesta nuestra.
 - **Inscripciones y estado del curso** (Courses, #6): las filas de `student_course` entran por `STUDENT_ENROLLED` (Kafka) o por el fallback pull de participantes (HU-48).
 - **Outbox**: publica `NODE_COMPLETED`, `NODE_UNLOCKED`, `BADGE_AWARDED` y
-  `ROADMAP_MANDATORY_AVAILABILITY_CHANGED` en `roadmap.events` (topic, key `studentId` y `producer` definidos).
+  `ROADMAP_MANDATORY_AVAILABILITY_CHANGED` en `roadmap.events` (topic, key `student_id` y `producer` definidos).
 - **Token técnico para clientes salientes**: T-03.2 implementa el cliente HTTP de Accounting,
   su caché y degradación, pero `mode=http` requiere la implementación real de
   `TechnicalTokenProvider` cuando Gateway/Users confirme client_credentials y permisos.
diff --git a/docs/faq-notifications-bus.md b/docs/faq-notifications-bus.md
index 565b60a4..f5003f58 100644
--- a/docs/faq-notifications-bus.md
+++ b/docs/faq-notifications-bus.md
@@ -20,7 +20,7 @@ Para eventos de Roadmap, se utiliza el tópico existente **`roadmap.events`**, d
   "event_type": "NODE_COMPLETED",
   "event_version": 1,
   "timestamp": "2026-10-15T08:30:00.000Z",
-  "producer": "roadmap-service",
+  "producer": "tema-10-roadmap-service",
   "payload": {
     "student_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
     "course_id": "e2a1b3c4-d5e6-7f8a-9b0c-1d2e3f4a5b6c",
@@ -34,7 +34,7 @@ Para eventos de Roadmap, se utiliza el tópico existente **`roadmap.events`**, d
 
 ### Q3: ¿Cómo garantiza Roadmap que los eventos se publiquen incluso si Kafka se cae momentáneamente?
 **Respuesta:** Mediante el **Transactional Outbox Pattern**:
-1. Cuando un alumno completa un nodo o sube de nivel, la lógica del servicio guarda el cambio de negocio y un registro en la tabla `outbox_event` (migración V15) con estado `PENDING` **dentro de la misma transacción de PostgreSQL**.
+1. Cuando un alumno completa un nodo, se le desbloquea otro o recibe una insignia (el nivel todavía no genera evento), la lógica del servicio guarda el cambio de negocio y un registro en la tabla `outbox_event` (migración V15) con estado `PENDING` **dentro de la misma transacción de PostgreSQL**.
 2. Si la base confirma el commit, el evento queda asegurado.
 3. Un poller periódico en segundo plano (`OutboxPoller`) lee los eventos pendientes y los envía a Kafka. Si Kafka está caído, el poller reintenta más tarde sin pérdida de datos ni desincronización transaccional.
 
```
