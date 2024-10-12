class Piece:
    def __init__(self, player: str):
        self.in_game = True
        self.player = player
        self.playable = True
        self.king = False

    def remove_from_game(self) -> None:
        self.in_game = False
        self.playable = False

    def is_king(self) -> bool:
        return self.king

    def set_king(self) -> None:
        self.king = True
