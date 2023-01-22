from game.pieces.piece import Piece
from game.pieces.knight import Knight
from game.pieces.king import King
import assets


class Centaur(Piece):
    def __init__(self, color):
        super().__init__(color, "centaur")
    
    def get_moves(self, pos, board):
        return King(self.color).get_moves(pos, board) + \
            Knight(self.color).get_moves(pos, board)