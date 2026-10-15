---
tags: [tpi, g10, taiga, hu]
codigo: HU-64
ref: 8613
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8631 Correcciones de los profes|EP-8631]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8613
---

# HU-64: Nodos de inicio y fin obligatorios

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8613) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8631 Correcciones de los profes|EP-8631]] · Tareas cerradas: **0/5**

[G10] — HU-64 — Nodos de inicio y fin obligatorios
--------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: que el roadmap tenga siempre un nodo de inicio «Bienvenidos» y uno de fin «Felicitaciones», y que no se pueda guardar sin ellos
*   **Para**: que el alumno sepa dónde empieza y dónde termina el curso

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Exactamente un `START` y un `END` por roadmap y por cada unidad/sección (P8). Todo nodo alcanzable desde `START` y `END` alcanzable. Un roadmap nuevo nace con los dos.
*   [ ] Validaciones: Al guardar, si falta alguno o hay nodos sueltos, error con la lista de problemas.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño del curso.
*   [ ] Accesibilidad (WCAG/teclado/lectores): El visual de inicio y fin tiene texto, no solo un ícono.
*   [ ] Otros: Llegar a `END` puede otorgar una insignia de fin de curso (HU-21).

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Tipos de nodo `START` y `END`.
*   [ ] **CA2**: Un roadmap nuevo y cada unidad/sección nueva se crean con los dos.
*   [ ] **CA3**: No se puede guardar sin uno de cada uno ni con nodos inalcanzables.
*   [ ] **CA4**: Visual propio en el mapa 2D y en el mundo 3D.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Inicio y fin obligatorios

**Escenario 1**

*   **Dado**: un roadmap nuevo
*   **Cuando**: el profesor lo crea
*   **Entonces**: ya tiene «Bienvenidos» y «Felicitaciones»

**Escenario 2**

*   **Dado**: un roadmap sin `END`
*   **Cuando**: el profesor guarda
*   **Entonces**: recibe error «falta el nodo final»

**Escenario 3**

*   **Dado**: un nodo sin camino desde `START`
*   **Cuando**: el profesor guarda
*   **Entonces**: recibe error que nombra ese nodo

* * *

Prototipo
---------

*   **Capturas**: Mapa 2D y mundo 3D con inicio y fin.
*   **URL Figma**: Pendiente.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: Validación en el guardado del grafo.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 5
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 5 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: Módulo graph (validación), mapa 2D, mundo 3D.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Migración: agregar START y END a los roadmaps existentes.
*   Riesgos y mitigación (opcional): Roadmaps existentes inválidos; mitigación: la migración los completa.


## Tareas

- [ ] #9179 T-64.1 Tipos de nodo de inicio y fin · New · Stefano Zoffoli
- [ ] #9180 T-64.2 Validar al guardar que haya inicio, fin y camino · New · Stefano Zoffoli
- [ ] #9183 T-64.3 Agregar inicio y fin a los roadmaps que ya existen · New · Stefano Zoffoli
- [ ] #9187 T-64.4 Cómo se ven el inicio y el fin · New · Ludmila Mailen Cejas
- [ ] #9352 T-64.5 Wiki, OpenAPI y diagrama de secuencia · New · Franco Maximiliano Amarilla
