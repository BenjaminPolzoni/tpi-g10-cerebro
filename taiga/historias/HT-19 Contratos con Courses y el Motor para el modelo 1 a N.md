---
tags: [tpi, g10, taiga, ht]
codigo: HT-19
ref: 8602
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8602
---

# HT-19: Contratos con Courses y el Motor para el modelo 1 a N

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8602) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Tareas cerradas: **1/5**

[G10] — HT-19 — Contratos con Courses y el Motor para el modelo 1 a N
---------------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: adaptar los contratos con Courses y con el Motor al modelo de varios roadmaps por curso
*   **Para**: que las integraciones sigan funcionando cuando un curso tenga N roadmaps

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Hoy cada sección se sincroniza con una sección de Courses (HU-36) y el Motor manda `id_course` + `id_node`.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: Los acuerdos se registran en `acuerdos/` y los contratos en `tpi-roadmap/docs/contracts/`.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Contrato con G01 para N roadmaps: el profesor elige por roadmap secciones de Courses o propias (P3) y define las restricciones de cada roadmap, que se copian al clonarlo (G4).
*   [ ] **CA2**: `node_id` único global, también en los roadmaps clonados (G8, confirmado el 2026-10-15).
*   [ ] **CA3**: Código y contratos actualizados.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Contratos para N roadmaps

**Escenario 1**

*   **Dado**: un curso con 2 roadmaps
*   **Cuando**: Courses publica una sección nueva
*   **Entonces**: llega al roadmap acordado

**Escenario 2**

*   **Dado**: un nodo del roadmap 2
*   **Cuando**: el Motor manda el resultado con `id_node`
*   **Entonces**: se registra en el roadmap correcto

**Escenario 3**

*   **Dado**: un curso con un roadmap que usa secciones de Courses y otro con secciones propias
*   **Cuando**: Courses cambia una sección
*   **Entonces**: el sync solo modifica el primer roadmap

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

*   Servicios involucrados: Courses, Motor.
*   Módulos afectados: Sync de secciones, listener del Motor.
*   Otros equipos / aprobaciones: G01, G09.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que G01 tarde en acordar; mitigación: proponer el mapeo por escrito la primera semana.


## Tareas

- [ ] #8946 T-19.1 Proponerle a Courses (G01) cómo se usan sus secciones con varios roadmaps · New · Mateo Delgado Costa
- [x] #8947 T-19.2 Confirmar con el Motor (G09) que node_id alcanza · Closed · Sin asignar
- [ ] #8948 T-19.3 Sincronizar secciones solo en los roadmaps que las usan · New · Baltasar Rodriguez Teruel
- [ ] #8950 T-19.4 Ubicar el roadmap correcto en los eventos del Motor · New · Baltasar Rodriguez Teruel
- [ ] #8953 T-19.5 Actualizar los contratos escritos · New · Quinteros Tomás
