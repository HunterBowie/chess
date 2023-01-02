from game.board import Board

class Player:
    def __init__(self, game, color: str):
        self.game = game
        self.board = game.board
        self.color = color
    
    def eventloop(self, event):
        pass

    def update(self):
        pass
