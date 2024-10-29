from dataclasses import dataclass

from typing import Optional, List


@dataclass(frozen=True)
class CaptureMove:
    name_target_cell: str
    name_final_cell: str


@dataclass
class MoveState:
    src_name: str
    target_names: List[str]
    is_capture_move: bool = False
    capture_moves: Optional[List[CaptureMove]] = None

    def is_capture(self):
        return self.is_capture_move

    def __repr__(self):
        return f"MoveDTO(src='{self.src_name}', target='{self.target_names}', is_capture={self.is_capture_move}, capture_moves='{self.capture_moves}')"

    def __eq__(self, other) -> bool:
        """
        Overrides the default Equals behavior. Assume no importance of the items inside the MoveState when multiple targets and captures having several CaptureMove items.
        """
        if not isinstance(other, MoveState):
            return False
        return (
                self.src_name == other.src_name and
                sorted(self.target_names) == sorted(other.target_names) and
                self.is_capture_move == other.is_capture_move and
                sorted(self.capture_moves or [], key=lambda x: (x.name_target_cell, x.name_final_cell)) ==
                sorted(other.capture_moves or [], key=lambda x: (x.name_target_cell, x.name_final_cell))
        )

    def get_capture_moves(self) -> List[CaptureMove]:
        """
        Gets the capture moves for the current capture state.
        """
        return self.capture_moves
