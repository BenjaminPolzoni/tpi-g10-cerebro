---
tags: [tpi, g10, taiga, hu]
codigo: HU-06
ref: 594
estado: "Done"
responsable: "Fenoglio Santino"
epicas: "[[epicas/EP-593 Nodos de contenido y lectura previa|EP-593]]"
sprint: "G10 - Sprint 1"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/594
---

# HU-06: Marcar un nodo de contenido como leído

> [!info] Generado desde Taiga (2026-10-15 23:01). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/594) · Estado: **Done** · Responsable: **Fenoglio Santino** · Sprint: **G10 - Sprint 1**
> Épica: [[epicas/EP-593 Nodos de contenido y lectura previa|EP-593]] · Tareas cerradas: **6/6**

[G10] — HU-06 — Marcar un nodo de contenido como leído
------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: marcar como leído un contenido de una unidad desbloqueada
*   **Para**: que mi avance cuente para habilitar los desafíos

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El registro es append-only con fecha e idempotente por alumno y nodo, garantizado con clave única en base. Está prohibido marcar en una unidad bloqueada. Dar de baja un nodo o dejarlo no disponible no borra las lecturas ni hace que sigan contando para la obligatoriedad.
*   [ ] Validaciones: El nodo tiene que ser de tipo CONTENIDO, estar en una unidad desbloqueada, y el alumno tiene que estar matriculado.
*   [ ] Datos obligatorios: Curso-cohorte y nodo; el alumno sale del token.
*   [ ] Performance (tiempos, volumen, límites): Respuesta en menos de 300 ms.
*   [ ] Seguridad (roles, permisos, datos sensibles): El alumno solo puede registrar y consultar sus propias lecturas.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Botón con el estado anunciado en texto.
*   [ ] Otros: Alimenta la proyección avance_lectura_unidad, que consume el gate de HU-15. No existe desmarcar: el registro es append-only. Trazabilidad: RF-NFR-01, DoD nivel 2. Dependencias: solo datos propios de E2 y E3, más el Gateway; ninguna dependencia externa de equipo. Datos: crea lectura_contenido con clave única por alumno y nodo. Riesgo: duplicados; mitigación, clave única en base.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El marcado queda registrado con su fecha.
*   [ ] **CA2**: Marcar de nuevo no duplica el registro.
*   [ ] **CA3**: En una unidad bloqueada el marcado se rechaza.
*   [ ] **CA4**: Dar de baja el nodo no borra las lecturas ya registradas.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Marcado de lectura de contenido por el alumno

**Escenario 1**  

*   **Dado**: una unidad desbloqueada con el nodo pendiente
*   **Cuando**: el alumno marca el contenido
*   **Entonces**: queda leído y se registra un movimiento con fecha

**Escenario 2**  

*   **Dado**: un nodo ya marcado
*   **Cuando**: el alumno repite el marcado
*   **Entonces**: no se duplica y sigue leído

**Escenario 3**  

*   **Dado**: una unidad bloqueada
*   **Cuando**: el alumno intenta marcar
*   **Entonces**: se rechaza sin registrar ningún movimiento

**Escenario 4**  

*   **Dado**: un nodo leído por varios alumnos
*   **Cuando**: el profesor lo da de baja
*   **Entonces**: las lecturas siguen existiendo y el nodo deja de contar

* * *
Prototipo
---------

*   **Capturas**: Boceto Marcado de lectura (alumno).
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente: botón de marcado con estado en texto.
*   **Mock API / Swagger**: POST /api/roadmap/nodos/{id}/lectura, idempotente por alumno y nodo.


## Tareas

- [x] #595 T-06.1 — Endpoint de marcado append-only idempotente · Closed · Fenoglio Santino
- [x] #596 T-06.2 — Validación de unidad desbloqueada · Closed · Fenoglio Santino
- [x] #597 T-06.3 — Proyección avance_lectura_unidad · Closed · Fenoglio Santino
- [x] #598 T-06.4 — Frontend: botón y estado · Closed · Fenoglio Santino
- [x] #599 T-06.5 — Tests BDD · Closed · Fenoglio Santino
- [x] #2889 T-06.6 — Wiki: secuencia del marcado de lectura · Closed · Quinteros Tomás
