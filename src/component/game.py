from dataclasses import dataclass, field
from email.policy import default
from enum import Enum
from typing import Optional


class Player(Enum):
    P1 = ("p1", "X")
    P2 = ("p2", "O")
    NONE = ("none", " ")

    @property
    def name(self) -> str:
        return self.value[0]

    @property
    def symbol(self) -> str:
        """
        They symbol to display on the board for this piece owner.
        """
        return self.value[1]


# alias Player as P
P = Player


@dataclass
class Game:
    _chaining_cell_name: Optional[str] = None
    _current_player: P = field(default=P.P1)
    turn_counter: int = field(default=0)
    _is_chained_move: bool = field(default=False)
    _is_game_over: bool = field(default=False)
    _winner: Optional[P] = None

    @property
    def chaining_cell_name(self):
        return self._chaining_cell_name

    @chaining_cell_name.setter
    def chaining_cell_name(self, value: str):
        self._chaining_cell_name = value

    @chaining_cell_name.deleter
    def chaining_cell_name(self):
        self._chaining_cell_name = None

    @property
    def current_player(self):
        return self._current_player

    @current_player.setter
    def current_player(self, value: P):
        self._current_player = value

    @property
    def is_chained_move(self):
        return self._is_chained_move

    @is_chained_move.setter
    def is_chained_move(self, value: bool):
        self._is_chained_move = value

    @property
    def is_game_over(self) -> bool:
        return self._is_game_over

    @is_game_over.setter
    def is_game_over(self, value: bool):
        self._is_game_over = value

    @property
    def winner(self) -> Player:
        return self._winner

    @winner.setter
    def winner(self, value: P):
        self._winner = value

    def toggle_player_turn(self) -> None:
        if not self.is_chained_move:
            self.current_player = P.P2 if self.current_player == P.P1 else P.P1
            self.turn_counter += 1

    # todo move to player?
    def set_player_manually(self, player: P) -> None:
        """
        Utility method to manually setting current player.

        Not for normal gameplay with "automatic" toggle.
        """
        if player == P.P1.name:
            self.current_player = P.P1
        else:
            self.current_player = P.P2
