import pytest
from src.board import Board
from src.move_generator import MoveGenerator

@pytest.mark.parametrize("test_input, expected_number_of_moves", [
    ("8/6pp/8/2p5/2P5/8/PP1Pp3/8 w - - 0 0", 6),
    ("8/6pp/8/2p5/2P5/8/PP1Pp3/8 b - - 0 0", 5),
    ("8/8/8/8/8/p1p1p1p1/P1P1P1P1/8 w - - 0 0", 0),
    ("8/8/8/8/8/p1p1p1p1/P1P1P1P1/8 b - - 0 0", 0),
])
def test_generator_contains_all_basic_pawns_movements_without_capturing(test_input, expected_number_of_moves):
    board = Board()
    board.load_FEN(test_input)
    generator = MoveGenerator(board)

    assert len(generator.generate_moves()) == expected_number_of_moves

@pytest.mark.parametrize("test_input, expected_number_of_moves", [
    ("8/8/8/8/8/2p1p3/3P4/8 w - - 0 0", 4),
    ("8/8/8/8/8/2p1p3/3P4/8 b - - 0 0", 4),
    ("8/8/8/8/8/pppppppp/PPPPPPPP/8 w - - 0 0", 14),
    ("8/8/8/8/8/pppppppp/PPPPPPPP/8 b - - 0 0", 14),
    ("8/2p5/2Ppp3/p3Ppp1/1p4P1/1P5P/8/8 w - - 0 0", 3),
    ("8/2p5/2Ppp3/p3Ppp1/1p4P1/1P5P/8/8 b - - 0 0", 5),
    ("8/6p1/2p1p3/3P4/2P5/1P6/6PP/8 w - - 0 0", 9),
    ("8/6p1/2p1p3/3P4/2P5/1P6/6PP/8 b - - 0 0", 6),
])
def test_generator_contains_all_basic_pawns_movements_without_en_passant(test_input, expected_number_of_moves):
    board = Board()
    board.load_FEN(test_input)
    generator = MoveGenerator(board)

    assert len(generator.generate_moves()) == expected_number_of_moves
