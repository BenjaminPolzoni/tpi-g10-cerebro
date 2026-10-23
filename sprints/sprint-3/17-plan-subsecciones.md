---
tipo: plan
sprint: 3
historia: HU-58
tareas: [T-58.2, T-58.3]
responsable: Fenoglio Santino
fecha: 2026-10-22
estado: propuesto
---

# Plan: subsecciones como zonas dentro de la isla

> **Qué se pide.** HU-58 CA6 (P6, DEC-018): las dependencias también se definen entre subsecciones.
> T-58.2 ([#9152](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9152)): las reglas aceptan subsecciones como requisito y al guardar se rechaza cualquier ciclo.
> **Cómo se ve.** El archipiélago sigue con una isla por sección principal. Las subsecciones son **zonas dentro de la isla**.

Relevado sobre `origin/develop` de los dos repos el 22/10/2026.

## Lo que ya existe

| Dónde | Qué hay | Qué significa para nosotros |
|---|---|---|
| Courses (`tpi-course/FRONTEND_SUBSECTIONS.md`) | Una subsección es una `CourseSection` con `parent_section_id`. Un solo nivel. Lista plana, el cliente agrupa. `order_index` relativo a las hermanas | El modelo de Courses ya es "sección hija" |
| Back, `HttpCourseSectionsClient` | Filtra las subsecciones de Courses a propósito (`parentSectionId == null`, BE#262) | Hoy el sync solo trae raíces. No rompe nada si no lo tocamos |
| Back, `GraphSection` (Neo4j) | `HAS_SUBSECTION`, un nivel (D4) | El modelo de grafo ya las preveía como `:Section` hija |
| Back, `RuleOwnerType.SECTION` | Javadoc: "desbloquea una sección o subsección" | Las reglas de sección sirven para subsecciones sin tipo nuevo |
| Back, V59 | `unlock_rule_operand.element_type` (NODE o SECTION) por hoja | Base para mezclar hojas; no hace falta para este plan |
| Back, `GraphService` | `sectionGraph.assertNoCycle` y error `section.prerequisite-cycle` | El detector de ciclos entre secciones ya existe; falta sumarle la contención |
| Back, `NodeType.UNIT` | Existe pero nada le da comportamiento | D3 proponía convertirlo en subsección. Este plan no lo usa |
| Front, `world-gen.ts` | Cada isla es un camino con un tramo (con niebla propia) por desafío | Una zona = varios tramos seguidos. Encaja sin rehacer el generador |
| Front, `genIslandsLayout` | Una isla por sección, en serpentina | Si el back manda solo raíces en `sections`, el hub no cambia |
| Front, `courses/` | Ya maneja `parentSectionId` y restricciones de subsección | Courses tiene su propio sistema; el roadmap no lo usa |

**Lo que no existe:** ninguna columna ni tabla de subsección en Postgres del roadmap. DEC-021 dice que todo dato nuevo va primero a Postgres.

## Alternativas

| | Opción | A favor | En contra |
|---|---|---|---|
| **A** | **Subsección = sección con `parent_section_id`** (como Courses y como `HAS_SUBSECTION`) | Reusa reglas, gate, detector de ciclos, nodos y endpoints. Alineada con Courses, Neo4j y DEC-021 | Hay que cuidar que nada trate a una hija como unidad del mapa; la completitud del padre cambia |
| B | Tabla `subsection` propia y `node.subsection_id` | No toca las consultas de secciones | Duplica reglas, prerrequisitos, ciclos y API. Diverge de Courses y de Neo4j |
| C | Zona solo visual (etiqueta en el nodo o `UNIT`) | Rápida, solo front | No cumple CA6: no hay dependencias entre subsecciones |

**Elegida: A**, en cuatro fases. La C puede quedar como plan de emergencia si el equipo no quiere tocar el back en esta entrega.

## Propuestas para las decisiones abiertas

Llevar al equipo. Si nadie objeta, el plan avanza con estas:

| # | Pregunta | Propuesta |
|---|---|---|
| S1 | ¿Un padre puede tener nodos propios además de subsecciones? | Sí. Sus nodos van antes de la primera zona |
| S2 | ¿Las subsecciones llevan su propio inicio y fin (D7)? | No en esta entrega |
| S3 | ¿Se importan las subsecciones de Courses? | No en esta entrega. Se crean a mano. Los roadmaps `COURSE` siguen trayendo solo raíces. Se acuerda con G01 después |
| S4 | ¿Bioma propio por subsección? | No, hereda el del padre |
| S5 | ¿Qué pasa al dar de baja un padre con hijas activas? | Se rechaza (409) hasta dar de baja o mover las hijas |
| S6 | ¿Una subsección puede exigir una subsección de otra unidad? | Sí, mientras sea del mismo roadmap |
| S7 | ¿Se puede mover una subsección a otro padre? | No en la fase 1. Se borra y se crea |

## Fases

### Fase 1 · Back: modelo y contención (parte de T-58.2)

1. **Migración** (próximo número libre; en develop el último es V59 y hay huecos por PRs abiertos, revisar antes):
   `section.parent_section_id UUID NULL REFERENCES section (id)`, índice, `CHECK (parent_section_id <> id)`. SQL común H2 y Postgres si alcanza.
2. **Entidad:** `parentSection` (lazy) y lista `subsections` ordenada por `sortOrder`. El `sortOrder` de una hija es relativo a sus hermanas, como en Courses.
3. **API:**
   - `SectionRequest` acepta `parent_section_id` opcional (solo al crear, S7).
   - `SectionResponse` lleva `parent_section_id` y `subsections` (lista anidada).
   - El roadmap devuelve **solo raíces** en `sections`. Así el front de hoy sigue dibujando una isla por raíz sin cambios.
4. **Validaciones** (errores nuevos en `RoadmapErrorCode` y `ErrorCatalog`):
   - El padre existe, está vivo y es del mismo roadmap.
   - El padre es raíz: no hay segundo nivel (D4).
   - Baja de un padre con hijas vivas: 409 (S5).
5. **Contención en el gate:**
   - Completar el padre = sus nodos obligatorios **y** los de todas sus hijas. Hoy un padre sin nodos propios contaría como completo y abriría lo que depende de él.
   - Entrar a una hija exige poder entrar al padre (regla del padre más la de la hija).
6. **Clonado:** `RoadmapCloner` copia las hijas con el padre nuevo (HU-71).
7. **Revisar sin cambiar:** que `CourseSectionsReconciliationService` no dé de baja hijas creadas a mano en un roadmap `COURSE` (no tienen `course_section_id`).
8. **Tests:** migración, alta y validaciones, respuesta anidada, completitud del padre, gate de la hija, clonado, sync que no toca hijas.

### Fase 2 · Back: reglas entre subsecciones y ciclos (resto de T-58.2)

- Las reglas de sección aceptan hijas como hoja (ya son secciones; se valida mismo roadmap, S6).
- **Ciclos con contención:** una hija no puede exigir a su padre ni el padre a su hija (se trabaría). El detector suma las aristas padre-hija al grafo antes de `assertNoCycle`.
- Lecturas del editor (`sectionRulesOf`) y `unit_missing` (T-59.5) nombran a la subsección.
- Tests de cada caso de ciclo, de hermanas que se exigen entre sí y de hojas de otra unidad.

### Fase 3 · Back: propagación

- Proyector a Neo4j: `HAS_SUBSECTION` desde `parent_section_id` (`RoadmapGraphMapper`, `RoadmapStructureReader`).
- Sync con Courses (S3) solo si el equipo y G01 lo aprueban.

### Fase 4 · Front: editor y mundo

- **Modelo:** `Section.subsections` y `parentSectionId` en `roadmap.models.ts` y en el mapper.
- **Editor:** crear subsección dentro de una unidad, y `rules-wizard` en modo unidad con subsecciones elegibles (T-58.3).
- **Mundo (zonas en la isla):**
  - `worldSectionOf` agrupa los desafíos por zona; los de cada zona quedan **seguidos** en el camino, ordenados por sus reglas.
  - `genSectionWorld` pone en la entrada de cada zona una **puerta por bioma** con cartel. En zombie: barricada o contenedor rojo. En pradera: arco o cerca.
  - Zona bloqueada: niebla en todos sus tramos, puerta cerrada y cartel "Requiere …" (reusa `missing` y `unit_missing`).
  - Panel "Nodos de la unidad": agrupado por zona con su estado.
  - El hub del archipiélago no cambia; la card de la isla puede decir "3 zonas".
- Maqueta de referencia: la del bioma zombie que se armó el 22/10.

## Prompt para arrancar la fase 1

Copiar tal cual en una sesión nueva sobre `tpi-roadmap`:

```text
Tarea: T-58.2, fase 1 (Taiga #9152). Modelo de subsecciones en el back de Roadmap (tpi-roadmap).
Plan completo: C:\Users\Santino04\Desktop\tpi-g10-cerebro\sprints\sprint-3\17-plan-subsecciones.md (leelo entero antes de empezar, sección "Fase 1" y "Propuestas para las decisiones abiertas").

Reglas:
- Nada de co-autores ni "Generated with Claude Code" ni ninguna atribución a IA en commits ni en PRs.
- Antes de escribir Java consultá el MCP skillhub (search_skills) y seguí lo que aplique. No llames propose_skill sin preguntarme.
- Rama nueva desde origin/develop: feature/t-58-2-subsecciones-modelo. El checkout local está viejo (120 commits atrás) y tiene un docker/docker-compose.override.yml sin trackear que no es tuyo: no lo toques.
- Varios commits chicos y con sentido (migración, entidad y API, validaciones, gate, clonado, tests). Mensajes en español como el resto del repo.
- Me evalúan por líneas: quiero tests reales y completos de cada caso (validaciones, respuesta anidada, completitud del padre, gate de la hija, clonado, sync que no toca hijas). Nada de relleno.
- Antes de terminar corré ./mvnw -o -B clean verify (Checkstyle con Javadoc y @param en todo, PMD CommentSize de 6 líneas y 80 columnas, CPD). Si un target/classes viejo trae una migración repetida, borrala de target.
- No pushees ni abras PR sin mi OK.

Qué hacer (fase 1):
1. Migración con el próximo número libre (en develop el último es V59; revisá PRs abiertos por huecos): section.parent_section_id UUID NULL con FK a section, índice y CHECK de que no sea la misma sección.
2. SectionEntity: parentSection y subsections (orden por sortOrder, relativo a las hermanas).
3. API: SectionRequest acepta parent_section_id opcional solo al crear. SectionResponse devuelve parent_section_id y subsections anidadas. El roadmap devuelve solo raíces en sections, para que el front actual siga dibujando una isla por raíz.
4. Validaciones con códigos nuevos en RoadmapErrorCode y ErrorCatalog: padre vivo y del mismo roadmap, padre raíz (un solo nivel), baja de padre con hijas vivas = 409.
5. Contención en el gate: completar el padre exige sus obligatorios y los de todas sus hijas (SectionPrerequisiteService.isComplete y lo que lo use); entrar a una hija exige poder entrar al padre.
6. RoadmapCloner copia las hijas con el padre nuevo.
7. Verificá que CourseSectionsReconciliationService no dé de baja hijas creadas a mano en roadmaps COURSE; si lo hace, corregilo y testealo.

Fuera de alcance: reglas entre subsecciones y ciclos (fase 2), proyector Neo4j y sync con Courses (fase 3), front (fase 4).
Al terminar, contame qué decisión tomaste en cada punto que el plan no cerraba, cuántas líneas agregaste (código y tests por separado) y qué quedó para la fase 2.
```

## Prompt para la fase 2

Arrancar cuando la fase 1 esté terminada (no hace falta que esté mergeada: se corta de su rama).

```text
Tarea: T-58.2, fase 2 (Taiga #9152). Reglas entre subsecciones y sin ciclos en el back de Roadmap (tpi-roadmap).
Plan completo: C:\Users\Santino04\Desktop\tpi-g10-cerebro\sprints\sprint-3\17-plan-subsecciones.md (leé "Fase 2", "Propuestas para las decisiones abiertas" y lo que dejó la fase 1).

Reglas:
- Nada de co-autores ni "Generated with Claude Code" ni ninguna atribución a IA en commits ni en PRs.
- Antes de escribir Java consultá el MCP skillhub (search_skills) y seguí lo que aplique. No llames propose_skill sin preguntarme.
- Rama nueva normal: feature/t-58-2-subsecciones-reglas, cortada de feature/t-58-2-subsecciones-modelo (fase 1). Si la fase 1 ya se mergeó, cortala de origin/develop. No toques docker/docker-compose.override.yml.
- Varios commits chicos y con sentido. Mensajes en español como el resto del repo.
- Me evalúan por líneas: tests reales y completos de cada caso. Nada de relleno.
- Antes de terminar corré ./mvnw -o -B clean verify (Checkstyle, PMD CommentSize de 6 líneas y 80 columnas, CPD).
- No pushees ni abras PR sin mi OK.

Qué hacer (fase 2):
1. Hojas: la regla de una unidad o subsección (PATCH /sections/{id}/rules, plano y con árbol) acepta subsecciones como requisito. Validá que la hoja sea del mismo roadmap y esté viva; puede ser de otra unidad (S6).
2. Contención: una hija no puede exigir a su propio padre ni el padre a su hija, directo o dentro de un grupo. Error nuevo en RoadmapErrorCode y ErrorCatalog.
3. Ciclos: el detector de secciones (sectionGraph.assertNoCycle en GraphService) suma las aristas padre-hija antes de buscar ciclos, así se rechaza por ejemplo "1.2 exige Unidad 2" cuando "Unidad 2 exige Unidad 1". Cubrí también el agregado suelto de un prerrequisito (appendToRoot) y el cambio de modo.
4. Lecturas: sectionRulesOf y la lectura del roadmap devuelven las reglas de las hijas; las hojas a hijas dadas de baja u ocultas se podan como las de unidades.
5. Alumno: lo que le falta (missing y unit_missing de T-59.5) nombra la subsección cuando la exigida es una hija.
6. Gate: verificá con tests de punta a punta que una subsección exigida bloquea y desbloquea bien, sola y combinada con XP mínimo.

Fuera de alcance: proyector Neo4j y sync con Courses (fase 3), front (fase 4).
Al terminar, contame qué decidiste en lo que el plan no cerraba, cuántas líneas agregaste (código y tests por separado) y qué quedó pendiente.
```

## Registro

| Fecha | Qué |
|---|---|
| 22/10 | Plan propuesto. Pendiente: decisiones S1 a S7 con el equipo |
