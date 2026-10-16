---
tags: [tpi, g10, taiga, ht]
codigo: HT-02
ref: 555
estado: "Done"
responsable: "Stefano Zoffoli"
epicas: "[[epicas/EP-144 Esqueleto del servicio Roadmap — TRANSVERSAL (v3)|EP-144]]"
sprint: "G10 - Sprint 1"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/555
---

# HT-02: Semilla de datos y guion de demostración

> [!info] Generado desde Taiga (2026-10-15 23:01). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/555) · Estado: **Done** · Responsable: **Stefano Zoffoli** · Sprint: **G10 - Sprint 1**
> Épica: [[epicas/EP-144 Esqueleto del servicio Roadmap — TRANSVERSAL (v3)|EP-144]] · Tareas cerradas: **2/2**

[G10] — HT-02 — Semilla de datos y guion de demostración
--------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: un script de semilla y un guion de demostración que carguen curso-cohorte, alumnos, roadmap, contenidos, lecturas y reglas
*   **Para**: poder demostrar las historias del sprint en menos de diez minutos entrando por el gateway con token real

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Solo para entornos local y de demostración, nunca con datos reales. Corre en CI para no desactualizarse. No introduce reglas de negocio propias: es script y documento.
*   [ ] Validaciones: Un tercero que sigue el guion recorre las historias del sprint sin cargas manuales.
*   [ ] Datos obligatorios: La semilla y el guion.
*   [ ] Performance (tiempos, volumen, límites): La demostración completa se recorre en menos de diez minutos.
*   [ ] Seguridad (roles, permisos, datos sensibles): Solo usuarios de prueba; nunca datos reales de personas.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: Es la última historia en cerrarse porque usa todas las demás. Trazabilidad: DoD nivel 3. Dependencias: ninguna en runtime ni de otros equipos. Datos: solo datos de prueba. Riesgo: que la semilla se desactualice; mitigación, corre en CI.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: La semilla levanta el curso con 12 alumnos y el grafo completo.
*   [ ] **CA2**: Un tercero sigue el guion sin ayuda.
*   [ ] **CA3**: La semilla corre en CI.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Semilla de datos y guion de Sprint Review

**Escenario 1**  

*   **Dado**: una base con la semilla cargada
*   **Cuando**: un tercero sigue el guion con token real
*   **Entonces**: recorre las historias del sprint en menos de diez minutos

**Escenario 2**  

*   **Dado**: un cambio en el modelo de datos
*   **Cuando**: corre el pipeline de CI
*   **Entonces**: la semilla se valida sola y falla si quedó desactualizada

**Escenario 3**  

*   **Dado**: un entorno limpio sin semilla
*   **Cuando**: se ejecuta el script de carga
*   **Entonces**: quedan el curso-cohorte, los 12 alumnos y el grafo con nodos de los tres tipos

* * *
Prototipo
---------

*   **Capturas**: No aplica: historia técnica sin pantalla propia.
*   **URL Figma**: No aplica.
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: Guion sobre los endpoints reales entrando por el gateway con token real, más los lectores simulados declarados en el review.


## Tareas

- [x] #590 T-02.1 — Script de semilla · Closed · Gabriela Camacho
- [x] #591 T-02.2 — Guion de Sprint Review · Closed · Gabriela Camacho
