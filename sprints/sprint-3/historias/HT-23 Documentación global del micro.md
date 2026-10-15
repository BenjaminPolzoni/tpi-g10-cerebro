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

- [ ] **T-23.1 Escribir la guía del micro** · Docs
    - **Qué:** un documento en `docs/` del back con: qué hace roadmap-service, el modelo (Postgres y Neo4j), endpoints principales, eventos que publica y consume, flags (`SECTIONS_SYNC_ENABLED`, `ROADMAP_BY_GROUP_ENABLED`…), cómo levantarlo local y enlaces a decisiones y contratos. Se arma con lo que ya está en el Obsidian (`arquitectura/`, `decisiones/`, `acuerdos/`).
    - **Listo cuando:** alguien que no conoce el micro lo levanta y entiende qué hace leyendo solo ese documento.
- [ ] **T-23.2 Corregir los contratos que no coinciden con el código** · Docs
    - **Qué:** revisar `docs/contracts/` contra develop (DT-18). Por ejemplo, `roadmap-service.asyncapi.yaml` sigue en v3 y camelCase, y la documentación nombra `TraceIdFilter`, que se borró a propósito (E7).
    - **Listo cuando:** cada contrato coincide con develop.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

La documentación está repartida por tarea; el README del micro es básico.

### Depende de

Nada: se puede empezar ya.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|E7]] `TraceIdFilter` se borró a propósito: sacarlo de la documentación.
