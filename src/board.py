from cell import Cell


class Board:
    _rows = _columns = 8

    def __init__(self, rows=_rows, columns=_columns):
        self.rows = rows
        self.columns = columns
        # generate an array
        self.board = [
            [Cell(y, x) for x in range(rows)]
            for y in range(columns)]
        # generate a dictionary for O(1) access
        self.cell_map = {cell.name: cell for row in self.board for cell in row}

    def get_cell(self, row, column):
        return self.board[row][column]

    def get_board(self):
        return self.board

    def get_board_size(self):
        return self.rows * self.columns

    def get_column_size(self):
        return self.columns

    def get_row_size(self):
        return self.rows

    def set_up_piece(self, row, column, piece):
        cell = self.get_cell(row, column)
        cell.set_piece(piece)

    def get_cell_by_name(self, name):
        return self.cell_map[name]
