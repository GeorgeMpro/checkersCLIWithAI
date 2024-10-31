from dataclasses import dataclass
from typing import List

from component.cell import Cell


@dataclass
class BoardState:
    cells: List[List[Cell]]
