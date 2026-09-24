# Tareas: integración del catálogo Sofifa

Estas tareas pertenecen a una fase posterior al MVP. No deben comenzar hasta
aprobarse la especificación y el plan de esta carpeta.

## Aprobación del alcance

- [ ] **S1. Aprobar el contrato de la fase Sofifa**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** `spec.md` y `plan.md` fijan fuente única, temporada,
    formato, límites, errores, operación fuera de búsquedas y ausencia de
    fuentes simultáneas.

- [ ] **S2. Fijar la versión y dependencias del scraper**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** Se documentan commit o versión, `requests`, `parsel`,
    licencia, límites de páginas y procedimiento reproducible sin credenciales.

## Extracción y transformación

- [ ] **S3. Definir el contrato de datos Sofifa**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** Se documenta el formato de entrada y el mapeo explícito
    de `id`, `name`, `birth_date`, `nationality`, `position`, `overall`, `age`
    y `season`, incluidos campos ausentes y posiciones múltiples.

- [ ] **S4. Implementar el adaptador de ejecución**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** Una ejecución local usa temporada y límite configurables,
    guarda el JSON o CSV original en `data/raw/<season>/` y devuelve errores
    controlados sin modificar el catálogo.

- [ ] **S5. Implementar transformación y validación**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** Los registros válidos producen `Player` y los
    incompletos, inválidos, ambiguos o duplicados se rechazan antes de importar.

## Persistencia e integración

- [ ] **S6. Implementar el adaptador SQLite**
  - **RF:** RF-1, RF-2, RF-7
  - **Hecho cuando:** SQLite implementa `CatalogPort`, usa una ruta configurable,
    conserva los campos de `Player` y reemplaza datos de forma atómica.

- [ ] **S7. Conectar la importación con el catálogo local**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** La colección validada se importa mediante el contrato
    existente, se respeta la temporada y FastAPI consulta SQLite, no Sofifa.

## Pruebas y operación

- [ ] **S8. Probar extracción y transformación**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** Hay tests para respuesta vacía, red, HTTP, campos
    faltantes, fecha inválida, posiciones múltiples, tipos e IDs duplicados.

- [ ] **S9. Probar persistencia y atomicidad**
  - **RF:** RF-1, RF-2, RF-7
  - **Hecho cuando:** Se verifica que una importación fallida no altera el
    catálogo y que SQLite recupera los datos tras recrear la aplicación.

- [ ] **S10. Documentar la operación anual**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** El README explica obtener el scraper, ejecutarlo con
    límites, revisar `data/raw/`, importar en SQLite y repetir sin duplicados;
    los artefactos y la base local quedan fuera de Git.




    ## Integración del catálogo Sofifa

Estas tareas forman una fase posterior al MVP. Antes de implementarlas debe
aprobarse una ampliación de la spec y del plan que documente Sofifa como fuente
anual única del catálogo. El scraper no se ejecutará durante las búsquedas ni
será una dependencia de disponibilidad en tiempo real de la API.

- [ ] **T28. Aprobar el alcance de la fuente Sofifa**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** La spec y el plan definen la ejecución manual o programada
    de una importación anual, la temporada soportada, el comportamiento ante
    errores de Sofifa, los límites de peticiones y que no se gestionan fuentes
    simultáneas.

- [ ] **T29. Definir el contrato de datos del scraper**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** Existe un contrato versionado que identifica el formato
    de entrada (`json` o `csv`) y el mapeo explícito de ID, nombre, fecha de
    nacimiento, nacionalidad, posición, media, edad y temporada hacia `Player`,
    incluyendo campos ausentes, fechas no interpretables y posiciones múltiples.

- [ ] **T30. Fijar la versión y dependencias del scraper externo**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** El proyecto documenta el commit o versión de
    `sofifa-scraper`, sus dependencias `requests` y `parsel`, la licencia MIT,
    el límite de páginas y el procedimiento reproducible de ejecución sin
    incorporar credenciales ni modificar el scraper sin trazabilidad.

- [ ] **T31. Implementar el adaptador de ejecución Sofifa**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** Un adaptador o comando local ejecuta el scraper con la
    temporada y límite de páginas configurados, guarda el JSON o CSV original
    en `data/raw/<season>/`, devuelve un error controlado si falla y no modifica
    el catálogo por sí mismo.

- [ ] **T32. Implementar la transformación y validación del artefacto**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** El adaptador transforma `country` y `positions` a los
    campos del dominio, convierte los tipos, asigna la temporada y produce
    `Player` válidos; los registros incompletos, duplicados o ambiguos se
    rechazan antes de enviar cualquier actualización.

- [ ] **T33. Implementar la persistencia local con SQLite**
  - **RF:** RF-1, RF-2, RF-7
  - **Hecho cuando:** Existe un adaptador SQLite que implementa `CatalogPort`,
    crea o migra la tabla del catálogo en una ruta configurable como
    `data/catalog.db`, conserva los campos de `Player` y reemplaza los datos de
    forma atómica sin depender de FastAPI ni del scraper.

- [ ] **T34. Conectar la API con el catálogo SQLite**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** La composición local usa SQLite en lugar de memoria, la
    importación envía la colección validada a `PUT /api/v1/players/catalog`,
    respeta el control de temporada, conserva la atomicidad existente y la API
    consulta el catálogo persistido, no Sofifa.

- [ ] **T35. Probar el pipeline y la persistencia**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** Hay tests para el mapeo válido, campos faltantes, fecha
    inválida, posiciones múltiples, ID duplicado, respuesta vacía, fallo de
    red, error HTTP, garantía de que una importación fallida no altera el
    catálogo y recuperación del catálogo después de recrear la aplicación.

- [ ] **T36. Documentar la operación anual local**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** El README explica cómo obtener el scraper fijado, instalar
    sus dependencias, ejecutarlo con límites responsables, revisar el artefacto
    en `data/raw/`, importar la temporada en `data/catalog.db` y repetir la
    operación sin duplicar datos. Los artefactos generados y la base local no se
    incorporan al repositorio Git.
