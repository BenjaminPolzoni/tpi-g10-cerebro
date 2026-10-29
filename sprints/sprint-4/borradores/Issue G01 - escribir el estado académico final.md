---
tags: [tpi, g10, sprint-4, borrador, issue, G01, HU-72]
fecha: 2026-10-26
autor: Benjamin Polzoni
estado: publicado
issue: https://github.com/2026-P4-BE/tpi-course/issues/239
destino: 2026-P4-BE/tpi-course
tarea: T-72.1
verificado_contra: tpi-course develop 01c8df4 (2026-10-26)
---

# Issue para G01 · Escribir el estado académico final antes de archivar

> [!info] Contexto
> Es T-72.1 de [[sprints/sprint-4/Planes/Benja/HU-72 Back+Front - cierre del curso y roadmap archivado|HU-72]] y responde la duda G14. Lo de abajo de la línea es el cuerpo del issue, listo para pegar. Sigue el contrato de errores de `tpi-course#148`.

## Qué verificamos en su código (`develop` `01c8df4`)

- `CohortArchiveRules.assertEveryEnrollmentHasFinalStatus` → `409 MISSING_FINAL_ACADEMIC_STATUS` si una matrícula `VALIDATED` activa no tiene estado final.
- `Enrollment.finalAcademicStatus` (columna `final_academic_status`, V1) solo tiene el `@Setter` de Lombok. **Nadie lo llama en `src/main`** (tampoco hay `copyProperties` ni `UPDATE` nativo).
- Los valores ya están en `system_parameter` (V6, `FINAL_ACADEMIC_STATUS`): `PROMOTED`, `REGULAR`, `NOT_REGULAR` («Libre») y `DROPPED_OUT`.
- Ya existe todo lo demás:
  - `GET /course-cohorts/{id}/enrollments` devuelve `final_academic_status` y `student_number`;
  - el alumno ve el suyo como `condition` en su listado;
  - `CourseCohortArchiveService.archive` publica `COURSE_COHORT_ARCHIVED`, que Roadmap ya consume.
- El patrón a copiar es `POST /enrollments/{id}/reject`: permiso `membership.isCanWrite()` y `EnrollmentResponse` como respuesta.

## Qué pedimos y qué no

| Se pide | No se pide (ya está o no hace falta) |
|---|---|
| 1 endpoint de escritura en lote | Listado de matrículas con estado y legajo (ya existe) |
| Validación de los 4 valores y del estado de la cohorte | Evento nuevo (Roadmap no lo necesita: el archivado ya publica `COURSE_COHORT_ARCHIVED`) |
| Códigos de error según #148 | Scope M2M: lo llama el front con el token del profesor |

---

## Título

`[T10 · Roadmap] Pedido: endpoint para cargar el estado académico final (hoy no se puede archivar una cohorte con alumnos)`

## Cuerpo

### Problema

`CohortArchiveRules` rechaza el archivado con `409 MISSING_FINAL_ACADEMIC_STATUS` mientras haya una matrícula `VALIDATED` activa sin `finalAcademicStatus`. Pero ningún endpoint ni servicio escribe ese campo: en `develop` (`01c8df4`) solo lo leen `EnrollmentMapper` y `EnrollmentResponseDto`, y lo setean los tests.

Resultado: **ninguna cohorte con alumnos validados se puede archivar**, `COURSE_COHORT_ARCHIVED` nunca sale y Roadmap nunca pasa el roadmap y el ranking a solo lectura (RF-CUR-09).

### Pedido

Un endpoint para que el profesor cargue el estado final de los alumnos de su cohorte. El front lo usa desde la pantalla de cierre de Roadmap (HU-72): ahí el profesor ve los candidatos P90/P10 del ranking, elige el estado de cada alumno, confirma y después archiva con el `POST /course-cohorts/{id}/archive` de ustedes.

```
PUT /api/course/course-cohorts/{courseCohortId}/final-academic-statuses
Content-Type: application/json

{
  "items": [
    { "enrollment_id": "7c1e…", "final_academic_status": "PROMOTED" },
    { "enrollment_id": "a40b…", "final_academic_status": "REGULAR" }
  ]
}
```

- **200** → `{ "items": EnrollmentResponse[] }` con las matrículas actualizadas.
- **Lote atómico:** si un ítem falla, no se guarda ninguno.
- **Se puede volver a llamar** para corregir mientras la cohorte esté `ACTIVE`. El último valor gana.
- **No hace falta mandar a todos.** Los que no vienen quedan como estaban, así que se puede guardar de a partes. El archivado ya controla que no falte ninguno.

### Reglas

| Caso | Respuesta |
|---|---|
| El que llama no tiene escritura en la cohorte (`membership.isCanWrite()`, igual que `archive` y `reject`; GESTOR sí, `PROFESSOR_READ_ONLY` no) | 403 `FORBIDDEN` |
| La cohorte no existe o está inactiva | 404 `NOT_FOUND` |
| La cohorte no está `ACTIVE` (DRAFT o ARCHIVED) | 409 `COURSE_COHORT_NOT_ACTIVE` (o el código que ya usen para eso) |
| Valor fuera de `system_parameter` `FINAL_ACADEMIC_STATUS` | 400 `VALIDATION_ERROR`, con `errors[]` = `{ field: "items[i].final_academic_status", code: "VALIDATION_INVALID_VALUE", params: { allowed: [...] } }` |
| Matrícula que no es de esa cohorte, o que no está `VALIDATED` y activa | 409 `COURSE_ENROLLMENT_NOT_FINALIZABLE`, con `params.enrollmentId` |
| `items` vacío o con un `enrollment_id` repetido | 400 `VALIDATION_ERROR` |

- Que quede registrado quién y cuándo cargó el estado (`lastUpdatedUser` / `lastUpdatedDatetime` de la matrícula, como en `reject`).
- OpenAPI en `swagger.yaml`, con los códigos nuevos en el enum de `code` (#148).

### Criterios de aceptación

1. Con todas las matrículas `VALIDATED` cargadas, `POST /course-cohorts/{id}/archive` deja de responder `MISSING_FINAL_ACADEMIC_STATUS`.
2. `GET /course-cohorts/{id}/enrollments` devuelve el `final_academic_status` cargado, y el alumno lo ve como `condition`.
3. Un profesor `PROFESSOR_READ_ONLY` recibe 403, y una cohorte archivada responde 409.
4. Un valor inválido no guarda nada del lote.

### Para conversar

- ¿Prefieren `enrollment_id` o `student_id` en los ítems? Nosotros tenemos los dos: `student_id` sale del ranking y `enrollment_id` del listado de ustedes.
- ¿Algún estado se puede cargar antes del fin de la cursada? Por ejemplo, `DROPPED_OUT` en el momento en que el alumno deja.

Si les parece bien, **el PR lo armamos nosotros (G10)** contra `develop`, siguiendo el patrón de `reject` y los tests de `CourseCohortArchiveApiTest`, y se lo pasamos para revisión. Si prefieren otro contrato, avísennos en este issue antes de que lo empecemos.
