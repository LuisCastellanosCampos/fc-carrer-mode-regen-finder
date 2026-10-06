from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_readme_explains_sofifa_catalog_update() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

    required_readme_content = (
        "jugadores_importables.csv",
        "sin usar el scraper",
        "py scripts/import_catalog.py",
        "sofifa-scraper",
        "no convierte automáticamente",
        "data/catalog.db",
    )
    assert all(content in readme for content in required_readme_content)
    assert "data/" in gitignore.splitlines()
    assert "*.db" in gitignore.splitlines()
