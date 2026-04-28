from src.board import Board

PIECE_SYMBOLS = {
    Board.WHITE_KING: '♔',
    Board.WHITE_QUEEN: '♕',
    Board.WHITE_ROOK: '♖',
    Board.WHITE_BISHOP: '♗',
    Board.WHITE_KNIGHT: '♘',
    Board.WHITE_PAWN: '♙',

    Board.BLACK_KING: '♚',
    Board.BLACK_QUEEN: '♛',
    Board.BLACK_ROOK: '♜',
    Board.BLACK_BISHOP: '♝',
    Board.BLACK_KNIGHT: '♞',
    Board.BLACK_PAWN: '♟',

    Board.EMPTY: '·'
}

def draw_board(board: Board):
    
    for i in range(7, -1, -1):
        row = f"{i+1}|"
        row = row + " ".join(PIECE_SYMBOLS[square] for square in board.squares[16*i : 16*(i+1)-8])
        print(row)
    print("  a b c d e f g h")