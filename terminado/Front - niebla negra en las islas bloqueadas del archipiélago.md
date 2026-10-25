---
tags:
  - tpi
  - g10
  - sprint-3
  - plan
  - front
  - mapa
fecha: 2026-10-22
autor: Benja
estado: terminado
repo: 2026-PIV-TPI-FE
taiga: sin asignar
orden: 1 de 4 (no depende de nadie)
---

# Front — Islas bloqueadas en negro (niebla) en la vista del barquito

> [!info] Contexto
> Auditoría del 2026-10-22. Parte de un pedido del equipo: en el mapa del archipiélago las islas que el alumno todavía no alcanzó deben verse **en negro / bajo niebla**. Hoy solo se deshabilita el botón «Entrar».

## 1. Estado actual (verificado en código)

| Qué | Dónde | Hallazgo |
|---|---|---|
| Bloqueo por isla | `pages/worlds-page/worlds-page.component.ts:660-677` (`isLocked`, `lockMessage`), regla en `domain/unlock-rules.ts:349` (`sectionLockState`) | Ya decide qué isla está bloqueada |
| Envío al motor | `worlds-page...:728-738` (`sections3d()`) manda `locked` | OK |
| Motor 3D | `engine/archipelago-3d.service.ts:25,40,1301` | `locked` se copia a la isla y **nunca se usa visualmente** |
| Niebla actual | `setupPerimeterFog` (`:1116`), `scene.fog = FogExp2` (`:399`) | Decorativa, de borde y global; no es por isla |
| Dentro de la unidad | `engine/world-3d.service.ts:2800-2825` (`fogWall`) | Ya tiene niebla real; no se toca |
| Docente | `hex-world-page...:1212` ve todo | Mantener: el docente ve el mapa completo |

## 2. Decisión

Reemplazar materiales por uno oscuro en las islas `locked`, guardando los originales para restaurar. Es lo más barato y no requiere assets. Se descarta una `fogWall` por isla (costo en sprites y colisión sin necesidad).

## 3. Pasos

1. En `archipelago-3d.service.ts`, al construir cada isla (`buildHexClusterIslands`, ~`:1285-1303`), si `locked`: `group.traverse` y, por cada `Mesh`, guardar `userData.origMaterial` y asignar un `MeshBasicMaterial` casi negro (`0x0b0d12`). Ocultar etiquetas y decoración de la isla bloqueada.
2. Al cambiar `locked` (desbloqueo): `updateSections` ya reconstruye las islas; confirmar que se restauran los materiales y que se liberan los materiales negros (`dispose`) para no perder memoria.
3. Verificar que `progressKey` (`worlds-page:741`) incluye `locked` (hace `JSON.stringify` de las secciones, debería).
4. Docente: no pasar `locked` (o pasarlo en `false`) para que vea todo, igual que `hex-world-page:1212`.
5. Mantener el card de la isla con el mensaje de bloqueo (`island-dock-card`), de modo que el negro no deje al alumno sin explicación.

## 4. Verificación

- Alumno con una unidad sin prerrequisitos cumplidos: la isla se ve negra, el card dice por qué.
- Completar el prerrequisito: la isla recupera color sin recargar.
- Docente: todas las islas con color.
- Sin warnings de materiales sin liberar en consola tras varios desbloqueos.

## 5. Preguntas abiertas

- [ ] ¿Negro total o silueta oscura con borde sutil? (propongo negro con leve emisión del contorno, definir con UX).
- [ ] ¿La isla bloqueada sigue siendo seleccionable para ver el card? (propongo que sí).
