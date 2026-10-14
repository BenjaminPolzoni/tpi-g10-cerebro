---
tags: [tpi, g10, taiga, hu]
codigo: HU-25
ref: 4242
estado: "Done"
responsable: "Lorenzo Araujo"
epica: "[G10] — Ranking y cierre académico"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4242
---

# HU-25: Desempatar el ranking en cascada

> [!info] Generado desde Taiga (2026-10-14 18:47). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4242) · Estado: **Done** · Responsable: **Lorenzo Araujo** · Sprint: **G10 - Sprint 2**

[G10] — HU-25 — Desempatar el ranking en cascada
------------------------------------------------


* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: que los empates en XP se resuelvan con una regla conocida
*   **Para**: entender por qué estoy arriba o abajo de alguien con mi mismo XP


* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: XP desc → más insignias (HU-21) → menos vidas perdidas → más ejercicios superados (completed_node). Si persiste el empate comparten posición.
*   [ ] Otros: La fuente de vidas perdidas depende de P-28 (lost_lives nunca se actualiza; Accounting no implementa lives-progress). Dependencias / impactos: Depende de: HU-24, HU-21. Servicios: G12 — Accounting (vidas perdidas, P-28). Preguntas abiertas: P-28.


* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Dos alumnos con igual XP se ordenan por insignias.
*   [ ] **CA2**: Con igual XP e insignias, por vidas perdidas.
*   [ ] **CA3**: Con todo igual, por ejercicios; si persiste, comparten posición.
*   [ ] **CA4**: La fila muestra qué criterio resolvió el desempate.


* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Desempate en cascada del ranking

**Escenario 1**  

*   **Dado**: dos alumnos con 300 XP, uno con 2 insignias y otro con 1
*   **Cuando**: se calcula el ranking
*   **Entonces**: el de 2 insignias queda arriba

**Escenario 2**  

*   **Dado**: igual XP e insignias, 1 y 3 vidas perdidas
*   **Cuando**: se calcula
*   **Entonces**: queda arriba el de 1

**Escenario 3**  

*   **Dado**: todos los criterios iguales
*   **Cuando**: se calcula
*   **Entonces**: comparten posición

* * *
Prototipo
---------

*   **Capturas**: Pendiente.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: Mismo endpoint de HU-24; detalle del desempate en la fila.


## Tareas

- [x] #4294 T-25.1 Desempate por cantidad de insignias · Closed · Lorenzo Araujo
- [x] #4295 T-25.2 Desempate por vidas perdidas (student_course.lost_lives, según P-28) · Closed · Lorenzo Araujo
- [x] #5389 T-25.3 Desempate por ejercicios superados · Closed · Lorenzo Araujo
- [x] #5390 T-25.4 Mismos casos de prueba que ranking.rules.ts en Java · Closed · Lorenzo Araujo
- [x] #5391 T-25.5 Front: detalle del criterio de desempate en la fila · Closed · Lorenzo Araujo
- [x] #5392 T-25.6 Wiki, OpenAPI y diagrama de secuencia · Closed · Quinteros Tomás
