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

Para actualizar el catálogo anual, realiza una petición `PUT` a
`http://127.0.0.1:8000/api/v1/players/catalog` con el header
`Content-Type: application/json`. | To update the annual catalog, send a
`PUT` request to `http://127.0.0.1:8000/api/v1/players/catalog` with the
`Content-Type: application/json` header.

```

Respuesta esperada: | Expected response:

```json
{
	"season": "2026",
	"inserted": 1,
	"updated": 0
}
```


# Licencia | License

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles. | This project is under the MIT License - check the LICENSE file for more details.
