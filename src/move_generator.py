from src.board import Board
from src.move import Move


class MoveGenerator:
    def __init__(self, board: Board):
        self.board = board

    def generate_moves(self) -> list[Move]:
        moves: list[Move] = []

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
                elif piece == Board.WHITE_QUEEN:
                    self.generate_queen_moves(square, piece, moves)
                elif piece == Board.WHITE_KING:
                    self.generate_king_moves(square, piece, moves)

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
                elif piece == Board.BLACK_QUEEN:
                    self.generate_queen_moves(square, piece, moves)
                elif piece == Board.BLACK_KING:
                    self.generate_king_moves(square, piece, moves)

        for m in moves:
            m.previous_en_passant_square = self.board.en_passant_square
            m.previous_white_short_castle = self.board.can_white_short_castle
            m.previous_white_long_castle = self.board.can_white_long_castle
            m.previous_black_short_castle = self.board.can_black_short_castle
            m.previous_black_long_castle = self.board.can_black_long_castle

        return moves

    # Chec if piece is the same color as the moving piece
    def is_friendly(self, piece: int) -> bool:
        turn = self.board.turn

        if piece == Board.EMPTY:
            return False

        return (turn == Board.WHITE and piece > 0) or (
            turn == Board.BLACK and piece < 0
        )

    # Check if piece is opposite color from the moving piece
    def is_enemy(self, piece: int) -> bool:
        turn = self.board.turn

        if piece == Board.EMPTY:
            return False

        return (turn == Board.WHITE and piece < 0) or (
            turn == Board.BLACK and piece > 0
        )

    def is_square_under_atack(self, square: int, attacking_color: int) -> bool:
        DIRECTIONS_BISHOP_QUEEN = [15, 17, -15, -17]
        DIRECTIONS_ROOK_QUEEN = [16, -16, 1, -1]
        DIRECTIONS_KNIGHT = [33, 18, -14, -31, -33, -18, 14, 31]
        DIRECTIONS_KING = [1, -17, -16, -15, -1, 15, 16, 17]

        if attacking_color == Board.WHITE:
            left_pawn = square - 17
            right_pawn = square - 15
            if (left_pawn & 0x88) == 0 and self.board.squares[
                left_pawn
            ] == Board.WHITE_PAWN:
                return True
            elif (right_pawn & 0x88) == 0 and self.board.squares[
                right_pawn
            ] == Board.WHITE_PAWN:
                return True
        else:  # attacking_color == Board.BLACK
            left_pawn = square + 15
            right_pawn = square + 17
            if (left_pawn & 0x88) == 0 and self.board.squares[
                left_pawn
            ] == Board.BLACK_PAWN:
                return True
            elif (right_pawn & 0x88) == 0 and self.board.squares[
                right_pawn
            ] == Board.BLACK_PAWN:
                return True

        attacking_king = (
            Board.WHITE_KING if attacking_color == Board.WHITE else Board.BLACK_KING
        )
        attacking_knight = (
            Board.WHITE_KNIGHT if attacking_color == Board.WHITE else Board.BLACK_KNIGHT
        )
        attacking_bishop = (
            Board.WHITE_BISHOP if attacking_color == Board.WHITE else Board.BLACK_BISHOP
        )
        attacking_queen = (
            Board.WHITE_QUEEN if attacking_color == Board.WHITE else Board.BLACK_QUEEN
        )
        attacking_rook = (
            Board.WHITE_ROOK if attacking_color == Board.WHITE else Board.BLACK_ROOK
        )

        for direction in DIRECTIONS_KING:
            target_square = square + direction

            if (target_square & 0x88) == 0 and self.board.squares[
                target_square
            ] == attacking_king:
                return True

        for direction in DIRECTIONS_KNIGHT:
            target_square = square + direction

            if (target_square & 0x88) == 0 and self.board.squares[
                target_square
            ] == attacking_knight:
                return True

        for direction in DIRECTIONS_BISHOP_QUEEN:
            target_square = square + direction
            while (target_square & 0x88) == 0:
                if (
                    self.board.squares[target_square] == attacking_bishop
                    or self.board.squares[target_square] == attacking_queen
                ):
                    return True
                elif self.board.squares[target_square] != Board.EMPTY:
                    break

                target_square += direction

        for direction in DIRECTIONS_ROOK_QUEEN:
            target_square = square + direction
            while (target_square & 0x88) == 0:
                if (
                    self.board.squares[target_square] == attacking_rook
                    or self.board.squares[target_square] == attacking_queen
                ):
                    return True
                elif self.board.squares[target_square] != Board.EMPTY:
                    break

                target_square += direction

        return False

    def generate_white_pawn_moves(self, square: int, piece: int, moves: list[Move]):
        one_square_ahead = square + 16
        two_squares_ahead = square + 32

        # Basic one square move
        if (
            not (one_square_ahead & 0x88)
            and self.board.squares[one_square_ahead] == Board.EMPTY
        ):
            # Check if pawn is promoting
            if square // 16 == 6:
                self.pawn_promotion(square, one_square_ahead, moves)
            else:
                moves.append(
                    Move(
                        from_square=square,
                        to_square=one_square_ahead,
                        piece_moved=piece,
                    )
                )

        # Check if pawn is in second row
        if square // 16 == 1:
            # Check if two squares ahead are empty
            if (
                self.board.squares[one_square_ahead] == Board.EMPTY
                and self.board.squares[two_squares_ahead] == Board.EMPTY
            ):
                moves.append(
                    Move(
                        from_square=square,
                        to_square=two_squares_ahead,
                        piece_moved=piece,
                        is_double_pawn_move=True,
                    )
                )

        # Capturing
        left_capture = square + 15
        right_capture = square + 17

        en_passant_square = self.board.en_passant_square

        if en_passant_square == left_capture:
            moves.append(
                Move(
                    from_square=square,
                    to_square=left_capture,
                    piece_moved=piece,
                    piece_captured=piece * (-1),
                    is_en_passant=True,
                )
            )

        if en_passant_square == right_capture:
            moves.append(
                Move(
                    from_square=square,
                    to_square=right_capture,
                    piece_moved=piece,
                    piece_captured=piece * (-1),
                    is_en_passant=True,
                )
            )

        if not (left_capture & 0x88) and self.is_enemy(
            self.board.squares[left_capture]
        ):
            # Check if pawn is promoting
            if square // 16 == 6:
                self.pawn_promotion(square, left_capture, moves)
            else:
                moves.append(
                    Move(
                        from_square=square,
                        to_square=left_capture,
                        piece_moved=piece,
                        piece_captured=self.board.squares[left_capture],
                    )
                )

        if not (right_capture & 0x88) and self.is_enemy(
            self.board.squares[right_capture]
        ):
            # Check if pawn is promoting
            if square // 16 == 6:
                self.pawn_promotion(square, right_capture, moves)
            else:
                moves.append(
                    Move(
                        from_square=square,
                        to_square=right_capture,
                        piece_moved=piece,
                        piece_captured=self.board.squares[right_capture],
                    )
                )

    def generate_black_pawn_moves(self, square: int, piece: int, moves: list[Move]):
        one_square_ahead = square - 16
        two_squares_ahead = square - 32

        # Basic one square move
        if (
            not (one_square_ahead & 0x88)
            and self.board.squares[one_square_ahead] == Board.EMPTY
        ):
            # Check if pawn is promoting
            if square // 16 == 1:
                self.pawn_promotion(square, one_square_ahead, moves)
            else:
                moves.append(
                    Move(
                        from_square=square,
                        to_square=one_square_ahead,
                        piece_moved=piece,
                    )
                )

        # Check if pawn is in seventh row
        if square // 16 == 6:
            # Check if two squares ahead are empty
            if (
                self.board.squares[one_square_ahead] == Board.EMPTY
                and self.board.squares[two_squares_ahead] == Board.EMPTY
            ):
                moves.append(
                    Move(
                        from_square=square,
                        to_square=two_squares_ahead,
                        piece_moved=piece,
                        is_double_pawn_move=True,
                    )
                )

        # Capturing
        left_capture = square - 15
        right_capture = square - 17

        en_passant_square = self.board.en_passant_square

        if en_passant_square == left_capture:
            moves.append(
                Move(
                    from_square=square,
                    to_square=left_capture,
                    piece_moved=piece,
                    piece_captured=piece * (-1),
                    is_en_passant=True,
                )
            )

        if en_passant_square == right_capture:
            moves.append(
                Move(
                    from_square=square,
                    to_square=right_capture,
                    piece_moved=piece,
                    piece_captured=piece * (-1),
                    is_en_passant=True,
                )
            )

        if not (left_capture & 0x88) and self.is_enemy(
            self.board.squares[left_capture]
        ):
            # Check if pawn is promoting
            if square // 16 == 1:
                self.pawn_promotion(square, left_capture, moves)
            else:
                moves.append(
                    Move(
                        from_square=square,
                        to_square=left_capture,
                        piece_moved=piece,
                        piece_captured=self.board.squares[left_capture],
                    )
                )

        if not (right_capture & 0x88) and self.is_enemy(
            self.board.squares[right_capture]
        ):
            # Check if pawn is promoting
            if square // 16 == 1:
                self.pawn_promotion(square, right_capture, moves)
            else:
                moves.append(
                    Move(
                        from_square=square,
                        to_square=right_capture,
                        piece_moved=piece,
                        piece_captured=self.board.squares[right_capture],
                    )
                )

    def generate_knight_moves(self, square: int, piece: int, moves: list[Move]):
        directions = {33, 18, -14, -31, -33, -18, 14, 31}

        for direction in directions:
            target_square = square + direction

            if not (target_square & 0x88):
                target_piece = self.board.squares[target_square]

                if target_piece == Board.EMPTY:
                    moves.append(
                        Move(
                            from_square=square,
                            to_square=target_square,
                            piece_moved=piece,
                        )
                    )
                elif self.is_enemy(target_piece):
                    moves.append(
                        Move(
                            from_square=square,
                            to_square=target_square,
                            piece_moved=piece,
                            piece_captured=target_piece,
                        )
                    )

    # Helper function to generate Queen, Bishop and Rook moves
    def sliding_pieces(
        self, square: int, piece: int, directions: list[int], moves: list[Move]
    ):

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
                    moves.append(
                        Move(
                            from_square,
                            to_square,
                            piece,
                            piece_captured=piece_on_to_square,
                        )
                    )
                    break
                elif self.is_friendly(piece_on_to_square):
                    break

    def generate_bishop_moves(self, square: int, piece: int, moves: list[Move]):
        directions = [15, 17, -15, -17]
        self.sliding_pieces(square, piece, directions, moves)

    def generate_rook_moves(self, square: int, piece: int, moves: list[Move]):
        directions = [1, -1, 16, -16]
        self.sliding_pieces(square, piece, directions, moves)

    def generate_queen_moves(self, square: int, piece: int, moves: list[Move]):
        directions = [15, 17, -15, -17, 1, -1, 16, -16]
        self.sliding_pieces(square, piece, directions, moves)

    def generate_king_moves(self, square: int, piece: int, moves: list[Move]):
        directions = [1, -17, -16, -15, -1, 15, 16, 17]

        color = piece / Board.KING
        if self.can_king_short_castle(color):
            moves.append(
                Move(
                    square, square + 2, piece, is_castling=True, is_short_castling=True
                )
            )

        if self.can_king_long_castle(color):
            moves.append(
                Move(square, square - 2, piece, is_castling=True, is_long_castling=True)
            )

        for direction in directions:
            to_square = square + direction

            if to_square & 0x88:
                continue

            piece_on_to_square = self.board.squares[to_square]

            if piece_on_to_square == Board.EMPTY:
                moves.append(
                    Move(from_square=square, to_square=to_square, piece_moved=piece)
                )
            elif self.is_enemy(piece_on_to_square):
                moves.append(
                    Move(
                        from_square=square,
                        to_square=to_square,
                        piece_moved=piece,
                        piece_captured=piece_on_to_square,
                    )
                )
            elif self.is_friendly(piece_on_to_square):
                continue

    def generate_legal_moves(self) -> list[Move]:
        moves = self.generate_moves()
        legal_moves = []

        for move in moves:
            self.board.make_move(move)

            # When we make move the turn switches up
            king_position = (
                self.board.white_king_square
                if self.board.turn == Board.BLACK
                else self.board.black_king_square
            )

            if not self.is_square_under_atack(king_position, self.board.turn):
                legal_moves.append(move)

            self.board.undo_move(move)

        return legal_moves

    def pawn_promotion(self, from_square: int, to_square: int, moves: list[Move]):
        pieces_to_promote_into = [Board.KNIGHT, Board.BISHOP, Board.ROOK, Board.QUEEN]

        color = self.board.turn
        piece_captured = self.board.squares[to_square]

        for piece in pieces_to_promote_into:
            piece_moved = Board.PAWN * color

            move = Move(
                from_square=from_square,
                to_square=to_square,
                piece_moved=piece_moved,
                piece_captured=piece_captured,
                is_promotion=True,
                promotion_to=piece * color,
            )

            moves.append(move)

    def can_king_short_castle(self, color: int) -> bool:
        if color == Board.WHITE:
            if not self.board.can_white_short_castle:
                return False

            # If king and rook are in correct position and king is not checked and the squares he is going to move through are not under attack and are empty
            if (
                self.board.squares[0x04] == Board.WHITE_KING
                and self.board.squares[0x07] == Board.WHITE_ROOK
                and self.board.squares[0x05] == Board.EMPTY
                and self.board.squares[0x06] == Board.EMPTY
                and not self.is_square_under_atack(0x04, Board.BLACK)
                and not self.is_square_under_atack(0x05, Board.BLACK)
                and not self.is_square_under_atack(0x06, Board.BLACK)
            ):
                return True
        else:  # color == Board.BLACK
            if not self.board.can_black_short_castle:
                return False

            # If king and rook are in correct position and king is not checked and the squares he is going to move through are not under attack and are empty
            if (
                self.board.squares[0x74] == Board.BLACK_KING
                and self.board.squares[0x77] == Board.BLACK_ROOK
                and self.board.squares[0x75] == Board.EMPTY
                and self.board.squares[0x76] == Board.EMPTY
                and not self.is_square_under_atack(0x74, Board.WHITE)
                and not self.is_square_under_atack(0x75, Board.WHITE)
                and not self.is_square_under_atack(0x76, Board.WHITE)
            ):
                return True

        return False

    def can_king_long_castle(self, color: int) -> bool:
        if color == Board.WHITE:
            if not self.board.can_white_long_castle:
                return False

            # If king and rook are in correct position and king is not checked and the squares he is going to move through are not under attack and are empty
            if (
                self.board.squares[0x04] == Board.WHITE_KING
                and self.board.squares[0x00] == Board.WHITE_ROOK
                and self.board.squares[0x01] == Board.EMPTY
                and self.board.squares[0x02] == Board.EMPTY
                and self.board.squares[0x03] == Board.EMPTY
                and not self.is_square_under_atack(0x02, Board.BLACK)
                and not self.is_square_under_atack(0x03, Board.BLACK)
                and not self.is_square_under_atack(0x04, Board.BLACK)
            ):
                return True
        else:  # color == Board.BLACK
            if not self.board.can_black_long_castle:
                return False

            # If king and rook are in correct position and king is not checked and the squares he is going to move through are not under attack and are empty
            if (
                self.board.squares[0x74] == Board.BLACK_KING
                and self.board.squares[0x70] == Board.BLACK_ROOK
                and self.board.squares[0x71] == Board.EMPTY
                and self.board.squares[0x72] == Board.EMPTY
                and self.board.squares[0x73] == Board.EMPTY
                and not self.is_square_under_atack(0x72, Board.WHITE)
                and not self.is_square_under_atack(0x73, Board.WHITE)
                and not self.is_square_under_atack(0x74, Board.WHITE)
            ):
                return True

        return False

    def perft(self, depth: int) -> int:

        nodes = 0

        if depth == 0:
            return 1

        moves = self.generate_legal_moves()

        for move in moves:
            self.board.make_move(move)
            nodes += self.perft(depth - 1)
            self.board.undo_move(move)

        return nodes
