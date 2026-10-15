---
tags: [tpi, g10, taiga, hu]
codigo: HU-13
ref: 600
estado: "Done"
responsable: "Ludmila Mailen Cejas"
epicas: "[[epicas/EP-60 Progreso y desbloqueo|EP-60]]"
sprint: "G10 - Sprint 1"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/600
---

# HU-13: Configurar las reglas de desbloqueo de una unidad (prerrequisitos AND/OR)

> [!info] Generado desde Taiga (2026-10-15 16:53). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/600) · Estado: **Done** · Responsable: **Ludmila Mailen Cejas** · Sprint: **G10 - Sprint 1**
> Épica: [[epicas/EP-60 Progreso y desbloqueo|EP-60]] · Tareas cerradas: **6/6**

[G10] — HU-13 — Configurar las reglas de desbloqueo de una unidad (prerrequisitos AND/OR)
-----------------------------------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: definir por nodo qué prerrequisitos exige, todos con AND o alguno con OR, permitiendo bifurcación
*   **Para**: que el avance siga la secuencia pedagógica sin umbrales de XP (RF-CUR-06 reescrito, PAR-08 retirado)

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Cada nodo define un modo AND, que exige todos sus prerrequisitos, u OR, que exige alguno, sobre sus aristas. Se valida la aciclicidad rechazando en el alta la arista que genere un ciclo (P-01). Los cambios rigen hacia adelante y no revierten desbloqueos ya alcanzados (RF-CFG-06). La primera unidad no tiene prerrequisitos.
*   [ ] Validaciones: El modo tiene que ser válido, las aristas tienen que apuntar a nodos existentes, no puede haber ciclos y la unidad tiene que ser del curso-cohorte.
*   [ ] Datos obligatorios: Nodo, modo y aristas.
*   [ ] Performance (tiempos, volumen, límites): Respuesta en menos de 300 ms.
*   [ ] Seguridad (roles, permisos, datos sensibles): Solo el PROFESSOR dueño del curso.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Formulario con las advertencias comunicadas en texto.
*   [ ] Otros: Reemplaza en su rol a la configuración de umbral por sección del backlog anterior: en v3 no existe umbral de XP como regla de desbloqueo. Trazabilidad: RF-CUR-06 reescrito, RF-CFG-06, D-01. Dependencias: Courses (propiedad del curso) y Gateway; ninguna dependencia externa de equipo. Datos: modo y aristas por nodo, sin campo de umbral. Riesgo: ciclos introducidos por bifurcación; mitigación, rechazo en el alta (P-01).

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor configura AND u OR y la regla queda disponible para el gate.
*   [ ] **CA2**: Una arista que cierra un ciclo se rechaza.
*   [ ] **CA3**: Un profesor que no es dueño queda bloqueado.
*   [ ] **CA4**: Cambiar las reglas no revierte desbloqueos ya alcanzados.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Reglas de desbloqueo por prerrequisitos AND/OR

**Escenario 1**  

*   **Dado**: un nodo sin reglas configuradas
*   **Cuando**: configuro OR sobre dos prerrequisitos
*   **Entonces**: el gate usa la regla en la próxima consulta

**Escenario 2**  

*   **Dado**: A es prerrequisito de B
*   **Cuando**: agrego B como prerrequisito de A
*   **Entonces**: se rechaza por ciclo

**Escenario 3**  

*   **Dado**: un profesor de otro curso
*   **Cuando**: intenta configurar las reglas
*   **Entonces**: se rechaza por permiso

**Escenario 4**  

*   **Dado**: un alumno ya desbloqueado
*   **Cuando**: el profesor agrega un prerrequisito
*   **Entonces**: el alumno sigue desbloqueado

* * *
Prototipo
---------

*   **Capturas**: Boceto Reglas de desbloqueo (profesor).
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente: selector AND/OR y editor de aristas.
*   **Mock API / Swagger**: PATCH /api/roadmap/nodos/{id}/reglas.


## Tareas

- [x] #601 T-13.1 — Endpoint de reglas AND/OR por nodo · Closed · Ludmila Mailen Cejas
- [x] #602 T-13.2 — Validación acíclica y evaluación AND/OR · Closed · Ludmila Mailen Cejas
- [x] #603 T-13.3 — Garantía de no retroactividad · Closed · Ludmila Mailen Cejas
- [x] #604 T-13.4 — Frontend: formulario de reglas · Closed · Ludmila Mailen Cejas
- [x] #605 T-13.5 — Tests BDD · Closed · Ludmila Mailen Cejas
- [x] #2857 T-13.6 — Wiki: diagrama de estados del nodo · Closed · Franco Maximiliano Amarilla
