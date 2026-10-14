---
tags: [tpi, g10, taiga, hu]
codigo: HU-43
ref: 4249
estado: "Done"
responsable: "Gabriela Camacho"
epicas: "[[epicas/EP-4232 Edición del roadmap por el profesor|EP-4232]]"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4249
---

# HU-43: Elegir el ícono de un desafío

> [!info] Generado desde Taiga (2026-10-14 20:44). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4249) · Estado: **Done** · Responsable: **Gabriela Camacho** · Sprint: **G10 - Sprint 2**
> Épica: [[epicas/EP-4232 Edición del roadmap por el profesor|EP-4232]] · Tareas cerradas: **6/6**

[G10] — HU-43 — Elegir el ícono de un desafío
---------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: elegir el ícono con el que se muestra cada desafío en el roadmap
*   **Para**: que el alumno distinga de un vistazo cada desafío en su recorrido

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Propuesta: el ícono se guarda como clave de un catálogo cerrado (icon_key), no como imagen libre (P-15). Sin ícono elegido se usa el que hoy muestra el front por tipo de nodo. Es cosmético: no toca el gate, el progreso ni el XP. Se muestra en las vistas del recorrido que queden tras HU-29.
*   [ ] Validaciones: icon_key perteneciente al catálogo; solo nodos DESAFIO (y EXAMEN si el PO lo confirma); solo el PROFESSOR dueño del curso.
*   [ ] Datos obligatorios: Nodo e icon_key. Migración: columna nueva y nullable en nodo (número de migración a asignar tras V16).
*   [ ] Performance (tiempos, volumen, límites): El ícono viaja en el NodeResponse del grafo (GET /courses/{courseId}), que es lo que lee el recorrido; el progreso solo trae estado por nodo. Sin llamada extra (menos de 200 ms).
*   [ ] Seguridad (roles, permisos, datos sensibles): Solo el PROFESSOR dueño del curso.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Texto alternativo en el ícono; el nombre del desafío siempre visible, sin transmitir información solo por ícono.
*   [ ] Otros: Sin requisito identificado en la Propuesta de Sprint 2 ni en el Modelo de tareas; confirmar con el PO si corresponde a un RF (P-15). Hoy el front usa un ícono fijo por tipo (emoji) en el editor y el mapa. Reutilizar pixel-icon y el patrón de GENERIC_ICONS del selector de insignias (P-26). El mundo 3D recibe datos por postMessage: sumar el iconKey a ese mensaje. Dependencias: HU-41 (panel de edición) y HU-29 (vistas que quedan).

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor elige un ícono para un desafío y queda guardado.
*   [ ] **CA2**: El alumno ve ese ícono en su recorrido.
*   [ ] **CA3**: Un ícono fuera del catálogo se rechaza.
*   [ ] **CA4**: Sin ícono elegido se ve el ícono por defecto.
*   [ ] **CA5**: Cambiar el ícono no modifica estados de nodos ni desbloqueos.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Ícono de un desafío elegido por el profesor

**Escenario 1**  

*   **Dado**: un desafío sin ícono elegido
*   **Cuando**: el profesor elige uno del catálogo
*   **Entonces**: queda guardado y se ve en el recorrido del alumno

**Escenario 2**  

*   **Dado**: un icon_key que no existe en el catálogo
*   **Cuando**: el profesor intenta guardarlo
*   **Entonces**: rechazo con mensaje, sin cambios

**Escenario 3**  

*   **Dado**: un alumno con nodos desbloqueados
*   **Cuando**: el profesor cambia un ícono
*   **Entonces**: ningún estado de nodo cambia

* * *
Prototipo
---------

*   **Capturas**: Selector de ícono dentro del panel de edición de HU-41.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente: selector de ícono basado en pixel-icon.
*   **Mock API / Swagger**: PATCH /api/roadmap/nodes/{nodeId} con iconKey (NodePatch), propuesta.


## Tareas

- [x] #4316 T-43.1 Migración, campo y validación contra el catálogo · Closed · Gabriela Camacho
- [x] #4318 T-43.2 Exponer iconKey en NodeResponse · Closed · Gabriela Camacho
- [x] #4320 T-43.3 Selector de ícono en el editor · Closed · Gabriela Camacho
- [x] #4322 T-43.4 Mostrar el ícono en las vistas del recorrido · Closed · Gabriela Camacho
- [x] #4323 T-43.5 Tests BDD · Closed · Gabriela Camacho
- [x] #5406 T-43.6 Wiki, OpenAPI y diagrama de secuencia · Closed · Franco Maximiliano Amarilla
