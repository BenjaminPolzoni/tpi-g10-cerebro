---
tags: [presentacion, roadmap]
---

# A6. Preguntas difíciles

**¿Por qué no guardan todo directamente en Neo4j?** La decisión vigente deja escritura transaccional en Postgres y mantiene un grafo de lectura reconstruible. La convergencia no es instantánea garantizada.

**¿Por qué una función del front podría dar puesto 2 si el servidor devuelve 1 compartido?** El servidor devuelve 1,1,3 para empate completo; la función auxiliar `rankBy` numera 1,2,3 y podría cambiar percentiles o zonas si se usara. En el recorrido HTTP inspeccionado el mapper conserva los valores del servidor y no encontramos llamada productiva a esa función; no afirmamos una divergencia visual sin probarla. Ver `_presentacion-src/tpi-roadmap/src/main/java/com/utn/tpi/roadmap/services/RankingRules.java:85-103`, `_presentacion-src/fe/src/app/features/ranking/domain/ranking.rules.ts:188-224` y `_presentacion-src/fe/src/app/features/ranking/data-access/ranking-http/ranking-mapper.ts:71-76`.

**¿Si falla Courses se abre igual?** Si el gate necesita una fuente y no está disponible, responde bloqueado con el motivo correspondiente.

**¿Hay entrega exactamente una vez?** No lo afirmamos. El outbox y los controles de duplicados reducen riesgos en caminos concretos; no prueban garantía global.

**¿Si se arrastra un nodo se guarda?** Reordenar y cambiar de sección tienen rutas persistentes; el layout de regiones tiene persistencia con control de versión. Las coordenadas libres de nodo no están implementadas por el adaptador.

**¿Ya está terminado el cierre HU-72?** No está confirmado el flujo completo. Roadmap recibe archivo y aporta indicadores; Courses mantiene el estado académico.

**¿Una rectificación nunca quita progreso?** No: puede reabrir un nodo si ya no queda aprobación válida; no aseguramos una reversión total de consecuencias.

**¿Todo el ranking es anónimo?** Depende de configuración y vista; no lo garantizamos universalmente.

**¿El grafo de Obsidian demuestra Neo4j funcionando?** No. `C/demo-neo4j/` contiene datos simulados sin sincronización con base.

**¿Nunca usan nombres para relacionar datos?** En general se relacionan por UUID, pero la sincronización puede adoptar unidades legacy por nombre y orden, o zonas manuales por nombre y padre. Una coincidencia accidental es un riesgo del enlace inicial; ver [[11-Identificadores-y-datos-entre-micros]].

**¿Qué pasa si Users o Courses no responden?** Depende de la operación: puede faltar información de perfil, una matrícula no verificarse o el material marcarse no disponible; no se debe presentar una falla como prueba de que no existen datos.

**¿El resultado del Motor trae el ID del roadmap?** El contrato consumido inspeccionado trae cohorte, alumno y desafío, y puede traer nodo e intento; Roadmap resuelve el mapa. No afirmamos que todos los mensajes incluyan roadmapId.
