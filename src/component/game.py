from enum import Enum
from typing import Optional


class Player(Enum):
    P1 = ("p1", "X")
    P2 = ("p2", "O")
    NONE = ("none", " ")

    @property
    def name(self):
        return self.value[0]

    @property
    def symbol(self):
        """
        They symbol to display on the board for this piece owner.
        """
        return self.value[1]


# alias Player as P
P = Player


class Game:
    def __init__(self):
        self.chaining_cell_name: Optional[str] = None
        self.current_player = P.P1
        # todo del capture move?
        # self.is_capture_move_ = False
        self.is_chained_moved = False

    def get_turn(self) -> str:
        """
        Return the current player's turn.
        """
        return self.current_player.name

    def toggle_whose_turn(self) -> None:
        if not self.is_chained_moved:
            self.current_player = P.P2 if self.current_player == P.P1 else P.P1

    def set_chained_move(self, has_chained: bool) -> None:
        self.is_chained_moved = has_chained

    def set_chaining_cell(self, chaining_cell) -> None:
        self.chaining_cell_name = chaining_cell

    def get_chaining_cell(self) -> str | None:
        return self.chaining_cell_name

    def remove_chaining_cell(self) -> None:
        self.chaining_cell_name = None

    def is_chained(self) -> bool:
        return self.is_chained_moved

    def set_player(self, player: P) -> None:
        """
        Utility method to manually setting current player.

        Not for normal gameplay with "automatic" toggle.
        """
        if player == P.P1.name:
            self.current_player = P.P1
        else:
            self.current_player = P.P2
