---
tags: [tpi, g10, sprint-3, historia, hu]
id: M08
tipo: HU
epica: "EP-S3-1"
capa: "Back + Front"
esfuerzo: M
puntos: 5
prioridad: Should
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M02]
---

# M08: El alumno elige qué roadmap recorrer

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HU** · Capa: **Back + Front** · **5 pts** · **Should** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-xx — El alumno elige qué roadmap recorrer** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: ALUMNO
- **Quiero**: elegir qué roadmap del curso recorrer y ver mi progreso en cada uno
- **Para**: seguir el recorrido que me corresponde

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Qué roadmaps ve el alumno depende de P5 (todos o por comisión). XP, nivel y ranking según P2.
- [ ] Seguridad (roles, permisos, datos sensibles): Solo roadmaps no archivados del curso donde está matriculado.
- [ ] Accesibilidad (WCAG/teclado/lectores): Selector accesible.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Si el curso tiene varios roadmaps visibles, el alumno elige uno.
- [ ] **CA2**: El progreso de cada roadmap se ve por separado.
- [ ] **CA3**: XP, nivel y ranking se muestran según P2.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Elegir roadmap

**Escenario 1**

- **Dado**: un curso con 2 roadmaps visibles
- **Cuando**: el alumno abre el curso
- **Entonces**: elige cuál recorrer

**Escenario 2**

- **Dado**: un alumno con avance en ambos
- **Cuando**: cambia de roadmap
- **Entonces**: ve el progreso de cada uno

**Escenario 3**

- **Dado**: un roadmap archivado
- **Cuando**: el alumno abre el curso
- **Entonces**: no aparece

* * *

## Prototipo

- **Capturas**: Selector de roadmap del alumno.
- **URL Figma**: Pendiente.
- **Storybook**: `generic-segmented` o `generic-select`.
- **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/roadmaps.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 5
- **Prioridad (MoSCoW / Numérica)**: Should

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: Roadmap del alumno, `RoadmapStore`.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Depende de P1, P2 y P5.

## Tareas

- [ ] T-M08.1 Endpoint de roadmaps visibles
- [ ] T-M08.2 Selector en el front
- [ ] T-M08.3 Tests

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

El alumno ve un único roadmap por curso.

### Depende de

- [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps|M02]] Modelo 1 a N de curso a roadmaps

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P1]]
- [[sprints/sprint-3/08-dudas|P2]]
- [[sprints/sprint-3/08-dudas|P5]]
