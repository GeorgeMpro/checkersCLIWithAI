import pytest
import board
import piece

from piece import Piece
from cell import Cell


@pytest.fixture
def board_setup():
    return board.Board()


@pytest.fixture
def piece_setup(request):
    # Default to 'p1' if no parameter is provided
    return piece.Piece(request.param if hasattr(request, 'param') else 'p1')


def put_piece_on_cell_and_return_cell(board_setup, cell_piece, row, column) -> Cell:
    board_setup.set_up_piece(row, column, cell_piece)
    cell = board_setup.get_cell(row, column)
    return cell


def setup_piece_on_cell_by_name_and_owner(board_setup, piece_owner, cell_name) -> Piece:
    cell = board_setup.get_cell_by_name(cell_name)
    piece = Piece(piece_owner)
    cell.set_piece(piece)
    return piece
