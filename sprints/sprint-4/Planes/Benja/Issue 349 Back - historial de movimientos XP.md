---
tags: [tpi, g10, sprint-4, plan, back, roadmap, xp, accounting]
fecha: 2026-10-27
autor: Benjamin Polzoni
estado: borrador
issue: https://github.com/2026-P4-BE/tpi-roadmap/issues/349
repo: 2026-P4-BE/tpi-roadmap
base: origin/develop 6268b669 (2026-10-27)
worktree: /Users/benjaminpolzoni/orca/workspaces/tpi-roadmap/issue-349-xp-history
rama: feature/issue-349-xp-history
---

# Issue #349 · Historial de movimientos XP para inventario (Accounting T08)

> [!info] Alcance
> Exponer el ledger **existente** de Roadmap al frontend para mostrar XP junto a monedas y vidas. Accounting no almacena XP, no consume otro evento y no requiere scope M2M ni trabajo de plataforma. Este plan es una propuesta de implementación; no hay código cambiado todavía.

## Diagnóstico verificado en `origin/develop`

- `XpHistoryController` tiene `@Profile("dev")`: en mesh sin ese perfil la ruta no existe. El README la presenta como depuración. `docs/api_doc/swagger.json` tampoco documenta la ruta.
- `XpMovementView` devuelve solo `challenge_id`, `roadmap_id`, `xp`, `recorded_at`, `required_minimums_met`, `score` y `max_score`; la entidad ya guarda el resto de los datos pedidos. No hace falta migración.
- `XpMovementRepository.findByStudentIdAndCourseCohortId` consulta por cohorte y alumno, **sin filtrar `roadmap_id` ni `counted_in_course`**: el historial actual mezcla movimientos de todos los roadmaps de la cohorte. Conviene conservar esta semántica y explicitarla.
- La autorización del historial no incluye GESTOR. `StudentDashboardController` sí contempla ADMIN/GESTOR/profesor dueño/alumno propio. Su `xp-timeline` además exige matrícula activa; el historial actual no hace esa comprobación.
- La ordenación por defecto solo usa `recordedAt DESC`; empates pueden cambiar la composición de páginas. El parámetro `size` no tiene tope propio.
- `ProgressService.applyRectification` persiste `xp = expectedXp - priorXp`; el delta puede ser negativo. `post_pass_repeat=true` **no implica** que la fila tenga `xp=0`: una rectificación que congela en cero un intento antes remunerado puede guardar un delta negativo.
- El balance del curso (`StudentCourseEntity.totalXp`) se modifica solo si `countedInCourse=true`. El XP propio de un roadmap en modo ROADMAP se obtiene sumando sus movimientos `countedInCourse=false`. `LevelService` exige matrícula activa aun para lecturas actuales; no prometer equivalencia para alumnos desmatriculados sin probar el escenario.

## Contrato propuesto / decisiones a validar

1. Promover la ruta actual `GET /courses/{courseId}/students/{studentId}/xp-history` a producto: quitar `@Profile("dev")`, cambiar tag/Javadoc, conservar paginación y añadir `@Operation` con alcance, autorización y semántica. No crear otra ruta duplicada.
2. Autorizar como en dashboard: alumno **solo propio**, ADMIN, GESTOR o profesor dueño de la cohorte. Usar guard de propiedad que exima a ADMIN y GESTOR; añadir pruebas para gestor y profesor ajeno. Evitar una condición basada solo en igualdad de UUID sin rol STUDENT.
3. Mantener la lectura del ledger histórico sin `requireEnrolled` ni veto por cohorte archivada, para que el alumno pueda consultar hechos pasados. **Validar explícitamente** el caso de alumno desmatriculado, la identidad del alumno y las reglas de Courses/Gateway antes de fijarlo como contrato público. Si una restricción externa impide esta decisión, documentar 403/404 y acordarlo con Accounting.
4. Ampliar `XpMovementView` con `id_attempt` (desde `attemptId`), `node_id`, `section_id`, `result_revision`, `previous_result_revision`, `counted_in_course`, `post_pass_repeat`, `status` y `attempt_number`, manteniendo los siete campos actuales. `@JsonProperty` explícito para snake_case y nulabilidad de datos legacy.
5. Orden fijo `recorded_at DESC, id DESC` en el servidor, no controlado por `sort` del cliente; el UUID de movimiento desempata sin alterar el orden temporal. `page >= 0`, `size` por defecto 20 y máximo 200 (rechazar valores fuera de rango con 400, o documentar si se adopta clamp). Tests con timestamps idénticos entre páginas.
6. Historial por curso: **todas** las filas de la cohorte; el frontend filtra/agrupará visualmente usando `roadmap_id` y `counted_in_course`. `xp_total`/`total_xp` de curso cierran con la suma firmada de las filas `counted_in_course=true` para una matrícula consistente; las `false` se muestran separadas o etiquetadas, no se suman al saldo del curso. Aclarar que `/roadmaps/{id}/.../level` en modo ROADMAP tiene otro ámbito.
7. No añadir en este cambio `/students/me/xp-history`, variante por roadmap ni `group_id`: el front ya conoce su ID, puede resolver el roadmap mediante `roadmap_id`, y `group_id` no altera el ledger. Reconsiderar variante por roadmap solo con un consumidor concreto.

## Pasos de implementación

1. **Tests primero:** extender `XpHistoryControllerTest` para perfil sin `dev`, roles, lectura histórica, `size` inválido y desempate estable. Agregar test de serialización/mapeo de `XpMovementView` con rectificación negativa, campos nulos legacy y `counted_in_course=false`.
2. Modificar controlador, DTO y, si conviene para imponer el orden fijo, consulta/servicio de repositorio. No cambiar escritura del ledger ni migraciones.
3. Documentar respuesta paginada real de `ApiEnvelopeAdvice` (no asumir exactamente el ejemplo de Accounting), semántica de delta firmado, mezcla de roadmaps, campos nulos, autorización, máximo de página y códigos de error. Actualizar `README.md` y regenerar `docs/api_doc/swagger.json` mediante `SpringDocConfigTest`.
4. Verificar tests focalizados y `mvn verify` (Checkstyle/PMD/CPD). Inspeccionar diff de OpenAPI y comprobar que no entran secretos ni cambios locales del checkout `develop`. PR hacia `develop` con merge commit.
5. Responder en la issue las cinco preguntas con la semántica comprobada y ejemplos de corrección negativa/repetición. Coordinar con Accounting el criterio de mostrar movimientos `counted_in_course=false` y el resultado de la lectura de cursos cerrados.

## Preguntas de la issue: respuesta prevista

1. **Signo:** sí, `xp` es delta firmado; una rectificación puede ser negativa.
2. **Saldos:** para el curso, sumar solo `counted_in_course=true`; las filas `false` son XP de ámbito ROADMAP y no deben mezclarse con `xp_total` del curso. Verificar migraciones/fixtures legacy antes de afirmar identidad matemática universal.
3. **Desmatriculado/archivado:** proponer lectura del historial pasado sin matrícula activa ni bloqueo por archivado; requiere test de integración y validación de autorización. Hoy el controlador no exige matrícula activa.
4. **Repetición:** no siempre cero por fila; el total neto del intento repetido queda cero, pero una rectificación compensatoria puede ser negativa.
5. **Variantes:** la ruta de cohorte mezcla roadmaps; `roadmap_id` permite separarlos. No se necesita `group_id` para el ledger. Las rutas `me` y por roadmap quedan fuera de este pedido salvo feedback de Accounting.

## Riesgos y fuera de alcance

- La lectura histórica debe evitar exposición cruzada de alumnos/cohortes, especialmente si Courses no reconoce matrículas inactivas.
- La paginación por offset con orden total es estable ante empates, pero **no es snapshot**: inserciones nuevas entre solicitudes pueden desplazar filas. No prometer inmunidad a escrituras concurrentes.
- Las rectificaciones se muestran como movimientos separados, no se reescriben filas anteriores. El frontend correlaciona por `id_attempt` y revisión.
- Sin cambios de Accounting, Gateway, Kafka, esquema de base de datos ni frontend en este PR.
