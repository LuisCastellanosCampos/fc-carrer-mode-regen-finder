import sqlite3
from datetime import date
from pathlib import Path

from BACKEND.application.ports.catalog import CatalogPort
from BACKEND.domain.entities.player import Player
from BACKEND.domain.services.catalog_validation import validate_player_collection


class SQLiteCatalog(CatalogPort):
    """Adaptador local de catálogo persistente basado en SQLite."""

    def __init__(self, path: str | Path | None = None) -> None:
        if path is None:
            catalog_path = Path(__file__).resolve().parents[3] / "data" / "catalog.db"
        else:
            catalog_path = Path(path)

        self._path = catalog_path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _initialize(self) -> None:
        with sqlite3.connect(self._path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS players (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    birth_date TEXT NOT NULL,
                    nationality TEXT NOT NULL,
                    position TEXT NOT NULL,
                    overall INTEGER NOT NULL,
                    age INTEGER NOT NULL,
                    season TEXT NOT NULL
                )
                """
            )
            connection.commit()

    def read_players(self) -> tuple[Player, ...]:
        with sqlite3.connect(self._path) as connection:
            rows = connection.execute(
                """
                SELECT id, name, birth_date, nationality, position, overall, age, season
                FROM players
                ORDER BY rowid
                """
            ).fetchall()

        return tuple(
            Player(
                id=row[0],
                name=row[1],
                birth_date=date.fromisoformat(row[2]),
                nationality=row[3],
                position=row[4],
                overall=row[5],
                age=row[6],
                season=row[7],
            )
            for row in rows
        )

    def replace_players(self, players: tuple[Player, ...]) -> None:
        validated_players = validate_player_collection(players)
        with sqlite3.connect(self._path) as connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute("DELETE FROM players")
            if validated_players:
                connection.executemany(
                    """
                    INSERT INTO players (
                        id, name, birth_date, nationality, position, overall, age, season
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    [
                        (
                            player.id,
                            player.name,
                            player.birth_date.isoformat(),
                            player.nationality,
                            player.position,
                            player.overall,
                            player.age,
                            player.season,
                        )
                        for player in validated_players
                    ],
                )
            connection.commit()


SqliteCatalog = SQLiteCatalog
__all__ = ["SQLiteCatalog", "SqliteCatalog"]
