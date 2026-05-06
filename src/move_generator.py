from src.board import Board
from src.move import Move

class MoveGenerator:
    def __init__(self, board: Board):
        self.board = Board

    def generate_moves(self) -> list[Move]:
        moves = []

        for square in range(128):
            if square & 0x88:
                continue

            piece = self.board.squares[square]

            if piece == Board.WHITE_PAWN:
                self.generate_white_pawn_moves(square, piece, moves)
        
        return moves
    
    def generate_white_pawn_moves(self, square: int, piece: int, moves: list[Move]):
        one_square_ahead = square + 16
        
        if not (one_square_ahead & 0x88) and self.board.squares[one_square_ahead] == Board.EMPTY:
            moves.append(Move(from_square=square, to_square=one_square_ahead, piece_moved=piece))
    