---
tags: [tpi, g10, taiga, hu]
codigo: HU-37
ref: 4236
estado: "Done"
responsable: "Iker Alonso"
epica: "[G10] — Unidades del roadmap sincronizadas con Courses"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4236
---

# HU-37: Ver en el editor del roadmap las unidades de Cursos y sincronizarlas (front)

> [!info] Generado desde Taiga (2026-10-14 18:47). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4236) · Estado: **Done** · Responsable: **Iker Alonso** · Sprint: **G10 - Sprint 2**

[G10] — HU-37 — Ver en el editor del roadmap las unidades de Cursos y sincronizarlas (front)
--------------------------------------------------------------------------------------------


* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: armar los nodos del roadmap sobre las unidades que vienen de Cursos
*   **Para**: no mantener dos estructuras distintas del curso


* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El editor ya no crea, renombra, reordena ni borra secciones propias (addSection, updateSection, moveSection, removeSection): las unidades son de solo lectura y se editan en Cursos. Los nodos dentro de cada unidad se siguen editando acá (HU-41).
*   [ ] Accesibilidad (WCAG/teclado/lectores): Estados de carga y error en texto; operable por teclado.
*   [ ] Otros: Comparte course-builder-page con HU-41 y con la rama feature/roadmap-adapter-refinements: coordinar para no pisarse. Dependencias / impactos: Depende de: HU-36, HU-17. Relacionadas: HU-41, HU-04 (selector de material). Preguntas abiertas: —


* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El editor muestra las unidades de Cursos sin opciones de alta, renombre, orden ni baja.
*   [ ] **CA2**: El botón «Sincronizar con Cursos» actualiza la lista y muestra error reintentable si falla.
*   [ ] **CA3**: Una unidad dada de baja en Cursos con nodos se avisa al profesor.
*   [ ] **CA4**: Desde cada unidad hay un acceso a la sección en Cursos.


* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Editor con unidades de Cursos

**Escenario 1**  

*   **Dado**: un profesor en el editor
*   **Cuando**: abre el curso
*   **Entonces**: ve las unidades de Cursos sin botones de ABM de secciones

**Escenario 2**  

*   **Dado**: Courses no responde
*   **Cuando**: el profesor sincroniza
*   **Entonces**: ve un error con opción de reintentar

**Escenario 3**  

*   **Dado**: una sección dada de baja con nodos
*   **Cuando**: se sincroniza
*   **Entonces**: el editor muestra el aviso de HU-17

* * *
Prototipo
---------

*   **Capturas**: Pendiente.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: course-builder-page y course-map-page; endpoint de HU-36.


## Tareas

- [x] #4271 T-37.1 Quitar el ABM de secciones propias y mostrar las unidades de solo lectura · Closed · Iker Alonso
- [x] #4272 T-37.2 Botón «Sincronizar con Cursos» con carga y error reintentable · Closed · Iker Alonso
- [x] #4273 T-37.3 Aviso de unidades dadas de baja con nodos · Closed · Iker Alonso
- [x] #4274 T-37.4 Coordinar el editor (course-builder-page) con HU-04, HU-41 y HU-43 · Closed · Iker Alonso
- [x] #4275 T-37.5 Pruebas de componente y capturas · Closed · Iker Alonso
- [x] #5380 T-37.6 Wiki, OpenAPI y diagrama de secuencia · Closed · Quinteros Tomás
