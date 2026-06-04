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
