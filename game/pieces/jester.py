from game.pieces.piece import Piece
from game.pieces.knight import Knight
from game.pieces.king import King
from game.pieces.bishop import Bishop
from game.pieces.rook import Rook
import assets, random


class Jester(Piece):
    def __init__(self, color):
        super().__init__(color, "jester")
        self.moves = []
        self.start_of_turn = False
    
    def _change_moves(self, pos, board):
        self.moves.clear()
        new_moves = Rook(self.color).get_moves(pos, board) + \
            Knight(self.color).get_moves(pos, board) + \
            Bishop(self.color).get_moves(pos, board) + \
            King(self.color).get_moves(pos, board)
        
        for i in range(8):
            move = random.choice(new_moves)
            new_moves.remove(move)
            self.moves.append(move)
            if not new_moves:
                break
    
    def on_start_of_turn(self):
        self.start_of_turn = True
    
    def get_moves(self, pos, board):
        if self.start_of_turn or not self.moves:
            self._change_moves(pos, board)
            self.start_of_turn = False
        moves = []
        for move in self.moves:
            if not type(board[move[0]][move[1]]) is King:
                moves.append(move)
        return moves