from dataclasses import dataclass, field
from typing import Optional

from .game import Player as P
from .piece import Piece


@dataclass
class Cell:
    _name: str = field(init=False)
    row: int
    column: int
    color: str = field(init=False)
    playable: bool = field(init=False)
    piece: Optional[Piece] = None
    king: bool = False

    def __post_init__(self):
        self.color = "black" if (is_black := (self.row + self.column) % 2 == 0) else "white"
        self.playable = is_black
        self._name = f"a{self.row}{self.column}"

    @property
    def name(self) -> str:
        return self._name

    def __str__(self):
        return f"Cell(name={self.name},  piece={self.piece})"

    def set_piece(
            self, piece: Optional[Piece]
    ) -> None:
        """Place a piece in the cell if playable."""
        if self.playable:
            self.piece = piece

    def remove_piece(self) -> None:
        self.set_piece(None)

    def remove_piece_from_game(self) -> None:
        piece = self.piece
        piece.remove_from_game()

    def has_piece(self) -> bool:
        return self.piece is not None

    def get_piece(self) -> Piece:
        return self.piece

    # todo walrus?
    def get_piece_owner(self) -> str | None:
        if not self.has_piece():
            return None
        return self.piece.player

    def display(self) -> str:
        if self.has_piece():
            player = self.get_piece_owner()
            return P.P1.symbol if player == P.P1.name else P.P2.symbol
        return P.NONE.symbol

    def remove_piece_reference(self) -> None:
        self.piece = None

    def is_king(self) -> bool:
        return self.piece is not None and self.piece.is_king()

    def set_king(self):
        self.piece.set_king()
