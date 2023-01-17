from game.board import Board
from game.pieces import Piece
from minimax.scoring import scoring 

class Move:
    def __init__(self, piece: Piece, end_pos: tuple, board: Board):
        self.end_pos = end_pos
        self.piece = piece
        self.board = board
    
def predict_value(move):
    end_piece = move.board[move.end_pos[0]][move.end_pos[1]]
    if end_piece:
        if end_piece.color != move.piece.color:
            return scoring[end_piece.name] - scoring[move.piece.name]
    if move.piece.name != "pawn":
        return 1
    return 0

def get_moves(board: Board, color):
    moves = []
    for piece in board.get_pieces():
        if piece.color == color:
            for move in board.get_moves(piece):
                moves.append(Move(piece, move, board))

    moves.sort(key=predict_value, reverse=True)
    return moves