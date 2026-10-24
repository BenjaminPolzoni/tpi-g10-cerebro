---
tags: [tpi, g10, roadmap, qa, k-07]
---

# Resultados del QA: desafíos de recuperación y adicionales (K-07)

Fecha de la corrida: 2026-10-24. Checklist: `docs/roadmap/qa-recovery-additional-challenges.md` en el repo del front (corregido con esta corrida). Informe original en el mismo repo: `docs/roadmap/qa-recovery-additional-challenges-results.md`.
Frontend `feature/roadmap-integration` en `409369bac` (= `origin/develop`), servido con un proxy local
(ver "Entorno"). Backends: `tpi-roadmap` `develop` (ya estaba corriendo), `tpi-engine-challenge`
`develop` y `tpi-accounting` `develop` (clonados y levantados para esta corrida).

## Resumen

- **Primera corrida (stack incompleto): 0 de 8 filas ejecutables.** Accounting y el Motor estaban caídos,
  así que no se pudo crear ningún nodo de desafío ni leer el progreso de un alumno. Esa corrida queda al
  final como historia.
- **Segunda corrida (Motor y Accounting levantados, Practical simulado en su frontera de contrato):**
  el flujo real se ejecutó de punta a punta para **crear los dos nodos, un intento adicional fallido, un
  intento adicional aprobado y un intento de recuperación aprobado**. Se observaron XP, ranking, estado
  del nodo, billetera e historial antes y después de cada caso.
- **No se completó:** el crédito de la vida de la recuperación (bloqueado por Backoffice, ver BUG-4), el
  intento de recuperación fallido (se trabó un consumidor del Motor, ver BUG-5), la racha (la función
  viene apagada por defecto), las notificaciones (servicio ausente) y la UI de alumno (ningún alumno del
  mock coincide con uno de Courses, ver BUG-6).
- Ningún hallazgo es un defecto de la lógica de recuperación ni de los desafíos adicionales. El checklist
  tenía cuatro expectativas equivocadas (sección "Correcciones al checklist").

## Quién es dueño de qué

Cada fila de la corrida involucró varias piezas. Esta tabla separa lo que hizo cada una, para que un
hallazgo no se lea como un defecto de Roadmap cuando no lo es. "No verificado" significa que la corrida
no pudo determinarlo.

| Dueño                              | Funcionó como se esperaba (evidencia)                                                                                                                                                                                                                                                                                                                                                                                                                                            | Hallazgos                                                                                                                                                                                                                                       | No verificado                                                                                                                                                                |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Roadmap** (`tpi-roadmap`)        | La puerta (gate) y el progreso coincidieron con las vidas de Accounting (`lives_available`, `no_lives`, recuperación ofrecida con 0). Cierre fallido: entrada en el historial, sin XP, sin pérdida de vida. Cierre aprobado: +250 XP, nodo completado, ranking actualizado. Recuperación aprobada: nodo completado, 0 XP. Mandó a la DLT el evento camelCase del Motor `main`. Sincronización de unidades, alta del roadmap y persistencia de nodos (`RECOVERY`, `mandatory=f`). | Ninguno contra la lógica probada.                                                                                                                                                                                                               | Que refleje una vida de recuperación acreditada, la proyección `recovery_pending`, la racha (flag `STREAK_ENABLED` apagado), las zonas del ranking (hacen falta 10 alumnos). |
| **Frontend** (este repo)           | El asistente creó los dos nodos con el `lives_policy` y el `mandatory` correctos; el mundo 3D y la página del curso se renderizan.                                                                                                                                                                                                                                                                                                                                               | BUG-1 (la revisión dice "Sin prerrequisitos" mientras el padre encadena el nodo anterior como prerrequisito), BUG-2 (la revisión no muestra la política de vidas), BUG-3 (el `proxy.conf.json` por defecto cierra la sesión sin Notifications). | La vista de alumno con un alumno que coincida, y el texto "No tenés vidas disponibles".                                                                                      |
| **Motor** (`tpi-engine-challenge`) | Abrió intentos (`201`), aplicó la finalización y la corrección, calculó el veredicto contra el umbral y publicó un evento de cierre válido (`develop`: snake_case; `add_live=true`, 0 XP y 0 monedas para una recuperación aprobada).                                                                                                                                                                                                                                            | BUG-5 (un hilo consumidor queda en reintento ante un evento `ATTEMPT_FINALIZED`; no se capturó la causa). La release `main` (1.0.0) todavía emite el formato camelCase.                                                                         | Por qué falló ese evento; el intento de recuperación fallido (caso D).                                                                                                       |
| **Accounting** (`tpi-accounting`)  | Creó la cuenta al recibir `STUDENT_ENROLLED` (3 vidas), reservó y liquidó intentos, acreditó `CHALLENGE_CREDIT +50` monedas en la aprobación.                                                                                                                                                                                                                                                                                                                                    | BUG-4 (el crédito de la vida de recuperación va a la DLT cuando no puede leer PAR-12; no se verificó si existe un reproceso posterior).                                                                                                         | El crédito de la vida en sí, `min(L+1, max)`.                                                                                                                                |
| **Courses** (`tpi-course`)         | Sirvió cohortes, secciones, participantes y los endpoints con alcance de servicio que usan los demás.                                                                                                                                                                                                                                                                                                                                                                            | BUG-4 (la lectura de PAR-12 responde `503` porque faltan sus valores por defecto, que vienen de Backoffice), BUG-6 (su alumno matriculado no tiene login en el mock).                                                                           | Que emita `STUDENT_ENROLLED` para las matrículas sembradas (acá no lo hizo).                                                                                                 |
| **Backoffice** (`tpi-backoffice`)  | No estaba corriendo.                                                                                                                                                                                                                                                                                                                                                                                                                                                             | BUG-4 (origen de los valores por defecto de los parámetros).                                                                                                                                                                                    | Todo.                                                                                                                                                                        |
| **Practical** (Tema 05)            | No estaba corriendo: simulado.                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Ninguno.                                                                                                                                                                                                                                        | Aprovisionamiento, finalización, corrección.                                                                                                                                 |
| **Notifications** (Tema 11)        | No estaba corriendo.                                                                                                                                                                                                                                                                                                                                                                                                                                                             | BUG-3 (su ausencia rompe el proxy de desarrollo por defecto).                                                                                                                                                                                   | La campana y los avisos.                                                                                                                                                     |
| **Checklist y entorno**            | —                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Cuatro expectativas equivocadas; no hay gateway en `:8080`, un curso de Roadmap que no existe en Courses, ningún alumno del mock consistente.                                                                                                   | —                                                                                                                                                                            |

Dónde se arregla BUG-4 lo deciden los equipos de Courses, Accounting y Backoffice: la corrida solo
muestra que la aprobación se mandó a la DLT cuando el parámetro no estaba disponible.

## Qué dice esta corrida sobre Roadmap

En los casos que se ejecutaron, **Roadmap trató correctamente los datos que recibió**:

- La puerta coincidió con las vidas de Accounting en cada paso (`lives_available` con 3 vidas;
  `no_lives` y nodo de recuperación ofrecido con 0).
- Un cierre fallido registró la entrada en el historial y no dio XP ni quitó vida; un cierre aprobado dio
  el XP (250), completó el nodo y movió el ranking.
- Un cierre de recuperación aprobado completó el nodo con 0 XP, como dice el contrato.
- Rechazó con una carta muerta (DLT) el evento de cierre del Motor `main` (formato camelCase), como
  corresponde.

Lo que esto **no** demuestra:

- El crédito de la vida de una recuperación aprobada vive en Accounting, que no pudo hacerlo (BUG-4). No
  se ejercitó si Roadmap refleja una vida acreditada ni su proyección `recovery_pending`.
- El servicio Practical se simuló, así que los datos de entrada son verosímiles, no reales.
- Un alumno, un desafío, un curso. Sin zonas de ranking con 10 alumnos ni otros tipos de nodo.
- La racha (flag apagado) y las notificaciones (servicio ausente) no se probaron.
- Los dos problemas del asistente (BUG-1, BUG-2) son del frontend, BUG-4 es de Backoffice, Courses y
  Accounting, y BUG-5 es del Motor; no son de Roadmap.

## Entorno (segunda corrida)

Este entorno temporal se **desarmó después de la corrida**: se eliminaron el Motor, Accounting, el gateway
de desarrollo y el MySQL de Accounting; el contenedor de Roadmap se recreó con su configuración original;
el roadmap de QA y sus datos se borraron de Roadmap; y se eliminaron la base del Motor y los topics,
grupos y registros de Kafka creados para la corrida. Queda un evento `STUDENT_ENROLLED` en
`courses.events`. Repetir la corrida implica reconstruirlo con las notas de la sesión.

| Pieza               | Cómo                                                                                                                                                                          | Notas                                                                                                                                                                                                                          |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Roadmap `:8010`     | contenedor Docker existente, **recreado** con `GATEWAY_URL=http://host.docker.internal:8888`, `ROADMAP_TECHNICAL_CLIENT_ID/SECRET` (de mentira), `SECTIONS_SYNC_ENABLED=true` | Override de compose en las notas de la sesión (`k07-env/roadmap-k07.yml`)                                                                                                                                                      |
| Motor `:8096`       | `mvn spring-boot:run`, perfil `dev`, base `challenge` creada en el Postgres de Roadmap, Kafka `localhost:29092`                                                               | `develop`. `main` (release 1.0.0) emite un formato camelCase que Roadmap y Accounting mandan a la DLT                                                                                                                          |
| Accounting `:8090`  | `mvn spring-boot:run`, contenedor MySQL `k07-accounting-mysql`, Kafka `localhost:29092`, `KAFKA_CONSUMERS_ENABLED=true`                                                       | `develop`                                                                                                                                                                                                                      |
| Gateway dev `:8888` | `k07-env/dev-gateway.mjs` (Node, ~100 líneas)                                                                                                                                 | Reemplazo del API gateway: tokens `client_credentials` falsos, encabezados de principal de servicio (`MS,<scope>`), JWKS y ruteo. **También simula el servicio Practical** (aprovisionamiento del intento, finalizado, estado) |
| Frontend `:4200`    | `ng serve --proxy-config <k07-env/proxy.k07.cjs>`                                                                                                                             | Agrega `/api/engine-challenge` y `/api/accounting`; la identidad de las llamadas a Roadmap se cambia por cookie                                                                                                                |

Simulado, no real: el servicio Practical (Tema 05), el recibo `PRACTICAL_CONTENT` del desafío semilla
(una fila insertada en la base del Motor), los eventos `ATTEMPT_FINALIZED` y `CHALLENGE_CORRECTED`
(publicados en `challenges.events` con el nombre de productor de Practical) y un evento
`STUDENT_ENROLLED` (Courses nunca lo emitió para la matrícula sembrada). El Motor, Roadmap y Accounting
son los servicios reales, con sus eventos de cierre reales. Cuenta del alumno: alumno de Courses
`7b1d6c1e-…a10`, cohorte `7926fe83-…` ("Programacion IV"), 3 vidas, máximo 3. Las vidas se dejaron en 0
con un `UPDATE` SQL en Accounting (preparación de datos, no una acción del producto).

## Plan de pruebas y resultados (segunda corrida)

Los valores son "antes → después". Toda la evidencia es una salida de `curl` o `psql` tomada el
2026-10-24; las capturas están en la carpeta de notas de la sesión (`k07-evidence/`).

| #     | Paso                                                                                                                                              | Esperado                                  | Observado                                                                                                                                                                                                                                                             | Resultado                                                    | Evidencia                                                                      |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| A     | Profesor: página del curso → unidad → Añadir contenido → Nodo guiado → Desafío práctico → desafío semilla → **Recuperación de vida** → Crear nodo | Nodo guardado con `RECOVERY`              | `node`: `QA K-07 Recuperación`, `PRACTICAL_CHALLENGE`, `lives_policy=RECOVERY`, `mandatory=t`, unidad 1, `sort_order=1`. Aparece listado en la unidad.                                                                                                                | OK                                                           | `06-…` + `select … from node`                                                  |
| A-ui  | La revisión del asistente antes de "Crear nodo"                                                                                                   | Muestra la política de vidas              | La revisión lista unidad, tipo, nombre, desafío, dificultad, obligatorio, ubicación y prerrequisitos. **No muestra la política de vidas elegida.**                                                                                                                    | FALLA (UX)                                                   | `07-…`                                                                         |
| B     | Mismo asistente, **Consume vida** (por defecto), "Desafío obligatorio" apagado                                                                    | Guardado como opcional                    | `QA K-07 Adicional`, `lives_policy=STANDARD`, `mandatory=f`, `sort_order=2`                                                                                                                                                                                           | OK                                                           | `08-…` + `select`                                                              |
| B-pre | La revisión decía "Sin prerrequisitos: se abre al entrar a la unidad"                                                                             | Sin prerrequisito                         | `node_prerequisite` tiene una fila: **Adicional requiere Recuperación** (el texto de ubicación "último de la unidad" sí decía "el nodo anterior queda como requisito"). La línea de la revisión contradice lo guardado.                                               | FALLA (UX), ver BUG-1                                        | `select … node_prerequisite`                                                   |
| C0    | Alumno con 3 vidas: elegibilidad y progreso                                                                                                       | ¿Nodo de recuperación utilizable?         | Recuperación: `eligible=false`, `reason=lives_available`, progreso `locked / lives_available`. Adicional: `eligible=true`, `enabled`. (El prerrequisito sobre Recuperación no se aplica al nodo opcional.)                                                            | OK según el diseño (RF-REC-04); el A5 del checklist está mal | `GET …/eligibility`, `GET …/progress`                                          |
| E1    | Adicional, intento 1, nota 20 (umbral 60)                                                                                                         | Desaprueba                                | Motor `COMPLETED`, cierre `DISAPPROVE`. Roadmap: XP 0 → 0, vidas 3 → 3, nodo `enabled`, historial `[(0, nota 20)]`, ranking XP 0                                                                                                                                      | OK (no pierde vida: `life_at_stake_policy = LAST_ATTEMPT`)   | `GET …/progress`, `xp-history`                                                 |
| E2    | Adicional, intento 2, nota 80                                                                                                                     | Aprueba                                   | Roadmap: **XP 0 → 250**, nodo `enabled → completed`, ranking `xp 0 → 250`, `completed_exercises 0 → 1`, vidas 3 → 3, historial `[(250, 80), (0, 20)]`. Accounting: `coins_ledgers` `CHALLENGE_CREDIT +50`, billetera 0 → 50.                                          | OK                                                           | `GET …/ranking`, `coins_ledgers`, `challenge_settlements` (`APPROVED`)         |
| E3    | Con 0 vidas: nodo adicional estándar (ya completado) y nodo de recuperación                                                                       | Estándar bloqueado, recuperación ofrecida | Adicional `eligible=false`, `reason=no_lives`. Recuperación `eligible=true`, `attempt_type=LIVES`, progreso `locked → enabled`.                                                                                                                                       | OK                                                           | `GET …/eligibility`, `progress`                                                |
| C     | Recuperación aprobada (nota 80), con 0 vidas                                                                                                      | Vidas 0 → 1, nodo completado              | Nodo `enabled → completed`, ranking `completed 1 → 2`, XP 250 → 250 (**por diseño 0 XP y 0 monedas**, `add_live=true` en el evento de cierre). **Las vidas siguen en 0**: Accounting mandó el evento a la DLT (`RETRIES_EXHAUSTED`, lectura de PAR-12 → Courses 503). | **FALLA / BLOQUEADO**, ver BUG-4                             | evento de cierre, `EVENT_SENT_TO_DLT`, `lives_ledgers` (solo `INITIAL_CREDIT`) |
| D     | Recuperación fallida (nota 20)                                                                                                                    | Sin cambio de vidas ni XP                 | No se completó: el segundo intento de recuperación quedó en `STARTED`; el consumidor del Motor entró en reintento ante su `ATTEMPT_FINALIZED` (BUG-5). No se cerró nada, así que no se observó nada.                                                                  | BLOQUEADO                                                    | volcado de hilos del Motor, `kafka-consumer-groups` (lag 3)                    |
| ST    | Racha después de una aprobación                                                                                                                   | La racha se actualiza                     | `current_streak` queda en 0 y `max_streak` en 0. `app.features.streak.enabled` es `false` por defecto (DEC-004). `daily_activity` sí registra `2026-10-24`.                                                                                                           | NO PROBABLE (flag apagado)                                   | fila de `daily_activity`                                                       |
| N     | Notificaciones                                                                                                                                    | Campana / aviso tras una aprobación       | `/api/notifications/*` → 404 (servicio no levantado)                                                                                                                                                                                                                  | BLOQUEADO                                                    | —                                                                              |
| UI    | Vista de alumno del mundo y del HUD                                                                                                               | Vidas, estrellas, estados de nodos        | El mapa 3D se renderiza ("Archipiélago Programacion IV", 2 islas), pero el panel de la unidad muestra `0/0 estrellas`: el usuario del mock logueado no es el alumno matriculado (BUG-6).                                                                              | BLOQUEADO                                                    | `09-…`, `10-…`                                                                 |

### Sección F del checklist, completada

| Verificación                                                           | Resultado                                                                                           |
| ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Nodo de recuperación guardado con `RECOVERY` y sobrevive a una recarga | **OK** (persistido en la base; no se repitió la recarga en la UI)                                   |
| Nodo opcional guardado como no obligatorio y sobrevive a una recarga   | **OK** (persistido)                                                                                 |
| Recuperación aprobada: +1 vida con tope en el máximo                   | **FALLA / BLOQUEADO** (BUG-4)                                                                       |
| Recuperación aprobada: se actualizan XP y ranking                      | Ranking y nodo **OK**; **el XP no sube, por diseño** (el checklist está mal)                        |
| Recuperación fallida: no pierde vida ni gana XP                        | **BLOQUEADO** (BUG-5)                                                                               |
| Desafío opcional: XP, vida en juego, reintento                         | **OK** (XP 250, la vida se mantiene; la vida solo está en juego en el último intento)               |
| Con 0 vidas: desafío estándar bloqueado con su explicación             | **OK a nivel API** (`no_lives`); no se vio el texto del mensaje en la UI (BUG-6)                    |
| Los movimientos de la billetera coinciden con los intentos             | **Parcial**: se vio `CHALLENGE_CREDIT +50` por la aprobación; no hubo movimiento de vidas por BUG-4 |

## Correcciones al checklist (el documento, no el producto)

1. **A5 / C0:** el nodo de recuperación _no_ está "disponible como cualquier otro". Se ofrece solo con 0
   vidas libres (`RF-REC-04`): con 3 vidas queda `locked / lives_available`.
2. **C3:** una recuperación aprobada da **+1 vida, 0 monedas y 0 XP** (`G09-HU26-DESAFIO-RECUPERACION.md`,
   `AttemptRewardRules`). El checklist decía que el XP sube.
3. **E2:** un intento fallido **no** cuesta una vida por defecto: el semilla usa
   `life_at_stake_policy = LAST_ATTEMPT`, así que la vida se pierde solo en el último intento permitido.
4. **A2 / "Política de vidas":** el control del asistente dice **Consume vida** y **Recuperación de vida**; "Común (exige vidas)" es la redacción de la ayuda del asistente y de las etiquetas del editor de nodos (dos nombres para la misma opción).

## Bugs y hallazgos

Dueños: BUG-1, BUG-2 y BUG-3 del frontend · BUG-4 de Courses / Accounting / Backoffice · BUG-5 del Motor ·
BUG-6 del entorno (mock de Users vs. semillas de Courses). Ninguno es un defecto de Roadmap. Ver "Quién es
dueño de qué".

### BUG-1 (UX): la revisión del asistente contradice el prerrequisito que guarda

- **Pasos:** unidad con un nodo → Nodo guiado → Desafío práctico → dejar la ubicación en "Último de la unidad (después de «QA K-07 Recuperación»)" → Prerrequisitos (sin tildar nada) → Revisión.
- **Esperado:** la revisión muestra el prerrequisito real.
- **Observado:** "Prerrequisitos: Sin prerrequisitos: se abre al entrar a la unidad". Después de "Crear nodo", `node_prerequisite` contiene `Adicional → Recuperación`. El paso de ubicación sí dice que el nodo anterior queda como requisito, pero la revisión no. Como el nodo anterior es un nodo de **recuperación** (se ofrece solo con 0 vidas), un prerrequisito lineal sobre él podría ocultar el nodo opcional a los alumnos; en esta corrida la puerta lo ignoró (`enabled`), así que el efecto real depende de las reglas de la puerta y no se probó más.

### BUG-2 (UX): la revisión no muestra la política de vidas

- **Pasos:** elegir "Recuperación de vida" en Detalle → Revisión.
- **Observado:** no hay una fila para la política de vidas, así que el profesor no puede confirmar un nodo de recuperación antes de guardarlo.

### BUG-3 (entorno de desarrollo): `proxy.conf.json` cierra la sesión sin Notifications

Igual que en la primera corrida: con `npm run start`, las llamadas sin autenticación a
`/api/notifications/*` reciben un 401 de `:8080` y la app vuelve a `/login`. `proxy.conf.cjs` lo evita.

### BUG-4 (bloqueante para el crédito de la recuperación): Accounting no puede leer PAR-12 sin Backoffice

- **Pasos:** un alumno con 0 vidas aprueba el nodo de recuperación. El Motor publica `CHALLENGE_COMPLETED` con `add_live=true`.
- **Esperado:** Accounting acredita una vida (`min(L+1, max)`).
- **Observado:** Accounting llama a `GET /api/course/course-cohorts/{id}/parameters/PAR-12`; Courses responde `503 "Course parameter defaults are not available"` (su caché de parámetros se llena desde Backoffice, que no está corriendo; `GET …/configuration` responde igual). Tras los reintentos, el evento va a `challenges.events.DLT` (`EVENT_SENT_TO_DLT … RETRIES_EXHAUSTED`) y **no se escribe ningún movimiento de vidas**. El alumno queda con 0 vidas y el nodo de recuperación completado.
- **Por qué importa:** en producción, una caída de Backoffice durante una aprobación de recuperación pierde el crédito de la vida (el evento va a la DLT, no se reintenta más adelante). No se verificó si existe un reproceso de la DLT.
- **Para destrabar la prueba:** Backoffice corriendo (o Courses reiniciado con filas en `course_parameter_default`), y repetir el paso C.

### BUG-5 (abierto): un evento que falla traba el consumidor del Motor

- **Pasos:** un segundo intento de recuperación sobre un nodo ya completado (`278ece73-…`), y luego `ATTEMPT_FINALIZED` (offset 20) y `CHALLENGE_CORRECTED` (offset 21).
- **Observado:** el intento queda en `STARTED`. El grupo de consumidores `engine-challenge-service` se queda en el offset 20 (lag 3, incluso después de reiniciar); un volcado de hilos muestra a `practical-content-0-C-1` dormido en `DefaultErrorHandler → FailedRecordTracker.recovered → DefaultBackOffHandler`, es decir, reintentando el mismo registro. El Motor no registra ninguna excepción con su nivel de log por defecto (un reinicio con DEBUG para el listener y `attempts` tampoco registró un stack trace). Todo evento posterior de la partición queda esperando detrás.
- **No establecido:** la excepción. Es candidato a un problema de bloqueo de cabecera de cola en el Motor, pero no se reprodujo de forma aislada.

### BUG-6 (entorno de desarrollo): ningún alumno del mock coincide con uno de Courses

Los alumnos del mock de Users (`alumno@…` = `…0004`) no están matriculados en ninguna cohorte de Courses; el alumno matriculado en Courses es `7b1d6c1e-…a10`, que no tiene login en el mock. Por eso la UI de alumno muestra un progreso vacío (`0/0 estrellas`) para el usuario del mock logueado, aunque la misma cohorte tiene datos para `7b1d6c1e-…`. Todas las verificaciones de alumno de esta corrida se hicieron contra las APIs con los encabezados de identidad de ese alumno.

### HALLAZGO-7 (positivo): la puerta y el cierre son consistentes de punta a punta

La elegibilidad, el progreso, el ranking, el historial de XP, el estado del nodo y la billetera se movieron juntos en los casos E1, E2, E3 y C (la parte de nodo y ranking). La puerta de Roadmap (`lives_available`, `no_lives`) coincidió con las vidas de Accounting en cada paso.

## Qué falta

1. Backoffice (o `course_parameter_default` sembrada en Courses) → repetir C y verificar `min(L+1, max)`, y luego D.
2. Encontrar la excepción detrás de BUG-5 (nivel de log del Motor, o reproducirla con un test unitario sobre `AttemptFactTransitions.applyFinalization`).
3. Un alumno del mock que coincida con el de Courses (o una matrícula en Courses para `…0004`) → repetir las verificaciones en la UI, incluido el texto "No tenés vidas disponibles".
4. `STREAK_ENABLED=true` en Roadmap para verificar la racha; Notifications para verificar la campana.
5. Las cuatro correcciones al checklist de arriba ya se aplicaron en `qa-recovery-additional-challenges.md`.

## Primera corrida (historia, stack incompleto)

Solo estaban corriendo Roadmap, Courses y el mock de Users. Resultados: el editor de nodos del curso
sembrado (cohorte `1111…`) fue denegado por Courses (la cohorte no existe allá); la cohorte `7926fe83…`
de Courses no tenía roadmap; el pool de desafíos devolvió `503 engine/catalog`; el progreso devolvió
`503 accounting/lives`; el ranking quedó `DEGRADED`. Esto llevó a la preparación de la segunda corrida
(ruteo a través de un gateway de desarrollo, sincronización de unidades con `SECTIONS_SYNC_ENABLED=true`
y creación del roadmap para `7926fe83…`).

## Evidencia (capturas)

Las capturas de la segunda corrida están en `tareas/K-07-evidencia/`. Las filas de la tabla las citan como `06-…`, `07-…`, etc.

| Captura | Qué muestra |
|---|---|
| `01-map-cohort-1111` | Mapa de la cohorte sembrada de Roadmap (`1111…`), con el nombre de la materia no disponible (primera corrida) |
| `02-editor-access-denied-cohort-1111` | El editor de nodos de esa cohorte lleva a "Acceso denegado" (primera corrida) |
| `03-map-cohort-7926-not-found` | Mapa de la cohorte de Courses `7926…` sin roadmap: "Asignatura no encontrada" (primera corrida) |
| `04-courses-general-7926-no-roadmap` | Página del curso: "esta sección todavía no es una unidad del roadmap" (primera corrida) |
| `05-wizard-sin-unidades` | El asistente de nodos dice "Sin unidades" (primera corrida) |
| `06-recovery-node-created` | El nodo de recuperación listado en la Unidad 1 (caso A) |
| `07-wizard-review-recovery-no-lives-policy` | Revisión del asistente: no muestra la política de vidas (BUG-2) |
| `08-wizard-review-additional` | Revisión del nodo adicional: "Sin prerrequisitos" y ubicación tras la recuperación (BUG-1) |
| `09-student-world-3d` | Mundo 3D del curso (UI de alumno) |
| `10-unit1-panel-0of0-stars` | Panel de la Unidad 1 con `0/0 estrellas` (BUG-6) |

![[K-07-evidencia/06-recovery-node-created.jpg]]

![[K-07-evidencia/07-wizard-review-recovery-no-lives-policy.jpg]]

![[K-07-evidencia/08-wizard-review-additional.jpg]]

![[K-07-evidencia/10-unit1-panel-0of0-stars.jpg]]
