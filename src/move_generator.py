from src.board import Board
from src.move import Move

class MoveGenerator:
    def __init__(self, board: Board):
        self.board = board

    def generate_moves(self) -> list[Move]:
        moves = []

        for square in range(128):
            if square & 0x88:
                continue

            piece = self.board.squares[square]

            if piece == Board.WHITE_PAWN:
                self.generate_white_pawn_moves(square, piece, moves)
            elif piece == Board.BLACK_PAWN:
                self.generate_black_pawn_moves(square, piece, moves)
        
        return moves
    
    def generate_white_pawn_moves(self, square: int, piece: int, moves: list[Move]):
        one_square_ahead = square + 16
        two_squares_ahead = square + 32

        # Basic one square move
        if not (one_square_ahead & 0x88) and self.board.squares[one_square_ahead] == Board.EMPTY:
            moves.append(Move(from_square=square, to_square=one_square_ahead, piece_moved=piece))

        # Check if pawn is in second row
        if square // 16 == 1:
            # Check if two squares ahead are empty
            if self.board.squares[one_square_ahead] == Board.EMPTY\
            and self.board.squares[two_squares_ahead] == Board.EMPTY:
                moves.append(Move(from_square=square, to_square=two_squares_ahead, piece_moved=piece))

    def generate_black_pawn_moves(self, square: int, piece: int, moves: list[Move]):
        one_square_ahead = square - 16
        two_squares_ahead = square - 32

        # Basic one square move
        if not (one_square_ahead & 0x88) and self.board.squares[one_square_ahead] == Board.EMPTY:
            moves.append(Move(from_square=square, to_square=one_square_ahead, piece_moved=piece))

        # Check if pawn is in seventh row
        if square // 16 == 6:
            # Check if two squares ahead are empty
            if self.board.squares[one_square_ahead] == Board.EMPTY\
            and self.board.squares[two_squares_ahead] == Board.EMPTY:
                moves.append(Move(from_square=square, to_square=two_squares_ahead, piece_moved=piece))
    