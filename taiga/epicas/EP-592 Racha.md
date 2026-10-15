---
tags: [tpi, g10, taiga, epica]
ref: 592
estado: "New"
responsable: "Sin asignar"
avance: "0/0"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/592
---

# EP-592: Racha

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/592) · Estado: **New** · Responsable: **Sin asignar** · HU cerradas: **0/0**

[G10] — Racha
-------------

* * *

Objetivo
--------

Mostrar al alumno su racha de días consecutivos con actividad resuelta —entrar y resolver correctamente un ejercicio— como incentivo de constancia, y usarla como criterio de otorgamiento de insignias. Por ejemplo, 50 días consecutivos otorgan una insignia.

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: la racha se calcula sobre hechos que ya administramos —nodos completados y contenidos obligatorios leídos— y no requiere pedirle nada a ningún otro equipo. Es por curso-cohorte y la zona horaria de corte del día es la del curso, no la del navegador del alumno. La racha vigente se deriva del registro de actividad diaria; la máxima se persiste. Dos actividades el mismo día cuentan como un solo día.
*   Restricciones (legales/técnicas): no hay comodines en el MVP; un día sin actividad corta la racha. La racha es cosmética: no habilita ni bloquea ninguna entrega. No tiene RF en el PRD (P-07), así que va detrás de flag hasta que el PO la incorpore o la declare alcance extra.

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] Un alumno resuelve algo tres días seguidos y ve racha 3; se saltea un día y al volver ve racha 1 con máxima 3. Dos actividades el mismo día cuentan como un día.
*   [ ] KPIs iniciales: ningún KPI de producto aplica. El indicador propio es que la consulta de racha responde en menos de 200 ms y se muestra en la misma carga de la pantalla de progreso, sin una llamada extra.
*   [ ] Sin regresiones críticas en E2 y E3: registrar actividad para la racha no altera ningún estado de desbloqueo ni ninguna lectura. Es una lectura derivada, no una escritura de progreso.
*   [ ] Observabilidad y alertas: distribución de rachas vigentes por curso. Alerta si la racha de un alumno crece más de un día por día real, que sería una falla del corte horario o de idempotencia.
*   [ ] Documentación publicada: definición operativa de "día con actividad" y de la zona horaria de corte en la Wiki, más el endpoint de racha en OpenAPI.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: ninguno externo. Es la única épica del tema sin dependencia de otro equipo.
*   Módulos afectados: registro de actividad diaria, cálculo de racha, HUD de progreso y evaluador de criterios de insignia (E4).
*   Otros equipos: ninguno.
*   Impacto en datos / migraciones: tabla nueva actividad\_diaria (alumno, curso-cohorte, día) con clave única compuesta por los tres campos, y campo nuevo racha\_maxima por alumno y curso-cohorte. Migración: crear tabla y campo, sin datos históricos que migrar.
*   Feature toggles / flags: racha, con la épica entera detrás del flag desde el primer commit, porque es cosmética y todavía no está trazada al PRD (P-07). Plan de retiro: se mantiene el flag hasta que el PO incorpore la racha al PRD o la declare alcance extra.


## Historias

_Sin historias de G10._
