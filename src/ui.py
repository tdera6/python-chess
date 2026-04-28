from src.board import Board
from rich.console import Console

console = Console(highlight=False)

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

    Board.EMPTY: ' '
}

def draw_board(board: Board):
    for row in range(7, -1, -1):
        row_str = f"[bold]{row+1}[/bold] "
        for column in range(8):
            piece = board.squares[16 * row + column]
            piece_color = "#FFFFFF" if piece > 0 else "#282828"
            square_color = "#C5C5C5" if (row + column) % 2 else "#769656"

            row_str = row_str + f"[{piece_color} on {square_color}]{PIECE_SYMBOLS[-abs(piece)]} [/{piece_color} on {square_color}]"

        console.print(row_str)

    console.print("  [bold]a b c d e f g h[/bold]")