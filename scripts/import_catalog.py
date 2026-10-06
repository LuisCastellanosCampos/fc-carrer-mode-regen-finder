import csv
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "examples" / "jugadores_importables.csv"
API_URL = "http://127.0.0.1:8000/api/v1/players/catalog"


def load_payload(csv_path: Path = CSV_PATH) -> dict[str, object]:
    with csv_path.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise ValueError("El CSV no contiene jugadores.")

    return {
        "season": rows[0]["season"],
        "players": [
            {field: value for field, value in row.items() if field != "season"}
            for row in rows
        ],
    }


def main() -> None:
    try:
        payload = load_payload()
    except (OSError, ValueError, KeyError) as error:
        raise SystemExit(f"No se pudo leer el CSV: {error}") from error

    request = Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="PUT",
    )
    try:
        with urlopen(request) as response:
            print(response.read().decode("utf-8"))
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Error de la API ({error.code}): {detail}") from error
    except URLError as error:
        raise SystemExit(
            "No se pudo conectar con la API. Comprueba que está en ejecución."
        ) from error


if __name__ == "__main__":
    main()
