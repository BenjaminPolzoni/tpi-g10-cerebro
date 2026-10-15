---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-30
estado: Propuesta
responsable: ""
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 34
prioridad: Must
prioridad_sprint: 1
en_taiga: false
---

# HT-30: Criterios pendientes de las HU del Sprint 1 y 2

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga. El 2026-10-15 junta en una sola HT lo que les falta a 10 HU que figuran Done en Taiga: HU-01, HU-15, HU-16, HU-20, HU-21, HU-41, HU-43, HU-44, HU-46 y HU-48 (34 puntos). Las HU originales quedan en Done en su sprint; cada tarea dice a qué HU y a qué CA corresponde.

> [!important] Prioridad 1 del sprint (2026-10-15)
> Va primero, junto con la otra prioridad 1: HT-26 (UI-KIT). Son criterios que ya se dieron por terminados y no se cumplen. Dentro de la HT, las tareas de **insignias** (HU-20 y HU-21, T-30.7 a T-30.11) van primero.

[G10] — HT-30 — Criterios pendientes de las HU del Sprint 1 y 2
---------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: cumplir los criterios de aceptación que quedaron sin cumplir en HU ya cerradas del Sprint 1 y 2
*   **Para**: que esas HU hagan lo que se dio por terminado, sin reabrirlas ni cambiar los sprints donde se cerraron

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Cada tarea lleva el código de la HU original y el CA que cierra. Al terminarla se deja un comentario en la HU original de Taiga. Se respetan las decisiones vigentes: gate fail-closed (DEC-003), baja lógica sin borrar progreso (DEC-005), insignias del sistema y del curso (DEC-006).
*   [ ] Validaciones: Cada CA cerrado tiene su test.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): El gate no supera el P95 de 200 ms (HU-15, HU-48).
*   [ ] Seguridad (roles, permisos, datos sensibles): El pre-chequeo de HU-48 usa el JWT del alumno y solo responde por él. Las acciones de profesor (HU-20, HU-41, HU-43) siguen exigiendo ser dueño del curso.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Los motivos del gate (`origen_no_disponible`, `group_restricted`) y los datos desactualizados se muestran en texto.
*   [ ] Otros: HU-46 ya no lleva el Templo (P13): se redefine su CA en Taiga.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1** (HU-01 CA8): Al recibir la baja de un desafío del Motor, el nodo queda «desafío no disponible», el profesor lo ve en el editor y el gate responde con un motivo claro, sin tocar el progreso.
*   [ ] **CA2** (HU-15 CA5): Con Accounting o Courses caídos y sin caché vigente, el gate responde `eligible=false` con `origen_no_disponible` (no 503), el front lo muestra y el acta del gate queda actualizada con G09.
*   [ ] **CA3** (HU-16 CA3): La pantalla de inventario muestra el último dato de vidas con aviso durante 24 h si Accounting no responde, y el gate nunca habilita con un dato `stale`.
*   [ ] **CA4** (HU-20): El profesor edita y da de baja insignias de su curso desde el front; las ya otorgadas se conservan y las del sistema no muestran esas acciones.
*   [ ] **CA5** (HU-21 CA1): `SECTION_NO_LIVES_LOST`, `NODE_NO_RETRIES` y `LIFE_RECOVERED` se otorgan una sola vez y publican `BADGE_AWARDED`.
*   [ ] **CA6** (HU-41 CA2): El nodo tiene reintentos validados contra PAR-13 y un PUT sin `lives_policy` no lo resetea a STANDARD.
*   [ ] **CA7** (HU-43): El ícono de desafío solo se acepta en nodos de desafío o examen; en `CONTENT` o `UNIT` devuelve 400.
*   [ ] **CA8** (HU-44 CA1 a CA4): El alumno con más de una comisión elige la comisión en el roadmap, ve lo habilitado para ella y el motivo `group_restricted` en texto, con `ROADMAP_BY_GROUP_ENABLED` encendido en la demo.
*   [ ] **CA9** (HU-46 CA3): El material desbloqueado se abre en un visor embebido, y el CA de HU-46 queda redefinido en Taiga sin el Templo.
*   [ ] **CA10** (HU-48 CA1 a CA3): El alumno consulta la elegibilidad con su JWT, recibe el mismo motivo que el gate y el front usa ese endpoint en vez del del Motor.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Criterios pendientes de HU cerradas

**Escenario 1** (HU-15)

*   **Dado**: Accounting caído y sin caché vigente
*   **Cuando**: el Motor consulta el gate por un alumno
*   **Entonces**: recibe `eligible=false` con `origen_no_disponible`, no un 503

**Escenario 2** (HU-48)

*   **Dado**: un alumno sin la lectura obligatoria de un nodo
*   **Cuando**: elige el desafío de ese nodo
*   **Entonces**: ve «contenido no leído» y no se llama al Motor

**Escenario 3** (HU-01)

*   **Dado**: un nodo con un desafío
*   **Cuando**: el Motor publica la baja de ese desafío, una o dos veces
*   **Entonces**: el nodo queda marcado como «desafío no disponible» una sola vez y el progreso no cambia

* * *

Prototipo
---------

*   **Capturas**: Editor de nodo (reintentos, ícono, desafío no disponible), catálogo de insignias, selector de comisión, inventario con dato desactualizado, visor de material.
*   **URL Figma**: Pendiente.
*   **Storybook**: Componentes del kit (`generic-select`, `generic-modal`, `generic-callout`).
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/nodes/{nodeId}/eligibility (alumno, HU-48).

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 34
*   **Prioridad (MoSCoW / Numérica)**: Must · 1 (máxima del sprint)

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 34 | Must · 1 (máxima del sprint) |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Motor (evento de baja de desafío, contrato del gate), Accounting (vidas, `LIVES_*`), Courses (comisiones, material), Backoffice (PAR-13), API Gateway (JWT del alumno).
*   Módulos afectados: Gate, listener de eventos del Motor, insignias, inventario, editor de nodo, roadmap del alumno, visor de material.
*   Otros equipos / aprobaciones: G09 (evento de baja y acta del gate), G01 (URLs del material).
*   Impacto en datos / migraciones: Columna de reintentos en el nodo (HU-41) y estado «desafío no disponible» del nodo (HU-01).
*   Riesgos y mitigación (opcional): Son 10 frentes chicos; mitigación: cada tarea se asigna y se cierra por separado, y se avisa en la HU original al terminar.

## Tareas

⭐ **HU-01 CA8: baja de desafío del Motor** ([us/76](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/76))
- [ ] **T-30.1 HU-01 CA8 · Marcar como «desafío no disponible» el nodo cuyo desafío da de baja el Motor** · Back
    - **Qué:** consumir el evento de baja de desafío del Motor (confirmar el nombre del evento con G09) y marcar como no disponibles los nodos que lo usan, igual que hoy hace el PATCH manual `/availability`. Sin tocar el progreso.
    - **Dónde:** `RoadmapEventListener` (topic de eventos de desafíos), `GraphService`.
    - **Listo cuando:** el evento repetido marca una sola vez, el gate da un motivo claro para ese nodo y hay tests.
- [ ] **T-30.2 HU-01 CA8 · Que el profesor vea qué nodos quedaron sin desafío** · Front
    - **Qué:** la lista de nodos del profesor ya muestra «No disponible»; verificar que se vea para estos nodos y que el editor deje elegir otro desafío para reemplazarlo.
    - **Dónde:** `roadmap-section-nodes`, `entity-editor-dialog`.
    - **Listo cuando:** el profesor identifica el nodo y lo puede arreglar sin ayuda.

**HU-15 CA5: motivo `origen_no_disponible`** ([us/741](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/741))
- [ ] **T-30.3 HU-15 CA5 · El gate responde `origen_no_disponible` en vez de 503** · Back
    - **Qué:** si Accounting o Courses no responden y no hay caché vigente, el gate responde `eligible=false` con `reason=origen_no_disponible` (fail-closed, DEC-003).
    - **Dónde:** `GateService`, `GateEvaluator`, `InventoryClient`, clientes de Courses.
    - **Listo cuando:** hay tests con Accounting caído y con Courses caído, y ninguno devuelve 503.
- [ ] **T-30.4 HU-15 CA5 · Acordar el cambio con el Motor y mostrar el motivo** · Coordinación + Front
    - **Qué:** pasar de 503 a 200 con motivo cambia el contrato: actualizar el acta del gate (`roadmap-motor-gate-v1.md`) con G09 antes de mergear. En el front, agregar el texto del motivo en `roadmapLabels.blockReason`.
    - **Listo cuando:** G09 aprobó el acta y el alumno ve el motivo en palabras.

**HU-16 CA3: último dato de vidas si Accounting cae** ([us/4237](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4237))
- [ ] **T-30.5 HU-16 CA3 · Mostrar el último dato de vidas con aviso durante 24 h** · Back + Front
    - **Qué:** la pantalla de inventario usa el último dato conocido marcado `stale` con una retención configurable de 24 h; pasado ese tiempo no se muestra. El front avisa que el dato está desactualizado.
    - **Dónde:** `InventoryService`, `InventoryController`, pantalla de inventario.
    - **Listo cuando:** con Accounting caído se ve el último dato con aviso, y a las 24 h deja de verse. Hay test.
- [ ] **T-30.6 HU-16 CA3 · El gate nunca habilita con un dato viejo** · Back
    - **Qué:** `GateService` ignora el dato `stale` de vidas y responde como en T-30.3.
    - **Listo cuando:** hay tests con caché vigente, vencida y sin caché.

⭐ **HU-20: editar y dar de baja insignias en el front** ([us/4243](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4243)) — insignias, prioridad 1
- [ ] **T-30.7 HU-20 · Editar las insignias del curso desde el front** · Front
    - **Qué:** acción «Editar» en las insignias del curso (nombre, descripción e ícono) usando la API de `BadgeCatalogController`. Las insignias del sistema no muestran la acción (DEC-006).
    - **Dónde:** `badges-catalog-page`.
    - **Listo cuando:** el profesor dueño edita una insignia y el cambio se ve al recargar. Hay test.
- [ ] **T-30.8 HU-20 · Dar de baja una insignia del curso** · Back + Front
    - **Qué:** baja lógica de una insignia del curso (DEC-005); si `BadgeCatalogController` no tiene el endpoint, crearlo. Las insignias ya otorgadas se siguen viendo; un profesor que no es dueño recibe 403.
    - **Listo cuando:** la insignia dada de baja no se puede otorgar más, la ya otorgada sigue en el perfil del alumno y hay tests.

⭐ **HU-21 CA1: tres criterios que nunca se otorgan** ([us/4244](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4244)) — insignias, prioridad 1
- [ ] **T-30.9 HU-21 CA1 · Otorgar la insignia «sección sin perder vidas» (`SECTION_NO_LIVES_LOST`)** · Back
    - **Qué:** al completar una sección, consultar las vidas perdidas del alumno en esa sección (`LostLivesClient` de Accounting) y otorgar la insignia una sola vez.
    - **Dónde:** `BadgeEvaluator`, `BadgeCriteriaChecks`.
    - **Listo cuando:** se otorga una vez, publica `BADGE_AWARDED` por el outbox y hay test.
- [ ] **T-30.10 HU-21 CA1 · Otorgar la insignia «nodo sin reintentos» (`NODE_NO_RETRIES`)** · Back
    - **Qué:** al cerrar un nodo aprobado en el primer intento (dato del evento de cierre del Motor), otorgar la insignia.
    - **Dónde:** `BadgeEvaluator`, `RoadmapEventListener`.
    - **Listo cuando:** se otorga solo si no hubo reintentos, una sola vez, con test.
- [ ] **T-30.11 HU-21 CA1 · Otorgar la insignia «recuperó una vida» (`LIFE_RECOVERED`)** · Back
    - **Qué:** consumir `LIVES_EXHAUSTED` / `LIVES_AVAILABLE` de Accounting (E8) y otorgar la insignia cuando el alumno recupera una vida.
    - **Dónde:** `AccountingEventsListener`, `BadgeEvaluator`.
    - **Listo cuando:** el evento repetido no duplica la insignia y hay test.

**HU-41 CA2: reintentos y política de vidas** ([us/4247](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4247))
- [ ] **T-30.12 HU-41 CA2 · Que guardar un nodo no le borre la política de vidas** · Back
    - **Qué:** hoy un PUT del nodo sin `lives_policy` lo vuelve a STANDARD. Si el campo no viene, se conserva el valor actual.
    - **Dónde:** `NodeController`, `GraphService`.
    - **Listo cuando:** editar el nombre de un nodo no cambia su política de vidas. Hay test.
- [ ] **T-30.13 HU-41 CA2 · Configurar los reintentos permitidos de cada nodo** · Back + Front
    - **Qué:** migración con `reintentos_permitidos` en el nodo, validado entre 0 y el tope de PAR-13 de Backoffice (falta definir de dónde sale PAR-13; ver `acuerdos/backoffice`). El gate lo usa en la siguiente consulta y el editor de nodo lo muestra y lo guarda.
    - **Listo cuando:** el profesor cambia los reintentos, el gate aplica el valor nuevo y hay tests.

**HU-43: ícono solo en desafíos y exámenes** ([us/4249](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4249))
- [ ] **T-30.14 HU-43 · Aceptar el ícono de desafío solo en desafíos y exámenes** · Back
    - **Qué:** en el PATCH del nodo, rechazar con 400 un `iconKey` de desafío en nodos `CONTENT` o `UNIT`.
    - **Dónde:** `NodeController`, `GraphService`.
    - **Listo cuando:** hay un test por tipo de nodo.

**HU-44: selector de comisión** ([us/5373](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5373))
- [ ] **T-30.15 HU-44 CA2 · Elegir la comisión en el roadmap del alumno** · Front
    - **Qué:** si el alumno está en más de una comisión, un `generic-select` para elegir cuál ver; usa la selección de comisión que ya existe en el back (`GroupSelectionService`).
    - **Listo cuando:** un alumno de 2W1 y 2W2 elige 2W2 y ve sus unidades con el mismo XP. Hay test.
- [ ] **T-30.16 HU-44 CA3 · Explicar con texto el bloqueo por comisión (`group_restricted`)** · Front
    - **Qué:** sumar el texto del motivo `group_restricted` en `roadmapLabels.blockReason`.
    - **Listo cuando:** el alumno ve por qué no puede entrar a un nodo de otra comisión.
- [ ] **T-30.17 HU-44 CA1, CA3 y CA4 · Encender el filtro por comisión en la demo y probarlo** · Infra
    - **Qué:** activar `ROADMAP_BY_GROUP_ENABLED` (`app.features.roadmap-by-group.enabled`) en el entorno de demo y probar los cuatro CA con un alumno en 2W1 y 2W2.
    - **Listo cuando:** los cuatro CA andan de punta a punta en la demo.

**HU-46 CA3: visor embebido** ([us/5375](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5375))
- [ ] **T-30.18 HU-46 CA3 · Abrir el material dentro de la página** · Front
    - **Qué:** hoy `material-access` abre la URL firmada en una pestaña nueva. Mostrar PDF y video en un visor dentro de la página (por ejemplo en un `generic-modal`), con la opción de abrir en pestaña nueva como respaldo.
    - **Listo cuando:** el alumno lee el material sin salir del roadmap. Hay test.
- [ ] **T-30.19 HU-46 CA1 · Redefinir el CA de HU-46 en Taiga sin el Templo** · Equipo
    - **Qué:** editar HU-46 (us/5375) en Taiga para sacar el CA1 del Templo, que no existe más (P13).
    - **Listo cuando:** la HU en Taiga ya no menciona el Templo.

**HU-48: pre-chequeo con el JWT del alumno** ([us/7206](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7206))
- [ ] **T-30.20 HU-48 CA1 · Endpoint para que el alumno pregunte si puede entrar a un desafío** · Back
    - **Qué:** `GET /api/roadmap/courses/{courseId}/nodes/{nodeId}/eligibility` con el JWT del alumno, que use el mismo `GateService` y vocabulario que el gate del Motor y no cree intentos. Hoy `/eligibility` está reservado a `ServiceIdentity` en `SecurityConfig` y al alumno le da 403. Borrar de paso `ProgressService.startChallenge` (código muerto) y actualizar OpenAPI.
    - **Listo cuando:** un alumno sin la lectura obligatoria recibe `content_not_read`. Hay BDD.
- [ ] **T-30.21 HU-48 CA1 · Que el front pregunte con el endpoint del alumno** · Front
    - **Qué:** `challenge-attempt.service` llama al endpoint nuevo, muestra el motivo si está bloqueado y, si está habilitado, abre el intento como hoy (con su `attempt_type`).
    - **Listo cuando:** se cumplen los CA1 a CA3 originales de HU-48 de punta a punta.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Verificado contra `origin/develop` (back `fc1917e`, front `67cbad4a`) el 2026-10-15. ❌ no cumple · ⚠️ hecho pero no anda de punta a punta.

| HU original | Sprint | CA que falta | Estado hoy |
|---|---|---|---|
| [[taiga/historias/HU-01 Crear nodos en el grafo (unidades, contenidos, desafíos, exámenes)\|HU-01]] | 1 | ❌ CA8: un desafío dado de baja deja el nodo no disponible | No hay consumidor del evento de baja; solo el PATCH manual `/availability` |
| [[taiga/historias/HU-15 Impedir la entrega en un nodo bloqueado (gate, vocabulario v3)\|HU-15]] | 1 | ❌ CA5: `origen_no_disponible` si un origen no responde | Devuelve 503 |
| [[taiga/historias/HU-16 Integración real con Inventario para las vidas del gate\|HU-16]] | 2 | ❌ CA3: último dato conocido si Accounting cae | `lastKnown` solo lo usa la pantalla de inventario |
| [[taiga/historias/HU-20 Definir el catálogo de insignias del curso\|HU-20]] | 2 | Sin CA pendiente: falta editar y dar de baja en el front | El front no lo permite |
| [[taiga/historias/HU-21 Otorgar insignias automáticamente\|HU-21]] | 2 | ❌ CA1: cumplir un criterio otorga la insignia | Tres criterios no tienen evaluador |
| [[taiga/historias/HU-41 Editar un nodo del roadmap de forma individual\|HU-41]] | 2 | ❌ CA2: reintentos y reglas nuevas en la próxima consulta | No hay campo de reintentos; un PUT sin `lives_policy` vuelve a STANDARD |
| [[taiga/historias/HU-43 Elegir el ícono de un desafío\|HU-43]] | 2 | Sin CA pendiente: validar el ícono por tipo de nodo | El back acepta el ícono en cualquier tipo |
| [[taiga/historias/HU-44 Ver el roadmap de cada una de mis comisiones\|HU-44]] | 2 | ❌ CA2 y ⚠️ CA1, CA3, CA4 | No hay selector en el front; lo demás depende de `ROADMAP_BY_GROUP_ENABLED`, que está en false |
| [[taiga/historias/HU-46 Ver en los nodos y en el Templo el material teórico de Courses\|HU-46]] | 2 | ❌ CA1 (Templo, descartado por P13) y ❌ CA3: visor embebido | El material se abre en una pestaña nueva |
| [[taiga/historias/HU-48 Saber si puedo entrar a un desafío antes de abrirlo\|HU-48]] | 2 | ❌ CA1 y ⚠️ CA2, CA3 | `/eligibility` está reservada a `ServiceIdentity`: con el JWT del alumno da 403 |

### Depende de

Nada: se puede empezar ya.

### Deuda técnica que cierra

- [[deuda-tecnica|DT-04]]

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|G8]] `node_id` único global (HU-01).
- ✅ [[sprints/sprint-3/08-dudas|E9]] Con Backoffice caído se usan los valores en caché (HU-15).
- ✅ [[sprints/sprint-3/08-dudas|E2]] Los tres criterios de insignia se implementan (HU-21).
- ✅ [[sprints/sprint-3/08-dudas|E8]] Hay que consumir `LIVES_EXHAUSTED` / `LIVES_AVAILABLE` (HU-21).
- ✅ [[sprints/sprint-3/08-dudas|P5]] El profesor configura si un roadmap va por comisión (HU-44).
- ✅ [[sprints/sprint-3/08-dudas|P13]] El Templo no existe más (HU-46).
