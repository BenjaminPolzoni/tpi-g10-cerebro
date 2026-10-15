---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-68
estado: Propuesta
responsable: ""
epica: "Correcciones de los profes"
sprint: "G10 - Sprint 3"
puntos: 1
prioridad: Should
en_taiga: false
---

# HU-68: Obligatoriedad visible en la lista de nodos

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Correcciones de los profes|Correcciones de los profes]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

> [!question] A qué se refiere
> **Lo que pidieron los profes:** «Lista de nodos que muestre la obligatoriedad (qué nodo es prerrequisito de otro)».
> **Dónde:** la lista de nodos de cada sección que ve el **profesor** al armar la materia (página de la materia → sección → nodos; componente `roadmap-section-nodes`). Cada fila de esa lista describe un nodo en una línea, por ejemplo: «Lectura · Obligatoria · Requiere: Teoría 1, Práctica 2 (todos) · Disponible».
> **Estado al 2026-10-15:** casi todo está hecho (commit `b592bf2e`, 13/10). Solo falta mostrar si es obligatorio en los **desafíos y exámenes**: hoy esa palabra aparece solo en los nodos de lectura.

[G10] — HU-68 — Obligatoriedad visible en la lista de nodos
-----------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: ver en la lista de nodos de cada sección, sin abrir cada nodo, cuáles son obligatorios y de qué otros nodos depende cada uno
*   **Para**: revisar de un vistazo cómo armé el recorrido de la unidad

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: «Obligatorio» es la marca que el profesor le pone al nodo (lectura obligatoria o desafío obligatorio). «Requiere» lista los nodos que el alumno tiene que completar antes, con el modo de la regla: «(todos)» si es AND y «(cualquiera)» si es OR. Un nodo sin requisitos dice «Abierto al entrar a la unidad».
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): Solo el profesor dueño, el gestor o el admin ven la lista (es la pantalla de edición).
*   [ ] Accesibilidad (WCAG/teclado/lectores): La obligatoriedad y los requisitos se escriben con texto, no solo con color o ícono.
*   [ ] Otros: La lista del **alumno** dentro del mundo (`unit-node-list`) ya muestra «Obligatorio/Opcional» en los nodos que puede ver; mostrarle también «Requiere» no es parte de esta HU.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [x] **CA1**: Cada nodo de la lista dice qué nodos requiere: «Requiere: X, Y (todos)» o «(cualquiera)». ✅ hecho
*   [x] **CA2**: Un nodo sin requisitos dice «Abierto al entrar a la unidad». ✅ hecho
*   [x] **CA3**: Los nodos de lectura dicen «Obligatoria» u «Opcional». ✅ hecho
*   [ ] **CA4**: Los desafíos y exámenes también dicen «Obligatorio» u «Opcional».

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Obligatoriedad y requisitos en la lista de nodos del profesor

**Escenario 1**  

*   **Dado**: un nodo que requiere «Teoría 1» y «Práctica 2» con regla AND
*   **Cuando**: el profesor abre la lista de nodos de la sección
*   **Entonces**: la fila dice «Requiere: Teoría 1, Práctica 2 (todos)»

**Escenario 2**  

*   **Dado**: el primer nodo de la unidad, sin requisitos
*   **Cuando**: el profesor abre la lista
*   **Entonces**: la fila dice «Abierto al entrar a la unidad»

**Escenario 3**  

*   **Dado**: un desafío marcado como obligatorio
*   **Cuando**: el profesor abre la lista
*   **Entonces**: la fila dice «Obligatorio», igual que una lectura obligatoria

* * *

Prototipo
---------

*   **Capturas**: Lista de nodos de una sección en la página de la materia.
*   **URL Figma**: No aplica (la pantalla ya existe).
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: Datos existentes del roadmap (`isMandatory` y conexiones entre nodos).

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 1
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 1 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: `roadmap-section-nodes` (método `detailsOf`).
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Ninguno.

## Tareas

- [x] T-68.1 «Requiere: …» y «Abierto al entrar a la unidad» por nodo (`b592bf2e`)
- [x] T-68.2 «Obligatoria / Opcional» en los nodos de lectura
- [ ] T-68.3 «Obligatorio / Opcional» también en desafíos y exámenes
- [ ] T-68.4 Test de la fila de un desafío obligatorio

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Verificado contra el front en `develop` (`dd642114`, 2026-10-15):

- **Lista del profesor** (`features/roadmap/embeds/section-nodes/roadmap-section-nodes.component.ts`, se muestra en la página de la materia): `detailsOf` arma la línea de cada nodo con el tipo, la obligatoriedad (**solo si es de lectura**: `node.type === 'theory'`), el material, el XP, la regla («Requiere: …» con `describeRule`) y si está disponible. Lo agregó `b592bf2e` (13/10, reglas por unidad y editor de reglas en 3 pasos).
- **Lista del alumno** (`ui/unit-node-list`, HUD del mundo hexagonal): muestra tipo · «Obligatorio/Opcional» y el estado en los nodos que puede ver; los bloqueados muestran el motivo. No muestra «Requiere».

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

Ninguna.
