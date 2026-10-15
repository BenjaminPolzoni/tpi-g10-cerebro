---
tags: [tpi, g10, sprint-3, historia, hu]
id: C07
tipo: HU
epica: "EP-S3-2"
capa: "Front (3D)"
esfuerzo: M
puntos: 5
prioridad: Could
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# C07: Archibaldo: Enter, aspecto de Hernán y destello

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes|EP-S3-2]] · **HU** · Capa: **Front (3D)** · **5 pts** · **Could** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-xx — Archibaldo: Enter, aspecto de Hernán y destello** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: ALUMNO
- **Quiero**: hablar con Archibaldo con Enter, que tenga el aspecto de Hernán y que un destello me guíe por el camino
- **Para**: moverme por el mundo sin depender del mouse y saber a dónde ir

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Enter abre el diálogo solo con el NPC en rango. El destello marca el camino al próximo nodo disponible.
- [ ] Performance (tiempos, volumen, límites): El destello no baja los FPS del mundo.
- [ ] Accesibilidad (WCAG/teclado/lectores): El diálogo toma el foco y se cierra con Escape (`generic-modal`).
- [ ] Otros: Modelo o skin de Hernán según la referencia de los profes (P11).

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Enter abre el diálogo con el NPC en rango.
- [ ] **CA2**: El foco queda en el diálogo y Escape lo cierra.
- [ ] **CA3**: Archibaldo con el aspecto de Hernán.
- [ ] **CA4**: Destello sobre el camino al próximo nodo disponible.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Archibaldo y guía

**Escenario 1**

- **Dado**: el alumno junto a Archibaldo
- **Cuando**: presiona Enter
- **Entonces**: se abre el diálogo con el foco adentro

**Escenario 2**

- **Dado**: el alumno lejos de Archibaldo
- **Cuando**: presiona Enter
- **Entonces**: no pasa nada

**Escenario 3**

- **Dado**: un nodo disponible
- **Cuando**: el alumno está en el mundo
- **Entonces**: un destello marca el camino hacia él

* * *

## Prototipo

- **Capturas**: Mundo 3D con Archibaldo.
- **URL Figma**: No aplica.
- **Storybook**: `generic-modal`.
- **Mock API / Swagger**: No aplica.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 5
- **Prioridad (MoSCoW / Numérica)**: Could

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: `world-3d.service`, `archipelago-3d.service`, `npc-dialogue`.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Depende de P11 para el aspecto.

## Tareas

- [ ] T-C07.1 Interacción con Enter y foco
- [ ] T-C07.2 Modelo de Hernán
- [ ] T-C07.3 Destello del camino

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

El NPC usa la skin del capitán pirata del kit (`world-3d.service.ts:3109`). El diálogo se abre con clic. No hay destello.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P11]]
