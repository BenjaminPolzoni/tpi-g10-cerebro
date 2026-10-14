---
tags: [tpi, g10, taiga, hu]
codigo: HU-22
ref: 4245
estado: "Done"
responsable: "Ludmila Mailen Cejas"
epicas: "[[epicas/EP-69 Logros e insignias|EP-69]]"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4245
---

# HU-22: Ver mis insignias

> [!info] Generado desde Taiga (2026-10-14 20:44). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4245) · Estado: **Done** · Responsable: **Ludmila Mailen Cejas** · Sprint: **G10 - Sprint 2**
> Épica: [[epicas/EP-69 Logros e insignias|EP-69]] · Tareas cerradas: **5/5**

[G10] — HU-22 — Ver mis insignias
---------------------------------


* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: ver las insignias que gané en el curso y las que me faltan
*   **Para**: saber qué logros puedo perseguir


* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Se muestran las ganadas con fecha y las pendientes con su criterio; solo del propio curso-cohorte.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Ícono con texto alternativo y nombre siempre visible.
*   [ ] Otros: Dependencias / impactos: Depende de: HU-20, HU-21. Preguntas abiertas: —


* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El alumno ve sus insignias ganadas con fecha.
*   [ ] **CA2**: Ve las pendientes con el criterio.
*   [ ] **CA3**: Sin insignias ve un estado vacío claro.


* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Vista de mis insignias

**Escenario 1**  

*   **Dado**: un alumno con 2 insignias
*   **Cuando**: abre sus insignias
*   **Entonces**: ve las 2 con fecha

**Escenario 2**  

*   **Dado**: un alumno sin insignias
*   **Cuando**: abre sus insignias
*   **Entonces**: ve el estado vacío

**Escenario 3**  

*   **Dado**: otro alumno
*   **Cuando**: consulta las insignias del primero
*   **Entonces**: 403

* * *
Prototipo
---------

*   **Capturas**: Pendiente.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/students/me/badges (propuesta).


## Tareas

- [x] #4300 T-22.1 Endpoint de insignias del alumno · Closed · Ludmila Mailen Cejas
- [x] #4301 T-22.2 HttpBadgesAdapter para las ganadas · Closed · Benjamin Polzoni
- [x] #5400 T-22.3 Estado vacío y pendientes con criterio · Closed · Benjamin Polzoni
- [x] #5401 T-22.4 BDD insignias del alumno · Closed · Ludmila Mailen Cejas
- [x] #5402 T-22.5 Wiki, OpenAPI y diagrama de secuencia · Closed · Quinteros Tomás
