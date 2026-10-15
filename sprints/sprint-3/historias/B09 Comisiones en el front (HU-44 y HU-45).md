---
tags: [tpi, g10, sprint-3, historia, hu]
id: B09
tipo: HU
epica: "EP-S3-0"
capa: "Front (+ Back)"
esfuerzo: L
puntos: 8
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "HU-44, HU-45"
depende: [B02]
---

# B09: Comisiones en el front (HU-44 y HU-45)

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HU** · Capa: **Front (+ Back)** · **8 pts** · **Must** · Taiga: [[taiga/historias/HU-44 Ver el roadmap de cada una de mis comisiones|HU-44]], [[taiga/historias/HU-45 Ranking de la cohorte y avance por comisión|HU-45]]
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-44, HU-45 — Comisiones en el front (HU-44 y HU-45)**

* * *

## Descripción (Como / Quiero / Para)

- **Como**: ALUMNO / PROFESOR
- **Quiero**: ver el roadmap de cada una de mis comisiones y, como profesor, el avance por comisión
- **Para**: seguir el curso según la comisión en la que estoy o que tengo a cargo

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: El back ya filtra por comisión detrás de `ROADMAP_BY_GROUP_ENABLED` (modelo B, DEC-014). El motivo `group_restricted` se muestra en texto.
- [ ] Seguridad (roles, permisos, datos sensibles): El alumno solo ve sus comisiones. El avance por comisión: ADMIN o PROFESSOR.
- [ ] Accesibilidad (WCAG/teclado/lectores): Selector accesible con teclado (`generic-select`).

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Selector de comisión en el roadmap del alumno cuando tiene más de una.
- [ ] **CA2**: El motivo `group_restricted` se muestra con un texto claro.
- [ ] **CA3**: El profesor ve el avance por comisión.
- [ ] **CA4**: HU-44 y HU-45 cumplen sus CA en Taiga.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Comisiones en el front

**Escenario 1**

- **Dado**: un alumno en las comisiones 2w1 y 2w2
- **Cuando**: abre el roadmap
- **Entonces**: elige la comisión y ve su roadmap

**Escenario 2**

- **Dado**: un nodo restringido a otra comisión
- **Cuando**: el alumno lo abre
- **Entonces**: ve el motivo `group_restricted` en texto

**Escenario 3**

- **Dado**: un profesor del curso
- **Cuando**: abre el avance por comisión
- **Entonces**: ve el progreso de cada comisión

* * *

## Prototipo

- **Capturas**: Roadmap del alumno con selector; panel del profesor.
- **URL Figma**: Pendiente.
- **Storybook**: `generic-select`, `generic-table`.
- **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/groups/{groupId}/progress.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 8
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Courses (comisiones).
- Módulos afectados: Roadmap del alumno, panel del profesor, `GroupSelectionService`.
- Otros equipos / aprobaciones: G01.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Depende de B02 (flag) y de que Courses tenga las comisiones cargadas en la demo.

## Tareas

- [ ] T-B09.1 Selector de comisión
- [ ] T-B09.2 Texto para `group_restricted`
- [ ] T-B09.3 Avance por comisión del profesor
- [ ] T-B09.4 Tests y actualizar HU-44/45 en Taiga

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

El back está hecho detrás de `ROADMAP_BY_GROUP_ENABLED`. El front no tiene selector de comisión ni vista de avance por comisión. HU-45 sigue en New.

### Depende de

- [[sprints/sprint-3/historias/B02 Encender los flags en los entornos|B02]] Encender los flags en los entornos

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P5]]
