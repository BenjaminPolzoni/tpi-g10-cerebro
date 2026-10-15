---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-70
estado: Propuesta
responsable: ""
epica: "Consistencia visual con la UI-KIT"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Must
en_taiga: false
---

# HU-70: Componente de grafo en la UI-KIT

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Consistencia visual con la UI-KIT|Consistencia visual con la UI-KIT]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HU-70 — Componente de grafo en la UI-KIT
------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: FRONT DE CUALQUIER GRUPO
*   **Quiero**: un componente de grafo en la UI-KIT
*   **Para**: no tener que hacer uno propio

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Envuelve `ngx-vflow` o `@foblex/flow` + `elkjs`, con tokens del kit.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Selección con teclado, foco visible y minimapa.
*   [ ] Otros: El dueño del componente de grafo es G10 (G13).

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: `generic-node-graph` en el kit con pan, zoom, minimapa, aristas y teclado.
*   [ ] **CA2**: Publicado en una versión del kit.
*   [ ] **CA3**: Usado por HU-62.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Componente de grafo

**Escenario 1**  

*   **Dado**: un grafo de 100 nodos
*   **Cuando**: se renderiza
*   **Entonces**: permite pan, zoom y minimapa

**Escenario 2**  

*   **Dado**: un usuario con teclado
*   **Cuando**: recorre el grafo
*   **Entonces**: pasa de nodo en nodo con foco visible

**Escenario 3**  

*   **Dado**: el kit publicado
*   **Cuando**: el roadmap lo instala
*   **Entonces**: HU-62 lo usa

* * *

Prototipo
---------

*   **Capturas**: No aplica.
*   **URL Figma**: Pendiente.
*   **Storybook**: Historia del componente en el Storybook del kit.
*   **Mock API / Swagger**: No aplica.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 8 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: Repo `2026-PIV-TPI-UI-KIT`.
*   Otros equipos / aprobaciones: Equipo del kit, para publicarlo (el dueño es G10, G13).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que el kit no lo acepte; mitigación: acordar antes de empezar.

## Tareas

- [ ] T-70.1 Acordar con el equipo del kit
- [ ] T-70.2 Componente
- [ ] T-70.3 Storybook y release

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

El kit no tiene componente de grafo. La vista de grafo del roadmap es un SVG propio.

### Depende de

Ninguna.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|G13]] El componente de grafo es nuestro (G10).
