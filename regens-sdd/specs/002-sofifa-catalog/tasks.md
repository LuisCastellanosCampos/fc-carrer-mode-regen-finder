# Tareas definitivas: integración del catálogo Sofifa

- [x] **T1. Aprobar el alcance de la fuente Sofifa**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** la especificación y el plan fijan la fuente anual única, la temporada soportada, el límite de extracción, el manejo de errores y que la API no consulta Sofifa en tiempo real ni se gestionan fuentes simultáneas.

- [x] **T2. Fijar la versión y dependencias del scraper**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** se documenta la versión o commit del scraper, sus dependencias `requests` y `parsel`, la licencia, los límites de páginas y el procedimiento reproducible sin credenciales ni cambios sin trazabilidad.

- [x] **T3. Definir el contrato de datos del scraper**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** existe un contrato versionado para el formato de entrada (`json` o `csv`) y el mapeo explícito de `id`, `name`, `birth_date`, `nationality`, `position`, `overall`, `age` y `season` hacia `Player`, incluyendo campos ausentes, posiciones múltiples y fechas no interpretables.

- [x] **T4. Implementar el adaptador de ejecución Sofifa**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** un adaptador local ejecuta el scraper con temporada y límite configurables, guarda el artefacto original en `data/raw/<season>/` y devuelve errores controlados sin modificar el catálogo.

- [x] **T5. Implementar transformación y validación del artefacto**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** los registros válidos producen `Player` y los incompletos, inválidos, ambiguos o duplicados se rechazan antes de cualquier actualización del catálogo.

- [x] **T6. Implementar la persistencia local con SQLite**
  - **RF:** RF-1, RF-2, RF-7
  - **Hecho cuando:** SQLite implementa `CatalogPort`, usa una ruta configurable, conserva los campos de `Player` y reemplaza los datos de forma atómica sin depender de FastAPI ni del scraper.

- [x] **T7. Conectar la API con el catálogo SQLite**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** la composición local usa SQLite en lugar de memoria, la importación valida la colección y la envía mediante el contrato existente, y la API consulta el catálogo persistido, no Sofifa.

- [x] **T8. Probar el pipeline, la validación y la persistencia**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** hay tests para respuesta vacía, fallo de red, error HTTP, campos faltantes, fecha inválida, posiciones múltiples, IDs duplicados, importación fallida sin alterar el catálogo y recuperación tras recrear la aplicación.

- [ ] **T9. Documentar la operación anual local**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** el README explica cómo obtener el scraper fijado, instalar sus dependencias, ejecutarlo con límites responsables, revisar el artefacto en `data/raw/`, importar la temporada en `data/catalog.db` y repetir la operación sin duplicar datos; los artefactos generados y la base local quedan fuera de Git.
