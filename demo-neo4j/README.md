---
demo: true
tags: [neo4j-demo]
tipo_entidad: documentacion
---

# Demo visual del modelo Neo4j

**Todo lo que está en esta carpeta es SIMULADO.** Los IDs, nombres, estados y relaciones se inventaron para ilustrar el modelo. Estas notas no se generaron desde una instancia live, no son datos reales y no se sincronizan con Neo4j ni Postgres. No editar ni importar como seed.

## Abrir el grafo en Obsidian

1. Abrí [[00 - Índice de la demo]].
2. En la nota, usá `⋯` → **Open local graph** (o clic derecho en el nombre de la pestaña → **Open local graph**).
3. En los controles del grafo local aumentá **Depth** a `2` o `3` para ver las entidades conectadas y sus relaciones. También se puede abrir el panel Graph y buscar el tag `#neo4j-demo`.
4. Cada nota representa una entidad. Las listas de relaciones en las notas indican **tipo y sentido** explícitamente: el grafo nativo de Obsidian muestra que existe un wikilink, pero no puede mostrar etiquetas distintas para cada arista.

Las propiedades `demo: true` y `tags: [neo4j-demo]` permiten filtrar las notas sintéticas. No se modificó el grafo global ni la configuración del vault.

## Modelo visualizado

- Jerarquía: roadmap → secciones → subsección → nodos.
- Desbloqueo: nodo → regla AND → operandos; una regla OR anidada representa una alternativa.
- Relaciones informativas: `RECOMMENDS` y `RELATED_TO` entre nodos.
- Las aristas son enlaces documentales, no relaciones creadas en la base de datos.

Abrí [[00 - Índice de la demo]] para navegar las notas.
