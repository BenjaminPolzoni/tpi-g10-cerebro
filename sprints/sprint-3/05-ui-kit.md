---
tags: [tpi, g10, sprint-3, frontend, ui-kit]
fecha: 2026-10-14
estado: borrador
---

# 05 — Consistencia visual: adopción de la UI-KIT

> [!info] Alcance de la auditoría
> Auditoría de solo lectura del 2026-10-14:
> - Kit `2026-P4-FE/2026-PIV-TPI-UI-KIT` en `origin/main` (27eb1a8, **v0.8.0**).
> - Front `2026-P4-FE/2026-PIV-TPI-FE` en `origin/develop` (8a770d50).
>
> Los conteos salen de búsquedas por regex sobre templates y CSS, así que son aproximados.

## Resumen

- El front **ya consume el kit**: 407 imports de `@2026-p4-fe/ui`. No usa otras librerías de UI (ni Material, ni PrimeNG, ni Tailwind). Solo usa `@angular/cdk` para a11y y drag-drop.
- **Está una versión atrás**: `^0.7.1` contra la 0.8.0 del kit. La rama `feature/ui-lib-0-8-0` del front sube la versión, pero **no está mergeada**.
- Se usan **unos 50 de los ~87 componentes** del kit. Hay 36 sin usar, varios de gamificación que el roadmap reimplementa a mano.
- **Roadmap (G10)**: adopción **media en componentes** y **baja en tokens**:
  - 316 líneas con colores hardcodeados.
  - 114 `font-size` literales.
  - Solo 2 usos de `--space-*` / `--fs-*`.
  - Un "puente" de tokens estilo daisyUI (`--color-*`) en `roadmap-theme.component.css`.
- Hay **9 TODOs del front que esperan cambios del kit**, y **todos están cerrados en el kit**. Se destraban con el bump a 0.8.0.
- `AGENTS.md` y `docs/design/SKILL.md` del front ya obligan a usar solo componentes del kit. Falta aplicarlo y controlarlo en CI.

## Cómo se consume

| Aspecto | Estado |
|---|---|
| Paquete | `@2026-p4-fe/ui`, desde npm privado en GitHub Packages (`.npmrc`). El token se configura con `npm run auth` |
| Versión | `^0.7.1` en develop. **Hay que subirla a 0.8.0** (rama `feature/ui-lib-0-8-0`) |
| Estilos | `src/styles.css` importa `theme.css`, y además `theme/tokens.css` (redundante, es un alias histórico) |
| Overrides propios | `--border-control`, `--link-color`, `--tpi-surface-alt`, `--tpi-shadow-modal`, `--tpi-radius-*`. Son candidatos a subir al kit (contrastes que el kit no cumple) |
| Docs del kit | No hay Storybook. Hay una app `projects/showcase` y un `.md` por componente. **El README del kit está desactualizado**: habla de `Tpi*Component` y lo real es `Generic*` con selectores `generic-*` |
| Tokens del kit | `--bg-*`, `--text-*`, `--accent-*`, `--font-*`, `--fs-*`, `--radius-*`, `--shadow-*`, `--focus-*`, `--badge-*` y `--space-1..7` (nuevo en 0.8.0). Más servicios de tema y apariencia (arcade/sober) |

## Componentes del kit que el front no usa

Por categoría:

- **Formularios**:
  - `combobox`
  - `date-time-field`
  - `time-field`
  - `otp-input`
  - `star-rating`
- **Overlays**:
  - `popover`
  - `file-modal`
  - `course-modal`
- **Layout**:
  - `content-card`
  - `data-list`
  - `dashboard`
  - `footer`
  - **`sidebar`** (TODO #36)
  - `account-menu`
  - `lesson-header`
  - `option-cards`
  - `type-card`
  - `math-block`
  - `survey`
  - `rubric-panel`
  - **`course-outline`**
  - `cell-name`
- **Gamificación (relevantes para G10)**:
  - **`xp-bar`**
  - **`coin-counter`**
  - **`coin-delta`**
  - **`wallet`**
  - **`streak-flame`**
  - **`insignia-icon`**
  - **`item-tile`**
  - **`item-slot`**
- **Dominio**:
  - `activity-kind-badge`
  - `activity-status-badge`
  - `course-status-badge`
  - `course-meta-badges`
  - `grade-badge`

## Adopción por feature

| Feature | Nivel | Controles crudos (btn / input / select / textarea / table / dialog) | Colores hardcodeados | Notas |
|---|---|---|---|---|
| core | Medio | 7 / 0 / 0 / 0 / 0 / 1 | 19 | Sidebar y topbar propios (kit #36/#33), `row-actions-menu` (el kit tiene `actionsMode='menu'`) |
| accounting | Alto | 3 / 0 / 0 / 0 / 0 / 0 | 0 | |
| admin | Alto | 15 / 20 / 3 / 2 / 12 / 3 | 196 | 5 modales sin `GenericModal`, `searchable-select` en vez de `combobox`, `timeseries-chart` en vez de `chart` |
| auth | Alto | 10 / 1 / 0 / 0 / 0 / 0 | 62 | |
| challenges | Medio | 42 / 7 / 5 / 2 / 0 / 4 | 468 | `toggle-switch` en vez de `switch`, `attempt-stepper` en vez de `stepper` |
| chat | Alto | 1 / 1 / 0 / 1 / 0 / 0 | 109 | Banners en vez de `callout` |
| courses | Medio | 40 / 24 / 1 / 0 / 2 / 0 | 261 | Cards y tablas propias, 172 `font-size` literales |
| marketplace | Alto | 1 / 1 / 0 / 0 / 0 / 0 | 2 | |
| notifications, onboarding, profile, ai-tutor, surveys, dashboard | Alto | ≈ bajos | ≤ 34 | `profile` usa `::ng-deep` para centrar tabs y pagination (se resuelve con 0.8.0) |
| **ranking** (G10) | **Bajo** | 5 / 0 / 0 / 0 / **3** / 0 | 63 | 3 `<table>` crudas, chips `rk-chip` y `rk-status` hechos a mano, solo 3 de 7 componentes con el kit |
| **roadmap** (G10) | **Medio / Bajo en tokens** | 16 / 5 / 9 / 1 / 0 / 2 | 316 | Detalle abajo |

## Roadmap (G10): qué reemplazar

Rutas relativas a `src/app/features/roadmap/`.

### Transversal
- **Borrar el puente `--color-*`** de `ui/roadmap-theme/roadmap-theme.component.css` y usar los tokens reales del kit.
- **Parche `.rm-dark`**: repinta `--accent-primary` y usa `--rm-app-accent`. Hay que pedir al kit una variante dark por sección.
- **Reemplazar emojis de UI** (19 archivos) por `generic-icon` (`map`, `swords`, `trophy`, `heart`, `fire`, `bag`...).
- **Espaciado y tipografía**: pasar `rem/px` literales a `--space-*` y `--fs-*`.

### Por pantalla o componente

| Archivo | Hoy | Reemplazar por |
|---|---|---|
| `pages/course-editor-page` (**vista tipo Moodle**) | `<h1>` con emoji, `<a class="manage-units">` crudo | `generic-title`; `genericButton variant=ghost` sobre `<a>` |
| `embeds/section-nodes/roadmap-section-nodes` (918 líneas) | 2 `<button>` crudos (L192, L201) | `genericButton`/`genericIconButton`. Lista de nodos con **`generic-course-outline`** o `generic-disclosure` |
| `pages/course-map-page` (**vista de nodos**, 921 líneas) | SVG a mano, hex en `SECTION_COLOR`/`NODE_COLOR`, 3 `<button>` crudos | Botones del kit, colores a `--accent-*`/`--badge-*`. **El canvas de grafo no existe en el kit** (ver huecos) |
| `pages/hex-world-page` (HUD 3D) | `.hud-linkbtn` crudos, overlays propios, 28 colores | `genericButton variant=ghost`, paneles con `generic-modal`/`generic-drawer`, tokens `--bg-*`/`--shadow-*` |
| `pages/worlds-page` | Hex de fondo y rgb translúcidos | `--bg-app`, `--bg-surface`, `--text-*` |
| `pages/badges-catalog-page` | 2 `<input>`, 3 `<select>`, 1 `<button>`, `::ng-deep` | `generic-search-field`/`generic-input`, `generic-select`, `genericButton`. Insignias con `generic-badge-showcase` o `generic-insignia-icon` |
| `ui/entity-editor-dialog` | Usa `generic-drawer` pero adentro tiene 3 `<input>`, 4 `<select>`, `<textarea>` y `<button>` crudos | `generic-input`, `generic-select`, `generic-textarea`, `genericButton` |
| `ui/avatar-panel` | 3 `<button>`, 2 `<select>` | `genericButton`, `generic-select` |
| `ui/lives`, `ui/streak` | `PixelIconComponent` propio | `generic-icon heart/heart-empty` o `generic-progress [hearts]`; `generic-streak-flame` |
| `ui/level-hud` | `level-badge` + `progress` | `generic-xp-bar` |
| `ui/inventory-item-card` | Tarjeta propia | `generic-item-tile` / `generic-item-slot` |
| `ui/feedback-toast` | Toast propio + `<button>` crudo | `GenericToast` + `ToastService` (en `core` ya delega al kit) |
| `ui/npc-dialogue`, `ui/shop-interior` | `role="dialog"` propio, colores | `generic-modal` / `generic-drawer` |
| `ui/island-card` (2) | 25 líneas de color | `generic-card`/`generic-content-card` + tokens |
| `ui/role-switch` | `generic-button` con `aria-pressed` | `generic-segmented` / `generic-view-toggle` |
| `ui/unit-node-list` | `generic-badge` | `generic-course-outline` / `generic-disclosure` |
| `ranking/*` (G10) | 3 `<table>` crudas, chips propios | `generic-table`, `generic-badge`; quitar el TODO #59 de `ranking-detail.component.ts:190` |
| Bien adoptados | `rules-wizard`, `node-creation-wizard`, `embeds/course-status`, `teacher-home-page` | Nada relevante |
| Fuera de alcance | `engine/**` (three.js) y `ui/avatar-sprite` (arte) | Se quedan, aislados de la UI |

## Huecos del kit: hay que aportarlos al kit, no hacerlos locales

1. **Componente de grafo (`generic-node-graph`)** con pan, zoom, selección con teclado y foco, aristas y minimapa. Es **clave para la vista de nodos del Sprint 3** ([03](03-requerimientos-profes.md)). Hay dos opciones:
   - Envolver una librería (`ngx-vflow` o `@foblex/flow` + `elkjs` para el acomodo) con los tokens del kit.
   - Construirlo sobre el SVG actual de `course-map-page`.
2. **Íconos y arte pixel**: `insignia-art` trae ~8 arts; el roadmap tiene su propio registro (`ui/badge-icons`).
3. **Panel HUD translúcido** sobre la escena 3D. Se puede cubrir con `generic-popover`, que está en la rama `feature/generic-popover` sin mergear.
4. **Tema oscuro por sección** (`data-theme` por árbol), para eliminar `.rm-dark`.
5. **Lista reordenable con drag-drop**: hoy es CDK propio en `section-reorder-list`.
6. **Contraste del tema claro**: breadcrumb (4.34:1), headers de tabla (3.86:1), bordes de controles. Los overrides del front pueden subir al kit.

## TODOs del front que se destraban con 0.8.0

| TODO | Dónde | Qué trae 0.8.0 |
|---|---|---|
| ui-kit#59 | `ranking-detail.component.ts:190` | `interactive=false` + `earnedLabel`/`lockedLabel` en `badge-showcase` |
| ui-kit#51 | `quiz-selection-card.component.html:40` | Íconos `edit`/`trash` |
| ui-kit#53 | `profile-page.component.css:26` | `align` en `GenericTabs` |
| ui-kit#63 | `parameter-history-list`, `ingestion-events-table` | Tooltip que describe al elemento enfocado |
| ui-kit#83/#84 | `timeseries-chart.component.ts` | aria en button; chart con muchas columnas |
| ui-kit#85 | `ceiling-usage.component.ts` | `valueText` en progress |
| ui-kit#36 | `core/layout/sidebar` | `GenericSidebar` (ya existía en 0.7.1, sin adoptar) |
| ui-kit#33 | `core/layout/nav-icon-sprite` | Íconos lucide. **Verificar** que cubran el sprite |
| sin número | pagination centrada (`access-history-panel`, `profile-students-panel`) | Centrada por defecto |
| sin número | `admin-audit-table` | `caption` en `GenericTable` |

## Plan priorizado

| # | Paso | Alcance | Esfuerzo |
|---|---|---|---|
| 1 | Mergear el bump a **0.8.0** (`feature/ui-lib-0-8-0`), correr `npm run verify` y los tests visuales. Revisar `--fs-*` y la pagination | Todo el front | S |
| 2 | Quitar los TODOs destrabados (#59, #53, #51, #83/#84/#85, `::ng-deep` de pagination) | Varios | S-M |
| 3 | **Roadmap**: controles de formulario crudos → kit (`entity-editor-dialog`, `badges-catalog-page`, `avatar-panel`) | G10 | S |
| 4 | **Roadmap**: botones y headings sueltos (`course-editor-page`, `section-nodes`, `course-map-page`, `hex-world-page`, `feedback-toast`) | G10 | S |
| 5 | **Roadmap**: borrar el puente `--color-*` y pasar colores, espaciado y tipografía a tokens | G10 | M |
| 6 | **Roadmap**: overlays y componentes locales → kit (`npc-dialogue`, `shop-interior`, `lives`, `streak`, `role-switch`, `inventory-item-card`, `level-hud`) | G10 | M |
| 7 | **Ranking**: `generic-table`, chips → `generic-badge` | G10 | S-M |
| 8 | Transversal: sidebar y topbar → `generic-sidebar`/`navbar`/`account-menu`; modales de admin → `generic-modal`; `toggle-switch`/`searchable-select` → `switch`/`combobox` | Otros grupos | M |
| 9 | **Aportar al kit**: componente de grafo, más arts de insignias, dark por sección, contraste del tema claro, actualizar el README del kit | UI-KIT | L |
| 10 | **CI**: regla de `stylelint` contra hex/rgb literales (excepto `engine/` y arte) + chequeo de `<button>`/`<input>`/`<select>` crudos | Todo el front | S |

> [!tip] Alcance para G10 en el Sprint 3
> Para el Sprint 3, G10 debería encarar los pasos **1, 3 a 7 y el componente de grafo del paso 9**: son la base de las HU 9 y 10 del [backlog](06-backlog-sprint-3.md). Los pasos 2, 8 y 10 conviene coordinarlos con el resto de los grupos.

> [!question] A confirmar con el equipo del kit
> - Si #33 cubre el `nav-icon-sprite`.
> - Si el avatar `2xl` (#39) alcanza para el perfil.
> - Quién es dueño del componente de grafo.
