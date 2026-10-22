---
tags: [tpi, g10, sprint-3, plan, fix, front]
fecha: 2026-10-20
autor: Benja
estado: en curso
repo: 2026-P4-FE/2026-PIV-TPI-FE
---

# Fix Front — la card del curso del alumno entra al modo elegido (simple o aventura)

- **Rama:** `fix/courses-card-modo-simple` (desde `origin/develop` `bfc040971`, 2026-10-20)
- **Worktree:** `Frontend/2026-PIV-TPI-FE-fix-card-modo-simple`
- **HU/Tarea Taiga:** sin asignar
- **Antes de empezar:** `npm ci` (la worktree no tiene `node_modules`). Tests con `NODE_OPTIONS=--no-experimental-webstorage` (Node 25).
- El archivo `PLAN-fix-card-modo-simple.md` de la raíz del worktree es una copia de este plan: no commitearlo.

## Objetivo
En "Mis Cursos", como alumno:
1. Un click en cualquier parte de la card del curso entra al curso.
2. Un **switch** en la toolbar ("Abrir cursos en Modo Aventura") elige a qué modo entra ese click:
   - Apagado (default): la card abre el **modo simple** (`opened` → `/courses/:id`).
   - Prendido: la card abre el **Modo Aventura** (`openRoadmap` → `/roadmap/play/:id`).
3. El botón de modo del pie de la card abre **el modo opuesto** al del switch:
   - Switch apagado → botón dorado "Modo Aventura".
   - Switch prendido → botón primario "Entrar/Continuar" (modo simple).
   Ya no se muestran los dos botones a la vez. **Ranking** queda igual.
4. La elección se recuerda en el navegador (preferencia de vista, nada sensible).

## Contexto
- Card: `src/app/features/courses/ui/student-course-card/` (`.html`, `.ts`, `.css`, `.spec.ts`).
  Dos layouts en el mismo template: `view() === 'list'` (`article.row-card`) y grilla (`article.grid-card`).
- Outputs de la card: `opened` (simple), `openRoadmap` (aventura), `chatOpened`. Los consume
  `ui/student-courses/student-courses.component.ts` → `course-list-page.component.ts` (`openStudentCourse()` / roadmap).
  El container no cambia.
- La toolbar (búsqueda, orden, grilla/lista) vive en `student-courses.component.ts` (template inline).
- Kit: `GenericSwitch` (`label`, `hint`, `disabled`, `[(checked)]`). No inventar un toggle propio.
- Patrón de preferencia en localStorage con try/catch: `features/accounting/data-access/bag-row-preferences.ts`.
  La regla #10 de AGENTS.md prohíbe tokens/roles; la clave no puede contener token/role/jwt/session/secret.
- Controles dentro de la card que **no** deben disparar el click de card:
  botón de modo, Ranking (`a[genericButton]`), "Ver mochila" del HUD (ya hace `stopPropagation()`),
  y todo `app-external-groups-panel` (botón Guía, links Telegram/Discord, drawer y confirm modal renderizados dentro).

## Implementación
1. **`courses/data-access/card-mode-preference.ts`** (nuevo, chico): `loadOpensAdventure(): boolean` y
   `saveOpensAdventure(value: boolean): void`, clave `tpi.courses.card-opens-adventure`, try/catch como bag-row-preferences.
2. **`student-courses.component.ts`**:
   - `readonly opensAdventure = signal(loadOpensAdventure());` y un `onOpensAdventureChange(v)` que setea y guarda.
   - En la toolbar: `<generic-switch [label]="'courses.student.cardMode.label' | t" [checked]="opensAdventure()" (checkedChange)="onOpensAdventureChange($event)" />`.
   - Pasar `[opensAdventure]="opensAdventure()"` a las dos `app-student-course-card`.
3. **`student-course-card.component.ts`**:
   - `readonly opensAdventure = input(false);`
   - Handler:
     ```ts
     /** The whole card opens the chosen mode, except clicks on its own controls. */
     protected onCardClick(event: MouseEvent): void {
       const target = event.target as Element | null;
       if (target?.closest('a, button, input, select, textarea, [role="dialog"], app-external-groups-panel')) return;
       const id = this.course().id;
       if (this.opensAdventure()) this.openRoadmap.emit(id);
       else this.opened.emit(id);
     }
     ```
4. **`student-course-card.component.html`**: `(click)="onCardClick($event)"` en los dos `<article>`.
   En `.row-action` y `.grid-foot`: `@if (opensAdventure())` → botón primario Entrar (`opened`), `@else` → botón dorado Aventura (`openRoadmap`).
   Ranking sin cambios. Sin `role="button"`/`tabindex` en el `article` (interactivo dentro de interactivo):
   por teclado se usa el botón del pie; el click en la card es atajo de mouse/touch.
5. **`student-course-card.component.css`**: `.tile-card { cursor: pointer; }`. Revisar que el pie de grilla
   (antes 3 botones) se vea bien con 2.
6. **i18n `src/assets/i18n/es.json` y `en.json`**: `courses.student.cardMode.label`
   ("Abrir cursos en Modo Aventura" / "Open courses in Adventure Mode") y, si se usa, `.hint`.
7. **Specs**:
   - Card (`'cards'` y `'list'`): switch apagado → click en título/descripción emite `opened` una vez; botón del pie es Aventura y emite `openRoadmap` sin `opened`.
     Switch prendido → click en la card emite `openRoadmap`; botón del pie es Entrar y emite `opened` una vez sin `openRoadmap`.
     Ranking y clicks dentro de `app-external-groups-panel` → no emiten nada.
   - `student-courses`: el switch cambia el input de las cards y guarda la preferencia.
   - `student-courses` y `course-list-page` hoy clickean `generic-button[variant="primary"]`: con el switch apagado
     ese botón ya no existe → ajustar esos tests (clickear la card o prender el switch).

## Verificación
- `NODE_OPTIONS=--no-experimental-webstorage npm run test` y `npm run lint:all` (o `npm run verify`).
- Manual (`npm run dev`), alumno en "Mis Cursos", grilla y lista, con el switch apagado y prendido:
  zona libre → modo del switch; botón del pie → modo opuesto; Ranking → `/ranking/:id`; Ver mochila → inventario;
  Guía de grupos → abre el drawer sin navegar; recargar → el switch conserva su estado.
- Leer `AGENTS.md`, `docs/design/SKILL.md` y `docs/skills/accessibility/SKILL.md` del repo FE (lo pide el hook para cambios de UI).

## Fuera de alcance
- Card del profesor (`cohort-card`): no se toca.
- Guardar la preferencia en el backend: por ahora solo el navegador.
