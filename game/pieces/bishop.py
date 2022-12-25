from game.pieces.piece import Piece
import assets


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, "bishop")
    
    def get_moves(self, pos, board):
        return self.get_diagonal_moves(pos, board)