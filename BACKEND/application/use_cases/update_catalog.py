from BACKEND.application.ports.catalog import CatalogPort
from BACKEND.application.ports.use_cases import CatalogUpdateResult, UpdateCatalogCommand
from BACKEND.domain.services.catalog_validation import validate_player_collection
from BACKEND.domain.exceptions.errors import CatalogConflictError


class UpdateCatalogService:
    """Actualiza el catálogo anual mediante reemplazo por identificador."""

    def __init__(self, catalog: CatalogPort) -> None:
        self._catalog = catalog

    def execute(self, command: UpdateCatalogCommand) -> CatalogUpdateResult:
        validated_players = validate_player_collection(command.players)
        current_players = self._catalog.read_players()
        current_seasons = {player.season for player in current_players if player.season}
        if current_seasons and command.season < max(current_seasons):
            raise CatalogConflictError(
                "La temporada del catálogo no puede ser anterior a la vigente"
            )
        current_by_id = {player.id: player for player in current_players}
        incoming_by_id = {player.id: player for player in validated_players}

        updated = sum(player_id in current_by_id for player_id in incoming_by_id)
        inserted = len(incoming_by_id) - updated

        replaced_ids = set(incoming_by_id)
        merged_players = tuple(
            incoming_by_id[player.id] if player.id in replaced_ids else player
            for player in current_players
        )
        existing_ids = {player.id for player in current_players}
        new_players = tuple(
            player for player in validated_players if player.id not in existing_ids
        )

        self._catalog.replace_players(merged_players + new_players)
        return CatalogUpdateResult(
            season=command.season,
            inserted=inserted,
            updated=updated,
        )