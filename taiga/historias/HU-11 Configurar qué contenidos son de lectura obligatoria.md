---
tags: [tpi, g10, taiga, hu]
codigo: HU-11
ref: 738
estado: "Done"
responsable: "Gabriela Camacho"
epicas: "[[epicas/EP-593 Nodos de contenido y lectura previa|EP-593]]"
sprint: "G10 - Sprint 1"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/738
---

# HU-11: Configurar qué contenidos son de lectura obligatoria

> [!info] Generado desde Taiga (2026-10-15 23:02). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/738) · Estado: **Done** · Responsable: **Gabriela Camacho** · Sprint: **G10 - Sprint 1**
> Épica: [[epicas/EP-593 Nodos de contenido y lectura previa|EP-593]] · Tareas cerradas: **5/5**

[G10] — HU-11 — Configurar qué contenidos son de lectura obligatoria
--------------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: decidir qué nodos de contenido son de lectura obligatoria
*   **Para**: que el gate exija solo lo indispensable

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: La obligatoriedad se define por nodo. Los cambios rigen hacia adelante y no revierten desbloqueos ya alcanzados (RF-CFG-06). Dar de baja un nodo hace que deje de contar sin borrar las lecturas registradas.
*   [ ] Validaciones: El nodo tiene que ser de tipo CONTENIDO y estar en una unidad activa del curso-cohorte.
*   [ ] Datos obligatorios: Nodo y el valor obligatorio, sí o no.
*   [ ] Performance (tiempos, volumen, límites): Respuesta en menos de 300 ms, visible en el próximo gate sin recálculo.
*   [ ] Seguridad (roles, permisos, datos sensibles): Solo el PROFESSOR dueño del curso.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Toggle operable por teclado con el estado anunciado en texto.
*   [ ] Otros: Es lo que da contenido real al criterio contenido_no_leido del gate de HU-15. Trazabilidad: RF-CFG-06, RF-NFR-01. Dependencias: Courses (propiedad del curso) y Gateway; ninguna dependencia externa de equipo. Datos: campo obligatorio en el nodo de contenido. Riesgo: reversión accidental de desbloqueos; mitigación, test de regresión compartido con HU-15.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Marcar un contenido como obligatorio hace que cuente en la regla desde ese momento.
*   [ ] **CA2**: Desmarcarlo no revierte ningún desbloqueo ya alcanzado.
*   [ ] **CA3**: Un profesor que no es dueño queda bloqueado.
*   [ ] **CA4**: Dar de baja el nodo hace que deje de contar sin borrar las lecturas.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Obligatoriedad de lectura por nodo de contenido

**Escenario 1**  

*   **Dado**: un nodo que no es obligatorio
*   **Cuando**: el profesor lo marca como obligatorio
*   **Entonces**: cuenta en la regla desde ese momento

**Escenario 2**  

*   **Dado**: un alumno ya desbloqueado con la regla anterior
*   **Cuando**: el profesor agrega un contenido obligatorio
*   **Entonces**: el alumno sigue desbloqueado y la regla nueva solo aplica a los pendientes

**Escenario 3**  

*   **Dado**: un profesor de otro curso
*   **Cuando**: intenta cambiar la obligatoriedad
*   **Entonces**: se rechaza por permiso

**Escenario 4**  

*   **Dado**: un nodo obligatorio con lecturas registradas
*   **Cuando**: el profesor lo da de baja
*   **Entonces**: deja de contar y las lecturas quedan intactas

* * *
Prototipo
---------

*   **Capturas**: Boceto Obligatoriedad (profesor).
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente: toggle de obligatoriedad accesible por teclado.
*   **Mock API / Swagger**: PATCH /api/roadmap/nodos/{id}/obligatoriedad.


## Tareas

- [x] #1066 T-11.1 — Endpoint de obligatoriedad por nodo · Closed · Gabriela Camacho
- [x] #1067 T-11.2 — Garantía de no retroactividad · Closed · Gabriela Camacho
- [x] #1068 T-11.3 — Validación de permiso de dueño · Closed · Gabriela Camacho
- [x] #1069 T-11.4 — Frontend: toggle en el editor · Closed · Gabriela Camacho
- [x] #1070 T-11.5 — Tests BDD · Closed · Gabriela Camacho
