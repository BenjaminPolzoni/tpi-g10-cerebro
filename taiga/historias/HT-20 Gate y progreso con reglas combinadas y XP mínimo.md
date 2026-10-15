---
tags: [tpi, g10, taiga, ht]
codigo: HT-20
ref: 8603
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8603
---

# HT-20: Gate y progreso con reglas combinadas y XP mínimo

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8603) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Tareas cerradas: **0/5**

[G10] — HT-20 — Gate y progreso con reglas combinadas y XP mínimo
-----------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: que el gate y el progreso evalúen las reglas combinadas y el XP mínimo con el mismo evaluador
*   **Para**: que el alumno vea bloqueado exactamente lo que el gate bloquea

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Un único evaluador para el gate y el recorrido (como hoy `block_reason`).
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): El P95 del gate no supera 200 ms con la caché de reglas.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El gate y el recorrido usan el mismo evaluador sobre el árbol de reglas.
*   [ ] **CA2**: El XP mínimo de sección se evalúa.
*   [ ] **CA3**: Tests BDD con el ejemplo de los profes (secciones 1 a 5).
*   [ ] **CA4**: Medición del P95 del gate.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Gate con reglas nuevas

**Escenario 1**  

*   **Dado**: el ejemplo de los profes
*   **Cuando**: un alumno completa las secciones 1 y 2
*   **Entonces**: se desbloquea la 3 y la 5 sigue bloqueada

**Escenario 2**  

*   **Dado**: la sección 4 con XP ≥ 500
*   **Cuando**: el alumno llega a 500 XP
*   **Entonces**: la 4 se desbloquea

**Escenario 3**  

*   **Dado**: una regla `A y (B o C)`
*   **Cuando**: el Motor consulta el gate
*   **Entonces**: responde igual que el recorrido

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
*   Módulos afectados: `GateEvaluator`, `GateService`, servicio de progreso.
*   Otros equipos / aprobaciones: G09 (el gate es su contrato).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Latencia; mitigación: caché de reglas.


## Tareas

- [ ] #9030 T-20.1 Un solo evaluador de reglas para el gate y para lo que ve el alumno · New · Fenoglio Santino
- [ ] #9048 T-20.2 Evaluar el XP mínimo · New · Fenoglio Santino
- [ ] #9058 T-20.3 Escenarios BDD con el ejemplo de los profes · New · Fenoglio Santino
- [ ] #9060 T-20.4 Medir la latencia del gate · New · Fenoglio Santino
- [ ] #9338 T-20.5 Wiki, OpenAPI y diagrama de secuencia · New · Franco Maximiliano Amarilla
