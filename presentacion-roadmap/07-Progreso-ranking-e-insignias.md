---
tags: [presentacion, roadmap]
---

# 7. Progreso, experiencia y ranking

## Lo que decimos

«Sigamos el recorrido completo de un resultado, desde el desafío hasta la pantalla de ranking. Primero, Courses aporta el marco académico: la cohorte, sus inscriptos y comisiones. El Motor administra el intento, lo resuelve y calcula la experiencia que corresponde al resultado. Una vez que el resultado está disponible, lo comunica mediante un evento que Roadmap puede consumir.

> [!info]- Detalle técnico: evento del Motor
> `RoadmapEventListener` despacha `CHALLENGE_COMPLETED`, `CHALLENGE_ABORTED` y `CHALLENGE_RESULT_RECTIFIED`. Los eventos son transportados por Kafka y su recepción depende de configuración. Ver `B/java/com/utn/tpi/roadmap/events/RoadmapEventListener.java`.

A partir de ese mensaje empieza nuestro trabajo de progreso. Roadmap verifica el contexto y registra el movimiento de experiencia recibido en su libro de movimientos. Con esos movimientos actualiza el acumulado que corresponde al alumno y al ámbito del recorrido. Si el resultado reúne las condiciones de aprobación, registra además la actividad como completada. Esa actualización puede disparar la evaluación de insignias y reflejarse en los estados visibles del mundo.

> [!info]- Detalle técnico: cálculo y ledger de XP
> El Motor calcula el XP base; `ProgressService` aplica el valor recibido, incluso cuando no hay aprobación, y completa el nodo cuando corresponde. `xp_movement` identifica eventos y controla duplicados; el ámbito depende de si el roadmap agrega XP al curso. Ver `B/java/com/utn/tpi/roadmap/services/ProgressService.java` y `entities/XpMovementEntity.java`.

El resultado del desafío y nuestro cálculo del acumulado cumplen funciones distintas. El Motor conoce el intento y determina su resultado. Nosotros incorporamos la experiencia informada, conservamos los movimientos y la integramos con el progreso del recorrido. Esto nos da una base para mostrar nivel, avance e historial y para construir el ranking de la cohorte o de un roadmap, según la consulta.

Para construir la clasificación combinamos varias piezas. Tomamos los inscriptos activos y la información de comisiones de Courses. Sumamos nuestros movimientos y progreso: experiencia, actividades completadas e insignias. Incorporamos datos de vidas desde Accounting, perfiles desde Users y notas según la fuente disponible. El servicio arma las filas y las ordena por la métrica elegida, que puede ser experiencia o nota. La nota local contempla la mejor nota por desafío y también existe una fuente del Motor.

> [!info]- Detalle técnico: composición del ranking
> `RankingService` reúne alumnos, XP, insignias, completados, vidas y notas; `RankingMotorScores` contempla origen Motor y el promedio local usa mejor nota por desafío. Ver `B/java/com/utn/tpi/roadmap/services/RankingService.java` y `RankingMotorScores.java`.

Para entender los empates, pensemos una clasificación por XP de tres personas. Ana y Bruno tienen **1.000 XP, 3 insignias, 1 vida perdida, 8 ejercicios completados y la misma hora de último movimiento positivo**. Carla tiene 900 XP. Para ordenar, se compara primero la métrica elegida —XP o nota promedio, de mayor a menor— y, ante igualdad, se mira en este orden: más insignias; menos vidas perdidas; más ejercicios completados; y hora más temprana de XP registrada. En ranking por nota, el XP total no se usa como criterio adicional. Si Ana tuviera una insignia más que Bruno, quedaría antes y no haría falta mirar los demás criterios.

Si falta el dato de vidas para alguien del grupo empatado en métrica e insignias, ese criterio se neutraliza para todo ese grupo. La hora registrada corresponde al último movimiento positivo recibido por Roadmap, no necesariamente al momento real del logro. Con diez o más filas, la clasificación que contempla promoción puede priorizar antes a quienes cumplen las condiciones de elegibilidad; la cascada se aplica dentro de ese orden.

> [!info]- Detalle técnico: desempate y elegibilidad
> `_presentacion-src/tpi-roadmap/src/main/java/com/utn/tpi/roadmap/services/RankingRules.java:40-61`, `:127-153`; neutralización y elegibilidad en `RankingService.java:321-345`.

En nuestro ejemplo Ana y Bruno empatan en **todos** los criterios. El servidor conserva el orden de entrada entre ellos y devuelve puestos **1, 1, 3**: comparten el primer puesto y Carla queda tercera. Es lo que se conoce como *competition ranking*. Para tres participantes, el percentil calculado por la fórmula del servidor sería 100, 100 y 33; no hay zonas extremas porque el mínimo es diez.

> [!info]- Detalle técnico: puesto compartido
> `_presentacion-src/tpi-roadmap/src/main/java/com/utn/tpi/roadmap/services/RankingRules.java:85-103`, `:112-117`, `:158-180`.

Hay una diferencia importante entre una **función auxiliar** y la pantalla conectada: la función `rankBy` del front, si recibe esas tres filas, asigna **1, 2, 3**, aunque Ana y Bruno sigan iguales; con la misma fórmula esos puestos darían 100, 67 y 33. A partir de diez participantes una renumeración también podría afectar las zonas. Pero en el código vigente inspeccionado no encontramos llamadas productivas a esa función: el adaptador HTTP mapea el puesto, percentil y zona recibidos del servidor. Por eso **no afirmamos que la pantalla integrada renumere el empate**; si en la demo se observa otra cosa, la mostramos como comportamiento observado y revisamos la configuración y el recorrido concreto.

> [!info]- Detalle técnico: función auxiliar frente a pantalla
> `_presentacion-src/fe/src/app/features/ranking/domain/ranking.rules.ts:177-224` numera consecutivamente; `_presentacion-src/fe/src/app/features/ranking/data-access/ranking-http/ranking-mapper.ts:71-76` conserva los valores recibidos. El cálculo de percentil y zonas del servidor está en `_presentacion-src/tpi-roadmap/src/main/java/com/utn/tpi/roadmap/services/RankingRules.java:158-186`.

Además del ranking individual, el docente puede observar comparaciones por grupo a partir de integrantes y resultados disponibles. Las insignias del sistema y del curso agregan otra forma de reconocer hitos; el docente administra el catálogo del curso y el alumno consulta las que recibió. Si después llega una rectificación del Motor, registramos la diferencia de experiencia y ajustamos el resultado y el progreso que correspondan. Así el recorrido refleja también las correcciones posteriores.

> [!info]- Detalle técnico: insignias y rectificación
> `BadgeEvaluator` evalúa criterios y `BadgeEventService` publica premios por outbox. `ProgressService` valida revisión y registra delta con signo; una desaprobación puede reabrir si no queda otra aprobación. Ver `B/java/com/utn/tpi/roadmap/services/BadgeEvaluator.java` y `ProgressService.java`.

En resumen, el ranking reúne información de varios equipos, pero la convierte en una lectura propia del recorrido: desde el resultado del Motor hasta el avance y la presentación que consulta cada usuario.

El recorrido de datos también nos permite distinguir lo que estamos viendo: una posición es una forma de ordenar el conjunto, una zona es una lectura relativa de esa posición y el progreso muestra actividades del camino. Cuando el docente compara comisiones, el front construye promedios con los integrantes encontrados en las filas disponibles. Así cada vista responde a una pregunta diferente, usando el mismo contexto de cursada.

**Transición:** «Con esta información individual disponible, pasemos a la vista que ayuda al docente a seguir a toda la comisión».»

## Qué se ve en pantalla
Mostrar XP, insignia obtenida y ranking con datos ficticios preparados; si hay empate real, señalar explícitamente la diferencia de presentación. Mostrar comparación de comisiones si hay al menos dos con alumnos.

## Preguntas probables

**¿Quién calcula el XP base?** El Motor; Roadmap registra movimientos y calcula el acumulado correspondiente.

**¿Por qué podría diferir un cálculo auxiliar del front?** `rankBy` numera consecutivamente, pero la pantalla HTTP inspeccionada conserva valores del servidor; no afirmamos divergencia visual sin probarla.

**¿Qué significa reached_first?** Hora del último movimiento positivo registrado por Roadmap, no necesariamente del logro real.

**¿Siempre hay zonas de ranking?** No; los cortes requieren al menos diez inscriptos.

**¿El ranking determina promoción?** No; aporta indicadores y candidatos, y Courses mantiene el estado académico.

**¿El ranking siempre es anónimo?** La visibilidad depende de configuración; no se garantiza anonimato universal.

**¿Una rectificación puede reabrir un nodo?** Sí, si una desaprobación deja al nodo sin otra aprobación válida; examen tiene tratamiento específico.
