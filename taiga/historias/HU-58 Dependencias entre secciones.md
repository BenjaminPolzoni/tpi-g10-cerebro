---
tags: [tpi, g10, taiga, hu]
codigo: HU-58
ref: 8608
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8608
---

# HU-58: Dependencias entre secciones

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8608) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Tareas cerradas: **0/5**

[G10] — HU-58 — Dependencias entre secciones
--------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: definir de qué secciones depende cada sección (AND/OR), con un XP mínimo opcional y un atajo para «todas las anteriores»
*   **Para**: armar el recorrido del curso como en el ejemplo de los profes

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Ya existen las dependencias AND/OR entre secciones (V25). La regla AND/OR (árbol `Rule`) se define en HU-59; esta HU la aplica a secciones y es la dueña del XP mínimo. Vuelve el XP mínimo por sección (se borró en V8, DEC-011). «Todas las anteriores» es un atajo de la UI que guarda un AND. Las dependencias también se definen entre subsecciones (P6).
*   [ ] Validaciones: No se puede guardar un ciclo. XP mínimo ≥ 0.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Selector de secciones usable con teclado.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Elegir las secciones requeridas con la regla AND/OR de HU-59.
*   [ ] **CA2**: XP mínimo opcional por sección.
*   [ ] **CA3**: Atajo «todas las anteriores».
*   [ ] **CA4**: Guardar un ciclo devuelve error.
*   [ ] **CA5**: El alumno ve por qué una sección está bloqueada.
*   [ ] **CA6**: Las dependencias se pueden definir también entre subsecciones.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Dependencias entre secciones

**Escenario 1**

*   **Dado**: las secciones 1 y 2
*   **Cuando**: el profesor hace que la 3 dependa de ambas con AND
*   **Entonces**: la 3 se desbloquea solo con 1 y 2 completas

**Escenario 2**

*   **Dado**: la sección 4 depende de la 2 con XP ≥ 500
*   **Cuando**: un alumno completa la 2 con 300 XP
*   **Entonces**: la 4 sigue bloqueada y ve «te faltan 200 XP»

**Escenario 3**

*   **Dado**: la sección 1 depende de la 3
*   **Cuando**: el profesor hace que la 3 dependa de la 1
*   **Entonces**: recibe error de ciclo

* * *

Prototipo
---------

*   **Capturas**: Editor de reglas de sección.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-select`, `generic-input`.
*   **Mock API / Swagger**: PATCH /api/roadmap/sections/{sectionId}/rules.

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
*   Módulos afectados: Reglas de sección, `GateEvaluator`, `rules-wizard`.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: XP mínimo en Neo4j (`Rule.minXp`).
*   Riesgos y mitigación (opcional): Depende de HT-18 y P6.


## Tareas

- [ ] #9151 T-58.1 Volver a tener XP mínimo por sección · New · Fenoglio Santino
- [ ] #9152 T-58.2 Dependencias entre subsecciones y sin ciclos · New · Fenoglio Santino
- [ ] #9153 T-58.3 Editor de reglas de sección con XP mínimo y «todas las anteriores» · New · Fenoglio Santino
- [ ] #9154 T-58.4 Explicarle al alumno por qué una sección está bloqueada · New · Lorenzo Araujo
- [ ] #9348 T-58.5 Wiki, OpenAPI y diagrama de secuencia · New · Franco Maximiliano Amarilla
