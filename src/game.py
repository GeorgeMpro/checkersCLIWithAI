from enum import Enum


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
        self.current_player = P.P1
        # todo
        self.is_capture_move_ = False
        self.is_chained_moved = False

    def get_turn(self) -> str:
        return self.current_player.name

    def toggle_whose_turn(self) -> None:
        if not self.is_chained_moved:
            self.current_player = P.P2 if self.current_player == P.P1 else P.P1
