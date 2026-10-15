---
tags: [tpi, g10, sprint-3, historia, hu]
id: C01
tipo: HU
epica: "EP-S3-2"
capa: "Back + Front"
esfuerzo: M
puntos: 5
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M03]
---

# C01: Nodos de inicio y fin obligatorios

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes|EP-S3-2]] · **HU** · Capa: **Back + Front** · **5 pts** · **Must** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-xx — Nodos de inicio y fin obligatorios** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: PROFESOR
- **Quiero**: que el roadmap tenga siempre un nodo de inicio «Bienvenidos» y uno de fin «Felicitaciones», y que no se pueda guardar sin ellos
- **Para**: que el alumno sepa dónde empieza y dónde termina el curso

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Exactamente un `START` y un `END` por roadmap. Todo nodo alcanzable desde `START` y `END` alcanzable. Un roadmap nuevo nace con los dos.
- [ ] Validaciones: Al guardar, si falta alguno o hay nodos sueltos, error con la lista de problemas.
- [ ] Accesibilidad (WCAG/teclado/lectores): El visual de inicio y fin tiene texto, no solo un ícono.
- [ ] Otros: Llegar a `END` puede otorgar una insignia de fin de curso (HU-21).

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Tipos de nodo `START` y `END`.
- [ ] **CA2**: Un roadmap nuevo se crea con los dos.
- [ ] **CA3**: No se puede guardar sin uno de cada uno ni con nodos inalcanzables.
- [ ] **CA4**: Visual propio en el mapa 2D y en el mundo 3D.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Inicio y fin obligatorios

**Escenario 1**

- **Dado**: un roadmap nuevo
- **Cuando**: el profesor lo crea
- **Entonces**: ya tiene «Bienvenidos» y «Felicitaciones»

**Escenario 2**

- **Dado**: un roadmap sin `END`
- **Cuando**: el profesor guarda
- **Entonces**: recibe error «falta el nodo final»

**Escenario 3**

- **Dado**: un nodo sin camino desde `START`
- **Cuando**: el profesor guarda
- **Entonces**: recibe error que nombra ese nodo

* * *

## Prototipo

- **Capturas**: Mapa 2D y mundo 3D con inicio y fin.
- **URL Figma**: Pendiente.
- **Storybook**: Pendiente.
- **Mock API / Swagger**: Validación en el guardado del grafo.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 5
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: Módulo graph (validación), mapa 2D, mundo 3D.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Migración: agregar START y END a los roadmaps existentes.
- Riesgos y mitigación (opcional): Roadmaps existentes inválidos; mitigación: la migración los completa.

## Tareas

- [ ] T-C01.1 Tipos START/END y validación al guardar
- [ ] T-C01.2 Migración de roadmaps existentes
- [ ] T-C01.3 Visual en 2D y 3D
- [ ] T-C01.4 Tests

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

`NodeType` tiene `UNIT`, `CONTENT`, `THEORETICAL_CHALLENGE`, `PRACTICAL_CHALLENGE` y `EXAM`. No existen START ni END.

### Depende de

- [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial|M03]] Módulo graph en Neo4j y migración inicial

### Dudas que la frenan

Ninguna.
