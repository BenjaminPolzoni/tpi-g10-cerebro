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

*   [ ] Reglas de negocio: Fuera del perfil productivo. Usa los usuarios demo de G07; si no existen a tiempo, usa usuarios de prueba configurables y se reemplazan cuando G07 los publique. Incluye START/END, tipos de relación, examen con ventana horaria y varias secciones.
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
*   [ ] **CA3**: Usa los usuarios demo de G07 o, si todavía no existen, usuarios de prueba configurables.
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
*   Riesgos y mitigación (opcional): Depende de casi todo el sprint (ver «Depende de»); mitigación: el guion (T-21.1) se escribe la semana 1 y el seed se arma a medida que cierran las HU. Si G07 no tiene usuarios demo, se usan usuarios de prueba configurables.

## Tareas

- [ ] **T-21.1 Escribir el guion del curso de demo** · Equipo
    - **Qué:** definir el curso que se muestra: secciones, nodos de cada tipo, inicio y fin, relaciones con tipo, reglas combinadas, un examen con ventana de Courses, insignias, dos roadmaps y dos comisiones, y en qué punto está cada alumno demo.
    - **Listo cuando:** el guion está en el Obsidian y el equipo lo aprobó.
- [ ] **T-21.2 Cargar el curso del guion con un seed repetible** · Back
    - **Qué:** seed del curso del guion en el perfil `demo` (nunca en el productivo), con los usuarios demo de G07 y la curva PAR-09 de Backoffice (E4). Correrlo dos veces no duplica nada. Los ids de los usuarios demo todavía no existen (G7): mientras tanto, ids de prueba configurables por variable de entorno.
    - **Listo cuando:** base vacía → seed → la demo se puede recorrer completa.
- [ ] **T-21.3 Recorrer la demo de punta a punta en el entorno de demo** · Equipo
    - **Qué:** levantar el entorno de demo, correr el seed y seguir el guion con un alumno y un profesor.
    - **Listo cuando:** el recorrido sale sin errores; lo que falle queda anotado como issue.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Los datos de ejemplo se sacaron del micro (HT-09).

### Depende de

- [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial|HT-18]] Módulo graph en Neo4j y migración inicial
- [[sprints/sprint-3/historias/HU-57 Habilitar y gestionar varios roadmaps por curso|HU-57]] Habilitar y gestionar varios roadmaps por curso (dos roadmaps)
- [[sprints/sprint-3/historias/HU-58 Dependencias entre secciones|HU-58]] Dependencias entre secciones
- [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas|HU-59]] Dependencias entre nodos con reglas combinadas
- [[sprints/sprint-3/historias/HU-64 Nodos de inicio y fin obligatorios|HU-64]] Nodos de inicio y fin obligatorios
- [[sprints/sprint-3/historias/HU-65 Relaciones con tipo|HU-65]] Relaciones con tipo
- [[sprints/sprint-3/historias/HU-49 Aplicar en el roadmap las restricciones de sección y actividad que publica Courses|HU-49]] Restricciones de Courses y examen con ventana horaria
- [[sprints/sprint-3/historias/HT-30 Insignias pendientes de HU-20 y HU-21|HT-30]] Insignias pendientes de HU-20 y HU-21
- G07 Users: usuarios demo (G7). Si no llegan, usuarios de prueba configurables.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|E4]] La curva activa es la de Backoffice (1200/3500/7300 para los niveles 3/5/7).

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G7]] Usuarios demo de G07: todavía no hay.
