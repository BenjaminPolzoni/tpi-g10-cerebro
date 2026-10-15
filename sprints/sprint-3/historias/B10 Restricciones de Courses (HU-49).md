---
tags: [tpi, g10, sprint-3, historia, hu]
id: B10
tipo: HU
epica: "EP-S3-0"
capa: "Back + Front"
esfuerzo: L
puntos: 8
prioridad: Should
estado: Propuesta
responsable: ""
taiga: "HU-49"
depende: [C04]
---

# B10: Restricciones de Courses (HU-49)

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HU** · Capa: **Back + Front** · **8 pts** · **Should** · Taiga: [[taiga/historias/HU-49 Aplicar en el roadmap las restricciones de sección y actividad que publica Courses|HU-49]]
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-49 — Restricciones de Courses (HU-49)**

* * *

## Descripción (Como / Quiero / Para)

- **Como**: ALUMNO
- **Quiero**: saber por qué un nodo está oculto o bloqueado por fecha, y que se actualice cuando Courses cambia la restricción
- **Para**: no perderme una actividad habilitada ni intentar una que todavía no lo está

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Courses publica restricciones por sección y actividad. HIDDEN: el alumno no ve el nodo. LOCKED: lo ve bloqueado con la fecha. El gate ya evalúa `DATE_RESTRICTED`.
- [ ] Validaciones: Si llega un evento de cambio, se invalida la caché de restricciones del curso.
- [ ] Accesibilidad (WCAG/teclado/lectores): La fecha de habilitación en texto, no solo con un ícono.
- [ ] Otros: Depende de G01 (evento de cambio) y de la respuesta a P9 sobre quién define la ventana.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Un nodo HIDDEN no aparece al alumno.
- [ ] **CA2**: Un nodo LOCKED aparece bloqueado con su fecha de habilitación.
- [ ] **CA3**: Al llegar el evento de cambio de Courses, el estado se actualiza.
- [ ] **CA4**: El front muestra el aviso con la fecha.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Restricciones de Courses

**Escenario 1**

- **Dado**: un nodo con restricción HIDDEN
- **Cuando**: el alumno abre el roadmap
- **Entonces**: no lo ve

**Escenario 2**

- **Dado**: un nodo LOCKED hasta el 20/10
- **Cuando**: el alumno lo abre el 18/10
- **Entonces**: lo ve bloqueado con «se habilita el 20/10»

**Escenario 3**

- **Dado**: Courses cambia la fecha de un nodo
- **Cuando**: llega el evento
- **Entonces**: el roadmap muestra la fecha nueva

* * *

## Prototipo

- **Capturas**: Nodo bloqueado por fecha en el mapa.
- **URL Figma**: Pendiente.
- **Storybook**: `generic-badge` para el estado.
- **Mock API / Swagger**: Restricciones de Courses (`course.restrictions.read`) y evento de cambio a acordar.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 8
- **Prioridad (MoSCoW / Numérica)**: Should

* * *

## Dependencias / Impactos

- Servicios involucrados: Courses (restricciones y evento).
- Módulos afectados: `CourseRestrictionsClient`, `GateEvaluator`, mapa del alumno.
- Otros equipos / aprobaciones: G01 (bloqueante para el evento).
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Que G01 no publique el evento a tiempo; mitigación: leer por pull con caché corta.

## Tareas

- [ ] T-B10.1 HIDDEN vs LOCKED en el back
- [ ] T-B10.2 Consumir el evento de cambio de restricción
- [ ] T-B10.3 Front: oculto, bloqueado y aviso con fecha
- [ ] T-B10.4 Tests y acta con G01

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

El gate aplica la restricción por fecha. Falta distinguir oculto (HIDDEN) de bloqueado (LOCKED), consumir el evento de cambio y avisar. El front no tiene nada. Depende de G01.

### Depende de

- [[sprints/sprint-3/historias/C04 Nodo examen con ventana horaria|C04]] Nodo examen con ventana horaria

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P9]]
- [[sprints/sprint-3/08-dudas|G4]]
