---
tags: [tpi, g10, sprint-3, historia, ht]
id: M02
tipo: HT
epica: "EP-S3-1"
capa: "Back"
esfuerzo: L
puntos: 8
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M01]
---

# M02: Modelo 1 a N de curso a roadmaps

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HT** · Capa: **Back** · **8 pts** · **Must** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HT-xx — Modelo 1 a N de curso a roadmaps** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: EQUIPO DE DESARROLLO
- **Quiero**: que un curso pueda tener varios roadmaps sin romper las rutas ni los datos actuales
- **Para**: habilitar el pedido de los profes sin una migración a ciegas

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Se quita el UNIQUE de `roadmap.course_cohort_id`. Las rutas `/courses/{id}/...` siguen funcionando contra el roadmap principal del curso mientras el front migra a `/roadmaps/{id}/...`. Dónde viven XP, vidas, nivel y ranking lo define P2.
- [ ] Validaciones: Un curso sin roadmaps devuelve 404 claro; con varios, las rutas viejas usan el principal.
- [ ] Seguridad (roles, permisos, datos sensibles): Mismas reglas de autorización que hoy.
- [ ] Otros: Bloqueado por P1 (si "el mapa es el curso" descarta N roadmaps, esta HT se achica).

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Migración que quita el UNIQUE y marca un roadmap principal por curso.
- [ ] **CA2**: Rutas y DTOs con `roadmap_id`.
- [ ] **CA3**: Las rutas `/courses/{id}/...` siguen respondiendo igual.
- [ ] **CA4**: XP, vidas, nivel y ranking según P2.
- [ ] **CA5**: Todos los tests existentes pasan.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Modelo 1 a N

**Escenario 1**

- **Dado**: un curso con un roadmap
- **Cuando**: el front llama a `/courses/{id}/progress`
- **Entonces**: responde igual que antes

**Escenario 2**

- **Dado**: un curso con 2 roadmaps
- **Cuando**: se pide `/roadmaps/{id}/progress` de cada uno
- **Entonces**: cada uno devuelve su progreso

**Escenario 3**

- **Dado**: un curso con 2 roadmaps
- **Cuando**: se llama a la ruta vieja
- **Entonces**: responde con el roadmap principal

* * *

## Prototipo

- **Capturas**: No aplica.
- **URL Figma**: No aplica.
- **Storybook**: No aplica.
- **Mock API / Swagger**: Rutas nuevas `/api/roadmap/roadmaps/{roadmapId}/...` en el OpenAPI.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 8
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno nuevo.
- Módulos afectados: Entidades, repositorios, controllers y DTOs de roadmap, progreso, ranking y nivel.
- Otros equipos / aprobaciones: Front (migración de rutas).
- Impacto en datos / migraciones: Migración: quitar UNIQUE, columna `is_primary`.
- Riesgos y mitigación (opcional): Regresiones en todo el front; mitigación: mantener las rutas viejas hasta que el front migre.

## Tareas

- [ ] T-M02.1 Migración y entidades
- [ ] T-M02.2 Rutas `/roadmaps/{id}` y compatibilidad
- [ ] T-M02.3 XP, nivel y ranking según P2
- [ ] T-M02.4 Tests de regresión

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

`roadmap.course_cohort_id` es UNIQUE (V1/V12) y todas las rutas son `/courses/{id}/...`. XP, vidas, nivel y ranking dependen de `student_course`, por curso.

### Depende de

- [[sprints/sprint-3/historias/M01 Validar la infra de Neo4j y modelar las relaciones|M01]] Validar la infra de Neo4j y modelar las relaciones

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P1]]
- [[sprints/sprint-3/08-dudas|P2]]
- [[sprints/sprint-3/08-dudas|P3]]
