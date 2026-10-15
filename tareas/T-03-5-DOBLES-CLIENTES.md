# T-03.5 — Dobles en memoria de los contratos de `clients/`

Plan de implementación de la tarea T-03.5 de **HT-03** (doble estable de los contratos de
integración, activado por perfil). Contexto funcional en `agent.md` §2.2 (Inventario), §4.1
(nunca micro a micro directo); contrato propuesto en `G10-CONTRATOS-v2 (1).md` §A.1.

> **Nota de vigencia:** este documento registra las decisiones históricas del doble. Los paths,
> DTOs, eventos y políticas funcionales provisionales quedaron reemplazados por
> `docs/contracts/accounting-roadmap-v1.md`. T-03.2 ya adaptó el puerto; las formas y pendientes
> descriptos debajo se conservan como historia y no son el contrato externo vigente.

> **Nota T-09.5 (#4354):** el doble `InMemoryInventoryClient` se eliminó; Inventario
> siempre va por HTTP y los escenarios usan `InventoryHttpScenario` (cliente real
> guionado). Lo que sigue debajo se conserva como historia.

> **Alcance de T-03.5**: implementación en memoria, determinista y sin red, de cada interfaz de
> `clients/` (`CoursesCatalogClient`, `InventoryClient`), activada por property `mode` en vez de
> perfil de Spring, para poder combinar un cliente real con un doble en la misma corrida.
> **Incluye** la interfaz `InventoryClient` (no existía: T-03.2 solo tiene la fila pendiente en
> `ESTRUCTURA.md`). **No incluye** el cliente HTTP real de Inventario: eso es T-03.2.

---

## 1. Qué ya existe

| Pieza | Dónde | Estado |
|---|---|---|
| Interfaz + cliente HTTP + caché del catálogo de Courses | `clients/courses` (T-03.4) | Hecho |
| Interfaz de Inventario | — | No existe: la crea esta tarea |
| Cliente HTTP real de Inventario | — | T-03.2, fuera de esta tarea |

## 2. Decisiones de diseño

### D-T035-01 — Activación por property `mode`, no por perfil de Spring

Se evaluaron perfil de Spring (`@Profile("stub")`) y property por cliente. Se elige **property**
(`app.clients.courses.mode`, `app.clients.inventory.mode`, valores `http`/`stub`) porque hoy
mismo hace falta la combinación asimétrica: Courses ya tiene cliente real (T-03.4) e Inventario
todavía no (T-03.2). Un perfil único obligaría a que los dos fueran reales o los dos falsos.

`ClientMode` es un enum compartido en `clients/` (`HTTP`, `STUB`). Cada `*Properties` lo valida
con `@NotNull`: un valor mal escrito falla al arrancar, no arma un `NoSuchBeanDefinitionException`
a mitad de camino.

### D-T035-02 — Datos deterministas por identificador, sin sembrar nada

El doble no arranca vacío ni necesita un seeder: cualquier UUID que se le consulte devuelve
siempre la misma respuesta, entre reinicios y sin coordinar IDs de antemano con quien lo consuma
(front, tests de integración, otro grupo). La semilla es un plegado XOR explícito de los bits del
UUID (`getMostSignificantBits() ^ getLeastSignificantBits()`), documentado para que la regla se
pueda verificar a mano, no un `Objects.hash` opaco.

- **Courses** (`InMemoryCoursesCatalogClient`): semilla por `contentId`. 1 de cada 4 materiales
  queda `DRAFT` (RF/HU-04 CA2: solo lo publicado se vincula), el resto `PUBLISHED`.
- **Inventario** (`InMemoryInventoryClient`): semilla por **`courseId` + `studentId`** plegados
  entre sí, porque vidas y XP son por curso (RF-REC-01): el mismo alumno da otro resultado en otro
  curso. `activeLives` cae en 0..3 (1 de cada 4 con 0 vidas → dispara `without_lives`/RF-REC-04) y
  `historicalLivesLost` en 0..2 (1 de cada 3 en cero → candidato a promoción, RF-RNK-05/12, y 2°
  criterio de desempate RF-RNK-11), independiente entre sí.

Se descartó un mapa sembrable (control total pero un ID no sembrado "no existe": rompe cualquier
prueba con IDs propios) y sembrado + overrides (más superficie sin necesidad hoy; se puede agregar
después si hace falta forzar un caso puntual, sin romper esta interfaz).

### D-T035-03 — El doble también simula la caída del servicio

Property `stub-unavailable` (default `false`) por cliente. En `true`, el doble lanza siempre la
excepción de indisponibilidad. Sirve para demostrar dos reglas de negocio que solo se ven cuando el
servicio externo falla:

- `CatalogUnavailableException`: un 503 de Courses **nunca** es "catálogo vacío" (ya documentado en
  `HttpCoursesCatalogClient`).
- La decisión histórica D-07 proponía convertir la caída en bloqueo funcional. El contrato v3 de
  T-15.1 ya no incluye `origen_no_disponible`: la caída permanece como error real 503. T-15.2 debe
  cerrar la política de caché y degradación sin inventar un nuevo `reason`.

### D-T035-04 — Forma provisional de `InventoryClient`

```java
public interface InventoryClient {
    StudentLives fetchLives(UUID courseId, UUID studentId);                          // REQ-WAL-01 + 02
    Map<UUID, StudentLives> fetchLivesBatch(UUID courseId, Collection<UUID> studentIds); // REQ-WAL-03
}

public record StudentLives(UUID courseId, UUID studentId,
                           int activeLives, int maximum, int historicalLivesLost) {
    public boolean hasLives()      { return activeLives > 0; }
    public boolean neverLostLife() { return historicalLivesLost == 0; }
}
```

- `fetchLives` trae REQ-WAL-01 (vigentes) y REQ-WAL-02 (histórico) **juntos**: el ranking necesita
  el histórico y el gate necesita las vigentes, separarlos duplicaría viajes por el Gateway.
- `neverLostLife()` se **deriva** de `historicalLivesLost`, no es un campo propio: el acta lo
  propone aparte, pero dos fuentes de verdad para el criterio de promoción es pedir una
  inconsistencia. Si la forma real trae el campo, se ignora al mapear.
- Ausente del mapa del batch = Inventario no conoce a ese alumno en ese curso. Que no responda es
  otra cosa y se señala con `InventoryUnavailableException`: mismas tres situaciones que ya
  documenta `CoursesCatalogClient` (presente / ausente / excepción), nunca degradar una a otra.
- Los paths y la forma JSON del cliente HTTP real (`GET .../lives`, `POST .../lives/batch`) **no
  se definen acá**: son propuesta del acta (§A.1), a confirmar con Inventario en T-03.2.

## 3. Archivos

```
src/main/java/com/utn/tpi/roadmap/clients/
├── ClientMode.java                          NUEVO — HTTP | STUB, compartido
├── courses/
│   ├── CoursesCatalogProperties.java        EDITADO — + mode, + stubUnavailable
│   ├── CoursesCatalogConfig.java            EDITADO — dos @Bean condicionados por mode
│   └── InMemoryCoursesCatalogClient.java    NUEVO
└── inventory/                               NUEVO (paquete completo)
    ├── InventoryClient.java                 interfaz
    ├── StudentLives.java                    record del contrato
    ├── InventoryUnavailableException.java   503, D-07
    ├── InventoryProperties.java             mode + stub-unavailable (sin campos de red aún)
    ├── InventoryConfig.java                 publica el doble; T-03.2 agrega el @Bean http
    └── InMemoryInventoryClient.java
```

## 4. Properties

```properties
##### Clientes externos (HT-03) #####
app.clients.courses.mode=${COURSES_CLIENT_MODE:http}
app.clients.courses.stub-unavailable=${COURSES_STUB_UNAVAILABLE:false}
# PENDIENTE (T-03.2): el cliente HTTP de Inventario todavía no existe; "stub" es el único modo
# con implementación. Cambiar el default a "http" cuando T-03.2 agregue el cliente real.
app.clients.inventory.mode=${INVENTORY_CLIENT_MODE:stub}
app.clients.inventory.stub-unavailable=${INVENTORY_STUB_UNAVAILABLE:false}
```

Cada doble loguea `WARN` al construirse (`"... en modo STUB: no usar en producción"`). No se agrega
un guard por perfil de producción porque su nombre sigue abierto (T-03.1, H6).

## 5. Fuera de alcance de T-03.5

- `HttpInventoryClient` real, con caché y degradación (mismo patrón que `HttpCoursesCatalogClient`)
  → **T-03.2**.
- `InventoryClient` quedó conectado a `GateService` en T-15.1 para producir `no_lives` sin acoplar
  el dominio al transporte. El cliente HTTP, token técnico, caché y degradación son T-15.2. La
  lista activa de razones queda definida por el acta del Gate de T-15.5.
- Consumir `LIVES_EXHAUSTED` / `LIVES_AVAILABLE` → el contrato y el topic ya están definidos en
  el acta Accounting ↔ Roadmap v1, pero su implementación no pertenece a esta tarea histórica.
- El `contentId` en el nodo (HU-04) → T-04.1, con su migración.
- Sin migraciones: los dobles no persisten nada.

## 6. Tests

- `InMemoryCoursesCatalogClientTest`: determinismo por `contentId`; todo ID existe; aparecen
  `DRAFT` y `PUBLISHED` en un lote conocido; lote vacío → mapa vacío sin excepción;
  `stub-unavailable=true` → `CatalogUnavailableException`.
- `InMemoryInventoryClientTest`: determinismo por (`courseId`, `studentId`); el mismo alumno en dos
  cursos puede diferir; `activeLives` siempre en 0..3; aparece al menos un caso sin vidas y uno con
  `neverLostLife()`; el batch coincide con las consultas individuales; batch vacío → mapa vacío;
  `stub-unavailable=true` → `InventoryUnavailableException` en ambos métodos.
- `CoursesCatalogConfigTest` / `InventoryConfigTest` (`ApplicationContextRunner`): `mode=stub`
  publica el doble, `mode=http` publica el real (Courses) o ningún bean (Inventario, porque el real
  no existe todavía), `mode` inválido no arranca el contexto.
- Se extiende `CoursesCatalogPropertiesTest` con los dos campos nuevos y un caso de `mode` inválido.

## 7. Mensaje para quien tome T-03.2 (cliente HTTP real de Inventario)

1. **La interfaz `InventoryClient` sigue siendo un puerto provisorio.** El contrato externo
   vigente separa disponibilidad, históricos y lotes bajo `/api/accounting`; ver
   `docs/contracts/accounting-roadmap-v1.md`. Las antiguas propuestas `/api/wallet/inventory/*`
   están obsoletas.
2. **REST y eventos son piezas distintas del mismo contrato.** El Gate usa
   `lives-availability`; Accounting publica `LIVES_EXHAUSTED` y `LIVES_AVAILABLE` en
   `accounting.ledger.events`. T-03.2 no debe inventar otro endpoint o nombre de evento.
3. **El token técnico de servicio tampoco está resuelto** (mismo `PENDIENTE` que ya tiene
   `HttpCoursesCatalogClient`, ver `docs/T-01-7-EUREKA-GATEWAY.md`). Dejar el mismo comentario en
   `HttpInventoryClient`.
4. **La degradación debe respetar el vocabulario v3 y el acta vigente.** Una caché vigente puede
   respaldar el Gate; sin ella, `InventoryUnavailableException` se propaga como error real 503.
   Nunca se traduce la falla a `no_lives`, `eligible=true` ni un `reason` inventado. El TTL es
   corto y configurable, pero su valor numérico se define en T-03.2.

## 8. Pasos

1. `clients/ClientMode.java`.
2. `clients/courses`: editar `CoursesCatalogProperties` (+ `mode`, + `stubUnavailable`),
   `InMemoryCoursesCatalogClient`, editar `CoursesCatalogConfig` (dos `@Bean` condicionados).
3. `clients/inventory`: `InventoryClient`, `StudentLives`, `InventoryUnavailableException`,
   `InventoryProperties`, `InMemoryInventoryClient`, `InventoryConfig`.
4. `messages.properties`: `error.inventory.unavailable`.
5. `application.properties`, `src/test/resources/application.properties`, `.env.example`: agregar
   las properties nuevas.
6. Tests (§6), incluida la actualización de `CoursesCatalogPropertiesTest` y
   `HttpCoursesCatalogClientTest` (constructor de `CoursesCatalogProperties` con dos campos más).
7. `mvn verify` local; actualizar `docs/ESTRUCTURA.md` y `README.md`.

Trazabilidad del PR: **HT-03 · T-03.5** · REQ-WAL-01/02/03 · D-07 · RF-REC-01/04 · RF-RNK-05/11/12
· RF-NFR-04 (excepción documentada) · HU-04 CA2.
