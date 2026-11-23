---
tags: [presentacion, roadmap]
---

# 8. Seguimiento docente y cierre

## Lo que decimos

«Hasta ahora seguimos a un alumno. Cambiemos de perspectiva y pensemos en el docente que necesita acompañar a un grupo completo. En la pantalla de seguimiento puede elegir una comisión y consultar, para cada estudiante, su experiencia y el avance expresado como nodos completados sobre el total. Es una manera directa de ver cómo se mueve el grupo por el recorrido que acabamos de construir.

Cuando la cohorte tiene al menos dos comisiones, la interfaz ofrece una comparación entre ellas. Esto permite observar diferencias de avance dentro de la misma cursada y decidir dónde conviene profundizar el acompañamiento. El docente puede complementar esa mirada con el ranking de la cohorte y con la inspección de las actividades del mapa. Son perspectivas distintas sobre la misma experiencia: una muestra la estructura, otra el recorrido individual y otra la evolución del grupo.

> [!info]- Detalle técnico: progreso por comisión
> `GroupProgressPageComponent` consulta la comisión seleccionada y construye la tabla comparativa; el enlace al ranking corresponde a la cohorte completa. Ver `F/app/features/roadmap/pages/group-progress-page/group-progress-page.component.ts`.

También hay una vista general de cohorte en Courses que reúne bloques de información. Roadmap aporta datos como el resumen de progreso y la evolución de experiencia. El bloque de riesgo o salud que integra esa pantalla pertenece al ámbito de Backoffice y está sujeto a la capacidad correspondiente. Además, Roadmap dispone de una consulta de salud individual. El valor de la integración está en poder combinar datos especializados y presentarlos de manera útil para el seguimiento.

> [!info]- Detalle técnico: dashboard y salud
> Roadmap expone `/courses/{courseId}/progress/summary`, `/xp-timeline` y salud individual. La UI de Courses consulta resumen y serie; su bloque de riesgo proviene de Backoffice. Ver `B/java/com/utn/tpi/roadmap/controllers/CohortDashboardController.java`, `HealthController.java` y `F/app/features/courses/pages/cohort-dashboard-page/cohort-dashboard-page.component.ts`.

Al final de la cursada, el estado académico corresponde a Courses: un gestor o docente autorizado registra la condición final, y Courses verifica requisitos antes de archivar. La pantalla de calificaciones también ofrece exportación CSV; no la presentamos como un acta oficial.  Desde Roadmap aportamos indicadores y candidatos construidos sobre la información del recorrido. También reaccionamos al evento que comunica el archivo de la cohorte: actualizamos el estado de sus roadmaps para acompañar ese cierre. Así conservamos clara la responsabilidad de cada servicio en una etapa especialmente importante para el docente.

> [!info]- Detalle técnico: archivo y HU-72
> Courses implementa escritura de estados (`_presentacion-src/tpi-course/src/main/java/ar/edu/utn/frc/tup/p4/controllers/EnrollmentsApi.java:445`) y archivo con validaciones (`_presentacion-src/tpi-course/src/main/java/ar/edu/utn/frc/tup/p4/controllers/CourseCohortsApi.java:127`). El CSV de calificaciones se genera en el front (`_presentacion-src/fe/src/app/features/courses/pages/cohort-grades-page/cohort-grades-page.component.ts:813`). Roadmap reacciona al archivo (`_presentacion-src/tpi-roadmap/src/main/java/com/utn/tpi/roadmap/events/CoursesLifecycleEventListener.java:92`); no se probó el circuito completo.

El seguimiento completa el circuito de valor: el docente diseña el camino, el alumno avanza y la información vuelve a quienes necesitan acompañar la cursada. Para cerrar, veamos cómo circula técnicamente esa información entre equipos.

Al elegir una comisión, la tabla facilita pasar de la impresión general a una conversación concreta sobre avance. El resumen de cohorte y la serie de experiencia agregan otra escala temporal: ayudan a observar la evolución del conjunto. La combinación resulta útil para acompañar el proceso mientras ocurre, no solo al final, y para volver al mapa cuando una actividad requiere atención especial.

**Transición:** «Terminemos con las integraciones y las decisiones que hacen posible conectar todas estas piezas».»

## Qué se ve en pantalla
Con cuenta docente mostrar seguimiento por comisión y tabla comparativa. Si está habilitado, abrir el dashboard de Courses e identificar la procedencia de cada bloque; no ejecutar cierre sobre datos de demo principal.

## Preguntas probables

**¿La comparación es entre cohortes?** La evidencia corresponde a comisiones de una misma cohorte.

**¿El ranking enlazado filtra la comisión?** No; corresponde a la cohorte completa.

**¿Roadmap es dueño del dashboard general?** No; la vista general está en Courses y combina aportes.

**¿El cierre HU-72 está terminado de punta a punta?** Courses implementa registro y archivo, y el front exporta calificaciones; queda validar el circuito integrado y el alcance exacto del CSV.

**¿Salud de alumno es el healthcheck técnico?** No; son conceptos diferentes.
