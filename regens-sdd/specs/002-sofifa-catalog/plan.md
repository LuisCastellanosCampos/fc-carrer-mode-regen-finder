# Plan de implementación: catálogo Sofifa

## 1. Trazabilidad

Esta fase depende del MVP `001-regen-mvp` y cubre principalmente RF-1 y RF-2.
RF-7 se cubre en la persistencia cuando el catálogo local no está disponible.

| Área | Requisitos |
|---|---|
| Contrato y versión del scraper | SF-1, SF-5 |
| Ejecución y artefactos originales | SF-1 |
| Transformación y validación | SF-2 |
| Persistencia SQLite | SF-3 |
| Importación y composición | SF-4 |
| Operación y pruebas | SF-1 a SF-5 |

## 2. Flujo propuesto

1. Ejecutar manualmente el scraper fijado para una temporada y límite de páginas.
2. Guardar el JSON o CSV original sin modificar en `data/raw/<season>/`.
3. Transformar el artefacto a jugadores del dominio.
4. Validar toda la colección, incluidos tipos, fechas, rangos, ambigüedades e IDs.
5. Persistir mediante SQLite o enviar la colección validada al endpoint existente.
6. Consultar siempre el catálogo local desde FastAPI.

El scraper no se ejecutará dentro de una petición de búsqueda y no tendrá
acceso directo al puerto de consulta.

## 3. Fronteras arquitectónicas

- `domain` conserva `Player` y sus validaciones sin importar Sofifa, requests,
  parsel, SQLite ni FastAPI.
- `application` coordina la importación mediante puertos.
- Un adaptador externo ejecuta el scraper y conserva el artefacto original.
- Un transformador convierte el formato externo al modelo de dominio.
- Un adaptador SQLite implementa `CatalogPort`.
- FastAPI compone el catálogo local, pero no conoce detalles del scraper.

## 4. Decisiones técnicas pendientes de aprobación

Antes de implementar se deberá fijar:

- commit o versión exacta del scraper;
- formato de entrada y contrato de campos;
- temporada y límite máximo de páginas;
- ruta de SQLite y estrategia de migración;
- procedimiento de importación y política ante errores;
- exclusiones de Git para artefactos y base local.

## 5. Estrategia de pruebas

- Tests del adaptador de ejecución con respuesta vacía, error de red y error HTTP.
- Tests de transformación para campos válidos, ausentes, fechas inválidas,
posiciones múltiples y tipos incorrectos.
- Tests de duplicados, ambigüedades y atomicidad antes de persistir.
- Tests SQLite para creación, reemplazo atómico y recuperación tras recrear la
aplicación.
- Tests de composición para demostrar que FastAPI consulta SQLite y no Sofifa.
- Tests operativos para repetir una importación sin duplicar datos.
