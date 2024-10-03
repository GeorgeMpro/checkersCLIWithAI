class Piece:
    def __init__(self, player):
        self.in_game = True
        self.player = player
        self.playable = True

    def remove_from_game(self):
        self.in_game = False
        self.playable = False
