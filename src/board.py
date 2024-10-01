from cell import Cell


class Board:
    _rows = _columns = 8

    def __init__(self, rows=_rows, columns=_columns):
        self.rows = rows
        self.columns = columns
        self.board = [

            [Cell(y, x) for x in range(rows)]
            for y in range(columns)]

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
