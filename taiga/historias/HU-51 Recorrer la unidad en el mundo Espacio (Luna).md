---
tags: [tpi, g10, taiga, hu]
codigo: HU-51
ref: 7342
estado: "Done"
responsable: "Ludmila Mailen Cejas"
epica: "[G10] — Mundos (biomas) del roadmap"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7342
---

# HU-51: Recorrer la unidad en el mundo Espacio (Luna)

> [!info] Generado desde Taiga (2026-10-14 18:48). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7342) · Estado: **Done** · Responsable: **Ludmila Mailen Cejas** · Sprint: **G10 - Sprint 2**

[G10] — HU-51 — Recorrer la unidad en el mundo Espacio (Luna)
-------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ESTUDIANTE
*   **Quiero**: recorrer una unidad en el mundo Espacio, donde personajes me entregan el material y me llevan a cada desafío
*   **Para**: que estudiar se sienta como una aventura y sepa siempre qué me falta para terminar la unidad

* * *

Notas / Observaciones
---------------------

*   [x] Reglas de negocio: solo en el bioma Espacio. No hay cofres: cada desafío tiene un custodio que entrega los anexos de ese desafío y lleva al desafío por el flujo existente del Motor. El desafío teórico *es* el personaje (sin torre); el práctico mantiene su torre con el custodio al lado. La Biblioteca con su bibliotecario está en todos los biomas para releer anexos. Es visual: no toca gate, progreso ni XP.
*   [x] Validaciones: el anexo entregado muestra el detalle de HU-05 (si el nodo está bloqueado no se puede leer); "Ir al desafío" solo aparece con los anexos del desafío leídos.
*   [x] Datos obligatorios: ninguno nuevo; usa el bioma de la sección (HU-50) y los nodos del roadmap.
*   [x] Performance (tiempos, volumen, límites): +4,1 MB de modelos en el repo (Ultimate Space Kit, CC0); descarga real de una unidad ~5,7 MB vs ~6,0 MB en pradera. Los efectos de ambiente se apagan con la tecla X.
*   [x] Seguridad (roles, permisos, datos sensibles): abrir un intento real requiere rol STUDENT (lo valida el Motor); sin datos sensibles.
*   [x] Accesibilidad (WCAG/teclado/lectores): la charla y el aviso "Pulsa E" tienen botón clickeable equivalente; Esc cierra la charla; el texto de la charla es legible por lectores (`aria-live`).
*   [x] Otros: edificios por bioma (`BIOME_BUILDINGS`, torre de radar en Espacio; el resto sigue medieval) y ningún otro elemento de los mapas se mueve. Guía para replicarlo en otros biomas: `docs/roadmap/npc-world-biomes.md`.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [x] **CA1**: En Espacio no hay cofres: cada anexo lo entrega el custodio de su desafío y al leerlo se vuelve a la charla.
*   [x] **CA2**: La charla muestra cuánto falta para completar la unidad y, con los anexos leídos, lleva al desafío.
*   [x] **CA3**: Una torre práctica con anexos sin leer indica con quién hablar y señala al personaje.
*   [x] **Extras (opcional)**: el bibliotecario permite volver a ver los anexos leídos en todos los biomas; los efectos se apagan con X.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Recorrido en el mundo Espacio

**Escenario 1**  

*   **Dado**: un desafío teórico con un anexo sin leer
*   **Cuando**: el alumno habla con su custodio y elige el anexo
*   **Entonces**: se abre el anexo y, al terminar, el custodio dice "¡Listo!" y ofrece el desafío

**Escenario 2**  

*   **Dado**: todos los anexos del desafío leídos
*   **Cuando**: el alumno elige "Ir al desafío"
*   **Entonces**: se abre el intento del desafío teórico en el Motor

**Escenario 3**  

*   **Dado**: una torre práctica con anexos sin leer
*   **Cuando**: el alumno se acerca
*   **Entonces**: la torre indica con qué personaje hablar y lo señala con una flecha

* * *

Prototipo
---------

*   **Capturas**: en el PR 2026-P4-FE/2026-PIV-TPI-FE#303 (vista de Luna, charla con un custodio, torre de radar, Biblioteca).
*   **URL Figma**: no aplica.
*   **Storybook**: no aplica.
*   **Mock API / Swagger**: sin endpoints nuevos; usa [GET /api/roadmap/courses/{courseId}], [GET /api/roadmap/courses/{courseId}/nodes/{nodeId}], [POST /api/roadmap/.../nodes/{nodeId}/read] y el inicio de intento del Motor.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Should

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: front Angular; tpi-roadmap (lectura de contenido y progreso); Motor de Desafíos (abrir intento).
*   Módulos afectados: front `world-gen`, `world-3d.service`, `npc-controller`, `npc-dialogue`, `hex-world-page`, editor del profesor.
*   Otros equipos / aprobaciones: ninguno.
*   Impacto en datos / migraciones: ninguno.
*   Riesgos y mitigación (opcional): peso de los assets → se comparten 5 modelos entre 10 personajes (tintes y tamaños). Depende de HU-50. Implementación: 2026-P4-FE/2026-PIV-TPI-FE#303.

## Tareas

- [x] #7355 T-51.1 Bioma Espacio: terreno, decoración y ambiente · Closed · Ludmila Mailen Cejas
- [x] #7356 T-51.2 Custodios por desafío · Closed · Ludmila Mailen Cejas
- [x] #7357 T-51.3 Anexos entregados por personajes · Closed · Ludmila Mailen Cejas
- [x] #7358 T-51.4 Biblioteca y bibliotecario en todos los biomas · Closed · Ludmila Mailen Cejas
- [x] #7359 T-51.5 Edificios por bioma · Closed · Ludmila Mailen Cejas
- [x] #7360 T-51.6 Tests · Closed · Ludmila Mailen Cejas
- [x] #7361 T-51.7 Guía para replicarlo en otros biomas · Closed · Ludmila Mailen Cejas
