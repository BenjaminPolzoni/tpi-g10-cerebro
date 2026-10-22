---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-32
estado: New
responsable: "Sin asignar"
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Must
prioridad_sprint: 1
en_taiga: true
ref: 9271
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9271
responsables_tareas: ["Gabriela Camacho", "Lorenzo Araujo", "Iker Alonso", "Lautaro Jesus Diego", "Ludmila Mailen Cejas", "Quinteros Tomás"]
tareas_cerradas: "0/6"
---

# HT-32: Nodos y editor pendientes de HU-01, HU-41 y HU-43

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **0/6** · Sprint: **G10 - Sprint 3**
> Cargada en Taiga: [[taiga/historias/HT-32 Nodos y editor pendientes de HU-01, HU-41 y HU-43|HT-32]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9271)) · Épica en Taiga: [[epicas/EP-8632 Deuda del Sprint 2|EP-8632]] · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Gabriela Camacho|Gabriela Camacho]] (1), [[sprints/sprint-3/12-responsables#Lorenzo Araujo|Lorenzo Araujo]] (1), [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]] (1), [[sprints/sprint-3/12-responsables#Lautaro Jesus Diego|Lautaro Jesus Diego]] (1), [[sprints/sprint-3/12-responsables#Ludmila Mailen Cejas|Ludmila Mailen Cejas]] (1), [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]] (1). Sale de dividir por tema la HT de criterios pendientes (2026-10-15): ver [[sprints/sprint-3/historias/HT-30 Insignias pendientes de HU-20 y HU-21|HT-30]]. Las HU originales quedan en Done en su sprint; cada tarea dice a qué HU y a qué CA corresponde.

> [!important] Prioridad 1 del sprint (2026-10-15)
> Va después de las insignias (HT-30). Son criterios que ya se dieron por terminados y no se cumplen.

[G10] — HT-32 — Nodos y editor pendientes de HU-01, HU-41 y HU-43
-----------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: que un nodo quede «desafío no disponible» cuando el Motor da de baja su desafío, que editar un nodo no le borre la política de vidas y que el ícono de desafío solo se acepte donde corresponde
*   **Para**: cumplir lo que les falta a HU-01, HU-41 y HU-43 sin reabrirlas

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Cada tarea lleva el código de la HU original y el CA que cierra; al terminarla se deja un comentario en la HU original de Taiga. La baja de un desafío no toca el progreso del alumno (DEC-005).
*   [ ] Validaciones: Reintentos entre 0 y el tope de PAR-13. Ícono de desafío solo en nodos de desafío o examen.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): Editar nodos: ADMIN, GESTOR o PROFESSOR dueño del curso.
*   [ ] Accesibilidad (WCAG/teclado/lectores): «Desafío no disponible» se muestra en texto.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1** (HU-01 CA8): Al recibir la baja de un desafío del Motor, el nodo queda «desafío no disponible», el profesor lo ve en el editor y el gate responde con un motivo claro, sin tocar el progreso.
*   [ ] **CA2** (HU-41 CA2): El nodo tiene reintentos validados contra PAR-13 y un PUT sin `lives_policy` no lo resetea a STANDARD.
*   [ ] **CA3** (HU-43): El ícono de desafío solo se acepta en nodos de desafío o examen; en `CONTENT` o `UNIT` devuelve 400.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Nodos y editor

**Escenario 1** (HU-01)

*   **Dado**: un nodo con un desafío
*   **Cuando**: el Motor publica la baja de ese desafío, una o dos veces
*   **Entonces**: el nodo queda marcado como «desafío no disponible» una sola vez y el progreso no cambia

**Escenario 2** (HU-41)

*   **Dado**: un nodo con política de vidas distinta de STANDARD
*   **Cuando**: el profesor le cambia solo el nombre
*   **Entonces**: la política de vidas no cambia

**Escenario 3** (HU-43)

*   **Dado**: un nodo `CONTENT`
*   **Cuando**: el profesor le pone un ícono de desafío
*   **Entonces**: recibe 400

* * *

Prototipo
---------

*   **Capturas**: Editor de nodo (reintentos, ícono, desafío no disponible).
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-input`, `generic-select`.
*   **Mock API / Swagger**: PATCH /api/roadmap/nodes/{nodeId} con `reintentos_permitidos`.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Must · 1 (máxima del sprint)

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 8 | Must · 1 (máxima del sprint) |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Motor (evento de baja de desafío), Backoffice (PAR-13).
*   Módulos afectados: `RoadmapEventListener`, `GraphService`, `NodeController`, `roadmap-section-nodes`, `entity-editor-dialog`.
*   Otros equipos / aprobaciones: G09 (nombre del evento de baja).
*   Impacto en datos / migraciones: Columna de reintentos en el nodo (HU-41) y estado «desafío no disponible» del nodo (HU-01).
*   Riesgos y mitigación (opcional): Que no esté definido de dónde sale PAR-13; mitigación: usar el tope en caché de Backoffice y anotarlo en `acuerdos/backoffice`.

## Tareas

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **0/6**. Historia en Taiga: [[taiga/historias/HT-32 Nodos y editor pendientes de HU-01, HU-41 y HU-43|HT-32]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9271)

- [ ] [#9293](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9293) **T-32.1 HU-01 CA8 · Marcar como «desafío no disponible» el nodo cuyo desafío da de baja el Motor** · Back · New · [[sprints/sprint-3/12-responsables#Gabriela Camacho|Gabriela Camacho]]
    - **Qué:** consumir el evento de baja de desafío del Motor (confirmar el nombre del evento con G09) y marcar como no disponibles los nodos que lo usan, igual que hoy hace el PATCH manual `/availability`. Sin tocar el progreso.
    - **Dónde:** `RoadmapEventListener` (topic de eventos de desafíos), `GraphService`.
    - **Listo cuando:** el evento repetido marca una sola vez, el gate da un motivo claro para ese nodo y hay tests.
- [ ] [#9294](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9294) **T-32.2 HU-01 CA8 · Que el profesor vea qué nodos quedaron sin desafío** · Front · New · [[sprints/sprint-3/12-responsables#Lorenzo Araujo|Lorenzo Araujo]]
    - **Qué:** la lista de nodos del profesor ya muestra «No disponible»; verificar que se vea para estos nodos y que el editor deje elegir otro desafío para reemplazarlo.
    - **Dónde:** `roadmap-section-nodes`, `entity-editor-dialog`.
    - **Listo cuando:** el profesor identifica el nodo y lo puede arreglar sin ayuda.
**HU-41 CA2: reintentos y política de vidas** ([us/4247](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4247))
- [x] [#9295](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9295) **T-32.3 HU-41 CA2 · Que guardar un nodo no le borre la política de vidas** · Back · Hecha (#297, mergeada el 21/10; falta cerrar en Taiga) · [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]]
    - **Qué:** hoy un PUT del nodo sin `lives_policy` lo vuelve a STANDARD. Si el campo no viene, se conserva el valor actual.
    - **Dónde:** `NodeController`, `GraphService`.
    - **Listo cuando:** editar el nombre de un nodo no cambia su política de vidas. Hay test.
- [ ] [#9296](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9296) **T-32.4 HU-41 CA2 · Configurar los reintentos permitidos de cada nodo** · Back + Front · New · [[sprints/sprint-3/12-responsables#Lautaro Jesus Diego|Lautaro Jesus Diego]]
    - **Qué:** migración con `reintentos_permitidos` en el nodo, validado entre 0 y el tope de PAR-13 de Backoffice (falta definir de dónde sale PAR-13; ver `acuerdos/backoffice`). El gate lo usa en la siguiente consulta y el editor de nodo lo muestra y lo guarda.
    - **Listo cuando:** el profesor cambia los reintentos, el gate aplica el valor nuevo y hay tests.
**HU-43: ícono solo en desafíos y exámenes** ([us/4249](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4249))
- [ ] [#9297](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9297) **T-32.5 HU-43 · Aceptar el ícono de desafío solo en desafíos y exámenes** · Back · New · [[sprints/sprint-3/12-responsables#Ludmila Mailen Cejas|Ludmila Mailen Cejas]]
    - **Qué:** en el PATCH del nodo, rechazar con 400 un `iconKey` de desafío en nodos `CONTENT` o `UNIT`.
    - **Dónde:** `NodeController`, `GraphService`.
    - **Listo cuando:** hay un test por tipo de nodo.
- [ ] [#9343](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9343) **T-32.6 Wiki, OpenAPI y diagrama de secuencia** · New · [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]]
    - Tarea de documentación agregada en Taiga por el equipo; no estaba en la propuesta.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Verificado contra `origin/develop` (back `fc1917e`, front `67cbad4a`) el 2026-10-15.

| HU original | Sprint | CA que falta | Estado hoy |
|---|---|---|---|
| [[taiga/historias/HU-01 Crear nodos en el grafo (unidades, contenidos, desafíos, exámenes)\|HU-01]] | 1 | ❌ CA8: un desafío dado de baja deja el nodo no disponible | No hay consumidor del evento de baja; solo el PATCH manual `/availability` |
| [[taiga/historias/HU-41 Editar un nodo del roadmap de forma individual\|HU-41]] | 2 | ❌ CA2: reintentos y reglas nuevas en la próxima consulta | No hay campo de reintentos; un PUT sin `lives_policy` vuelve a STANDARD |
| [[taiga/historias/HU-43 Elegir el ícono de un desafío\|HU-43]] | 2 | Sin CA pendiente: validar el ícono por tipo de nodo | El back acepta el ícono en cualquier tipo |

### Depende de

Nada: se puede empezar ya. Si HT-18 ya pasó la lectura a Neo4j, los cambios del nodo van en el módulo `graph`.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|G8]] `node_id` único global (HU-01).
