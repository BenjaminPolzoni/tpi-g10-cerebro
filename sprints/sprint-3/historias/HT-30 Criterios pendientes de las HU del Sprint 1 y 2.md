---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-30
estado: Propuesta
responsable: ""
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 34
prioridad: Must
en_taiga: false
---

# HT-30: Criterios pendientes de las HU del Sprint 1 y 2

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga. El 2026-10-15 junta en una sola HT lo que les falta a 10 HU que figuran Done en Taiga: HU-01, HU-15, HU-16, HU-20, HU-21, HU-41, HU-43, HU-44, HU-46 y HU-48 (34 puntos). Las HU originales quedan en Done en su sprint; cada tarea dice a qué HU y a qué CA corresponde.

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
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 34 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Motor (evento de baja de desafío, contrato del gate), Accounting (vidas, `LIVES_*`), Courses (comisiones, material), Backoffice (PAR-13), API Gateway (JWT del alumno).
*   Módulos afectados: Gate, listener de eventos del Motor, insignias, inventario, editor de nodo, roadmap del alumno, visor de material.
*   Otros equipos / aprobaciones: G09 (evento de baja y acta del gate), G01 (URLs del material).
*   Impacto en datos / migraciones: Columna de reintentos en el nodo (HU-41) y estado «desafío no disponible» del nodo (HU-01).
*   Riesgos y mitigación (opcional): Son 10 frentes chicos; mitigación: cada tarea se asigna y se cierra por separado, y se avisa en la HU original al terminar.

## Tareas

**HU-01 CA8: baja de desafío del Motor** ([us/76](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/76))
- [ ] T-30.1 HU-01 CA8: consumir el evento de baja de desafío del Motor (idempotente)
- [ ] T-30.2 HU-01 CA8: marca «desafío no disponible» en el nodo, el editor y el gate
- [ ] T-30.3 HU-01 CA8: tests con el evento repetido

**HU-15 CA5: motivo `origen_no_disponible`** ([us/741](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/741))
- [ ] T-30.4 HU-15 CA5: motivo `origen_no_disponible` en el gate en vez de 503
- [ ] T-30.5 HU-15 CA5: tests con Accounting y Courses caídos
- [ ] T-30.6 HU-15 CA5: actualizar el acta del gate con G09 y el texto en el front

**HU-16 CA3: último dato de vidas si Accounting cae** ([us/4237](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4237))
- [ ] T-30.7 HU-16 CA3: retención de 24 h del último dato en la pantalla de inventario
- [ ] T-30.8 HU-16 CA3: el gate ignora los datos `stale`
- [ ] T-30.9 HU-16 CA3: tests de caché vigente, vencida y sin caché

**HU-20: editar y dar de baja insignias en el front** ([us/4243](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4243))
- [ ] T-30.10 HU-20: front de edición de insignias del curso
- [ ] T-30.11 HU-20: front de baja lógica de insignias (y endpoint si no existe)
- [ ] T-30.12 HU-20: tests

**HU-21 CA1: tres criterios que nunca se otorgan** ([us/4244](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4244))
- [ ] T-30.13 HU-21 CA1: evaluador de `SECTION_NO_LIVES_LOST`
- [ ] T-30.14 HU-21 CA1: evaluador de `NODE_NO_RETRIES`
- [ ] T-30.15 HU-21 CA1: evaluador de `LIFE_RECOVERED`, consumiendo `LIVES_EXHAUSTED` / `LIVES_AVAILABLE` de Accounting (E8)
- [ ] T-30.16 HU-21 CA1: tests (una sola vez y `BADGE_AWARDED`)

**HU-41 CA2: reintentos y política de vidas** ([us/4247](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4247))
- [ ] T-30.17 HU-41 CA2: columna de reintentos validada contra PAR-13
- [ ] T-30.18 HU-41 CA2: corregir el PUT que resetea `lives_policy`
- [ ] T-30.19 HU-41 CA2: reintentos en el editor de nodo y tests

**HU-43: ícono solo en desafíos y exámenes** ([us/4249](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4249))
- [ ] T-30.20 HU-43: validar el ícono según el tipo de nodo, con un test por tipo

**HU-44 CA1 a CA4: selector de comisión** ([us/5373](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5373))
- [ ] T-30.21 HU-44 CA2: selector de comisión en el roadmap del alumno
- [ ] T-30.22 HU-44 CA3: texto para `group_restricted`
- [ ] T-30.23 HU-44 CA1, CA3 y CA4: encender `ROADMAP_BY_GROUP_ENABLED` en la demo y probar de punta a punta

**HU-46 CA3: visor embebido** ([us/5375](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5375))
- [ ] T-30.24 HU-46 CA3: abrir el material desbloqueado en un visor embebido
- [ ] T-30.25 HU-46 CA1: redefinir el CA en Taiga sin el Templo (P13)

**HU-48 CA1 a CA3: pre-chequeo con el JWT del alumno** ([us/7206](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7206))
- [ ] T-30.26 HU-48 CA1: endpoint de elegibilidad para el alumno sobre `GateService`
- [ ] T-30.27 HU-48 CA1: el front usa el endpoint del alumno
- [ ] T-30.28 HU-48: borrar `ProgressService.startChallenge`, BDD y OpenAPI

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
