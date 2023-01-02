import assets, constants, pygame, windowgui
from game.board import Board
from game.players import Human

class Game:    
    def __init__(self, window):
        self.window = window
        self.board = Board()
        self.turn = "white"
        self.selected_piece = None
        self.white_player = Human(self, "white")
        self.black_player = Human(self, "black")
    
    def change_turn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

    def eventloop(self, event):
        if self.turn == "white":
            self.white_player.eventloop(event)
        else:
            self.black_player.eventloop(event)
   
    def update(self):
        self.board.render(self.window.screen)

        if self.selected_piece:
            self.board.render_move_dots(self.selected_piece, self.window.screen)

        if self.board.is_king_checkmated(self.turn):
            color = "white"
            if self.turn == "white":
                color = "black"
            print(str(color) + " wins")
            self.window.end()
        
            
        

               

        
