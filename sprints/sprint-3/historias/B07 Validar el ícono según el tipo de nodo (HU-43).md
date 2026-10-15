---
tags: [tpi, g10, sprint-3, historia, hu]
id: B07
tipo: HU
epica: "EP-S3-0"
capa: "Back"
esfuerzo: S
puntos: 1
prioridad: Could
estado: Propuesta
responsable: ""
taiga: "HU-43"
depende: []
---

# B07: Validar el ícono según el tipo de nodo (HU-43)

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HU** · Capa: **Back** · **1 pts** · **Could** · Taiga: [[taiga/historias/HU-43 Elegir el ícono de un desafío|HU-43]]
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-43 — Validar el ícono según el tipo de nodo (HU-43)**

* * *

## Descripción (Como / Quiero / Para)

- **Como**: PROFESOR
- **Quiero**: que el ícono de desafío solo se pueda asignar a nodos de desafío o examen
- **Para**: que el roadmap no muestre íconos que confundan al alumno

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: El ícono de desafío aplica a `THEORETICAL_CHALLENGE`, `PRACTICAL_CHALLENGE` y `EXAM`.
- [ ] Validaciones: En otro tipo de nodo, 400 con un mensaje claro.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Asignar el ícono a un nodo `CONTENT` o `UNIT` devuelve 400.
- [ ] **CA2**: Asignarlo a un desafío o examen funciona como hoy.
- [ ] **CA3**: Un test por tipo de nodo.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Ícono según el tipo de nodo

**Escenario 1**

- **Dado**: un nodo de contenido
- **Cuando**: el profesor le asigna el ícono de desafío
- **Entonces**: recibe 400 con el motivo

**Escenario 2**

- **Dado**: un nodo de desafío práctico
- **Cuando**: le asigna el ícono
- **Entonces**: se guarda

**Escenario 3**

- **Dado**: un nodo examen
- **Cuando**: le asigna el ícono
- **Entonces**: se guarda

* * *

## Prototipo

- **Capturas**: No aplica (sin pantalla).
- **URL Figma**: No aplica.
- **Storybook**: No aplica.
- **Mock API / Swagger**: No aplica.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 1
- **Prioridad (MoSCoW / Numérica)**: Could

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: Validación de nodos en `GraphController`/servicio de nodos.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Ninguno.

## Tareas

- [ ] T-B07.1 Validación del ícono por tipo de nodo
- [ ] T-B07.2 Tests por tipo

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

El back acepta el ícono en cualquier tipo de nodo.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

Ninguna.
