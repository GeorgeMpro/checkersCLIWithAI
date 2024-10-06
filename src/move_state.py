from dataclasses import dataclass

from typing import Optional


@dataclass
class MoveState:
    src_name: str
    target_name: str
    is_capture_move: bool
    final_dest_name: Optional[str] = None

    def __repr__(self):
        return f"MoveDTO(src='{self.src_name}', target='{self.target_name}', capture={self.is_capture_move}, final_dest='{self.final_dest_name}')"
