---
tags: [tpi, g10, taiga, epica]
ref: 4231
estado: "New"
responsable: "Sin asignar"
avance: "1/1"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/4231
---

# EP-4231: Niveles por curso

> [!info] Generado desde Taiga (2026-10-14 20:45). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/4231) · Estado: **New** · Responsable: **Sin asignar** · HU cerradas: **1/1**

[G10] — Niveles por curso
-------------------------

* * *

Objetivo
--------

Mostrarle al alumno su nivel en cada curso, derivado del XP del ledger con la curva PAR-09, y avisar cuando sube. RF-NIV es de G10 y del MVP, pero quedó sin épica cuando se cerró la épica de XP y niveles del backlog v3.

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: el nivel se deriva del XP total de xp\_movement y no se persiste como fuente. Curva PAR-09: 0 / 250 / 600 / 1.100 / 1.800 / 2.800 / 4.200 / 6.000 / 8.500 / 12.000, leída con ParCatalogClient, que ya existe. Los niveles son por curso-cohorte (RF-NIV-01).
*   Restricciones (legales/técnicas): son cosméticos, el ranking usa siempre el XP real (RF-NIV-05). Máximo 10 niveles (RF-NIV-04). Sin parámetros hardcodeados. Los niveles propios del profesor (RF-NIV-03) y por insignias (RF-NIV-02) quedan fuera hasta resolver P-06 con la cátedra.

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] Un alumno con 620 XP ve "Nivel 3" y cuánto le falta para el 4 (1.100). Al superar 1.100 XP ve el nivel 4 y se publica COURSE\_LEVEL\_UP una sola vez.
*   [ ] KPIs iniciales: ningún KPI de producto aplica. El indicador propio es que el nivel viaja en la misma respuesta de progreso, sin llamada extra, en menos de 200 ms.
*   [ ] Sin regresiones críticas en E3 y E6: el nivel no participa del gate ni del orden del ranking.
*   [ ] Observabilidad y alertas: log de cada subida de nivel; alerta si PAR-09 no está disponible y se sirve el último valor conocido.
*   [ ] Documentación publicada: la curva y la regla de derivación en la Wiki; COURSE\_LEVEL\_UP documentado con el envelope del bus.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: Backoffice (PAR-09, cliente existente) y Notificaciones (consume COURSE\_LEVEL\_UP, topic según P-09). Cátedra para P-06.
*   Módulos afectados: ProgressService (flujo de HU-03), respuesta de progreso, HUD del front.
*   Otros equipos: Notificaciones asigna el topic de COURSE\_LEVEL\_UP.
*   Impacto en datos / migraciones: ninguno obligatorio; el nivel es derivado.
*   Feature toggles / flags: ninguno.
*   Historias previstas: HU-38 (Sprint 2) y HU-39 (Sprint 3).


## Historias

| HU | Estado | Responsable | Sprint | Tareas |
|---|---|---|---|---|
| [[historias/HU-38 Ver mi nivel en el curso y cuánto me falta para el siguiente\|HU-38]] Ver mi nivel en el curso y cuánto me falta para el siguiente | Done | Benjamin Polzoni | G10 - Sprint 2 | 5/5 |
