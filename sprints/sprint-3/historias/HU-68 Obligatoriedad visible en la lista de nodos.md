---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-68
estado: Propuesta
responsable: ""
epica: "Correcciones de los profes"
sprint: "G10 - Sprint 3"
puntos: 2
prioridad: Should
en_taiga: false
---

# HU-68: Obligatoriedad visible en la lista de nodos

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Correcciones de los profes|Correcciones de los profes]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HU-68 — Obligatoriedad visible en la lista de nodos
-----------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: ver en la lista de nodos cuáles son obligatorios y de qué dependen
*   **Para**: revisar el armado del curso sin abrir nodo por nodo

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Obligatorio = lectura obligatoria o requisito de otro nodo.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): La marca de obligatorio tiene texto alternativo.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Marca de obligatorio en cada nodo que lo es.
*   [ ] **CA2**: «Requiere: X, Y» por nodo.
*   [ ] **CA3**: Con componentes del kit.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Obligatoriedad en la lista

**Escenario 1**  

*   **Dado**: un nodo de lectura obligatoria
*   **Cuando**: el profesor ve la lista
*   **Entonces**: tiene la marca «Obligatorio»

**Escenario 2**  

*   **Dado**: el nodo 3 requiere 1 y 2
*   **Cuando**: el profesor ve la lista
*   **Entonces**: dice «Requiere: 1, 2»

**Escenario 3**  

*   **Dado**: un nodo sin requisitos
*   **Cuando**: el profesor ve la lista
*   **Entonces**: no muestra «Requiere»

* * *

Prototipo
---------

*   **Capturas**: `unit-node-list`.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-badge`.
*   **Mock API / Swagger**: Datos existentes del grafo.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 2
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 2 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: `unit-node-list`.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Ninguno.

## Tareas

- [ ] T-68.1 Marca y requisitos en la lista
- [ ] T-68.2 Tests

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

`unit-node-list` muestra los nodos sin dependencias.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

Ninguna.
