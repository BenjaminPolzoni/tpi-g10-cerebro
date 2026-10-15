---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-21
estado: Propuesta
responsable: ""
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Should
en_taiga: true
---

# HU-21: Otorgar insignias automáticamente

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Ya existe en Taiga: [[taiga/historias/HU-21 Otorgar insignias automáticamente|HU-21]] (épica EP-69). En el Sprint 3 se **reabre** con lo que falta.

[G10] — HU-21 — Otorgar insignias automáticamente
-------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: que todas las insignias del catálogo se puedan ganar
*   **Para**: que el catálogo no prometa insignias imposibles

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Cada criterio del catálogo tiene un evaluador que lo otorga, o se quita del catálogo (decisión E2 del equipo). Las insignias salen por el outbox como `BADGE_AWARDED`.
*   [ ] Validaciones: El otorgamiento es idempotente: una insignia no se otorga dos veces al mismo alumno.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: `LIFE_RECOVERED` necesita un evento de Accounting que hoy no consumimos (E8).

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: `SECTION_NO_LIVES_LOST` se otorga con su test, o se quita del catálogo.
*   [ ] **CA2**: `NODE_NO_RETRIES` se otorga con su test, o se quita del catálogo.
*   [ ] **CA3**: `LIFE_RECOVERED` se otorga con su test, o se quita del catálogo.
*   [ ] **CA4**: Cada otorgamiento publica `BADGE_AWARDED` una sola vez.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Otorgamiento de todos los criterios

**Escenario 1**  

*   **Dado**: una sección completada sin perder vidas
*   **Cuando**: se cierra el último nodo
*   **Entonces**: el alumno recibe `SECTION_NO_LIVES_LOST`

**Escenario 2**  

*   **Dado**: un desafío resuelto al primer intento
*   **Cuando**: llega el resultado del Motor
*   **Entonces**: el alumno recibe `NODE_NO_RETRIES`

**Escenario 3**  

*   **Dado**: una insignia ya otorgada
*   **Cuando**: se repite el evento
*   **Entonces**: no se otorga de nuevo

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
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 5 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Accounting (vidas perdidas y recuperadas), Motor (reintentos).
*   Módulos afectados: Evaluador de criterios de insignias, outbox.
*   Otros equipos / aprobaciones: Accounting (si se implementa `LIFE_RECOVERED`).
*   Impacto en datos / migraciones: Si se quitan criterios, migración que los marque inactivos.
*   Riesgos y mitigación (opcional): Depende de eventos de Accounting que no consumimos; mitigación: quitar el criterio si no llegan a tiempo.

## Tareas

- [ ] T-21.7 Decidir qué criterios se implementan (E2)
- [ ] T-21.8 Evaluador de `SECTION_NO_LIVES_LOST`
- [ ] T-21.9 Evaluador de `NODE_NO_RETRIES`
- [ ] T-21.10 `LIFE_RECOVERED` o quitarlo
- [ ] T-21.11 Tests

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Tres criterios del catálogo nunca se otorgan: `SECTION_NO_LIVES_LOST`, `NODE_NO_RETRIES` y `LIFE_RECOVERED`.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E2]]
- [[sprints/sprint-3/08-dudas|E8]]
