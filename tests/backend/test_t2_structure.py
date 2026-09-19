import ast
from pathlib import Path


ROOT = Path(__file__).parents[2]

REQUIRED_DIRECTORIES = (
    "BACKEND/domain/entities",
    "BACKEND/domain/services",
    "BACKEND/domain/exceptions",
    "BACKEND/application/ports",
    "BACKEND/application/use_cases",
    "BACKEND/adapters/inbound/http",
    "BACKEND/adapters/outbound",
    "FRONTEND/src/app/core",
    "FRONTEND/src/app/features/regen",
    "FRONTEND/src/app/shared",
    "tests/backend",
    "tests/frontend",
)


def test_t2_creates_the_hexagonal_monorepo_areas() -> None:
    missing = [path for path in REQUIRED_DIRECTORIES if not (ROOT / path).is_dir()]

    assert not missing, f"Faltan áreas de T2: {', '.join(missing)}"


def test_domain_has_no_interface_or_persistence_dependencies() -> None:
    forbidden_modules = {"fastapi", "angular", "adapters", "persistence"}
    domain_files = (ROOT / "BACKEND" / "domain").rglob("*.py")

    violations = []
    for path in domain_files:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                imported = [(node.module or "").split(".")[0]]
            else:
                continue
            violations.extend(
                f"{path.relative_to(ROOT)}: {module}"
                for module in imported
                if module in forbidden_modules
            )

    assert not violations, "Dependencias prohibidas en domain: " + ", ".join(violations)
