---
tags: [tpi, g10, taiga, hu]
codigo: HU-14
ref: 4238
estado: "Done"
responsable: "Fenoglio Santino"
epicas: "[[epicas/EP-70 Visualización del recorrido|EP-70]]"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4238
---

# HU-14: Ver mi recorrido como lista con sus bloqueos

> [!info] Generado desde Taiga (2026-10-15 16:53). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4238) · Estado: **Done** · Responsable: **Fenoglio Santino** · Sprint: **G10 - Sprint 2**
> Épica: [[epicas/EP-70 Visualización del recorrido|EP-70]] · Tareas cerradas: **5/5**

[G10] — HU-14 — Ver mi recorrido como lista con sus bloqueos
------------------------------------------------------------


* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: ver mi recorrido en lista con qué nodos tengo bloqueados y por qué
*   **Para**: saber qué me falta para avanzar


* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El motivo sale del mismo evaluador del gate (HU-15): prerrequisitos faltantes, lectura obligatoria pendiente, sin vidas, no disponible o de otro grupo (HU-44). Una unidad bloqueada muestra solo la existencia de sus nodos (HU-05).
*   [ ] Accesibilidad (WCAG/teclado/lectores): El estado y el motivo van en texto, no solo en color o ícono.
*   [ ] Otros: Dependencias / impactos: Relacionadas: HU-15 (Done), HU-16, HU-44. Preguntas abiertas: —


* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El alumno ve todas las unidades y nodos en lista con su estado.
*   [ ] **CA2**: Cada nodo bloqueado muestra el motivo en texto.
*   [ ] **CA3**: El motivo coincide con lo que responde el gate.


* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Lista con motivos de bloqueo

**Escenario 1**  

*   **Dado**: un nodo con un prerrequisito sin completar
*   **Cuando**: el alumno abre el recorrido
*   **Entonces**: ve el nodo bloqueado con el prerrequisito que falta

**Escenario 2**  

*   **Dado**: una lectura obligatoria pendiente
*   **Cuando**: abre el recorrido
*   **Entonces**: ve «lectura pendiente» en los desafíos de esa unidad

**Escenario 3**  

*   **Dado**: todos los prerrequisitos completos
*   **Cuando**: abre el recorrido
*   **Entonces**: ve el nodo disponible

* * *
Prototipo
---------

*   **Capturas**: Pendiente.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/progress extendido con el motivo por nodo.


## Tareas

- [x] #4279 T-14.1 Motivo de bloqueo por nodo en GET .../progress · Closed · Fenoglio Santino
- [x] #4280 T-14.2 Lista del recorrido por unidad con estado y motivo · Closed · Fenoglio Santino
- [x] #4281 T-14.3 Accesibilidad: estado en texto y teclado · Closed · Fenoglio Santino
- [x] #5383 T-14.4 BDD progress con motivos · Closed · Fenoglio Santino
- [x] #5384 T-14.5 Wiki, OpenAPI y diagrama de secuencia · Closed · Franco Maximiliano Amarilla
