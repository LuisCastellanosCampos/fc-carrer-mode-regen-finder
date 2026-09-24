import json
from pathlib import Path


FRONTEND_DIR = Path(__file__).parents[2] / "FRONTEND"


def test_angular_development_server_uses_fastapi_proxy() -> None:
    angular_config = json.loads((FRONTEND_DIR / "angular.json").read_text())
    serve_options = angular_config["projects"]["regen-finder-frontend"]["architect"]["serve"]

    assert serve_options["configurations"]["development"]["proxyConfig"] == "proxy.conf.json"

    proxy = json.loads((FRONTEND_DIR / "proxy.conf.json").read_text())

    assert proxy["/api"]["target"] == "http://127.0.0.1:8000"
    assert proxy["/api"]["secure"] is False