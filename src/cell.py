class Cell:
    def __init__(self, row, column):
        # generating an 8*8 matrix display a_ij, i,j=1,...,8
        # the +1 to start the values from 1 and not 0
        # [f"a{y + 1}{x + 1}" for x in range(rows)]
        self.name = f"a{row + 1}{column + 1}"
        self.color = "black" if (row + column) % 2 == 0 else "white"
        self.playable = True if (row + column) % 2 == 0 else False
