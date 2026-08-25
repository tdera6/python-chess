from src.board import Board
from src.gui import GUI

board = Board()
board.load_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
gui = GUI(board=board)
gui.main_loop()
