---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-21
estado: Propuesta
responsable: ""
epica: "Correcciones de los profes"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Must
en_taiga: false
---

# HT-21: Seed de demo curado

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Correcciones de los profes|Correcciones de los profes]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HT-21 — Seed de demo curado
-----------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: un seed de demo con un curso completo, curado y reproducible
*   **Para**: levantar la demo siempre igual y mostrar todas las funciones

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Fuera del perfil productivo. Usa los usuarios demo de G07. Incluye START/END, tipos de relación, examen con ventana horaria y varias secciones.
*   [ ] Validaciones: Correrlo dos veces no duplica datos.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Script o migración `demo` separada del perfil productivo.
*   [ ] **CA2**: Un curso completo con todo lo del sprint.
*   [ ] **CA3**: Usa los usuarios demo de G07.
*   [ ] **CA4**: Es idempotente.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Seed de demo

**Escenario 1**  

*   **Dado**: un entorno vacío
*   **Cuando**: se corre el seed
*   **Entonces**: aparece el curso de demo completo

**Escenario 2**  

*   **Dado**: el seed ya corrido
*   **Cuando**: se corre otra vez
*   **Entonces**: no duplica datos

**Escenario 3**  

*   **Dado**: el perfil productivo
*   **Cuando**: arranca el servicio
*   **Entonces**: el seed no se ejecuta

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
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 5 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Users (usuarios demo), Courses (curso de demo).
*   Módulos afectados: Scripts de seed.
*   Otros equipos / aprobaciones: G07, G01.
*   Impacto en datos / migraciones: Datos de demo.
*   Riesgos y mitigación (opcional): Depende de HU-64, HU-65 y HU-67.

## Tareas

- [ ] T-21.1 Guion del curso de demo
- [ ] T-21.2 Script idempotente
- [ ] T-21.3 Probarlo en el entorno de demo

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Los datos de ejemplo se sacaron del micro (HT-09).

### Depende de

- [[sprints/sprint-3/historias/HU-64 Nodos de inicio y fin obligatorios|HU-64]] Nodos de inicio y fin obligatorios
- [[sprints/sprint-3/historias/HU-65 Relaciones con tipo|HU-65]] Relaciones con tipo
- [[sprints/sprint-3/historias/HU-67 Nodo examen con ventana horaria|HU-67]] Nodo examen con ventana horaria

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|E4]] La curva activa es la de Backoffice (1200/3500/7300 para los niveles 3/5/7).

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G7]] Usuarios demo de G07: todavía no hay.
