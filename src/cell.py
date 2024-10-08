from typing import Optional

from game import Player as P
from piece import Piece


class Cell:

    def __init__(self, row, column):

        self.name = f"a{row}{column}"
        # playable cells are black
        self.color = "black" if (row + column) % 2 == 0 else "white"
        self.playable = True if (row + column) % 2 == 0 else False
        self.piece = None

    def set_piece(self, piece: Optional[Piece]):
        if self.playable:
            self.piece = piece

    def remove_piece(self):
        self.set_piece(None)

    def remove_piece_from_game(self):
        piece = self.piece
        piece.remove_from_game()

    def has_piece(self) -> bool:
        return self.piece is not None

    def get_piece(self) -> Piece:
        return self.piece

    def get_piece_owner(self) -> str | None:
        if not self.has_piece():
            return None
        return self.piece.player

    def display(self) -> str:
        if self.has_piece():
            player = self.get_piece_owner()
            return P.P1.symbol if player == P.P1.name else P.P2.symbol
        return P.NONE.symbol

    def remove_piece_reference(self):
        self.piece = None
