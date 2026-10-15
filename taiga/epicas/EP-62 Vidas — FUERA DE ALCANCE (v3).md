---
tags: [tpi, g10, taiga, epica]
ref: 62
estado: "New"
responsable: "Ludmila Mailen Cejas"
avance: "0/0"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/62
---

# EP-62: Vidas — FUERA DE ALCANCE (v3)

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/62) · Estado: **New** · Responsable: **Ludmila Mailen Cejas** · HU cerradas: **0/0**

[G10] — Vidas — FUERA DE ALCANCE (v3)
-------------------------------------

* * *

Objetivo
--------

Esta épica pertenece al alcance anterior y **no forma parte del alcance v3**. La propiedad de las vidas pasó al dominio **Inventario** (ex-Coins/Wallet): Roadmap ya no las administra, sólo las lee para el gate.

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: Inventario persiste las vidas y los ítems. Roadmap las consulta para resolver el motivo sin\_vidas del gate y muestra el inventario para que el alumno equipe un ítem (HU-35), pero el Motor de Desafíos aplica la lógica del ítem y lo descuenta. El desafío de recuperación sigue siendo la excepción al gate por vidas (RF-REC-04).
*   Restricciones (legales/técnicas): no abrir historias contra esta épica. La lectura de vidas se planifica dentro de Progreso y desbloqueo, y la interfaz de inventario dentro de Nodos de contenido y lectura previa. Se conserva sin borrar por RF-NFR-01 (baja lógica) y para mantener la trazabilidad de las decisiones del Sprint 1.

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] No aplica: no hay flujo propio. El motivo sin\_vidas se verifica en los criterios de Progreso y desbloqueo.
*   [ ] KPIs iniciales: no aplica.
*   [ ] Sin regresiones críticas: no aplica, la épica no tiene código asociado.
*   [ ] Observabilidad y alertas: cubiertas por Progreso y desbloqueo (degradación de Inventario como origen externo).
*   [ ] Documentación publicada: el traspaso de las vidas a Inventario está documentado en G10-CONTRATOS-v3.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: ninguno propio. La lectura de vidas a Inventario vive en Progreso y desbloqueo.
*   Módulos afectados: ninguno propio.
*   Otros equipos: ninguno propio. Inventario es el dueño del dato.
*   Impacto en datos / migraciones: ninguno. Roadmap no persiste vidas ni su histórico.
*   Feature toggles / flags: no aplica.


## Historias

_Sin historias de G10._
