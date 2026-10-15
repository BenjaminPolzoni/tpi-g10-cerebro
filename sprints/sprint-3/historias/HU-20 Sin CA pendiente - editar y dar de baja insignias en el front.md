---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-20
estado: Propuesta
responsable: ""
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 3
prioridad: Should
en_taiga: true
---

# HU-20: Sin CA pendiente - editar y dar de baja insignias en el front

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Ya existe en Taiga: [[taiga/historias/HU-20 Definir el catálogo de insignias del curso|HU-20]] (épica EP-69). En el Sprint 3 se **reabre** con lo que falta.

[G10] — HU-20 — Definir el catálogo de insignias del curso
----------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: editar y dar de baja las insignias de mi curso desde el front
*   **Para**: mantener el catálogo sin pedir ayuda al equipo

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: La baja es lógica: las insignias ya otorgadas se conservan (DEC-005). Las insignias del sistema no se editan desde un curso (DEC-006).
*   [ ] Validaciones: Nombre obligatorio; ícono del catálogo de íconos.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN o PROFESSOR dueño del curso; un profesor que no es dueño recibe 403.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Formulario con labels y foco gestionado (UI-KIT).
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor edita nombre, descripción e ícono de una insignia de su curso desde el front.
*   [ ] **CA2**: El profesor da de baja una insignia y las ya otorgadas se siguen viendo.
*   [ ] **CA3**: Un profesor que no es dueño recibe 403.
*   [ ] **CA4**: Las insignias del sistema no muestran las acciones de editar ni dar de baja.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Mantenimiento del catálogo de insignias

**Escenario 1**  

*   **Dado**: una insignia de curso
*   **Cuando**: el profesor dueño cambia su nombre
*   **Entonces**: el alumno ve el nombre nuevo

**Escenario 2**  

*   **Dado**: una insignia ya otorgada
*   **Cuando**: el profesor la da de baja
*   **Entonces**: deja de otorgarse y el alumno que la tenía la sigue viendo

**Escenario 3**  

*   **Dado**: una insignia del sistema
*   **Cuando**: el profesor abre el catálogo
*   **Entonces**: no puede editarla ni darla de baja

* * *

Prototipo
---------

*   **Capturas**: Catálogo de insignias del profesor (`badges-catalog-page`).
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-badge-showcase`.
*   **Mock API / Swagger**: PUT /api/roadmap/courses/{courseId}/badges/{badgeId} y baja lógica (DELETE o PATCH a definir).

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 3
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 3 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: `BadgeCatalogController`, `badges-catalog-page`.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración (la baja usa el campo de baja lógica).
*   Riesgos y mitigación (opcional): Ninguno.

## Tareas

- [ ] T-20.8 Front: edición de insignias
- [ ] T-20.9 Front: baja lógica de insignias
- [ ] T-20.10 Endpoint de baja si no existe
- [ ] T-20.11 Tests

---

## Contexto del Sprint 3 (no va a Taiga)

### Criterios de la HU original (Taiga)

Verificados contra `origin/develop` (back `fc1917e`, front `67cbad4a`) el 2026-10-15. ✅ cumple · ❌ no cumple · ⚠️ hecho pero no anda de punta a punta.

- [x] ✅ **CA1**: El profesor ve las insignias del sistema y las de su curso. — `GET /courses/{id}/badges`
- [x] ✅ **CA2**: Crea una insignia con criterio válido y queda guardada. — `POST /courses/{id}/badges`
- [x] ✅ **CA3**: Un criterio fuera del catálogo se rechaza. — `BadgeValidation`
- [x] ✅ **CA4**: El front deja de usar localStorage. — el front ya no usa localStorage

### Qué hay hoy en el código

El front no permite editar ni dar de baja insignias.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

Ninguna.
