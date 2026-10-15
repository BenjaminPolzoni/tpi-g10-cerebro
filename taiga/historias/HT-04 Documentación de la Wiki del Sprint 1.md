---
tags: [tpi, g10, taiga, ht]
codigo: HT-04
ref: 2844
estado: "Done"
responsable: "Franco Maximiliano Amarilla"
epicas: "Sin épica"
sprint: "G10 - Sprint 1"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/2844
---

# HT-04: Documentación de la Wiki del Sprint 1

> [!info] Generado desde Taiga (2026-10-15 16:53). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/2844) · Estado: **Done** · Responsable: **Franco Maximiliano Amarilla** · Sprint: **G10 - Sprint 1**
> Épica: Sin épica · Tareas cerradas: **2/2**

\[G10\] — HT-04 — Documentación de la wiki del Sprint 1
-------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: las páginas transversales de la Wiki del módulo, con la portada del servicio y el inventario de endpoints del sprint
*   **Para**: que cualquier integrante o grupo externo entienda qué hace Roadmap y Progreso y cómo consumirlo sin leer el código

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: No introduce reglas propias: es documentación. La fuente de verdad es lo implementado en el repo (migraciones, código mergeado y OpenAPI), nunca los documentos previos.
*   [ ] Validaciones: Toda página sigue la regla de nombrado GXX - TEMA y cada diagrama tiene su enlace Draw.io editable más su explicación.
*   [ ] Datos obligatorios: La portada del módulo y el listado de endpoints del sprint.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No se publican tokens, credenciales ni datos reales de personas; los ejemplos usan usuarios de prueba.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Cada diagrama lleva su explicación en texto, de modo que la información no dependa solo de la imagen.
*   [ ] Otros: Contiene solo lo transversal; la documentación de una historia concreta vive como tarea dentro de esa historia. Trazabilidad: DoD nivel 1. Dependencias: T-01.8 (Swagger publicado) y T-15.5 (contrato del gate). Riesgo: documentar contra versiones desactualizadas; mitigación, se valida contra el repo y quien implementó cada parte revisa.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: La portada publica descripción, alcance, fuera de alcance e índice, con links permanentes a las historias del sprint.
*   [ ] **CA2**: El listado de endpoints coincide con el OpenAPI vigente y enlaza al Swagger en lugar de duplicarlo.
*   [ ] **CA3**: Cada página respeta la regla de nombrado y la revisa quien implementó esa parte.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Documentación transversal de la Wiki

**Escenario 1**  

*   **Dado**: un integrante nuevo que no conoce el módulo
*   **Cuando**: abre la portada de la Wiki
*   **Entonces**: encuentra el alcance del servicio y el índice con links a las historias y a las páginas de diagramas

**Escenario 2**  

*   **Dado**: el Swagger publicado del servicio
*   **Cuando**: se compara con la página de endpoints
*   **Entonces**: los métodos, URLs y contratos coinciden, y la página enlaza al Swagger sin repetir su contenido

**Escenario 3**  

*   **Dado**: una página con un diagrama publicado
*   **Cuando**: otro grupo necesita modificarlo
*   **Entonces**: accede al archivo Draw.io editable desde el enlace de la página y encuentra la explicación del diagrama

* * *

Prototipo
---------

*   **Capturas**: No aplica: historia técnica sin pantalla propia.
*   **URL Figma**: No aplica.
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: La página de endpoints se construye sobre el Swagger real publicado en T-01.8 y el contrato del gate de T-15.5.

## Tareas

- [x] #2852 T-04.6 — Wiki: portada G10 - Roadmap y Progreso · Closed · Franco Maximiliano Amarilla
- [x] #2866 T-04.7 — Wiki: endpoints del Sprint 1 · Closed · Quinteros Tomás
