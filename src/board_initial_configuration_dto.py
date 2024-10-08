from dataclasses import dataclass


@dataclass
class BoardInitialConfigurationDTO:
    def __init__(self, board, rows, columns, game):
        self.board = board
        self.rows = rows
        self.columns = columns
        self.cell_map = {cell.name: cell for row in board.get_board() for cell in row}
        self.game = game
