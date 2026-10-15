---
tags: [tpi, g10, sprint-3, historia, ht]
id: M11
tipo: HT
epica: "EP-S3-1"
capa: "Back"
esfuerzo: M
puntos: 5
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M02]
---

# M11: Contratos con Courses y el Motor para el modelo 1 a N

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HT** · Capa: **Back** · **5 pts** · **Must** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HT-xx — Contratos con Courses y el Motor para el modelo 1 a N** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: EQUIPO DE DESARROLLO
- **Quiero**: adaptar los contratos con Courses y con el Motor al modelo de varios roadmaps por curso
- **Para**: que las integraciones sigan funcionando cuando un curso tenga N roadmaps

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Hoy cada sección se sincroniza con una sección de Courses (HU-36) y el Motor manda `id_course` + `id_node`.
- [ ] Otros: Los acuerdos se registran en `acuerdos/` y los contratos en `tpi-roadmap/docs/contracts/`.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Acordado con G01 cómo se mapean sus secciones con N roadmaps (P3, G4).
- [ ] **CA2**: Confirmado con G09 que `node_id` alcanza (G8).
- [ ] **CA3**: Código y contratos actualizados.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Contratos para N roadmaps

**Escenario 1**

- **Dado**: un curso con 2 roadmaps
- **Cuando**: Courses publica una sección nueva
- **Entonces**: llega al roadmap acordado

**Escenario 2**

- **Dado**: un nodo del roadmap 2
- **Cuando**: el Motor manda el resultado con `id_node`
- **Entonces**: se registra en el roadmap correcto

**Escenario 3**

- **Dado**: el acuerdo con G01
- **Cuando**: se registra
- **Entonces**: queda en `acuerdos/courses-g01`

* * *

## Prototipo

- **Capturas**: No aplica (sin pantalla).
- **URL Figma**: No aplica.
- **Storybook**: No aplica.
- **Mock API / Swagger**: No aplica.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 5
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Courses, Motor.
- Módulos afectados: Sync de secciones, listener del Motor.
- Otros equipos / aprobaciones: G01, G09.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Que G01 tarde en acordar; mitigación: proponer el mapeo por escrito la primera semana.

## Tareas

- [ ] T-M11.1 Propuesta de mapeo a G01
- [ ] T-M11.2 Confirmación con G09
- [ ] T-M11.3 Código y contratos

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

Cada sección del roadmap se sincroniza con una sección de Courses (HU-36). El Motor manda `id_course` + `id_node`.

### Depende de

- [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps|M02]] Modelo 1 a N de curso a roadmaps

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P3]]
- [[sprints/sprint-3/08-dudas|G4]]
- [[sprints/sprint-3/08-dudas|G8]]
