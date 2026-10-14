---
tags: [tpi, g10, taiga, hu]
codigo: HU-44
ref: 5373
estado: "Done"
responsable: "Baltasar Rodriguez Teruel"
epicas: "[[epicas/EP-5371 Roadmap por grupo de la cohorte|EP-5371]]"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5373
---

# HU-44: Ver el roadmap de cada una de mis comisiones

> [!info] Generado desde Taiga (2026-10-14 20:45). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5373) · Estado: **Done** · Responsable: **Baltasar Rodriguez Teruel** · Sprint: **G10 - Sprint 2**
> Épica: [[epicas/EP-5371 Roadmap por grupo de la cohorte|EP-5371]] · Tareas cerradas: **10/10**

[G10] — HU-44 — Ver el roadmap de cada una de mis comisiones
------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: ver y avanzar en el roadmap de cada una de mis comisiones, con solo las unidades que corresponden a cada una
*   **Para**: no confundirme con el recorrido de otra comisión y conservar mi XP en todas

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Comisión = grupo de Courses dentro del curso-cohorte. El roadmap sigue siendo uno por curso-cohorte: la vista por comisión filtra sus unidades por las restricciones GROUP de cada sección. Un alumno en varias comisiones elige cuál ver con un selector; con una sola comisión la vista no cambia. Una unidad sin restricción GROUP la ven todas las comisiones; una restringida, solo las indicadas. La XP, los completados y las lecturas son de la cohorte y valen en todas las comisiones del alumno. El gate rechaza un nodo cuya unidad no corresponde a ninguna comisión del alumno (group_restricted). Al cerrar un intento, el nodo se resuelve por el node_id del evento del Motor: el mismo desafío puede estar en unidades de comisiones distintas. Agregar, quitar o mover de comisión no borra progreso (RF-CFG-06).
*   [ ] Validaciones: La comisión elegida es una de las del alumno; la visibilidad se calcula por course_section_id.
*   [ ] Datos obligatorios: Alumno (del token), courseCohortId, comisiones del alumno (HT-10) y comisión elegida (opcional).
*   [ ] Performance (tiempos, volumen, límites): Sin llamadas extra a Courses por consulta del recorrido: se usan las membresías guardadas.
*   [ ] Seguridad (roles, permisos, datos sensibles): Rol STUDENT con matrícula activa; solo puede elegir sus propias comisiones.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Selector de comisión con etiqueta en texto; el motivo de rechazo del gate va en texto («unidad de otra comisión»).
*   [ ] Otros: Flag roadmap-by-group (ya en develop, T-44.4): apagado, toda la cohorte ve todas las unidades como hoy. Decisión del 08/10: varias comisiones por alumno y XP compartida (reemplaza P-29). Depende de HT-10 y HU-36. Relacionadas: HU-45, HU-49.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Un alumno solo de 2W1 no ve las unidades restringidas a 2W2.
*   [ ] **CA2**: Un alumno de 2W1 y 2W2 elige 2W2 y ve sus unidades con la misma XP.
*   [ ] **CA3**: El gate rechaza con group_restricted un nodo de una unidad que no es de ninguna comisión del alumno.
*   [ ] **CA4**: Con el mismo desafío en unidades de 2W1 y 2W2, el cierre del Motor suma la XP en el nodo correcto.
*   [ ] **CA5**: Una cohorte sin comisiones se comporta igual que hoy.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Roadmap por comisión

**Escenario 1**  

*   **Dado**: una unidad restringida a 2W2
*   **Cuando**: un alumno solo de 2W1 abre su recorrido
*   **Entonces**: no la ve

**Escenario 2**  

*   **Dado**: un alumno de 2W1 y 2W2 con 300 XP
*   **Cuando**: elige 2W2 en el selector
*   **Entonces**: ve las unidades de 2W2 y sus 300 XP

**Escenario 3**  

*   **Dado**: un alumno solo de 2W1
*   **Cuando**: intenta entrar a un nodo de una unidad de 2W2
*   **Entonces**: el gate rechaza con «unidad de otra comisión»

**Escenario 4**  

*   **Dado**: el mismo desafío en una unidad de 2W1 y otra de 2W2
*   **Cuando**: el Motor cierra el intento abierto desde el nodo de 2W2
*   **Entonces**: se completa el nodo de 2W2 y no el de 2W1

* * *
Prototipo
---------

*   **Capturas**: Selector de comisión en el recorrido del alumno; el resto de la pantalla no cambia.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId} con la comisión elegida (parámetro a definir) y GET …/progress, filtrados por comisión; gate existente con el motivo group_restricted.

* * *
Estimación / Prioridad
----------------------

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Must

* * *
Dependencias / Impactos
-----------------------

*   Servicios involucrados: Courses (comisiones y restricciones GROUP, vía HT-10), Motor (node_id en el cierre y motivo nuevo), API Gateway.
*   Módulos afectados: GraphService, ProgressService, GateEvaluator, recorrido del front.
*   Otros equipos / aprobaciones: G01 (HT-10) y G09 (T-44.10).
*   Impacto en datos / migraciones: Usa student_course_group de HT-10.
*   Riesgos y mitigación (opcional): Eventos de cierre viejos sin node_id; mitigación: se resuelve por challenge_id como hoy.

## Tareas

- [x] #5414 T-44.1 Resolver las unidades visibles para cada comisión del alumno · Closed · Baltasar Rodriguez Teruel
- [x] #5415 T-44.2 Recorrido y avance por la comisión elegida · Closed · Baltasar Rodriguez Teruel
- [x] #5416 T-44.3 Gate: rechazo group_restricted si la unidad no es de ninguna comisión del alumno · Closed · Baltasar Rodriguez Teruel
- [x] #5417 T-44.4 Flag roadmap-por-grupo · Closed · Baltasar Rodriguez Teruel
- [x] #5418 T-44.5 Cambio de comisión sin pérdida de progreso · Closed · Baltasar Rodriguez Teruel
- [x] #5419 T-44.6 BDD por comisión · Closed · Ludmila Mailen Cejas
- [x] #5420 T-44.7 Wiki, OpenAPI y diagrama de secuencia · Closed · Quinteros Tomás
- [x] #7221 T-44.8 Resolver el cierre del Motor por node_id · Closed · Mateo Delgado Costa
- [x] #7222 T-44.9 Selector de comisión en el recorrido del alumno · Closed · Mateo Delgado Costa
- [x] #7223 T-44.10 Pedido a G09: node_id en el cierre y motivos nuevos del gate · Closed · Mateo Delgado Costa
