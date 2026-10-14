---
tags: [tpi, g10, taiga, hu]
codigo: HU-21
ref: 4244
estado: "Done"
responsable: "Ludmila Mailen Cejas"
epica: "[G10] — Logros e insignias"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4244
---

# HU-21: Otorgar insignias automáticamente

> [!info] Generado desde Taiga (2026-10-14 18:47). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4244) · Estado: **Done** · Responsable: **Ludmila Mailen Cejas** · Sprint: **G10 - Sprint 2**

[G10] — HU-21 — Otorgar insignias automáticamente
-------------------------------------------------


* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: recibir una insignia apenas cumplo su criterio
*   **Para**: ver reconocido mi avance sin pedirlo


* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El evaluador corre al procesar el cierre del Motor (ProgressService), es idempotente (un replay no otorga dos veces) y publica BADGE_AWARDED por outbox. «Sección en un día» y «primero en completar» se calculan con completed_at.
*   [ ] Otros: El topic depende de P-09; sin topic las filas quedan PENDING (como NODE_COMPLETED). Dependencias / impactos: Depende de: HU-20. Servicios: Notificaciones (P-09), Plataforma (topic). Preguntas abiertas: P-09.


* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Cumplir un criterio otorga la insignia una sola vez.
*   [ ] **CA2**: Un replay del mismo cierre no duplica.
*   [ ] **CA3**: Se publica BADGE_AWARDED por outbox.
*   [ ] **CA4**: Los criterios de tiempo usan completed_at.


* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Otorgamiento automático de insignias

**Escenario 1**  

*   **Dado**: una insignia MIN_XP 500 y un alumno con 480
*   **Cuando**: completa un desafío de 30 XP
*   **Entonces**: recibe la insignia

**Escenario 2**  

*   **Dado**: ese mismo cierre reenviado
*   **Cuando**: se procesa
*   **Entonces**: no se otorga otra vez

**Escenario 3**  

*   **Dado**: un alumno que completa toda una sección en un día
*   **Cuando**: cierra el último nodo
*   **Entonces**: recibe la insignia «sección en un día»

* * *
Prototipo
---------

*   **Capturas**: Pendiente.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: Evaluador dentro del consumo del cierre; outbox V15.


## Tareas

- [x] #4298 T-21.1 Evaluador de criterios idempotente al procesar el cierre · Closed · Ludmila Mailen Cejas
- [x] #4299 T-21.2 BADGE_AWARDED por outbox · Closed · Ludmila Mailen Cejas
- [x] #5397 T-21.3 Criterios por tiempo con completed_at · Closed · Ludmila Mailen Cejas
- [x] #5398 T-21.4 BDD otorgamiento y replay · Closed · Ludmila Mailen Cejas
- [x] #5399 T-21.5 Wiki, OpenAPI y diagrama de secuencia · Closed · Quinteros Tomás
- [x] #6516 T-21.6 Criterio ZONE_P90 con el ranking de la cohorte · Closed · Ludmila Mailen Cejas
