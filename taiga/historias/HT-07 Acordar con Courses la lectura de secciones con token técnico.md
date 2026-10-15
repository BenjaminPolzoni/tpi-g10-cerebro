---
tags: [tpi, g10, taiga, ht]
codigo: HT-07
ref: 4233
estado: "Done"
responsable: "Mateo Delgado Costa"
epicas: "[[epicas/EP-4230 Unidades del roadmap sincronizadas con Courses|EP-4230]]"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4233
---

# HT-07: Acordar con Courses la lectura de secciones con token técnico

> [!info] Generado desde Taiga (2026-10-14 20:44). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4233) · Estado: **Done** · Responsable: **Mateo Delgado Costa** · Sprint: **G10 - Sprint 2**
> Épica: [[epicas/EP-4230 Unidades del roadmap sincronizadas con Courses|EP-4230]] · Tareas cerradas: **5/5**

[G10] — HT-07 — Acordar con Courses la lectura de secciones con token técnico
-----------------------------------------------------------------------------


* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: acordar por escrito con Courses que GET /api/course/course-cohorts/{id}/sections acepte nuestro token técnico, y activar HttpCourseSectionsClient en modo http
*   **Para**: que el roadmap reciba las unidades reales de Cursos y no las dos por defecto


* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Courses es la única fuente de las secciones. Las llamadas van por el Gateway y con token técnico, nunca con el JWT de una persona (agent.md §2.5). Si G01 no habilita el token a tiempo rige el plan B: se construye contra el doble con el flag unidades-desde-courses apagado. Justificación técnica: Ningún usuario la percibe, pero sin ella HU-36, HU-17 y HU-18 no tienen fuente de datos: hoy COURSES_SECTIONS_CLIENT_MODE=stub por defecto, PendingCourseSectionsClient lanza «sin acta» e init-mvp cae a dos unidades fijas. Courses no acepta token de servicio en GET /course-cohorts/{id}/sections (solo GESTOR, PROFESSOR y STUDENT).
*   [ ] Validaciones: El cliente lee todas las páginas (hoy solo la primera de 50), filtra inactivas y ordena por orderIndex.
*   [ ] Seguridad (roles, permisos, datos sensibles): Audience y scope del token técnico definidos en el acta; 401/403 de Courses se registran y no se reintentan en bucle.
*   [ ] Otros: El acta se archiva en tpi-roadmap/docs/contracts/ y en la Wiki. Dependencias / impactos: Servicios: G01 (bloqueante: token técnico en secciones). Relacionadas: HU-36, HU-17, HU-18, HT-09 (T-09.2). Preguntas abiertas: P-11, P-20.


* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Existe un acta firmada con G01 con endpoint, token técnico, paginación y errores.
*   [ ] **CA2**: Con el perfil integrado el cliente de secciones corre en modo http y lee todas las páginas.
*   [ ] **CA3**: El perfil integrado no arranca si el cliente queda en stub (validación al arrancar).
*   [ ] **CA4**: Un 401/403/503 de Courses devuelve un error explícito, nunca unidades inventadas.


* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Lectura de secciones con identidad de servicio

**Escenario 1**  

*   **Dado**: una cohorte con 60 secciones en Courses
*   **Cuando**: Roadmap las lee con el token técnico
*   **Entonces**: recibe las 60 ordenadas por orderIndex y sin las inactivas

**Escenario 2**  

*   **Dado**: Courses rechaza el token
*   **Cuando**: se pide la lista de secciones
*   **Entonces**: error explícito registrado en el log y sin unidades por defecto

**Escenario 3**  

*   **Dado**: el perfil integrado con el cliente en stub
*   **Cuando**: arranca el servicio
*   **Entonces**: el arranque falla con un mensaje claro

* * *
Prototipo
---------

*   **Capturas**: Pendiente.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: GET /api/course/course-cohorts/{id}/sections vía Gateway. CourseSectionsClient existente (hoy solo lo usa init-mvp).


---
ACTUALIZACION (plan vigente - scopes H1)
- Estado: implementado. La lectura de secciones con identidad de servicio quedo como M2M con el scope `course.sections.read` (ver G01-US-23 #6639).
- Scopes finales (hibrido H1): grupos=`course.groups.read`; participantes=`course.enrollment.read`; secciones=`course.sections.read`; restricciones de seccion y de nodo/actividad=`course.restrictions.read`; orden/material de actividades=`course.activities.read`.
- Modelo B: un roadmap por cohorte (la vista por comision es filtrada); restricciones por PULL, no por evento.

## Tareas

- [x] #4260 T-07.1 Redactar y acordar el acta con G01 (token técnico, paginación, errores, eventos opcionales) · Closed · Mateo Delgado Costa
- [x] #4261 T-07.2 Audience y scope del token y COURSES_SECTIONS_CLIENT_MODE=http; leer todas las páginas · Closed · Mateo Delgado Costa
- [x] #4262 T-07.3 Vista de servicio: descartar ocultas (isVisible) + contract tests S7.7 · Closed · Ludmila Mailen Cejas
- [x] #4263 T-07.4 Validación al arrancar: el perfil integrado no levanta con el cliente en stub · Closed · Mateo Delgado Costa
- [x] #4264 T-07.5 Wiki, OpenAPI y diagrama de secuencia · Closed · Quinteros Tomás
