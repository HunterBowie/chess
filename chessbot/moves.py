from game.board import Board
from game.pieces import Piece
from chessbot.scoring import scoring 


def predict_value(action):
    end_piece = action["board"][action["move"][0]][action["move"][1]]
    if end_piece:
        if end_piece.color != action["piece"].color:
            return 1
        
    return 0

def get_piece_actions(board: Board, color):
    actions = []
    for piece in board.get_pieces():
        if piece.color == color:
            for move in board.get_moves(piece):
                actions.append({"piece": piece, "move": move, "board": board})

    actions.sort(key=predict_value, reverse=True)
    return actions

def get_capture_actions(board: Board, color):
    capture_actions = []
    for piece in board.get_pieces():
        if piece.color == color:
            for move in board.get_moves(piece):
                end_piece = board[move[0]][move[1]]
                if end_piece:
                    if end_piece.color != color:
                        capture_actions.append({"piece": piece, "move": move})
    return capture_actions
