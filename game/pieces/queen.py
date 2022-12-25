from game.pieces.piece import Piece
import assets


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, "queen")
    
    def get_moves(self, pos, board):
        return self.get_diagonal_moves(pos, board) + self.get_line_moves(pos, board)