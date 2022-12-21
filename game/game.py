import assets, constants
from game.pieces.piece import Piece

class Game:
    def __init__(self, window):
        self.window = window
        self.board = []
        self.pieces.append(Piece(5, 5, "white", assets.IMAGES["white_rook"]))
    
    def init_pieces(self):
        self.init_back_row(0, "black")
        self.init_pawn_row(1, "black")
        self.init_pawn_row(6, "white")
        self.init_back_row(7, "white")
    
    def init_pawn_row(self, row, color):
        for col in range(8):
            self.board.append(Piece(row, col, color, assets.IMAGES[color + "_pawn"]))

    def init_back_row(self, row, color):
        self.board.append(Piece(row, 0, assets.IMAGES[color + "_rook"]))
        self.board.append(Piece(row, 1, assets.IMAGES[color + "_knight"]))
        self.board.append(Piece(row, 2, assets.IMAGES[color + "_bishop"]))
        self.board.append(Piece(row, 3, assets.IMAGES[color + "_queen"]))
        self.board.append(Piece(row, 4, assets.IMAGES[color + "_king"]))
        self.board.append(Piece(row, 5, assets.IMAGES[color + "_bishop"]))
        self.board.append(Piece(row, 6, assets.IMAGES[color + "_knight"]))
        self.board.append(Piece(row, 7, assets.IMAGES[color + "_rook"]))         
    
    def update(self):
        for row in range(8):
            for col in range(8):
                pos = col*constants.SQUARE_WIDTH, row*constants.SQUARE_WIDTH
                if (row + col) % 2 == 0:
                    self.window.screen.blit(assets.IMAGES["dark_square"], pos)
                else:
                    self.window.screen.blit(assets.IMAGES["light_square"], pos)
                
        for piece in self.board:
            piece.render(self.window.screen)

        
