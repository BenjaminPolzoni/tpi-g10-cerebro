---
tags: [tpi, g10, sprint-3, historia, hu]
id: M04
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

# M04: Habilitar y gestionar varios roadmaps por curso

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HU** · Capa: **Back + Front** · **5 pts** · **Should** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-xx — Habilitar y gestionar varios roadmaps por curso** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: GESTOR / PROFESOR
- **Quiero**: habilitar varios roadmaps en un curso y crearlos, renombrarlos y archivarlos
- **Para**: organizar el curso en recorridos distintos

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Flag por curso `multiple_roadmaps_allowed`. Con el flag apagado no se puede crear un segundo roadmap. Archivar es baja lógica y conserva el progreso.
- [ ] Validaciones: Nombre obligatorio y único dentro del curso.
- [ ] Seguridad (roles, permisos, datos sensibles): GESTOR, ADMIN o PROFESSOR dueño del curso.
- [ ] Accesibilidad (WCAG/teclado/lectores): Pantalla con componentes del kit.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: El profesor dueño o el gestor activa varios roadmaps en un curso.
- [ ] **CA2**: Con el flag apagado, crear un segundo roadmap devuelve 409.
- [ ] **CA3**: Crear, renombrar y archivar un roadmap.
- [ ] **CA4**: Archivar no borra el progreso de los alumnos.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Varios roadmaps por curso

**Escenario 1**

- **Dado**: un curso con el flag apagado
- **Cuando**: el profesor intenta crear un segundo roadmap
- **Entonces**: recibe un error claro

**Escenario 2**

- **Dado**: un curso con el flag encendido
- **Cuando**: el profesor crea «Roadmap práctico»
- **Entonces**: aparece en la lista del curso

**Escenario 3**

- **Dado**: un roadmap con alumnos avanzados
- **Cuando**: el profesor lo archiva
- **Entonces**: deja de verse y el progreso se conserva

* * *

## Prototipo

- **Capturas**: Lista de roadmaps del curso.
- **URL Figma**: Pendiente.
- **Storybook**: `generic-table`, `generic-modal`.
- **Mock API / Swagger**: POST/PATCH /api/roadmap/courses/{courseId}/roadmaps.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 5
- **Prioridad (MoSCoW / Numérica)**: Should

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: Controller y servicio de roadmaps, pantalla del profesor.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Columna `multiple_roadmaps_allowed`.
- Riesgos y mitigación (opcional): Depende de P1.

## Tareas

- [ ] T-M04.1 Flag por curso
- [ ] T-M04.2 ABM de roadmaps
- [ ] T-M04.3 Pantalla del profesor
- [ ] T-M04.4 Tests

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

Un curso tiene un único roadmap.

### Depende de

- [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps|M02]] Modelo 1 a N de curso a roadmaps

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P1]]
