---
tags: [tpi, g10, sprint-3, historia, hu]
id: M05
tipo: HU
epica: "EP-S3-1"
capa: "Back + Front"
esfuerzo: M
puntos: 5
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M02, M03]
---

# M05: Dependencias entre secciones

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HU** · Capa: **Back + Front** · **5 pts** · **Must** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-xx — Dependencias entre secciones** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: PROFESOR
- **Quiero**: definir de qué secciones depende cada sección (AND/OR), con un XP mínimo opcional y un atajo para «todas las anteriores»
- **Para**: armar el recorrido del curso como en el ejemplo de los profes

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Ya existen las dependencias AND/OR entre secciones (V25). Vuelve el XP mínimo por sección (se borró en V8, DEC-011). «Todas las anteriores» es un atajo de la UI que guarda un AND.
- [ ] Validaciones: No se puede guardar un ciclo. XP mínimo ≥ 0.
- [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño.
- [ ] Accesibilidad (WCAG/teclado/lectores): Selector de secciones usable con teclado.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Elegir las secciones requeridas y el modo AND/OR.
- [ ] **CA2**: XP mínimo opcional por sección.
- [ ] **CA3**: Atajo «todas las anteriores».
- [ ] **CA4**: Guardar un ciclo devuelve error.
- [ ] **CA5**: El alumno ve por qué una sección está bloqueada.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Dependencias entre secciones

**Escenario 1**

- **Dado**: las secciones 1 y 2
- **Cuando**: el profesor hace que la 3 dependa de ambas con AND
- **Entonces**: la 3 se desbloquea solo con 1 y 2 completas

**Escenario 2**

- **Dado**: la sección 4 depende de la 2 con XP ≥ 500
- **Cuando**: un alumno completa la 2 con 300 XP
- **Entonces**: la 4 sigue bloqueada y ve «te faltan 200 XP»

**Escenario 3**

- **Dado**: la sección 1 depende de la 3
- **Cuando**: el profesor hace que la 3 dependa de la 1
- **Entonces**: recibe error de ciclo

* * *

## Prototipo

- **Capturas**: Editor de reglas de sección.
- **URL Figma**: Pendiente.
- **Storybook**: `generic-select`, `generic-input`.
- **Mock API / Swagger**: PATCH /api/roadmap/sections/{sectionId}/rules.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 5
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: Reglas de sección, `GateEvaluator`, `rules-wizard`.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: XP mínimo en Neo4j (`Rule.minXp`).
- Riesgos y mitigación (opcional): Depende de M03 y P6.

## Tareas

- [ ] T-M05.1 XP mínimo y reglas en el módulo graph
- [ ] T-M05.2 Validación de ciclos
- [ ] T-M05.3 Editor de reglas de sección
- [ ] T-M05.4 Tests con el ejemplo de los profes

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

Ya existen las dependencias AND/OR entre secciones (V25). El XP mínimo por sección se borró en V8 (DEC-011).

### Depende de

- [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps|M02]] Modelo 1 a N de curso a roadmaps
- [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial|M03]] Módulo graph en Neo4j y migración inicial

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P6]]
