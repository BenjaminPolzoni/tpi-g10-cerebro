---
tags: [tpi, g10, taiga, hu]
codigo: HU-40
ref: 4246
estado: "Done"
responsable: "Lautaro Jesus Diego"
epica: "[G10] — Nodos de contenido y lectura previa"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4246
---

# HU-40: Ver en el roadmap los ítems del alumno (mapeo visual del inventario)

> [!info] Generado desde Taiga (2026-10-14 18:47). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4246) · Estado: **Done** · Responsable: **Lautaro Jesus Diego** · Sprint: **G10 - Sprint 2**

[G10] — HU-40 — Ver en el roadmap los ítems del alumno (mapeo visual del inventario)
-----------------------------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: ver en mi recorrido los ítems que tengo en el curso, con su efecto y su estado reales
*   **Para**: saber con qué cuento antes de encarar un desafío sin salir del roadmap

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Roadmap no tiene lógica de ítems ni de Mercado. La compra, el equipamiento, el consumo y el efecto son un flujo micro a micro entre Mercado y Accounting (y el Motor para el efecto); Roadmap solo lee lo que devuelve Accounting y lo muestra. Nunca inventa ítems: sin respuesta muestra el último dato conocido con aviso, sin bloquear la lectura. Retira el mock de ítems de HT-03 y la compra simulada del mundo hexagonal. Alcance redefinido por el equipo el 30/09.
*   [ ] Validaciones: Solo ítems del alumno autenticado y del curso-cohorte; matrícula activa.
*   [ ] Datos obligatorios: Alumno (del token) y courseCohortId.
*   [ ] Performance (tiempos, volumen, límites): Lista en menos de 300 ms con caché de corta expiración.
*   [ ] Seguridad (roles, permisos, datos sensibles): Token técnico hacia Accounting (equip-summary acepta rol MS), nunca el JWT de persona; rol STUDENT; sin endpoints de escritura.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Efecto y estado en texto, no solo ícono.
*   [ ] Otros: Para comprar o equipar, el roadmap lleva a las pantallas de Mercado y Accounting que ya existen en el front. Estado actual: GET /api/roadmap/courses/{courseId}/inventory (T-35.1) está hecho pero en stub por defecto (INVENTORY_CLIENT_MODE=stub) y sin audience ni scope (P-12); el front no lo consume y la tienda del mundo hexagonal simula compras (SHOP_ITEMS, 100 monedas). item_equip.feature describe una activación que ya no es de Roadmap y no tiene step definitions: reescribirla como lectura. Dependencias: Accounting (Tema 08) por Gateway. Riesgo: audience y scope sin confirmar; mitigación: último dato conocido. Trazabilidad: HU-35.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El alumno ve sus ítems reales (nombre, efecto, estado y cargas) sin datos simulados.
*   [ ] **CA2**: Roadmap no compra ni equipa: esas acciones llevan a las pantallas de Mercado o Accounting y Roadmap no cambia ningún estado.
*   [ ] **CA3**: Sin respuesta de Accounting se muestra el último dato con aviso de desactualización.
*   [ ] **CA4**: Un alumno no matriculado recibe 403 y no ve ítems.
*   [ ] **CA5**: Una compra o un cambio de equipado hecho en Mercado o Accounting se ve en la próxima consulta.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Inventario del alumno visible en el roadmap

**Escenario 1**  

*   **Dado**: un alumno con un ítem comprado en el Mercado
*   **Cuando**: abre su inventario en el roadmap
*   **Entonces**: lo ve con su efecto y su estado reales

**Escenario 2**  

*   **Dado**: Accounting sin respuesta
*   **Cuando**: el alumno abre su inventario
*   **Entonces**: ve el último dato con aviso y puede seguir leyendo

**Escenario 3**  

*   **Dado**: un alumno que quiere equipar un ítem
*   **Cuando**: elige la acción desde el roadmap
*   **Entonces**: lo lleva a la pantalla de Accounting y Roadmap no cambia ningún estado

* * *
Prototipo
---------

*   **Capturas**: HUD de inventario de HU-35 dentro del mundo (world-3d y hex-world).
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/inventory (T-35.1, en stub por defecto). Sin endpoints de escritura.


## Tareas

- [x] #4302 T-40.1 Audience y scope hacia Accounting e INVENTORY_CLIENT_MODE=http · Closed · Lautaro Jesus Diego
- [x] #4303 T-40.2 Reescribir item_equip.feature como lectura · Closed · Lautaro Jesus Diego
- [x] #4304 T-40.3 HUD de inventario contra GET /inventory · Closed · Lautaro Jesus Diego
- [x] #4305 T-40.4 Retirar la compra simulada (SHOP_ITEMS, 100 monedas) y enlazar al Mercado · Closed · Lautaro Jesus Diego
- [x] #4306 T-40.5 e2e con Accounting · Closed · Lautaro Jesus Diego
- [x] #5403 T-40.6 Wiki, OpenAPI y diagrama de secuencia · Closed · Franco Maximiliano Amarilla
- [x] #7031 T-40.7 Restaurar el interior 3D de la tienda del mundo hexagonal y enlazar al vendedor con el Mercado · Closed · Lautaro Jesus Diego
