from dataclasses import dataclass

from typing import Optional, List


@dataclass(frozen=True)
class CaptureMove:
    """
    Represents a capture move holding the names of the target cell and the cell you end up after capture.
    """
    name_target_cell: str
    name_final_cell: str


@dataclass
class MoveState:
    """
    A move state consists of the source, target(s) and optional capture move(s).
    """
    src_name: str
    target_names: List[str]
    is_capture_move: bool = False
    capture_moves: Optional[List[CaptureMove]] = None

    def is_capture(self) -> bool:
        return self.is_capture_move

    def __eq__(self, other) -> bool:
        """
        Assume no importance of the order of items inside the MoveState when multiple targets and captures having several CaptureMove items.
        """
        if not isinstance(other, MoveState):
            return False
        return (
                self.src_name == other.src_name
                and sorted(self.target_names) == sorted(other.target_names)
                and self.is_capture_move == other.is_capture_move
                and self._sorted_capture_moves() == other._sorted_capture_moves()
        )

    def _sorted_capture_moves(self) -> List[CaptureMove]:
        """
        Returns a sorted list of capture moves.
        """
        capture_list = self.capture_moves or []
        return sorted(
            capture_list,
            key=lambda x: (x.name_target_cell, x.name_final_cell)
        )

    def get_capture_moves(self) -> List[CaptureMove]:
        """
        Returns capture moves for the current capture state.
        """
        return self.capture_moves
