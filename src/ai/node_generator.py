from dataclasses import dataclass, field

from ai.educated_guess_heuristic import eval_player_state
from component.cell import Cell
from component.game import Game
from state.move_state import MoveState


@dataclass
class Node:
    score: int
    player: str
    moves: list = field(default_factory=list)


class NodeGenerator:
    def generate_root_node(self, map_cp, game_cp) -> Node:
        self.set_ai_cell_map(map_cp)

        return self._initialize_node(game_cp)

    # todo
    #   maybe pass cell_map each time?
    def _initialize_node(self, game_copy: Game) -> Node:
        player, opponent = self._get_player_and_opponent_names(game_copy)
        player_cells, opponent_cells = self._get_all_game_cells(player, opponent)
        moves = self._get_moves(player, game_copy)
        score = self._get_score(opponent_cells, player_cells)

        return Node(score, player, moves)

    @staticmethod
    def _get_score(
            opponent_cells: list[Cell], player_cells: list[Cell]
    ) -> int:
        return eval_player_state(
            player_cells, opponent_cells
        )

    def _get_moves(
            self, player: str, game_copy: Game
    ) -> list[MoveState]:
        return self.ai_cell_manager.generate_available_moves_for_player(
            player, game_copy.chaining_cell_name
        )

    def set_ai_cell_map(self, cell_map_copy: dict[str, Cell]) -> None:
        self.ai_cell_manager.cell_map = cell_map_copy

    @staticmethod
    def _get_player_and_opponent_names(
            game_copy: Game
    ) -> tuple[str, str]:
        player = game_copy.current_player.name
        opponent = P.P2.name if player else P.P1.name
        return player, opponent

    def _get_all_game_cells(
            self, player: str, opponent: str
    ) -> tuple[list[Cell], list[Cell]]:
        player_cells = self.ai_cell_manager.get_player_cells(player)
        opponent_cells = self.ai_cell_manager.get_player_cells(opponent)

        return player_cells, opponent_cells
