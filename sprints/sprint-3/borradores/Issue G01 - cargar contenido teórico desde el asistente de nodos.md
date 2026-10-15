---
tags: [tpi, g10, sprint-3, borrador, issue]
para: G01 Courses
estado: enviado
issue: https://github.com/2026-P4-FE/2026-PIV-TPI-FE/issues/582
fecha: 2026-10-15
---

> [!success] Enviado a G01 el 2026-10-15: [#582](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/issues/582). Lo que se mandó es lo que está debajo de la línea.

---

# Poder cargar archivos y enlaces de contenido teórico desde el asistente de creación de nodos

## Contexto

Cuando el profesor arma la materia, crea los nodos del roadmap con el **asistente de nodos** (componente de G10, `app-node-creation-wizard`, que se abre desde la lista de nodos de cada sección). Tiene 4 pasos: unidad, tipo, detalle y revisión.

Si elige un **nodo de lectura** (contenido teórico), hoy el paso «Detalle» solo ofrece:
- un campo de texto libre para una URL,
- la casilla de «lectura obligatoria».

**No se puede subir un archivo ni cargar el enlace como contenido de la materia.** Para eso el profesor tiene que salir del asistente, ir a «+ Añadir contenido» de la sección, cargarlo ahí y después volver a crear el nodo.

Queremos que, al crear un nodo de lectura, el profesor pueda **cargar ahí mismo el archivo o el enlace** del contenido teórico, y que quede publicado en Courses como cualquier otro contenido de la sección.

## Por qué se lo pedimos a ustedes

El contenido teórico es de Courses: lo guardan ustedes (Garage) y el roadmap solo lo referencia (no guarda archivos). La carga ya existe en su front:

- `CourseContentService`: `create` (registra el contenido y, si es archivo, devuelve la URL firmada), `uploadBytes` (sube los bytes al storage) y `confirm` (confirma la subida).
- `app-section-resources-editor`: el formulario de recursos de la sección (archivo por `fileSelected`; enlace o video por `externalSubmitted` con `type`, `title` y `externalUrl`).

Para no duplicar ese flujo ni usar piezas internas de su feature, les pedimos **exponer la carga como una pieza reutilizable** que podamos poner dentro del asistente.

## Qué pedimos

1. Un componente (o función) **público** de Courses para cargar un contenido en una sección, con:
   - entrada: `courseCohortId`, `courseSectionId` y el tipo permitido (archivo, enlace o video externo);
   - salida: el **contenido creado y confirmado** (`CourseContent`, con su `id`), o el error;
   - estados de subiendo, error y reintento, con los mismos textos y límites que «+ Añadir contenido».
2. Que se pueda usar **dentro de un modal** (el asistente ya es un modal) sin que abra otro modal.

## Criterios de aceptación

- [ ] **CA1**: Existe una pieza pública de Courses para cargar un archivo, un enlace o un video externo en una sección, que devuelve el contenido confirmado.
- [ ] **CA2**: Un archivo se sube con el mismo flujo que hoy (crear → subir a la URL firmada → confirmar), con los mismos límites de tamaño y tipos.
- [ ] **CA3**: Si la subida falla, la pieza muestra el error y permite reintentar, sin dejar contenidos pendientes a medias.
- [ ] **CA4**: El contenido cargado así aparece en la sección igual que uno cargado desde «+ Añadir contenido».

**Ejemplo (BDD)**
- **Dado** un profesor creando un nodo de lectura en la sección «Unidad 1»
- **Cuando** sube «apunte-unidad-1.pdf» desde el paso «Detalle» del asistente
- **Entonces** el archivo queda publicado como contenido de «Unidad 1» y el nodo de lectura lo tiene como material

## Lo que hacemos nosotros (G10)

Cuando la pieza esté disponible:
- la sumamos al paso «Detalle» del asistente cuando el tipo es «lectura», en lugar del campo de URL libre;
- vinculamos el nodo con el contenido devuelto (su `id`), como hoy se vincula un nodo con el material de la sección;
- mostramos el contenido en el paso «Revisión».

## Referencias

- Asistente de nodos (G10): `src/app/features/roadmap/ui/node-creation-wizard/node-creation-wizard.component.ts` (paso `detail`, rama `isTheory()`).
- Servicio de contenidos (G01): `src/app/features/courses/data-access/course-content.service.ts`.
- Editor de recursos (G01): `src/app/features/courses/ui/section-resources-editor/section-resources-editor.component.ts`.

Contacto: G10 Roadmap.
