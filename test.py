from game.board import Board
import minimax

board = Board()

# board.move_piece((0, 6), (2, 5))
# board.move_piece((6, 4), (4, 4))
score, start_pos, end_pos = minimax.minimax(board, 2, True)
board.move_piece(start_pos, end_pos)
print(minimax.get_board_score(board))


