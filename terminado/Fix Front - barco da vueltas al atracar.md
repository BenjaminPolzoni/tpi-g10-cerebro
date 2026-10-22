# Fix Front — el barco da vueltas al atracar en una isla

- **Rama:** `fix/roadmap-barco-atraque` (desde `origin/develop` `18227d713`)
- **Worktree:** `Frontend/2026-PIV-TPI-FE-fix-barco-atraque`
- **HU/Tarea Taiga:** sin asignar
- **Archivo único:** `src/app/features/roadmap/engine/archipelago-3d.service.ts`

## Problema

Al elegir una isla en el archipiélago, el autopiloto (`sailYDock`) arranca girando contra la costa de la isla de origen, zigzaguea y a veces tarda hasta 12 s (`AUTOPILOT_MAX_SECONDS`) en atracar, cuando lo fuerza con un salto de posición.

## Causa

1. **La salida apunta a la isla de origen.** `startExit` se proyecta 4.2 u. hacia adelante con `boatHeading`. Atracado, el barco tiene `dockHeading = dockAngle + π` (proa al muelle), así que el primer tramo de la curva entra en la isla: los colliders (`resolveBoatCollisions`) lo empujan, se desliza por la costa y da media vuelta.
2. **El watchdog mide contra el muelle final, no contra el waypoint.** `autoPilotBestDist` / `autoPilotStall` usan `remainingToFinal`. En el tramo de salida el barco se aleja (o va de costado) del destino → cada 1.2 s cree que está trabado y salta un waypoint → el rumbo cambia de golpe (zigzag). Con 33 puntos de curva, se llega al tope de 12 s.

> El waypoint del canal (`x * 0.18`) está bien: las islas van en dos columnas `x ∈ [-42,-10] ∪ [10,42]` y los muelles miran al canal central.

## Cambios

### 1. Salir hacia mar abierto cuando está atracado — `sailYDock` (~l. 4281)

Reemplazar el cálculo de `startExit`:

```ts
// Docked, the bow faces the pier (dockHeading points into the island): leave toward open sea.
const origin = this.islands.find(
  isl => Math.hypot(isl.dockX - start.x, isl.dockZ - start.z) < 3.8,
);
const exitHeading = origin ? origin.dockHeading - Math.PI : this.boatHeading;

// Exit vector toward open sea moving away from the origin pier
const startExit = new THREE.Vector3(
  start.x + Math.sin(exitHeading) * 4.2,
  0.44,
  start.z + Math.cos(exitHeading) * 4.2,
);
```

- Se usa la distancia al muelle (mismo umbral `3.8` que el auto-dock manual) y no `currentDockedId`, porque `currentDockedId` sigue seteado después de navegar a mano lejos de la isla.
- No usar `this.isSailing`: ya se pone en `true` unas líneas antes.

### 2. Watchdog contra el waypoint actual — `updateBoatNavigation` (~l. 3594)

```ts
this.autoPilotElapsed += dt;
if (distReal < this.autoPilotBestDist - 0.5) {
  this.autoPilotBestDist = distReal;
  this.autoPilotStall = 0;
} else {
  this.autoPilotStall += dt;
}

if (remainingToFinal < 2.5 || this.autoPilotElapsed > AUTOPILOT_MAX_SECONDS) {
  this.finishAutoPilot();
} else if (distReal < 2.5 || this.autoPilotStall > AUTOPILOT_STALL_SECONDS) {
  this.autoPilotStall = 0;
  this.autoPilotBestDist = Infinity; // new waypoint, new best distance
  this.autoPilotIndex++;
  if (this.autoPilotIndex >= this.autoPilotPath.length) this.finishAutoPilot();
}
```

- Actualizar el comentario del campo (~l. 262): "closest the boat got to the **current waypoint**".
- `remainingToFinal` se sigue usando para la velocidad y para terminar el viaje; solo cambia el criterio de "trabado".

## Fuera de alcance

- Frenar en giros cerrados (`desiredSpeed * max(0.35, cos(diff))`): el barco arranca a velocidad 0 tras atracar y gira rápido; agregarlo solo si después del fix siguen viéndose arcos abiertos.
- Pathfinding con conciencia de colisiones: la curva actual alcanza con la salida corregida.

## Verificación

- No hay spec de `archipelago-3d.service` (WebGL); verificación manual en `/roadmap` (archipiélago):
  - Atracado en una isla de la izquierda → elegir otra de la misma columna, de la columna opuesta y la más lejana: el barco sale hacia el canal sin rozar la costa y atraca sin salto.
  - Navegar a mano (click en el mar / teclado) lejos de un muelle → elegir isla: sale hacia adelante como antes.
  - Elegir una isla mientras ya navega hacia otra: sigue sin colgarse "Atracando en el puerto...".
- `npm run lint` sobre el archivo tocado.
