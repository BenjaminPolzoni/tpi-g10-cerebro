# T-03.3 — Suma al ledger con idempotencia y desbloqueos

Plan de implementación de la tarea T-03.3 de **HU-03**. Contexto funcional en `agent.md` §3.0, §3.1
y §5.4; el listener que trae el evento está en `docs/T-03-1-LISTENER-RESULTADO-MOTOR.md`.

> **Alcance de T-03.3**: `INSERT` en `xp_movement` con `event_id` único, donde el duplicado es
> **no-op silencioso con log**; si el resultado viene **aprobado** marca `completed_node` y **dispara
> la evaluación de desbloqueos**; si viene `esRepeticion` **descarta sin tocar nada**.

> **Etiqueta mal puesta, ya resuelta**: el identificador `T-03.3` aparecía en el repo referido al path
> del lote del catálogo de Courses, pero el commit que lo introdujo es
> `0b383ca feat(clients): T-03.4 cliente de catálogo de Courses con caché por lote`: la tarea de ese
> cliente es **T-03.4**. Se corrigen las cuatro referencias (`application.properties:23`,
> `docs/ESTRUCTURA.md:124`, `CoursesCatalogProperties.java:14` y la cita en
> `docs/T-03-1-LISTENER-RESULTADO-MOTOR.md:43`) en un commit `docs:` aparte de esta rama. `T-03.3` es
> esta tarea.

> **`esRepeticion` desactualizado (2026-09-27)**: este documento registra el diseño de la tarea
> cuando `esRepeticion` todavía era un campo real del evento. `motor-desafios.md` §2.2 ya lo daba
> por eliminado del contrato ("cae REQ-MOT-03: un alumno no puede volver a hacer un ejercicio que
> ya aprobó"), y ni el payload v2 ni `motor-desafios-evento-cierre.md` lo traen. Las menciones de
> abajo (§1, §3, §4) describen una rama ya mergeada y quedan como historia de esa implementación,
> no como contrato vigente del evento.

---

## 1. Qué ya está construido

T-03.1 dejó hecha la mayor parte de esta tarea. El estado real en `develop` (commit `4eddf75`):

| Punto del alcance | Estado | Dónde |
|---|---|---|
| `INSERT` en `xp_movement` con `event_id` único | Hecho | `ProgressService.insertMovement` + `uq_xp_movement_event_id` (`V1__esquema_inicial.sql`) |
| Duplicado = no-op | Hecho | Pre-check `movements.existsByEventId` + `DataIntegrityViolationException` → `DuplicateEventException` (carrera, H3 de T-03.1) |
| Duplicado **con log** | **Parcial** | El pre-check retorna sin loguear (`ProgressService:120`). Solo la carrera loguea, y en el listener (`RoadmapEventListener`, `DEBUG`) |
| Aprobado → `completed_node` | Hecho | `recordResult`, idempotente por `uq_completed_node` |
| Aprobado → **evaluación de desbloqueos persistida** | **Falta** | `recordResult` guarda `completed_node` y termina |
| `esRepeticion` → descarta sin tocar nada | Hecho | `ProgressService:116`, antes de cualquier lectura |
| XP y `total_xp` en la misma transacción | Hecho | `@Transactional` + lock pesimista de `student_course` (H3) |

---

## 2. Huecos

### 2.1 D-T033-01 — Persistir el desbloqueo al completar (revierte H5 de T-03.1)

Hoy el desbloqueo es **derivado en lectura**: `PrerequisiteService.isSatisfied` consulta
`completed_node` al vuelo, así que el alumno **ya puede avanzar** en cuanto llega el resultado
aprobado. No hay bug funcional. `node_unlock` solo se escribe desde
`GraphService:191` → `freezeReachedUnlocks`, es decir cuando el profesor está por cambiar las reglas
(HU-13 CA4).

T-03.1 §2.2 **H5** decidió exactamente lo contrario de lo que hacemos acá: *"el desbloqueo ya es
derivado… no se agrega persistencia nueva; `node_unlock` sigue siendo solo el congelado de HU-13"*.

**Decisión de T-03.3: se revierte H5.** El motivo que manda es la **trazabilidad de la causa**:
el desbloqueo tiene que dejar registrado *qué acción lo produjo*, no solo que el nodo quedó abierto.
La pregunta que hay que poder responder es "con esta aprobación, ¿qué caminos se abrieron?", y un
estado derivado no la responde: dice que el nodo está abierto, nunca por qué ni desde cuándo.

El CA1 de T-03.1 ("el nodo siguiente queda desbloqueado") ya se cumplía con la lectura derivada, así
que esto **no arregla un CA roto**: agrega el registro que la evaluación tiene que dejar. Como
consecuencia, además, `NODE_UNLOCKED` (`agent.md` §5.5) pasa a tener un instante concreto que
disparar cuando llegue el outbox (T-01.12.5).

Lo que **no** cambia: `isSatisfied` sigue consultando `completed_node` cuando no hay fila en
`node_unlock`, así que el progreso histórico (la semilla `demo`, lo cargado antes de esta rama) se
sigue resolviendo igual. La fila nueva es un atajo y un registro, nunca la única fuente de verdad.

### 2.2 D-T033-02 — Reusar `isSatisfied`, no `freezeReachedUnlocks`

`freezeReachedUnlocks(nodeId)` ya evalúa y persiste desbloqueos, pero barre **todos los inscriptos
del curso** por nodo: está pensado para el cambio de reglas del profesor. Llamarlo por cada evento
sería un escaneo del padrón completo por desafío superado. Se evalúa el **único alumno** del evento
con `isSatisfied`, que ya resuelve AND/OR y el congelado.

### 2.3 D-T033-03 — Las dos rutas que escriben `node_unlock` compiten por el unique

`recordResult` serializa los eventos del mismo alumno con el lock pesimista de `student_course`, así
que dos eventos no compiten entre sí. Pero `freezeReachedUnlocks` corre en **otra** transacción (el
profesor editando reglas) y no comparte ningún lock con la nuestra: `updateRules` toma
`roadmaps.findByIdForUpdate`, que serializa a los profesores entre sí, y el evento toma
`student_course`. Nadie serializa una contra la otra.

La carrera es **simétrica**, y las dos direcciones no son igual de graves:

| Quién llega segundo | Qué pasa sin protección | Gravedad |
|---|---|---|
| El evento de Kafka | Rollback; no queda fila en `xp_movement` y el reintento entra limpio (`DataIntegrityViolationException` no está en `addNotRetryableExceptions`) | Tolerable: se reintenta solo |
| **El profesor** | `freezeReachedUnlocks` filtró por `findStudentIdsByNodeId` **antes** de que nuestra fila existiera, su `saveAll` viola `uq_node_unlock` y **se cae todo el cambio de reglas con un 500** | **Grave: no hay reintento.** Un PATCH HTTP no se redespacha |

Una versión anterior de este plan solo miró la primera fila de esa tabla y concluyó que alcanzaba con
dejar explotar y reintentar. Eso rompía al profesor, y encima el pre-filtro de `freezeReachedUnlocks`
hace que el problema **no se reproduzca en un test secuencial**: solo aparece con una fila sin
commitear del otro lado.

**Decisión: un único camino de escritura, atómico.** `NodeUnlockRepository.insertIfAbsent` es un
`INSERT ... ON CONFLICT DO NOTHING` nativo que usan **las dos** rutas. El choque se resuelve dentro
del INSERT: no hay violación, no aborta ninguna transacción y devuelve `1` o `0` según quién insertó
(lo que además hace que el log nombre solo los caminos realmente abiertos). No hace falta lock nuevo
ni reintento, y la transacción del ledger queda intacta.

Portable: H2 corre en `MODE=PostgreSQL` (`src/test/resources/application.properties`), que acepta la
misma cláusula. Se usa `ON CONFLICT DO NOTHING` sin nombrar el constraint, que es la forma que
entienden los dos motores.

### 2.4 D-T033-04 — XP con `passed = false`

`recordResult` inserta en el ledger sea `passed` `true` o `false`; solo `completed_node` depende del
`passed`. **Se mantiene**: si el motor manda 0 XP en un fallo el movimiento queda en 0 y sirve de
traza del intento. No está definido en el PRD ni en el contrato de T-03.1 §3.2 → queda como pregunta
al Grupo 09 (§6), sin cambiar el comportamiento actual.

### 2.5 Bloqueantes externos

Ninguno nuevo. Los de T-03.1 (B1 topic, B3 DLQ, B4 delta/total, B5 key) siguen abiertos y no frenan
esta tarea: T-03.3 es todo del lado del service, después del listener.

---

## 3. Diseño

```
RoadmapEventListener ──► ProgressService.recordResult(eventId, result)   @Transactional
    1. esRepeticion = true        → log DEBUG + return, sin tocar nada        (ya estaba)
    2. eventId ya en xp_movement  → log DEBUG + return, no-op                 (se agrega el log)
    3. lock de student_course, validar alumno / nodo / challengeId cruzado    (ya estaba)
    4. INSERT xp_movement                                                     (ya estaba)
         unique de event_id → DuplicateEventException → el listener descarta
    5. sumar XP y vidas en student_course                                     (ya estaba)
    6. si passed:
         a. completed_node nuevo? → INSERT                                    (ya estaba)
         b. si era nuevo → prerequisites.recordUnlocksAfter(nodeId, studentId, eventId) ← NUEVO
                 para cada nodo que tiene a este como prerrequisito:
                     isSatisfied(sucesor, studentId) y sin fila previa → INSERT node_unlock
```

El paso 6b va **dentro** de la misma transacción: si falla el ledger, no queda un desbloqueo
huérfano. Y solo corre si el `completed_node` era **nuevo**: si el nodo ya estaba completado, los
desbloqueos que habilita ya se evaluaron.

### 3.1 Archivos que se tocan

```
src/main/java/com/utn/tpi/roadmap/
├── repositories/NodePrerequisiteRepository.java   + findByPrerequisiteNodeId (método derivado)
├── services/PrerequisiteService.java              + recordUnlocksAfter(nodeId, studentId)
└── services/ProgressService.java                  log del duplicado + llamada al paso 6b
src/main/java/com/utn/tpi/roadmap/
├── models/UnlockOrigin.java                       NUEVO (PROGRESS / RULE_CHANGE)
├── entities/NodeUnlockEntity.java                 + origin, unlockedByNodeId, unlockedByEventId
└── repositories/NodeUnlockRepository.java         + findByStudentIdAndNodeId
src/main/resources/db/migration/V11__node_unlock_origin.sql   NUEVO
src/main/resources/messages.properties             (reusa error.event.duplicate, ya existe)
src/test/java/com/utn/tpi/roadmap/
└── NodeUnlockOnResultTest.java                    NUEVO
```

La tabla, el unique y el repositorio de `node_unlock` ya existen desde HU-13; `V11` le agrega las tres
columnas de causa. Sin properties y sin cambios de contrato HTTP.

**`origin` explícito, no inferido.** La tabla pasa a tener dos orígenes con semántica distinta:
`RULE_CHANGE` (congelado del profesor, sin causa) y `PROGRESS` (progreso del alumno, con nodo y
evento causantes). Se guarda la columna en vez de deducirlo de `unlocked_by_node_id IS NULL`: se lee
sin conocer la convención, y si mañana aparece un tercer origen no hay que reinterpretar los nulos.
Las filas previas a `V11` son todas congelados, de ahí el `DEFAULT` en el `ALTER`, que se quita
enseguida para que toda fila nueva declare su origen.

### 3.2 `recordUnlocksAfter`

```java
@Transactional
public void recordUnlocksAfter(UUID completedNodeId, UUID studentId, UUID eventId) {
    List<UUID> opened = prerequisites.findByPrerequisiteNodeId(completedNodeId).stream()
            .map(NodePrerequisiteEntity::getNodeId)
            .distinct()
            .filter(nodeId -> !nodeUnlocks.existsByStudentIdAndNodeId(studentId, nodeId))
            .filter(nodeId -> isSatisfied(nodeId, studentId))
            .toList();
    nodeUnlocks.saveAll(opened.stream()
            .map(nodeId -> NodeUnlockEntity.builder()
                    .studentId(studentId).nodeId(nodeId)
                    .origin(UnlockOrigin.PROGRESS)
                    .unlockedByNodeId(completedNodeId)
                    .unlockedByEventId(eventId)
                    .build())
            .toList());
    if (!opened.isEmpty()) {
        log.debug("Evento {}: el alumno {} superó el nodo {} y desbloqueó {}",
                eventId, studentId, completedNodeId, opened);
    }
}
```

La lista `opened` es la evaluación misma: **qué nodos abre lo que el alumno acaba de aprobar**. Queda
en la base (una fila por camino, con su causa) y en el log, que dice la frase completa en un renglón.

- `distinct()`: un nodo puede llegar por más de una arista.
- El orden de los `filter` importa: el `exists` es más barato que `isSatisfied`.
- El insert pasa por `insertIfAbsent` (`ON CONFLICT DO NOTHING`), el mismo que usa
  `freezeReachedUnlocks`: la carrera con el profesor no rompe a ninguno de los dos (D-T033-03).
- **Un solo nivel**, sin cascada: si al desbloquear el nodo B se cumpliera además el prerrequisito de
  C, C se evalúa cuando **B se complete**, no cuando se desbloquea. Desbloquear no es completar, así
  que no hay cascada que seguir.

---

## 4. Pasos

1. **`NodePrerequisiteRepository`**: `List<NodePrerequisiteEntity> findByPrerequisiteNodeId(UUID)`,
   con Javadoc por parámetro (Checkstyle).
2. **`NodeUnlockRepository`**: `insertIfAbsent` (`ON CONFLICT DO NOTHING`), único camino de escritura.
3. **`PrerequisiteService`**: `recordUnlocksAfter`, y `freezeReachedUnlocks` pasa a usar el mismo insert (D-T033-03).
3. **`ProgressService`**: log del duplicado en el pre-check (`error.event.duplicate`, ya en
   `messages.properties`, RF-NFR-07) y llamada a `recordUnlocksAfter` solo cuando el
   `completed_node` se insertó en este evento.
4. **`NodeUnlockOnResultTest`** (sin broker, se invoca el service directo):
   - AND: aprobar el nodo 1 → el 5 (exige 1 y 2) **no** queda en `node_unlock`; aprobar el 2 → sí.
   - OR: aprobar el 7 → el 9 (exige 7 u 8) queda en `node_unlock` con una sola aprobación.
   - Sin sucesores: aprobar el último nodo no escribe nada.
   - `passed = false` → `xp_movement` sí, `completed_node` no, `node_unlock` no.
   - `esRepeticion = true` → ninguna de las tres tablas cambia.
   - Mismo `eventId` dos veces → un movimiento, un `completed_node`, un `node_unlock`.
   - Fila de `node_unlock` ya congelada por el profesor → el evento no falla ni duplica.
5. **`mvn verify`** local (hook `pre-push`): tests + Checkstyle + PMD.
6. **Etiqueta T-03.4**: commit `docs:` aparte que corrige las cuatro referencias que decían T-03.3
   (ver el recuadro del encabezado). No toca comportamiento.
7. **Documentación**: esta sección de `README.md` (bloque del consumidor Kafka) y
   `docs/ESTRUCTURA.md` si cambia el mapa de clases. En el PR, marcar que T-03.3 **revierte H5** de
   T-03.1 para que el revisor no lo lea como una contradicción.

Trazabilidad del PR: HU-03 · T-03.3 · RF-CUR-06 (reescrito, D-01) · RF-CFG-06 · RF-NIV-05 ·
`agent.md` §3.1 y §5.4.

---

## 5. Fuera de alcance de T-03.3

- **Outbox y publicación de `NODE_COMPLETED` / `NODE_UNLOCKED`** (T-01.12.5): no existe la tabla
  `outbox_event` ni el poller, y el topic es P-09 pendiente. Esta tarea deja el dato listo para
  cuando llegue.
- Ajustes posteriores de XP, delta vs. total (REQ-MOT-04, B4 de T-03.1).
- Niveles (PAR-09) y ranking P90/P10: consumen el XP registrado, son historias aparte.
- Lectura de vidas a Inventario: acá solo se guarda el valor vigente que trae el evento.

---

## 6. Preguntas para el equipo antes de cerrar el PR

1. **Taiga**: confirmar que la tarea del cliente de catálogo de Courses es **T-03.4**, como dice su
   commit `0b383ca`. Esta rama ya corrige las referencias que decían T-03.3.
2. **Grupo 09 (Motor)**: un resultado con `passed = false`, ¿manda `xp = 0` o un XP parcial? Define
   si el movimiento en 0 es traza útil o ruido (D-T033-04).
3. **Equipo**: confirmar que se revierte H5 de T-03.1 y que `node_unlock` pasa a registrar también
   los desbloqueos alcanzados por progreso, no solo los congelados antes de un cambio de reglas
   (D-T033-01).
