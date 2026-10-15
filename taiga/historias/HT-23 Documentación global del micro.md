---
tags: [tpi, g10, taiga, ht]
codigo: HT-23
ref: 8606
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8631 Correcciones de los profes|EP-8631]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8606
---

# HT-23: Documentación global del micro

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8606) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8631 Correcciones de los profes|EP-8631]] · Tareas cerradas: **0/2**

[G10] — HT-23 — Documentación global del micro
----------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: un documento global del micro: qué hace, modelo, endpoints, eventos, flags, cómo levantarlo y decisiones
*   **Para**: que cualquiera entienda el servicio sin preguntar

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Se arma desde el cerebro (`arquitectura/`, `decisiones/`, `acuerdos/`) y los contratos del repo.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: Incluye la matriz de roles y permisos (HT-22).

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Documento global en el repo del back.
*   [ ] **CA2**: Incluye modelo, endpoints, eventos, flags y cómo levantarlo.
*   [ ] **CA3**: Enlaza decisiones y contratos.
*   [ ] **CA4**: Contratos desactualizados corregidos (DT-18).

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Documentación global

**Escenario 1**  

*   **Dado**: un integrante nuevo
*   **Cuando**: lee el documento
*   **Entonces**: levanta el servicio sin ayuda

**Escenario 2**  

*   **Dado**: otro grupo
*   **Cuando**: busca qué eventos publicamos
*   **Entonces**: los encuentra con su contrato

**Escenario 3**  

*   **Dado**: un flag
*   **Cuando**: se busca en el documento
*   **Entonces**: dice qué hace y su valor por defecto

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

*   **Puntos (Fibonacci)**: 2
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 2 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: `docs/` del back.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Ninguno.


## Tareas

- [ ] #9094 T-23.1 Escribir la guía del micro · New · Franco Maximiliano Amarilla
- [ ] #9095 T-23.2 Corregir los contratos que no coinciden con el código · New · Quinteros Tomás
