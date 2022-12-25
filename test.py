pieces = ["rook", "knight", "king", "queen", "bishop", "pawn"]

string = '"dark_square": windowgui.load_image("dark_square", IMAGES_DIR),'

for piece in pieces:
    for color in ["white", "black"]:
        print(f'"{color}_{piece}": windowgui.load_image("{color}_{piece}", IMAGES_DIR),')




class Board:
    def __init__(self):
        self.board = [[None for i in range(8)] for i in range(8)]
    
    def check_move(self, move):
        if move[0] < 0 or move[1] < 0:
            return False

        try:
            if self.board[move[0]][move[1]]:
                return False
            return True

        except IndexError:
            return False
    
    def get_line_moves(self, pos):
        moves = []
        for row_change in range(1, 8):
            move = pos[0]+row_change, pos[1]
            if not self.check_move(move):
                break
            moves.append(move)
            
        for row_change in range(-7, 0):
            move = pos[0]+row_change, pos[1]
            if not self.check_move(move):
                break
            moves.append(move)
        for col_change in range(1, 8):
            move = pos[0]+row_change, pos[1]
            if not self.check_move(move):
                break
            moves.append(move)
        for col_change in range(-7, 0):
            move = pos[0]+row_change, pos[1]
            if not self.check_move(move):
                break
            moves.append(move)
        
        return moves
    
    def get_diagonal_moves(self, pos):
        moves = []
        for pos_change in range(1, 8):
            move = pos[0]+pos_change, pos[1]+pos_change
            if not self.check_move(move):
                break
            moves.append(move)
        for pos_change in range(1, 8):
            move = pos[0]+pos_change, pos[1]-pos_change
            if not self.check_move(move):
                break
            moves.append(move)
        for pos_change in range(1, 8):
            move = pos[0]-pos_change, pos[1]+pos_change
            if not self.check_move(move):
                break
            moves.append(move)
        for pos_change in range(1, 8):
            move = pos[0]-pos_change, pos[1]-pos_change
            if not self.check_move(move):
                break
            moves.append(move)
        return moves
    
    def get_knight_moves(self, pos):
        moves = []
        possible_pos_changes = [(2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for row_change, col_change in possible_pos_changes:
            move = pos[0]+row_change, pos[1]+col_change
            if self.check_move(move):
                moves.append(move)
        return moves
    
    def get_king_moves(self, pos):
        moves = []
        possible_pos_changes = [(1, 0), (1, 1), (1, -1), (-1, 0), 
        (-1, 1), (-1, -1), (0, 1), (0, -1)]

        for row_change, col_change in possible_pos_changes:
            move = pos[0]+row_change, pos[1]+col_change
            if self.check_move(move):
                moves.append(move)
        return moves





board = Board()

print(len(board.get_king_moves((5, 5))))