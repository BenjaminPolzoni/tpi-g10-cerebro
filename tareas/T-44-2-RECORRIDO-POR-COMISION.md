# T-44.2 — Contrato Roadmap ↔ Frontend por comisión

> **Estado: implementado en T-44.2** para el alumno, detrás del flag `ROADMAP_BY_GROUP_ENABLED`. El
> reparto con T-45.2 (HU-45) se acordó el 2026-10-09 con su responsable; lo marcado como «a
> plantear con el equipo» sigue abierto.

## Alcance

Este documento define únicamente el contrato HTTP que consume el frontend para HU-44. Las
comisiones y las restricciones de sección se resuelven internamente; el frontend no consulta
Courses ni replica sus reglas. Gate (T-44.3), selector visual (T-44.9) y condiciones
`DATE`/`SECTION_COMPLETED` quedan fuera de T-44.2.

El flag `ROADMAP_BY_GROUP_ENABLED=false` conserva las respuestas actuales y no exige
`group_id`.

## Dependencias

T-44.2 se apoya en lo que ya está en `develop`; este documento no replica rutas, scopes ni DTOs de
Courses.

| Pieza | Origen | Qué aporta |
|---|---|---|
| `CourseGroupsClient` | T-10.2 (PR #150) | Comisiones de cada alumno de la cohorte, por pull |
| `GroupUnitsService`, `GroupVisibilityRules` | T-44.1 (PR #151) | Unidades visibles en cada comisión del alumno y unidades no resueltas |
| `RoadmapGroupProperties` | T-44.4 (PR #136) | Flag `ROADMAP_BY_GROUP_ENABLED` |
| Acta T-10.1 | [`contracts/courses-grupos-t-10-1.md`](contracts/courses-grupos-t-10-1.md) | Contrato con Courses: comisiones, participantes y restricciones |

## Reparto con T-45.2 (HU-45)

T-44.2 y T-45.2 («parámetro de comisión en el avance») describen el mismo `group_id`. Para no
duplicar, el reparto **acordado el 2026-10-09 con el responsable de T-45.2** (Lorenzo Araujo) es:

| Responsabilidad | Tarea |
|---|---|
| Parámetro `group_id` en recorrido y progreso del alumno | T-44.2 |
| Filtro reutilizable «comisión elegida → unidades y nodos visibles» | T-44.2 |
| Autorización del alumno: matrícula activa, comisión propia, selección automática | T-44.2 |
| Casos de staff: profesor dueño, gestor y administrador eligen cualquier comisión | T-45.2 |
| Validar que la comisión pertenece a la cohorte cuando la elige el staff | T-45.2 |
| Avance de los alumnos de una comisión (CA1 y CA3 de HU-45) | T-45.2 |

La regla «el alumno solo pide sus comisiones; `403` si es ajena» figura en las dos tareas (es el
CA4 de HU-45): se implementa una sola vez, en T-44.2. T-45.2 se construye sobre la rama de T-44.2 y
reutiliza el filtro.

Para el avance de una comisión, T-45.2 propone un **endpoint nuevo, solo para staff**, en lugar de
extender los dos de este documento, que son por alumno:

```http
GET /api/roadmap/courses/{courseId}/groups/{groupId}/progress
```

Devolvería una fila resumida por alumno de la comisión. Su contrato lo define T-45.2, no este
documento.

## Parámetro de comisión

Los dos endpoints existentes aceptan el mismo query param opcional:

```http
GET /api/roadmap/courses/{courseId}?group_id={groupId}
GET /api/roadmap/courses/{courseId}/students/{studentId}/progress?group_id={groupId}
```

Reglas para el **alumno** (T-44.2):

- `group_id`: UUID estable de una comisión del alumno.
- Una sola comisión: si se omite, Roadmap la selecciona automáticamente.
- Varias comisiones: es obligatorio; si falta, Roadmap responde `400` e informa las opciones.
- Comisión ajena: `403`.

Antes de resolver comisiones, Roadmap valida la matrícula activa en `student_course`. Una lista
vacía de comisiones nunca concede acceso: sin matrícula activa se responde `403`. Una cohorte sin
comisiones conserva el recorrido completo; un alumno matriculado sin comisión ve solo unidades
generales.

### La comisión pertenece a la cohorte

HU-45 exige que la comisión elegida pertenezca al curso-cohorte.

- **Alumno:** queda cubierto por la regla de comisión propia. Las comisiones del alumno se leen de
  la cohorte consultada, así que un `group_id` de otra cohorte o inexistente no figura entre las
  suyas y responde `403`, igual que una comisión ajena. No se distingue «no existe» de «no es tuya»
  para no exponer qué comisiones hay.
- **Staff:** la validación contra las comisiones de la cohorte y su código de error corresponden a
  T-45.2, en su endpoint.

### Staff

T-44.2 no cambia lo que ve el staff en los dos endpoints de este documento: sigue recibiendo la
respuesta actual, sin filtrar por comisión. Los casos de staff corresponden a T-45.2, que los
resuelve con su endpoint propio. Si T-45.2 necesitara además el recorrido filtrado para staff, lo
agrega reutilizando el filtro de T-44.2.

HU-45 nombra tres roles que podrían elegir cualquier comisión. No todos están autorizados hoy en
los endpoints de Roadmap:

| Rol en HU-45 | Estado actual en Roadmap |
|---|---|
| Profesor dueño de la cohorte | Existe el rol `PROFESSOR`. El progreso admite `PROFESSOR` y `ADMIN`; este documento no afirma que hoy se verifique que el profesor sea dueño de la cohorte en esa consulta |
| Gestor | No existe como rol en Roadmap (`Roles` define `ADMIN`, `PROFESSOR` y `STUDENT`). Autorizarlo es una decisión de T-45.2 |
| Administrador | Existe el rol `ADMIN`, ya admitido en el progreso |

El recorrido (`GET /courses/{courseId}`) no declara hoy una restricción de rol propia.

## Recorrido

La respuesta exitosa conserva el envelope de plataforma y agrega el contexto necesario para el
selector:

```json
{
  "data": {
    "id": "6db2c4fb-f65e-4a64-bd35-62b998b3ed60",
    "course_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "archived": false,
    "group_selection": {
      "available_groups": [
        { "id": "8b1f0c5e-2a4d-4e3b-9f1a-0c7d5e2a1b34", "name": "2W1" },
        { "id": "c2d9e7a1-5b6f-4c8d-a3e2-1f0b9d8c7a65", "name": "2W2" }
      ],
      "selected_group_id": "c2d9e7a1-5b6f-4c8d-a3e2-1f0b9d8c7a65"
    },
    "sections": []
  },
  "message": null,
  "success": true,
  "timestamp": "2026-10-09T18:00:00Z"
}
```

`sections` contiene solo unidades visibles para la selección. Con el flag apagado, o para staff,
se conserva el payload anterior, sin `group_selection`. Sin comisiones,
`available_groups` es `[]` y `selected_group_id` es `null`.

## Unidades no resueltas

T-44.1 marca como **no resuelta** a la unidad que tiene una sección de Courses asociada
(`course_section_id`) que Courses no encuentra, por inexistente o inactiva. No se puede saber si
estaba restringida, así que no se concede acceso por defecto.

- No aparecen en `sections` del recorrido, en ninguna comisión.
- Sus nodos no aparecen en `nodes` del progreso, así que no cuentan en el numerador ni en el
  denominador del avance.
- Tampoco las ve un alumno sin comisión.
- Su progreso guardado (XP, completados y lecturas) no se borra ni se modifica.
- El contrato no las informa al frontend del alumno: quedan registradas en el log del servicio.

Una unidad **manual**, sin sección de Courses asociada, no es una unidad no resuelta: es general y
se ve en todas las comisiones.

## Progreso

La respuesta mantiene `student_id`, `course_id`, `xp_total`, `current_lives` y `nodes`. Solo cambia
la proyección de `nodes`: incluye exclusivamente nodos de las unidades visibles para `group_id`.

- XP, completados y lecturas continúan almacenados a nivel cohorte/alumno-nodo; cambiar de comisión
  no los modifica.
- Cambio de comisión (T-44.5): cuando Courses agrega, quita o mueve al alumno, Roadmap no guarda
  ni borra nada; la próxima consulta refleja la membresía vigente. Lo que el alumno hizo en una
  unidad que deja de ver queda guardado y vuelve a mostrarse como completado si regresa a esa
  comisión. Verificado en `GroupMembershipChangeTest`.
- T-44.2 no agrega una fórmula de porcentaje. El frontend calcula el avance como hoy usando la lista
  filtrada: tanto el numerador de completados como el denominador total salen de `nodes`.
- El frontend envía al progreso el mismo `group_id` que quedó seleccionado en el recorrido.

## Errores

Los errores usan Problem Details y conservan `trace_id`.

Varias comisiones sin selección:

```json
{
  "type": "about:blank",
  "title": "Bad Request",
  "status": 400,
  "detail": "Debe seleccionar una comisión.",
  "available_groups": [
    { "id": "8b1f0c5e-2a4d-4e3b-9f1a-0c7d5e2a1b34", "name": "2W1" },
    { "id": "c2d9e7a1-5b6f-4c8d-a3e2-1f0b9d8c7a65", "name": "2W2" }
  ],
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736"
}
```

| Estado | Situación |
|---|---|
| `400` | `group_id` inválido o ausente cuando el alumno tiene varias comisiones |
| `401` | Identidad ausente o inválida en el Gateway |
| `403` | Matrícula inactiva/inexistente, rol sin permiso, o comisión que no es del alumno (ajena, de otra cohorte o inexistente) |
| `404` | La cohorte no tiene roadmap |
| `503` | No se pudieron resolver comisiones o restricciones; nunca se asume una vista pública |

El `400` por selección faltante incluye `available_groups` para que T-44.9 construya el selector sin
otro endpoint ni una llamada directa a Courses. Los demás errores no exponen membresías.

Los errores del endpoint de staff los define T-45.2.

## Gate y acciones del alumno (T-44.3)

Este contrato no cambia, pero el filtro de la vista no es el único control. Con el flag encendido,
Roadmap rechaza además del lado del servidor las acciones sobre una unidad que no es de ninguna
comisión del alumno, sin depender del frontend:

| Ruta | Respuesta para una unidad de otra comisión |
|---|---|
| Gate del Motor (`.../nodes/{nodeId}/eligibility`) | `200`, `eligible=false`, `reason=group_restricted` ([gate v1.1](contracts/roadmap-motor-gate-v1.md)) |
| `POST /courses/{courseId}/nodes/{nodeId}/start` | `403` `group.restricted` |
| `POST /nodes/{nodeId}/read` | `403` `group.restricted`; la lectura no se registra |

A diferencia de la vista, estas rutas consideran **todas** las comisiones del alumno, no la elegida.
Una unidad no resuelta responde `403` `node.unit-unresolved` y Courses caído, `503`.

**Rutas de solo lectura todavía sin control por comisión** (pendiente, bloqueante antes de encender
el flag en un entorno real): `GET /courses/{courseId}/nodes/{nodeId}` y
`GET /courses/{courseId}/materials` devuelven el detalle y el material, con su URL de acceso, de
unidades de otra comisión; `GET /courses/{courseId}/sections/{sectionId}/reading-progress` devuelve
sus contadores de lectura.

**Progreso consultado por el staff:** no aplica la regla de comisión. Un nodo de una unidad ajena a
las comisiones del alumno puede figurar como `enabled` aunque el Gate responda `group_restricted`.
La vista de avance por comisión del staff es de T-45.2.

## Implementación

| Pieza | Qué hace |
|---|---|
| `GroupSelectionService` | Filtro reutilizable: valida la matrícula activa, resuelve la comisión (automática con una sola, `400` con varias sin elegir, `403` si no es del alumno) y devuelve las unidades visibles. Con el flag apagado no interviene |
| `CohortGroupContext` | Foto de la cohorte ya leída de Courses. Separa la carga (una vez por cohorte, `GroupUnitsService.contextOf`) de la evaluación por alumno, que no usa la red: es lo que reutiliza T-45.2 para resolver a todos los alumnos de una comisión con una sola carga |
| `StudentViewer` | Reconoce al alumno que consulta lo suyo; quien tiene además un rol de staff conserva la vista completa |
| `GraphController`, `ProgressController` | Aceptan `group_id` y aplican el filtro solo para ese alumno |

Orden de validación para el alumno: existencia del roadmap y matrícula activa, y recién después
las comisiones.

## Discrepancia abierta con HU-45: llamadas a Courses

HU-45 pide, en su nota de performance, que el parámetro de comisión funcione «sin llamadas extra a
Courses». La implementación vigente es **pull** y no lo cumple:

- `GroupUnitsService` (T-44.1) consulta a Courses en cada cálculo: lee las comisiones de toda la
  cohorte (`CourseGroupsClient`) y la restricción de cada unidad anclada, una llamada por sección
  (`CourseRestrictionsClient`).
- No hay caché ni almacenamiento local de membresías: la tabla `student_course_group` que menciona
  HU-45 se deprecó junto con la HT-10 original.

Con el flag encendido, cada consulta de recorrido o de progreso con comisión genera esas llamadas.

Postura acordada entre los responsables de HU-44 y HU-45, **a plantear con el equipo**:

- El requisito «sin llamadas extra a Courses» se mantiene para el **ranking**, que no depende de
  Courses.
- El avance por comisión sí necesita leer las comisiones de Courses por lote.
- La tabla local con sincronización por eventos queda fuera de este sprint.
- El texto de HU-45 (la nota de performance y la mención a `student_course_group`) se corrige.

Sigue abierto: el filtro por comisión lee además la restricción de cada unidad anclada, una llamada
por sección. Este documento no propone una solución de caché para eso.
