---
tags: [tpi, g10, taiga, epica]
ref: 72
estado: "New"
responsable: "Sin asignar"
avance: "0/0"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/72
---

# EP-72: Avatares

> [!info] Generado desde Taiga (2026-10-14 20:45). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/72) · Estado: **New** · Responsable: **Sin asignar** · HU cerradas: **0/0**

[G10] — Avatares
----------------

* * *

Objetivo
--------

Que el alumno elija su avatar de un catálogo de skins por curso, desbloqueables por nivel, insignia o monedas, y lo vea reflejado en el HUD y en su fila del ranking. Es la capa de identidad visual del progreso. Fase 2.

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: el catálogo de avatares y la regla de desbloqueo son nuestros, igual que el catálogo de insignias. El desbloqueo se evalúa contra las insignias otorgadas en E4 y contra el nivel derivado del XP que leemos del ledger propio. La compra con monedas la resuelve Inventario; nosotros recibimos la confirmación y registramos el desbloqueo.
*   Restricciones (legales/técnicas): el avatar es cosmético total y no afecta XP, vidas, desbloqueo ni posición en el ranking. La selección es por curso-cohorte. El avatar de juego es un dato distinto del avatar\_url institucional que provee Usuarios: hay que distinguirlos en el modelo para no pisarlos. Un avatar bloqueado no se puede seleccionar aunque se llame directamente al endpoint. Se respeta el anonimato del ranking: el avatar viaja en la fila ajena, el nombre no (RF-RNK-03). El límite con Mercado queda por acordar.

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] El alumno abre el catálogo, ve cuáles tiene disponibles y cuáles bloqueados con su condición, elige uno y el cambio se refleja en el HUD y en su fila del ranking. Alcanzar el nivel o la insignia que desbloquea un avatar lo habilita solo.
*   [ ] KPIs iniciales: ningún KPI de producto aplica, el avatar es cosmético y no mueve ninguna métrica académica. El indicador propio es que el avatar elegido se refleja en el HUD en la misma carga de página, sin refresco manual.
*   [ ] Sin regresiones críticas en el anonimato del ranking: la fila ajena sigue viajando sin nombre (RF-RNK-03), y un avatar bloqueado no se puede seleccionar ni llamando directamente al endpoint.
*   [ ] Observabilidad y alertas: log de cada desbloqueo con el criterio que lo disparó (nivel, insignia o compra). Alerta ante un desbloqueo por compra sin confirmación de Inventario.
*   [ ] Documentación publicada: catálogo de avatares y condiciones de desbloqueo en la Wiki, junto con el límite acordado con Mercado sobre qué es avatar (nuestro) y qué es equipamiento (de ellos).

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: Inventario (confirmación de la compra con monedas), Usuarios (avatar institucional, que es un dato distinto), Mercado (límite con el equipamiento cosmético).
*   Módulos afectados: catálogo de avatares, evaluador de desbloqueo, HUD de progreso, fila del ranking.
*   Otros equipos: Mercado y nosotros debemos acordar por escrito el límite entre avatares del curso y equipamiento del personaje.
*   Impacto en datos / migraciones: tablas de catálogo de avatares y de avatar seleccionado por alumno y curso-cohorte, más el desbloqueo derivado de XP e insignias.
*   Feature toggles / flags: avatares, con la épica entera detrás del flag. Es cosmético y es Fase 2: apagarlo no toca XP, vidas, desbloqueo ni posición en el ranking, la fila se dibuja igual con el avatar por defecto. Plan de retiro: no se retira mientras la épica siga en Fase 2; cuando pase a alcance firme y sea estable en producción, se elimina el flag.


## Historias

_Sin historias de G10._
