import pytest
import board
import piece


@pytest.fixture
def board_setup():
    return board.Board()


@pytest.fixture
def piece_setup(request):
    # Default to 'p1' if no parameter is provided
    return piece.Piece(request.param if hasattr(request, 'param') else 'p1')


def put_piece_on_board(board_setup, cell_piece, row, column):
    board_setup.set_up_piece(row, column, cell_piece)
    cell = board_setup.get_cell(row, column)
    return cell


def piece_placement_setup(board_setup, piece_setup, row=0, column=0):
    cell_piece = piece_setup
    cell = put_piece_on_board(board_setup, cell_piece, row, column)
    return cell, cell_piece


class TestBoardSetup:
    cell_names = [f"a{i}{j}" for i in range(1, 9) for j in range(1, 9)]
    player_one_initial_cells = [f"a{i}{j}" for i in range(1, 4) for j in range(1, 9) if (i + j) % 2 == 0]

    @pytest.mark.parametrize("cell_name", cell_names)
    def test_can_get_cell_by_name(self, board_setup, cell_name):
        cell = board_setup.get_cell_by_name(cell_name)
        assert cell.name == cell_name

    @pytest.mark.parametrize("cell_name", player_one_initial_cells)
    def test_board_player_one_setup(self, board_setup, piece_setup, cell_name):
        cell, cell_piece = piece_placement_setup(board_setup, piece_setup)
        assert cell.has_piece() is True
        assert cell.get_piece_owner() == 'p1'

    # todo
    # 1. inital setup
    #     3 rows with pieces
    #         from both sides
    # 2. legal moves
    #       on empty cell
    #       eating 1
    #       eating more than one
    # 3. illegal moves
    #       out of bounds
    #       on existing pieces
    #       eating piece blocked from behind
    #       eating same player piece
    # 4. play order
    #   keeping track
    #   switching
    # 5. win lose draw conditions
    # 6. display
#           display p1 as X
#           display p2 as O
#           display no piece as . or whatever

    #optional: add a pieces array/dict?
