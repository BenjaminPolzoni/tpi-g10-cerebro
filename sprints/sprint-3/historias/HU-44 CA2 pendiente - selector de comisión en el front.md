---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-44
estado: Propuesta
responsable: ""
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Must
en_taiga: true
---

# HU-44: CA2 pendiente - selector de comisión en el front

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Ya existe en Taiga: [[taiga/historias/HU-44 Ver el roadmap de cada una de mis comisiones|HU-44]] (épica EP-5371). En el Sprint 3 se **reabre** con lo que falta.

[G10] — HU-44 — Ver el roadmap de cada una de mis comisiones
------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: ver el roadmap de cada una de mis comisiones
*   **Para**: seguir el curso según la comisión en la que estoy (2w1, 2w2…)

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El back ya filtra por comisión detrás de `ROADMAP_BY_GROUP_ENABLED` (modelo B, DEC-014). Con N roadmaps, el profesor configura si un roadmap se asigna por comisión o lo ven todos (P5). El motivo `group_restricted` se muestra en texto.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): El alumno solo ve sus comisiones.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Selector accesible con teclado (`generic-select`).
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Selector de comisión en el roadmap del alumno cuando tiene más de una.
*   [ ] **CA2**: El roadmap muestra lo habilitado para la comisión elegida.
*   [ ] **CA3**: El motivo `group_restricted` se muestra con un texto claro.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Roadmap por comisión

**Escenario 1**  

*   **Dado**: un alumno en las comisiones 2w1 y 2w2
*   **Cuando**: abre el roadmap
*   **Entonces**: elige la comisión y ve su roadmap

**Escenario 2**  

*   **Dado**: un alumno en una sola comisión
*   **Cuando**: abre el roadmap
*   **Entonces**: no ve el selector

**Escenario 3**  

*   **Dado**: un nodo restringido a otra comisión
*   **Cuando**: el alumno lo abre
*   **Entonces**: ve el motivo `group_restricted` en texto

* * *

Prototipo
---------

*   **Capturas**: Roadmap del alumno con selector de comisión.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-select`.
*   **Mock API / Swagger**: Endpoints existentes del roadmap con `ROADMAP_BY_GROUP_ENABLED`.

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

*   Servicios involucrados: Courses (comisiones).
*   Módulos afectados: Roadmap del alumno, `GroupSelectionService`.
*   Otros equipos / aprobaciones: G01.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Depende de que Courses tenga las comisiones de la demo.

## Tareas

- [ ] T-44.11 Selector de comisión
- [ ] T-44.12 Texto para `group_restricted`
- [ ] T-44.13 Tests

---

## Contexto del Sprint 3 (no va a Taiga)

### Criterios de la HU original (Taiga)

Verificados contra `origin/develop` (back `fc1917e`, front `67cbad4a`) el 2026-10-15. ✅ cumple · ❌ no cumple · ⚠️ hecho pero no anda de punta a punta.

- [ ] ⚠️ **CA1**: Un alumno solo de 2W1 no ve las unidades restringidas a 2W2. — hecho en el back, pero `ROADMAP_BY_GROUP_ENABLED` está en false
- [ ] ❌ **CA2**: Un alumno de 2W1 y 2W2 elige 2W2 y ve sus unidades con la misma XP. — el front no tiene selector de comisión
- [ ] ⚠️ **CA3**: El gate rechaza con group_restricted un nodo de una unidad que no es de ninguna comisión del alumno. — `group_restricted` existe, pero depende del mismo flag
- [ ] ⚠️ **CA4**: Con el mismo desafío en unidades de 2W1 y 2W2, el cierre del Motor suma la XP en el nodo correcto. — depende del mismo flag
- [x] ✅ **CA5**: Una cohorte sin comisiones se comporta igual que hoy. — con el flag apagado se comporta igual que antes

### Qué hay hoy en el código

El back filtra por comisión detrás de `ROADMAP_BY_GROUP_ENABLED`. El front no tiene selector de comisión.

### Depende de

Ninguna.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P5]] Lo configura el profesor: todos los roadmaps o por comisión.
