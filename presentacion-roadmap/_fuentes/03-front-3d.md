# Vista 3D de Roadmap — fuentes para presentación

**Alcance.** Lectura estática del front Angular en `origin/develop` (HEAD `d1c5766227`), sin ejecutar la aplicación ni pruebas. Se revisaron los 60 commits recientes: `0dae62fcf2` corrige el visor de videos externos y `240d37e3bf` la estabilidad de la rueda de emotes; el resto no se presume relevante sin verificarlo. Las rutas citadas son relativas a `/Users/benjaminpolzoni/dev/TPI_2026/_presentacion-src/fe/`; las afirmaciones describen código existente, no una verificación de despliegue, datos de demo ni funcionamiento en vivo. El cerebro contiene planes; no se toma un plan como prueba de implementación.

## Tecnología y arquitectura — implementado

### Explicación de producto/técnica media

La experiencia se renderiza en tiempo real: Angular coordina pantallas y Three.js dibuja los mundos, no se trata de un video.

### Detalle técnico

- Three.js **0.186.1** (`package.json:88`), WebGL y `GLTFLoader`: Angular aloja el canvas y coordina datos, navegación y UI; `WorldsPageComponent` usa `Archipelago3dService` para el mapa marítimo y `HexWorldPageComponent` usa `World3dService` para el interior de una unidad (`src/app/features/roadmap/pages/worlds-page/worlds-page.component.ts:71`, `:986`; `src/app/features/roadmap/pages/hex-world-page/hex-world-page.component.ts:121`, `:326`; `src/app/features/roadmap/pages/hex-world-page/hex-world-page.component.html:58`). Sin WebGL el archipiélago informa la limitación (`worlds-page.component.ts:92`, `:574`).
- El motor crea escena, cámara de perspectiva, niebla, renderer y sombras (`src/app/features/roadmap/engine/archipelago-3d.service.ts:311-331`). Un ciclo con `requestAnimationFrame` actualiza movimiento y efectos, renderiza y agenda el siguiente cuadro (`archipelago-3d.service.ts:3420`, `:3650-3657`; mundo interior `world-3d.service.ts:4448`, `:4865`). No es un video precalculado.

## Del dominio al mundo — implementado

### Explicación de producto/técnica media

El curso se vuelve un archipiélago; sus unidades son islas y dentro de ellas los desafíos y materiales se convierten en objetos navegables. Las relaciones condicionan el progreso, no necesariamente cada curva del camino.

### Detalle técnico

### Archipiélago

- El curso es un archipiélago: **una isla por unidad**, con bioma propio; las zonas directas aparecen como islotes al lado de su unidad y zonas más profundas se alcanzan mediante portales (`src/app/features/roadmap/domain/world-gen/from-nodes.ts:30-61`; `src/app/features/roadmap/engine/archipelago-3d.service.ts:1304-1358`). Mar y barco son el medio de navegación, no actividades académicas.
- Las unidades se ordenan según el orden del curso, se numeran sin huecos y se representan con comienzo y meta; máximo cinco unidades principales por página marítima, con pasajes y sus zonas acompañantes (`src/app/features/roadmap/pages/worlds-page/worlds-page.component.ts:1266-1299`; `src/app/features/roadmap/domain/archipelago-navigation.ts:16-26`; `src/app/features/roadmap/engine/archipelago-3d.service.ts:2883-2896`, `:2956-2980`). El camino visual ordena la travesía: no asumir que cada segmento dibujado equivale a una arista de dependencia.
- Posicionamiento: plantillas según cantidad de islas y, luego, 16 pasadas que separan pares para dejar canales navegables, limitando coordenadas; cada isla se arma como un conjunto de hexágonos con costa y colisiones (`src/app/features/roadmap/engine/archipelago-3d.service.ts:1240-1316`). Los islotes se ubican junto a la unidad (`:1345-1358`).
- Una unidad bloqueada aparece atenuada, con candado dorado; al desbloquearse desaparecen esas marcas. Hay niebla por zonas bloqueadas y una celebración con desplazamiento de cámara, aro y cartel; con movimiento reducido se omite el viaje de cámara (`archipelago-3d.service.ts:464-469`, `:2984-2997`; `src/app/features/roadmap/domain/world-gen/fog-spots.ts:85-109`). Los portales de zonas tienen variantes abierta, bloqueada y completada (`archipelago-3d.service.ts:1345-1358`). Los datos de completado/bloqueo llegan al motor desde el progreso de la página (`worlds-page.component.ts:1266-1299`).

### Interior de la isla

- Los desafíos teóricos, prácticos y jefes/exámenes se convierten en **torres**; los contenidos se representan como **cofres/anexos**. Los límites técnicos de inicio/fin y los hitos no generan torre ni cofre; actividades no disponibles pueden ocultarse al alumno (`src/app/features/roadmap/domain/world-gen/from-nodes.ts:64-85`, `:184-225`). Una unidad solo de contenidos tiene un tramo auxiliar de contenido (`:226-236`).
- Cada cofre se agrupa con la torre alcanzable más próxima siguiendo el grafo; si no hay una, se usa la siguiente en orden o un tramo de contenido (`from-nodes.ts:188-208`). Esto es una decisión de disposición visual, no significa que el cofre herede necesariamente la regla de la torre.
- La disposición respeta prerequisitos **internos** mediante orden topológico estable; sin aristas internas o ante un ciclo se conserva el orden de la sección. Los prerequisitos externos no cambian ese orden pero sí pueden afectar el bloqueo (`from-nodes.ts:154-177`, `:248-292`). Se excluyen conexiones a límites técnicos y, para alumnos, a nodos invisibles (`:87-108`).
- El terreno se genera sobre una grilla hexagonal, con caminos y elementos según bioma; una semilla derivada de curso y unidad hace reproducible la generación (`src/app/features/roadmap/domain/world-gen/world-gen.ts:382-436`, `:536`, `:717`; modelos de camino `src/app/features/roadmap/domain/world-gen/auto-tiler.ts:1-14`, `:34`). El dibujo del camino no es una representación literal de todas las aristas del grafo.
- Los bloqueos se calculan con progreso y reglas de prerequisitos: AND exige todos, OR al menos uno y sin regla queda abierto; el código aclara que los bloqueos del backend son autoritativos (`src/app/features/roadmap/domain/world-unlock.ts:53-85`). La niebla marca torres y cofres bloqueados; cada cofre sigue su propia regla (`src/app/features/roadmap/domain/world-gen/fog-spots.ts:13-16`, `:37-59`). **No presentar la niebla como única medida de seguridad.**

## Interacción y continuidad — implementado

### Explicación de producto/técnica media

El alumno navega en barco, recorre la isla con un personaje y puede volver a su ubicación después de entrar a un desafío.

### Detalle técnico

- En el mar se maneja el barco con WASD/flechas o apuntando con el mouse; elegir una isla puede activar navegación automática a un punto navegable de la costa. La cámara sigue suavemente al barco y la proximidad determina la isla seleccionada (`src/app/features/roadmap/engine/archipelago-3d.service.ts:3799-3802`, `:3953-3988`, `:4138-4155`, `:4265`; `src/app/features/roadmap/domain/archipelago-navigation.ts:28-49`). Para entrar debe existir selección y no haber mensaje de bloqueo (`src/app/features/roadmap/pages/worlds-page/worlds-page.component.ts:1114-1135`).
- El último atraque se recuerda por curso en memoria y `sessionStorage`; al volver se abre en esa isla si todavía existe, o en la primera (`src/app/features/roadmap/data-access/session/archipelago-dock.service.ts:3-8`, `:33-42`; `worlds-page.component.ts:1098-1105`). Es una comodidad local de sesión, no sincronización entre dispositivos.
- Dentro de la unidad hay cámara libre/orbital, tercera y primera persona; en modo libre se puede orbitar y acercar/alejar (`src/app/features/roadmap/engine/camera-controller.ts:5-6`, `:87-111`, `:146-155`). La escena también incluye efectos por bioma, agua y fauna (`src/app/features/roadmap/engine/archipelago-3d.service.ts:3420`, `:3650`; `src/app/features/roadmap/engine/archipelago-3d.waves.ts:1`; `src/app/features/roadmap/engine/archipelago-3d.wildlife.ts:1`).
- Al entrar efectivamente a un intento se guarda la posición y orientación del personaje y el giro horizontal de cámara; al volver se consume una sola vez y se restablece. Se guarda por curso/unidad en `sessionStorage`, con tolerancia a almacenamiento no disponible; no prometer restauración permanente ni de todos los parámetros de cámara (`src/app/features/roadmap/pages/hex-world-page/hex-world-page.component.ts:2705-2753`, `:1922-1925`; `src/app/features/roadmap/data-access/roadmap/return-position.ts:1-31`, `:40-75`).

## Modelos, carga y performance — implementado

### Explicación de producto/técnica media

Los modelos son archivos del front que se cargan y reutilizan; no son los materiales educativos del curso.

### Detalle técnico

- Los modelos y texturas identificados se sirven desde `/assets/roadmap/`: por ejemplo caminos glTF en `src/assets/roadmap/world/Hexagon/Assets/gltf/` (`src/app/features/roadmap/domain/world-gen/auto-tiler.ts:1-14`) y barco GLB en `src/assets/roadmap/world-3d/Assets/Vehicles/ship-large.glb` (`src/app/features/roadmap/engine/archipelago-3d.service.ts:3166`, `:3297-3298`). Si falla el modelo del barco queda uno procedural (`:3362`). Son rutas locales del front; esto **no prueba** que el hosting final no use CDN. Tampoco implica que materiales educativos usen el mismo almacenamiento.
- `AssetCacheService` carga con GLTFLoader, reutiliza modelos y solicitudes en curso, comparte dependencias y clona escenas; también gestiona cancelación y liberación de recursos (`src/app/features/roadmap/engine/asset-cache.service.ts:10-19`, `:32-70`, `:137-142`). Hay agrupación de geometría estática (`src/app/features/roadmap/engine/asset-cache.service.ts:93-100`; `src/app/features/roadmap/engine/static-mesh-batching.ts:1`). El pixel ratio se limita a 2 (`archipelago-3d.service.ts:326`; `world-3d.service.ts:2507`) y se liberan recursos al destruir (`archipelago-3d.service.ts:582-611`, `:4358-4390`). No hay medición de FPS en este análisis.

## Material educativo: visor desde la escena, no objeto 3D

### Explicación de producto/técnica media

El cofre abre una interfaz de lectura 2D sobre el mundo, no un libro tridimensional.

### Detalle técnico

- Desde el mundo se accede al material; la página integra `app-material-access` (`src/app/features/roadmap/pages/hex-world-page/hex-world-page.component.html:449`). El visor identificado es un **panel/drawer de interfaz 2D superpuesto**, no un libro o pantalla tridimensional en la escena: HTML se abre en un frame, y otros tipos con `app-content-preview` (`src/app/features/roadmap/ui/material-access/material-access.component.ts:148-179`). La selección del visor contempla metadatos y extensión; hay lógica para PDF, y el editor identifica HTML y Markdown (`material-access.component.ts:282-321`, `:380`; `src/app/features/roadmap/ui/entity-editor-dialog/entity-editor-dialog.component.ts:1015-1017`). La apertura puede ser visor, descarga o pestaña nueva según material (`material-access.component.ts:50`, `:328`). No afirmar que todo PDF/HTML/MD siempre abre embebido.

El cambio reciente `0dae62fcf2` incorpora previsualización de videos externos: para `VIDEO_EXTERNAL` intenta construir una URL embebida de YouTube (`src/app/features/roadmap/ui/material-access/material-access.component.ts:287-295,312-314`). No garantiza que cualquier enlace sea embebible.

## Alumno y docente — implementado

### Explicación de producto/técnica media

El alumno ve su recorrido y restricciones; el docente inspecciona una previsualización sin jugar como alumno.

### Detalle técnico

- El alumno juega con progreso y restricciones; el docente/gestor en previsualización ve los nodos disponibles y no queda bloqueado por unidad, porque está revisando, no jugando (`src/app/features/roadmap/pages/hex-world-page/hex-world-page.component.ts:1097-1110`, `:1242-1266`). Las actividades no disponibles pueden quedar ocultas al alumno (`src/app/features/roadmap/domain/world-gen/from-nodes.ts:75-85`).
- El docente puede revisar detalle y material y abrir la vista previa del desafío; eso no equivale a completar un intento del alumno (`hex-world-page.component.ts:799-836`). No se verificó aquí toda la matriz de roles ni permisos del backend.

## Nodos del cerebro y zonas: alcance

### Explicación de producto/técnica media

Las zonas son partes del recorrido, no cursos nuevos: la unidad puede mostrar islotes cercanos y puertas hacia zonas internas. El grafo de Obsidian sirve para explicar la idea a la audiencia, no para afirmar que esos datos existen en producción.

### Detalle técnico

La guía `tpi-g10-cerebro/demo-neo4j/README.md` declara notas e IDs simulados, no sincronizados ni importables; permite ver reglas AND/OR y relaciones mediante enlaces sin etiquetas gráficas. `tpi-g10-cerebro/arquitectura/mapa-modelo-neo4j.md` y DEC-016/018/021 documentan el modelo y decisiones, no prueban funcionamiento en vivo. El mapeo de zonas e islas sí está en `src/app/features/roadmap/domain/world-gen/from-nodes.ts:30-61` y `src/app/features/roadmap/engine/archipelago-3d.service.ts:1304-1358`.

## Momentos sugeridos para demo

1. Abrir curso con varias unidades y mostrar archipiélago, biomas, orden y diferencia entre isla abierta y bloqueada. Preparar datos de antemano.
2. Navegar manualmente y seleccionar otra isla para mostrar piloto automático y atraque; entrar y volver para evidenciar continuidad.
3. En una isla, recorrer caminos con avatar, cambiar cámara y explicar torres versus cofres; mostrar prerequisito bloqueado y su mensaje, sin atribuir seguridad a la niebla.
4. Abrir un contenido compatible y mostrar el panel de lectura; volver al mundo.
5. Entrar a un desafío real y volver al mismo lugar; si el entorno y los datos lo permiten, completar un prerequisito y mostrar el desbloqueo. No garantizar animación ni progreso sin ensayo integrado.
6. Opcional: alternar a cuenta docente y contrastar la vista previa con la experiencia de alumno, evitando mostrar datos reales.

## Dudas para el usuario

- ¿Quieren incluir zonas y portales, o enfocar la presentación en unidades, contenidos y desafíos? Las zonas precisan datos preparados.
- ¿La demo tendrá dos cuentas y datos de progreso que permitan mostrar bloqueo, desbloqueo y retorno de un intento de punta a punta? El código no demuestra disponibilidad del entorno integrado.
- ¿Conviene mostrar la vista de docente y el visor de materiales, o reservar el tiempo para navegación y desafío?
- ¿Qué biomas y formatos de material están efectivamente publicados y accesibles en el entorno de demo? No se validaron URLs, licencias, rendimiento ni comportamiento de navegador.
- ¿Quieren usar el grafo simulado de Obsidian como apoyo conceptual, aclarando que no son datos de Neo4j en vivo?
