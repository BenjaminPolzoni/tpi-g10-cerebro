---
tags: [tpi, g10, sprint-3, historia, hu]
id: C03
tipo: HU
epica: "EP-S3-2"
capa: "Front"
esfuerzo: L
puntos: 8
prioridad: Should
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M09, C02]
---

# C03: Editor con arrastre y el curso como mapa

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes|EP-S3-2]] · **HU** · Capa: **Front** · **8 pts** · **Should** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-xx — Editor con arrastre y el curso como mapa** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: PROFESOR
- **Quiero**: arrastrar nodos, crear relaciones arrastrando y ver el curso como un mapa
- **Para**: editar el curso de forma visual, como en Google Maps

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Las posiciones se guardan. Al crear una relación se elige su tipo (C02). Cómo se ve «el curso como mapa» depende de P1.
- [ ] Accesibilidad (WCAG/teclado/lectores): Alternativa con teclado para mover y relacionar.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Arrastrar nodos y guardar su posición.
- [ ] **CA2**: Crear una relación arrastrando y eligiendo su tipo.
- [ ] **CA3**: El editor muestra el curso como mapa según P1.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Editor como mapa

**Escenario 1**

- **Dado**: el editor abierto
- **Cuando**: el profesor arrastra un nodo
- **Entonces**: la posición se guarda

**Escenario 2**

- **Dado**: dos nodos
- **Cuando**: arrastra de uno al otro y elige `REQUIRES`
- **Entonces**: se crea la relación

**Escenario 3**

- **Dado**: un curso completo
- **Cuando**: el profesor abre el editor
- **Entonces**: lo ve como un mapa navegable

* * *

## Prototipo

- **Capturas**: Editor del curso.
- **URL Figma**: Pendiente.
- **Storybook**: `generic-node-graph`.
- **Mock API / Swagger**: Endpoints de M09 y C02.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 8
- **Prioridad (MoSCoW / Numérica)**: Should

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: `course-editor-page`, vista de grafo.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Depende de M09, C02 y P1.

## Tareas

- [ ] T-C03.1 Arrastre en el editor
- [ ] T-C03.2 Crear relación con tipo
- [ ] T-C03.3 Vista de mapa

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

`course-editor-page` es una vista tipo Moodle. Las posiciones no se guardan.

### Depende de

- [[sprints/sprint-3/historias/M09 Vista de grafo cómoda para el profesor|M09]] Vista de grafo cómoda para el profesor
- [[sprints/sprint-3/historias/C02 Relaciones con tipo|C02]] Relaciones con tipo

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P1]]
