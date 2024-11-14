from dataclasses import dataclass, field


@dataclass
class Node:
    score: int
    player: str
    moves: list[tuple[str, str]] = field(default_factory=list)
    children: dict[tuple[str, str], "Node"] = field(default_factory=dict)
    depth: int = field(default=0)

    # todo add score on move?
    def add_child(self, move_pair: tuple[str, str], child: "Node") -> None:
        self.children[move_pair] = child
        child.depth = self.depth + 1
