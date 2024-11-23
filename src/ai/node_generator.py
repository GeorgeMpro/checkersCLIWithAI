from dataclasses import dataclass
from typing import Optional

from ai.educated_guess_heuristic import eval_player_state
from ai.node import Node
from component.cell import Cell


# comparison based on the first field
@dataclass(order=True)
class Path:
    depth: int
    move: tuple[str, str]
    score: int
    current_player: str
    moves: list[tuple[str, str]]


# todo ? change to util class?
class NodeGenerator:
    def __init__(self):
        self._root_node: Optional[Node] = None

    @property
    def root_node(self) -> Node:
        return self._root_node

    @root_node.setter
    def root_node(self, root_node: Node):
        self._root_node = root_node

    @root_node.deleter
    def root_node(self):
        self._root_node = None

    def generate_root_node(
            self, current_players: tuple[str, str], move_pairs, all_cells: tuple[list[Cell], list[Cell]]
    ) -> Node:
        return self._initialize_node(
            current_players,
            move_pairs,
            all_cells
        )

    # todo move?
    @staticmethod
    def _initialize_node(
            current_players: tuple[str, str], move_pairs: list[tuple[str, str]],
            all_cells: tuple[list[Cell], list[Cell]]
    ) -> Node:
        """
        Generate a node from given values.

        Notice: assumes provided correct values.
        """
        player, opponent = current_players
        player_cells, opponent_cells = all_cells
        score = eval_player_state(player_cells, opponent_cells)

        return Node(score, player, move_pairs)

    # todo doc when done
    def generate_path_by_dfs(
            self, node: Node = None, is_root: bool = True
    ) -> list[Path]:

        # todo error handling when zip error?
        path = []
        if is_root:
            node = self._setup_path_root_node(path)

        self._validate_child_and_move_lengths(node)

        self._dfs_explore_and_append(node, path)

        return path

    def _setup_path_root_node(
            self, path: list[Path]
    ) -> Node:
        root = self.root_node
        self._append_path(root, None, path)
        return root

    @staticmethod
    def _validate_child_and_move_lengths(
            node: Node
    ) -> None:
        # Validate moves and children
        # todo del? handle error?
        if len(node.moves) != len(node.children):
            # todo
            # print(f"\n{node.moves=} {node.children=}")
            raise ValueError(f"Mismatch: moves={len(node.moves)} and children={len(node.children)}")

    def _dfs_explore_and_append(
            self, node: Node, path: list[Path]
    ) -> None:
        for move, child in zip(node.moves, node.children.values(), strict=True):
            self._append_path(child, move, path)
            self._dfs_explore_children_of_current_child(child, path)

    @staticmethod
    def _append_path(
            node, move: Optional[tuple[str, str]], dfs_path: list[Path]
    ) -> None:
        dfs_path.append(
            Path(
                node.depth, move, node.score, node.player, node.moves
            )
        )

    def _dfs_explore_children_of_current_child(
            self, child: Node, path: list[Path]
    ) -> None:
        path.extend(
            self.generate_path_by_dfs(child, is_root=False)
        )
