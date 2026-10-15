---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-15
estado: Propuesta
responsable: ""
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 2
prioridad: Must
en_taiga: false
---

# HT-15: Poner Taiga al día

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HT-15 — Poner Taiga al día
----------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: que Taiga refleje el estado real del código y tenga cargadas las historias del Sprint 3
*   **Para**: planificar y evaluar sobre datos ciertos

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Taiga es la fuente de verdad del estado de las HU. Una HU que no cumple sus CA no puede estar en Done.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: Después de cargar, correr `scripts/taiga_sync.py` para actualizar el cerebro.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Las HU que no cumplen sus CA vuelven a In progress (ver HU-48 a HU-41 y HU-01).
*   [ ] **CA2**: Las épicas con todas sus HU cerradas pasan a Done (E10).
*   [ ] **CA3**: HT-11 actualizado a snake_case v8.
*   [ ] **CA4**: HT-04, HT-05, HT-10 y HT-11 con épica o tag `g10` (E11).
*   [ ] **CA5**: Las historias de este sprint cargadas en Taiga con su código.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Taiga al día

**Escenario 1**  

*   **Dado**: HU-44 en Done sin selector de comisión en el front
*   **Cuando**: se revisa Taiga
*   **Entonces**: vuelve a In progress con un comentario

**Escenario 2**  

*   **Dado**: HT-05 sin épica ni tag
*   **Cuando**: se le agrega el tag `g10`
*   **Entonces**: aparece en el cerebro al correr el sync

**Escenario 3**  

*   **Dado**: las notas de `historias/` del Sprint 3
*   **Cuando**: se cargan en Taiga
*   **Entonces**: cada nota tiene su código de Taiga en la propiedad `taiga`

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
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 2 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Taiga.
*   Módulos afectados: Ninguno.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Ninguno.

## Tareas

- [ ] T-15.1 Reabrir las HU incompletas
- [ ] T-15.2 Ordenar épicas, tags y HT-11
- [ ] T-15.3 Cargar las historias del Sprint 3
- [ ] T-15.4 Correr el sync del cerebro

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

15 de 17 épicas están en New aunque sus HU estén Done. HT-11 dice camelCase y el código usa snake_case. HT-04, HT-10 y HT-11 no tienen épica, y HT-05 no tiene ni épica ni tag.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E10]]
- [[sprints/sprint-3/08-dudas|E11]]

### Deuda técnica que cierra

- [[deuda-tecnica|DT-19]]
