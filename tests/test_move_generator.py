import pytest
from src.board import Board
from src.move_generator import MoveGenerator

@pytest.mark.parametrize("test_input, target_square, expected_number_of_moves", [
    ("8/8/8/8/8/8/3P4/8 w - - 0 0", 0x13, 2),
    ("8/3p4/8/8/8/8/8/8 b - - 0 0", 0x63, 2),
    ("8/8/8/8/8/4p3/4P3/8 w - - 0 0", 0x14, 0),
    ("8/8/8/8/8/4p3/4P3/8 b - - 0 0", 0x24, 0),
])
def test_single_pawn_movement_without_capturing(test_input: str, target_square: int, expected_number_of_moves: int):
    board = Board()
    board.load_FEN(test_input)
    generator = MoveGenerator(board)
    moves = []

    if board.turn == Board.WHITE:
        generator.generate_white_pawn_moves(target_square, Board.WHITE_PAWN, moves)
    elif board.turn == Board.BLACK:
        generator.generate_black_pawn_moves(target_square, Board.BLACK_PAWN, moves)
    
    assert len(moves) == expected_number_of_moves

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
def test_multiple_pawns_integration_without_en_passant(test_input, expected_number_of_moves):
    board = Board()
    board.load_FEN(test_input)
    generator = MoveGenerator(board)

    moves = generator.generate_moves()

    if board.turn == Board.WHITE:
        pawns_moves = [move for move in moves if move.piece_moved == Board.WHITE_PAWN]
    elif board.turn == Board.BLACK:
        pawns_moves = [move for move in moves if move.piece_moved == Board.BLACK_PAWN]


    assert len(pawns_moves) == expected_number_of_moves

@pytest.mark.parametrize("test_input, expected_number_of_moves", [
    ("8/8/8/8/8/2N5/8/8 w - - 0 0", 8),
    ("8/8/8/8/8/8/8/N7 w - - 0 0", 2),
    ("8/8/8/8/8/8/8/1N6 w - - 0 0", 3),
    ("8/8/8/8/8/2n5/8/8 b - - 0 0", 8),
    ("8/8/8/8/8/8/8/n7 b - - 0 0", 2),
    ("8/8/8/8/8/8/8/1n6 b - - 0 0", 3),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 0", 4),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b - - 0 0", 4),
    ("8/8/8/8/2p1p3/1p3p2/3N4/8 w - - 0 0", 6),
    ("8/8/8/8/2P1p3/1P3P2/3n4/8 b - - 0 0", 5),
])
def test_knights_movement(test_input, expected_number_of_moves):
    board = Board()
    board.load_FEN(test_input)
    generator = MoveGenerator(board)

    moves = generator.generate_moves()

    if board.turn == Board.WHITE:
        knight_moves = [move for move in moves if move.piece_moved == Board.WHITE_KNIGHT]
    elif board.turn == Board.BLACK:
        knight_moves = [move for move in moves if move.piece_moved == Board.BLACK_KNIGHT]


    assert len(knight_moves) == expected_number_of_moves

@pytest.mark.parametrize("test_input, expected_number_of_moves", [
    ("B7/8/8/8/8/8/8/8 w - - 0 0", 7),
    ("1B6/8/8/8/8/8/8/8 w - - 0 0", 7),
    ("8/8/8/8/4B3/8/8/8 w - - 0 0", 13),
    ("8/8/8/3P1P2/4B3/8/8/8 w - - 0 0", 6),
    ("8/8/8/3P1P2/4B3/8/2p5/8 w - - 0 0", 5),
    ("8/8/8/2P5/1B6/2p5/8/8 w - - 0 0", 3),
    ("8/8/8/8/8/8/1P6/B7 w - - 0 0", 0),
    ("b7/8/8/8/8/8/8/8 b - - 0 0", 7),
    ("1b6/8/8/8/8/8/8/8 b - - 0 0", 7),
    ("8/8/8/8/4b3/8/8/8 b - - 0 0", 13),
    ("8/8/8/3p1p2/4b3/8/8/8 b - - 0 0", 6),
    ("8/8/8/3p1p2/4b3/8/2P5/8 b - - 0 0", 5),
    ("8/8/8/2p5/1b6/2P5/8/8 b - - 0 0", 3),
    ("8/8/8/8/8/8/1p6/b7 b - - 0 0", 0),
])
def test_bishop_movement(test_input, expected_number_of_moves):
    board = Board()
    board.load_FEN(test_input)
    generator = MoveGenerator(board)

    moves = generator.generate_moves()

    if board.turn == Board.WHITE:
        bishop_moves = [move for move in moves if move.piece_moved == Board.WHITE_BISHOP]
    elif board.turn == Board.BLACK:
        bishop_moves = [move for move in moves if move.piece_moved == Board.BLACK_BISHOP]


    assert len(bishop_moves) == expected_number_of_moves

@pytest.mark.parametrize("test_input, expected_number_of_moves", [
    ("R7/8/8/8/8/8/8/8 w - - 0 0", 14),
    ("8/8/1R6/8/8/8/8/8 w - - 0 0", 14),
    ("8/8/4P3/4RP2/8/8/8/8 w - - 0 0", 8),
    ("8/8/4p3/4Rp2/8/8/8/8 w - - 0 0", 10),
    ("8/8/8/8/8/5r2/8/8 b - - 0 0", 14),
    ("8/8/8/8/8/8/8/r7 b - - 0 0", 14),
    ("8/8/8/P7/rP6/P7/8/8 b - - 0 0", 3),
    ("8/8/8/p7/rp6/p7/8/8 b - - 0 0", 0),
])
def test_rook_movement(test_input, expected_number_of_moves):
    board = Board()
    board.load_FEN(test_input)
    generator = MoveGenerator(board)

    moves = generator.generate_moves()

    if board.turn == Board.WHITE:
        rook_moves = [move for move in moves if move.piece_moved == Board.WHITE_ROOK]
    elif board.turn == Board.BLACK:
        rook_moves = [move for move in moves if move.piece_moved == Board.BLACK_ROOK]


    assert len(rook_moves) == expected_number_of_moves

@pytest.mark.parametrize("test_input, expected_number_of_moves", [
    ("8/8/8/8/1Q6/8/8/8 w - - 0 0", 23),
    ("8/8/3p4/1P6/1Q1p4/8/3p4/8 w - - 0 0", 12),
    ("Q7/PP6/8/8/8/8/8/8 w - - 0 0", 7),
    ("8/8/3ppp2/3pqp2/3ppp2/8/8/8 b - - 0 0", 0),
    ("8/2PpP3/2pQp3/2PpP3/8/8/8/8 w - - 0 0", 4),
])
def test_queen_movement(test_input, expected_number_of_moves):
    board = Board()
    board.load_FEN(test_input)
    generator = MoveGenerator(board)

    moves = generator.generate_moves()

    if board.turn == Board.WHITE:
        queen_moves = [move for move in moves if move.piece_moved == Board.WHITE_QUEEN]
    elif board.turn == Board.BLACK:
        queen_moves = [move for move in moves if move.piece_moved == Board.BLACK_QUEEN]


    assert len(queen_moves) == expected_number_of_moves

@pytest.mark.parametrize("test_input, expected_number_of_moves", [
    ("8/8/8/8/8/2K5/8/8 w - - 0 0", 8),
    ("8/8/8/8/1PPP4/1pKp4/8/8 w - - 0 0", 5),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 0", 0),
    ("7k/8/8/8/8/8/8/8 b - - 0 0", 3),
    ("8/8/8/6pp/6Pk/7p/8/8 b - - 0 0", 2),
])
def test_king_movement(test_input, expected_number_of_moves):
    board = Board()
    board.load_FEN(test_input)
    generator = MoveGenerator(board)

    moves = generator.generate_moves()

    if board.turn == Board.WHITE:
        king_moves = [move for move in moves if move.piece_moved == Board.WHITE_KING]
    elif board.turn == Board.BLACK:
        king_moves = [move for move in moves if move.piece_moved == Board.BLACK_KING]

    assert len(king_moves) == expected_number_of_moves

@pytest.mark.parametrize("test_input, expected_number_of_moves", [
    ("1k2R3/ppp5/8/8/8/8/P7/K7 b - - 0 0", 0),
    ("r1bqkbnr/p1pp1Qpp/1pn5/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b - - 0 0", 0),
    ("2k5/8/8/8/8/8/PPP5/1K2r2R w - - 0 0", 1),
    ("7k/8/8/8/8/6Qq/8/6RK w - - 0 0", 2),
])
def test_only_legal_moves_are_generated_without_special_moves(test_input: str, expected_number_of_moves: int):
    board = Board()
    board.load_FEN(test_input)
    generator = MoveGenerator(board)

    moves = generator.generate_legal_moves()

    assert len(moves) == expected_number_of_moves

@pytest.mark.parametrize("test_input, expected_number_of_moves", [
    ("8/3P4/8/8/8/8/8/8 w - - 0 0", 4),
    ("2q5/3P4/8/8/8/8/8/8 w - - 0 0", 8),
    ("8/8/8/8/8/8/2p5/8 b - - 0 0", 4),
    ("8/8/8/8/8/8/p7/1B6 b - - 0 0", 8),
])
def test_pawn_promotion_generates_correct_amount_of_moves(test_input: str, expected_number_of_moves: int):
    board = Board()
    board.load_FEN(test_input)
    generator = MoveGenerator(board)

    moves = generator.generate_moves()

    assert len(moves) == expected_number_of_moves