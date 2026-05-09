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

            # Generate moves for white if there is their turn
            if self.board.turn == Board.WHITE:
                if piece == Board.WHITE_PAWN:
                    self.generate_white_pawn_moves(square, piece, moves)
            
            # Generate moves for black if there is their turn
            elif self.board.turn == Board.BLACK:
                if piece == Board.BLACK_PAWN:
                    self.generate_black_pawn_moves(square, piece, moves)
        
        return moves

    # Chec if piece is the same color as the moving piece
    def is_friendly(self, piece: int) -> bool:
        turn = self.board.turn

        if piece == Board.EMPTY:
            return False
        
        return  (turn == Board.WHITE and piece > 0) or\
                (turn == Board.BLACK and piece < 0)
    
    # Check if piece is opposite color from the moving piece
    def is_enemy(self, piece: int) -> bool:
        turn = self.board.turn

        if piece == Board.EMPTY:
            return False
        
        return  (turn == Board.WHITE and piece < 0) or\
                (turn == Board.BLACK and piece > 0)
    
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

        # Capturing
        left_capture = square + 15
        right_capture = square + 17

        if not (left_capture & 0x88) and self.is_enemy(self.board.squares[left_capture]):
            moves.append(Move(from_square=square, to_square=left_capture, piece_moved=piece, piece_captured=self.board.squares[left_capture]))

        if not (right_capture & 0x88) and self.is_enemy(self.board.squares[right_capture]):
            moves.append(Move(from_square=square, to_square=right_capture, piece_moved=piece, piece_captured=self.board.squares[right_capture]))

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

        # Capturing
        left_capture = square - 15
        right_capture = square - 17

        if not (left_capture & 0x88) and self.is_enemy(self.board.squares[left_capture]):
            moves.append(Move(from_square=square, to_square=left_capture, piece_moved=piece, piece_captured=self.board.squares[left_capture]))

        if not (right_capture & 0x88) and self.is_enemy(self.board.squares[right_capture]):
            moves.append(Move(from_square=square, to_square=right_capture, piece_moved=piece, piece_captured=self.board.squares[right_capture]))
    