---
tags: [tpi, g10, sprint-3, historia, hu]
id: M10
tipo: HU
epica: "EP-S3-1"
capa: "Front"
esfuerzo: L
puntos: 8
prioridad: Should
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [U01, U02]
---

# M10: Vista tipo Moodle con la UI-KIT

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HU** · Capa: **Front** · **8 pts** · **Should** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-xx — Vista tipo Moodle con la UI-KIT** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: PROFESOR
- **Quiero**: una vista de lista tipo Moodle cómoda y sincronizada con la vista de grafo
- **Para**: editar el curso en el formato que conozco

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Las dos vistas editan el mismo roadmap.
- [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño.
- [ ] Accesibilidad (WCAG/teclado/lectores): Reordenar también con teclado, no solo con drag-drop.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: `course-editor-page` refactorizada con componentes del kit.
- [ ] **CA2**: Un cambio en una vista se ve en la otra sin recargar.
- [ ] **CA3**: Reordenar secciones y nodos con drag-drop y con teclado.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Vista tipo Moodle

**Escenario 1**

- **Dado**: el profesor renombra una sección en la lista
- **Cuando**: cambia a la vista de grafo
- **Entonces**: ve el nombre nuevo

**Escenario 2**

- **Dado**: una lista de secciones
- **Cuando**: el profesor arrastra la 3 arriba de la 2
- **Entonces**: el orden se guarda

**Escenario 3**

- **Dado**: un profesor con teclado
- **Cuando**: reordena con las flechas
- **Entonces**: el orden se guarda

* * *

## Prototipo

- **Capturas**: `course-editor-page`.
- **URL Figma**: Pendiente.
- **Storybook**: `generic-course-outline`, `generic-disclosure`.
- **Mock API / Swagger**: Endpoints existentes de secciones y nodos.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 8
- **Prioridad (MoSCoW / Numérica)**: Should

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: `course-editor-page`, `section-reorder-list`.
- Otros equipos / aprobaciones: Equipo UI-KIT (lista reordenable).
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Depende de U01 y U02.

## Tareas

- [ ] T-M10.1 Refactor con el kit
- [ ] T-M10.2 Sincronización con la vista de grafo
- [ ] T-M10.3 Reordenar accesible

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

Existe `course-editor-page` con controles propios.

### Depende de

- [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs|U01]] Subir la UI-KIT a 0.8.0 y cerrar sus TODOs
- [[sprints/sprint-3/historias/U02 Controles y botones del roadmap con el kit|U02]] Controles y botones del roadmap con el kit

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P1]]
