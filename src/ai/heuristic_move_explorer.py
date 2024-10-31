from itertools import chain

from ai.educated_guess_heuristic import eval_player_state
from component.cell import Cell
from managers.cell_manager import CellManager
from state.move_state import MoveState


def calculate_copy_state_score(
        map_copy: dict[str, Cell], player_name: str, opponent_name: str,
        heuristic=eval_player_state
) -> int:
    player_cells = CellManager.get_player_cells_from_copy(map_copy, player_name)
    opponent_cells = CellManager.get_player_cells_from_copy(map_copy, opponent_name)

    return heuristic(player_cells, opponent_cells)


def get_number_of_moves(
        available_moves: list[MoveState]
) -> int:
    """
    Get the number of available moves for given move list.

    """
    return len(
        list(chain.from_iterable(
            move.target_names for move in available_moves)
        )
    )


def extract_in_order_all_move_src_target(
        available_moves: list[MoveState]
) -> list[tuple[str, str]]:
    """
    Extract all move pairs from given move states and returned sorted.
    """
    unsorted_list = [
        (move.src_name, target_name)
        for move in available_moves
        for target_name in move.target_names
    ]
    unsorted_list.sort()  # In-place sort by (src_name, target_name)
    return unsorted_list
