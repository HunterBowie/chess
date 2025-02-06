from game.pieces.piece import Piece
import assets


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "pawn")
        self.enpussantable = False
    
    def get_moves(self, pos, board):
        moves = []
        row_change = 1
        if self.color == "white":
            row_change = -1

        move = pos[0]+row_change, pos[1]
        if self.check_move(move, board, takes=False):
            moves.append(move)
        
            if not self.moved:
                move = pos[0]+row_change*2, pos[1]
                if self.check_move(move, board, takes=False):
                    moves.append(move)
        
        for col_change in [1, -1]:
            move = pos[0]+row_change, pos[1]+col_change
            if self.check_move(move, board, must_take=True):
                moves.append(move)
        
        return moves



    
