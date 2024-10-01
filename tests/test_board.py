import pytest
import board

ROWS = COLUMNS = 8


@pytest.fixture
def board_setup():
    return board.Board()


class TestBoard:
    def test_has_valid_board(self, board_setup):
        actual_board_size = sum(len(row) for row in board_setup.get_board())
        assert len(
            board_setup.get_board()) == board_setup.get_column_size(), f"expected {board_setup.get_column_size()} but has {len(board_setup.get_board())}"
        assert all(len(row) == board_setup.get_column_size() for row in
                   board_setup.get_board()), f"expected each row to have {board_setup.get_column_size()} columns"
        assert actual_board_size == board_setup.get_board_size(), f"expected {board_setup.get_board_size()} cells but got {actual_board_size}"

    def test_cell_has_name(self, board_setup):
        assert board_setup.get_cell(0, 0).name == 'a11'

    @pytest.mark.parametrize("y, x",
                             [(y, x) for y in range(ROWS) for x in range(COLUMNS)])
    def test_has_valid_cells(self, y, x, board_setup):
        expected_value = f"a{y + 1}{x + 1}"
        cell = board_setup.get_cell(y, x)
        assert cell.name == expected_value, f"Expected {expected_value}, but got {cell.name}"

    def test_cell_has_color(self, board_setup):
        assert board_setup.get_cell(0, 0).color in ['black']
        assert board_setup.get_cell(0, 1).color in ['white']
        assert board_setup.get_cell(1, 0).color in ['white']
        assert board_setup.get_cell(1, 1).color in ['black']
        assert board_setup.get_cell(7, 7).color in ['black']

    def test_cell_determine_playable(self, board_setup):
        assert board_setup.get_cell(0, 0).playable is True
        assert board_setup.get_cell(0, 1).playable is False
        assert board_setup.get_cell(7, 7).playable is True
