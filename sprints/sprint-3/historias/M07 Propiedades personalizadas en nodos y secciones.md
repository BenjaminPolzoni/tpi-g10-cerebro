---
tags: [tpi, g10, sprint-3, historia, hu]
id: M07
tipo: HU
epica: "EP-S3-1"
capa: "Back + Front"
esfuerzo: M
puntos: 3
prioridad: Could
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M03]
---

# M07: Propiedades personalizadas en nodos y secciones

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HU** · Capa: **Back + Front** · **3 pts** · **Could** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-xx — Propiedades personalizadas en nodos y secciones** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: PROFESOR
- **Quiero**: agregar datos propios (clave y valor) a nodos y secciones
- **Para**: personalizar el roadmap sin pedir cambios de código

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Las propiedades libres no pisan los campos fijos que usa el dominio (tipo, vidas, reglas). Qué tan libre es depende de P8.
- [ ] Validaciones: Claves únicas por nodo; tamaño máximo por valor.
- [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño.
- [ ] Accesibilidad (WCAG/teclado/lectores): Lista de pares editable con teclado.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Agregar, editar y borrar propiedades en un nodo o sección.
- [ ] **CA2**: Se muestran en el detalle del nodo.
- [ ] **CA3**: Una clave reservada devuelve error.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Propiedades personalizadas

**Escenario 1**

- **Dado**: un nodo
- **Cuando**: el profesor agrega «dificultad: alta»
- **Entonces**: el alumno la ve en el detalle

**Escenario 2**

- **Dado**: un nodo con una propiedad
- **Cuando**: el profesor la borra
- **Entonces**: deja de mostrarse

**Escenario 3**

- **Dado**: la clave reservada `type`
- **Cuando**: el profesor la usa
- **Entonces**: recibe error

* * *

## Prototipo

- **Capturas**: Panel de propiedades del nodo.
- **URL Figma**: Pendiente.
- **Storybook**: `generic-input`.
- **Mock API / Swagger**: PATCH /api/roadmap/nodes/{nodeId} con `props`.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 3
- **Prioridad (MoSCoW / Numérica)**: Could

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: Módulo graph, editor de nodo, detalle de nodo.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: `props` en Neo4j.
- Riesgos y mitigación (opcional): Depende de P8.

## Tareas

- [ ] T-M07.1 Props en el módulo graph
- [ ] T-M07.2 Panel en el editor
- [ ] T-M07.3 Mostrar en el detalle

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

Nodos y secciones tienen columnas fijas (tipo, nombre, ícono, vidas, etc.).

### Depende de

- [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial|M03]] Módulo graph en Neo4j y migración inicial

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P8]]
