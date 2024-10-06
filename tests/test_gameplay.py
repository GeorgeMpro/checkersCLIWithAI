import pytest

from conftest import board_setup, piece_setup
from exceptions.cell_not_found_error import CellNotFoundError
from exceptions.illegal_move_error import IllegalMoveError
from piece import Piece


class TestBoardSetup:
    cell_names = [f"a{i}{j}" for i in range(1, 9) for j in range(1, 9)]
    p1_init = [(f"a{i}{j}", "p1") for i in range(1, 4) for j in range(1, 9) if (i + j) % 2 == 0]
    p2_init = [(f"a{i}{j}", "p2") for i in range((9 - 3), 9) for j in range(1, 9) if (i + j) % 2 == 0]
    init_cells = p1_init + p2_init

    @pytest.mark.parametrize("cell_name", cell_names)
    def test_can_get_cell_by_name(self, board_setup, cell_name):
        cell = board_setup.get_cell_by_name(cell_name)
        assert cell.name == cell_name

    @pytest.mark.parametrize("cell_name, expected_owner", init_cells)
    def test_board_can_setup_initial_players(self, board_setup, cell_name, expected_owner):
        board_setup.initial_setup()
        cell = board_setup.get_cell_by_name(cell_name)
        assert cell.has_piece() is not None, f"Cell {cell_name} should have a piece, but it is empty."
        assert cell.get_piece_owner() == expected_owner

    # todo del
    def test_can_print(self, board_setup):
        board_setup.initial_setup()
        print(f"\n{board_setup}")


def setup_piece_on_cell_by_name_and_owner(board_setup, owner, source_name):
    cell = board_setup.get_cell_by_name(source_name)
    piece = Piece(owner)
    cell.set_piece(piece)
    return piece


class TestMovingOnBoard:
    @pytest.mark.parametrize("source_name, target_name, owner",
                             [("a11", "a22", "p1"), ("a13", "a22", "p1"), ("a13", "a24", "p1"),
                              ("a82", "a71", "p2"), ("a82", "a73", "p2"), ("a88", "a77", "p2")]
                             )
    def test_piece_can_move_on_board(self, board_setup, piece_setup, source_name, target_name, owner):
        piece = setup_piece_on_cell_by_name_and_owner(board_setup, owner, source_name)
        assert board_setup.get_cell_by_name(source_name).piece == piece

        board_setup.move_piece(source_name, target_name)
        assert board_setup.get_cell_by_name(target_name).piece == piece
        assert board_setup.get_cell_by_name(source_name).piece is None

    @pytest.mark.parametrize("source_name, target_name,owner",
                             [("a22", "a11", "p1"), ("a22", "a13", "p1"), ("a24", "a13", "p1"),
                              ("a71", "a82", "p2"), ("a73", "a82", "p2"), ("a77", "a88", "p2")]
                             )
    def test_player_cannot_move_backwards(self, board_setup, piece_setup, source_name, target_name, owner):
        piece = setup_piece_on_cell_by_name_and_owner(board_setup, owner, source_name)
        assert board_setup.get_cell_by_name(source_name).piece == piece

        board_setup.move_piece(source_name, target_name)
        assert board_setup.get_cell_by_name(target_name).piece is None
        assert board_setup.get_cell_by_name(source_name).piece == piece

    @pytest.mark.parametrize("source_name, target_name,owner",
                             [("a11", "a1-1", "p1"), ("a11", "a199", "p1"), ("a11", "a182", "p1")]
                             )
    def test_piece_cannot_move_out_of_bounds(self, board_setup, piece_setup, source_name, target_name, owner):
        setup_piece_on_cell_by_name_and_owner(board_setup, owner, source_name)

        with pytest.raises(CellNotFoundError, match=f"Cell {target_name} not found"):
            board_setup.move_piece(source_name, target_name)

    @pytest.mark.parametrize("source_name, owner",
                             [("a-111", "p1"), ("a00", "p1"), ("a-1-1", "p1"), ("b11", "p2"), ("a99", "p2"),
                              ("a1", "p1")]
                             )
    def test_piece_cannot_setup_out_of_bounds(self, board_setup, piece_setup, source_name, owner):
        with pytest.raises(CellNotFoundError, match=f"Cell {source_name} not found"):
            setup_piece_on_cell_by_name_and_owner(board_setup, owner, source_name)

    @pytest.mark.parametrize("source_name, target_name, owner",
                             [("a11", "a11", "p1"), ("a22", "a22", "p1"), ("a24", "a24", "p1"),
                              ("a82", "a82", "p2"), ("a73", "a73", "p2"), ("a88", "a88", "p2")]
                             )
    def test_cannot_move_on_itself(self, board_setup, piece_setup, source_name, target_name, owner):
        setup_piece_on_cell_by_name_and_owner(board_setup, owner, source_name)

        with pytest.raises(IllegalMoveError, match="Cannot move to the same cell"):
            board_setup.move_piece(source_name, target_name)

    # todo cannot move on same owner

    # todo begin capture logic

    # todo
    @pytest.mark.skip
    @pytest.mark.parametrize("source_name, target_name, owner",
                             [("a11", "a22", "p1"), ("a13", "a22", "p1"), ("a13", "a24", "p1"),
                              ("a82", "a71", "p2"), ("a82", "a73", "p2"), ("a88", "a77", "p2")]
                             )
    def test_non_capture_move_is_one_cell(self, board_setup, piece_setup, source_name, target_name, owner):
        piece = setup_piece_on_cell_by_name_and_owner(board_setup, owner, source_name)
        assert board_setup.get_cell_by_name(source_name).piece == piece

        board_setup.move_piece(source_name, target_name)
        assert board_setup.get_cell_by_name(target_name).piece == piece
        assert board_setup.get_cell_by_name(source_name).piece is None
