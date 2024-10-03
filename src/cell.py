class Cell:

    def __init__(self, row, column):
        """"
        generating an 8*8 matrix display a_ij, i,j=1,...,8
         the +1 to start the values from 1 and not 0
         [f"a{y + 1}{x + 1}" for x in range(rows)]
        """
        self.name = f"a{row + 1}{column + 1}"
        self.color = "black" if (row + column) % 2 == 0 else "white"
        self.playable = True if (row + column) % 2 == 0 else False
        self.piece = None

    def set_piece(self, piece):
        if self.playable:
            self.piece = piece

    def remove_piece(self):
        self.set_piece(None)

    def remove_piece_from_game(self):
        piece = self.piece
        piece.remove_from_game()

    def has_piece(self):
        return self.piece is not None

    def get_piece_owner(self):
        return self.piece.player

    def display(self):
        if self.has_piece():
            player = self.get_piece_owner()
            return "X" if player == "p1" else "O"
        return ""
