---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-64
estado: Propuesta
responsable: ""
epica: "Correcciones de los profes"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Must
en_taiga: false
---

# HU-64: Nodos de inicio y fin obligatorios

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Correcciones de los profes|Correcciones de los profes]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

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

- [ ] **T-64.1 Tipos de nodo de inicio y fin** · Back
    - **Qué:** agregar `START` y `END` a los tipos de nodo (DEC-018). Al crear un roadmap y cada unidad o sección se crean solos, con los nombres «Bienvenidos» y «Felicitaciones».
    - **Listo cuando:** un roadmap nuevo y una unidad nueva ya traen los dos.
- [ ] **T-64.2 Validar al guardar que haya inicio, fin y camino** · Back
    - **Qué:** `GraphValidator` rechaza guardar si falta el inicio o el fin, o si algún nodo no tiene camino desde el inicio, y devuelve la lista de problemas.
    - **Listo cuando:** hay tests de cada error.
- [ ] **T-64.3 Agregar inicio y fin a los roadmaps que ya existen** · Back
    - **Qué:** migración que agrega `START` y `END` a cada roadmap y unidad existente y los conecta con el primer y el último nodo.
    - **Listo cuando:** después de migrar, todos los roadmaps pasan la validación de T-64.2.
- [ ] **T-64.4 Cómo se ven el inicio y el fin** · Front
    - **Qué:** visual propio en el mapa 2D y en el mundo 3D, con texto y no solo un ícono.
    - **Listo cuando:** el alumno identifica dónde empieza y dónde termina.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

`NodeType` tiene `UNIT`, `CONTENT`, `THEORETICAL_CHALLENGE`, `PRACTICAL_CHALLENGE` y `EXAM`. No existen START ni END.

### Depende de

- [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial|HT-18]] Módulo graph en Neo4j y migración inicial

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P8]] Inicio y fin son obligatorios siempre, en el curso y en cada unidad/sección.
