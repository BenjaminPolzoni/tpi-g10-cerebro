---
tags: [tpi, g10, taiga, hu]
codigo: HU-16
ref: 4237
estado: "Done"
responsable: "Lautaro Jesus Diego"
epica: "[G10] — Progreso y desbloqueo"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4237
---

# HU-16: Integración real con Inventario para las vidas del gate

> [!info] Generado desde Taiga (2026-10-14 18:47). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4237) · Estado: **Done** · Responsable: **Lautaro Jesus Diego** · Sprint: **G10 - Sprint 2**

[G10] — HU-16 — Integración real con Inventario para las vidas del gate
-----------------------------------------------------------------------


* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: que el roadmap use mis vidas reales del curso
*   **Para**: que el bloqueo por falta de vidas sea el mismo que veo en mi cuenta


* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Accounting es la fuente de verdad de las vidas (acta Roadmap ↔ Accounting v1). Si Accounting no responde se usa el último dato conocido (24 h) con stale=true y aviso; nunca se habilita por defecto. Con 0 vidas el gate rechaza con motivo.
*   [ ] Performance (tiempos, volumen, límites): Lectura con caché; el gate no espera más de 300 ms a Accounting.
*   [ ] Seguridad (roles, permisos, datos sensibles): Token técnico con audience y scope de Accounting (P-12).
*   [ ] Otros: Dependencias / impactos: Servicios: G12 — Accounting (audience y scope, P-12). Relacionadas: HU-40, HT-09 (T-09.5). Preguntas abiertas: P-12, P-28.


* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El gate usa las vidas que devuelve Accounting.
*   [ ] **CA2**: Con 0 vidas la entrega se rechaza con motivo «sin vidas».
*   [ ] **CA3**: Con Accounting caído se usa el último dato conocido marcado como desactualizado.
*   [ ] **CA4**: Sin ningún dato conocido la respuesta es 503, no «habilitado».


* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Vidas reales en el gate

**Escenario 1**  

*   **Dado**: un alumno con 2 vidas en Accounting
*   **Cuando**: consulta el gate
*   **Entonces**: ve 2 vidas y puede entregar

**Escenario 2**  

*   **Dado**: un alumno con 0 vidas
*   **Cuando**: intenta entregar
*   **Entonces**: rechazo con motivo «sin vidas»

**Escenario 3**  

*   **Dado**: Accounting caído y un dato de hace 1 h
*   **Cuando**: se consulta el gate
*   **Entonces**: responde con ese dato y stale=true

* * *
Prototipo
---------

*   **Capturas**: Pendiente.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: GET equip-summary de Accounting (ya consumido por T-35.1).


## Tareas

- [x] #4276 T-16.1 Cliente HTTP de vidas contra Accounting con token técnico; quitar el valor simulado · Closed · Lautaro Jesus Diego
- [x] #4277 T-16.2 Último dato conocido (24 h) y degradación con stale=true · Closed · Lautaro Jesus Diego
- [x] #4278 T-16.3 Gate con vidas reales y motivo «sin vidas» · Closed · Lautaro Jesus Diego
- [x] #5381 T-16.4 Contract test con Accounting y e2e · Closed · Lautaro Jesus Diego
- [x] #5382 T-16.5 Wiki, OpenAPI y diagrama de secuencia · Closed · Franco Maximiliano Amarilla
