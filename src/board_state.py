from dataclasses import dataclass
from typing import List

from cell import Cell


@dataclass
class BoardState:
    cells: List[List['Cell']]
