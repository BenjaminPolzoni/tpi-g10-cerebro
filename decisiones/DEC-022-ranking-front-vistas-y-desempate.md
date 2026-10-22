---
tags: [tpi, g10, decision, ranking, front]
fecha: 2026-10-22
estado: aceptada
reemplaza: ""
---

# DEC-022: Cómo muestra el front el ranking (vistas, orden y desempate)

> [!info] Aceptada
> Son decisiones de producto tomadas en la revisión del ranking (PR front [#1003](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/1003), rama `feature/ranking-alumno`). Las diferencias con el PRD y con [[decisiones/DEC-007-anonimato-ranking-en-servidor|DEC-007]] de abajo las confirmó el equipo el 2026-10-22.

## Contexto
La pantalla del ranking (`/ranking`, `/ranking/:courseId`) se revisó con UX/UI y con uso real. El back ya resuelve el anonimato y los puestos (DEC-007, DEC-019); el front decide cómo los muestra.

## Decisión

**Alumno**
- Ve los **3 primeros, su puesto, los 3 últimos y las filas de los cortes P90 y P10** (RF-RNK-03), con un separador donde se saltean puestos (1, 2, 3 ┄ 10 ┄ 41 ┄ 91 ┄ 98, 99, 100). Sin buscador, filtro de estado ni orden por columnas: su ranking va **siempre por XP**.
- Las filas ajenas siguen anónimas (DEC-007), con un nombre de programación estable por curso y lugar en la lista ("Lambda veloz", "Puntero audaz"; 512 combinaciones, sin repetir en un curso). El seudónimo del back queda de respaldo.
- Cualquier fila abre su detalle (RF-RNK-07): la ajena, anónima y solo con números (XP, insignias, vidas, monedas, diferencia).
- La tarjeta propia dice cuánto XP falta para entrar a la zona de promoción (P90) y el avance de obligatorios ("Obligatorios aprobados: 25 %").

**Staff (profesor, admin, gestor)**
- Buscador por nombre o legajo, filtro por estado, por grupo y "Limpiar filtros" (activo solo con algún filtro).
- **Orden XP / Notas como vista personal**: reordena solo lo que ve quien lo elige (guardado en su navegador) y no llama al back. El criterio oficial del curso (T-45.11) lo configura Backoffice.
- **Ranking de grupos**: "Alumnos / Grupos". Cada grupo del curso con su XP promedio (todos sus integrantes) y su nota promedio (los que tienen nota), con detalle de integrantes. La composición sale de los participantes de Courses que el ranking ya lee.
- Exportar CSV (alumnos o grupos), con `;` y coma decimal en castellano.

**Ambos**
- **Puestos siempre consecutivos (1, 2, 3, 4…)**. En el orden del curso se respetan el orden y los criterios del back; lo que el back marca como compartido pasa a puestos seguidos, en el orden en que llega. En otro orden el front aplica la cascada RF-RNK-11 (insignias, menos vidas perdidas, ejercicios, quién llegó primero a ese XP).
- **Zonas, percentil y estado salen de esos puestos consecutivos**, en el orden del curso: P90 = el primer décimo de los inscriptos (mínimo 1), P10 = el último. El back cuenta el puesto compartido, y en un curso con muchos empatados en 0 XP nadie llegaba al último décimo (no había zona de riesgo).
- Zonas solo con 10 o más inscriptos (RF-RNK-09): candidatos a promoción en **verde** (RF-RNK-05) y riesgo de regularidad en **rojo** (RF-RNK-06). Columna "Percentil" (RF-RNK-02) y una marca "Corte P90" / "Corte P10" entre filas (RF-RNK-04); sin encabezados por zona ni filas reagrupadas.
- Sin tarjeta de "Requisitos de promoción": las reglas de promoción y de desempate están en la ayuda (ⓘ) junto al título.
- Podio de tres escalones (plata, oro al centro, bronce), con medallas 🥇🥈🥉 y confeti 3 s al entrar; un escalón sin dueño queda como "Puesto libre".
- El detalle se abre desde el podio o desde el nombre; no hay botón en cada fila. Muestra vidas con corazones (máximo del curso, PAR-12) y monedas, ambos de la cuenta de Accounting.
- Tooltips del kit (`generic-tooltip`), nunca el `title` nativo.

## Se aparta de (confirmado)
- **RF-RNK-11 y DEC-007** ("si persiste el empate, misma posición"): el front numera consecutivo.
- **RF-RNK-03** (el alumno ve top 3 y bottom 3 **identificados**): se mantienen anónimos, como DEC-007.

## Fuera del front
- **RF-RNK-10 / RF-RNK-13** (cierre del curso y su exportación): Courses.
- **HU-45 CA5 / T-45.11** (criterio oficial del curso): Backoffice.
- **RF-NOT-02** (avisar al entrar o salir de P90 / P10): back / notificaciones.
- Monedas de las filas anónimas: el endpoint del ranking no las trae; el detalle muestra "—".

## Consecuencias
- Positivas: el alumno ve solo lo que le sirve; el profesor puede comparar grupos sin pedidos nuevos al back; los colores y los cortes siguen el PRD; las zonas aparecen también con empates masivos.
- Negativas / deuda: el front y el back pueden diferir en la zona de una fila empatada; si se quiere una sola fuente, el back debería asignar las zonas con puestos consecutivos.

## Referencias
- PR front [#1003](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/1003): `ranking-page` (`withZones`, `cutPlaces`, `pageRows`), `ranking-course-picker`, `ranking-groups`, `ranking-group-detail`, `ranking-detail`, `domain/ranking.rules.ts` (`rankBy`, `rankGroups`), `domain/anonymous-alias.ts`.
- [[sprints/sprint-3/historias/HU-45 Ranking de la cohorte y avance por comisión|HU-45]], [[decisiones/DEC-007-anonimato-ranking-en-servidor|DEC-007]], [[decisiones/DEC-019-ranking-estado-de-datos-y-cache-de-respaldo|DEC-019]].
