import pytest
from conftest import board_setup, piece_setup, setup_piece_on_cell_by_name_and_owner
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

        with pytest.raises(IllegalMoveError, match="Normal piece cannot move in opposite direction"):
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

    @pytest.mark.parametrize("source_name, target_name, owner",
                             [("a11", "a31", "p1"), ("a13", "a33", "p1"), ("a13", "a44", "p1"),
                              ("a82", "a62", "p2"), ("a84", "a64", "p2"), ("a82", "a75", "p2")]
                             )
    def test_non_capture_move_cannot_move_more_than_a_cell(self, board_setup, piece_setup, source_name, target_name,
                                                           owner):
        setup_piece_on_cell_by_name_and_owner(board_setup, owner, source_name)
        with pytest.raises(IllegalMoveError, match="Non capture move is a single cell distance."):
            board_setup.move_piece(source_name, target_name)


class TestCapture:
    @pytest.mark.parametrize("source_name, target_name, owner",
                             [("a11", "a22", "p1"), ("a13", "a24", "p1"), ("a13", "a24", "p1"),
                              ("a82", "a71", "p2"), ("a84", "a73", "p2"), ("a82", "a73", "p2")]
                             )
    def test_cannot_capture_same_owner(self, board_setup, piece_setup, source_name, target_name,
                                       owner):
        setup_piece_on_cell_by_name_and_owner(board_setup, owner, source_name)
        setup_piece_on_cell_by_name_and_owner(board_setup, owner, target_name)
        with pytest.raises(IllegalMoveError, match="Cannot capture same owner"):
            board_setup.move_piece(source_name, target_name)

    # todo check p2 logic
    @pytest.mark.parametrize("source ,src_owner ,target, tar_owner, expected_cell_after_capture",
                             [("a11", "p1", "a22", "p2", "a33"),
                              ("a13", "p1", "a22", "p2", "a31"),
                              ("a82", "p2", "a73", "p1", "a64"),
                              ("a84", "p2", "a73", "p1", "a62")
                              ])
    def test_can_capture_opponent(self, board_setup, piece_setup, source, src_owner, target, tar_owner,
                                  expected_cell_after_capture):
        # setup
        piece_in_starting_location = setup_piece_on_cell_by_name_and_owner(board_setup, src_owner, source)
        setup_piece_on_cell_by_name_and_owner(board_setup, tar_owner, target)
        board_setup.move_piece(source, target)

        # assert that the pieces are removed from given locations and is its new location after capturing opponent
        assert board_setup.get_cell_by_name(source).has_piece() is not True
        assert board_setup.get_cell_by_name(target).has_piece() is not True
        assert piece_in_starting_location == board_setup.get_cell_by_name(expected_cell_after_capture).piece

    @pytest.mark.parametrize("source ,src_owner ,target, tar_owner, expected_cell_after_capture",
                             [("a11", "p1", "a22", "p2", "a33"),
                              ("a13", "p1", "a22", "p2", "a31"),
                              ("a82", "p2", "a73", "p1", "a64"),
                              ("a84", "p2", "a73", "p1", "a62")
                              ])
    def test_cannot_capture_if_after_capture_destination_is_blocked(self, board_setup, piece_setup, source, src_owner,
                                                                    target, tar_owner,
                                                                    expected_cell_after_capture):
        # setup
        setup_piece_on_cell_by_name_and_owner(board_setup, src_owner, source)
        setup_piece_on_cell_by_name_and_owner(board_setup, tar_owner, target)
        setup_piece_on_cell_by_name_and_owner(board_setup, tar_owner, expected_cell_after_capture)

        # assert that the pieces are removed from given locations and is its new location after capturing opponent
        with pytest.raises(IllegalMoveError, match="Cannot capture if destination cell is blocked"):
            board_setup.move_piece(source, target)

    @pytest.mark.parametrize("source ,src_owner ,target, tar_owner ",
                             [("a22", "p1", "a31", "p2"),
                              ("a17", "p1", "a28", "p2"),
                              ("a82", "p2", "a71", "p1"),
                              ("a77", "p2", "a68", "p1",)
                              ])
    def test_cannot_capture_if_after_capture_destination_is_out_of_bounds(self, piece_setup, board_setup, source,
                                                                          src_owner, target, tar_owner, ):
        setup_piece_on_cell_by_name_and_owner(board_setup, src_owner, source)
        setup_piece_on_cell_by_name_and_owner(board_setup, tar_owner, target)

        with pytest.raises(CellNotFoundError, match="Cannot capture if after target cell out of bounds"):
            board_setup.move_piece(source, target)
