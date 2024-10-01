import pytest

ROWS = COLUMNS = 8


class Board:
    _rows = _columns = 8

    def __init__(self, rows=_rows, columns=_columns):
        self.rows = rows
        self.columns = columns
        self.board = [
            # generating a 8*8 matrix display a_ij, i,j=1,..,8
            # the +1 to start the values from 1 and not 0
            [f"a{y + 1}{x + 1}" for x in range(rows)]
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


@pytest.fixture
def board():
    return Board()


class TestBoard:
    def test_has_valid_board(self, board):
        actual_board_size = sum(len(row) for row in board.get_board())
        assert len(
            board.get_board()) == board.get_column_size(), f"expected {board.get_column_size()} but has {len(board.get_board())}"
        assert all(len(row) == board.get_column_size() for row in
                   board.get_board()), f"expected each row to have {board.get_column_size()} columns"
        assert actual_board_size == board.get_board_size(), f"expected {board.get_board_size()} cells but got {actual_board_size}"

    @pytest.mark.parametrize("y, x",
                             [(y, x) for y in range(ROWS) for x in range(COLUMNS)])
    def test_has_valid_cells(self, y, x, board):
        expected_value = f"a{y + 1}{x + 1}"
        assert board.get_cell(y, x) == expected_value, f"Expected {expected_value}, but got {board.get_cell(y, x)}"
