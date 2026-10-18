---
tags: [tpi, g10, guia, pr, revision]
fecha: 2026-10-18
---

# Criterios para aprobar PRs (front y back)

Checklist que usamos para revisar una PR antes de aprobarla, a mano o con IA. El veredicto es siempre uno de tres: **✅ Aprobar**, **💬 Aprobar con comentarios** o **❌ Pedir cambios**.

> [!info] Cómo se clasifica
> - **🔴 Bloqueante**: cualquiera alcanza para pedir cambios.
> - **🟡 Importante**: aprobar con comentarios; si son varios, pedir cambios.
> - **⚪ Nit**: no bloquea.
>
> Cada hallazgo lleva `archivo:línea`, qué está mal, qué regla o DEC rompe y cómo arreglarlo. Lo que no se puede verificar desde el diff va en "No verificado". No se piden refactors fuera del alcance de la PR.

## Back (tpi-roadmap)

Fuentes: [[arquitectura/estructura-codigo|estructura del código]], `AGENTS.md` del repo y las DEC.

### 🔴 Bloqueantes
1. **CI** en verde: `mvn verify` (tests, Checkstyle y PMD de la cátedra). `.code_quality/` no se toca.
2. **Rama**: a `develop` desde `feature/*` o `fix/*`; a `main` desde `release/*` o `hotfix/*`.
3. **Capas**: un controller nunca usa un repository ni devuelve una entity. Los DTO se arman con `from(model)`, nunca desde una entity. `common/` no depende de ninguna capa.
4. **Flyway**: migración nueva con la versión siguiente; nunca editar una `V*` ya mergeada. Si el SQL depende del motor, va la variante en `db/migration-vendor/{h2,postgresql}`.
5. **Contrato**: snake_case en HTTP y Kafka ([[decisiones/DEC-001-wire-kafka-v8-snake-case|DEC-001]]). Si cambia un endpoint o evento, se actualizan OpenAPI/AsyncAPI y `contratos/`.
6. **Eventos salientes** solo por outbox ([[decisiones/DEC-002-outbox-transaccional-eventos-salientes|DEC-002]]).
7. **Consumidores idempotentes** por `event_id`; Roadmap no calcula XP ([[decisiones/DEC-013-roadmap-no-calcula-xp-ledger-idempotente|DEC-013]]).
8. **Seguridad**: identidad del Gateway fail-closed ([[decisiones/DEC-003-gate-pull-identidad-de-servicio-fail-closed|DEC-003]]), chequeo de rol en endpoints nuevos, sin secretos ni URLs fijas, `.env.example` al día.
9. **Flags** nuevos apagados por defecto ([[decisiones/DEC-004-flags-apagados-por-defecto|DEC-004]]).
10. **Baja lógica**, sin borrar progreso ([[decisiones/DEC-005-baja-logica-sin-borrar-progreso|DEC-005]]).
11. **Cumple la HU**: todos los criterios de aceptación y nada fuera de alcance.

### 🟡 Importantes
- Errores con código en `messages.properties` y status correcto ([[decisiones/DEC-015-4xx-de-accounting-no-es-indisponibilidad|DEC-015]], [[decisiones/DEC-020-gate-origen-no-disponible-en-vez-de-503|DEC-020]]); nada de 500 genéricos ni `catch` que traga.
- Clientes salientes (`ClientMode` http/stub) con timeout, manejo de error y stub actualizado.
- Tests de integración del cambio: camino feliz y al menos un error. Solo los pertinentes.
- Sin N+1, colecciones paginadas, índices si se agregan filtros, `@Transactional` si hay más de una escritura.
- Respeta las DEC de dominio que toque (insignias, anonimato del ranking, comisiones, grafo).

### ⚪ Nits
- Nombres, logs sin datos personales, código muerto, Javadoc de clases nuevas.

## Front (2026-PIV-TPI-FE)

Fuente de verdad: el `AGENTS.md` del repo (sección FORBIDDEN). Si cambia, manda sobre esta nota.

### 🔴 Bloqueantes
1. **CI** en verde (lint, build, tests). No toca archivos protegidos (`package.json`, `angular.json`, `tsconfig*`, `.github/**`…) salvo que el autor sea CODEOWNER.
2. **Rama**: igual que en el back.
3. **HTTP**: sin URLs ni puertos fijos; todo por `environment.apiUrl` y `HttpGenericService`. Consultas con `httpResource`, mutaciones con `post/put/patch/delete`. Respuestas tipadas con `ApiResponse<T>` o `PaginatedResponse<T>`.
4. **Angular moderno**: sin `NgModule`, sin `*ngIf/*ngFor`, sin `@Input/@Output/@ViewChild`, sin inyección por constructor (`inject()`), signals `readonly`, sin `BehaviorSubject` para estado de UI, sin `zone.js`.
5. **UI-KIT**: usa los `Generic*` de `@2026-p4-fe/ui`; si falta un componente, issue en el UI-KIT, no réplica local.
6. **Estilos**: solo tokens (`--tpi-*`, `--fs-*`, `--font-*`); sin colores, tamaños ni fuentes literales; sin Tailwind ni clases utilitarias globales.
7. **i18n**: sin importar `@jsverse/transloco` fuera de `core/i18n`; cada clave nueva en `es.json` y `en.json`.
8. **Estado y seguridad**: nada de tokens, roles ni estado de negocio en `localStorage` (la fuente de verdad es el back). Lo que valida el back no se esquiva en el front ([[decisiones/DEC-007-anonimato-ranking-en-servidor|DEC-007]]).
9. **Accesibilidad** (WCAG 2.2 AA): nada de `<div (click)>`, íconos sin `aria-label` traducido, `tabindex > 0`, `outline: none` sin `:focus-visible`, color como única señal.
10. **Sin `console.log`**: se usa `LoggerService`.
11. **Cumple la HU.**

### 🟡 Importantes
- Por feature: `pages/` (smart), `ui/` (dumb, `input/output`, `OnPush`), `data-access/` (SignalStore, service, models).
- Ruteo: una sola entrada por módulo en `app.routes.ts`, guards dentro del `*.routes.ts` del feature, sin repetir `authGuard`.
- Estados de carga, vacío y error manejados; errores del back visibles.
- Modelos alineados al contrato, en camelCase: el interceptor `case-converter` traduce el snake_case, no se mapea a mano. Si el endpoint no está mergeado en el back, se marca.
- TypeScript sin `any`; código y comentarios en inglés.
- Spec del componente o servicio que cambió.
- Si hay cambio visual, la PR trae capturas o video.

### ⚪ Nits
- Orden de imports, imports sin uso, Conventional Commits.

## Revisión con IA

Benjamín tiene estos criterios como comandos de Claude Code, **locales y sin commitear** (no están en este cerebro ni en los repos compartidos):

| Comando | Dónde vive | Uso |
|---|---|---|
| `/review-pr-back` | `tpi-roadmap/.claude/commands/` (`.claude/` está en el `.gitignore`) | `/review-pr-back 266` |
| `/review-pr-front` | `2026-PIV-TPI-FE/.claude/commands/`, excluido en `.git/info/exclude` | `/review-pr-front 729` |

- Leen el diff, los checks y la descripción con `gh`, y cruzan con las DEC, los contratos y la HU de este cerebro.
- Con `--comment` publican la revisión en la PR. **Nunca aprueban**: el approve lo da una persona.
- Solo aparecen si Claude se abre en ese repo. Los worktrees no los traen porque el archivo no está trackeado; hay que agregarles un symlink al del checkout principal.

## Historial
- 2026-10-18: creado.
