---
tags: [presentacion, roadmap]
---

# 6. Del cofre al material

## Lo que decimos

«Estamos frente a un cofre dentro de la isla. Al abrirlo, el alumno accede al material de estudio asociado con ese nodo. La experiencia mantiene el contexto del mundo y muestra el recurso en una interfaz de lectura. Cuando termina, puede cerrar el panel y seguir el recorrido. Así el contenido aparece en el momento y el lugar en que el docente decidió incorporarlo.

El visor considera el tipo de recurso para decidir cómo ofrecerlo. Algunos contenidos se pueden previsualizar dentro de la interfaz; otros se abren en una pestaña o se descargan, según sus características. También hay tratamiento para enlaces de video externo compatibles. Para la demo vamos a mostrar un recurso preparado que permita ver cómo pasamos del objeto del mundo al material académico.

> [!info]- Detalle técnico: visor 2D
> `material-access` usa frame para HTML o `content-preview`, selecciona según metadatos y extensión y contempla video externo compatible. Ver `F/app/features/roadmap/ui/material-access/material-access.component.ts`.

Acá es importante distinguir dos conjuntos de archivos. Los modelos del barco, las torres, los caminos y otros elementos visuales son assets de la experiencia y forman parte del front. El material de estudio pertenece al ámbito de Courses. Roadmap conserva la vinculación con la actividad y consulta la información necesaria para que la persona autorizada pueda acceder.

> [!info]- Detalle técnico: materiales y assets
> Modelos GLB y glTF se copian con los assets del front (`_presentacion-src/fe/angular.json:38`). Courses usa storage compatible S3 con cliente y presigner (`_presentacion-src/tpi-course/src/main/java/ar/edu/utn/frc/tup/p4/configs/StorageConfig.java:19`), bucket por defecto `course-materials` (`_presentacion-src/tpi-course/src/main/resources/application.properties:154`); los enlaces externos son distintos (`_presentacion-src/tpi-course/src/main/java/ar/edu/utn/frc/tup/p4/entities/CourseContent.java:27`). Ver [[06-integracion-backoffice-courses]].

Esta separación nos permite combinar una presentación rica con la organización académica existente: el docente trabaja con recursos del curso y el estudiante los encuentra en el recorrido. Cada cofre, entonces, es una puerta de entrada al contenido, integrada a la navegación que acabamos de mostrar.

El recurso continúa siendo parte de la cursada y aparece integrado a nuestra experiencia.

**Transición:** «Después de estudiar y resolver actividades, aparece la otra gran pregunta: ¿cómo se refleja ese avance y cómo se compara dentro de la cursada?».»

## Qué se ve en pantalla
Abrir un cofre con material previamente probado; mostrar el panel y volver al mundo. Tener un recurso alternativo si una URL no responde.

## Preguntas probables

**¿Dónde viven los modelos 3D?** En assets del front; el hosting final puede incluir infraestructura adicional.

**¿Dónde se guardan los materiales del curso?** Los archivos usan almacenamiento compatible S3; la configuración del proyecto apunta a Garage y al bucket `course-materials`. Los enlaces externos no son archivos del bucket. Falta confirmar la configuración y el recurso efectivo de la demo.

**¿Todo material se ve embebido?** No; según tipo puede previsualizarse, abrirse en otra pestaña o descargarse.

**¿El visor es un libro 3D?** Es un panel de interfaz 2D superpuesto al mundo.

**¿Cualquier video externo se puede embeber?** No; se contemplan enlaces compatibles y depende del proveedor.
