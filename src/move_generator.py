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
                elif piece == Board.WHITE_KNIGHT:
                    self.generate_knight_moves(square, piece, moves)
                elif piece == Board.WHITE_BISHOP:
                    self.generate_bishop_moves(square, piece, moves)
                elif piece == Board.WHITE_ROOK:
                    self.generate_rook_moves(square, piece, moves)
            
            # Generate moves for black if there is their turn
            elif self.board.turn == Board.BLACK:
                if piece == Board.BLACK_PAWN:
                    self.generate_black_pawn_moves(square, piece, moves)
                elif piece == Board.BLACK_KNIGHT:
                    self.generate_knight_moves(square, piece, moves)
                elif piece == Board.BLACK_BISHOP:
                    self.generate_bishop_moves(square, piece, moves)
                elif piece == Board.BLACK_ROOK:
                    self.generate_rook_moves(square, piece, moves)
        
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
    
    def generate_knight_moves(self, square: int, piece: int, moves: list[Move]):
        directions = {33, 18, -14, -31, -33, -18, 14, 31}

        for direction in directions:
            target_square = square + direction
            
            if not (target_square & 0x88):
                target_piece = self.board.squares[target_square]
                
                if target_piece == Board.EMPTY:
                    moves.append(Move(from_square=square, to_square=target_square, piece_moved=piece))
                elif self.is_enemy(target_piece):
                    moves.append(Move(from_square=square, to_square=target_square, piece_moved=piece, piece_captured=target_piece))
    
    # Helper function to generate Queen, Bishop and Rook moves
    def sliding_pieces(self, square: int , piece: int, directions: list[int], moves: list[Move]):

        from_square = square

        for direction in directions:
            to_square = from_square
            while True:
                to_square += direction

                if to_square & 0x88:
                    break
                
                piece_on_to_square = self.board.squares[to_square]
                if piece_on_to_square == Board.EMPTY:
                    moves.append(Move(from_square, to_square, piece))
                elif self.is_enemy(piece_on_to_square):
                    moves.append(Move(from_square, to_square, piece, piece_captured=piece_on_to_square))
                    break
                elif self.is_friendly(piece_on_to_square):
                    break

    def generate_bishop_moves(self, square: int, piece: int, moves: list[Move]):
        directions = [15, 17, -15, -17]
        self.sliding_pieces(square, piece, directions, moves)

    def generate_rook_moves(self, square: int, piece: int, moves: list[Move]):
        directions = [1, -1, 16, -16]
        self.sliding_pieces(square, piece, directions, moves)