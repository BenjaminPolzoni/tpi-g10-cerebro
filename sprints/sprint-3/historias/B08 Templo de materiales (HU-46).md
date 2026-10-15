---
tags: [tpi, g10, sprint-3, historia, hu]
id: B08
tipo: HU
epica: "EP-S3-0"
capa: "Front"
esfuerzo: M
puntos: 5
prioridad: Should
estado: Propuesta
responsable: ""
taiga: "HU-46"
depende: []
---

# B08: Templo de materiales (HU-46)

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HU** · Capa: **Front** · **5 pts** · **Should** · Taiga: [[taiga/historias/HU-46 Ver en los nodos y en el Templo el material teórico de Courses|HU-46]]
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-46 — Templo de materiales (HU-46)**

* * *

## Descripción (Como / Quiero / Para)

- **Como**: ALUMNO
- **Quiero**: ver en el Templo todo el material teórico de mi curso agrupado por unidad
- **Para**: repasar sin recorrer el mapa nodo por nodo

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: El material lo guarda Courses en Garage y Roadmap lo pide (D-03); Roadmap no guarda archivos. En una unidad bloqueada el material se lista pero no se puede abrir.
- [ ] Seguridad (roles, permisos, datos sensibles): Solo el alumno matriculado.
- [ ] Accesibilidad (WCAG/teclado/lectores): Lista navegable con teclado; los ítems bloqueados indican el motivo en texto.
- [ ] Otros: Si el PO prefiere no rehacerlo, se redefine el criterio de aceptación de HU-46 en Taiga (P13).

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Página Templo (`/student/materials`) con el material agrupado por unidad.
- [ ] **CA2**: En una unidad bloqueada el material aparece sin poder abrirse.
- [ ] **CA3**: Abrir un material desbloqueado lo muestra en el visor.
- [ ] **CA4**: O el CA de HU-46 queda redefinido en Taiga.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Templo de materiales

**Escenario 1**

- **Dado**: un alumno con 2 unidades desbloqueadas
- **Cuando**: abre el Templo
- **Entonces**: ve el material de ambas agrupado por unidad

**Escenario 2**

- **Dado**: una unidad bloqueada
- **Cuando**: el alumno la mira en el Templo
- **Entonces**: ve el material listado sin poder abrirlo

**Escenario 3**

- **Dado**: un material desbloqueado
- **Cuando**: lo abre
- **Entonces**: se muestra en el visor

* * *

## Prototipo

- **Capturas**: Templo del mundo (antes `materials-page`).
- **URL Figma**: Pendiente.
- **Storybook**: `generic-course-outline`.
- **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/materials.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 5
- **Prioridad (MoSCoW / Numérica)**: Should

* * *

## Dependencias / Impactos

- Servicios involucrados: Courses (material en Garage).
- Módulos afectados: Página Templo (front), `UnitMaterialService`.
- Otros equipos / aprobaciones: G01 (URLs del material).
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Que el PO no lo quiera; mitigación: preguntar antes (P13).

## Tareas

- [ ] T-B08.1 Confirmar con el PO (P13)
- [ ] T-B08.2 Página Templo con la UI-KIT
- [ ] T-B08.3 Estados bloqueado y desbloqueado
- [ ] T-B08.4 Tests

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

Se borró la página Templo (`student/materials`). El material de los nodos sí se ve.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P13]]
