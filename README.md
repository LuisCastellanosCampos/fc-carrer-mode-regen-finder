# FC Career Mode Regen Finder
Buscador de regens para el Modo Carrera de EA FC | A regen finder for EA FC Career Mode.

Permite buscar posibles regens comparando la fecha de nacimiento y la nacionalidad de los jugadores. | Finds possible regens by comparing players' birth dates and nationalities.

# Propósito del proyecto | Project Purpose
Este proyecto se está creando bajo la metodología **Spec-Driven Development (SDD)** para reforzar mis conocimientos en desarrollo de software con inteligencia artificial. | This project is being developed under the **Spec-Driven Development (SDD)** methodology to strengthen my software development skills with artificial intelligence.

# Tecnologías | Technologies

| Área / Area | Tecnologías / Technologies |
| --- | --- |
| Backend | Python 3.12+, FastAPI, Uvicorn, SQLite, Pydantic v2 |
| Frontend | Angular, TypeScript |
| Tests | pytest, httpx, Vitest (Angular CLI) |

# Persistencia local del catálogo | Local Catalog Persistence

La API guarda el catálogo anual en `data/catalog.db` y puede actualizarlo sin depender del scraper. | The API stores the yearly catalog in `data/catalog.db` and can update it without depending on the scraper.

## Actualizar el catálogo Sofifa | Updating the Sofifa Catalog

Para probar el proyecto sin usar el scraper, puedes importar el CSV de ejemplo [jugadores_importables.csv](examples/jugadores_importables.csv). Con la API en marcha, ejecuta desde la raíz: | To try the project without the scraper, you can import the example CSV [jugadores_importables.csv](examples/jugadores_importables.csv). With the API running, run this from the project root:

```powershell
py scripts/import_catalog.py
```

El script envía el CSV a la API, que guarda el catálogo en SQLite. | The script sends the CSV to the API, which stores the catalog in SQLite.

Si quieres obtener datos nuevos, puedes usar [sofifa-scraper](https://github.com/sagunsh/sofifa-scraper). El proyecto no convierte automáticamente sus datos al formato que espera la API. | To get new data, you can use [sofifa-scraper](https://github.com/sagunsh/sofifa-scraper). The project does not automatically convert its data to the format expected by the API.

# Instalación y ejecución local | Installation and Local Execution

Desde la raíz del proyecto, instala las dependencias del backend: | From the project root, install the backend dependencies:

```powershell
py -m pip install fastapi uvicorn httpx pytest
```

Para levantar la API localmente: | To start the local API:

```powershell
py -m uvicorn BACKEND.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`. | The API will be
available at `http://127.0.0.1:8000`.

Para levantar el frontend Angular, abre otra terminal desde la raíz del
proyecto y ejecuta: | To start the Angular frontend, open another terminal
from the project root and run:

```powershell
Push-Location FRONTEND
npm install
npm start
Pop-Location
```

La aplicación estará disponible en `http://localhost:4200`. | The application
will be available at `http://localhost:4200`.

La API y el frontend se ejecutan en puertos distintos. Durante el desarrollo,
Angular redirige las rutas `/api` a FastAPI mediante `FRONTEND/proxy.conf.json`.
También puedes probar la API directamente en `http://127.0.0.1:8000`. | The
API and frontend run on separate ports. During development, Angular forwards
`/api` routes to FastAPI through `FRONTEND/proxy.conf.json`. You can also test
the API directly at `http://127.0.0.1:8000`.

Para actualizar el catálogo anual, realiza una petición `PUT` a
`http://127.0.0.1:8000/api/v1/players/catalog` con el header
`Content-Type: application/json`. | To update the annual catalog, send a
`PUT` request to `http://127.0.0.1:8000/api/v1/players/catalog` with the
`Content-Type: application/json` header.

Body de la petición: | Request body:

```json
{
	"season": "2026",
	"players": [
		{
			"id": "p-1042",
			"name": "Alejandro Ruiz",
			"birth_date": "1998-04-12",
			"nationality": "Spain",
			"position": "ST",
			"overall": 87,
			"age": 24
		}
	]
}
```

Respuesta esperada: | Expected response:

```json
{
	"season": "2026",
	"inserted": 1,
	"updated": 0
}
```

## Búsqueda de posibles regens | Possible Regen Search

Para buscar coincidencias, realiza una petición `GET` a
`http://127.0.0.1:8000/api/v1/regens`. Los parámetros `birth_date` y
`nationality` son obligatorios; `position` es opcional. | To search for
matches, send a `GET` request to the same URL. `birth_date` and `nationality`
are required; `position` is optional.

Ejemplo con posición: | Example with position:

```text
GET /api/v1/regens?birth_date=1998-04-12&nationality=Spain&position=ST
```

Respuesta con coincidencias: | Response with matches:

```json
{
	"query": {
		"birth_date": "1998-04-12",
		"nationality": "Spain",
		"position": "ST"
	},
	"matches": [
		{
			"player": {
				"id": "p-1042",
				"name": "Alejandro Ruiz",
				"birth_date": "1998-04-12",
				"nationality": "Spain",
				"position": "ST",
				"overall": 87,
				"age": 24,
				"season": "2026"
			},
			"match": {
				"birth_date": true,
				"nationality": true,
				"position": true,
				"is_possible_regen": true,
				"message": "Posible regen: coinciden fecha de nacimiento, nacionalidad y posición."
			}
		}
	],
	"message": null
}
```

Si no hay coincidencias, la respuesta mantiene `200 OK` y devuelve una lista
vacía con un mensaje informativo: | When there are no matches, the response
is still `200 OK` and includes an empty list with an informative message:

```json
{
	"query": {
		"birth_date": "1998-04-12",
		"nationality": "Spain",
		"position": null
	},
	"matches": [],
	"message": "No se encontraron posibles regens."
}
```

### Códigos HTTP | HTTP Status Codes

- `200 OK`: operación correcta, incluso si no hay resultados. | Request completed, even if there are no results.
- `400 Bad Request`: datos ausentes, inválidos o duplicados. | Missing, invalid, or duplicate data.
- `409 Conflict`: temporada anterior a la ya guardada. | Season is older than the saved one.
- `503 Service Unavailable`: catálogo no disponible. | Catalog is unavailable.
- `500 Internal Server Error`: error inesperado del servidor. | Unexpected server error.

## Pruebas | Tests

Desde la raíz del proyecto, ejecuta los tests del backend: | From the project root, run the backend tests:

```powershell
py -m pytest -q
```

Para ejecutar los tests y compilar el frontend desde la raíz del proyecto: | To run the frontend tests and build it from the project root:

```powershell
Push-Location FRONTEND
npm test -- --watch=false
npm run build
Pop-Location
```



## Licencia | License

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles. | This project is under the MIT License - check the LICENSE file for more details.
