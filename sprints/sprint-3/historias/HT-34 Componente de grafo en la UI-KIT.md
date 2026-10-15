---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-34
estado: Propuesta
responsable: ""
epica: "Consistencia visual con la UI-KIT"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Must
prioridad_sprint: 1
en_taiga: false
---

# HT-34: Componente de grafo en la UI-KIT

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Consistencia visual con la UI-KIT|Consistencia visual con la UI-KIT]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga. Sale de dividir [[sprints/sprint-3/historias/HT-26 Adopción de la UI-KIT en el roadmap|HT-26]] el 2026-10-15 (21 pts, fuera del máximo de 8): HT-26 queda con las pantallas y esta HT con `generic-node-graph`.

> [!important] Prioridad 1 del sprint (2026-10-15)
> Va primero: [[sprints/sprint-3/historias/HU-62 Vista de grafo cómoda para el profesor|HU-62]] depende de este componente.

[G10] — HT-34 — Componente de grafo en la UI-KIT
------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: sumar a la UI-KIT un componente de grafo (`generic-node-graph`) con pan, zoom, minimapa, aristas y teclado
*   **Para**: que la vista de grafo del profesor (HU-62) use un componente del kit y no un SVG propio

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El componente es nuestro (G13) y se publica en el kit; lo que falta en el kit se aporta al kit, no se hace local. Usa los tokens del kit.
*   [ ] Validaciones: Historia en Storybook y tests del componente en verde.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): Fluido con 150 nodos.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Se recorre con teclado entre nodos y aristas, con foco visible; las aristas se distinguen por texto y forma de línea, no solo por color.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: La API del componente y la librería que envuelve están acordadas por escrito con el equipo del kit.
*   [ ] **CA2**: `generic-node-graph` está publicado en una versión del kit, con pan, zoom, minimapa, aristas con etiqueta y navegación con teclado.
*   [ ] **CA3**: Tiene historia en Storybook y lo puede usar HU-62.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Componente de grafo del kit

**Escenario 1**  

*   **Dado**: la historia de Storybook con un grafo de 150 nodos
*   **Cuando**: se hace zoom y pan
*   **Entonces**: se mueve fluido y el minimapa muestra la parte visible

**Escenario 2**  

*   **Dado**: el componente con el foco en un nodo
*   **Cuando**: se usan las flechas del teclado
*   **Entonces**: el foco pasa al nodo vecino y se ve

**Escenario 3**  

*   **Dado**: una arista con tipo
*   **Cuando**: se dibuja el grafo
*   **Entonces**: la arista muestra el nombre del tipo y su forma de línea

* * *

Prototipo
---------

*   **Capturas**: Historia de Storybook del componente.
*   **URL Figma**: Pendiente.
*   **Storybook**: Historia nueva de `generic-node-graph`.
*   **Mock API / Swagger**: No aplica.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Must · 1 (máxima del sprint)

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 8 | Must · 1 (máxima del sprint) |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: Repo `2026-PIV-TPI-UI-KIT`.
*   Otros equipos / aprobaciones: Equipo del kit, para publicar el componente (el dueño es G10).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que el kit no acepte el componente o tarde en publicarlo; mitigación: acordarlo antes de empezar (T-34.1) y que HU-62 arranque sobre la librería directa.

## Tareas

- [ ] **T-34.1 Acordar el componente de grafo con el equipo del kit** · Coordinación
    - **Qué:** acordar la API de `generic-node-graph`, la librería que envuelve (`ngx-vflow` o `@foblex/flow` con `elkjs`) y cómo se publica. El dueño es G10 (G13).
    - **Listo cuando:** el equipo del kit aceptó la propuesta por escrito.
- [ ] **T-34.2 Construir y publicar `generic-node-graph` en el kit** · Front (repo del kit)
    - **Qué:** componente con pan, zoom, minimapa, aristas, navegación con teclado y tokens del kit; historia en Storybook; release de una versión del kit.
    - **Listo cuando:** el componente está en una versión publicada del kit y lo puede usar HU-62.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

El kit no tiene componente de grafo; la vista de grafo del roadmap es un SVG propio. Detalle en [[sprints/sprint-3/05-ui-kit|05-ui-kit]].

### Depende de

Nada: se puede empezar ya.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|G13]] El componente de grafo es nuestro (G10).
