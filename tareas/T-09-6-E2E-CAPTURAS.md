# T-09.6 — E2E del perfil integrado y capturas (HU-40/HU-16)

Criterio: la prueba pasa en el entorno integrado sin ningún doble (alcance:
Inventario; el resto de los clientes se documenta donde no haya servicio real).

## 1. Prerrequisitos del entorno

1. Docker Desktop corriendo.
2. Modo `local`: clon de `tpi-system-compose` con la plataforma (Eureka, Gateway,
   Kafka) arriba y la red `tpi-roadmap` creada (ver `.tpi/platform/up.sh`).
   Modo `mesh`: Tailscale logueado en el host.
3. `.tpi/platform/.env` completo. Ojo: `APP_CLIENT_SECRET` viene vacío de ejemplo;
   pedirlo a Identidad, sin él las llamadas con token de servicio fallan (el propio
   `up.sh` lo avisa).
4. Cuentas de prueba de Users con 2FA (ver `docs/T-02-2-GUION-SPRINT-REVIEW.md`,
   "Antes de arrancar", paso 3): un profesor y un alumno inscripto **con ítems
   ya comprados en Accounting** (el e2e exige `items.size() > 0`), más un nodo
   desafío real para el Gate. Sin Bearer real no hay e2e.
5. Accounting reachable por el Gateway con `equip-summary` y `lives-availability`.

## 2. Levantar y verificar

```sh
cd .tpi/platform
./up.sh local        # o: ./up.sh mesh
./verify.sh local    # todo OK, en especial "gateway routes /api/roadmap/public/ping"
```

## 3. Correr el e2e

Suite `com.utn.tpi.roadmap.e2e.InventoryIntegratedE2ETest`: caja negra por Gateway
real, perfil `integrated`. En el `verify` normal se salta (flag ausente).

> El test es caja negra y no puede comprobar el perfil: levantar Roadmap con
> `SPRING_PROFILES_ACTIVE=prod,integrated` (local o mesh)
> para que el `IntegratedClientsValidator` exija todos los clientes en `http`.

```sh
./mvnw -B test "-Dtest=InventoryIntegratedE2ETest" \
  "-Droadmap.e2e=true" \
  "-Dgateway.url=http://localhost:8080" \
  "-De2e.student.token=<JWT alumno>" \
  "-De2e.service.token=<Bearer client_credentials>" \
  "-De2e.course.id=<course-cohorte>" \
  "-De2e.student.id=<uuid alumno>" \
  "-De2e.node.id=<uuid nodo desafío>"
```
(En PowerShell, `./mvnw` es `.\mvnw.cmd`.)

Escenarios: ping público por Gateway (200); inventario vigente con ítems reales y
campos snake (`student_id`, `item_effect`, `status`, `stale=false`); dos lecturas
consistentes (mismo `item_instance_id` y `status`); Gate prohibido al alumno
(401/403, solo servicio a servicio) y, con Bearer técnico, elegibilidad con
vocabulario cerrado (`eligible` booleano, `reason` nulo o del enum `GateReason`).
Sin alguna property, el escenario se aborta, no falla.

## 4. Evidencia (pegar salida de terminal al correr en integrado)

```text
(pendiente de corrida en entorno integrado)
```

## 5. Qué NO cubre este e2e

- Caída de Accounting en integrado (requiere tumbar el servicio a propósito;
  la degradación 503/stale está cubierta en unitarios y BDD).
- Carga (T-15.6, fixture local con k6).
- Los otros 5 clientes con stub (Courses, Motor…): dependen de sus equipos;
  el validador del perfil `integrated` los exige en `http` cuando estén.
