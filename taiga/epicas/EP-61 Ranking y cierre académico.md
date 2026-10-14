---
tags: [tpi, g10, taiga, epica]
ref: 61
estado: "New"
responsable: "Sin asignar"
avance: "2/2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/61
---

# EP-61: Ranking y cierre académico

> [!info] Generado desde Taiga (2026-10-14 20:45). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/61) · Estado: **New** · Responsable: **Sin asignar** · HU cerradas: **2/2**

[G10] — Ranking y cierre académico
----------------------------------

* * *

Objetivo
--------

Exponer la posición relativa del alumno respetando las reglas de visibilidad del PRD, con percentiles P90/P10 y desempate en cascada. El cierre académico —confirmación del estado final y resumen exportable— queda diferido a una fase futura.

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: el XP ordenante se suma del ledger propio xp\_movement, que persistimos nosotros. Las vidas perdidas históricas se consultan a Inventario. Los percentiles P90/P10 sólo se activan en cursos con 10 o más inscriptos (RF-RNK-09). Los perfiles (nombre, apellido, legajo, avatar) los provee Usuarios por lote: con 120 alumnos, una llamada por fila serían 120 viajes por el gateway para pintar una sola tabla. La fila del ranking viaja con la identidad ya resuelta, para que la regla de anonimato de RF-RNK-03 viva en un solo lugar.
*   Restricciones (legales/técnicas): el alumno ve su propio puntaje completo, el top 3 y el bottom 3 identificados, y los cortes P90 y P10 sin identidad (RF-RNK-03). Ninguna pantalla ni respuesta de API expone datos personales de un alumno a otro. El desempate se aplica en cascada: 1° más insignias, 2° menos vidas perdidas, 3° más nodos completados (RF-RNK-11). Si Inventario no responde se muestra el último dato conocido con aviso, nunca ceros. La confirmación manual del estado académico final (HU-27) y la exportación del resumen de cierre (HU-28) quedan diferidas; el cálculo P90/P10 sigue en el MVP.

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] Un curso de 24 alumnos muestra los cortes P90/P10 sin identidad y resalta a los candidatos; uno de 7 muestra posiciones y XP sin zonas. El alumno ve su fila completa y las ajenas sin datos personales.
*   [ ] KPIs iniciales: es la épica que alimentará los KPIs de producto del cierre —KPI-03 abandono, KPI-04 aprobados y KPI-05 promoción—, pero esa carga queda diferida junto con HU-27 y HU-28. El indicador propio en el alcance vigente es el tiempo de recálculo del ranking en cursos de 120 alumnos.
*   [ ] Sin regresiones críticas en privacidad: ninguna pantalla ni respuesta de API expone datos personales de un alumno a otro, ni siquiera al abrir el detalle de una fila ajena (RF-RNK-03 y RF-RNK-07).
*   [ ] Observabilidad y alertas: métrica del tiempo de recálculo del ranking con alerta si se degrada en cursos de 120 alumnos, más contador de respuestas servidas con dato de Inventario desactualizado.
*   [ ] Documentación publicada: página de Wiki con la regla de visibilidad por fila y la cascada de desempate.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: Accounting, Inventario (vidas perdidas históricas), Usuarios (perfiles por lote), Courses (consulta de cierre, fase futura), Backoffice.
*   Módulos afectados: ranking por curso, percentiles, cascada de desempate.
*   Otros equipos: Usuarios debe exponer la lectura de perfiles por lote. La consulta de cierre de Courses debe ser una lectura rápida e idempotente, no una espera de la decisión del profesor, y queda para la fase en que se retome HU-27.
*   Impacto en datos / migraciones: proyección ranking\_curso y caché de perfiles y XP. La tabla de estado académico final se crea cuando se retome el cierre.
*   Feature toggles / flags: ninguno. El ranking es una lectura que los alumnos ya vieron: apagarlo a mitad de cuatrimestre es peor que un ranking con un error. El cierre académico tampoco lo necesita porque no tiene estado intermedio que un flag pueda representar.


## Historias

| HU | Estado | Responsable | Sprint | Tareas |
|---|---|---|---|---|
| [[historias/HU-24 Ver el ranking de mi curso\|HU-24]] Ver el ranking de mi curso | Done | Lorenzo Araujo | G10 - Sprint 2 | 6/6 |
| [[historias/HU-25 Desempatar el ranking en cascada\|HU-25]] Desempatar el ranking en cascada | Done | Lorenzo Araujo | G10 - Sprint 2 | 6/6 |
