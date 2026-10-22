# T-44.4 - Flag roadmap por grupo

## Objetivo

T-44.4 publica el interruptor externo que reservará la activación del roadmap por grupo.
Esta tarea no implementa comportamiento funcional de grupos.

## Configuración

- Variable de entorno: `ROADMAP_BY_GROUP_ENABLED`.
- Property interna: `app.features.roadmap-by-group.enabled`.
- Valor por defecto: `false`.

Para dejar preparado el flag en un entorno:

```dotenv
ROADMAP_BY_GROUP_ENABLED=true
```

La configuración se enlaza al iniciar el contexto de Spring. Con el mecanismo actual, cambiar
la variable requiere reiniciar la aplicación para que el nuevo valor tenga efecto.

## Comportamiento actual

- Con `false`, Roadmap conserva exactamente su comportamiento actual.
- Con `true`, el alumno ve su recorrido y su avance filtrados por comisión (T-44.2): ver
  [`T-44-2-RECORRIDO-POR-COMISION.md`](T-44-2-RECORRIDO-POR-COMISION.md). Cada consulta lee las
  comisiones y las restricciones de Courses (T-10.2 y T-44.1).
- El staff sigue viendo el recorrido y el avance completos.
- El Gate rechaza con `group_restricted` un nodo cuya unidad no es de ninguna comisión del alumno,
  y el inicio de un desafío y el registro de una lectura responden `403` en ese caso (T-44.3).
- No se modifica el ranking, que es siempre de la cohorte (HU-45).
- No hay migraciones: XP, completados y lecturas siguen guardados por cohorte.
