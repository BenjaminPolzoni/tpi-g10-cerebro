---
tags: [tpi, g10, taiga, ht]
codigo: HT-34
ref: 9273
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8630 Consistencia visual con la UI-KIT|EP-8630]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9273
---

# HT-34: Componente de grafo en la UI-KIT

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9273) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8630 Consistencia visual con la UI-KIT|EP-8630]] · Tareas cerradas: **0/2**

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

- [ ] #9303 T-34.1 Acordar el componente de grafo con el equipo del kit · New · Ludmila Mailen Cejas
- [ ] #9304 T-34.2 Construir y publicar generic-node-graph en el kit · New · Ludmila Mailen Cejas
