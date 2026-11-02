---
tags: [tpi, g10, sprint-4, plan, front, roadmap, graph-editor]
fecha: 2026-11-01
autor: Benjamin Polzoni
estado: mockup aprobado - en implementacion
actualizado: 2026-11-01
repo: 2026-P4-FE/2026-PIV-TPI-FE
rama: refactor/graph-editor-inspector
---

# Plan — Inspector de solo lectura del editor de grafo

Mockup aprobado: https://claude.ai/artifact/NgsAzacwvb1p65AiAjukWv

## Decisión
- Se elimina el panel grande «Conectar requisitos» (modo pick: destino, combinar fuentes, lista de fuentes, guardar/cancelar) y los botones «Elegir requisitos en el mapa» y «Configurar prerrequisitos» del panel derecho.
- Toda edición (bioma, regla, subsección, renombrar, ocultar, subir/bajar, eliminar, requisitos XP/desbloqueo) vive en el menú ⋮ y en Añadir/Conectar sobre el mapa.
- El panel derecho pasa a ser un inspector **solo lectura**: sin botones de acción ni selects.

## Contenido del inspector
- **Sección:** nombre, chips (Sección, bioma, orden, nodos), resumen, requisitos para entrar (desbloqueo + XP, combinación Y/O), desbloquea.
- **Nodo desafío:** tipo, sección, obligatorio, desafío asignado, intentos/reintentos/ventana, información (orden, recompensa), requisitos, dependientes.
- **Nodo de info:** contenido, orden, recompensa, requisitos, dependientes.
- Pie: «Para editar, usá el menú ⋮ del mapa».

## Reglas
- Reutilizar `inspectorPrerequisites()` / `inspectorDependents()` y datos que ya existen; no tocar el back.
- Sin tests mientras se programa; solo antes de abrir PR (ver memoria no-tests-while-coding).
- Una sola rama de trabajo.
