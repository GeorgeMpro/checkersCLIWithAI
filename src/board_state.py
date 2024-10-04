from dataclasses import dataclass
from typing import List


@dataclass
class BoardState:
    cells: List[List['Cell']]
