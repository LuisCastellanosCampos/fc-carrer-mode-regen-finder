# Especificación: integración del catálogo Sofifa

## Alcance

Esta fase amplía el MVP para importar anualmente un catálogo de jugadores
activos desde Sofifa. Sofifa será la única fuente externa soportada para esta
fase. La importación se ejecutará de forma manual o programada, fuera del flujo
de búsqueda, y la API consultará únicamente el catálogo local validado.

La fase cubre RF-1 y RF-2 del MVP. No cambia las reglas de detección de regens ni
el contrato de búsqueda definido en `001-regen-mvp`.

## Requisitos funcionales

### SF-1. Ejecutar una extracción anual controlada

El sistema deberá ejecutar el scraper fijado para una temporada y un límite de
páginas configurables. La ejecución guardará el artefacto original en
`data/raw/<season>/` y no modificará el catálogo por sí misma.

La operación deberá ser manual o programable, nunca una dependencia de una
búsqueda ni una llamada en tiempo real desde FastAPI. No se gestionarán fuentes
simultáneas.

### SF-2. Transformar y validar el catálogo

El sistema deberá transformar cada registro de Sofifa al modelo `Player` del
MVP: `id`, `name`, `birth_date`, `nationality`, `position`, `overall`, `age` y
`season`.

Deberá convertir tipos, mapear `country` y `positions`, rechazar campos
obligatorios ausentes, fechas no interpretables, valores fuera de rango,
registros ambiguos y IDs duplicados antes de actualizar el catálogo.

### SF-3. Persistir el catálogo localmente

El sistema deberá ofrecer un adaptador SQLite compatible con `CatalogPort`,
con una ruta configurable por defecto `data/catalog.db`. La tabla conservará
los campos de `Player` y las sustituciones serán atómicas.

### SF-4. Importar mediante el contrato existente

La importación deberá enviar una colección validada a
`PUT /api/v1/players/catalog`, respetar la temporada y conservar el upsert y
la atomicidad definidos en el MVP. Una importación fallida no deberá modificar
el catálogo anterior.

### SF-5. Operar y repetir la importación

La documentación deberá explicar cómo obtener y ejecutar la versión fijada del
scraper, revisar el artefacto original, importar una temporada, comprobar el
resultado y repetir la operación sin duplicar registros.

## Restricciones y decisiones

- El scraper se fijará por commit o versión reproducible.
- Sus dependencias externas serán `requests` y `parsel`, con licencia y versión
documentadas.
- Se respetarán límites de páginas y peticiones responsables.
- No se incorporarán credenciales, artefactos generados ni bases locales al
repositorio.
- La aplicación no consultará Sofifa durante una búsqueda.
- Los identificadores y contratos técnicos estarán en inglés; la
 documentación operativa y los mensajes estarán en español.

## Criterios de aceptación

- Una extracción válida produce un artefacto original versionado por temporada.
- Una extracción fallida devuelve un error controlado y no altera el catálogo.
- Los registros incompletos, ambiguos, inválidos o duplicados se rechazan antes
de persistir.
- Un catálogo válido se puede importar por el endpoint existente.
- SQLite permite recuperar el catálogo después de recrear la aplicación.
- La repetición de una importación no crea duplicados.
- Las búsquedas siguen funcionando contra el catálogo local sin depender de
Sofifa.
