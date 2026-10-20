---
tags: [tpi, g10, sprint-3, plan, front]
fecha: 2026-10-20
autor: Benja
estado: borrador
repo: 2026-P4-FE/2026-PIV-TPI-FE
---

# Front — La card del curso del alumno entra al modo simple

> [!info] Contexto
> Plan de implementación para Benja. Todavía no tiene tarea en Taiga.

## Worktree
- **Carpeta:** `~/dev/TPI_2026/Frontend/2026-PIV-TPI-FE-student-card-click`
- **Rama:** `feature/student-card-click-simple-mode`, desde `origin/develop` en `bfc040971` (2026-10-20).
- **Antes de empezar:** `npm ci` (la worktree no tiene `node_modules`). Tests con `NODE_OPTIONS=--no-experimental-webstorage` (Node 25).
- El archivo `PLAN-student-card-click.md` de la raíz del worktree es una copia de este plan: no commitearlo.

## Objetivo
En "Mis Cursos", como alumno, un click en cualquier parte de la card del curso entra al
modo simple (`/courses/:id`, lo mismo que hoy hace el botón "Entrar/Continuar").
Excepciones: el botón **Modo Aventura** y el link **Ranking** mantienen su comportamiento,
y en general cualquier control interactivo propio de la card.

## Contexto
- Componente: `src/app/features/courses/ui/student-course-card/` (`.html`, `.ts`, `.css`, `.spec.ts`).
- Dos layouts en el mismo template: `view() === 'list'` (`article.row-card`) y grilla (`article.grid-card`).
- Outputs: `opened` (modo simple), `openRoadmap` (aventura), `chatOpened`.
- `opened` → `student-courses.component.ts` → `course-list-page.component.ts` `openStudentCourse()` →
  `router.navigate(['/courses', id])`. No hay que tocar nada fuera de la card.
- Controles dentro de la card que **no** deben navegar:
  - Modo Aventura (`generic-button.action-roadmap`) y Ranking (`a[genericButton]`).
  - Botón Entrar: ya emite `opened`; si el click burbujea, emitiría dos veces.
  - `app-student-course-hud`: link "Ver mochila" (ya hace `stopPropagation()`).
  - `app-external-groups-panel`: botón "Guía", links de Telegram/Discord, drawer de guía y
    confirm modal. Se renderizan dentro de la card, así que sus clicks burbujean al `article`.

## Implementación
1. **`student-course-card.component.ts`**: un handler.
   ```ts
   /** The whole card enters the simple mode, except clicks on its own controls. */
   protected onCardClick(event: MouseEvent): void {
     const target = event.target as Element | null;
     if (target?.closest('a, button, input, select, textarea, [role="dialog"], app-external-groups-panel')) return;
     this.opened.emit(this.course().id);
   }
   ```
   - `closest('button')` cubre `generic-button` (renderiza un `<button>` nativo): Aventura y Entrar quedan afuera sin doble emisión.
   - Se excluye `app-external-groups-panel` entero: tiene controles propios, drawer y modal.
   - Opcional: no navegar si el usuario está seleccionando texto (`window.getSelection()?.toString()`). Solo si molesta en la prueba manual.
2. **`student-course-card.component.html`**: `(click)="onCardClick($event)"` en los dos `<article>` (lista y grilla).
   - Sin `role="button"` ni `tabindex` en el `article`: tiene controles anidados (interactivo dentro de interactivo).
     Por teclado se sigue entrando con "Entrar", que ya tiene `ariaLabel`. El click en la card es un atajo de mouse/touch.
3. **`student-course-card.component.css`**: `.tile-card { cursor: pointer; }` (el hover ya existe).
4. **Spec `student-course-card.component.spec.ts`**, para `view` `'cards'` y `'list'`:
   - Click en título / descripción / período → `opened` emite el `course.id` una vez.
   - Click en Modo Aventura → emite `openRoadmap`, no `opened`.
   - Click en Ranking → no `opened`.
   - Click en Entrar → `opened` exactamente una vez.
   - Click dentro de `app-external-groups-panel` → no `opened`.

## Verificación
- `NODE_OPTIONS=--no-experimental-webstorage npm run test` (card, `student-courses` y `course-list-page`,
  que clickean `generic-button[variant="primary"]` y `gold`). Antes, `npm install` en el worktree.
- `npm run lint:all`.
- Manual (`npm run dev`), alumno en "Mis Cursos", grilla y lista: zona libre → modo simple;
  Aventura → `/roadmap/play/:id`; Ranking → `/ranking/:id`; Ver mochila → inventario;
  Guía de grupos → abre el drawer sin navegar.
- Leer `AGENTS.md`, `docs/design/SKILL.md` y `docs/skills/accessibility/SKILL.md` del repo FE (lo pide el hook para cambios de UI).

## Fuera de alcance
- Card del profesor (`cohort-card`): no se toca.
