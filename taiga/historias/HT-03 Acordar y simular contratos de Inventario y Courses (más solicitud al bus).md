---
tags: [tpi, g10, taiga, ht]
codigo: HT-03
ref: 732
estado: "Done"
responsable: "Sin asignar"
epicas: "[[epicas/EP-144 Esqueleto del servicio Roadmap — TRANSVERSAL (v3)|EP-144]]"
sprint: "G10 - Sprint 1"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/732
---

# HT-03: Acordar y simular contratos de Inventario y Courses (más solicitud al bus)

> [!info] Generado desde Taiga (2026-10-14 20:44). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/732) · Estado: **Done** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 1**
> Épica: [[epicas/EP-144 Esqueleto del servicio Roadmap — TRANSVERSAL (v3)|EP-144]] · Tareas cerradas: **7/7**

[G10] — HT-03 — Acordar y simular contratos de Inventario y Courses (más solicitud al bus)
------------------------------------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: acordar por escrito y simular los contratos de Inventario y Courses, y pedirle al grupo Notificaciones los datos del bus
*   **Para**: que el gate tenga contra qué probarse y HU-04, HU-06, HU-11, HU-15 y HU-35 se puedan desarrollar desde el día uno

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Contrato de Inventario: vidas vigentes más motivo degradado, nunca habilitado por defecto. Contrato de Courses: metadatos por lote. Todo con caché y degradación explícita, y todo por el Gateway. Al grupo Notificaciones se le pide, no se inventa: topic de resultados, topic de eventos propios, key, producer id, DLQ y reintentos.
*   [ ] Validaciones: El acta tiene que estar firmada por ambos equipos antes de dar el mock por definitivo; si el contrato real cambia, el mock se actualiza en el mismo PR.
*   [ ] Datos obligatorios: De Inventario: vidas vigentes y techo. De Courses: título, tipo y estado de publicación.
*   [ ] Performance (tiempos, volumen, límites): El mock responde en menos de 50 ms para no distorsionar la medición del gate (RF-NFR-03).
*   [ ] Seguridad (roles, permisos, datos sensibles): Token técnico siempre, nunca el JWT de una persona.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Sin pantalla propia.
*   [ ] Otros: El mock vive detrás de una interfaz única por contrato: cambiar al cliente real no toca a los consumidores. Trazabilidad: DoD niveles 1 y 2; trazabilidad de E2 y E3 con Inventario y Courses. Dependencias: Inventario, Courses, Notificaciones (P-09) y Gateway; es bloqueante de HU-04, HU-06, HU-11, HU-15 y HU-35, con las actas y la solicitud al bus pedidas el día 3. Datos: solo caché en memoria. Riesgo: acta tardía o topic sin definir; mitigación, mock con la forma propuesta y P-09 pedido por escrito el día 3.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Existe un acta escrita con Inventario que cubre vidas y degradación.
*   [ ] **CA2**: Existe un acta escrita con Courses que cubre la lectura de metadatos por lote.
*   [ ] **CA3**: Los mocks responden de forma consistente y el escenario degradado es reproducible en test.
*   [ ] **CA4**: Cambiar los datos del mock no obliga a tocar HU-04, HU-06, HU-11, HU-15 ni HU-35.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Contratos simulados de Inventario y Courses

**Escenario 1**  

*   **Dado**: el mock de Inventario con un alumno de 2 vidas
*   **Cuando**: el gate consulta
*   **Entonces**: recibe 2 vidas con la forma del contrato real

**Escenario 2**  

*   **Dado**: el mock configurado para no responder
*   **Cuando**: el gate consulta
*   **Entonces**: recibe degradación explícita, nunca habilitado ni un error genérico

**Escenario 3**  

*   **Dado**: el mock de Courses con 20 contenidos
*   **Cuando**: se piden los metadatos
*   **Entonces**: llegan en una sola llamada

* * *
Prototipo
---------

*   **Capturas**: No aplica: historia técnica sin pantalla propia.
*   **URL Figma**: No aplica.
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: Clientes simulados con interfaz idéntica a la real: lectura de vidas e ítems de Inventario y lectura por lote de metadatos de Courses.


## Tareas

- [x] #2074 T-03.1 — Acta del contrato de vidas e ítems con Inventario · Closed · Baltasar Rodriguez Teruel
- [x] #2075 T-03.2 — Cliente HTTP y caché con degradación · Closed · Baltasar Rodriguez Teruel
- [x] #2076 T-03.3 — Acta de metadatos con Courses · Closed · Iker Alonso
- [x] #2077 T-03.4 — Cliente HTTP y caché de catálogo por lote · Closed · Iker Alonso
- [x] #2078 T-03.5 — Mocks para integración · Closed · Iker Alonso
- [x] #2079 T-03.6 — Solicitud al grupo Notificaciones (P-09: topic, key, DLQ) · Closed · Iker Alonso
- [x] #2892 T-03.7 — Wiki: página de integraciones (Inventario, Courses y bus) · Closed · Quinteros Tomás
