---
tags: [tpi, g10, sprint-3, historia, hu]
id: B05
tipo: HU
epica: "EP-S3-0"
capa: "Back + Front"
esfuerzo: M
puntos: 5
prioridad: Should
estado: Propuesta
responsable: ""
taiga: "HU-20, HU-21"
depende: []
---

# B05: Completar insignias (HU-20 y HU-21)

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HU** · Capa: **Back + Front** · **5 pts** · **Should** · Taiga: [[taiga/historias/HU-20 Definir el catálogo de insignias del curso|HU-20]], [[taiga/historias/HU-21 Otorgar insignias automáticamente|HU-21]]
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-20, HU-21 — Completar insignias (HU-20 y HU-21)**

* * *

## Descripción (Como / Quiero / Para)

- **Como**: ALUMNO / PROFESOR
- **Quiero**: que todas las insignias del catálogo se puedan ganar, y poder editar y dar de baja las insignias de mi curso
- **Para**: que el catálogo no prometa insignias imposibles y el profesor lo mantenga sin pedir ayuda

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Cada criterio del catálogo tiene un evaluador que lo otorga, o se quita del catálogo (decisión E2). La baja es lógica: las insignias ya otorgadas se conservan (DEC-005). Las insignias del sistema no se editan desde un curso (DEC-006).
- [ ] Validaciones: Nombre obligatorio; ícono del catálogo de íconos.
- [ ] Seguridad (roles, permisos, datos sensibles): Editar y dar de baja: ADMIN o PROFESSOR dueño del curso.
- [ ] Accesibilidad (WCAG/teclado/lectores): Formulario con labels y foco gestionado (UI-KIT).

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: `SECTION_NO_LIVES_LOST`, `NODE_NO_RETRIES` y `LIFE_RECOVERED` se otorgan con su test, o se quitan del catálogo.
- [ ] **CA2**: El profesor edita nombre, descripción e ícono de una insignia de su curso desde el front.
- [ ] **CA3**: El profesor da de baja una insignia y las ya otorgadas se siguen viendo.
- [ ] **CA4**: Un profesor que no es dueño recibe 403.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Insignias completas

**Escenario 1**

- **Dado**: una sección completada sin perder vidas
- **Cuando**: se cierra el último nodo
- **Entonces**: el alumno recibe `SECTION_NO_LIVES_LOST`

**Escenario 2**

- **Dado**: una insignia de curso
- **Cuando**: el profesor dueño cambia su nombre
- **Entonces**: el alumno ve el nombre nuevo

**Escenario 3**

- **Dado**: una insignia ya otorgada
- **Cuando**: el profesor la da de baja
- **Entonces**: deja de otorgarse y el alumno que la tenía la sigue viendo

* * *

## Prototipo

- **Capturas**: Catálogo de insignias del profesor y vitrina del alumno.
- **URL Figma**: Pendiente.
- **Storybook**: `generic-badge-showcase`.
- **Mock API / Swagger**: PUT /api/roadmap/courses/{courseId}/badges/{badgeId} y baja lógica (DELETE o PATCH a definir).

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 5
- **Prioridad (MoSCoW / Numérica)**: Should

* * *

## Dependencias / Impactos

- Servicios involucrados: Accounting (vidas perdidas y recuperadas), Motor (reintentos).
- Módulos afectados: Evaluador de criterios de insignias, `BadgeCatalogController`, `badges-catalog-page`.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Sin migración (si se quitan criterios, migración que los marque inactivos).
- Riesgos y mitigación (opcional): `LIFE_RECOVERED` necesita un evento de Accounting que hoy no consumimos (E8).

## Tareas

- [ ] T-B05.1 Decidir con el equipo qué criterios se implementan (E2)
- [ ] T-B05.2 Implementar o quitar cada criterio con su test
- [ ] T-B05.3 Front: edición de insignias
- [ ] T-B05.4 Front: baja lógica de insignias

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

Tres criterios del catálogo nunca se otorgan: `SECTION_NO_LIVES_LOST`, `NODE_NO_RETRIES` y `LIFE_RECOVERED`. El front no permite editar ni dar de baja insignias.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E2]]
