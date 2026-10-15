---
tags: [tpi, g10, sprint-3, historia, hu]
id: C05
tipo: HU
epica: "EP-S3-2"
capa: "Front"
esfuerzo: S
puntos: 2
prioridad: Should
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# C05: Obligatoriedad visible en la lista de nodos

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes|EP-S3-2]] · **HU** · Capa: **Front** · **2 pts** · **Should** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-xx — Obligatoriedad visible en la lista de nodos** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: PROFESOR
- **Quiero**: ver en la lista de nodos cuáles son obligatorios y de qué dependen
- **Para**: revisar el armado del curso sin abrir nodo por nodo

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Obligatorio = lectura obligatoria o requisito de otro nodo.
- [ ] Accesibilidad (WCAG/teclado/lectores): La marca de obligatorio tiene texto alternativo.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Marca de obligatorio en cada nodo que lo es.
- [ ] **CA2**: «Requiere: X, Y» por nodo.
- [ ] **CA3**: Con componentes del kit.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Obligatoriedad en la lista

**Escenario 1**

- **Dado**: un nodo de lectura obligatoria
- **Cuando**: el profesor ve la lista
- **Entonces**: tiene la marca «Obligatorio»

**Escenario 2**

- **Dado**: el nodo 3 requiere 1 y 2
- **Cuando**: el profesor ve la lista
- **Entonces**: dice «Requiere: 1, 2»

**Escenario 3**

- **Dado**: un nodo sin requisitos
- **Cuando**: el profesor ve la lista
- **Entonces**: no muestra «Requiere»

* * *

## Prototipo

- **Capturas**: `unit-node-list`.
- **URL Figma**: Pendiente.
- **Storybook**: `generic-badge`.
- **Mock API / Swagger**: Datos existentes del grafo.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 2
- **Prioridad (MoSCoW / Numérica)**: Should

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: `unit-node-list`.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Ninguno.

## Tareas

- [ ] T-C05.1 Marca y requisitos en la lista
- [ ] T-C05.2 Tests

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

`unit-node-list` muestra los nodos sin dependencias.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

Ninguna.
