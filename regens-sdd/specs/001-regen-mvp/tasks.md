# Tareas de implementación: Regen Finder MVP

Cada tarea está estimada para un máximo de 20-30 minutos. Deben ejecutarse en
el orden indicado y marcarse únicamente cuando se cumpla su criterio verificable.

## Decisiones y base del dominio

- [x] **T1. Resolver las dudas abiertas de la spec**
  - **RF:** RF-5, RF-6
  - **Hecho cuando:** La spec indica si la media mínima de 85 se aplica al candidato concreto y define el desempate completo posterior a media y edad.

- [x] **T2. Preparar la estructura del monorepo**
  - **RF:** RF-1 a RF-7
  - **Hecho cuando:** Existen las áreas separadas para dominio, aplicación, adaptadores, API, frontend y tests, sin dependencias del dominio hacia la interfaz o la persistencia.

- [x] **T3. Definir el modelo de jugador activo**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** El modelo contempla `id`, `name`, `birth_date`, `nationality`, `position`, `overall`, `age` y `season`, con sus restricciones documentadas.

- [x] **T4. Definir el modelo de resultado de coincidencia**
  - **RF:** RF-3, RF-4, RF-5, RF-6, RF-7
  - **Hecho cuando:** El resultado representa el jugador activo, los estados de coincidencia de fecha, nacionalidad y posición, el estado de posible regen y el mensaje en español.

- [x] **T5. Definir errores y puertos de aplicación**
  - **RF:** RF-1 a RF-7
  - **Hecho cuando:** Existen contratos para actualizar el catálogo, consultar jugadores y comunicar errores sin importar FastAPI, Angular ni la persistencia.

## Catálogo anual

- [x] **T6. Implementar la validación de jugadores**
  - **RF:** RF-2
  - **Hecho cuando:** Se rechazan ID, nombre, fecha, nacionalidad, media o edad ausentes o inválidos, y los errores identifican el campo en español.

- [x] **T7. Implementar la validación de colecciones**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** Se rechazan colecciones con IDs duplicados y se valida toda la colección antes de modificar el catálogo.

- [x] **T8. Implementar el adaptador de persistencia del catálogo**
  - **RF:** RF-1, RF-2, RF-7
  - **Hecho cuando:** El catálogo puede leerse y reemplazarse mediante el puerto definido, sin exponer detalles de persistencia al dominio.

- [x] **T9. Implementar la actualización anual mediante upsert**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** Los IDs nuevos se insertan, los existentes se actualizan y una colección inválida no deja ningún cambio aplicado.

- [x] **T10. Probar la actualización anual del catálogo**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** Los tests cubren carga inicial, inserción, actualización por ID, duplicados, datos inválidos y atomicidad ante errores.

## Detección de posibles regens

- [x] **T11. Implementar la normalización de datos de consulta**
  - **RF:** RF-3, RF-4
  - **Hecho cuando:** Las fechas se validan como fechas exactas, la nacionalidad y la posición se normalizan para comparar, y los valores vacíos se rechazan.

- [x] **T12. Implementar el cruce exacto por fecha y nacionalidad**
  - **RF:** RF-3
  - **Hecho cuando:** Solo se consideran posibles coincidencias los jugadores activos que coinciden en ambos datos; las coincidencias parciales quedan excluidas.

- [x] **T13. Implementar la posición opcional**
  - **RF:** RF-4
  - **Hecho cuando:** La consulta funciona sin posición, informa de coincidencia cuando se proporciona y conserva el resultado aunque la posición difiera.

- [x] **T14. Implementar el filtro de media mínima**
  - **RF:** RF-5
  - **Hecho cuando:** Los resultados con media inferior a 85 se excluyen y un jugador con media exactamente 85 se incluye, conforme a la decisión de T1.

- [x] **T15. Implementar la ordenación de coincidencias**
  - **RF:** RF-6
  - **Hecho cuando:** Las coincidencias se ordenan por media descendente, edad descendente y el criterio final aprobado en T1.

- [x] **T16. Implementar el caso sin coincidencias**
  - **RF:** RF-7
  - **Hecho cuando:** Una consulta sin resultados devuelve una lista vacía y un mensaje informativo en español.

- [x] **T17. Probar las reglas de detección**
  - **RF:** RF-3, RF-4, RF-5, RF-6, RF-7
  - **Hecho cuando:** Los tests cubren coincidencia exacta, coincidencia parcial, posición ausente o discrepante, umbral 85, ordenación, empates y lista vacía.

## API REST

- [x] **T18. Implementar el endpoint de actualización anual**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** `PUT /api/v1/players/catalog` acepta el payload definido, ejecuta el caso de uso y devuelve el resumen de inserciones y actualizaciones.

- [x] **T19. Implementar el endpoint de búsqueda**
  - **RF:** RF-3, RF-4, RF-5, RF-6, RF-7
  - **Hecho cuando:** `GET /api/v1/regens` acepta fecha, nacionalidad y posición opcional, y devuelve coincidencias ordenadas o lista vacía con mensaje.

- [x] **T20. Mapear errores y códigos HTTP**
  - **RF:** RF-1 a RF-7
  - **Hecho cuando:** La API devuelve los códigos `200`, `400`, `409`, `503` y `500` definidos, con mensajes en español y sin aplicar cambios parciales.

- [x] **T21. Probar el contrato REST**
  - **RF:** RF-1 a RF-7
  - **Hecho cuando:** Los tests de backend verifican payloads, parámetros opcionales, respuestas exitosas, errores de validación, catálogo no disponible y fallos inesperados.

## Frontend

- [ ] **T22. Implementar el formulario de búsqueda**
  - **RF:** RF-3, RF-4
  - **Hecho cuando:** La pantalla permite introducir fecha y nacionalidad obligatorias, posición opcional, y bloquea envíos con datos inválidos.

- [ ] **T23. Integrar cliente REST y estados de pantalla**
  - **RF:** RF-3, RF-4, RF-5, RF-6, RF-7
  - **Hecho cuando:** El frontend envía los parámetros correctos, muestra coincidencias y posición, respeta el orden recibido y presenta estados vacío, error y carga en español.

- [ ] **T24. Probar el frontend con ng test**
  - **RF:** RF-3, RF-4, RF-5, RF-6, RF-7
  - **Hecho cuando:** `ng test` verifica validación del formulario, posición opcional, construcción de la petición, resultados ordenados, lista vacía y errores HTTP.

## Verificación final

- [ ] **T25. Ejecutar la validación completa del MVP**
  - **RF:** RF-1 a RF-7
  - **Hecho cuando:** `pytest` y `ng test` terminan correctamente, cada RF tiene al menos un test asociado y se revisan los criterios de finalización de la spec.

## Integración del catálogo Sofifa

Estas tareas forman una fase posterior al MVP. Antes de implementarlas debe
aprobarse una ampliación de la spec y del plan que documente Sofifa como fuente
anual única del catálogo. El scraper no se ejecutará durante las búsquedas ni
será una dependencia de disponibilidad en tiempo real de la API.

- [ ] **T26. Aprobar el alcance de la fuente Sofifa**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** La spec y el plan definen la ejecución manual o programada
    de una importación anual, la temporada soportada, el comportamiento ante
    errores de Sofifa, los límites de peticiones y que no se gestionan fuentes
    simultáneas.

- [ ] **T27. Definir el contrato de datos del scraper**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** Existe un contrato versionado que identifica el formato
    de entrada (`json` o `csv`) y el mapeo explícito de ID, nombre, fecha de
    nacimiento, nacionalidad, posición, media, edad y temporada hacia `Player`,
    incluyendo campos ausentes, fechas no interpretables y posiciones múltiples.

- [ ] **T28. Fijar la versión y dependencias del scraper externo**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** El proyecto documenta el commit o versión de
    `sofifa-scraper`, sus dependencias `requests` y `parsel`, la licencia MIT,
    el límite de páginas y el procedimiento reproducible de ejecución sin
    incorporar credenciales ni modificar el scraper sin trazabilidad.

- [ ] **T29. Implementar el adaptador de ejecución Sofifa**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** Un adaptador o comando local ejecuta el scraper con la
    temporada y límite de páginas configurados, guarda el JSON o CSV original
    en `data/raw/<season>/`, devuelve un error controlado si falla y no modifica
    el catálogo por sí mismo.

- [ ] **T30. Implementar la transformación y validación del artefacto**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** El adaptador transforma `country` y `positions` a los
    campos del dominio, convierte los tipos, asigna la temporada y produce
    `Player` válidos; los registros incompletos, duplicados o ambiguos se
    rechazan antes de enviar cualquier actualización.

- [ ] **T31. Implementar la persistencia local con SQLite**
  - **RF:** RF-1, RF-2, RF-7
  - **Hecho cuando:** Existe un adaptador SQLite que implementa `CatalogPort`,
    crea o migra la tabla del catálogo en una ruta configurable como
    `data/catalog.db`, conserva los campos de `Player` y reemplaza los datos de
    forma atómica sin depender de FastAPI ni del scraper.

- [ ] **T32. Conectar la API con el catálogo SQLite**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** La composición local usa SQLite en lugar de memoria, la
    importación envía la colección validada a `PUT /api/v1/players/catalog`,
    respeta el control de temporada, conserva la atomicidad existente y la API
    consulta el catálogo persistido, no Sofifa.

- [ ] **T33. Probar el pipeline y la persistencia**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** Hay tests para el mapeo válido, campos faltantes, fecha
    inválida, posiciones múltiples, ID duplicado, respuesta vacía, fallo de
    red, error HTTP, garantía de que una importación fallida no altera el
    catálogo y recuperación del catálogo después de recrear la aplicación.

- [ ] **T34. Documentar la operación anual local**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** El README explica cómo obtener el scraper fijado, instalar
    sus dependencias, ejecutarlo con límites responsables, revisar el artefacto
    en `data/raw/`, importar la temporada en `data/catalog.db` y repetir la
    operación sin duplicar datos. Los artefactos generados y la base local no se
    incorporan al repositorio Git.