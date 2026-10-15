---
tags: [tpi, g10, sprint-3, borrador, issue]
para: G01 Courses
estado: enviado
issue: https://github.com/2026-P4-FE/2026-PIV-TPI-FE/issues/581
origen: "[[sprints/sprint-3/historias/HU-68 Obligatoriedad visible en la lista de nodos|HU-68]]"
fecha: 2026-10-15
---

> [!success] Enviado a G01 el 2026-10-15: [#581](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/issues/581). Lo que se mandó es lo que está debajo de la línea.

---

# Mostrar obligatoriedad y requisitos de cada nodo en la vista simplificada de la sección

## Contexto

En las correcciones del 2026-10-14, los profes pidieron: **«Lista de nodos que muestre la obligatoriedad (qué nodo es prerrequisito de otro)»**.

En la página de contenido de la materia, cada sección tiene dos vistas:

- **Vista de edición** (quien puede editar el curso): muestra la lista de nodos del roadmap (componente `app-roadmap-section-nodes` de G10). Esa lista ya cumple el pedido: cada fila dice, por ejemplo, «Lectura · Obligatoria · Requiere: Teoría 1, Práctica 2 (todos) · Disponible».
- **Vista simplificada** (sin permiso de edición): es de ustedes. Hoy muestra solo un botón con el nombre de cada desafío y la lista de recursos (`app-section-resource-list`), **sin decir cuáles son obligatorios ni qué hay que completar antes**.

Les pedimos sumar esa información a la vista simplificada, para que se vea igual en las dos vistas.

## Dónde

- `src/app/features/courses/pages/cohort-general-page/section-resources-container.component.ts`: rama `@else` del template (lista `challenge-list` de desafíos y `app-section-resource-list`).
- `src/app/features/courses/ui/section-resource-list/section-resource-list.component.ts`.

## Qué pedimos

En cada desafío y en cada recurso que sea un nodo del roadmap:

1. **Obligatoriedad**: «Obligatorio» u «Opcional».
2. **Requisitos**: «Requiere: X, Y (todos)», «Requiere: X, Y (cualquiera)», «Requiere: X», o «Abierto al entrar a la unidad» si no tiene.
3. Escrito con texto, no solo con color o ícono (accesibilidad).

## Criterios de aceptación

- [ ] **CA1**: Cada desafío y cada recurso de lectura de la vista simplificada dice si es obligatorio u opcional.
- [ ] **CA2**: Cada uno dice qué requiere, con el mismo texto que la vista de edición («Requiere: … (todos/cualquiera)» o «Abierto al entrar a la unidad»).
- [ ] **CA3**: Si la sección no tiene unidad en el roadmap, la vista se sigue viendo como hoy, sin errores.
- [ ] **CA4**: Test del componente con un nodo obligatorio con requisitos y uno opcional sin requisitos.

**Ejemplo (BDD)**
- **Dado** un desafío obligatorio que requiere «Teoría 1» y «Práctica 2» con regla «todos»
- **Cuando** alguien sin permiso de edición abre la sección
- **Entonces** el desafío dice «Obligatorio · Requiere: Teoría 1, Práctica 2 (todos)»

## Los datos ya están en el front (no hace falta back nuevo)

`SectionResourcesContainerComponent` ya inyecta el `RoadmapStore` y calcula la unidad de la sección (`unit()`). De ahí salen:

| Dato | De dónde |
|---|---|
| Obligatoriedad | `Activity.isMandatory` de cada nodo de `unit().activities` |
| Requisitos | `prerequisitesOf(store.connections(), nodeId)` (`roadmap/domain/unlock-rules.ts`) |
| Modo de la regla (todos / cualquiera) | `prerequisiteModeOf(node)` (`roadmap/data-access/roadmap/roadmap.models.ts`) |
| Texto armado | `describeRule(nombres, modo)` (`roadmap/ui/rules-wizard`) con las claves `rulesWizard.node.requiresOne`, `requiresAll`, `requiresAny` y `open` |

**Propuesta de G10:** para que no tengan que importar piezas internas del roadmap, podemos exportar desde `features/roadmap/embeds` una función que, dado el id de un nodo, devuelva ya armados la obligatoriedad y el texto de los requisitos. Avísennos si les sirve y la sumamos antes de que empiecen.

## Referencias

- Pedido de los profes: correcciones del 2026-10-14, punto «Lista de nodos que muestre la obligatoriedad».
- Vista de edición que ya lo muestra: `features/roadmap/embeds/section-nodes/roadmap-section-nodes.component.ts` (`detailsOf`), commit `b592bf2e`.
- Historia de G10: HU-68.

Contacto: G10 Roadmap.
