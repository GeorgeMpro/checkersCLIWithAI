import pytest

from conftest import board_setup


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
    def test_piece_can_move_on_board(self):
        # put piece
        # move piece
        # asset new place
        # assert piece is not on last place
        pass

    # def test_player_one_moves_to_higher_index(self):

    # def test_player_one_piece_cannot_move_backwards(self):

    # todo
    ### test illegal moves
    # cannot step on non-empty cell
    # out of bounds
    # on existing piece
    # on existing piece blocked from behind
    # same player piece

    # todo
    ###test capture
    # can capture
    # can capture if free
    # cannot capture if not free
    # cannot capture same owner

# 4. play order
#   keeping track
#   switching
# 5. win lose draw conditions

# optional: add a pieces array/dict?
