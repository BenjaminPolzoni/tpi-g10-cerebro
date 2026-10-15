---
tags: [tpi, g10, taiga, hu]
codigo: HU-42
ref: 4248
estado: "Done"
responsable: "Fenoglio Santino"
epicas: "[[epicas/EP-593 Nodos de contenido y lectura previa|EP-593]]"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4248
---

# HU-42: Abrir y leer el material de un nodo de lectura desde el roadmap

> [!info] Generado desde Taiga (2026-10-15 16:54). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4248) · Estado: **Done** · Responsable: **Fenoglio Santino** · Sprint: **G10 - Sprint 2**
> Épica: [[epicas/EP-593 Nodos de contenido y lectura previa|EP-593]] · Tareas cerradas: **5/5**

[G10] — HU-42 — Abrir y leer el material de un nodo de lectura desde el roadmap
------------------------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: abrir el material vinculado a un nodo de lectura de mi unidad y marcarlo como leído al terminar
*   **Para**: leer sin perder el recorrido y habilitar los desafíos de la unidad

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El material lo guarda Courses en la plataforma Garage y Roadmap se lo pide (D-03, P-30); Roadmap guarda solo contenido_id (HU-04) y no guarda ni sube archivos. Solo en unidades desbloqueadas; en una bloqueada se informa solo la existencia (HU-05). El marcado sigue siendo explícito, append-only e idempotente (HU-06). Si Courses despublica el material, el nodo pasa a "no disponible" sin borrar lecturas. Reemplaza el material de ejemplo fijo de materials-page.
*   [ ] Validaciones: Nodo CONTENIDO del curso-cohorte del alumno; alumno matriculado.
*   [ ] Datos obligatorios: Curso-cohorte y nodo (alumno del token).
*   [ ] Performance (tiempos, volumen, límites): Detalle en menos de 300 ms; metadatos por lote (una llamada por unidad).
*   [ ] Seguridad (roles, permisos, datos sensibles): Solo nodos del propio curso-cohorte; token técnico hacia Courses; la URL de acceso al archivo la provee Courses (por ejemplo firmada y con vencimiento).
*   [ ] Accesibilidad (WCAG/teclado/lectores): Estado leído/pendiente en texto; operable por teclado.
*   [ ] Otros: Condicionada a G01: que guarde el material en Garage, habilite actividades FILE y LINK (hoy solo se crea QUIZ) y exponga por lote, con token técnico, los metadatos y la URL de acceso (P-16). Misma condición que HU-04. P-25 respondida por P-30 (02/10): el enlace no se guarda en Roadmap; resourceUrl y resourceType del front no pasan al backend y el visor pasa a usar la URL que devuelve Courses. Estado actual: la lectura y el marcado ya funcionan de punta a punta; falta de dónde sale el material. section-map-page y world-3d-page ya embeben el material por enlace (toEmbedUrl), pero resourceUrl y resourceType no existen en el back y el enlace se pierde con el adapter HTTP; materials-page sigue con EXAMPLE_SECTIONS. Riesgo: Courses sin catálogo de contenidos; mitigación: mismo pedido de HT-07 y, si no hay respuesta, pasa a Blocked con motivo y fecha. Relacionadas: HU-04, HU-19, HU-46, HU-05, HU-06 y HU-11. Posible superposición con HU-46 (material en el Templo): P-31 define si se fusionan o quedan separadas (HU-42 para el nodo de lectura, HU-46 para el Templo).

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Con la unidad desbloqueada, el alumno abre el nodo y accede al material real de Courses.
*   [ ] **CA2**: En una unidad bloqueada ve solo la existencia, nunca el título ni el material.
*   [ ] **CA3**: Marcar como leído desde esa vista registra una sola vez y actualiza el gate y la barra de HU-19.
*   [ ] **CA4**: Un material despublicado se ve "no disponible" y las lecturas quedan intactas.
*   [ ] **CA5**: No queda material de ejemplo fijo en la vista.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Lectura del material de un nodo

**Escenario 1**  

*   **Dado**: una unidad desbloqueada con un contenido publicado
*   **Cuando**: el alumno abre el nodo
*   **Entonces**: accede al material y ve su estado pendiente

**Escenario 2**  

*   **Dado**: una unidad bloqueada
*   **Cuando**: el alumno abre el detalle
*   **Entonces**: ve la existencia del nodo sin título ni material

**Escenario 3**  

*   **Dado**: un nodo leído por varios alumnos
*   **Cuando**: Courses despublica el material
*   **Entonces**: el nodo queda "no disponible" y las lecturas siguen registradas

* * *
Prototipo
---------

*   **Capturas**: Base existente: section-map-page y world-3d-page (material embebido por enlace).
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/nodes/{nodeId} (NodeDetailDto con metadatos y URL de acceso de Courses) y POST /api/roadmap/nodes/{nodeId}/read.


## Tareas

- [x] #4312 T-42.1 Traer de Courses (lote) los metadatos y la URL de acceso en Garage y sumarlos al NodeDetailDto (D-03) · Closed · Fenoglio Santino
- [x] #4313 T-42.2 Estado «no disponible» si Courses despublica el material · Closed · Fenoglio Santino
- [x] #4314 T-42.3 Visor con la URL de Courses; dejar de usar resourceUrl local · Closed · Fenoglio Santino
- [x] #4315 T-42.4 BDD node_detail extendido · Closed · Fenoglio Santino
- [x] #5405 T-42.5 Wiki, OpenAPI y diagrama de secuencia · Closed · Franco Maximiliano Amarilla
