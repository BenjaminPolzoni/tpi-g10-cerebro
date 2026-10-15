---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-60
estado: Propuesta
responsable: ""
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 3
prioridad: Could
en_taiga: false
---

# HU-60: Propiedades personalizadas en nodos y secciones

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HU-60 — Propiedades personalizadas en nodos y secciones
---------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: agregar datos propios (clave y valor) a nodos y secciones
*   **Para**: personalizar el roadmap sin pedir cambios de código

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Las propiedades libres no pisan los campos fijos que usa el dominio (tipo, vidas, reglas). Qué tan libre es depende de P8.
*   [ ] Validaciones: Claves únicas por nodo; tamaño máximo por valor.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Lista de pares editable con teclado.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Agregar, editar y borrar propiedades en un nodo o sección.
*   [ ] **CA2**: Se muestran en el detalle del nodo.
*   [ ] **CA3**: Una clave reservada devuelve error.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Propiedades personalizadas

**Escenario 1**  

*   **Dado**: un nodo
*   **Cuando**: el profesor agrega «dificultad: alta»
*   **Entonces**: el alumno la ve en el detalle

**Escenario 2**  

*   **Dado**: un nodo con una propiedad
*   **Cuando**: el profesor la borra
*   **Entonces**: deja de mostrarse

**Escenario 3**  

*   **Dado**: la clave reservada `type`
*   **Cuando**: el profesor la usa
*   **Entonces**: recibe error

* * *

Prototipo
---------

*   **Capturas**: Panel de propiedades del nodo.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-input`.
*   **Mock API / Swagger**: PATCH /api/roadmap/nodes/{nodeId} con `props`.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 3
*   **Prioridad (MoSCoW / Numérica)**: Could

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 3 | Could |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: Módulo graph, editor de nodo, detalle de nodo.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: `props` en Neo4j.
*   Riesgos y mitigación (opcional): Depende de P8.

## Tareas

- [ ] T-60.1 Props en el módulo graph
- [ ] T-60.2 Panel en el editor
- [ ] T-60.3 Mostrar en el detalle

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Nodos y secciones tienen columnas fijas (tipo, nombre, ícono, vidas, etc.).

### Depende de

- [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial|HT-18]] Módulo graph en Neo4j y migración inicial

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P8]]
