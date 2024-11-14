from copy import deepcopy

from ai.ai_context_manager import AIContextManager
from ai.node_generator import NodeGenerator, Node
from board import Board
from component.cell import Cell
from component.game import Game
from state.move_state import MoveState


class HeuristicExplorer:
    def __init__(self, board: Board):
        self.board = board
        self.node_gen = NodeGenerator()
        # todo
        with AIContextManager(board) as ai_context:
            self.ai_cell_manager = ai_context.cell_manager
            self.ai_game = ai_context.game

    def ai_execute_available_moves(
            self, depth_counter: int = 0, max_depth: int = 0, copy_game=None, copy_map=None
    ) -> None:
        is_exploration = depth_counter < max_depth
        if max_depth == 0:
            self._execute_ai_base_case()
        elif is_exploration:
            with AIContextManager(self.board) as ai_context:
                # todo, test?
                if ai_context.game.is_game_over:
                    return
            self._recursive_setup(copy_game, copy_map)
            self._execute_recursive_exploration(depth_counter, max_depth)

    def _execute_ai_base_case(self) -> None:
        self._setup_ai_base_level_copy_state()
        pairs, states = self._get_move_pairs_and_states_to_execute()
        self._execute_ai_moves_on_copied_states(pairs, states)

    def _recursive_setup(
            self, copy_game: Game, copy_map: dict[str, Cell]
    ) -> None:
        """
        Set up the AI states on the board.
        """
        self._setup_board_copy_state(copy_game, copy_map)
        if not copy_game and not copy_map:
            self._setup_ai_base_level_copy_state()

    def _execute_recursive_exploration(
            self, depth_counter: int, max_depth: int) -> None:
        """
        Execute the exploration on state copies.
        """
        pairs, states = self._get_move_pairs_and_states_to_execute()
        # todo consider changing to pair state and deconstruct in calling function
        for (src, tar), (game, cell_map) in zip(pairs, states, strict=True):
            self._explore_move((src, tar), (game, cell_map), depth_counter, max_depth)

    def _explore_move(
            self, pair: tuple[str, str], state: tuple[Game, dict[str, Cell]], depth_counter: int, max_depth: int
    ) -> None:
        """
        Explore given move, sending modified game for further exploration.
        """
        src, tar = pair
        game, cell_map = state
        # set AI state for each move to execute one
        self._setup_board_copy_state(game, cell_map)
        self._execute_ai_move(src, tar)
        # recursive call
        self.ai_execute_available_moves(depth_counter + 1, max_depth, game, cell_map)

    def _setup_ai_base_level_copy_state(self) -> None:
        """
        Setup AI states by copying the main game.
        """
        game_copy = deepcopy(self.board.game)
        map_copy = self.board.cell_manager.get_cell_map_copy()
        self._setup_board_copy_state(game_copy, map_copy)

    # todo, possibly remove.
    def _execute_ai_moves_on_copied_states(
            self, pairs: list[tuple[str, str]],
            states: list[tuple[Game, dict[str, Cell]]]
    ) -> None:
        for (src, tar), (game, cell_map) in zip(pairs, states):
            self._setup_board_copy_state(game, cell_map)
            self._execute_ai_move(src, tar)

    def _get_move_pairs_and_states_to_execute(
            self
    ) -> tuple[list[tuple[str, str]], list[tuple[Game, dict[str, Cell]]]]:
        """
        Generate move pairs and their corresponding game states for AI exploration.

        This generator yields one tuple at a time to reduce memory usage
        and allow for efficient handling of large numbers of moves.
        """
        pairs = self._generate_move_pairs(
            self._get_available_player_moves()
        )
        states = self._generate_state_copies(len(pairs))

        return pairs, states

    def _get_available_player_moves(self) -> list[MoveState]:
        """
        Generate all moves available to current player.
        """
        with AIContextManager(self.board) as ai_context:
            player_name = ai_context.game.current_player.name
            return ai_context.get_available_moves(player_name)

    def _setup_board_copy_state(
            self, game: Game, cell_map: dict[str, Cell]
    ) -> None:
        """
        Pass state directly to the board for update.
        """
        # todo can't seem to find a way to implicitly passing them through HS fields or other methods.
        # Notice: avoids mixing the reference to game and AI game
        self.board.set_ai_state_parameters(game, cell_map)

    def _execute_ai_move(self, src: str, tar: str) -> None:
        """
        Execute the move using AI specific board functionality.
        """
        with AIContextManager(self.board) as ai_context:
            ai_context.move_piece(src, tar)

    # todo ? move to move util?
    @staticmethod
    def _generate_move_pairs(
            player_moves: list[MoveState]
    ) -> list[tuple[str, str]]:
        move_pairs = [
            (move.src_name, target)
            for move in player_moves
            for target in move.target_names
        ]
        return move_pairs

    def _get_cell_map_and_game_copies(self) -> tuple[dict[str, Cell], Game]:
        map_copy = self.board.cell_manager.get_cell_map_copy()
        game_copy = deepcopy(self.board.game)

        return map_copy, game_copy

    def _generate_state_copies(
            self, number_of_copies: int
    ) -> list[tuple[Game, dict[str, Cell]]]:
        """
        Generate unique copies of game state for the AI to explore available moves.
        """
        copies = []
        for _ in range(number_of_copies):
            with AIContextManager(self.board) as ai_context:
                game_copy = deepcopy(ai_context.game)
                map_copy = ai_context.cell_manager.get_cell_map_copy()
                copies.append((game_copy, map_copy))

        return copies

    def generate_root_node(self) -> Node:
        map_copy, game_copy = self._get_cell_map_and_game_copies()

        return self.node_gen.generate_root_node(map_copy, game_copy)
