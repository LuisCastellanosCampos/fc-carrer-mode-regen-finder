from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_readme_documents_reproducible_sofifa_catalog_operation() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

    required_readme_content = (
        "sagunsh/sofifa-scraper",
        "1d43a18eaddcf97933d8aa921fb1ea66b9d68c5f",
        "requests==2.31.0",
        "parsel==1.7.0",
        "MIT",
        "--max_pages 50",
        "--year 2024",
        "data/raw/2024/sofifa.json",
        "PUT /api/v1/players/catalog",
        "data/catalog.db",
        "inserted",
        "updated",
    )
    assert all(content in readme for content in required_readme_content)
    assert "data/" in gitignore.splitlines()
    assert "*.db" in gitignore.splitlines()
