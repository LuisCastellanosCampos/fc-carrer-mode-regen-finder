# Tareas: coincidencias flexibles y enlaces de jugador

Cada tarea debe poder completarse en aproximadamente 20-30 minutos. Resolver y
aprobar las precisiones de alcance antes de implementar las reglas.

## Definir el alcance

- [ ] **T1. Cerrar las equivalencias y el contrato de URLs**
  - **SML:** SML-2 a SML-5.
  - **Hecho cuando:** La spec y el plan indican que se cubren las 57
    nacionalidades del CSV de ejemplo, definen las equivalencias disponibles,
    enumeran las 12 posiciones del CSV (`DC`, `DFC`, `ED`, `EI`, `LD`, `LI`,
    `MC`, `MCD`, `MCO`, `MD`, `MI`, `POR`) y sus alias ingleses, e indican cómo
    se representan y validan las dos URLs opcionales.

## Fecha de nacimiento

- [ ] **T2. Probar la coincidencia por día y mes**
  - **SML:** SML-1.
  - **Hecho cuando:** Los tests distinguen mismo día/mes con año igual o
    distinto, día distinto y mes distinto.

- [ ] **T3. Comparar la fecha sin tener en cuenta el año**
  - **SML:** SML-1.
  - **Hecho cuando:** La búsqueda compara día y mes, mantiene el contrato HTTP
    actual y pasan los tests de T2.

## Nacionalidad

- [ ] **T4. Probar la normalización de nacionalidad**
  - **SML:** SML-2.
  - **Hecho cuando:** Los tests cubren mayúsculas, espacios, acentos, alias
    español/inglés y dos nacionalidades que no deben coincidir.

- [ ] **T5. Normalizar texto de nacionalidad**
  - **SML:** SML-2.
  - **Hecho cuando:** La comparación ignora mayúsculas, espacios repetidos y
    acentos sin equiparar nombres diferentes por similitud parcial.

- [ ] **T6. Añadir equivalencias español/inglés del catálogo**
  - **SML:** SML-2.
  - **Hecho cuando:** Las 57 nacionalidades del CSV tienen las equivalencias
    acordadas en T1 y cada equivalencia queda cubierta por un test.

## Posición

- [ ] **T7. Probar posiciones múltiples y códigos completos**
  - **SML:** SML-3.
  - **Hecho cuando:** Los tests comprueban `MC,MCO` con `MC`, `MCO` y
    `MC,MCO`, y comprueban que `MCO` no coincide con `MC`.

- [ ] **T8. Comparar posiciones separadas por comas**
  - **SML:** SML-3.
  - **Hecho cuando:** Se separan y recortan los códigos antes de comparar; las
    posiciones distintas siguen en los resultados como no coincidentes.

- [ ] **T9. Añadir equivalencias de códigos de posición**
  - **SML:** SML-3.
  - **Hecho cuando:** Se aplican los alias ingleses/españoles definidos en T1
    como códigos completos y pasan los tests de posición.

## URLs del jugador

- [ ] **T10. Añadir URLs opcionales al jugador y al contrato de catálogo**
  - **SML:** SML-4.
  - **Hecho cuando:** El payload de catálogo acepta `image_url` y `sofifa_url`
    opcionales, conserva compatibilidad con payloads antiguos y pasa los tests
    del contrato.

- [ ] **T11. Guardar URLs en SQLite**
  - **SML:** SML-4.
  - **Hecho cuando:** SQLite conserva las URLs al guardar y leer jugadores, y
    una base anterior se abre sin perder sus registros.

- [ ] **T12. Devolver URLs desde la búsqueda**
  - **SML:** SML-4.
  - **Hecho cuando:** `GET /api/v1/regens` devuelve ambas propiedades con su
    valor o `null`, y sus tests comprueban ambos casos.

- [ ] **T13. Importar URLs desde el CSV de ejemplo**
  - **SML:** SML-4.
  - **Hecho cuando:** El CSV incluye los valores de `image` y `url` del origen
    como `image_url` y `sofifa_url`, y el script los envía a la API.

## Frontend

- [ ] **T14. Mostrar la imagen del jugador**
  - **SML:** SML-5.
  - **Hecho cuando:** La tarjeta muestra la imagen con texto alternativo y
    mantiene una presentación válida si falta la URL o falla la carga.

- [ ] **T15. Enlazar la ficha de Sofifa**
  - **SML:** SML-5.
  - **Hecho cuando:** La tarjeta muestra un enlace accesible cuando hay URL y lo
    abre en otra pestaña con `rel="noopener noreferrer"`.

- [ ] **T16. Probar datos opcionales en las tarjetas**
  - **SML:** SML-5.
  - **Hecho cuando:** Los tests de Angular cubren imagen disponible, imagen
    ausente o fallida, enlace disponible y enlace ausente.

## Verificación final

- [ ] **T17. Ejecutar las pruebas de backend y frontend**
  - **SML:** SML-1 a SML-5.
  - **Hecho cuando:** `python -m pytest -q` desde la raíz y `ng test
    --watch=false` desde `FRONTEND` terminan correctamente.
