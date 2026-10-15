---
tags: [tpi, g10, sprint-3, historia, hu]
id: U06
tipo: HU
epica: "EP-S3-3"
capa: "UI-KIT"
esfuerzo: L
puntos: 8
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [U01]
---

# U06: Componente de grafo en la UI-KIT

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-3 Consistencia visual con la UI-KIT|EP-S3-3]] · **HU** · Capa: **UI-KIT** · **8 pts** · **Must** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-xx — Componente de grafo en la UI-KIT** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: FRONT DE CUALQUIER GRUPO
- **Quiero**: un componente de grafo en la UI-KIT
- **Para**: no tener que hacer uno propio

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Envuelve `ngx-vflow` o `@foblex/flow` + `elkjs`, con tokens del kit.
- [ ] Accesibilidad (WCAG/teclado/lectores): Selección con teclado, foco visible y minimapa.
- [ ] Otros: Hay que acordar con el equipo del kit quién es dueño (G13).

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: `generic-node-graph` en el kit con pan, zoom, minimapa, aristas y teclado.
- [ ] **CA2**: Publicado en una versión del kit.
- [ ] **CA3**: Usado por M09.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Componente de grafo

**Escenario 1**

- **Dado**: un grafo de 100 nodos
- **Cuando**: se renderiza
- **Entonces**: permite pan, zoom y minimapa

**Escenario 2**

- **Dado**: un usuario con teclado
- **Cuando**: recorre el grafo
- **Entonces**: pasa de nodo en nodo con foco visible

**Escenario 3**

- **Dado**: el kit publicado
- **Cuando**: el roadmap lo instala
- **Entonces**: M09 lo usa

* * *

## Prototipo

- **Capturas**: No aplica.
- **URL Figma**: Pendiente.
- **Storybook**: Historia del componente en el Storybook del kit.
- **Mock API / Swagger**: No aplica.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 8
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: Repo `2026-PIV-TPI-UI-KIT`.
- Otros equipos / aprobaciones: Equipo del kit (G13).
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Que el kit no lo acepte; mitigación: acordar antes de empezar.

## Tareas

- [ ] T-U06.1 Acordar con el equipo del kit
- [ ] T-U06.2 Componente
- [ ] T-U06.3 Storybook y release

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

El kit no tiene componente de grafo. La vista de grafo del roadmap es un SVG propio.

### Depende de

- [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs|U01]] Subir la UI-KIT a 0.8.0 y cerrar sus TODOs

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G13]]
