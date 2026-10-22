---
tags: [tpi, g10, decision, ranking, front]
fecha: 2026-10-22
estado: propuesta
reemplaza: ""
---

# DEC-022: Cómo muestra el front el ranking (vistas, orden y desempate)

> [!warning] Propuesta
> Son decisiones de producto tomadas en la revisión del ranking (PR front [#1003](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/1003), rama `feature/ranking-alumno`). Algunas se apartan del PRD o de [[decisiones/DEC-007-anonimato-ranking-en-servidor|DEC-007]]: están marcadas abajo para confirmarlas con el equipo y los profes.

## Contexto
La pantalla del ranking (`/ranking`, `/ranking/:courseId`) se revisó con UX/UI y con uso real. El back ya resuelve el anonimato y los puestos (DEC-007, DEC-019); el front decide cómo los muestra.

## Decisión

**Alumno**
- Ve los **3 primeros, su puesto y los 3 últimos**, con un separador donde se saltean puestos (1, 2, 3 ┄ 41 ┄ 98, 99, 100). Sin buscador, filtro de estado ni orden por columnas: su ranking va **siempre por XP**.
- Las filas ajenas siguen anónimas (DEC-007), con un nombre de programación estable por curso y lugar en la lista ("Lambda veloz", "Puntero audaz"; 512 combinaciones, sin repetir en un curso). El seudónimo del back queda de respaldo.
- La tarjeta propia dice cuánto XP falta para entrar a la zona de promoción (P90) y el avance de obligatorios ("Obligatorios aprobados: 25 %").
- Las reglas de promoción y de desempate están en la ayuda (ⓘ) junto al título.

**Staff (profesor, admin, gestor)**
- Buscador por nombre o legajo, filtro por estado, por grupo y "Limpiar filtros" (activo solo con algún filtro).
- **Orden XP / Notas como vista personal**: reordena solo lo que ve quien lo elige (guardado en su navegador) y no llama al back. El criterio del curso (T-45.11, PATCH del roadmap) ya no se cambia desde esta pantalla.
- **Ranking de grupos**: "Alumnos / Grupos". Cada grupo del curso con su XP promedio (todos sus integrantes) y su nota promedio (los que tienen nota), con detalle de integrantes. La composición sale de los participantes de Courses que el ranking ya lee.
- Exportar CSV (alumnos o grupos), con `;` y coma decimal en castellano.

**Ambos**
- **Puestos siempre consecutivos (1, 2, 3, 4…)**. En el orden del curso se respetan el orden y los criterios del back; lo que el back marca como compartido pasa a puestos seguidos, en el orden en que llega. En otro orden el front aplica la cascada RF-RNK-11 (insignias, menos vidas perdidas, ejercicios, quién llegó primero a ese XP).
- Zonas (solo con 10 o más inscriptos, RF-RNK-09): candidatos a promoción en **verde** (RF-RNK-05) y riesgo de regularidad en **rojo** (RF-RNK-06).
- Podio de tres escalones (plata, oro al centro, bronce), con medallas y confeti 3 s al entrar; un escalón sin dueño queda como "Puesto libre".
- El detalle se abre desde el podio, o desde el nombre para staff; no hay botón en cada fila.

## Se aparta de
- **RF-RNK-11 y DEC-007** ("si persiste el empate, misma posición"): el front numera consecutivo. Verificar con los profes; si se quiere un 5.º criterio real, va en el back.
- **RF-RNK-03** (el alumno ve top 3 y bottom 3 **identificados**): se mantienen anónimos, como DEC-007.
- **RF-RNK-07** (click en fila ajena muestra su detalle anónimo): el alumno solo abre su propio detalle; la fila ajena ya muestra lo mismo.
- **HU-45 CA5 / T-45.11** (el profesor elige el criterio del curso): ahora es una vista personal.

## Consecuencias
- Positivas: el alumno ve solo lo que le sirve; el profesor puede comparar grupos sin pedidos nuevos al back; los colores siguen el PRD.
- Negativas / deuda: el criterio oficial del curso queda sin pantalla de configuración; las diferencias con el PRD de arriba hay que confirmarlas.

## Referencias
- PR front [#1003](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/1003): `ranking-page`, `ranking-course-picker`, `ranking-groups`, `ranking-group-detail`, `domain/ranking.rules.ts` (`rankBy`, `rankGroups`), `domain/anonymous-alias.ts`.
- [[sprints/sprint-3/historias/HU-45 Ranking de la cohorte y avance por comisión|HU-45]], [[decisiones/DEC-007-anonimato-ranking-en-servidor|DEC-007]], [[decisiones/DEC-019-ranking-estado-de-datos-y-cache-de-respaldo|DEC-019]].
