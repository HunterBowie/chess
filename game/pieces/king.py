from game.pieces.piece import Piece
import assets


class King(Piece):
    def __init__(self, color):
        super().__init__(color, "king")
    
    def get_moves(self, pos, board):
        moves = []
        possible_pos_changes = [(1, 0), (1, 1), (1, -1), (-1, 0), 
        (-1, 1), (-1, -1), (0, 1), (0, -1)]

        for row_change, col_change in possible_pos_changes:
            move = pos[0]+row_change, pos[1]+col_change
            if self.check_move(move, board):
                moves.append(move)
        return moves