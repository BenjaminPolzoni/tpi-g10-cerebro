---
tags: [tpi, g10, sprint-3, historia, hu]
id: C04
tipo: HU
epica: "EP-S3-2"
capa: "Back + Front"
esfuerzo: M
puntos: 5
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# C04: Nodo examen con ventana horaria

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes|EP-S3-2]] · **HU** · Capa: **Back + Front** · **5 pts** · **Must** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-xx — Nodo examen con ventana horaria** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: PROFESOR
- **Quiero**: habilitar un nodo examen (parcial) solo dentro de una ventana horaria
- **Para**: tomar parciales en el horario de la clase

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Campos `available_from` y `available_until` en nodos `EXAM`. Fuera de la ventana el gate responde `DATE_RESTRICTED`. Si Courses también define una ventana, gana lo que diga P9.
- [ ] Validaciones: `available_from` < `available_until`.
- [ ] Accesibilidad (WCAG/teclado/lectores): El alumno ve en texto cuándo se habilita.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Ventana horaria en nodos examen.
- [ ] **CA2**: Fuera de la ventana el gate bloquea con `DATE_RESTRICTED`.
- [ ] **CA3**: El alumno ve cuándo se habilita.
- [ ] **CA4**: Tests con hora simulada.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Examen por hora

**Escenario 1**

- **Dado**: un examen habilitado de 18:00 a 20:00
- **Cuando**: el alumno entra a las 17:59
- **Entonces**: el gate responde `DATE_RESTRICTED`

**Escenario 2**

- **Dado**: el mismo examen
- **Cuando**: el alumno entra a las 18:30
- **Entonces**: puede rendir

**Escenario 3**

- **Dado**: el mismo examen
- **Cuando**: el alumno lo mira antes de hora
- **Entonces**: ve «se habilita a las 18:00»

* * *

## Prototipo

- **Capturas**: Nodo examen bloqueado por hora.
- **URL Figma**: Pendiente.
- **Storybook**: Pendiente.
- **Mock API / Swagger**: PATCH /api/roadmap/nodes/{nodeId}/availability.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 5
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Courses (si también define ventanas).
- Módulos afectados: `GateEvaluator`, editor de nodo, mapa del alumno.
- Otros equipos / aprobaciones: G01 (según P9).
- Impacto en datos / migraciones: Columnas o props de ventana.
- Riesgos y mitigación (opcional): Zonas horarias; mitigación: guardar en UTC y mostrar en la del curso.

## Tareas

- [ ] T-C04.1 Ventana en el nodo
- [ ] T-C04.2 Evaluación en el gate
- [ ] T-C04.3 Front: aviso al alumno
- [ ] T-C04.4 Tests con reloj simulado

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

El gate evalúa `DATE_RESTRICTED` con ventanas que publica Courses (HU-49). El nodo no tiene ventana propia.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P9]]
