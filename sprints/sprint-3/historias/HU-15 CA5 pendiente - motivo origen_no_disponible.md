---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-15
estado: Propuesta
responsable: ""
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 3
prioridad: Should
en_taiga: true
---

# HU-15: CA5 pendiente - motivo origen_no_disponible

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Ya existe en Taiga: [[taiga/historias/HU-15 Impedir la entrega en un nodo bloqueado (gate, vocabulario v3)|HU-15]] (épica EP-60). En el Sprint 3 se **reabre** con lo que falta.

[G10] — HU-15 — Impedir la entrega en un nodo bloqueado (gate, vocabulario v3)
------------------------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: recibir un motivo claro cuando no puedo entrar a un desafío porque otro servicio está caído
*   **Para**: entender que no es mi culpa y reintentar más tarde

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Fail-closed (DEC-003): si Accounting o Courses no responden y no hay caché vigente, el gate bloquea con `origen_no_disponible` en vez de responder 503.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): Timeouts cortos hacia Accounting y Courses para no superar el P95 de 200 ms.
*   [ ] Seguridad (roles, permisos, datos sensibles): Sin cambios de permisos.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: Cambiar 503 por 200 con motivo cambia el contrato con el Motor: avisar a G09 y actualizar el acta del gate.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Con Accounting caído y sin caché vigente: `eligible=false`, `reason=origen_no_disponible`.
*   [ ] **CA2**: Con Courses caído al leer comisiones o restricciones: mismo motivo.
*   [ ] **CA3**: El front muestra un texto para `origen_no_disponible`.
*   [ ] **CA4**: Acta del gate actualizada con G09.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Gate con servicios caídos

**Escenario 1**  

*   **Dado**: Accounting caído y sin caché
*   **Cuando**: el Motor consulta el gate
*   **Entonces**: recibe `eligible=false` con `reason=origen_no_disponible`

**Escenario 2**  

*   **Dado**: Courses caído con `ROADMAP_BY_GROUP_ENABLED=true`
*   **Cuando**: se consulta el gate
*   **Entonces**: devuelve `origen_no_disponible`

**Escenario 3**  

*   **Dado**: Accounting vuelve a responder
*   **Cuando**: se consulta el gate
*   **Entonces**: responde con el motivo real

* * *

Prototipo
---------

*   **Capturas**: No aplica (sin pantalla).
*   **URL Figma**: No aplica.
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: No aplica.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 3
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 3 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Accounting, Courses, Motor.
*   Módulos afectados: `GateService`, `GateEvaluator`.
*   Otros equipos / aprobaciones: G09 (contrato del gate).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que el Motor espere 503; mitigación: acordarlo antes de mergear.

## Tareas

- [ ] T-15.9 Motivo `origen_no_disponible`
- [ ] T-15.10 Tests de servicios caídos
- [ ] T-15.11 Actualizar el acta con G09

---

## Contexto del Sprint 3 (no va a Taiga)

### Criterios de la HU original (Taiga)

Verificados contra `origin/develop` (back `fc1917e`, front `67cbad4a`) el 2026-10-15. ✅ cumple · ❌ no cumple · ⚠️ hecho pero no anda de punta a punta.

- [x] ✅ **CA1**: Un alumno sin la lectura obligatoria recibe contenido_no_leido. — `content_not_read`
- [x] ✅ **CA2**: Un alumno sin el prerrequisito recibe prerrequisito_pendiente. — `prerequisite_pending`
- [x] ✅ **CA3**: Un alumno fuera del curso recibe no_inscripto. — `not_enrolled`
- [x] ✅ **CA4**: Un alumno con 0 vidas recibe sin_vidas, salvo que se trate de recuperación o de un desafío LLM. — `no_lives`; RECOVERY y LLM exentos
- [ ] ❌ **CA5**: Si un origen externo no responde, devuelve habilitado en false con motivo origen_no_disponible, pendiente de acuerdo con G09. — si un origen no responde devuelve 503; no existe `origen_no_disponible`

### Qué hay hoy en el código

Si Accounting o Courses no responden, el gate devuelve 503 en vez del motivo `origen_no_disponible`.

### Depende de

Nada: se puede empezar ya.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|E9]] Con Backoffice caído se usan los valores guardados en caché.
