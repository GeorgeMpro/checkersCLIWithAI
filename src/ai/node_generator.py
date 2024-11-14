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

    def dfs_path(self, node: Node = None, is_root: bool = True):

        # todo error handling when zip error?
        path = []
        if is_root:
            root = self.root_node
            node = root
            path.append(
                Path(root.depth, None, root.score, root.player, root.moves)
            )

        # Validate moves and children
        # todo del? handle error?
        if len(node.moves) != len(node.children):
            # todo
            print(f"\n{node.moves=} {node.children=}")
            raise ValueError(f"Mismatch: moves={len(node.moves)} and children={len(node.children)}")

        for move, child in zip(node.moves, node.children.values(), strict=True):
            path.append(
                Path(child.depth, move, child.score, child.player, child.moves)
            )
            path.extend(self.dfs_path(child, is_root=False))

        return path
