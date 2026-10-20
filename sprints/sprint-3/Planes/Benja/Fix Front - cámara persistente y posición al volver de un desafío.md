# Fix Front — cámara persistente y posición al volver de un desafío

- **Rama:** `fix/roadmap-camara-y-posicion-retorno` (desde `origin/develop` `cd0d6d404`)
- **Worktree:** `Frontend/2026-PIV-TPI-FE-fix-camara-posicion`
- **HU/Tarea Taiga:** sin asignar

## Problema

1. La cámara (1 = primera, 2 = tercera, 3 = libre) vuelve a **libre** cada vez que se entra a una sección del mundo. `CameraController` se recrea en cada `world3d.init` con `view = 'free'` y el signal `view` de `hex-world-page` también arranca en `'free'`.
2. Al salir de un desafío real (Motor), `attempt-launch-page` / `attempt-page` navegan a `/roadmap/play/:courseId/:sectionId`; el mundo se reconstruye y el personaje aparece en `layout.spawn`, no en la torre donde estaba.

## Cambios

### 1. Cámara persistente (todo el roadmap)
`pages/hex-world-page/hex-world-page.component.ts`
- `view` arranca desde `localStorage['roadmap.cameraView']` (fallback `'free'`; try/catch).
- `setView` / `toggleView` guardan la vista activa.
- En el `.then()` de `world3d.init(...)`: `this.world3d.setView(this.view())` para que el motor recién creado tome la vista guardada (también oculta el cuerpo en primera).

### 2. Posición al volver de un desafío (solo ese caso)
`engine/world-3d.service.ts`
- `playerPose(): { x, z, rotY } | null` y `placePlayer(pose)` sobre `charController.char`.

`hex-world-page.component.ts`
- En `openChallenge`, rama de desafío real, antes de `challengeAttempts.open(...)`: guardar en `sessionStorage['roadmap.challengeReturn']` `{ courseId, sectionId, x, z, rotY }`.
- En `initWorld`, tras `world3d.init`: leer y **borrar siempre** la entrada; si la navegación trae `state.fromChallenge` y coincide `courseId|sectionId`, `placePlayer(pose)`.

`challenges/practical-challenges/pages/attempt-launch-page` (l. ~211) y `challenges/theoretical-challenges/pages/attempt-page` (l. ~1077)
- Al volver al mundo, pasar `state: { fromChallenge: true }` en la navegación.

**Por qué el flag de navegación:** `challengeAttempts.open()` es `void` y puede fallar con un toast sin salir de la página; sin el flag, una entrada vieja restauraría la posición al reentrar por otro camino. Con el flag, la posición solo se restaura al volver desde el desafío.

## Fuera de alcance
- Persistir la posición en otros casos (entrar desde el archipiélago, recargar) → sigue el spawn normal.
- Guardar yaw/distancia de la cámara libre.

## Verificación
- Spec de `hex-world-page`: la vista guardada se aplica al montar; `setView` persiste.
- Manual: elegir 1/2/3 → salir al archipiélago → entrar a otra sección → misma cámara. Entrar a un desafío → volver → personaje en la torre. Entrar a la sección desde el archipiélago → spawn normal.
