# Plan: coincidencias flexibles y enlaces de jugador

## Trazabilidad

Esta fase extiende la búsqueda y el contrato actual del catálogo. Sigue la
constitución del proyecto: la regla de coincidencia vive en el servicio de
aplicación y puede probarse sin FastAPI ni Angular.

| Área | Requisitos |
| --- | --- |
| Reglas de búsqueda | SML-1, SML-2, SML-3 |
| Catálogo y API | SML-4 |
| Tarjetas Angular | SML-5 |
| Pruebas y validación | SML-1 a SML-5 |

## Pasos

1. Añadir pruebas de dominio para día/mes, alias de nacionalidad y posiciones.
2. Implementar comparaciones normalizadas en el servicio de búsqueda, sin
   cambiar qué jugadores se devuelven por tener otra posición.
3. Añadir URLs opcionales al jugador, al endpoint del catálogo y a la respuesta
   de búsqueda.
4. Migrar SQLite de forma compatible, añadiendo las columnas opcionales cuando
   se inicializa una base existente.
5. Añadir las URLs del CSV de origen al CSV de ejemplo y actualizar el script de
   importación para conservarlas.
6. Mostrar la imagen con alternativa textual y el enlace de Sofifa en cada
   tarjeta.
7. Añadir pruebas para API, persistencia, importación y presentación.
8. Ejecutar `python -m pytest -q` y `ng test --watch=false`.

## Decisiones

- Las posiciones se dividen por comas y se comparan como códigos completos.
- Los códigos de posición se equiparan con sus traducciones españolas/inglesas
  conocidas; no se equiparan posiciones distintas como `MC` y `MCO`.
- Los nombres de nacionalidad se comparan con una lista de equivalencias en
  español e inglés para las nacionalidades del catálogo.
- Los enlaces serán opcionales para conservar compatibilidad con los payloads
  ya existentes. SQLite añade columnas nullable.
- El contrato JSON añade `image_url` y `sofifa_url`; no cambia los campos
  existentes.
