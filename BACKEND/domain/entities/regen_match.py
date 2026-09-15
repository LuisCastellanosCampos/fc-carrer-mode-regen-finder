from dataclasses import dataclass

from BACKEND.domain.entities.player import Player


@dataclass(frozen=True, slots=True)
class RegenMatch:
    """Proyección de lectura de un jugador y sus estados de coincidencia."""

    player: Player
    birth_date_matches: bool
    nationality_matches: bool
    position_matches: bool | None
    is_possible_regen: bool
    message: str

    def __post_init__(self) -> None:
        if not isinstance(self.player, Player):
            raise TypeError("El resultado debe representar un jugador activo")
        if type(self.birth_date_matches) is not bool:
            raise TypeError("La coincidencia de fecha debe ser booleana")
        if type(self.nationality_matches) is not bool:
            raise TypeError("La coincidencia de nacionalidad debe ser booleana")
        if self.position_matches is not None and type(self.position_matches) is not bool:
            raise TypeError("La coincidencia de posición debe ser booleana o nula")
        if type(self.is_possible_regen) is not bool:
            raise TypeError("El estado de posible regen debe ser booleano")
        if self.is_possible_regen and not (
            self.birth_date_matches and self.nationality_matches
        ):
            raise ValueError(
                "Un posible regen debe coincidir en fecha y nacionalidad"
            )
        if not isinstance(self.message, str) or not self.message.strip():
            raise ValueError("El mensaje no puede estar vacío")
