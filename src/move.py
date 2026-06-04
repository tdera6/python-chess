from dataclasses import dataclass


@dataclass
class Move:
    from_square: int
    to_square: int
    piece_moved: int
    piece_captured: int = 0
    is_promotion: bool = False
    promotion_to: int = 0

    def __str__(self):
        columns = "abcdefgh"
        starting_row = self.from_square // 16
        starting_column = self.from_square - starting_row * 16

        ending_row = self.to_square // 16
        ending_column = self.to_square - ending_row * 16

        promotion_str = "" if not self.is_promotion else f" -> {self.promotion_to}"

        return f"{columns[starting_column]}{starting_row + 1}-{columns[ending_column]}{ending_row + 1}{promotion_str}"
