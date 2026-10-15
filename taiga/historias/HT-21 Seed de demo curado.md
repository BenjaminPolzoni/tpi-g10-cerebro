---
tags: [tpi, g10, taiga, ht]
codigo: HT-21
ref: 8604
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8631 Correcciones de los profes|EP-8631]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8604
---

# HT-21: Seed de demo curado

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8604) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8631 Correcciones de los profes|EP-8631]] · Tareas cerradas: **0/4**

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

- [ ] #9087 T-21.1 Escribir el guion del curso de demo · New · Benjamin Polzoni
- [ ] #9088 T-21.2 Cargar el curso del guion con un seed repetible · New · Benjamin Polzoni
- [ ] #9089 T-21.3 Recorrer la demo de punta a punta en el entorno de demo · New · Benjamin Polzoni
- [ ] #9339 T-21.4 Wiki, OpenAPI y diagrama de secuencia · New · Quinteros Tomás
