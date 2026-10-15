---
tags: [tpi, g10, taiga, hu]
codigo: HU-68
ref: 8617
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8631 Correcciones de los profes|EP-8631]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8617
---

# HU-68: Obligatoriedad visible en la lista de nodos

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8617) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8631 Correcciones de los profes|EP-8631]] · Tareas cerradas: **2/4**

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

- [x] #9215 T-68.1 «Requiere: …» y «Abierto al entrar a la unidad» en cada nodo · Closed · Sin asignar
- [x] #9216 T-68.2 «Obligatoria / Opcional» en los nodos de lectura · Closed · Sin asignar
- [ ] #9217 T-68.3 Mostrar «Obligatorio / Opcional» también en desafíos y exámenes · New · Mateo Delgado Costa
- [ ] #9218 T-68.4 Seguir el pedido a Courses para la vista simplificada · New · Mateo Delgado Costa
