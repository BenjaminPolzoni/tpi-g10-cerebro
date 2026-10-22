---
tags: [tpi, g10, roadmap, sprint-3, rendimiento]
tarea: "T-20.4 (#9060)"
historia: "[[sprints/sprint-3/historias/HT-20 Gate y progreso con reglas combinadas y XP mínimo|HT-20]]"
---

# T-20.4 — Latencia del gate con la caché de reglas

**Historia:** HT-20 (CA4) · **Criterio:** el P95 del gate no supera 200 ms con la caché de reglas (HT-18, T-18.4) sobre un roadmap de 150 nodos.

Lo que se puede afirmar con lo medido está al final, en «Veredicto». Todo número de este documento sale de una corrida real en la máquina descripta; cambian de una corrida a otra y se informan como rango.

## Roadmap de 150 nodos

`GateRoadmapFixture` (código de test) lo arma igual en cada corrida: 10 unidades de 15 nodos obligatorios.

| Pieza | Regla |
|---|---|
| Unidad 1 | Sin requisito |
| Unidades 2, 3, 5, 6, 7, 9 | Exigen la anterior |
| Unidad 4 | Exige la 3 y **500 XP** |
| Unidad 8 | Exige la 7 y **1500 XP** |
| Unidad 10 | `U9 y (U7 o U8)` |
| Tema 1 de cada unidad | Sin requisito |
| Temas múltiplos de 5 | `A y (B o C)`: el anterior y (el de dos antes o el de tres antes) |
| Resto de los temas | Exigen el anterior |

Seis alumnos con progreso distinto: `ALL_DONE` (las 10 unidades), `NEWBIE` (nada), `HALFWAY` (1 a 5), `LOW_XP` (1 a 3 con 100 XP), `ENOUGH_XP` (1 a 3 con 500 XP) y `NEARLY_DONE` (1 a 9). Juntos cubren cada motivo de bloqueo de reglas: unidad pendiente por falta de unidades y por falta de XP, y tema pendiente.

## Qué prueban los tests (corren siempre en `verify`)

No miran el reloj:

- `GateRoadmapFixtureTest`: 150 nodos distintos, las reglas de arriba y el progreso de cada alumno.
- `GateOutcomesWithCacheTest` / `GateOutcomesWithoutCacheTest`: los 6 × 150 resultados coinciden con un oráculo escrito aparte, con la caché y sin ella.
- Mismas clases, por conteo de sentencias SQL: con la caché una consulta del gate no lee **ninguna** tabla de reglas; sin ella, sí. Armar la foto de un roadmap nuevo cuesta entre 1 y 15 sentencias y después las consultas no leen reglas.
- Invalidación: editar la regla de un tema, o subir el XP mínimo de una unidad, se ve en la consulta siguiente.
- `LatencyStatsTest` y `ConcurrentLoadTest`: el cálculo del percentil y el repartidor de carga, con sus casos borde.

## Cómo se mide la latencia

### En proceso (`-Pperf`)

`GateLatencyWithCacheTest` y `GateLatencyWithoutCacheTest` llevan `@Tag("perf")`: dependen del reloj, así que **no corren en `verify`**. Sí fallan si el P95 llega a 200 ms.

```bash
./mvnw -B test -Pperf
```

Ocho hilos, 3000 consultas de calentamiento y 20 000 medidas, repartidas entre los seis alumnos y los 150 nodos. Mide `GateService.evaluate`: servicio, JPA y H2 en memoria, sin HTTP.

### Por HTTP

`performance/k6/gate-eligibility.js` consulta el gate real con 120 usuarios virtuales. Arrancar Roadmap con el perfil `load` siembra el mismo roadmap (`GateLoadFixtureSeeder`) y el script lo recorre con ocho combinaciones de alumno y nodo, comprobando decisión y motivo. El procedimiento (mock de Accounting, arranque y `k6 run`) está en `performance/README.md` del repo `tpi-roadmap`; para medir con la caché hay que arrancar con `RULE_CACHE_ENABLED=true`.

Un tramo de calentamiento a la misma carga corre antes y queda fuera del umbral, porque con la JVM fría el P95 mide el JIT (ver resultados).

## Entorno de las mediciones

Portátil Windows 10, Intel Core i3-1215U (8 hilos lógicos), JDK 21.0.12, H2 2.3.232 en memoria (`MODE=PostgreSQL`), Spring Boot 4.0.0. El cliente de carga corría en la misma máquina. Accounting, simulado.

**k6 no está instalado en esta máquina y no se corrió.** Para el tramo HTTP se usó un script descartable de Node con los mismos ocho casos y 120 conexiones simultáneas sin pausa, que calcula el percentil con el mismo método de interpolación lineal. No es k6: no reemplaza la corrida del script versionado.

## Resultados

**En proceso**, tres corridas por configuración:

| | P50 | P95 | Sentencias por consulta | …de reglas |
|---|---|---|---|---|
| Con caché | 0,4–0,7 ms | **2,1–3,2 ms** | 7,8 | 0 |
| Sin caché | 1,0–1,8 ms | **4,4–6,9 ms** | 10,6 | 2,1 |

**Por HTTP**, 120 conexiones durante 30 s, una vez calentada la JVM, tres corridas seguidas por configuración:

| | P95 de cada corrida |
|---|---|
| Con caché | 39 ms · 45 ms · 146 ms |
| Sin caché | 48 ms · 41 ms · 199 ms |

**Por HTTP con la JVM recién arrancada** (primera corrida, sin calentamiento): P95 de **801 ms** con caché y **659 ms** sin ella.

## Veredicto

- **En proceso, el P95 es 2 a 7 ms**, muy por debajo de 200 ms, con y sin caché.
- **Por HTTP y con la JVM caliente, el P95 típico es de 40 a 50 ms**, pero dos de las seis corridas dieron 146 y 199 ms (una al borde): hay ruido, y el cliente de carga compartía la máquina con el servidor.
- **Por HTTP y con la JVM fría, el P95 supera el límite por mucho** (660 a 800 ms). El umbral de 200 ms solo se cumple si el servicio ya está caliente; el script versionado lo evalúa después de un calentamiento y eso hay que tenerlo presente al leer su resultado.
- **La caché reduce el trabajo, no se nota en la latencia de esta base**: saca las 2,1 sentencias de reglas por consulta (26 % del total), pero con H2 en memoria cada sentencia cuesta microsegundos y la diferencia entre configuraciones por HTTP queda dentro del ruido. Con Postgres por red cada sentencia cuesta más y el efecto debería ser mayor; **eso no se midió**.

Por eso el criterio de 200 ms está **cumplido en estado estable en esta máquina y base, no certificado** para el entorno desplegado.

## Qué no mide

- **No es PostgreSQL ni la red:** H2 en memoria y todo en `localhost`. Es el piso, no la latencia real.
- **Accounting, simulado** (vidas fijas en el mock); en producción suma una llamada, atenuada por la caché de vidas de 30 s.
- **No pasa por el Gateway** ni por Courses.
- **Una sola réplica y un solo roadmap en la caché.** Con muchos roadmaps y cohortes más grandes cambia el patrón de aciertos.
- **Carga cerrada sin pausas:** 120 usuarios que repiten sin respirar saturan el servicio; la latencia sale de la cola, no del gate. Es el diseño de T-15.6 y se mantiene para comparar.
- **Las corridas no son una muestra estadística:** son pocas y en un portátil.

## Cuello de botella y propuesta

Con la caché, el gate sigue haciendo unas 8 sentencias por consulta (matrícula, nodo, unidad, nodos completados, lecturas, etc.): la caché de T-18.4 solo cubre las de estructura. Propuestas, sin tocar código productivo en esta tarea:

1. Repetir la medición contra el servicio desplegado con Postgres (`k6 run` del script versionado) antes de dar el criterio por certificado.
2. Evaluar un calentamiento al arrancar (consultas sintéticas en el readiness) para que el primer tráfico no pague el JIT.
3. Si Postgres muestra que las sentencias que quedan pesan, revisar cuáles se pueden resolver en lote.
