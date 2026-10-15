---
tags: [tpi, g10, taiga, epica]
ref: 593
estado: "New"
responsable: "Sin asignar"
avance: "8/8"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/593
---

# EP-593: Nodos de contenido y lectura previa

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/593) · Estado: **New** · Responsable: **Sin asignar** · HU cerradas: **8/8**

[G10] — Nodos de contenido y lectura previa
-------------------------------------------

* * *

Objetivo
--------

Que el alumno lea el contenido de una unidad antes de habilitarse para sus desafíos, y que el profesor decida qué material es de lectura obligatoria. Es lo que convierte al roadmap de una lista de ejercicios en un recorrido pedagógico. Incluye la interfaz de inventario (HU-35): el alumno ve y equipa sus ítems antes de entrar a un desafío.

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: el material de estudio lo almacena Courses y nosotros guardamos el contenido\_id, la posición en el grafo y la regla de obligatoriedad, nunca el archivo ni el texto. Courses expone una lectura por lote de metadatos: con 20 nodos de contenido en una unidad, una llamada por nodo serían 20 viajes por el gateway. El MVP asume marcado explícito del alumno ("marcar como leído"); si Courses publica más adelante una señal de consumo real, se suma como segundo origen del mismo hecho sin cambiar el modelo. La lectura es append-only e idempotente por alumno y nodo, por curso-cohorte. El inventario (vidas e ítems) lo persiste el dominio Inventario (ex-Coins/Wallet): Roadmap muestra y equipa, el Motor aplica la lógica del ítem y lo descuenta.
*   Restricciones (legales/técnicas): la obligatoriedad se define por nodo, no por tipo de material. Un nodo dado de baja deja de contar para la regla pero no borra las lecturas ya registradas. Un alumno no puede marcar como leído un nodo de una unidad que todavía no desbloqueó. Los cambios rigen hacia adelante y no revierten desbloqueos ya alcanzados (RF-CFG-06).

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] Un profesor vincula tres contenidos a una unidad y marca dos como obligatorios; el alumno los lee y recién entonces el gate de E3 lo habilita para el primer desafío de esa unidad. El alumno equipa un ítem de su inventario y el Motor lo recibe en el contexto de inicio del desafío.
*   [ ] KPIs iniciales: ningún KPI de producto aplica. El indicador propio es que el avance de lectura de una unidad se calcula y responde en menos de 200 ms, porque el gate de E3 lo consulta en cada entrega.
*   [ ] Sin regresiones críticas en E3: agregar un contenido obligatorio a una unidad no revierte el desbloqueo de ningún alumno que ya la había desbloqueado.
*   [ ] Observabilidad y alertas: contador de marcados de lectura por unidad y por origen (manual / señal externa). Alerta si el porcentaje de alumnos que marcan todos los contenidos obligatorios en menos de diez segundos supera un umbral.
*   [ ] Documentación publicada: página de Wiki con el contrato de lectura acordado con Courses y la definición operativa de "leído", más el endpoint de avance de lectura publicado en OpenAPI para los equipos de desafíos.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: Courses (catálogo de contenidos por unidad y metadatos por lote), Inventario (ítems por lote), Motor de Desafíos (lógica del ítem equipado), API Gateway.
*   Módulos afectados: nodo de contenido, registro de lectura, proyección de avance de lectura, selección de ítem, gate de habilitación (E3).
*   Otros equipos: Courses es el bloqueante. Sin su contrato de lectura de contenidos, los nodos de contenido no tienen a qué apuntar. Pedido con fecha, día 3 del Sprint 1.
*   Impacto en datos / migraciones: tablas nodo\_contenido (referencia y obligatoriedad), lectura\_contenido (append-only) y seleccion\_item (ítem equipado por alumno y desafío), más la proyección avance\_lectura\_unidad.
*   Feature toggles / flags: lectura-obligatoria, que cubre el efecto de la regla sobre el gate. Con el flag apagado los nodos se ven y se marcan, pero no bloquean la entrega. Plan de retiro: se elimina cuando la regla esté acordada con los equipos de desafíos y estable en producción.


* * *

Ampliación Sprint 2: material teórico del curso (pedido 9) y ajustes de alcance
-------------------------------------------------------------------------------

*   Objetivo de la ampliación: que el roadmap muestre en sus nodos (nodos de lectura y el Templo del mundo 3D, materials-page) el material teórico que el profesor guarda en Cursos (PDF, video, enlace u otro), pidiéndoselo a Courses. Roadmap no guarda ni sube archivos. Se integra a esta épica (D-04, 02/10): no se crea épica nueva.
*   Suposiciones: Courses es dueño del material y lo guarda en la plataforma Garage (almacenamiento de objetos) para no cargar su base; Roadmap se lo solicita para mostrarlo (decisión del 02/10, P-30). course_activity ya tiene external_url, object_key y original_filename. Roadmap solo guarda la referencia del nodo al material (content_id, HU-04). Se reutiliza el visor embebido del front (toEmbedUrl: YouTube, Vimeo, Drive y visor de Office para PPT). Una unidad equivale a una sección (épica Unidades ↔ Courses).
*   Restricciones: token técnico por el Gateway. El material de una unidad bloqueada se lista sin poder abrirse (misma regla que HU-05). No es el banco de preguntas de Desafíos Teóricos (theory-bank-page), que es de otro equipo. Bajas lógicas (RF-NFR-01). 100 % escritorio (RF-NFR-05).
*   Alcance de ítems actualizado (decisión del equipo, 30/09): Roadmap no tiene lógica de ítems ni de Mercado y no equipa. La compra y el equipamiento son un flujo micro a micro entre Mercado y Accounting; Roadmap solo muestra lo que devuelve Accounting (HU-40). Reemplaza lo que esta épica dice sobre equipar ítems y enviarlos al Motor (cierra P-21 y P-22).

**Criterios de aceptación de la ampliación**

*   [ ] El alumno abre un nodo de lectura o el Templo y ve el material real que devuelve Courses (PDF, video o enlace), agrupado por unidad en el Templo; no queda EXAMPLE_SECTIONS en materials-page.
*   [ ] En una unidad bloqueada ve que hay material pero no puede abrirlo.
*   [ ] Abrir un material desde la biblioteca o desde su nodo de lectura muestra lo mismo; marcarlo como leído desde cualquiera de los dos registra una sola lectura (HU-06) y actualiza el gate.
*   [ ] Un material despublicado o dado de baja se ve «no disponible» y las lecturas quedan intactas.
*   [ ] Una sola llamada a Courses por curso: menos de 500 ms para 20 unidades (RF-NFR-03).

**Dependencias de la ampliación**

*   Servicios: G01 (bloqueante: guardar el material en Garage, habilitar actividades FILE y LINK —hoy solo se crea QUIZ— y exponer por lote, con token técnico, los metadatos y una URL de acceso a cada archivo, por ejemplo firmada y con vencimiento). Plataforma: Garage todavía no aparece en tpi-course ni en tpi-system-compose (relevado el 02/10).
*   Front: materials-page (hoy EXAMPLE_SECTIONS fijas), section-map-page y world-3d-page.
*   Feature toggles / flags: ninguno propuesto.

**Historias del Sprint 2 en esta épica**

*   HU-46 (el alumno ve en los nodos y en el Templo el material teórico de Courses). HU-47 retirada el 02/10: la carga del material es de Cursos (G01).
*   HU-04 (vincular el nodo al material, condicionada a G01) y HU-42 (abrir y leer) usan esta misma fuente de material.
*   HU-40 (ver en el roadmap los ítems del alumno: solo mapeo visual del inventario).
*   HU-19 entra al Sprint 2 (barra de avance de lectura).
*   HU-42 y HU-04 dependen de que G01 defina qué es un contenido y exponga la lectura por lote (P-16). Posible superposición entre HU-46 y HU-42 (P-31).



## Historias

| HU | Estado | Responsable | Sprint | Tareas |
|---|---|---|---|---|
| [[historias/HU-06 Marcar un nodo de contenido como leído\|HU-06]] Marcar un nodo de contenido como leído | Done | Fenoglio Santino | G10 - Sprint 1 | 6/6 |
| [[historias/HU-04 Vincular un nodo de contenido al material publicado por Courses\|HU-04]] Vincular un nodo de contenido al material publicado por Courses | Done | Iker Alonso | G10 - Sprint 2 | 5/5 |
| [[historias/HU-05 Ver el detalle de un nodo de contenido (canónica)\|HU-05]] Ver el detalle de un nodo de contenido (canónica) | Done | Lorenzo Araujo | G10 - Sprint 1 | 5/5 |
| [[historias/HU-11 Configurar qué contenidos son de lectura obligatoria\|HU-11]] Configurar qué contenidos son de lectura obligatoria | Done | Gabriela Camacho | G10 - Sprint 1 | 5/5 |
| [[historias/HU-19 Ver el avance de lectura de mi unidad\|HU-19]] Ver el avance de lectura de mi unidad | Done | Gabriela Camacho | G10 - Sprint 2 | 5/5 |
| [[historias/HU-40 Ver en el roadmap los ítems del alumno (mapeo visual del inventario)\|HU-40]] Ver en el roadmap los ítems del alumno (mapeo visual del inventario) | Done | Lautaro Jesus Diego | G10 - Sprint 2 | 7/7 |
| [[historias/HU-42 Abrir y leer el material de un nodo de lectura desde el roadmap\|HU-42]] Abrir y leer el material de un nodo de lectura desde el roadmap | Done | Fenoglio Santino | G10 - Sprint 2 | 5/5 |
| [[historias/HU-46 Ver en los nodos y en el Templo el material teórico de Courses\|HU-46]] Ver en los nodos y en el Templo el material teórico de Courses | Done | Fenoglio Santino | G10 - Sprint 2 | 5/5 |
