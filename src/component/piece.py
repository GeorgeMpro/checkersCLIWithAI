from attr import dataclass


@dataclass
class Piece:
    player: str
    in_game: bool = True
    playable = True
    king = False

    def remove_from_game(self) -> None:
        self.in_game = False
        self.playable = False

    def is_king(self) -> bool:
        return self.king

    def set_king(self) -> None:
        self.king = True
