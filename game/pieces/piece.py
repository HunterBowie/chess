import pygame, constants

class Piece:
    def __init__(self, row, col, color, image):
        self.row = row
        self.col = col
        self.color = color

        self.image = image

        self.rect = pygame.Rect(self.get_pos()[0], self.get_pos()[1],
        constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)

        self.selected = False
    
    def get_pos(self):
        return self.col*constants.SQUARE_WIDTH, self.row*constants.SQUARE_WIDTH

    def render(self, screen):
        screen.blit(self.image, (self.col*constants.SQUARE_WIDTH, self.row*constants.SQUARE_WIDTH))
    
    def check_move(self, row, col, board):
        if row < 0 or col < 0:
            return False

        if row > 7 or col > 7:
            return False

        for piece in board:
            if piece.row == row and piece.col == col:
                if piece.color != self.color:
                    return True
                return False
        return True
    
    def get_single_line_move(self)

    
    
    def get_line_moves(self, board):
        moves = []
        for row_offset in range(7):
            for piece in board:
                if piece.row == self.row+row_offset and piece.col == self.col:


    def get_diagonal_moves(self, board):
        pass