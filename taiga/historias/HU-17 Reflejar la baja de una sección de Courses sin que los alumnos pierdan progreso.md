---
tags: [tpi, g10, taiga, hu]
codigo: HU-17
ref: 4234
estado: "Done"
responsable: "Mateo Delgado Costa"
epica: "[G10] — Unidades del roadmap sincronizadas con Courses"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4234
---

# HU-17: Reflejar la baja de una sección de Courses sin que los alumnos pierdan progreso

> [!info] Generado desde Taiga (2026-10-14 18:47). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4234) · Estado: **Done** · Responsable: **Mateo Delgado Costa** · Sprint: **G10 - Sprint 2**

[G10] — HU-17 — Reflejar la baja de una sección de Courses sin que los alumnos pierdan progreso
-----------------------------------------------------------------------------------------------


* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: que si el profesor da de baja una sección en Cursos no pierda lo que ya hice
*   **Para**: conservar mi XP, mis lecturas y mis desbloqueos aunque cambie la estructura del curso


* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Si la sección desaparece o queda inactiva en Courses, la unidad y sus nodos pasan a baja lógica (RF-NFR-01). completed_node, content_reading y xp_movement no se tocan. El gate ignora los nodos de una unidad dada de baja. Las aristas que llegan desde otras unidades se resuelven según la decisión #2 del PO.
*   [ ] Validaciones: La baja solo la produce la sincronización (HU-36), no un ABM de Roadmap.
*   [ ] Otros: Si la sección vuelve a activarse, la unidad se reactiva con sus nodos y el progreso intacto. Dependencias / impactos: Depende de: HU-36. Relacionadas: HU-37 (aviso), HU-41 (baja de nodos). Preguntas abiertas: decisión #2 del PO.


* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Al sincronizar una sección dada de baja, la unidad deja de verse en el recorrido.
*   [ ] **CA2**: El XP, las lecturas y los completados de los alumnos quedan intactos.
*   [ ] **CA3**: Un nodo que tenía como prerrequisito un nodo de la unidad dada de baja se comporta según la decisión #2.
*   [ ] **CA4**: Reactivar la sección reactiva la unidad con el mismo progreso.


* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Baja de unidad originada en Courses

**Escenario 1**  

*   **Dado**: una unidad con 5 alumnos avanzando
*   **Cuando**: la sección se da de baja en Cursos y se sincroniza
*   **Entonces**: la unidad no se ve y el XP de los 5 alumnos no cambia

**Escenario 2**  

*   **Dado**: un nodo de otra unidad con prerrequisito en la unidad dada de baja
*   **Cuando**: el alumno consulta el gate
*   **Entonces**: se aplica la regla de la decisión #2 y el motivo se informa

**Escenario 3**  

*   **Dado**: una sección reactivada
*   **Cuando**: se sincroniza
*   **Entonces**: la unidad vuelve con los mismos completados

* * *
Prototipo
---------

*   **Capturas**: Pendiente.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: Parte de la sincronización de HU-36; aviso en el editor (HU-37).


---
ACTUALIZACION (plan vigente - modelo B / pull / regla c)
- Modelo B: un roadmap por cohorte. La baja de seccion se refleja por el sync (PULL) de HU-36, sin copia local ni evento de courses-lifecycle.
- La evaluacion del gate es por comision; restricciones por PULL (primero restriccion de SECCION, luego la de NODO).
- Regla (c): un prerrequisito no puede quedar fuera del scope de visibilidad del nodo que lo exige; se valida en el editor (transitivo) y se re-valida en el sync. DATE no restringe scope; HIDDEN y LOCKED por grupo hacen el prereq inalcanzable.
- Scopes finales (H1): restricciones de seccion y de nodo/actividad=`course.restrictions.read`.

## Tareas

- [x] #4265 T-17.1 Baja lógica de unidad, nodos y aristas cuando la sección se da de baja en Courses · Closed · Mateo Delgado Costa
- [x] #4266 T-17.2 Conservar progreso y excluir del gate los nodos dados de baja · Closed · Mateo Delgado Costa
- [x] #4267 T-17.3 Aristas desde otras unidades según la decisión n.º 2 del PO · Closed · Mateo Delgado Costa
- [x] #4268 T-17.4 BDD baja y reactivación con alumnos avanzando · Closed · Mateo Delgado Costa
- [x] #5377 T-17.5 Wiki, OpenAPI y diagrama de secuencia · Closed · Quinteros Tomás
- [x] #7476 Cliente pull de restricciones (seccion y actividad) con evaluacion por comision · Closed · Mateo Delgado Costa
- [x] #7477 Validacion de prerrequisitos (regla c) en editor y re-validacion en sync · Closed · Mateo Delgado Costa
- [x] #7478 Gate: restriccion de seccion -> nodo · Closed · Mateo Delgado Costa
