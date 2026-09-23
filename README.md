# fc-carrer-mode-regen-finder
Buscador de regens para el Modo Carrera de EA FC | Career mode regen finder for EA FC.

Permite cruzar datos de fecha de nacimiento y nacionalidad para identificar las reencarnaciones de jugadores legendarios. | Allows crossing birth date and nationality data to identify the reincarnations of legendary players.

# Propósito del proyecto | Project Purpose
Este proyecto se está creando bajo la metodología **Spec-Driven Development (SDD)** para reforzar mis conocimientos en desarrollo de software con inteligencia artificial. | This project is being developed under the **Spec-Driven Development (SDD)** methodology to strengthen my software development skills with artificial intelligence.

# Tecnologías utilizadas | Technologies Used
**Backend** | Python 3.12+, FastAPI, Uvicorn, Pydantic v2 |
**Frontend** | Angular |
**Testing** | pytest, httpx |

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

La API y el frontend se ejecutan actualmente en puertos distintos. El cliente
Angular usa rutas relativas `/api`; la configuración del proxy local para
redirigirlas a FastAPI está planificada en las tareas T24 y T25. Hasta
completar esas tareas, la API puede probarse directamente en
`http://127.0.0.1:8000`. | The API and frontend currently run on different ports.
The Angular client uses relative `/api` routes; the local proxy configuration
to forward them to FastAPI is planned in tasks T24 and T25. Until those tasks
are complete, the API can be tested directly at `http://127.0.0.1:8000`.

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

- `200 OK`: operación correcta, incluso cuando la búsqueda no encuentra resultados.
- `400 Bad Request`: datos de entrada ausentes, inválidos o duplicados.
- `409 Conflict`: actualización con una temporada anterior a la vigente.
- `503 Service Unavailable`: catálogo no disponible para consultar.
- `500 Internal Server Error`: fallo inesperado del servidor.

## Tests

Desde la raíz del proyecto, ejecuta la suite del backend: | From the project
root, run the backend test suite:

```powershell
py -m pytest -q
```

Para ejecutar los tests del frontend desde la raíz del proyecto: | To run the
frontend tests from the project root:

```powershell
Push-Location FRONTEND
ng test --watch=false --no-progress
Pop-Location
```



# Licencia | License

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles. | This project is under the MIT License - check the LICENSE file for more details.
