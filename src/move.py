from dataclasses import dataclass

@dataclass
class Move:
    from_square: int
    to_square: int
    piece_moved: int
    piece_captured: int = 0