---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-24
estado: Propuesta
responsable: ""
epica: "Correcciones de los profes"
sprint: "G10 - Sprint 3"
puntos: 2
prioridad: Should
en_taiga: false
---

# HT-24: Datos para el dashboard de G06

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Correcciones de los profes|Correcciones de los profes]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HT-24 — Datos para el dashboard de G06
----------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: BACKOFFICE (G06)
*   **Quiero**: saber qué datos de progreso, ranking y XP me da Roadmap y por dónde
*   **Para**: armar el dashboard entre todos los grupos

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Ya existen endpoints de progreso, ranking, nivel y avance por grupo, y el topic `roadmap.events`.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): Lectura entre servicios con scope (`roadmap.progress.read`).
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Acordado con G06 qué datos y por dónde (REST o eventos).
*   [ ] **CA2**: Registrado en `acuerdos/`.
*   [ ] **CA3**: Si hace falta algo nuevo, queda como HU.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Datos para el dashboard

**Escenario 1**  

*   **Dado**: el dashboard de G06
*   **Cuando**: pide el progreso agregado de un curso
*   **Entonces**: lo recibe con su scope

**Escenario 2**  

*   **Dado**: un nodo completado
*   **Cuando**: se publica en `roadmap.events`
*   **Entonces**: G06 lo puede consumir

**Escenario 3**  

*   **Dado**: un dato que no existe
*   **Cuando**: G06 lo pide
*   **Entonces**: queda como HU nueva

* * *

Prototipo
---------

*   **Capturas**: No aplica (sin pantalla).
*   **URL Figma**: No aplica.
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: No aplica.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 2
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 2 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Backoffice.
*   Módulos afectados: Endpoints de progreso y ranking, `roadmap.events`.
*   Otros equipos / aprobaciones: G06.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Ninguno.

## Tareas

- [ ] T-24.1 Reunión con G06
- [ ] T-24.2 Acta en `acuerdos/`

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Existen endpoints de progreso, ranking, nivel y avance por grupo, y el topic `roadmap.events`.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G3]]
