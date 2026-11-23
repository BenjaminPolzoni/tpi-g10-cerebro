# Gamificación y seguimiento — foto de origin/develop

Revisión estática de `_presentacion-src/tpi-roadmap` (HEAD `9337a823`) y `_presentacion-src/fe` (HEAD `d1c5766227`), sin ejecución ni repos antiguos. `B` = `_presentacion-src/tpi-roadmap/src/main/`, `F` = `_presentacion-src/fe/src/`, `C` = `tpi-g10-cerebro/`. Las líneas son de esos árboles. Código presente no acredita despliegue, contrato aceptado por otro equipo ni integración funcionando. En particular no inspeccionamos el código propio de Courses ni del Motor: sus responsabilidades vienen de los contratos del cerebro y de los clientes de Roadmap, no son una certificación de sus ramas actuales.

## Ranking: fuentes, cálculo y vistas

### Explicación de producto/técnica media

El Motor resuelve intentos y envía resultados; Courses es dueño de matrículas y comisiones; Accounting informa vidas, Users perfiles y Backoffice parámetros. Roadmap integra esas piezas con su propio avance, arma el ranking y expone vistas para alumno y docente; el front presenta y también recalcula algunas vistas. No confundamos «Roadmap suma y contabiliza XP» con «Roadmap corrige el desafío»: el valor de resultado llega del Motor. El ranking admite orden por XP o nota, vistas por comisión y comparación de grupos; no es un acta académica.

### Detalle técnico

- **Código**: listener de `CHALLENGE_COMPLETED`, `CHALLENGE_ABORTED` y `CHALLENGE_RESULT_RECTIFIED` (`B/java/com/utn/tpi/roadmap/events/RoadmapEventListener.java:144`, `:177`); matriculación/baja/archivo desde Courses (`B/java/com/utn/tpi/roadmap/events/CoursesLifecycleEventListener.java:34`, `:92`). Ledger `xp_movement`, acumulado `student_course`, completados `completed_node`, y premios `badge_award` (`B/java/com/utn/tpi/roadmap/entities/XpMovementEntity.java:31`, `StudentCourseEntity.java:20`, `CompletedNodeEntity.java:28`, `BadgeAwardEntity.java:24`). `ProgressService.java:180-205` aplica XP recibido incluso si no aprueba, completa si aprobó y evalúa insignias. Los roadmaps que no agregan XP al curso tienen ámbito propio; no sumar dos veces.
- `RankingService.java:313-350` combina inscriptos activos, insignias, completados, vidas y notas. La nota local es promedio de la mejor nota por desafío (`:354`); existe fuente del Motor (`RankingMotorScores.java:33`), por lo que no debe presentarse una única fuente como garantizada en todo ambiente. XP/nota decreciente; desempate: más insignias, menos vidas perdidas, más ejercicios completos, antes alcanzó XP (`RankingRules.java:44-61`). Si faltan vidas para alguien del grupo empatado en métrica e insignias, se neutraliza ese criterio para ese grupo (`RankingService.java:320-331`).
- `xp_reached_at` es el último movimiento positivo registrado por Roadmap, truncado al segundo; no es hora real del resultado: el comentario advierte retrasos y orden de consumo entre particiones (`RankingService.java:358-375`, `XpMovementRepository.java:219-234`). `reached_first` no es «quien inició antes» ni necesariamente quien realmente logró antes el puntaje.
- **DEC-022: diferencia vigente**. Back comparte puesto si coinciden todos los criterios y luego saltea puestos (1, 1, 3: `RankingRules.java:93-101`); marca `shared` (`:248-260`). Front asigna posiciones consecutivas en `rankBy` (`F/app/features/ranking/domain/ranking.rules.ts:188-223`) y normaliza posiciones del curso (`:306-316`). Por lo tanto una zona visual puede diferir de la devuelta por back en empates; no afirmar equivalencia. Front rankea grupos por sus promedios y omite grupos sin miembros presentes (`:247-285`); eso es comparación de grupos, no prueba por sí sola de un ranking agregado entre cohortes distintas.
- Ranking backend `GET /api/roadmap/courses/{courseId}/ranking` y por roadmap (`B/java/com/utn/tpi/roadmap/controllers/RankingController.java:89`, `:140`); UI `F/app/features/ranking/pages/ranking-page/ranking-page.component.ts:982`. La privacidad y visibilidad dependen de vista/configuración: no mostrar identidad real ajena sin probar permisos.

## Rectificaciones y progreso

### Explicación de producto/técnica media

Una rectificación del Motor puede modificar XP y resultados: Roadmap conserva movimientos y ajusta el progreso. **Corrección importante:** no se puede decir que el completado sea universalmente monótono. Una revisión puede reabrir un nodo; lo que no debe confundirse con borrar toda la historia o deshacer automáticamente todo lo desbloqueado.

### Detalle técnico

`ProgressService.java:250-328` valida inscripción, identidad, revisión y evidencia; obtiene XP previo por intento y registra delta con signo, no reemplaza a ciegas el ledger. Una desaprobación puede reabrir si no hay otra aprobación; una suba del objetivo puede requerir rehacer. Reintentos posteriores a aprobación no vuelven a pagar, y exámenes no se reabren (`:275-306`, `:357-365`). El listener recibe el evento (`RoadmapEventListener.java:177-196`); la idempotencia de eventos y revisiones tiene controles específicos, no equivale a garantía de entrega exactamente una vez. Al completar se persiste/revive el registro y se emite por outbox (`ProgressService.java:224-240`). No se verificó aquí exhaustivamente la reversión de cada desbloqueo, insignia o nivel.

## Insignias

### Explicación de producto/técnica media

Roadmap mantiene insignias del sistema y del curso; el docente puede administrar el catálogo de su curso y el alumno consultar sus logros. Se otorgan al evaluar condiciones propias del progreso; Motor aporta resultados, Courses el ámbito de cursada y Accounting puede aportar señales de vidas. Una notificación externa depende de su consumidor.

### Detalle técnico

**Código**: catálogo y estadísticas `GET /courses/{courseId}/badges` y `/badges/stats`; alta `POST`, edición `PUT /badges/{badgeId}`, visibilidad `PUT .../{badgeId}/hidden`, baja `DELETE` (`B/java/com/utn/tpi/roadmap/controllers/BadgeCatalogController.java:70-178`, prefijo `/api/roadmap`). Premios `GET /courses/{courseId}/students/{studentId}/badges` (`BadgeController.java:49`). Evaluación tras resultado y XP (`ProgressService.java:200-205`, `BadgeEvaluator.java:91`) y publicación `BADGE_AWARDED` por outbox (`BadgeEventService.java:35`). Hay chequeos de recuperación y sección sin pérdidas (`BadgeCriteriaChecks.java:154`); no se acreditó cada criterio y disparador extremo a extremo.

## Zonas y portales

### Explicación de producto/técnica media

Son dos conceptos distintos: las zonas del ranking indican posición relativa y las zonas del mundo/portales organizan visualmente el recorrido. Roadmap construye el mapa; Courses aporta las unidades de la cursada; el front crea la experiencia visual. Un portal dibujado no demuestra por sí mismo una regla de acceso de negocio.

### Detalle técnico

En ranking, con menos de 10 inscriptos no hay cortes; P90 y P10 corresponden a los extremos y se calcula el corte por tamaño del decil (`B/java/com/utn/tpi/roadmap/services/RankingRules.java:81`, `:178-207`). Promoción exige P90, cero vidas perdidas y 100% de obligatorios; riesgo P10 y obligatorios incompletos (`:219-231`); hay ajuste por elegibilidad al rankear (`:127-153`). Son candidatos, no estado académico definitivo. En el front existen estilos de portal por bioma (`F/app/features/roadmap/engine/zone-portal-styles.ts:20`, `:638`) y composición de posiciones en `F/app/features/roadmap/domain/world-gen/zone-islands.spec.ts:80` (test como evidencia de intención, no de ejecución). El modelo y los ejemplos de nodos/relaciones están en `C/arquitectura/mapa-modelo-neo4j.md`, `C/demo-neo4j/` y DEC-016/018/021; esas guías son documentación, no prueba de que un determinado grafo esté cargado.

## Examen

### Explicación de producto/técnica media

Hay implementación específica de nodo examen y de su elegibilidad: no es solamente una idea. El Motor sigue siendo quien crea y resuelve el intento. No se verificó la experiencia completa ni la integración real de horarios con Courses.

### Detalle técnico

`NodeType.EXAM` existe aunque su comentario histórico hable de fase 3 (`B/java/com/utn/tpi/roadmap/models/NodeType.java:20`); la creación/edición exige tiempo límite (`GraphService.java:399`, `:473`). Gate indica `is_exam` y tipo `EXAM` (`ChallengeParameterResolver.java:52`, `GateService.java:151`, `GateDtos.java:39-53`); el contrato expresa que se rinde sin reservar vidas. `ChallengeWindowController.java:55` expone ventanas; no asumir que el flujo real de agenda está conectado. En rectificación, examen no se reabre (`ProgressService.java:275-280`).

## Cierre de curso HU-72

### Explicación de producto/técnica media

Courses es dueño del estado académico final; Roadmap aporta datos y candidatos, no decide por el profesor ni sustituye el registro académico. Recibe el evento de archivado de cohorte. El cierre manual completo y exportación no se pueden vender como terminados a partir de esta revisión.

### Detalle técnico

**Código Roadmap**: `COURSE_COHORT_ARCHIVED` llama `archiveCohort` (`B/java/com/utn/tpi/roadmap/events/CoursesLifecycleEventListener.java:101`, `:133`); reglas candidatas en `RankingRules.java:219-231`. **Plan/cerebro, no verificado en Courses actual**: HU-72 describe confirmación docente y `PROMOTED`, `REGULAR`, `NOT_REGULAR`, `DROPPED_OUT` (`C/sprints/sprint-3/historias/HU-72 Cerrar el curso con el estado académico final.md:39`). El plan de sprint 4 afirma que faltaba endpoint de escritura en lote en la revisión histórica (`C/sprints/sprint-4/Planes/Benja/HU-72 Back+Front - cierre del curso y roadmap archivado.md:34-46`); no inferir que sigue faltando hoy sin auditar Courses. En los dos árboles revisados no se encontró implementación Roadmap de `finalAcademicStatus`.

## Dashboard de cohorte y salud

### Explicación de producto/técnica media

Backoffice es dueño del dashboard global y parámetros; Roadmap ofrece datos de avance, evolución y salud por alumno. La existencia de endpoints no prueba que G06 ya los consuma ni que sean el healthcheck técnico del servicio.

### Detalle técnico

`GET /api/roadmap/courses/{courseId}/progress/summary` y `/xp-timeline` (`B/java/com/utn/tpi/roadmap/controllers/CohortDashboardController.java:61`, `:91`). Salud individual `GET /courses/{courseId}/students/{studentId}/health` y variante `students/me/health`: consulta compuesta de lectura, con autorización y scope técnico `roadmap.health.read` (`HealthController.java:35`, `:70`, `:94-107`). XP por período incluye movimientos correctivos (`services/dashboard/CohortPeriodStatsService.java:32`). Curva efectiva desde parámetros (`services/EffectiveCourseParameterService.java:104`).

## Intentos y feedback del alumno

### Explicación de producto/técnica media

El mapa guía al alumno, informa impedimentos y lo lleva al intento; el Motor controla el intento y la corrección, y el servicio de desafíos entrega contenido. El feedback que efectivamente recibe depende de esos servicios y del estado de la integración; no confundir el aviso de guardado docente con devolución de corrección al alumno.

### Detalle técnico

El front hace prechequeo del gate y solicita al Motor crear intento con `course_id`, `node_id`, `attempt_type`; el Motor vuelve a evaluar el gate (`F/app/features/roadmap/data-access/challenge-attempt/challenge-attempt.service.ts:110-112`, `:231-242`). Maneja agotamiento y cooldown (`:197-201`), contempla reintento de preparación de práctico y doble clic (`:119-122`, `:261`). Excepciones individuales de cantidad de intentos reemplazan el total del nodo, no se suman (`F/app/features/roadmap/data-access/student-exceptions/student-exception.models.ts:2-12`). El feedback detallado de corrección y su persistencia no fueron auditados en el Motor: evitar afirmar campos, calidad o disponibilidad.

## Dudas para el usuario

1. ¿Qué ambiente, versiones, flags y cuentas reales se usarán para validar las vistas y permisos?
2. ¿Se desea comparar comisiones/grupos de una misma cohorte o cohortes distintas? La evidencia citada solo demuestra la primera construcción, no comparación global entre cohortes.
3. ¿Se acordó con G01 la escritura de `finalAcademicStatus` y existe flujo de cierre desplegado? El plan histórico no responde el estado actual.
4. ¿Cómo quieren explicar en la demo el empate compartido en back frente al puesto consecutivo visual y la hora de consumo usada por `reached_first`?
5. ¿G06 consume ya el resumen, la serie y salud individual? ¿Qué contrato de servicio técnico tiene habilitado?
6. ¿Qué resultados y feedback de intentos del Motor se mostrarán y se pueden probar con datos reales?
