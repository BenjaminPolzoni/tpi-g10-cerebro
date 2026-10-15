---
tags: [tpi, g10, sprint-3, correcciones, profes]
fecha: 2026-10-14
estado: vigente
---

# 07 — Correcciones de los profes vs lo ya planteado

> [!info] Fuente
> Documento "Correcciones — lo que nos toca" ([[fuentes/correcciones-profes-original|original]]), cruzado con las notas 01 a 06 de este sprint y con `origin/develop` del back y del front (2026-10-14).

**Leyenda:**
- ✅ **Ya planteado**: estaba en el cerebro.
- ⚠️ **Parcial**: estaba en parte o desde otro ángulo.
- 🆕 **Nuevo**: no estaba en el cerebro.

## Resumen

| | Cantidad |
|---|---|
| ✅ Ya planteado | 1 |
| ⚠️ Parcial | 7 |
| 🆕 Nuevo | 9 |

> [!important] Cambios de fondo que traen las correcciones
> 1. **La BD de grafos ahora la piden los profes.** Responde la pregunta 7 de [[03-requerimientos-profes]]. La opción C (Neo4j) de [[04-base-de-grafos]] pasa de "si los profes la piden" a **decisión del sprint**.
> 2. **Las relaciones pasan a tener tipo** (4 niveles, con nombre visible y configurables). Ya no son solo "prerrequisito AND/OR". Esto refuerza Neo4j: las relaciones con tipo y propiedades son su punto fuerte.
> 3. **Nodos de inicio y fin obligatorios.** Es una regla nueva del grafo, que se valida al guardar.
> 4. **"El mapa *es* el curso."** Puede chocar con "un curso con N roadmaps". Ver P1 en [[08-dudas]].

## 1. Lo que es nuestro

### Grafo y editor

| Corrección                                                                                                      | Estado | Dónde estaba                                                                                                         | Qué hay en el código                                                                                                     | Qué se agrega                                                                                                                           |
| --------------------------------------------------------------------------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Mejorar el arrastre del grafo y relacionar unidades desde el editor                                             | ⚠️     | [[03-requerimientos-profes]] (vista de nodos), [[06-backlog-sprint-3]] HU 5 y 9, [[05-ui-kit]] (componente de grafo) | `moveNode` devuelve 501: las posiciones no se guardan. Las aristas se escriben reescribiendo las reglas del nodo destino | Lo ya planteado más **crear relaciones arrastrando de un nodo a otro** en la vista de grafo                                             |
| Las unidades son el curso: el mapa *es* el curso (ejemplo Google Maps). `course-editor-page` es nuestra         | 🆕     | —                                                                                                                    | `course-editor-page` es la vista tipo Moodle                                                                             | Rediseñar el editor para que el curso se vea y se edite como mapa. Hay que conciliarlo con los N roadmaps (pregunta 1)                  |
| Regla: siempre nodo de inicio y nodo final, con el grafo en el medio. No dejar guardar sin ellos                | 🆕     | —                                                                                                                    | `NodeType`: `UNIT`, `CONTENT`, `THEORETICAL_CHALLENGE`, `PRACTICAL_CHALLENGE`, `EXAM`. No existen START ni END           | Tipos `START` y `END`. Validación al guardar: exactamente un inicio y un fin, todo nodo alcanzable desde el inicio, y el fin alcanzable |
| Relaciones con 4 niveles (Related to / Belongs to…): tipos definidos, configurable qué se ve, mostrar el nombre | 🆕     | —                                                                                                                    | Solo hay `prerequisite` con modo AND/OR                                                                                  | Catálogo de tipos de relación con nombre y visibilidad configurable. Etiqueta en la arista. Solo `REQUIRES` afecta el desbloqueo        |
| Usar una BD de grafos (ej. Neo4j) en vez de tablas relacionales                                                 | ✅      | [[04-base-de-grafos]] (opción C y diseño)                                                                            | Todo en Postgres                                                                                                         | Pasa a **decisión tomada**. El spike 1 del backlog deja de elegir la BD y pasa a validar la infra                                       |
| Lista de nodos que muestre la obligatoriedad (qué nodo es prerrequisito de otro)                                | ⚠️     | [[01-estado-actual]] HU-11 (⚠️ front: el flag se edita, pero no hay UI de bloqueo)                                   | `unit-node-list` muestra los nodos sin dependencias                                                                      | En la lista: marca de obligatorio y "requiere: X, Y" por nodo                                                                           |

### Nodos especiales

| Corrección | Estado | Dónde estaba | Qué hay en el código | Qué se agrega |
|---|---|---|---|---|
| Nodo de inicio "Bienvenidos", con un visual de que empieza acá | 🆕 | — | — | Nodo `START`, con su visual en el mapa 2D y en el mundo 3D |
| Nodo final "Felicitaciones", con un visual de que termina ahí | 🆕 | — | — | Nodo `END`, con su visual. Puede disparar una insignia de fin de curso (HU-21) |
| Nodo examen habilitado por hora. El nodo y su desbloqueo son nuestros (HU-01); el contenido lo arma desafíos (G04/G09) | ⚠️ | [[01-estado-actual]] HU-49 (restricciones por fecha que publica Courses) | El gate ya evalúa `DATE_RESTRICTED` con ventanas que vienen de Courses (`DateGateTest`) | Una **ventana horaria propia del nodo** (`available_from`/`available_until`), evaluada por el gate con el mismo motivo. Definir si manda Courses o nosotros (pregunta 3) |

### Ranking

| Corrección | Estado | Dónde estaba | Qué hay en el código | Qué se agrega |
|---|---|---|---|---|
| El ranking por grupo hoy da error. Ver por qué no se ve, explicar que todas las evaluaciones son del mismo curso y definir si el default es por curso | ⚠️ | [[01-estado-actual]] HU-44 y HU-45 (front ❌, flag `ROADMAP_BY_GROUP_ENABLED=false`) | Back: el ranking es solo por curso (`GET /courses/{id}/ranking`, sin parámetro de grupo). El avance por grupo está en otro endpoint (`/groups/{gid}/progress`). Front: no hay selector de grupo en el ranking | Reproducir el error. **Default: ranking por curso**, con filtro opcional por comisión. Encender el flag en la demo |

### Mundo y Archibaldo

| Corrección | Estado | Dónde estaba | Qué hay en el código | Qué se agrega |
|---|---|---|---|---|
| Archibaldo con el aspecto visual de Hernán | 🆕 | — | El NPC usa la skin del capitán pirata del kit (`world-3d.service.ts:3109`) | Modelo o skin nuevo |
| Destello en el camino que guíe por el mapa | 🆕 | — | — | Efecto de partículas o brillo sobre el camino al próximo nodo disponible |
| Hablar con Archibaldo con Enter, no solo con clic | ⚠️ | [[05-ui-kit]] (`npc-dialogue` debería ser `generic-modal`, con foco gestionado) | El mundo ya escucha `keydown` (`archipelago-3d.service.ts:3126`). El diálogo se abre con clic | Interactuar con Enter cuando el NPC está en rango. Es accesibilidad por teclado |

### De todos los grupos (hacemos nuestra parte)

| Corrección | Estado | Dónde estaba | Qué hay en el código | Qué se agrega |
|---|---|---|---|---|
| Seed de la demo con un curso entero: nuestra BD con un roadmap completo y curado | ⚠️ | [[01-estado-actual]] HT-02 (seed) y HT-09 (se sacaron las simulaciones) | Los datos de ejemplo se sacaron del micro (HT-09) | Un seed **curado** y reproducible (script o migración `demo`, fuera del perfil productivo) con un curso completo, con inicio y fin, tipos de relación y examen por hora. Usa los usuarios demo de G07 |
| Permisos en los endpoints en vez de roles. Hoy hay unos 16 `hasRole`/`hasAnyRole` en Roadmap | 🆕 | — | 17 `@PreAuthorize` con `hasRole`/`hasAnyRole` en 12 controllers, más un chequeo manual de rol en `RankingController` (`:74-86`) | Migrar a permisos (`hasAuthority('roadmap.graph.edit')`, etc.). Alinear el catálogo de permisos con G06 (roles y permisos desde parámetros globales) |
| Documentación global del micro Roadmap | ⚠️ | [[decisiones/README]], [[acuerdos/README]]; el back tiene `docs/` con contratos y T-* | Docs dispersos por tarea; el README del micro es básico | Un doc global: qué hace, modelo, endpoints, eventos, flags, cómo levantarlo, decisiones. Puede salir de este cerebro |
| Dashboard entre todos. Lo arma G06; nosotros definimos qué datos aportamos (progreso, ranking, XP) | 🆕 | — | Ya existen endpoints de progreso, ranking, nivel y avance por grupo | Acordar con G06 qué datos y por dónde (REST o eventos). Registrarlo en `acuerdos/` (nota nueva para G06) |

## 2. No son nuestros

Están fuera del alcance de G10. Igual hay que tenerlos presentes porque nos tocan de costado.

| Ítem | Dueño | Qué hacemos nosotros |
|---|---|---|
| Usuarios demo admin, profe y alumno | G07 Users | Usarlos en nuestro seed |
| Quitar el UUID del curso en buscadores y selects | G06 y G12 | En nuestras pantallas no aparece. Revisar que siga así (la regla aplica igual) |
| Parámetros globales en el BackOffice | G06 | Leemos los nuestros (curva de XP, PAR-09). Ver [[acuerdos/backoffice]] |
| Auditoría por curso (profesores) | G06 | Mandar nuestros eventos (`roadmap.events`) |
| Drag and drop del orden del desafío | G04 (probable) | Nada |
| Vista cross-curso del dashboard del admin | G06 | Aportar datos (ver "Dashboard") |
| Rango de fechas por defecto en el reporte | G06 | Nada |
| Roles y permisos desde parámetros globales | G06 | **Depende de nosotros**: nuestra migración a permisos tiene que usar su catálogo |
| Alertas | G06 | Nada |
| Permitir sumar parámetros globales | G06 | Nada |
| Chat y canales externos | G02 | Nada |
| Creación de desafíos | G04 / G09 | Nada. El pool del Motor ya está integrado (HU-47) |
| Resolución y corrección de desafíos | G04 / G09 | Nada |
| Git de desafíos | G04 / G09 | Nada |

## Preguntas nuevas para los profes

> [!question] Sumadas a [[08-dudas]] (P1, P4, P9, P10 y P11)
> 1. **"El mapa es el curso"** contra **"un curso puede tener 1 o más roadmaps"**: ¿cómo conviven? ¿Cada roadmap es un mapa distinto del mismo curso, o el curso es un único mapa y lo de los N roadmaps queda descartado?
> 2. **¿Cuáles son los 4 tipos de relación?** El documento menciona "Related to", "Belongs to" y "una necesita de otra". ¿Cuál es el cuarto? ¿Alguno además de "necesita" afecta el desbloqueo?
> 3. **Examen por hora**: ¿la ventana horaria la define el profesor en el roadmap, o la publica Courses (HU-49)?
> 4. **Ranking**: ¿confirmamos que el default es por curso y que la comisión es solo un filtro?
> 5. **Archibaldo como Hernán**: ¿hay referencia visual o un modelo que debamos usar?

## Impacto en el backlog

Se aplicó en [[06-backlog-sprint-3]]: se agregó la épica "Correcciones de los profes" y el spike 1 pasa a validar la infra de Neo4j, no a elegir la BD.
