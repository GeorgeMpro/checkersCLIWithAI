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
