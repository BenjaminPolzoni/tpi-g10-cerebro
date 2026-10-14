---
tags: [tpi, g10, taiga, hu]
codigo: HU-19
ref: 4239
estado: "Done"
responsable: "Gabriela Camacho"
epicas: "[[epicas/EP-593 Nodos de contenido y lectura previa|EP-593]]"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4239
---

# HU-19: Ver el avance de lectura de mi unidad

> [!info] Generado desde Taiga (2026-10-14 20:44). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4239) · Estado: **Done** · Responsable: **Gabriela Camacho** · Sprint: **G10 - Sprint 2**
> Épica: [[epicas/EP-593 Nodos de contenido y lectura previa|EP-593]] · Tareas cerradas: **5/5**

[G10] — HU-19 — Ver el avance de lectura de mi unidad
-----------------------------------------------------


* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: ver cuánto me falta leer de cada unidad
*   **Para**: saber cuándo se habilitan los desafíos


* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Avance = contenidos obligatorios leídos / obligatorios de la unidad; los opcionales no cuentan. Reutiliza SectionReadingProgressService, el mismo cálculo que usa el gate.
*   [ ] Performance (tiempos, volumen, límites): Menos de 200 ms por unidad.
*   [ ] Otros: Dependencias / impactos: Relacionadas: HU-06, HU-11 (Done), HU-42, HU-46. Preguntas abiertas: —


* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Cada unidad muestra la barra con leídos y total en texto.
*   [ ] **CA2**: Marcar como leído actualiza la barra sin recargar.
*   [ ] **CA3**: Una unidad sin obligatorios muestra «sin lecturas obligatorias».


* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Avance de lectura de la unidad

**Escenario 1**  

*   **Dado**: una unidad con 4 obligatorios y 1 leído
*   **Cuando**: el alumno la abre
*   **Entonces**: ve 1 de 4

**Escenario 2**  

*   **Dado**: ese alumno
*   **Cuando**: marca otro como leído
*   **Entonces**: ve 2 de 4 sin recargar

**Escenario 3**  

*   **Dado**: una unidad sin obligatorios
*   **Cuando**: la abre
*   **Entonces**: ve «sin lecturas obligatorias»

* * *
Prototipo
---------

*   **Capturas**: Pendiente.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/sections/{sectionId}/reading-progress (propuesta); section-map-page.


## Tareas

- [x] #4282 T-19.1 Endpoint de avance de lectura por unidad reutilizando SectionReadingProgressService · Closed · Gabriela Camacho
- [x] #4283 T-19.2 Barra por unidad en section-map-page · Closed · Gabriela Camacho
- [x] #4284 T-19.3 Actualizar la barra al marcar leído sin recargar · Closed · Gabriela Camacho
- [x] #5385 T-19.4 BDD reading_progress · Closed · Gabriela Camacho
- [x] #5386 T-19.5 Wiki, OpenAPI y diagrama de secuencia · Closed · Franco Maximiliano Amarilla
