---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-68
estado: New
responsable: "Sin asignar"
epica: "Correcciones de los profes"
sprint: "G10 - Sprint 3"
puntos: 1
prioridad: Should
en_taiga: true
ref: 8617
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8617
responsables_tareas: ["Mateo Delgado Costa"]
tareas_cerradas: "2/4"
---

# HU-68: Obligatoriedad visible en la lista de nodos

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Correcciones de los profes|Correcciones de los profes]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **2/4** · Sprint: **G10 - Sprint 3**
> Cargada en Taiga: [[taiga/historias/HU-68 Obligatoriedad visible en la lista de nodos|HU-68]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8617)) · Épica en Taiga: [[epicas/EP-8631 Correcciones de los profes|EP-8631]] · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Mateo Delgado Costa|Mateo Delgado Costa]] (2).

> [!question] A qué se refiere
> **Lo que pidieron los profes:** «Lista de nodos que muestre la obligatoriedad (qué nodo es prerrequisito de otro)».
> **Dónde:** en la página de contenido de la materia, cada sección tiene dos vistas:
> - **Vista de edición** (nuestra, componente `roadmap-section-nodes` embebido en Cursos): ya muestra en cada fila, por ejemplo, «Lectura · Obligatoria · Requiere: Teoría 1, Práctica 2 (todos) · Disponible» (`b592bf2e`, 13/10). Solo falta la obligatoriedad en **desafíos y exámenes**.
> - **Vista simplificada** (sin permiso de edición): es de **Cursos (G01)**. Muestra solo el nombre de los desafíos y los recursos, sin obligatoriedad ni requisitos. Lo pedimos con un issue: [[sprints/sprint-3/borradores/Issue G01 - obligatoriedad y requisitos en la vista simplificada|issue para G01]], enviado como [#581](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/issues/581).

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
*   [ ] **CA5**: La vista simplificada de la sección (de G01) muestra la misma obligatoriedad y los mismos requisitos (issue a G01).

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
*   Módulos afectados: `roadmap-section-nodes` (método `detailsOf`) y `features/roadmap/embeds` (función para G01). De G01: `section-resources-container` y `section-resource-list`.
*   Otros equipos / aprobaciones: G01 Courses, para la vista simplificada (CA5).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Ninguno.

## Tareas

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **2/4**. Historia en Taiga: [[taiga/historias/HU-68 Obligatoriedad visible en la lista de nodos|HU-68]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8617)

- [x] [#9215](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9215) **T-68.1 «Requiere: …» y «Abierto al entrar a la unidad» en cada nodo** · Front · Closed · Sin asignar
    - Hecho en `b592bf2e` (13/10) en la lista del profesor (`roadmap-section-nodes`).
- [x] [#9216](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9216) **T-68.2 «Obligatoria / Opcional» en los nodos de lectura** · Front · Closed · Sin asignar
    - Hecho: lo arma `detailsOf` en la misma lista.
- [ ] [#9217](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9217) **T-68.3 Mostrar «Obligatorio / Opcional» también en desafíos y exámenes** · Front · New · [[sprints/sprint-3/12-responsables#Mateo Delgado Costa|Mateo Delgado Costa]]
    - **Qué:** en `detailsOf` de `roadmap-section-nodes`, la obligatoriedad hoy se muestra solo si `node.type === 'theory'`; mostrarla para todos los tipos que pueden ser obligatorios.
    - **Listo cuando:** un desafío obligatorio dice «Obligatorio» en la lista y hay test.
- [ ] [#9218](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9218) **T-68.4 Seguir el pedido a Courses para la vista simplificada** · Coordinación · New · [[sprints/sprint-3/12-responsables#Mateo Delgado Costa|Mateo Delgado Costa]]
    - **Qué:** acompañar el issue [#581](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/issues/581). Si G01 lo acepta, exportar desde `features/roadmap/embeds` una función que devuelva ya armadas la obligatoriedad y los requisitos de un nodo.
    - **Listo cuando:** la vista simplificada muestra lo mismo que la del profesor.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Verificado contra el front en `develop` (`dd642114`, 2026-10-15):

- **Lista del profesor** (`features/roadmap/embeds/section-nodes/roadmap-section-nodes.component.ts`, se muestra en la página de la materia): `detailsOf` arma la línea de cada nodo con el tipo, la obligatoriedad (**solo si es de lectura**: `node.type === 'theory'`), el material, el XP, la regla («Requiere: …» con `describeRule`) y si está disponible. Lo agregó `b592bf2e` (13/10, reglas por unidad y editor de reglas en 3 pasos).
- **Lista del alumno** (`ui/unit-node-list`, HUD del mundo hexagonal): muestra tipo · «Obligatorio/Opcional» y el estado en los nodos que puede ver; los bloqueados muestran el motivo. No muestra «Requiere».

### Depende de

Nada: CA4 se puede empezar ya. CA5 depende de G01.

### Dudas que la frenan

Ninguna.
