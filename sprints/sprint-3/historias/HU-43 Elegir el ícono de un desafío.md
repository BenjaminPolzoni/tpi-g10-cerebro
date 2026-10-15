---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-43
estado: Propuesta
responsable: ""
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 1
prioridad: Could
en_taiga: true
---

# HU-43: Elegir el ícono de un desafío

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Ya existe en Taiga: [[taiga/historias/HU-43 Elegir el ícono de un desafío|HU-43]] (épica EP-4232). En el Sprint 3 se **reabre** con lo que falta.

[G10] — HU-43 — Elegir el ícono de un desafío
---------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: que el ícono de desafío solo se pueda asignar a nodos de desafío o examen
*   **Para**: que el roadmap no muestre íconos que confundan al alumno

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El ícono de desafío aplica a `THEORETICAL_CHALLENGE`, `PRACTICAL_CHALLENGE` y `EXAM`.
*   [ ] Validaciones: En otro tipo de nodo, 400 con un mensaje claro.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Asignar el ícono a un nodo `CONTENT` o `UNIT` devuelve 400.
*   [ ] **CA2**: Asignarlo a un desafío o examen funciona como hoy.
*   [ ] **CA3**: Un test por tipo de nodo.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Ícono según el tipo de nodo

**Escenario 1**  

*   **Dado**: un nodo de contenido
*   **Cuando**: el profesor le asigna el ícono de desafío
*   **Entonces**: recibe 400 con el motivo

**Escenario 2**  

*   **Dado**: un nodo de desafío práctico
*   **Cuando**: le asigna el ícono
*   **Entonces**: se guarda

**Escenario 3**  

*   **Dado**: un nodo examen
*   **Cuando**: le asigna el ícono
*   **Entonces**: se guarda

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

*   **Puntos (Fibonacci)**: 1
*   **Prioridad (MoSCoW / Numérica)**: Could

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 1 | Could |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: Validación de nodos en `GraphController`/servicio de nodos.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Ninguno.

## Tareas

- [ ] T-43.7 Validación del ícono por tipo de nodo
- [ ] T-43.8 Tests por tipo

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

El back acepta el ícono en cualquier tipo de nodo.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

Ninguna.
