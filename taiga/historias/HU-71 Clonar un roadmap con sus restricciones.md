---
tags: [tpi, g10, taiga, hu]
codigo: HU-71
ref: 8619
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8619
---

# HU-71: Clonar un roadmap con sus restricciones

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8619) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Tareas cerradas: **0/4**

[G10] — HU-71 — Clonar un roadmap con sus restricciones
-------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR / GESTOR
*   **Quiero**: clonar un roadmap con su estructura, sus reglas y sus restricciones para otra comisión del curso o para otro curso
*   **Para**: reusar un recorrido ya armado sin rehacerlo a mano

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: La copia lleva secciones, subsecciones, nodos (con `START`/`END`), relaciones con tipo, reglas de desbloqueo, restricciones y la configuración del roadmap (DEC-017). Todos los ids de la copia son nuevos: el `node_id` es único global también después de clonar (G8). No se copia el progreso de los alumnos.
*   [ ] Validaciones: Nombre obligatorio y único dentro del curso destino. El destino tiene que ser un curso o una comisión activos.
*   [ ] Datos obligatorios: Roadmap de origen, curso destino y nombre de la copia. La comisión destino es opcional.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño del curso de origen y del de destino.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Diálogo de clonado con componentes del kit, usable con teclado.
*   [ ] Otros: Si falla la escritura en Neo4j, no queda una copia a medias (la copia parcial se da de baja lógica). Con un roadmap que usa secciones de Courses y se clona a otro curso, falta definir qué pasa con ese vínculo (P17).

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor clona un roadmap a otra comisión del mismo curso o a otro curso.
*   [ ] **CA2**: La copia tiene la misma estructura, relaciones, reglas, restricciones y configuración que el original.
*   [ ] **CA3**: Todos los ids de la copia son nuevos y no chocan con los del original.
*   [ ] **CA4**: La copia arranca sin progreso de alumnos.
*   [ ] **CA5**: Sin permiso sobre el curso de destino, la operación devuelve 403.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Clonar un roadmap

**Escenario 1**  

*   **Dado**: un roadmap con 2 secciones, reglas `requires` y una restricción por fecha
*   **Cuando**: el profesor lo clona para la comisión 2w2
*   **Entonces**: la comisión 2w2 tiene un roadmap igual, con las mismas reglas y la misma restricción

**Escenario 2**  

*   **Dado**: un roadmap clonado
*   **Cuando**: el Motor manda el cierre de un intento con el `id_node` de la copia
*   **Entonces**: el progreso se registra en la copia y no en el original

**Escenario 3**  

*   **Dado**: un profesor que no es dueño del curso de destino
*   **Cuando**: intenta clonar un roadmap hacia ese curso
*   **Entonces**: recibe 403 y no se crea nada

* * *

Prototipo
---------

*   **Capturas**: Acción «Clonar» en la pantalla de roadmaps del curso (HU-57).
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-modal`, `generic-select`, `generic-input`.
*   **Mock API / Swagger**: POST /api/roadmap/roadmaps/{roadmapId}/clone con `target_course_id`, `target_group_id` (opcional) y `name`.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 8 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Courses (validar el curso y la comisión de destino).
*   Módulos afectados: Módulo `graph` (copia del subgrafo), roadmaps del curso, pantalla del profesor.
*   Otros equipos / aprobaciones: G01, solo si se clona a otro curso un roadmap con secciones de Courses (P17).
*   Impacto en datos / migraciones: Sin migración. La copia es un subgrafo nuevo en Neo4j.
*   Riesgos y mitigación (opcional): Copiar en dos bases sin transacción común; mitigación: escribir primero en Neo4j y dar de baja lógica la copia si algo falla (DEC-016).


## Tareas

- [ ] #9169 T-71.1 Copiar un roadmap con ids nuevos · New · Baltasar Rodriguez Teruel
- [ ] #9170 T-71.2 Endpoint de clonado con permisos · New · Baltasar Rodriguez Teruel
- [ ] #9171 T-71.3 Acción «Clonar» en la pantalla del profesor · New · Baltasar Rodriguez Teruel
- [ ] #9354 T-71.4 Wiki, OpenAPI y diagrama de secuencia · New · Quinteros Tomás
