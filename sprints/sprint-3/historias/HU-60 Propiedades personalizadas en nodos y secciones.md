---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-60
estado: Eliminada
responsable: ""
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 3
prioridad: Could
en_taiga: false
---

# HU-60: Propiedades personalizadas en nodos y secciones

> [!danger] Eliminada el 2026-10-15 (revisión de HU): no aportaba comportamiento nuevo después de P8. Nombre, ícono y descripción ya se editan (HU-41/HU-43), las reglas están en HU-58/HU-59 y el rechazo de campos libres pasó a HT-18 (CA7, T-18.7). **Borrar esta nota.**

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

> [!warning] 2026-10-15: alcance redefinido por P8
> No hay campos libres (clave y valor) ni tipos de nodo nuevos. "Personalizable" es nombre, ícono, descripción y reglas (DEC-018).

[G10] — HU-60 — Propiedades personalizadas en nodos y secciones
---------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: personalizar el nombre, el ícono, la descripción y las reglas de nodos y secciones
*   **Para**: personalizar el roadmap sin pedir cambios de código

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: No hay campos libres ni tipos de nodo nuevos (P8, DEC-018). Se personalizan nombre, ícono, descripción y reglas. Los tipos de nodo son fijos: desafíos teóricos, prácticos, de IA y de recuperación de vida, examen, contenido teórico, inicio y fin.
*   [ ] Validaciones: Nombre obligatorio; el ícono sale del catálogo de íconos (HU-43).
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Formulario editable con teclado.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Editar nombre, ícono, descripción y reglas de un nodo o sección.
*   [ ] **CA2**: Se muestran en el detalle del nodo.
*   [ ] **CA3**: No se pueden crear campos libres ni tipos de nodo nuevos.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Personalizar nodos y secciones

**Escenario 1**  

*   **Dado**: un nodo
*   **Cuando**: el profesor le cambia el nombre, el ícono y la descripción
*   **Entonces**: el alumno los ve en el detalle

**Escenario 2**  

*   **Dado**: un nodo con reglas de desbloqueo
*   **Cuando**: el profesor las cambia
*   **Entonces**: el desbloqueo usa las reglas nuevas

**Escenario 3**  

*   **Dado**: el editor de un nodo
*   **Cuando**: el profesor elige el tipo
*   **Entonces**: solo puede elegir entre los tipos fijos

* * *

Prototipo
---------

*   **Capturas**: Panel de edición del nodo.
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
*   Riesgos y mitigación (opcional): Ninguno abierto (P8 respondida el 2026-10-15: el alcance se achicó).

## Tareas

- [ ] **T-60.1 Editar nombre, ícono, descripción y reglas de nodos y secciones** · Back
    - **Qué:** esos cuatro campos son los únicos personalizables (P8, DEC-018). El back rechaza con 400 campos libres o tipos de nodo nuevos.
    - **Dónde:** módulo `graph`, `NodeController`.
    - **Listo cuando:** hay tests de lo permitido y lo rechazado.
- [ ] **T-60.2 Panel de edición del nodo y la sección** · Front
    - **Qué:** `entity-editor-dialog` con nombre, ícono (del catálogo de HU-43), descripción y acceso al editor de reglas.
    - **Listo cuando:** el profesor cambia los cuatro datos desde el editor.
- [ ] **T-60.3 Mostrarle al alumno lo personalizado** · Front
    - **Qué:** `node-detail` muestra el nombre, el ícono y la descripción que eligió el profesor.
    - **Listo cuando:** un cambio del profesor se ve en el detalle del alumno.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Nodos y secciones tienen columnas fijas (tipo, nombre, ícono, vidas, etc.).

### Depende de

- [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial|HT-18]] Módulo graph en Neo4j y migración inicial

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P8]] Sin campos libres ni tipos de nodo nuevos: se personalizan nombre, ícono, descripción y reglas.
