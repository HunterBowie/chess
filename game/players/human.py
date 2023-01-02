import pygame
from game.players.player import Player


class Human(Player):
    def eventloop(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            moves = []
            if self.game.selected_piece:
                moves = self.board.get_moves(self.game.selected_piece)
            if self.board.get_mouse_pos() in moves:
                selected_pos = self.board.get_pos(self.game.selected_piece)
                self.board.move_piece(selected_pos, self.board.get_mouse_pos())
                self.game.selected_piece = None
                self.board.rotate()
                self.game.change_turn()
                self.board.on_start_of_turn(self.game.turn)
                
            else:
                if self.board.get_mouse_pos() == self.board.get_pos(self.game.selected_piece):
                    self.game.selected_piece = None
                
                else:
                    self.game.selected_piece = None

                    row, col = self.board.get_mouse_pos()
                    piece = self.board[row][col]
                    if piece:
                        if piece.color == self.color:
                            self.game.selected_piece = piece
        