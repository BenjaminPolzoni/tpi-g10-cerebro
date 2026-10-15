---
tags: [tpi, g10, sprint-3, taiga, neo4j, grafo]
fecha: 2026-10-15
estado: propuesta
autor: Iker Alonso
---

# 10 — Tareas que faltan para cerrar el grafo (Neo4j + vista)

> [!info] Para quién es
> Para quienes cargan el Sprint 3 en Taiga. Sale de cruzar las tareas del Excel `Capacidad.xlsx` (hoja Tareas, reparto del 15/10) con [[sprints/sprint-3/historias/HT-16 Validar la infra de Neo4j y modelar las relaciones|HT-16]], [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial|HT-18]], [[sprints/sprint-3/historias/HU-65 Relaciones con tipo|HU-65]], [[sprints/sprint-3/historias/HU-62 Vista de grafo cómoda para el profesor|HU-62]], [[sprints/sprint-3/historias/HT-34 Componente de grafo en la UI-KIT|HT-34]], [[decisiones/DEC-016-neo4j-para-la-estructura-del-roadmap|DEC-016]] y [[decisiones/DEC-018-catalogo-de-relaciones-y-tipos-de-nodo|DEC-018]].
>
> No hay historias nuevas: todo entra como **tareas nuevas dentro de historias que ya existen**, más algunos **ajustes de criterio** y **cambios de responsable**. Los responsables marcados "a confirmar" todavía no aceptaron.

El plan de ejecución de estas tareas está en [[sprints/sprint-3/11-plan-ejecucion-grafo|11-plan-ejecucion-grafo]].

## Resumen

| Tipo | Cantidad | Horas |
|---|---|---|
| Tareas nuevas | 8 | 23 h |
| Ajustes de criterio en tareas existentes | 9 | 0 h (cambian el "listo cuando", no el tamaño), salvo T-18.6, que baja 2 h |
| Cambios de responsable | 4 historias o tareas | — |

## 1. Tareas nuevas

Mismo formato que la hoja Tareas del Excel. Observadores = revisores de cada responsable según la hoja Reparto.

### HT-18 · Módulo graph en Neo4j y migración inicial

#### T-18.9 Modelo común de la estructura y lector/escritor por base
- **Rol:** Backend · **Hs:** 4 · **Responsable:** Alonso Iker Guillermo · **Observadores:** Baltasar Rodriguez Teruel; Fenoglio Santino
- **Qué:** un modelo en memoria de la estructura de un roadmap (`RoadmapStructure`: secciones, subsecciones, nodos, relaciones con tipo y árbol de reglas) y dos puertos, `StructureReader` y `StructureWriter`, con una implementación sobre Postgres (la de hoy) y otra sobre Neo4j. El flag de T-18.6 elige cuál se usa.
- **Por qué hace falta:** HU-58, HU-59, HU-64, HU-71 y HT-19 dicen trabajar "en el módulo graph", pero ese módulo recién existe a mitad de sprint. Si cada historia programa contra las tablas de JPA, al pasar la lectura a Neo4j (T-18.6) hay que reescribirlas. Con esta tarea hecha en la primera semana, los validadores de ciclos (T-58.2, T-59.1), de inicio, fin y camino (T-64.2) y el clonado (T-71.1) trabajan sobre el modelo común y no dependen de la base.
- **Dónde:** `tpi-roadmap`, paquete `graph`.
- **Listo cuando:** la implementación de Postgres está mergeada en la primera semana y devuelve la misma estructura que hoy arma `GraphService`, con tests. La implementación de Neo4j pasa los mismos tests con Testcontainers.

#### T-18.10 Escenarios BDD de la estructura en Neo4j
- **Rol:** Backend · **Hs:** 3 · **Responsable:** Alonso Iker Guillermo · **Observadores:** Baltasar Rodriguez Teruel; Fenoglio Santino
- **Qué:** pasar a Cucumber los 4 escenarios que ya están escritos en HT-18 (migración, migración repetida sin duplicar, `GET /roadmaps/{id}/graph` y regla editada con el flag encendido), con el mismo formato que los `.feature` de `src/test/resources/features/`.
- **Por qué hace falta:** HT-18 trae BDD escrito pero, a diferencia de HT-20 (T-20.3), no tiene tarea que lo implemente.
- **Listo cuando:** los escenarios pasan en la suite local (`./mvnw verify`).

#### T-18.11 Sumar al catálogo los tipos de nodo de DEC-018 que faltan
- **Rol:** Backend · **Hs:** 3 · **Responsable:** Stefano Zoffoli (a confirmar) · **Observadores:** Alonso Iker Guillermo; Delgado Costa Mateo
- **Qué:** DEC-018 define desafío teórico, práctico, **de IA** y **de recuperación de vida**, examen, contenido, inicio y fin. Hoy `NodeType` tiene `UNIT`, `CONTENT`, `THEORETICAL_CHALLENGE`, `PRACTICAL_CHALLENGE` y `EXAM`. T-64.1 suma `START` y `END`, pero **ninguna tarea suma el desafío de IA ni el de recuperación de vida**. Hay que agregarlos al enum, a `isChallenge()`, al gate y al editor, y acordar con el Motor (G09) cómo se identifican esos desafíos en su catálogo.
- **Por qué este responsable:** Stefano ya toca `NodeType` en T-64.1 y tiene margen (12 h).
- **Listo cuando:** se puede crear un nodo de cada tipo de DEC-018, el gate trata a los dos nuevos como desafíos y el acuerdo con G09 queda en `acuerdos/motor-desafios-g09`. Hay tests.

### HU-65 · Relaciones con tipo

#### T-65.5 Endpoints para crear y borrar relaciones con tipo
- **Rol:** Backend · **Hs:** 4 · **Responsable:** Alonso Iker Guillermo · **Observadores:** Baltasar Rodriguez Teruel; Fenoglio Santino
- **Qué:** `POST /roadmaps/{roadmapId}/relations` (origen, destino, tipo y `label` opcional) y `DELETE /roadmaps/{roadmapId}/relations/{relationId}` (baja lógica). Valida que el tipo esté en el catálogo de T-65.1, que origen y destino sean del mismo roadmap y que un `REQUIRES` no arme un ciclo. La condición de un `REQUIRES` (AND/OR, XP mínimo) se sigue editando con las reglas de HU-58/HU-59. Documentado en OpenAPI.
- **Por qué hace falta:** T-65.1 define el catálogo y T-62.3/T-65.3 crean y borran relaciones desde el front, pero ninguna tarea expone el endpoint que las guarda.
- **Listo cuando:** se crea y se borra una relación de cada tipo, y un tipo desconocido, un ciclo o una relación entre roadmaps distintos devuelven 400. Hay tests del contrato.

#### T-65.6 Ocultar tipos de relación por roadmap y filtrarlos para el alumno
- **Rol:** Backend · **Hs:** 3 · **Responsable:** Delgado Costa Mateo (a confirmar) · **Observadores:** Alonso Iker Guillermo; Cejas, Ludmila Mailen
- **Qué:** guardar por roadmap qué tipos de relación están ocultos y que `GET /roadmaps/{id}/graph` no devuelva esas aristas cuando lo pide un alumno (el profesor las sigue recibiendo, marcadas `visible: false`).
- **Por qué hace falta:** T-65.2 hace el control en el front, pero si el filtro es solo visual, el alumno recibe igual las aristas ocultas en la respuesta. HU-65 CA3 pide que dejen de verse en el mapa del alumno.
- **Por qué este responsable:** Mateo hace la mitad de front (T-65.2) y tiene margen (7,8 h). Si no puede, la toma Iker.
- **Listo cuando:** con `BELONGS_TO` oculto, un alumno no recibe esas aristas y el profesor sí. Hay tests.

### HT-16 · Validar la infra de Neo4j y modelar las relaciones

#### T-16.5 Wiki, OpenAPI y diagrama de secuencia
- **Rol:** Documentación · **Hs:** 2 · **Responsable:** Quinteros, Tomás (a confirmar) · **Observadores:** Alonso Iker Guillermo
- **Qué:** documentar HT-16 en la Wiki: cómo se levanta Neo4j, el modelo del grafo (T-16.4) y qué queda en Postgres, según la guía de la Wiki.
- **Por qué hace falta:** es la única HT del sprint, junto con HT-34, sin tarea de Wiki.
- **Listo cuando:** lo aprueba un revisor y coincide con lo implementado.

### HT-34 · Componente de grafo en la UI-KIT

#### T-34.3 Wiki y documentación del componente
- **Rol:** Documentación · **Hs:** 2 · **Responsable:** Quinteros, Tomás (a confirmar) · **Observadores:** Alonso Iker Guillermo
- **Qué:** documentar en la Wiki cómo se usa `generic-node-graph` (entradas, salidas, teclado y accesibilidad) con capturas de Storybook.
- **Listo cuando:** lo aprueba un revisor y coincide con la versión publicada del kit.

### HU-62 · Vista de grafo cómoda para el profesor

#### T-62.7 Guardar posiciones en el módulo graph (mitad back de T-62.2)
- **Rol:** Backend · **Hs:** 2 · **Responsable:** Alonso Iker Guillermo (a confirmar con Mateo) · **Observadores:** Delgado Costa Mateo
- **Qué:** `PUT /roadmaps/{roadmapId}/layout` con las posiciones `{nodeId, x, y}` de varios nodos a la vez, guardadas en Neo4j. T-62.2 queda solo con el front (`moveNode` del store) y baja a 2 h.
- **Por qué:** T-62.2 está marcada "Back + Front", y las posiciones viven en el módulo graph (diseño de [[sprints/sprint-3/04-base-de-grafos|04-base-de-grafos]]).
- **Listo cuando:** se guardan las posiciones, `GET /graph` las devuelve en `layout` y hay test del contrato.

## 2. Ajustes de criterio en tareas existentes

| Tarea | Responsable | Qué se agrega al "listo cuando" | Por qué |
|---|---|---|---|
| **T-18.6** Pasar la lectura a Neo4j | Iker | El flag es **de una sola vía** en este sprint: apagarlo después de editar en Neo4j deja Postgres desactualizado. Queda documentado y la demo no lo apaga. **Baja de 4 h a 2 h**, porque la abstracción la hace T-18.9 | Hoy dice "con el flag apagado todo sigue en Postgres", pero no dice qué pasa si se apaga después de editar |
| **T-16.2** Neo4j en la plataforma | Stefano (a confirmar) | El health de Neo4j aparece en `/actuator/health` de roadmap-service | Si Neo4j se cae, la mesh tiene que verlo |
| **T-34.2** Construir y publicar el componente | Iker | Hay una historia de Storybook con 150 nodos y se mueve fluido | HT-34 y T-62.1 piden fluidez con 150 nodos y nadie lo prueba en el kit |
| **T-21.2** Seed de la demo | Benjamin | Si la demo corre con el flag encendido, el seed escribe en Neo4j o corre el job de T-18.2 después | Si no, la demo arranca con Neo4j vacío |
| **T-19.3** Sync de secciones por roadmap | Baltasar | El sync escribe con `StructureWriter` (T-18.9), no directo en las tablas | Con el flag encendido, el sync tiene que escribir en Neo4j |
| **T-19.4** Roadmap correcto en eventos del Motor | Baltasar | Busca el nodo con `StructureReader` (T-18.9) | Ídem, para la lectura |
| **T-58.1, T-58.2, T-59.1** Reglas y ciclos | Santino | Las reglas se guardan con `StructureWriter` y los ciclos se validan sobre `RoadmapStructure` | Para que funcionen con las dos bases |
| **T-64.1 a T-64.3** Inicio y fin | Stefano | `GraphValidator` trabaja sobre `RoadmapStructure`. La migración de T-64.3 corre **antes** de la corrida final del job de T-18.2 | Si no, Neo4j queda sin inicio ni fin |
| **T-71.1** Clonar un roadmap | Baltasar | Copia el subgrafo con `StructureWriter` | Para clonar en la base que mande |

## 3. Cambios de responsable

| Historia / tarea | Hs | De | A | Estado |
|---|---|---|---|---|
| **HT-34** (T-34.1 y T-34.2) | 12 | Cejas, Ludmila Mailen | Alonso Iker Guillermo | ✅ Acordado con Ludmila |
| **T-16.2** Neo4j en la plataforma y la demo | 4 | Alonso Iker Guillermo | Stefano Zoffoli | A confirmar |
| **T-32.3** Que guardar un nodo no borre la política de vidas | 2 | Alonso Iker Guillermo | Cejas, Ludmila Mailen | A confirmar |
| **T-62.2** Guardar posiciones | 4 → 2 | Delgado Costa Mateo | Mateo (front) + Iker (back, T-62.7) | A confirmar con Mateo |

## 4. Cómo queda la carga

Horas asignadas sobre la capacidad ajustada de la hoja Capacidad.

| Integrante | Antes | Cambio | Después | Ajustada | Uso |
|---|---|---|---|---|---|
| Alonso Iker Guillermo | 50 | −4 (T-16.2) −2 (T-32.3) −2 (T-18.6) +12 (HT-34) +4 (T-18.9) +3 (T-18.10) +4 (T-65.5) +2 (T-62.7) | **67** | 44,2 | 152 % |
| Cejas, Ludmila Mailen | 52 | −12 (HT-34) +2 (T-32.3) | 42 | 43,2 | 97 % |
| Stefano Zoffoli | 20 | +4 (T-16.2) +3 (T-18.11) | 27 | 32 | 84 % |
| Delgado Costa Mateo | 50 | +3 (T-65.6) −2 (T-62.2) | 51 | 57,8 | 88 % |
| Quinteros, Tomás | 31 | +2 (T-16.5) +2 (T-34.3) | 35 | 34 | 103 % |

> [!warning] Iker queda muy por encima de su capacidad
> Es una decisión personal de Iker tomar ese volumen. Si a mitad de sprint (día 7) va atrasado, estas tareas se pueden pasar sin romper el orden, en este orden de prioridad:
> 1. **T-18.3** (reconciliación, 5 h) → Stefano.
> 2. **T-18.4** (caché del gate, 4 h) → Fenoglio Santino, que ya mide esa caché en T-20.4.
> 3. **T-18.10** (BDD, 3 h) → cualquier back con margen.

## 5. Quedan para otro sprint

- **Borrar las tablas de estructura de Postgres** (`section`, `node`, `node_prerequisite`, `section_prerequisite`) cuando Neo4j ya mande en todos los entornos. Va a [[deuda-tecnica]].
- **Sincronización de vuelta de Neo4j a Postgres**, si alguna vez hace falta apagar el flag de lectura (ver el ajuste de T-18.6).
