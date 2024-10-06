import pytest

import conftest
import piece
from piece import Piece

ROWS = COLUMNS = 8


def piece_placement_setup(board_setup, piece_setup, row=0, column=0):
    cell_piece = piece_setup
    cell = conftest.put_piece_on_board(board_setup, cell_piece, row, column)
    return cell, cell_piece


@pytest.fixture
def expected_game_start_display():
    with open('tests/expected_initial_board_setup_display.txt', 'r') as file:
        return file.read()


class TestBoard:
    def test_has_valid_board(self, board_setup):
        actual_board_size = sum(len(row) for row in board_setup.get_board())
        assert len(
            board_setup.get_board()) == board_setup.get_column_size(), f"expected {board_setup.get_column_size()} but has {len(board_setup.get_board())}"
        assert all(len(row) == board_setup.get_column_size() for row in
                   board_setup.get_board()), f"expected each row to have {board_setup.get_column_size()} columns"
        assert actual_board_size == board_setup.get_board_size(), f"expected {board_setup.get_board_size()} cells but got {actual_board_size}"


class TestCell:
    def test_cell_has_name(self, board_setup):
        assert board_setup.get_cell(0, 0).name == 'a11'

    @pytest.mark.parametrize("y, x",
                             [(y, x) for y in range(ROWS) for x in range(COLUMNS)])
    def test_has_valid_cells(self, y, x, board_setup):
        expected_value = f"a{y + 1}{x + 1}"
        cell = board_setup.get_cell(y, x)
        assert cell.name == expected_value, f"Expected {expected_value}, but got {cell.name}"

    @pytest.mark.parametrize("row,col,color",
                             [(0, 0, 'black'), (0, 1, 'white'), (1, 0, 'white'), (1, 1, 'black'), (7, 7, 'black')])
    def test_cell_has_color(self, board_setup, row, col, color):
        assert board_setup.get_cell(row, col).color in color

    @pytest.mark.parametrize("row, col,truth_value",
                             [(0, 0, True), (0, 1, False), (7, 7, True)]
                             )
    def test_cell_determine_playable(self, board_setup, row, col, truth_value):
        assert board_setup.get_cell(row, col).playable is truth_value

    @pytest.mark.parametrize("row, col",
                             [(0, 0), (1, 1), (2, 0)]
                             )
    def test_playable_cell_has_piece(self, board_setup, piece_setup, row, col):
        cell_piece = piece_setup
        cell = conftest.put_piece_on_board(board_setup, cell_piece, row, col)
        assert cell.piece is not None, "Expected cell to have a piece, but it does not."

    def test_non_playable_cell_cannot_setup_piece(self, board_setup, piece_setup):
        cell_piece = piece_setup
        cell = conftest.put_piece_on_board(board_setup, cell_piece, 0, 1)
        assert cell.piece is None, "Expected cell to not have a piece, but it does."

    def test_cell_can_remove_piece(self, board_setup, piece_setup):
        cell_piece = piece_setup
        cell = conftest.put_piece_on_board(board_setup, cell_piece, 0, 0)
        cell.remove_piece()
        assert cell.piece is None, "Expected cell to have a piece, but it does not."

    # todo clean?
    def test_cell_can_display_on_board(self, board_setup, piece_setup):
        cell_empty = board_setup.get_cell(0, 1)
        cell_piece = piece_setup
        cell_p1 = conftest.put_piece_on_board(board_setup, cell_piece, 0, 0)
        cell_p2 = conftest.put_piece_on_board(board_setup, Piece("p2"), 1, 7)
        assert cell_empty.display() == " ", "expected empty cell to display space"
        assert cell_p1.display() == "X", "expected p1 cell to display X"
        assert cell_p2.display() == "O", "expected p2 cell to display O"


class TestPiece:
    def test_piece_has_player(self, board_setup, piece_setup):
        cell_piece = piece_setup
        assert cell_piece.player is not None

    def test_piece_can_be_placed_and_played(self, board_setup, piece_setup):
        cell, cell_piece = piece_placement_setup(board_setup, piece_setup)
        cell.has_piece()
        assert cell_piece.in_game is True
        assert cell_piece.playable is True

    @pytest.mark.parametrize("set_player, expected_player",
                             [("p1", "p1"), ("p2", "p2")]
                             )
    def test_piece_can_have_different_owners(self, board_setup, piece_setup, set_player, expected_player):
        cell_piece = piece.Piece(set_player)
        assert cell_piece.player == expected_player

    def test_remove_piece_from_game(self, board_setup, piece_setup):
        cell, cell_piece = piece_placement_setup(board_setup, piece_setup)
        cell.remove_piece_from_game()
        assert cell_piece.in_game is not True

    def test_removed_piece_is_unplayable(self, board_setup, piece_setup):
        cell, cell_piece = piece_placement_setup(board_setup, piece_setup)
        cell.remove_piece_from_game()
        assert cell_piece.playable is False
