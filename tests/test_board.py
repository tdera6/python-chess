import pytest
from src.board import Board
from src.move import Move


def test_board_initializes_with_128_squares():
    board = Board()

    assert len(board.squares) == 128


def test_board_starts_with_white_turn():
    board = Board()

    assert board.turn == board.WHITE


def test_board_pieces_constants():
    assert Board.WHITE_PAWN == 1
    assert Board.BLACK_BISHOP == -3
    assert Board.WHITE_KING == 6
    assert Board.BLACK_QUEEN == -5


def test_board_setup_starting_position():
    board = Board()
    board.setup_starting_position()

    # Check some key squares for white pieces
    assert board.squares[0] == Board.WHITE_ROOK
    assert board.squares[1] == Board.WHITE_KNIGHT
    assert board.squares[4] == Board.WHITE_KING
    assert board.squares[16] == Board.WHITE_PAWN

    # Check some key squares for black pieces
    assert board.squares[112] == Board.BLACK_ROOK
    assert board.squares[113] == Board.BLACK_KNIGHT
    assert board.squares[116] == Board.BLACK_KING
    assert board.squares[96] == Board.BLACK_PAWN


@pytest.mark.parametrize(
    "test_input, expected_turn",
    [
        ("8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b - - 99 50", Board.BLACK),
        ("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1", Board.BLACK),
        ("4k2r/6r1/8/8/8/8/3R4/R3K3 w Qk - 0 1", Board.WHITE),
    ],
)
def test_board_load_fen_check_if_turn_is_correct(test_input: str, expected_turn: int):
    board = Board()
    board.load_FEN(test_input)

    assert board.turn == expected_turn


@pytest.mark.parametrize(
    "test_input, square, expected_piece",
    [
        ("8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b - - 99 50", 0x00, Board.EMPTY),
        ("8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b - - 99 50", 0x20, Board.WHITE_PAWN),
        ("8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b - - 99 50", 0x65, Board.BLACK_KING),
        ("4k2r/6r1/8/8/8/8/3R4/R3K3 w Qk - 0 1", 0x66, Board.BLACK_ROOK),
        ("4k2r/6r1/8/8/8/8/3R4/R3K3 w Qk - 0 1", 0x13, Board.WHITE_ROOK),
        (
            "1r2k1r1/pbppnp1p/1b3P2/8/Q7/B1PB1q2/P4PPP/3R2K1 w - - 0 21",
            0x30,
            Board.WHITE_QUEEN,
        ),
        (
            "1r2k1r1/pbppnp1p/1b3P2/8/Q7/B1PB1q2/P4PPP/3R2K1 w - - 0 21",
            0x25,
            Board.BLACK_QUEEN,
        ),
    ],
)
def test_board_load_fen_check_if_pieces_are_correct(
    test_input: str, square: int, expected_piece: int
):
    board = Board()
    board.load_FEN(test_input)

    assert board.squares[square] == expected_piece


def test_make_move_updates_piece_positions():
    board = Board()
    board.setup_starting_position()
    board.make_move(Move(16, 48, Board.WHITE_PAWN))

    assert board.squares[16] == Board.EMPTY
    assert board.squares[48] == Board.WHITE_PAWN


def test_make_move_swaps_player_turn():
    board = Board()
    board.setup_starting_position()

    board.make_move(Move(16, 48, Board.WHITE_PAWN))

    assert board.turn == Board.BLACK


def test_undo_move_updates_piece_positions():
    board = Board()
    board.load_FEN("rnbqkbnr/ppp1pppp/8/3P4/8/8/PPPP1PPP/RNBQKBNR b - - 0 0")

    board.undo_move(Move(52, 67, Board.WHITE_PAWN, Board.BLACK_PAWN))

    assert board.squares[52] == Board.WHITE_PAWN
    assert board.squares[67] == Board.BLACK_PAWN


def test_undo_move_swaps_back_player_turn():
    board = Board()
    board.load_FEN("rnbqkbnr/ppp1pppp/8/3P4/8/8/PPPP1PPP/RNBQKBNR b - - 0 0")

    board.undo_move(Move(52, 67, Board.WHITE_PAWN, Board.BLACK_PAWN))

    assert board.turn == Board.WHITE


@pytest.mark.parametrize(
    "fen, move",
    [
        (
            "3k4/7P/8/8/8/8/8/3K4 w - - 0 0",
            Move(
                0x67,
                0x77,
                Board.WHITE_PAWN,
                is_promotion=True,
                promotion_to=Board.WHITE_QUEEN,
            ),
        ),
        (
            "3k2r1/7P/8/8/8/8/8/3K4 w - - 0 0",
            Move(
                0x67,
                0x76,
                Board.WHITE_PAWN,
                Board.BLACK_ROOK,
                is_promotion=True,
                promotion_to=Board.WHITE_BISHOP,
            ),
        ),
        (
            "3k4/8/8/8/8/8/7p/3K2R1 b - - 0 0",
            Move(
                0x17,
                0x07,
                Board.BLACK_PAWN,
                is_promotion=True,
                promotion_to=Board.BLACK_BISHOP,
            ),
        ),
        (
            "3k4/8/8/8/8/8/7p/3K2R1 b - - 0 0",
            Move(
                0x17,
                0x06,
                Board.BLACK_PAWN,
                Board.WHITE_ROOK,
                is_promotion=True,
                promotion_to=Board.BLACK_QUEEN,
            ),
        ),
    ],
)
def test_make_move_updates_piece_position_after_promotion(fen: str, move: Move):
    board = Board()
    board.load_FEN(fen)
    board.make_move(move)

    assert board.squares[move.to_square] == move.promotion_to
    assert board.squares[move.from_square] == Board.EMPTY


@pytest.mark.parametrize(
    "fen, move",
    [
        (
            "3k3Q/8/8/8/8/8/8/3K4 w - - 0 0",
            Move(
                0x67,
                0x77,
                Board.WHITE_PAWN,
                is_promotion=True,
                promotion_to=Board.WHITE_QUEEN,
            ),
        ),
        (
            "3k2B1/8/8/8/8/8/8/3K4 w - - 0 0",
            Move(
                0x67,
                0x76,
                Board.WHITE_PAWN,
                Board.BLACK_ROOK,
                is_promotion=True,
                promotion_to=Board.WHITE_BISHOP,
            ),
        ),
        (
            "3k4/8/8/8/8/8/8/3K2Rb b - - 0 0",
            Move(
                0x17,
                0x07,
                Board.BLACK_PAWN,
                is_promotion=True,
                promotion_to=Board.BLACK_BISHOP,
            ),
        ),
        (
            "3k4/8/8/8/8/8/8/3K2q1 b - - 0 0",
            Move(
                0x17,
                0x06,
                Board.BLACK_PAWN,
                Board.WHITE_ROOK,
                is_promotion=True,
                promotion_to=Board.BLACK_QUEEN,
            ),
        ),
    ],
)
def test_undo_move_updates_piece_position_to_state_before_promotion(
    fen: str, move: Move
):
    board = Board()
    board.load_FEN(fen)
    board.undo_move(move)

    assert board.squares[move.to_square] == move.piece_captured
    assert board.squares[move.from_square] == move.piece_moved


@pytest.mark.parametrize(
    "fen, square",
    [
        ("4k3/8/8/8/3pP3/3P4/8/4K3 b - e3 0 0", 0x24),
        ("4k3/8/8/8/2PpP3/3P4/8/4K3 b - c3 0 0", 0x22),
        ("4k3/8/8/8/2PpPpP1/3P4/8/4K3 b - g3 0 0", 0x26),
    ],
)
def test_load_FEN_correctly_updates_en_passant_possible_square(fen: str, square: int):
    board = Board()
    board.load_FEN(fen)

    assert board.en_passant_square == square


@pytest.mark.parametrize(
    "fen, move, from_square, to_square, captured_pawn_square",
    [
        (
            "4k3/8/8/8/2PpPpP1/3P4/8/4K3 b - e3 0 0",
            Move(
                0x33,
                0x24,
                Board.BLACK_PAWN,
                Board.WHITE_PAWN,
                is_en_passant=True,
                previous_en_passant_square=0x24,
            ),
            0x33,
            0x24,
            0x34,
        ),
        (
            "4k3/8/8/8/2PpPpP1/3P4/8/4K3 b - c3 0 0",
            Move(
                0x33,
                0x22,
                Board.BLACK_PAWN,
                Board.WHITE_PAWN,
                is_en_passant=True,
                previous_en_passant_square=0x22,
            ),
            0x33,
            0x22,
            0x32,
        ),
        (
            "4k3/8/8/8/2PpPpP1/3P4/8/4K3 b - g3 0 0",
            Move(
                0x35,
                0x26,
                Board.BLACK_PAWN,
                Board.WHITE_PAWN,
                is_en_passant=True,
                previous_en_passant_square=0x26,
            ),
            0x35,
            0x26,
            0x36,
        ),
        (
            "4k3/8/3p4/2pPpPp1/8/8/8/4K3 w - c6 0 0",
            Move(
                0x43,
                0x52,
                Board.WHITE_PAWN,
                Board.BLACK_PAWN,
                is_en_passant=True,
                previous_en_passant_square=0x52,
            ),
            0x43,
            0x52,
            0x42,
        ),
    ],
)
def test_make_move_correctly_updates_pieces_position_after_en_passant(
    fen: str, move: Move, from_square: int, to_square: int, captured_pawn_square: int
):
    board = Board()
    board.load_FEN(fen)

    board.make_move(move)

    assert board.squares[from_square] == Board.EMPTY
    assert board.squares[to_square] == move.piece_moved
    assert board.squares[captured_pawn_square] == Board.EMPTY


@pytest.mark.parametrize(
    "fen, move, en_passant_square",
    [
        (
            "4k3/8/8/8/3p4/8/4P3/4K3 w - - 0 0",
            Move(0x14, 0x34, Board.WHITE_PAWN, is_double_pawn_move=True),
            0x24,
        ),
        (
            "4k3/4p3/8/3P4/8/8/8/3K4 b - - 0 0",
            Move(0x64, 0x44, Board.BLACK_PAWN, is_double_pawn_move=True),
            0x54,
        ),
    ],
)
def test_make_move_correctly_updates_possible_en_passant_square(
    fen: str, move: Move, en_passant_square: int
):
    board = Board()
    board.load_FEN(fen)

    board.make_move(move)

    assert board.en_passant_square == en_passant_square


@pytest.mark.parametrize(
    "fen, move, from_square, to_square, captured_pawn_square",
    [
        (
            "3k4/8/8/8/8/3p4/8/3K4 w - - 0 0",
            Move(
                0x34,
                0x23,
                Board.BLACK_PAWN,
                Board.WHITE_PAWN,
                is_en_passant=True,
                previous_en_passant_square=0x23,
            ),
            0x34,
            0x23,
            0x33,
        ),
        (
            "rnbqkbnr/ppp1p1pp/5P2/3p4/8/8/PPPP1PPP/RNBQKBNR b - - 0 0",
            Move(
                0x44,
                0x55,
                Board.WHITE_PAWN,
                Board.BLACK_PAWN,
                is_en_passant=True,
                previous_en_passant_square=0x55,
            ),
            0x44,
            0x55,
            0x45,
        ),
    ],
)
def test_undo_move_correctly_updates_pieces_position_after_en_passant(
    fen: str, move: Move, from_square: int, to_square: int, captured_pawn_square: int
):
    board = Board()
    board.load_FEN(fen)

    board.undo_move(move)

    assert board.squares[from_square] == move.piece_moved
    assert board.squares[to_square] == Board.EMPTY
    assert board.squares[captured_pawn_square] == move.piece_captured


@pytest.mark.parametrize(
    "fen, move, en_passant_square",
    [
        (
            "3k4/8/8/8/8/3p4/8/3K4 w - - 0 0",
            Move(
                0x34,
                0x23,
                Board.BLACK_PAWN,
                Board.WHITE_PAWN,
                is_en_passant=True,
                previous_en_passant_square=0x23,
            ),
            0x23,
        ),
        (
            "rnbqkbnr/ppp1p1pp/5P2/3p4/8/8/PPPP1PPP/RNBQKBNR b - - 0 0",
            Move(
                0x44,
                0x55,
                Board.WHITE_PAWN,
                Board.BLACK_PAWN,
                is_en_passant=True,
                previous_en_passant_square=0x55,
            ),
            0x55,
        ),
    ],
)
def test_undo_move_correctly_brings_back_possible_en_passant_square(
    fen: str, move: Move, en_passant_square: int
):
    board = Board()
    board.load_FEN(fen)

    board.undo_move(move)

    assert board.en_passant_square == en_passant_square


@pytest.mark.parametrize(
    "fen, can_white_short_castle, can_white_long_castle, can_black_short_castle, can_black_long_castle",
    [
        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0",
            True,
            True,
            True,
            True,
        ),
        (
            "rnbqkbnr/pppppppp/8/8/R7/8/1PPPPPPP/1NBQKBNR w Kkq - 0 0",
            True,
            False,
            True,
            True,
        ),
        (
            "1nbqkbn1/1pppppp1/r6r/p6p/8/3PP3/PPPNNPPP/R1BQKB1R w KQ - 0 0",
            True,
            True,
            False,
            False,
        ),
        (
            "1nbqkbn1/1pppppp1/r6r/p6p/P6P/R2PP2R/1PPNNPP1/2BQKB2 w - - 0 0",
            False,
            False,
            False,
            False,
        ),
    ],
)
def test_load_FEN_correctly_setup_castling_rights(
    fen: str,
    can_white_short_castle: int,
    can_white_long_castle: int,
    can_black_short_castle: int,
    can_black_long_castle: int,
):
    board = Board()
    board.load_FEN(fen)

    assert board.can_white_short_castle == can_white_short_castle
    assert board.can_white_long_castle == can_white_long_castle
    assert board.can_black_short_castle == can_black_short_castle
    assert board.can_black_long_castle == can_black_long_castle


@pytest.mark.parametrize(
    "fen, move, can_white_short_castle, can_white_long_castle, can_black_short_castle, can_black_long_castle",
    [
        (
            "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 0",
            Move(0x04, 0x14, Board.WHITE_KING),
            False,
            False,
            True,
            True,
        ),
        (
            "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 0",
            Move(0x00, 0x40, Board.WHITE_ROOK),
            True,
            False,
            True,
            True,
        ),
        (
            "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 0",
            Move(0x07, 0x47, Board.WHITE_ROOK),
            False,
            True,
            True,
            True,
        ),
        (
            "r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 0",
            Move(0x74, 0x64, Board.BLACK_KING),
            True,
            True,
            False,
            False,
        ),
        (
            "r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 0",
            Move(0x77, 0x47, Board.BLACK_ROOK),
            True,
            True,
            False,
            True,
        ),
        (
            "r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 0",
            Move(0x70, 0x60, Board.BLACK_ROOK),
            True,
            True,
            True,
            False,
        ),
        (
            "r3k2r/8/8/8/8/8/6B1/R3K2R w KQkq - 0 0",
            Move(0x16, 0x70, Board.WHITE_BISHOP, Board.BLACK_ROOK),
            True,
            True,
            True,
            False,
        ),
        (
            "r3k2r/8/8/8/8/8/1b6/R3K2R b KQkq - 0 0",
            Move(0x11, 0x00, Board.BLACK_BISHOP, Board.WHITE_ROOK),
            True,
            False,
            True,
            True,
        ),
    ],
)
def test_make_move_withdraw_castling_rights(
    fen: str,
    move: Move,
    can_white_short_castle: bool,
    can_white_long_castle: bool,
    can_black_short_castle: bool,
    can_black_long_castle: bool,
):
    board = Board()
    board.load_FEN(fen)

    board.make_move(move)

    assert board.can_white_short_castle == can_white_short_castle
    assert board.can_white_long_castle == can_white_long_castle
    assert board.can_black_short_castle == can_black_short_castle
    assert board.can_black_long_castle == can_black_long_castle


def test_make_move_correctly_updates_piece_positions_after_white_short_castle():
    board = Board()
    board.load_FEN("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 0")

    board.make_move(
        Move(0x04, 0x06, Board.WHITE_KING, is_castling=True, is_short_castling=True)
    )

    assert board.squares[0x04] == Board.EMPTY
    assert board.squares[0x07] == Board.EMPTY
    assert board.squares[0x06] == Board.WHITE_KING
    assert board.squares[0x05] == Board.WHITE_ROOK


def test_make_move_correctly_updates_piece_positions_after_white_long_castle():
    board = Board()
    board.load_FEN("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 0")

    board.make_move(
        Move(0x04, 0x02, Board.WHITE_KING, is_castling=True, is_long_castling=True)
    )

    assert board.squares[0x04] == Board.EMPTY
    assert board.squares[0x00] == Board.EMPTY
    assert board.squares[0x02] == Board.WHITE_KING
    assert board.squares[0x03] == Board.WHITE_ROOK


def test_make_move_correctly_updates_piece_positions_after_black_short_castle():
    board = Board()
    board.load_FEN("r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 0")

    board.make_move(
        Move(0x74, 0x76, Board.BLACK_KING, is_castling=True, is_short_castling=True)
    )

    assert board.squares[0x74] == Board.EMPTY
    assert board.squares[0x77] == Board.EMPTY
    assert board.squares[0x76] == Board.BLACK_KING
    assert board.squares[0x75] == Board.BLACK_ROOK


def test_make_move_correctly_updates_piece_positions_after_black_long_castle():
    board = Board()
    board.load_FEN("r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 0")

    board.make_move(
        Move(0x74, 0x72, Board.BLACK_KING, is_castling=True, is_long_castling=True)
    )

    assert board.squares[0x74] == Board.EMPTY
    assert board.squares[0x70] == Board.EMPTY
    assert board.squares[0x72] == Board.BLACK_KING
    assert board.squares[0x73] == Board.BLACK_ROOK


def test_make_move_take_away_castling_rights_after_castling():
    board = Board()
    board.load_FEN("r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 0")

    board.make_move(
        Move(0x74, 0x72, Board.BLACK_KING, is_castling=True, is_long_castling=True)
    )

    assert not board.can_black_long_castle
    assert not board.can_black_short_castle


def test_undo_move_correctly_inverts_piece_positions_after_white_short_castle():
    board = Board()
    board.load_FEN("r3k2r/8/8/8/8/8/8/R4RK1 b kq - 0 0")

    board.undo_move(
        Move(
            0x04,
            0x06,
            Board.WHITE_KING,
            is_castling=True,
            is_short_castling=True,
            previous_black_long_castle=True,
            previous_black_short_castle=True,
            previous_white_long_castle=True,
            previous_white_short_castle=True,
        )
    )

    assert board.squares[0x04] == Board.WHITE_KING
    assert board.squares[0x07] == Board.WHITE_ROOK
    assert board.squares[0x06] == Board.EMPTY
    assert board.squares[0x05] == Board.EMPTY


def test_undo_move_correctly_inverts_piece_positions_after_white_long_castle():
    board = Board()
    board.load_FEN("r3k2r/8/8/8/8/8/8/2KR3R b kq - 0 0")

    board.undo_move(
        Move(
            0x04,
            0x02,
            Board.WHITE_KING,
            is_castling=True,
            is_long_castling=True,
            previous_black_long_castle=True,
            previous_black_short_castle=True,
            previous_white_long_castle=True,
            previous_white_short_castle=True,
        )
    )

    assert board.squares[0x04] == Board.WHITE_KING
    assert board.squares[0x00] == Board.WHITE_ROOK
    assert board.squares[0x02] == Board.EMPTY
    assert board.squares[0x03] == Board.EMPTY


def test_undo_move_correctly_inverts_piece_positions_after_black_short_castle():
    board = Board()
    board.load_FEN("r4rk1/8/8/8/8/8/8/R3K2R w KQ - 0 0")

    board.undo_move(
        Move(
            0x74,
            0x76,
            Board.BLACK_KING,
            is_castling=True,
            is_short_castling=True,
            previous_black_long_castle=True,
            previous_black_short_castle=True,
            previous_white_long_castle=True,
            previous_white_short_castle=True,
        )
    )

    assert board.squares[0x74] == Board.BLACK_KING
    assert board.squares[0x77] == Board.BLACK_ROOK
    assert board.squares[0x76] == Board.EMPTY
    assert board.squares[0x75] == Board.EMPTY


def test_undo_move_correctly_inverts_piece_positions_after_black_long_castle():
    board = Board()
    board.load_FEN("2kr3r/8/8/8/8/8/8/R3K2R w KQ - 0 0")

    board.undo_move(
        Move(
            0x74,
            0x72,
            Board.BLACK_KING,
            is_castling=True,
            is_long_castling=True,
            previous_black_long_castle=True,
            previous_black_short_castle=True,
            previous_white_long_castle=True,
            previous_white_short_castle=True,
        )
    )

    assert board.squares[0x74] == Board.BLACK_KING
    assert board.squares[0x70] == Board.BLACK_ROOK
    assert board.squares[0x72] == Board.EMPTY
    assert board.squares[0x73] == Board.EMPTY


def test_undo_move_gives_back_castling_rights_after_castling():
    board = Board()
    board.load_FEN("2kr3r/8/8/8/8/8/8/R3K2R w KQ - 0 0")

    board.undo_move(
        Move(
            0x74,
            0x72,
            Board.BLACK_KING,
            is_castling=True,
            is_long_castling=True,
            previous_black_long_castle=True,
            previous_black_short_castle=True,
            previous_white_long_castle=True,
            previous_white_short_castle=True,
        )
    )

    assert board.can_black_long_castle
    assert board.can_black_short_castle


@pytest.mark.parametrize(
    "fen, expected_white_king_square, expected_black_king_square",
    [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0", 0x04, 0x74),
        ("7k/8/8/p7/rp6/p7/8/7K w - - 0 0", 0x07, 0x77),
    ],
)
def test_board_finds_squares_of_kings(
    fen: str, expected_white_king_square: int, expected_black_king_square: int
):
    board = Board()
    board.load_FEN(fen)

    assert board.white_king_square == expected_white_king_square
    assert board.black_king_square == expected_black_king_square


@pytest.mark.parametrize(
    "fen, move, expected_white_king_square, expected_black_king_square",
    [
        (
            "7k/8/8/p7/rp6/p7/8/7K w - - 0 0",
            Move(0x07, 0x06, Board.WHITE_KING),
            0x06,
            0x77,
        ),
        (
            "7k/8/8/p7/rp6/p7/8/7K b - - 0 0",
            Move(0x77, 0x76, Board.BLACK_KING),
            0x07,
            0x76,
        ),
        (
            "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w - - 0 0",
            Move(
                0x04, 0x06, Board.WHITE_KING, is_castling=True, is_short_castling=True
            ),
            0x06,
            0x74,
        ),
        (
            "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w - - 0 0",
            Move(
                0x74,
                0x72,
                Board.BLACK_KING,
                is_castling=True,
                is_long_castling=True,
            ),
            0x04,
            0x72,
        ),
    ],
)
def test_make_move_updates_king_position(
    fen: str,
    move: Move,
    expected_white_king_square: int,
    expected_black_king_square: int,
):
    board = Board()
    board.load_FEN(fen)
    board.make_move(move)

    assert board.white_king_square == expected_white_king_square
    assert board.black_king_square == expected_black_king_square


@pytest.mark.parametrize(
    "fen, move, expected_white_king_square, expected_black_king_square",
    [
        (
            "7k/8/8/p7/rp6/p7/8/6K1 w - - 0 0",
            Move(0x07, 0x06, Board.WHITE_KING),
            0x07,
            0x77,
        ),
        (
            "6k1/8/8/p7/rp6/p7/8/7K b - - 0 0",
            Move(0x77, 0x76, Board.BLACK_KING),
            0x07,
            0x77,
        ),
        (
            "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R4RK1 w - - 0 0",
            Move(
                0x04, 0x06, Board.WHITE_KING, is_castling=True, is_short_castling=True
            ),
            0x04,
            0x74,
        ),
        (
            "2kr3r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w - - 0 0",
            Move(
                0x74,
                0x72,
                Board.BLACK_KING,
                is_castling=True,
                is_long_castling=True,
            ),
            0x04,
            0x74,
        ),
    ],
)
def test_undo_move_updates_king_position(
    fen: str,
    move: Move,
    expected_white_king_square: int,
    expected_black_king_square: int,
):
    board = Board()
    board.load_FEN(fen)
    board.undo_move(move)

    assert board.white_king_square == expected_white_king_square
    assert board.black_king_square == expected_black_king_square
