import assets 


class Piece:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.moved = False
        self._last_move_occupied = False
    
    def __repr__(self):
        return self.name[0].upper() + self.name[1:] + "(\"" + self.color + "\")"
    
    def get_image(self):
        return assets.IMAGES[self.color + "_" + self.name]
    
    def on_start_of_turn(self):
        pass

    def get_moves(self, pos, board):
        return []

    def check_move(self, move, board, takes=True, must_take=False):
        self._last_move_occupied = False
        if move[0] < 0 or move[1] < 0:
            return False

        try:
            if board[move[0]][move[1]]:
                self._last_move_occupied = True
                if board[move[0]][move[1]].color != self.color and takes:
                    return True
                return False
            
            if must_take:
                return False
            
            return True
            
            

        except IndexError:
            return False
    
    def get_line_moves(self, pos, board, jumps=False):
        moves = []
        for row_change in range(1, 8):
            move = pos[0]+row_change, pos[1]
            if not self.check_move(move, board):
                break
            moves.append(move)
            if self._last_move_occupied and not jumps:
                break
        for row_change in range(1, 8):
            move = pos[0]-row_change, pos[1]
            if not self.check_move(move, board):
                break
            moves.append(move)
            if self._last_move_occupied and not jumps:
                break
        for col_change in range(1, 8):
            move = pos[0], pos[1]+col_change
            if not self.check_move(move, board):
                break
            moves.append(move)
            if self._last_move_occupied and not jumps:
                break
        for col_change in range(1, 8):
            move = pos[0], pos[1]-col_change
            if not self.check_move(move, board):
                break
            moves.append(move)
            if self._last_move_occupied and not jumps:
                break
        return moves
    
    def get_diagonal_moves(self, pos, board, jumps=False):
        moves = []
        for pos_change in range(1, 8):
            move = pos[0]+pos_change, pos[1]+pos_change
            if not self.check_move(move, board):
                break
            moves.append(move)
            if self._last_move_occupied and not jumps:
                break
        for pos_change in range(1, 8):
            move = pos[0]+pos_change, pos[1]-pos_change
            if not self.check_move(move, board):
                break
            moves.append(move)
            if self._last_move_occupied and not jumps:
                break
        for pos_change in range(1, 8):
            move = pos[0]-pos_change, pos[1]+pos_change
            if not self.check_move(move, board):
                break
            moves.append(move)
            if self._last_move_occupied and not jumps:
                break
        for pos_change in range(1, 8):
            move = pos[0]-pos_change, pos[1]-pos_change
            if not self.check_move(move, board):
                break
            moves.append(move)
            if self._last_move_occupied and not jumps:
                break
        return moves

