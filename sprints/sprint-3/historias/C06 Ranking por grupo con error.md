---
tags: [tpi, g10, sprint-3, historia, bug]
id: C06
tipo: Bug
epica: "EP-S3-2"
capa: "Back + Front"
esfuerzo: M
puntos: 5
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [B02]
---

# C06: Ranking por grupo con error

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes|EP-S3-2]] · **Bug** · Capa: **Back + Front** · **5 pts** · **Must** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-xx — Ranking por grupo con error** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: ALUMNO / PROFESOR
- **Quiero**: ver el ranking sin errores, por curso por defecto y con filtro opcional por comisión
- **Para**: comparar mi avance con el de mi curso o mi comisión

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Default: ranking por curso. La comisión es un filtro (P10). El orden es por XP con desempate en cascada (HU-25); si van notas, lo define P14.
- [ ] Seguridad (roles, permisos, datos sensibles): Anonimato de filas ajenas (DEC-007).
- [ ] Otros: El error no está reproducido (E1).

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Error reproducido y documentado.
- [ ] **CA2**: El ranking muestra el del curso por defecto.
- [ ] **CA3**: Filtro opcional por comisión.
- [ ] **CA4**: Test que cubre el caso que fallaba.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Ranking por grupo

**Escenario 1**

- **Dado**: un curso con 2 comisiones
- **Cuando**: el alumno abre el ranking
- **Entonces**: ve el del curso completo

**Escenario 2**

- **Dado**: el mismo curso
- **Cuando**: elige su comisión
- **Entonces**: ve solo los de su comisión

**Escenario 3**

- **Dado**: el caso que fallaba
- **Cuando**: se repite
- **Entonces**: responde sin error

* * *

## Prototipo

- **Capturas**: Ranking con filtro.
- **URL Figma**: Pendiente.
- **Storybook**: `generic-select`, `generic-table`.
- **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/ranking?group_id=…

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 5
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Courses (comisiones).
- Módulos afectados: `RankingController`, `RankingService`, `ranking-panel`.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Depende de B02 (flag).

## Tareas

- [ ] T-C06.1 Reproducir el error
- [ ] T-C06.2 Filtro por comisión en el back
- [ ] T-C06.3 Filtro en el front
- [ ] T-C06.4 Tests

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

El back solo tiene ranking por curso (`GET /courses/{id}/ranking`); el avance por grupo es otro endpoint. El front no tiene selector de grupo. El error no está reproducido.

### Depende de

- [[sprints/sprint-3/historias/B02 Encender los flags en los entornos|B02]] Encender los flags en los entornos

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E1]]
- [[sprints/sprint-3/08-dudas|P10]]
- [[sprints/sprint-3/08-dudas|P14]]
