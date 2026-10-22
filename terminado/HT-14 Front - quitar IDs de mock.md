---
tags: [tpi, g10, sprint-3, plan, HT-14, front]
fecha: 2026-10-15
autor: Benja
estado: hecho
historia: HT-14
tareas: [T-14.1, T-14.2, T-14.3, T-14.4]
repo: 2026-P4-FE/2026-PIV-TPI-FE
---

# HT-14 · Front — Sacar los IDs de mock del front

> [!info] Contexto
> Plan de [[sprints/sprint-3/historias/HT-14 Sacar los IDs de mock del front|HT-14]].
> - En Taiga las tareas T-14.1 a T-14.4 están asignadas a Lorenzo Araujo. Las tomamos nosotros (Benja): **reasignarlas en Taiga** antes de abrir el PR y marcarlas hechas al mergear.
> - **No tiene parte back:** es todo front.
> - Lo disparó el error del ranking con el curso de mock, ver [[T-45.7 Front - estados de error del ranking]] §1b.

## 1. Qué hay hoy (verificado en `origin/develop`)

Usos de los IDs de prueba **fuera** de tests y de los adaptadores en memoria (que son mocks y se quedan):

| Archivo | Línea | Uso | Tarea |
|---|---|---|---|
| `features/roadmap/data-access/roadmap/roadmap.store.ts` | 134 | `currentUser()?.id ?? DEMO_STUDENT_ID` | T-14.1 |
| `features/roadmap/data-access/challenge-attempt/challenge-attempt.service.ts` | 76 | `currentUser()?.id ?? DEMO_STUDENT_ID` | T-14.1 |
| `features/roadmap/pages/hex-world-page/hex-world-page.component.ts` | 462 | `currentUser()?.id ?? DEMO_STUDENT_ID` | T-14.1 |
| `features/roadmap/data-access/roadmap/roadmap.store.ts` | 139 | `signal(COURSE_SEED_ID)` como curso por defecto | T-14.2 |
| `features/ranking/ui/ranking-panel/ranking-panel.component.ts` | 364 | `getRanking(COURSE_SEED_ID)` | T-14.2 |
| `features/ranking/ui/ranking-detail/ranking-detail.component.ts` | 485 | `studentId === CURRENT_STUDENT_ID \|\| … user?.id` | T-14.3 |

- `ranking-page` ya no usa el mock: lo arregló el commit `37c515a4` (13/10).
- Se quedan con los IDs, porque son mocks: `mocks/seed.ts`, `in-memory-roadmap.adapter.ts`, `in-memory-ranking.adapter.ts` y los specs.

## 2. Pasos

Rama `fix/14-quitar-ids-mock` desde `develop`, **en un worktree aparte**: el checkout principal está en `fix/par-09-curve-v2` con cambios staged y no se toca.

1. **T-14.1 Alumno de la sesión.** En los tres lugares, sacar `?? DEMO_STUDENT_ID` y tomar `auth.currentUser()?.id`. Sin sesión: no seguir con un alumno fijo.
   - En lugar de eso, mostrar un error anunciado con `aria-live`, usando un componente de la UI-KIT (`generic-empty-state` o `generic-callout`).
   - Specs: dos alumnos distintos ven su propio progreso, y sin sesión aparece el error.
2. **T-14.2 Curso de la URL.**
   - `RoadmapStore`: el curso no arranca en `COURSE_SEED_ID`. Se fija desde la ruta (`:courseId`) y queda `null` hasta entonces.
   - `ranking-panel`: recibir el curso por `input()` (`readonly`) o desde la ruta, no `COURSE_SEED_ID`.
   - Sin curso en la ruta: error claro, nunca el curso de mock.
   - Specs: dos cursos distintos muestran datos distintos, y hay un caso sin curso en la ruta.
3. **T-14.3 Mi fila en el ranking.** En `ranking-detail`, comparar solo con `user?.id` de la sesión, sin `CURRENT_STUDENT_ID`. Spec: se resalta la fila del alumno logueado.
4. **T-14.4 Barrido final.** Esta búsqueda tiene que dar 0 fuera de `*.spec.ts`, `/mocks/` y `in-memory-*.adapter.ts`:
   ```bash
   git grep -n -E 'DEMO_STUDENT_ID|COURSE_SEED_ID|CURRENT_STUDENT_ID' -- src ':!*.spec.ts'
   ```
5. **Verificar:** `npm run verify` (lint + tests). **No correr `ng build` local.**

**Reglas** (las del repo, `AGENTS.md`):
- Componentes standalone.
- Propiedades `signal()`, `computed()`, `input()` y `output()` siempre `readonly`.
- Textos en `es.json` **y** `en.json` vía `core/i18n`.
- **Todo lo visual, de la UI-KIT `@2026-p4-fe/ui`:** no se crean componentes propios.

**Listo cuando:** la búsqueda del paso 4 da 0, cada tarea tiene su spec y `npm run verify` está en verde.

## 3. Convenciones de commits y PR (front)

- **Commits:** Conventional Commits, uno por tarea: `fix(roadmap): tomar el alumno de la sesión (T-14.1)`, `fix(ranking): leer el curso de la ruta (T-14.2)`, `fix(ranking): resaltar la fila del alumno logueado (T-14.3)`, `chore: sacar los ids de prueba fuera de mocks (T-14.4)`.
- **Nunca** `Co-Authored-By` ni atribución a IA.
- **PR:**
  - Hacia `develop`, con la plantilla `.github/pull_request_template.md`: Fix, Scope Angular Frontend, How to Test, evidencia del error sin sesión o sin curso, y el checklist (lint, stylelint, tests al 100 %, sin secretos ni URLs, accesibilidad, Conventional Commits).
  - 1 aprobación, sin automerge; reviewer según `CODEOWNERS` y los observadores de la tarea.
  - Comentario en cada tarea de Taiga con el enlace al PR.
- **Sin push** hasta que Benja lo revise.

## 4. Relación con T-45.7

- Este PR elimina una de las causas candidatas del error del ranking: el curso de mock.
- Para el CA1 de T-45.7 hay que citarlo, junto con `37c515a4`.
- Conviene mergearlo antes de probar T-45.7 con un front de `develop`.
