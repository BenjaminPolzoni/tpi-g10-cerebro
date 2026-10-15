---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-23
estado: Propuesta
responsable: ""
epica: "Correcciones de los profes"
sprint: "G10 - Sprint 3"
puntos: 2
prioridad: Should
en_taiga: false
---

# HT-23: Documentación global del micro

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Correcciones de los profes|Correcciones de los profes]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

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

- [ ] T-23.1 Armar el documento
- [ ] T-23.2 Corregir contratos desactualizados

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

La documentación está repartida por tarea; el README del micro es básico.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E7]]

### Deuda técnica que cierra

- [[deuda-tecnica|DT-03]]
- [[deuda-tecnica|DT-18]]
