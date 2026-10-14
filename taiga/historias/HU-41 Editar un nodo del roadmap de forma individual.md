---
tags: [tpi, g10, taiga, hu]
codigo: HU-41
ref: 4247
estado: "Done"
responsable: "Stefano Zoffoli"
epica: "[G10] — Edición del roadmap por el profesor"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4247
---

# HU-41: Editar un nodo del roadmap de forma individual

> [!info] Generado desde Taiga (2026-10-14 18:47). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4247) · Estado: **Done** · Responsable: **Stefano Zoffoli** · Sprint: **G10 - Sprint 2**

[G10] — HU-41 — Editar un nodo del roadmap de forma individual
--------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: abrir cualquier nodo del roadmap y editar sus datos (referencia al desafío, examen o contenido, obligatoriedad, reintentos, modo AND/OR y prerrequisitos) sin tocar el resto del grafo
*   **Para**: ajustar mi curso nodo por nodo durante el cuatrimestre sin rearmar unidades ni afectar a los alumnos que ya avanzaron

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Edición permitida aun con el curso activo (RF-CUR-05). Los cambios rigen hacia adelante y no revierten desbloqueos ni tocan completed_node, lecturas ni XP (RF-CFG-06, RF-NFR-01). La arista que cierra un ciclo se rechaza. Los nodos opcionales no pueden ser prerrequisito (decisión del 20/09). Las unidades no se crean ni reordenan acá: vienen de Courses (HU-37).
*   [ ] Validaciones: Reintentos 0..PAR-13 (hoy sin soporte: el nodo no tiene el campo y no se lee PAR-13, P-23); desafío o examen publicado en el catálogo del Motor; contenido publicado en Courses; nodo de una unidad activa del curso-cohorte; sin autociclos.
*   [ ] Datos obligatorios: Nodo y los campos a modificar.
*   [ ] Performance (tiempos, volumen, límites): Guardado en menos de 300 ms; el cambio se ve en la próxima consulta del gate, sin recálculo.
*   [ ] Seguridad (roles, permisos, datos sensibles): Solo el PROFESSOR dueño del curso (403 sin cambios si no lo es); catálogos con token técnico.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Formulario operable por teclado; errores en texto junto al campo, anunciados con aria-live.
*   [ ] Otros: La baja de un nodo con dependientes queda fuera: depende de la decisión 2 del PO de la Propuesta de Sprint 2 (aristas huérfanas). Comparte pantalla con HU-37: coordinar con la rama feature/roadmap-adapter-refinements. Bugs conocidos que absorbe: el front manda lifeRecovery y el back usa livesPolicy desde V14, y el PUT sin livesPolicy deja el nodo en STANDARD; los campos descripción, dificultad, reintentos, enlace y tipo del material, posición, umbral de XP y bioma solo existen en el front y se pierden al recargar (P-24); el front no usa PATCH availability ni mandatory y hace un GET completo antes de cada guardado. Dependencias: HU-01, HU-11 y HU-13 (Done); Motor (catálogo), Courses (contenido), Gateway.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor abre un nodo y ve sus datos vigentes.
*   [ ] **CA2**: Al cambiar obligatoriedad, reintentos o reglas, el gate usa el valor nuevo en la próxima consulta.
*   [ ] **CA3**: Una edición que cierra un ciclo se rechaza sin cambios.
*   [ ] **CA4**: Un alumno que ya desbloqueó el nodo conserva el desbloqueo tras la edición.
*   [ ] **CA5**: Un profesor que no es dueño recibe 403 sin efectos.
*   [ ] **CA6**: Cada edición deja un log con autor, fecha, campos y cantidad de alumnos afectados.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Edición individual de un nodo

**Escenario 1**  

*   **Dado**: un nodo DESAFIO con 1 reintento permitido
*   **Cuando**: el profesor lo cambia a 2
*   **Entonces**: se guarda y el gate lo usa en la próxima consulta

**Escenario 2**  

*   **Dado**: un alumno desbloqueó el nodo C con la regla anterior
*   **Cuando**: el profesor agrega un prerrequisito a C
*   **Entonces**: el alumno sigue desbloqueado

**Escenario 3**  

*   **Dado**: A es prerrequisito de B
*   **Cuando**: el profesor edita A y agrega B como su prerrequisito
*   **Entonces**: rechazo por ciclo, sin cambios

**Escenario 4**  

*   **Dado**: un profesor de otro curso
*   **Cuando**: intenta editar el nodo
*   **Entonces**: rechazo por permiso, nada cambia

* * *
Prototipo
---------

*   **Capturas**: Base existente: course-map-page (entity-editor-dialog y unlock-rules-form) y course-builder-page (node-creation-wizard y rules-wizard).
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: PUT y PATCH /api/roadmap/nodes/{nodeId}; PATCH .../availability, .../mandatory, .../prerequisite-mode y .../rules; POST .../prerequisites; DELETE /api/roadmap/nodes/{nodeId}.


## Tareas

- [x] #4307 T-41.1 Corregir la deriva livesPolicy y pasar el front a PATCH parcial · Closed · Stefano Zoffoli
- [x] #4308 T-41.2 Migrar al back los campos del front que defina P-24 (sin reintentos) · Closed · Stefano Zoffoli
- [x] #4309 T-41.3 Panel: política de vidas, disponibilidad y reintentos (solo lectura) · Closed · Stefano Zoffoli
- [x] #4310 T-41.4 Log de edición · Closed · Stefano Zoffoli
- [x] #4311 T-41.5 Tests de no retroactividad y BDD sobre editor.feature · Closed · Stefano Zoffoli
- [x] #5404 T-41.6 Wiki, OpenAPI y diagrama de secuencia · Closed · Franco Maximiliano Amarilla
