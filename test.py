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




import assets, constants, pygame, windowgui
from game.pieces import Rook, Bishop, King, Queen, Knight, Pawn, Centaur

class Game:
    def __init__(self, window):
        self.window = window
        self.board = [[None for i in range(8)] for i in range(8)]
        self.init_pieces()
        self.possible_move_squares = []
        self.selected = None
    
    def init_pieces(self):
        self.init_back_row(0, "black")
        self.init_pawn_row(1, "black", "down")
        self.init_pawn_row(6, "white", "up")
        self.init_back_row(7, "white")
    
    def init_pawn_row(self, row, color, direction):
        for col in range(8):
            self.board[row][col] = Pawn(color, direction)

    def init_back_row(self, row, color):
        self.board[row][0] = Rook(color)
        self.board[row][1] = Knight(color)
        self.board[row][2] = Bishop(color)
        self.board[row][3] = Queen(color)
        self.board[row][4] = King(color)
        self.board[row][5] = Bishop(color)
        self.board[row][6] = Knight(color)
        self.board[row][7] = Rook(color)
    
    def get_mouse_board_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        col = mouse_pos[0]//constants.SQUARE_WIDTH
        row = mouse_pos[1]//constants.SQUARE_WIDTH
        return row, col
    
    def eventloop(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.selected:
                if self.get_mouse_board_pos() in self.possible_move_squares:
                    row, col = self.selected
                    piece = self.board[row][col]
                    self.board[row][col] = None
                    row, col = self.get_mouse_board_pos()
                    self.board[row][col] = piece
                    self.possible_move_squares.clear()
                    self.selected = None
                    piece.moved = True
                    
                else:
                    row, col = self.get_mouse_board_pos()
                    if (row, col) == self.selected:
                        self.possible_move_squares.clear()
                        self.selected = None
                        return None
                    piece = self.board[row][col]
                    if piece:
                        self.possible_move_squares = piece.get_moves((row, col), self.board)
                        self.selected = row, col
                
            else:
                row, col = self.get_mouse_board_pos()
                piece = self.board[row][col]
                if piece:
                    self.possible_move_squares = piece.get_moves((row, col), self.board)
                    self.selected = row, col
                    
    
    def draw_dot(self, pos):
        surf = pygame.Surface((constants.SQUARE_WIDTH, constants.SQUARE_WIDTH), pygame.SRCALPHA)
        pygame.draw.circle(surf, windowgui.Colors.GREY, (constants.SQUARE_WIDTH//2, constants.SQUARE_WIDTH//2), 15)
        surf.set_alpha(100)
        self.window.screen.blit(surf, pos)
    
    def update(self):
        for row in range(8):
            for col in range(8):
                pos = col*constants.SQUARE_WIDTH, row*constants.SQUARE_WIDTH
                if (row + col) % 2 == 0:
                    self.window.screen.blit(assets.IMAGES["light_square"], pos)
                else:
                    self.window.screen.blit(assets.IMAGES["dark_square"], pos)
                
                piece = self.board[row][col]
                if piece:
                    self.window.screen.blit(piece.image, pos)

                if (row, col) in self.possible_move_squares:
                    self.draw_dot(pos)
               

        
