---
tags: [tpi, g10, taiga, hu]
codigo: HU-05
ref: 735
estado: "Done"
responsable: "Lorenzo Araujo"
epicas: "[[epicas/EP-593 Nodos de contenido y lectura previa|EP-593]]"
sprint: "G10 - Sprint 1"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/735
---

# HU-05: Ver el detalle de un nodo de contenido (canónica)

> [!info] Generado desde Taiga (2026-10-14 20:44). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/735) · Estado: **Done** · Responsable: **Lorenzo Araujo** · Sprint: **G10 - Sprint 1**
> Épica: [[epicas/EP-593 Nodos de contenido y lectura previa|EP-593]] · Tareas cerradas: **5/5**

[G10] — HU-05 — Ver el detalle de un nodo de contenido (canónica)
-----------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: ver el detalle de un nodo de contenido de mi unidad
*   **Para**: saber qué leer y si ya lo marqué

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El título y el tipo vienen de Courses, la obligatoriedad de HU-11 y el marcado propio de HU-06. No hay reglas derivadas. En una unidad bloqueada solo se informa la existencia del nodo, según lo que resuelve el gate de E3.
*   [ ] Validaciones: El nodo tiene que ser de tipo CONTENIDO y pertenecer al curso-cohorte del alumno que consulta.
*   [ ] Datos obligatorios: Curso-cohorte y nodo; el alumno sale del token, nunca de un parámetro.
*   [ ] Performance (tiempos, volumen, límites): Respuesta en menos de 200 ms.
*   [ ] Seguridad (roles, permisos, datos sensibles): Solo se devuelven nodos del propio curso-cohorte del alumno.
*   [ ] Accesibilidad (WCAG/teclado/lectores): El estado se comunica en texto, no solo con icono o color.
*   [ ] Otros: Es la historia canónica de 1 punto: la referencia de la escala de estimación del equipo. Trazabilidad: RF-CUR-01, RF-NFR-03. Dependencias: Courses (título y tipo) vía HT-03 y Gateway; ninguna dependencia externa de equipo. Datos: lee nodo, contenido y lectura. Sin riesgos relevantes. Nota: la tabla del backlog la estima en 2 puntos y el detalle de la historia en 1; se toma 1 por ser la definición canónica de la escala.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: En una unidad desbloqueada el alumno ve título, tipo y su marcado.
*   [ ] **CA2**: En una unidad bloqueada ve la existencia del nodo, nunca el título.
*   [ ] **CA3**: Un nodo sin marcar figura siempre como pendiente.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Detalle de un nodo de contenido para el alumno

**Escenario 1**  

*   **Dado**: una unidad desbloqueada con el nodo vinculado
*   **Cuando**: el alumno abre el detalle
*   **Entonces**: ve título, tipo y el estado no marcado

**Escenario 2**  

*   **Dado**: una unidad bloqueada
*   **Cuando**: el alumno abre el detalle
*   **Entonces**: ve la existencia del nodo sin título ni material

**Escenario 3**  

*   **Dado**: un nodo de otro curso
*   **Cuando**: el alumno intenta abrirlo
*   **Entonces**: se rechaza por permiso

* * *
Prototipo
---------

*   **Capturas**: Boceto Detalle de nodo (alumno).
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente: vista de detalle y lista de nodos con estados.
*   **Mock API / Swagger**: GET /api/roadmap/nodos/{id}, incluyendo el estado de lectura del alumno.


## Tareas

- [x] #1076 T-05.1 — Endpoint de detalle con visibilidad por desbloqueo · Closed · Lorenzo Araujo
- [x] #1077 T-05.2 — Frontend: vista de detalle · Closed · Iker Alonso
- [x] #1078 T-05.3 — Tests BDD · Closed · Lorenzo Araujo
- [x] #2083 T-05.4 — Vista lista de nodos de mi unidad con estados (alumno) · Closed · Lorenzo Araujo
- [x] #2856 T-03.7 — Wiki: secuencia del consumo del evento del Motor · Closed · Franco Maximiliano Amarilla
