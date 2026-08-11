import pytest

from src.board import Board
from src.engine import ChessEngine
from src.move import Move


@pytest.mark.parametrize(
    "fen, expected_eval",
    [
        ("3k4/8/8/8/8/8/7p/3K2R1 w - - 0 0", 4),
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0", 0),
        ("r1bqkbnr/1ppp1Qpp/p1n5/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 0", 1),
        ("7k/5Q2/8/8/8/8/8/3K4 b - - 0 0", 9),
        ("7k/5Q2/8/8/8/8/q7/q2K4 w - - 0 0", -9),
        ("4k3/8/8/8/8/8/PPPPPPPP/RNBQKBNR w KQ - 0 0", 39),
        ("rnbqkbnr/pppppppp/8/8/8/8/8/4K3 w kq - 0 0", -39),
    ],
)
def test_correct_board_evaluation(fen: str, expected_eval: int):
    board = Board()
    board.load_FEN(fen)

    engine = ChessEngine(board)

    assert engine.evaluate_position(engine.board) == expected_eval


@pytest.mark.parametrize(
    "fen, correct_square_from, correct_square_to",
    [
        (
            "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 0",
            0x25,
            0x65,
        ),
        (
            "7k/6pp/8/8/8/8/8/1Q3K2 w - - 0 0",
            0x01,
            0x71,
        ),
        ("3k4/2q5/1r6/8/8/8/K7/8 b - - 0 0", 0x62, 0x60),
        ("3K4/2Q5/1R6/8/8/8/k7/8 w - - 0 0", 0x62, 0x60),
    ],
)
def test_mini_max_finds_mate_in_one(
    fen: str, correct_square_from: int, correct_square_to: int
):
    board = Board()
    board.load_FEN(fen)

    engine = ChessEngine(board)

    best_move = engine.find_best_move()

    assert best_move.from_square == correct_square_from
    assert best_move.to_square == correct_square_to


@pytest.mark.parametrize(
    "move, expected_prority",
    [
        (Move(0x01, 0x02, Board.WHITE_QUEEN, Board.BLACK_PAWN), 1),
        (Move(0x01, 0x02, Board.BLACK_KNIGHT, Board.WHITE_BISHOP), 27),
        (Move(0x01, 0x02, Board.BLACK_PAWN, Board.WHITE_QUEEN), 89),
    ],
)
def test_engine_move_score_priority(move: Move, expected_prority: int):
    board = Board()
    board.setup_starting_position()
    engine = ChessEngine(board)

    assert engine.score_move_priority(move) == expected_prority
