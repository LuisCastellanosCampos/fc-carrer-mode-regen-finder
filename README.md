# fc-carrer-mode-regen-finder
Buscador de regens para el Modo Carrera de EA FC | Career mode regen finder for EA FC.

Permite cruzar datos de fecha de nacimiento y nacionalidad para identificar las reencarnaciones de jugadores legendarios. | Allows crossing birth date and nationality data to identify the reincarnations of legendary players.

# Propósito del proyecto | Project Purpose
Este proyecto se está creando bajo la metodología **Spec-Driven Development (SDD)** para reforzar mis conocimientos en desarrollo de software con inteligencia artificial. | This project is being developed under the **Spec-Driven Development (SDD)** methodology to strengthen my software development skills with artificial intelligence.

# Tecnologías utilizadas | Technologies Used
**Backend** | Python 3.12+, FastAPI, Uvicorn, SQLite, Pydantic v2 |
**Frontend** | Angular, TypeScript, Reactive Forms, HttpClient |
**Testing** | pytest, httpx, Vitest mediante Angular CLI |

# Persistencia local del catálogo | Local Catalog Persistence

La API usa SQLite como almacenamiento local del catálogo anual. La base se guarda en `data/catalog.db` por defecto y puede configurarse inyectando un adaptador `CatalogPort` o pasando una ruta distinta a `SQLiteCatalog(path=...)`.

El adaptador mantiene el modelo `Player` completo (`id`, `name`, `birth_date`, `nationality`, `position`, `overall`, `age` y `season`) y reemplaza el contenido del catálogo de forma atómica, sin depender de FastAPI ni del scraper del catálogo.

## Operación anual del catálogo Sofifa

### Scraper fijado y entorno aislado

La referencia documentada para la extracción es [`sagunsh/sofifa-scraper`](https://github.com/sagunsh/sofifa-scraper), fijado al commit completo `1d43a18eaddcf97933d8aa921fb1ea66b9d68c5f` (sin versión etiquetada). Ese commit publica licencia MIT y fija `requests==2.31.0` y `parsel==1.7.0` en `requirements.txt`. Comprueba el commit antes de actualizar la referencia; no uses la rama `master` móvil como versión.

Desde PowerShell, clona el repositorio externo en una carpeta temporal y crea allí un entorno aislado. Ejecuta `git clone` solo la primera vez:

```powershell
$ScraperCommit = "1d43a18eaddcf97933d8aa921fb1ea66b9d68c5f"
$ScraperDir = Join-Path $env:TEMP "sofifa-scraper-1d43a18"
$VenvDir = Join-Path $env:TEMP "sofifa-scraper-venv"

git clone https://github.com/sagunsh/sofifa-scraper.git $ScraperDir
git -C $ScraperDir checkout --detach $ScraperCommit
py -m venv $VenvDir
$ScraperPython = Join-Path $VenvDir "Scripts\python.exe"
& $ScraperPython -m pip install -r (Join-Path $ScraperDir "requirements.txt")
```

El CLI de ese commit acepta años de 2007 a 2024, no 2025 ni 2026. No etiquetes una extracción de 2024 como una temporada posterior. Limita cada ejecución a un máximo de 50 páginas y no repitas extracciones innecesariamente; el scraper espera entre páginas.

### Extraer y revisar el artefacto original

En este ejemplo se extrae el año 2024. El archivo se conserva sin editar en `data/raw/2024/sofifa.json`; el scraper también admite CSV si se usa una extensión `.csv`.

```powershell
$Season = "2024"
$RawDir = Join-Path "data\raw" $Season
$Artifact = Join-Path $RawDir "sofifa.json"

New-Item -ItemType Directory -Force $RawDir | Out-Null
& $ScraperPython (Join-Path $ScraperDir "scrape_sofifa.py") `
    --year 2024 --max_pages 50 --filename $Artifact
if ($LASTEXITCODE -ne 0) {
    throw "Falló la extracción Sofifa; no importes el catálogo."
}

$Rows = Get-Content -Raw $Artifact | ConvertFrom-Json
"Registros extraídos: $($Rows.Count)"
$Rows | Select-Object -First 5 name, url, country, positions, overall, age |
    Format-Table -AutoSize
Get-FileHash $Artifact
```

Revisa el recuento, los campos, las fechas y el hash antes de importar. Una extracción vacía, incompleta o con datos inesperados se detiene y no se importa. El JSON externo no es directamente el cuerpo del endpoint: prepara una colección normalizada con `season`, `id`, `name`, `birth_date`, `nationality`, `position`, `overall` y `age`. Mapea `country` a `nationality` y `positions` a `position`; deriva el identificador estable del jugador y normaliza la fecha a `yyyy-MM-dd`. Rechaza campos ausentes, fechas inválidas, posiciones ambiguas e IDs repetidos.

**Límite de integración:** el repositorio no incluye un comando de importación que ejecute el scraper y normalice automáticamente su JSON. `SofifaRunner` valida y guarda un payload JSON ya obtenido, y `SofifaTransformer` valida filas que ya usan el contrato normalizado. Por tanto, no envíes el artefacto upstream directamente al endpoint: primero debes preparar y revisar el JSON del contrato. Si no puedes mapear un campo de forma inequívoca, detén la importación.

### Importar en SQLite y repetir con seguridad

Inicia FastAPI desde la raíz. Por defecto, la API usa `data/catalog.db`; no hace falta iniciar Sofifa durante las búsquedas:

```powershell
py -m uvicorn BACKEND.main:app --reload
```

Prepara el JSON normalizado para el endpoint existente, por ejemplo en `data/catalog-import-2024.json` (reemplaza el ejemplo por todos los registros revisados):

```json
{
  "season": "2024",
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

En otra terminal desde la raíz, importa la colección con `PUT /api/v1/players/catalog`:

```powershell
curl.exe --fail-with-body -X PUT `
    http://127.0.0.1:8000/api/v1/players/catalog `
    -H "Content-Type: application/json" `
    --data-binary "@data/catalog-import-2024.json"
```

Comprueba la respuesta `season`, `inserted` y `updated`. Si la validación falla o el servidor devuelve un error, no consideres completada la importación. Puedes verificar un jugador conocido consultando `GET /api/v1/regens` con su `birth_date` y `nationality`; SQLite conserva el catálogo al reiniciar la aplicación.

Si repites la importación con los mismos IDs, el upsert no crea duplicados: la respuesta esperada es `inserted: 0` y `updated` igual al número de IDs que ya existían. Los IDs nuevos se informan en `inserted`. Una repetición no borra jugadores existentes que no estén en el payload.

`data/` y `*.db` están excluidos de Git en `.gitignore`; por ello, el artefacto original, el JSON normalizado y `data/catalog.db` permanecen locales. No añadas esos ficheros al repositorio.

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
npm test -- --watch=false
npm run build
Pop-Location
```



# Licencia | License

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles. | This project is under the MIT License - check the LICENSE file for more details.
