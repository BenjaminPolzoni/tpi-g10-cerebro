---
tags: [tpi, g10, sprint-3, dudas]
fecha: 2026-10-14
estado: vigente
---

# 08 — Dudas del Sprint 3

> [!info] Cómo usar esta nota
> Todas las dudas abiertas del sprint en un solo lugar, con a quién preguntarle y qué trabajo frenan.
> - Cuando se responda una, completar **Respuesta** con la fecha y la fuente (minuta, mensaje), y pasarla a [[#Respondidas]].
> - Si la respuesta cambia una decisión técnica, registrarla también en [[decisiones/README|decisiones/]].
> - Los números entre paréntesis (1–12, C1–C11, Bloque 0) son ítems de [[06-backlog-sprint-3]].

**Prioridad:** 🔴 bloquea el diseño o el arranque · 🟠 bloquea una HU puntual · 🟢 se puede resolver sobre la marcha.

## 1. Para los profes o el PO

| # | Prio | Duda | Bloquea | Origen | Respuesta |
|---|---|---|---|---|---|
| P1 | 🔴 | **"El mapa es el curso" contra "un curso puede tener 1 o más roadmaps".** ¿Cada roadmap es un mapa distinto del mismo curso, o el curso es un único mapa y se descarta lo de N roadmaps? | 2, 4, 8, 11, C3 | [[07-correcciones-profes]] | |
| P2 | 🔴 | **XP, vidas, nivel y ranking**: ¿son por curso (compartidos entre roadmaps) o por roadmap? | 2, 8 | [[03-requerimientos-profes]] (1) | |
| P3 | 🔴 | **Secciones de Courses con N roadmaps**: ¿cada roadmap elige qué secciones de Courses usa, o las secciones pasan a ser propias del roadmap? | 2, 11 | [[03-requerimientos-profes]] (2) | |
| P4 | 🔴 | **¿Cuáles son los 4 tipos de relación?** El documento nombra "Related to", "Belongs to" y "una necesita de otra". ¿Cuál es el cuarto? ¿Alguno además de "necesita" afecta el desbloqueo? | 3, C2 | [[07-correcciones-profes]] | |
| P5 | 🟠 | ¿El alumno ve **todos** los roadmaps del curso, o se asignan **por comisión** (HU-44)? | 8 | [[03-requerimientos-profes]] (3) | |
| P6 | 🟠 | Secciones **"anidadas"**: ¿dependencias entre secciones o **subsecciones** (una sección adentro de otra)? | 3, 5 | [[03-requerimientos-profes]] (4) | |
| P7 | 🟠 | ¿Hacen falta **reglas combinadas** (`A y (B o C)`), o alcanza con AND/OR + XP mínimo por sección y por nodo? | 6, 12 | [[03-requerimientos-profes]] (5) | |
| P8 | 🟠 | ¿Qué significa **"completamente personalizable"**? ¿Campos libres definidos por el profesor, tipos de nodo nuevos, o solo nombre, ícono, descripción y reglas? | 7 | [[03-requerimientos-profes]] (6) | |
| P9 | 🟠 | **Examen por hora**: ¿la ventana horaria la define el profesor en el roadmap, o la publica Courses (HU-49)? | C4, HU-49 | [[07-correcciones-profes]] | |
| P10 | 🟢 | **Ranking**: ¿confirmamos que el default es por curso y que la comisión es solo un filtro? | C6 | [[07-correcciones-profes]] | |
| P11 | 🟢 | **Archibaldo como Hernán**: ¿hay referencia visual o un modelo que debamos usar? | C7 | [[07-correcciones-profes]] | |
| P12 | 🟢 | **Mínimo para la demo**: la épica nueva más las correcciones no entran enteras en un sprint. ¿Qué es imprescindible para la demo? | Todo el sprint | [[06-backlog-sprint-3#Riesgos del sprint]] | |
| P13 | 🟢 | **HU-46 (Templo)**: se borró del front. ¿Se rehace o se redefine el criterio de aceptación? | Bloque 0 | [[02-pendientes]] | |

> [!tip] Orden para la consulta
> P1 a P4 primero: definen el modelo de Neo4j (módulo `graph`) y el 1:N. Sin esas respuestas no conviene arrancar los ítems 2 y 3.

## 2. Para otros grupos

| # | Prio | Grupo | Duda | Bloquea | Origen | Respuesta |
|---|---|---|---|---|---|---|
| G1 | 🔴 | Plataforma (compose/mesh) | ¿Quién suma **Neo4j** al compose y a los entornos? ¿Hay recursos para un servicio más? | 1, 3 | [[decisiones/DEC-016-neo4j-para-la-estructura-del-roadmap\|DEC-016]] | |
| G2 | 🟠 | G06 Backoffice | **Catálogo de permisos**: ¿qué nombres usan (ej. `roadmap.graph.edit`) y cómo llegan en el token? | C9 | [[07-correcciones-profes]] | |
| G3 | 🟠 | G06 Backoffice | **Dashboard**: ¿qué datos quieren de nosotros (progreso, ranking, XP) y por dónde (REST o eventos)? | C11 | [[07-correcciones-profes]] | |
| G4 | 🟠 | G01 Courses | Con N roadmaps, ¿cómo queda el contrato de secciones (HT-07, HU-36) y el de restricciones (HU-49)? Depende de P3 | 11 | [[03-requerimientos-profes#Impacto en otros grupos]] | |
| G5 | 🟠 | G01 Courses | `courses.md` §7.3 sigue en camelCase y Roadmap lee solo snake_case desde #191. ¿Sus eventos reales ya salen en snake_case? | Bloque 0 | [[acuerdos/courses-g01]] | |
| G6 | 🟢 | G07 Users / G01 | **Vocabulario de roles**: Users emite `GESTOR`/`PROFESSOR`; Courses documenta `MANAGER`/`PROFESSOR_READ_ONLY`. ¿Cuál vale? (Pierde peso si migramos a permisos, C9) | C9 | [[acuerdos/courses-g01]], [[acuerdos/users]] | |
| G7 | 🟢 | G07 Users | Usuarios demo (admin, profe, alumno): ¿ids y credenciales estables para usarlos en nuestro seed? | C8 | [[07-correcciones-profes#2. No son nuestros]] | |
| G8 | 🟢 | G09 Motor | El evento de cierre trae `id_course` + `id_node`. Con N roadmaps, ¿alcanza con que `node_id` sea único global? | 11 | [[03-requerimientos-profes#Impacto en otros grupos]] | |
| G9 | 🟢 | G06 Backoffice | ¿Siguen dependiendo del header `X-User-Roles: MS` que exigía el contrato original? | — | [[acuerdos/backoffice]] | |
| G10 | 🟢 | Accounting / Inventario | ¿Qué **número de grupo** tienen? ¿Inventario y Accounting son el mismo equipo? | — | [[acuerdos/accounting]], [[acuerdos/inventario]] | |
| G11 | 🟢 | Plataforma | ¿Qué **número de grupo** tiene el equipo de Gateway / Kafka? | — | [[acuerdos/plataforma-gateway-kafka]] | |
| G12 | 🟢 | Plataforma | ¿Los scopes H1 de Courses y `users.legajo.read` están emitidos en el registry del entorno de la demo? | — | [[acuerdos/plataforma-gateway-kafka]] | |
| G13 | 🟢 | Equipo UI-KIT | ¿Quién es dueño del **componente de grafo**? ¿#33 cubre el `nav-icon-sprite`? ¿El avatar `2xl` (#39) alcanza para el perfil? | 9, 10 | [[05-ui-kit]] | |

## 3. Del equipo (las resolvemos nosotros)

| # | Prio | Duda | Cómo se resuelve | Bloquea | Origen | Respuesta |
|---|---|---|---|---|---|---|
| E1 | 🟠 | **Error del ranking por grupo**: no está reproducido. El back no tiene ranking por grupo (solo por curso, y `/groups/{gid}/progress` aparte) | Reproducirlo en el entorno integrado con `ROADMAP_BY_GROUP_ENABLED=true` y anotar request y respuesta | C6 | [[07-correcciones-profes]] | |
| E2 | 🟠 | **HU-20/21**: tres criterios de insignia nunca se otorgan. ¿Se implementan o se quitan? | Decidir en la reunión del equipo (quitar es S, implementar es M) | Bloque 0 | [[02-pendientes]] | |
| E3 | 🟠 | **HU-45 / HU-49**: ¿se cierran en el Bloque 0 o pasan al sprint con alcance nuevo? HU-49 depende de P9 | Decidir junto con P9 | Bloque 0, C4 | [[02-pendientes]] | |
| E4 | 🟢 | **Curva PAR-09**: `V17` anota 600/1800/4200 para los niveles 3/5/7 y la curva de ejemplo de Backoffice da 1200/3500/7300. ¿Cuál está activa? | Leer PAR-09 del Backoffice en el entorno integrado | C8 (seed) | [[decisiones/DEC-006-insignias-sistema-y-curso\|DEC-006]] | |
| E5 | 🟢 | `fix/account-not-found-gate`: ¿se cierra como obsoleta por #193? ¿El 404 llega bien al front? | Probarlo en el entorno integrado | Bloque 0 | [[acuerdos/inventario]] | |
| E6 | 🟢 | `KAFKA_TOPIC_ROADMAP`: en `develop` el default es `roadmap.events`. ¿El compose de cada entorno lo pisa con otro valor? | Revisar `tpi-system-compose` | — | [[acuerdos/notificaciones-bus]] | |
| E7 | 🟢 | `TraceIdFilter` figura en `08-comunicacion-gateway.md` pero no está en `develop`. ¿Se borró a propósito? ¿El MDC de `logback-spring.xml` sigue vigente? | Revisar el historial de git del back | C10 | [[acuerdos/plataforma-gateway-kafka]] | |
| E8 | 🟢 | Accounting publica `LIVES_EXHAUSTED` / `LIVES_AVAILABLE` y no tenemos consumidor. ¿Hace falta? | Revisar contra el Gate (hoy lee vidas por REST) | — | [[acuerdos/accounting]] | |
| E9 | 🟢 | `ParUnavailableException`: ¿qué casos de uso la propagan con Backoffice caído (ej. el nivel del alumno)? | Revisar el código y documentarlo | — | [[acuerdos/backoffice]] | |

## Respondidas

| # | Duda | Respuesta | Fecha y fuente |
|---|---|---|---|
| — | ¿Exigen una BD de grafos como requisito? | Sí, Neo4j. Ver [[decisiones/DEC-016-neo4j-para-la-estructura-del-roadmap\|DEC-016]] | 2026-10-14, [[07-correcciones-profes\|correcciones]] |
| — | ¿Qué número de grupo tienen Backoffice y Users? | Backoffice = G06, Users = G07 | 2026-10-14, [[07-correcciones-profes\|correcciones]] |
