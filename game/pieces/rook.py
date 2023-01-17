from game.pieces.piece import Piece
import assets

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, "rook")
    
    def get_moves(self, pos, board):
        return self.get_line_moves(pos, board) 