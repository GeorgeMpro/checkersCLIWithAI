import sys
from io import StringIO

import pytest

from ai.heuristic_explorer import HeuristicExplorer
from board import Board
from component import piece
from component.cell import Cell
from component.game import P
from component.piece import Piece

p1 = P.P1.name
p2 = P.P2.name


@pytest.fixture
def board_setup():
    return Board()


@pytest.fixture
def board(board_setup) -> Board:
    """board_setup alias"""
    return board_setup


@pytest.fixture
def heuristic_explorer(board_setup) -> HeuristicExplorer:
    return HeuristicExplorer(board_setup)


@pytest.fixture
def hs(heuristic_explorer) -> HeuristicExplorer:
    """heuristic_explorer alias"""
    return heuristic_explorer


@pytest.fixture
def piece_setup(request):
    # Default to 'p1' if no parameter is provided
    return piece.Piece(request.param if hasattr(request, 'param') else 'p1')


@pytest.fixture
def suppress_stdout(monkeypatch):
    """Fixture to suppress stdout messages from test."""
    monkeypatch.setattr(sys, "stdout", StringIO())


def put_piece_on_cell_and_return_cell(board_setup, cell_piece: Piece, row: int, column: int) -> Cell:
    board_setup.set_up_piece(row, column, cell_piece)
    cell = get_cell_by_index(board_setup, row, column)
    return cell


def get_cell_by_index(board_setup, row, column):
    cell = board_setup.cell_manager.get_cell_by_index(row, column)
    return cell


def setup_piece_on_cell_by_name_and_owner(board_setup, piece_owner: str, cell_name: str) -> Piece:
    cell = get_cell_by_name(board_setup, cell_name)
    piece = Piece(piece_owner)
    cell.set_piece(piece)
    return piece


def assert_player_turn_after_move(board_setup, src: str, target: str, expected_turn: str):
    board_setup.move_piece(src, target)
    actual_turn = board_setup.get_current_player_turn()
    assert actual_turn == expected_turn


def setup_board(
        board_setup, pieces: list[tuple[str, str]]
) -> None:
    """
    Helper function to set up the board with pieces.

    :param board_setup: The current board setup object.
    :param pieces: List of tuples in the format (piece_owner, cell_name).
    """
    for piece_owner, cell_name in pieces:
        setup_piece_on_cell_by_name_and_owner(board_setup, piece_owner, cell_name)


def get_cell_by_name(
        board_setup, cell_name
) -> Cell:
    return board_setup.cell_manager.get_cell_by_name(cell_name)


def get_valid_moves_for_given_cell(board_setup, cell):
    actual_moves = board_setup.cell_manager._get_valid_move_directions_for_cell(cell)
    return actual_moves


# AI
def setup_and_get_both_cells(
        board_setup: Board, cells: list[tuple[str, str]]
) -> tuple[list[Cell], list[Cell]]:
    setup_board(board_setup, cells)
    player_cells = board_setup.cell_manager.get_player_cells(p1)
    opponent_cells = board_setup.cell_manager.get_player_cells(p2)
    return player_cells, opponent_cells
