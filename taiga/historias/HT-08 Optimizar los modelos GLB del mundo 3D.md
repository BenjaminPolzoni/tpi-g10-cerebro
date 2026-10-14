---
tags: [tpi, g10, taiga, ht]
codigo: HT-08
ref: 4250
estado: "Done"
responsable: "Baltasar Rodriguez Teruel"
epica: "[G10] — Esqueleto del servicio Roadmap — TRANSVERSAL (v3)"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4250
---

# HT-08: Optimizar los modelos GLB del mundo 3D

> [!info] Generado desde Taiga (2026-10-14 18:47). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4250) · Estado: **Done** · Responsable: **Baltasar Rodriguez Teruel** · Sprint: **G10 - Sprint 2**

[G10] — HT-08 — Optimizar los modelos GLB del mundo 3D
-----------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: reducir el peso de los modelos GLB del mundo 3D sin cambios visibles y con el servido correcto desde nginx
*   **Para**: que el mundo 3D cargue más rápido para el alumno sin perder calidad visual

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Sin cambios visibles aceptados: el mundo 3D debe verse igual. La técnica (compresión de geometría, de texturas o reducción de polígonos) se elige después de medir y probar con una muestra. Si la técnica exige decodificadores en GLTFLoader, se incorporan al front (Angular e index.html de world-3d). Justificación técnica: ningún alumno ni profesor percibe esta tarjeta salvo por el tiempo de carga (falla la V de INVEST a propósito). El mundo 3D carga 115 archivos .glb desde /assets/roadmap/world-3d/ con 50,7 MB sin comprimir, más 110 .fbx (10,5 MB) sin referencia en ejecución y 186 glTF con .bin (9,1 MB). Los 4 Skeleton_* suman unos 19 MB. La capa de servido no está en el repo: el nginx.conf del front solo comprime texto, JS y JSON, y los .glb salen como application/octet-stream, sin gzip ni caché.
*   [ ] Validaciones: Los 115 modelos cargan sin errores en escritorio; compatibilidad de navegadores y de GLTFLoader de Three.js verificada.
*   [ ] Datos obligatorios: Línea base: 115 archivos, 50,7 MB, tiempo de primera carga y de carga posterior.
*   [ ] Performance (tiempos, volumen, límites): Meta de reducción a fijar en el planning (P-17).
*   [ ] Seguridad (roles, permisos, datos sensibles): Mantener X-Frame-Options SAMEORIGIN, no DENY: world-3d-page y avatar-panel cargan el mundo 3D en un iframe del propio front.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Sin cambios.
*   [ ] Otros: Pedido al responsable del nginx (P-27): (1) MIME: include mime.types más types { model/gltf-binary glb; }; poner solo el bloque types deja los .js como octet-stream y la app queda en blanco. (2) Gzip: model/gltf-binary en gzip_types (y application/octet-stream mientras los .glb no tengan MIME) con gzip_comp_level 5. (3) Caché: un año immutable solo para bundles con hash; /assets/ con no-cache y revalidación 304; index.html sin caché. (4) X-Frame-Options: SAMEORIGIN. Unos 37 GLB sin referencia estática detectable: verificar a mano, porque index.html arma rutas por nombre; si HU-29 archiva vistas, modelos sin uso podrían retirarse (P-17). Proceso reproducible y documentado en la Wiki o el README. Riesgo: pérdida de calidad visual; mitigación: piloto con una muestra y revisión antes de aplicar a los 115.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Línea base documentada (tamaño total y tiempos) antes de modificar nada.
*   [ ] **CA2**: El tamaño total baja respecto de la línea base en la meta que fije el planning.
*   [ ] **CA3**: Los 115 modelos cargan y se ven igual en el mundo 3D (revisión con capturas).
*   [ ] **CA4**: nginx sirve los .glb como model/gltf-binary comprimidos, /assets/ revalida con 304, los bundles con hash tienen caché immutable, la app no queda en blanco y el mundo 3D sigue embebido en su iframe (verificado con curl y en el navegador).
*   [ ] **CA5**: El proceso queda documentado y se puede repetir sobre los modelos.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Optimización de los modelos GLB

**Escenario 1**  

*   **Dado**: la línea base medida
*   **Cuando**: se ejecuta el proceso de optimización
*   **Entonces**: el tamaño total baja y el resultado queda registrado

**Escenario 2**  

*   **Dado**: los modelos optimizados
*   **Cuando**: el alumno abre el mundo 3D en escritorio
*   **Entonces**: todos se ven y no hay errores en consola

**Escenario 3**  

*   **Dado**: un navegador con caché previa
*   **Cuando**: recarga el mundo 3D
*   **Entonces**: no redescarga los modelos (304 o caché local)

* * *
Prototipo
---------

*   **Capturas**: No aplica: historia técnica sin pantalla. Evidencia: tabla antes/después y capturas del mundo 3D.
*   **URL Figma**: No aplica.
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: No aplica.


## Tareas

- [x] #4330 T-08.1 Medir línea base · Closed · Baltasar Rodriguez Teruel
- [x] #4331 T-08.2 Elegir técnica y probar con una muestra · Closed · Baltasar Rodriguez Teruel
- [x] #4332 T-08.3 Proceso reproducible sobre los 115 modelos · Closed · Baltasar Rodriguez Teruel
- [x] #4336 T-08.4 Verificar carga en el front con capturas · Closed · Baltasar Rodriguez Teruel
- [x] #4338 T-08.5 Re-medir y documentar · Closed · Baltasar Rodriguez Teruel
- [x] #4339 T-08.6 Pedir la configuración al responsable del nginx y verificarla con curl · Closed · Baltasar Rodriguez Teruel
- [x] #4340 T-08.7 Retirar .fbx y modelos sin uso tras confirmarlo · Closed · Baltasar Rodriguez Teruel
- [x] #5407 T-08.8 Wiki, OpenAPI y diagrama de secuencia · Closed · Quinteros Tomás
- [x] #6773 T-08.3.1 Corregir pipeline de cuantización para preservar transforms y bounds · Closed · Baltasar Rodriguez Teruel
