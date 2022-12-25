import assets, constants, pygame, windowgui
from game.pieces import Rook, Bishop, King, Queen, Knight, Pawn, Centaur

class Game:
    def __init__(self, window):
        self.window = window
        self.board = [[None for i in range(8)] for i in range(8)]
        self.board[5][5] = Centaur("white")
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
               

        
