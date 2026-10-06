# Especificación: coincidencias flexibles y enlaces de jugador

## Objetivo

Mejorar la búsqueda de posibles regens y mostrar datos útiles del jugador en
las tarjetas, manteniendo separadas las reglas de negocio, la API y Angular.

## Requisitos funcionales

### SML-1. Comparar fecha de nacimiento por día y mes

La búsqueda considerará coincidente una fecha cuando coincidan el día y el mes,
sin importar el año. La API conservará el formato de fecha actual.

### SML-2. Aceptar nacionalidades en español e inglés

La búsqueda comparará nacionalidades por su equivalencia en español o inglés,
sin distinguir mayúsculas, minúsculas ni acentos. Por ejemplo, `Spain` y
`España` representarán la misma nacionalidad. Las nacionalidades usadas en el
catálogo de ejemplo tendrán sus equivalencias documentadas mediante tests.

### SML-3. Comparar posiciones individuales y sus traducciones

Las posiciones separadas por comas se compararán individualmente. Una posición
del jugador coincidirá si es igual a alguna de las posiciones buscadas o si es
su equivalente en español/inglés. Por ejemplo, `MC,MCO` coincidirá con `MC`,
`MCO` y `MC,MCO`, pero `MCO` no coincidirá con `MC`. No se usarán coincidencias
parciales de texto.

### SML-4. Conservar los enlaces del jugador

El catálogo permitirá guardar de forma opcional la URL de imagen y la URL de la
ficha de Sofifa de cada jugador. El endpoint de búsqueda devolverá esos campos
cuando existan. Los catálogos guardados anteriormente seguirán funcionando sin
necesidad de volver a importarlos.

### SML-5. Mostrar imagen y ficha de Sofifa

Cada tarjeta mostrará la imagen del jugador cuando esté disponible y un enlace a
su ficha de Sofifa. Si falta la imagen o no se puede cargar, se mostrará una
alternativa textual. El enlace externo se abrirá en otra pestaña de forma segura.
Solo se permiten las imágenes y enlaces de jugador incluidos en los datos; no se
añaden otros recursos de terceros.

## Fuera de alcance

- Añadir idiomas distintos de español e inglés.
- Cambiar el formato de búsqueda HTTP o añadir endpoints.
- Filtrar resultados por posición: la posición seguirá siendo un indicador de
  coincidencia, sin eliminar los resultados que no coincidan.
- Añadir servicios, dependencias o recursos visuales externos adicionales.

## Criterios de aceptación

- Tests de dominio verifican fechas con el mismo día/mes y con años distintos.
- Tests verifican nacionalidades equivalentes, normalización de acentos y
  nacionalidades distintas.
- Tests verifican posiciones múltiples, alias español/inglés y que `MC` no
  coincida por texto parcial con `MCO`.
- Tests verifican la persistencia y respuesta de ambas URLs, incluida la lectura
  de una base previa sin esas columnas.
- Tests de Angular verifican la imagen, su alternativa cuando falta y el enlace
  accesible a Sofifa.
