from game.pieces.piece import Piece
from game.pieces.knight import Knight
from game.pieces.king import King
from game.pieces.bishop import Bishop
from game.pieces.rook import Rook
import assets, random


class Joker(Piece):
    def __init__(self, color):
        super().__init__(color, "joker")
        self.moves = []
        self.start_of_turn = False
    
    def _change_moves(self, pos, board):
        moves = Rook(self.color).get_moves(pos, board) + \
            Knight(self.color).get_moves(pos, board) + \
            Bishop(self.color).get_moves(pos, board) + \
            King(self.color).get_moves(pos, board)
        self.moves.clear()
        for i in range(8):
            index = random.randint(0, len(moves)-1)
            self.moves.append(moves.pop(index))
    
    def on_start_of_turn(self):
        self.start_of_turn = True
    
    def get_moves(self, pos, board):
        if self.start_of_turn or not self.moves:
            self._change_moves(pos, board)
            self.start_of_turn = False
        return self.moves