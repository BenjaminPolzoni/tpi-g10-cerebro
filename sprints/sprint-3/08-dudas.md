---
tags: [tpi, g10, sprint-3, dudas]
fecha: 2026-10-15
estado: vigente
---

# 08 — Dudas del Sprint 3

> [!info] Cómo usar esta nota
> Todas las dudas del sprint en un solo lugar, con a quién preguntarle y qué trabajo frenan.
> - Cuando se responda una, completar **Respuesta** con la fecha y la fuente (minuta, mensaje), y pasarla a [[#Respondidas]].
> - Si la respuesta cambia una decisión técnica, registrarla también en [[decisiones/README|decisiones/]].
> - Los códigos (HU-NN, HT-NN) son las historias de [[sprints/sprint-3/09-epicas-e-historias|09]]. "Bloque 0" = épica Deuda del Sprint 2.

**Prioridad:** 🔴 bloquea el diseño o el arranque · 🟠 bloquea una HU puntual · 🟢 se puede resolver sobre la marcha.

> [!success] Estado al 2026-10-15
> Se respondieron 36 de las 41 dudas (todas las de los profes). Quedan **5 abiertas** (G2, G3, G7, G9 y E6) y **6 pendientes nuevos** que salen de las respuestas (ver [[#Pendientes que salen de las respuestas]]).
> Las decisiones de modelo quedaron en [[decisiones/DEC-017-n-roadmaps-por-curso-configurables|DEC-017]] y [[decisiones/DEC-018-catalogo-de-relaciones-y-tipos-de-nodo|DEC-018]].

## Abiertas

### Para otros grupos

| # | Prio | Grupo | Duda | Bloquea | Origen | Estado |
|---|---|---|---|---|---|---|
| G2 | 🟠 | **G07 Users** (antes figuraba G06) | **Catálogo de permisos**: ¿qué nombres usan (ej. `roadmap.graph.edit`) y cómo llegan en el token? | HT-22 | [[07-correcciones-profes]] | 2026-10-15: todavía no está definido. El catálogo es de **Users**, no de Backoffice |
| G3 | 🟠 | G06 Backoffice | **Dashboard**: ¿qué datos quieren de nosotros (progreso, ranking, XP) y por dónde (REST o eventos)? | HT-24 | [[07-correcciones-profes]] | 2026-10-15: todavía no se sabe |
| G7 | 🟢 | G07 Users | Usuarios demo (admin, profe, alumno): ¿ids y credenciales estables para usarlos en nuestro seed? | HT-21 | [[07-correcciones-profes#2. No son nuestros]] | 2026-10-15: todavía no hay |
| G9 | 🟢 | G06 Backoffice | ¿Siguen dependiendo del header `X-User-Roles: MS` que exigía el contrato original? | — | [[acuerdos/backoffice]] | ⚠️ Confirmar: la respuesta recibida para G9 ("sí, debe ser único, incluso luego de una clonación…") habla del `node_id` y se cargó en G8 |

### Del equipo

| # | Prio | Duda | Cómo se resuelve | Bloquea | Origen | Estado |
|---|---|---|---|---|---|---|
| E6 | 🟢 | `KAFKA_TOPIC_ROADMAP`: en `develop` el default es `roadmap.events`. ¿El compose de cada entorno lo pisa con otro valor? | Revisar `tpi-system-compose` | — | [[acuerdos/notificaciones-bus]] | 2026-10-15: nadie lo sabe todavía |

### Pendientes que salen de las respuestas

Trabajo nuevo o cambios de alcance que aparecieron al responder. No tienen historia todavía.

- [ ] **Clonar un roadmap con sus restricciones** para otro grupo o curso (G4), generando `node_id` nuevos (G8). No hay HU: crearla en la épica [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps]].
- [ ] **Estado académico final** entra en el Sprint 3 (P15). No hay HU en el sprint (era HU-27/28, diferidas en EP-61): crearla o reabrirla.
- [ ] **Racha** es nueva para el Sprint 3 (E12). EP-592 no tiene HU: crearla.
- [ ] **Tipos de nodo nuevos en el código** (P8): faltan recuperación de vida, desafío de IA, `START` y `END`. Y `START`/`END` pasan a ser obligatorios **también por unidad/sección**, no solo por roadmap: ajustar [[sprints/sprint-3/historias/HU-64 Nodos de inicio y fin obligatorios|HU-64]].
- [ ] **Configuraciones del profesor** (P2, P3, P5): dónde viven XP, vidas, nivel y ranking; si un roadmap usa secciones de Courses o propias; si el alumno ve todos los roadmaps o por comisión. Ubicarlas en HT-17, HU-57 y HU-61.
- [ ] **Recortar el backlog con la capacidad del Excel** (P12): 445,6 h ajustadas para 12 personas. El equipo va a borrar algunas historias.

## Respondidas

### 1. Para los profes o el PO

Fuente de todas: respuestas cargadas por Ludmila el 2026-10-15.

| # | Duda | Respuesta | Impacto |
|---|---|---|---|
| P1 | "El mapa es el curso" contra "un curso puede tener 1 o más roadmaps" | **Cada roadmap es un mapa distinto del mismo curso**: puede armarse por grupos del curso, por secciones, por subsecciones, etc. Se mantienen los N roadmaps | HT-17, HU-57, HU-61, HT-19 y HU-66 siguen con su alcance completo. [[decisiones/DEC-017-n-roadmaps-por-curso-configurables\|DEC-017]] |
| P2 | XP, vidas, nivel y ranking: ¿por curso o por roadmap? | **Lo configura el profesor**: puede ser por curso (compartido) o por roadmap; se admiten las dos | HT-17 y HU-61: un ajuste por curso/roadmap en vez de un modelo fijo |
| P3 | Secciones de Courses con N roadmaps | **Lo configura el profesor**: el roadmap puede usar secciones de Courses o tener secciones propias; se admiten las dos | HT-17, HT-19 |
| P4 | ¿Cuáles son los tipos de relación? | Son **5**: `related_to`, `belongs_to`, `part_of` / `parte_de`, `requires` y `recommends`. En `requires` el profesor configura la condición: AND/OR, XP mínimo, o las dos | HU-65, HT-18. Ver el catálogo abajo y [[decisiones/DEC-018-catalogo-de-relaciones-y-tipos-de-nodo\|DEC-018]] |
| P5 | ¿El alumno ve todos los roadmaps del curso o por comisión? | **Lo configura el profesor**: todos o asignados por comisión; se admiten las dos | HU-61, HU-44 |
| P6 | Secciones "anidadas": ¿dependencias entre secciones o subsecciones? | **Dependencias entre subsecciones** | HU-58, HT-18: el modelo tiene que admitir subsecciones y relacionarlas |
| P7 | ¿Hacen falta reglas combinadas (`A y (B o C)`)? | **Sí**, además de AND/OR + XP mínimo | HU-59, HT-20 siguen con su alcance |
| P8 | ¿Qué significa "completamente personalizable"? | **No hay campos libres ni tipos de nodo nuevos.** Los tipos son: desafíos teóricos, prácticos, de IA y de recuperación de vida, examen, contenido teórico, inicio y fin. **Inicio y fin son obligatorios siempre**, para el curso y para cada unidad/sección. Personalizable = **nombre, ícono, descripción y reglas** | HU-60 se redefine (sin clave-valor libre). HU-64 se amplía a unidades/secciones. HT-18 |
| P9 | Examen por hora: ¿quién define la ventana? | **Courses** (la publica, como en HU-49) | HU-67 deja de tener una ventana propia en el nodo; HU-49 |
| P10 | Ranking: ¿default por curso y la comisión como filtro? | **Sí.** Comisión = grupo | HU-45 |
| P11 | Archibaldo como Hernán: ¿referencia visual? | Archibaldo pasa a ser un **avatar personalizable por el profesor y el gestor del curso**, que también le pueden **cambiar el nombre** | HU-69 cambia: ya no es "aspecto de Hernán" |
| P12 | Mínimo para la demo | **Guiarse por la capacidad del Excel** ([Capacidad Sprint 3](https://docs.google.com/spreadsheets/d/1v2ofVa0sACpaW6F9Y4JUAtQQvN-g20Op/edit?usp=drive_web&ouid=112280761703985307915&rtpof=true)). Algunas historias se van a borrar pronto | Al 2026-10-15: 12 integrantes, 14 días, **532 h efectivas / 445,6 h ajustadas**; las hojas Tareas y Reparto están vacías. Ver [[06-backlog-sprint-3]] |
| P13 | HU-46 (Templo): ¿se rehace o se redefine? | **El Templo no existe más** | HU-46 se redefine sin Templo: queda el material dentro de los nodos |
| P14 | Ranking por XP, por notas o por ambas | **Las notas vienen del Motor de desafíos (G09)** | HU-45: acordar con G09 cómo llegan las notas. No se especificó si el orden es solo por notas o XP + notas |
| P15 | Estado académico final: ¿entra en el Sprint 3? | **Sí** | No hay HU en el sprint: ver [[#Pendientes que salen de las respuestas]] |
| P16 | "Multiple choice con boss fight" | **Es de Desafíos teóricos** (G04/G09), no nuestro | Nada para G10 más allá del nodo `EXAM` |

### Catálogo de relaciones entre nodos (P4, cerrado)

Elegidas el 2026-10-15. Cada una lleva `label` visible y `visible` configurable.

- [x] `requires` / `requiere`: una necesita de otra para desbloquearse (Nodo B requires Nodo A). **Afecta el desbloqueo.** El profesor configura si la condición es AND/OR, XP mínimo o las dos
- [x] `recommends` / `recomienda`: sugerida, no obligatoria (Nodo B recommends Nodo A). No bloquea
- [x] `belongs_to` / `pertenece_a`: pertenencia a un grupo (Juan belongs_to Equipo A)
- [x] `related_to` / `relacionado_con`: relación genérica, sin especificar el tipo
- [x] `part_of` / `parte_de`: composición (wheel part_of car)

Descartadas: `is_a`, `instance_of`, `located_in`, `has_property` y `causes`.

> [!note] Sobre el desbloqueo
> Solo `requires` (y las reglas combinadas de P7) afectan el desbloqueo. `recommends` se muestra en el mapa pero no bloquea, como dice el catálogo propuesto.

### 2. Para otros grupos

| # | Grupo | Duda | Respuesta | Impacto |
|---|---|---|---|---|
| G1 | Plataforma | ¿Quién suma Neo4j al compose y a los entornos? | **Neo4j es solo para nuestro micro.** No se migra toda la base: solo los grafos (curso, sección, unidad, etc.) | HT-16, HT-18. Sigue por coordinar con plataforma quién lo suma al compose (T-16.2) |
| G4 | G01 Courses | Con N roadmaps, ¿cómo quedan los contratos de secciones y de restricciones? | **El profesor define las restricciones por cada roadmap.** Además puede **clonar un roadmap con sus restricciones** para otros grupos o cursos | HT-19, HU-49. Clonar es trabajo nuevo (sin HU) |
| G5 | G01 Courses | ¿Sus eventos reales ya salen en snake_case? | **Todo en snake_case** | HT-12. [[acuerdos/courses-g01]] |
| G6 | G07 Users / G01 | Vocabulario de roles | **Ya no habrá roles: habrá permisos.** Mientras tanto, vale `PROFESSOR`/`GESTOR` | HT-22 |
| G8 | G09 Motor | ¿Alcanza con que `node_id` sea único global? | **Sí.** Tiene que ser único incluso después de una clonación: clonar genera `node_id` nuevos | HT-19, HU-01 |
| G10 | Accounting / Inventario | ¿Qué número de grupo tienen? ¿Inventario y Accounting son el mismo equipo? | **Sí, es el mismo equipo: Accounting.** El número de grupo no se dio | [[acuerdos/accounting]], [[acuerdos/inventario]] |
| G11 | Plataforma | ¿Qué grupo tiene Gateway / Kafka? | **Gateway lo lleva Users (G07); Kafka lo lleva Notificaciones** | [[acuerdos/plataforma-gateway-kafka]] |
| G12 | Plataforma | ¿Están emitidos los scopes H1 de Courses y `users.legajo.read`? | **Existe `student.enrollment.read`**, que lee la matrícula del alumno en el curso | HT-13. [[acuerdos/plataforma-gateway-kafka]] |
| G13 | Equipo UI-KIT | ¿Quién es dueño del componente de grafo? ¿El avatar `2xl` alcanza para el perfil? | **Los dueños del componente de grafo somos nosotros (G10).** El avatar **no se usa como foto de perfil** | HU-70, HU-62, HT-25 |

### 3. Del equipo

| # | Duda | Respuesta | Impacto |
|---|---|---|---|
| E1 | Error del ranking por grupo | **Se arregla en este sprint** | HU-45 |
| E2 | Tres criterios de insignia que nunca se otorgan | **Se implementan** | HU-21: `SECTION_NO_LIVES_LOST`, `NODE_NO_RETRIES` y `LIFE_RECOVERED` |
| E3 | HU-45 / HU-49: ¿Bloque 0 o alcance nuevo? | **Ya debería estar hecho; se corrobora** | HU-45, HU-49 |
| E4 | Curva PAR-09: ¿cuál está activa? | **La de Backoffice** (1200/3500/7300 para los niveles 3/5/7) | HT-21 (seed). [[decisiones/DEC-012-curva-de-niveles-desde-par-09\|DEC-012]] |
| E5 | `fix/account-not-found-gate` | **Ya está hecho** | HT-12 |
| E7 | `TraceIdFilter`: ¿se borró a propósito? | **Sí, se borró a propósito** | HT-23: sacarlo de la documentación |
| E8 | ¿Hace falta consumir `LIVES_EXHAUSTED` / `LIVES_AVAILABLE`? | **Sí** | HU-21 (`LIFE_RECOVERED`). [[acuerdos/accounting]] |
| E9 | `ParUnavailableException`: ¿qué pasa con Backoffice caído? | **Se usan los valores guardados en caché** | HU-15. [[acuerdos/backoffice]] |
| E10 | ¿Se cierran las épicas viejas en Taiga? | **Sí** | HT-15 |
| E11 | HU sin épica (HT-04, HT-05, HT-10, HT-11) | **No llevan épica** (alcanza con el tag `g10`) | HT-15 |
| E12 | EP-72 Avatares y EP-592 Racha sin HU | **Avatares ya está hecho; Racha es nueva para el Sprint 3** | HT-28. Falta la HU de Racha |

### Anteriores

| # | Duda | Respuesta | Fecha y fuente |
|---|---|---|---|
| — | ¿Exigen una BD de grafos como requisito? | Sí, Neo4j. Ver [[decisiones/DEC-016-neo4j-para-la-estructura-del-roadmap\|DEC-016]] | 2026-10-14, [[07-correcciones-profes\|correcciones]] |
| — | ¿Qué número de grupo tienen Backoffice y Users? | Backoffice = G06, Users = G07 | 2026-10-14, [[07-correcciones-profes\|correcciones]] |
