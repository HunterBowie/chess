import assets, constants, pygame, windowgui
from game.board import Board

class Game:    
    def __init__(self, window):
        self.window = window
        self.board = Board()
        self.selected_piece = None
        self.turn = "white"

    def eventloop(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            moves = []
            if self.selected_piece:
                moves = self.board.get_moves(self.selected_piece)
            if self.board.get_mouse_pos() in moves:
                selected_pos = self.board.get_pos(self.selected_piece)
                self.board.move_piece(selected_pos, self.board.get_mouse_pos())
                self.selected_piece = None
                if self.turn == "white":
                    self.turn = "black"
                else:
                    self.turn = "white"
                
            else:
                if self.board.get_mouse_pos() == self.board.get_pos(self.selected_piece):
                    self.selected_piece = None
                
                else:
                    self.selected_piece = None

                    row, col = self.board.get_mouse_pos()
                    piece = self.board[row][col]
                    if piece:
                        if piece.color == self.turn:
                            self.selected_piece = piece
        
   
    
    def update(self):
        self.board.render(self.window.screen, self.turn)

        if self.selected_piece:
            self.board.render_move_dots(self.selected_piece, self.window.screen)
               

        
