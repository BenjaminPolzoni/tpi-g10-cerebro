---
tags: [tpi, g10, sprint-3, historia, hu]
id: M09
tipo: HU
epica: "EP-S3-1"
capa: "Front (+ Back)"
esfuerzo: L
puntos: 8
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M02, U06]
---

# M09: Vista de grafo cómoda para el profesor

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HU** · Capa: **Front (+ Back)** · **8 pts** · **Must** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-xx — Vista de grafo cómoda para el profesor** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: PROFESOR
- **Quiero**: ver y editar el roadmap como un grafo cómodo, con acomodo automático y posiciones guardadas
- **Para**: entender y modificar las relaciones del curso de un vistazo

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Las posiciones se guardan (hoy `moveNode` devuelve 501). Crear y borrar aristas arrastrando.
- [ ] Performance (tiempos, volumen, límites): Fluido con 150 nodos.
- [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño.
- [ ] Accesibilidad (WCAG/teclado/lectores): Navegación con teclado entre nodos, foco visible y alternativa en lista (M10).

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Acomodo automático (`elkjs`), zoom, pan y minimapa.
- [ ] **CA2**: Las posiciones se guardan y se recuperan.
- [ ] **CA3**: Crear y borrar aristas arrastrando.
- [ ] **CA4**: Usa el componente de grafo del kit (U06).
- [ ] **CA5**: Se puede usar con teclado.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Vista de grafo

**Escenario 1**

- **Dado**: un roadmap nuevo
- **Cuando**: el profesor abre la vista de grafo
- **Entonces**: los nodos aparecen acomodados automáticamente

**Escenario 2**

- **Dado**: el profesor mueve un nodo
- **Cuando**: recarga la página
- **Entonces**: el nodo sigue donde lo dejó

**Escenario 3**

- **Dado**: dos nodos
- **Cuando**: el profesor arrastra de uno al otro
- **Entonces**: se crea la relación

* * *

## Prototipo

- **Capturas**: Vista de grafo del editor.
- **URL Figma**: Pendiente.
- **Storybook**: `generic-node-graph` (U06).
- **Mock API / Swagger**: GET /api/roadmap/roadmaps/{roadmapId}/graph y PATCH de posiciones.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 8
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: `course-map-page`, endpoint `/graph`.
- Otros equipos / aprobaciones: Equipo UI-KIT (U06).
- Impacto en datos / migraciones: Posiciones en Neo4j.
- Riesgos y mitigación (opcional): Depende de U06; mitigación: arrancar sobre la librería directa y migrar al kit.

## Tareas

- [ ] T-M09.1 Integrar el componente de grafo
- [ ] T-M09.2 Guardar posiciones (reemplazar el 501)
- [ ] T-M09.3 Aristas arrastrando
- [ ] T-M09.4 Teclado y accesibilidad

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

La vista de grafo existe pero es incómoda. `moveNode` devuelve 501: las posiciones no se guardan.

### Depende de

- [[sprints/sprint-3/historias/M02 Modelo 1 a N de curso a roadmaps|M02]] Modelo 1 a N de curso a roadmaps
- [[sprints/sprint-3/historias/U06 Componente de grafo en la UI-KIT|U06]] Componente de grafo en la UI-KIT

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G13]]
