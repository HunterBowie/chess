from game.pieces import Piece, Knight, King, Bishop, Pawn, Queen, Rook
from game.board import Board
import copy

def get_board_score(board: Board):
    if board.is_stalemated("white") or board.is_stalemated("black"):
        return 0
    
    if board.is_checkmated("white"):
        return float("-inf")
    elif board.is_checkmated("black"):
        return float("inf")

    score = 0
    for piece in board.get_pieces():
        score += get_piece_score(piece, board)
    return score


def get_piece_score(piece: Piece, board: Board):
    try:
        score = scoring[piece.name]
    
        position = positional_scores[piece.name].copy()
        if piece.color == "black":
            position.reverse()

        row, col = board.get_pos(piece)
        score += position[row][col]

    except KeyError:
        return 0

    if piece.color == "black":
        return -score
    return score

scoring = {
    "pawn": 100,
    "bishop": 330,
    "knight": 320,
    "rook": 500,
    "queen": 900,
    "king": 0,


    "jester": 0,
    "centaur": 0,
    "cursed_pawn": 0
}

positional_scores = {
"pawn":[
[0,  0,  0,  0,  0,  0,  0,  0],
[50, 50, 50, 50, 50, 50, 50,50],
[10, 10, 20, 30, 30, 20, 10,10],
[5,  5, 10, 25, 25, 10,  5,  5],
[0,  0,  0, 20, 20,  0,  0,  0],
[5, -5,-10,  0,  0,-10, -5,  5],
[5, 10, 10,-20,-20, 10, 10,  5],
[0,  0,  0,  0,  0,  0,  0,  0]
],
"knight": [
[-50,-40,-30,-30,-30,-30,-40,-50],
[-40,-20,  0,  0,  0,  0,-20,-40],
[-30,  0, 10, 15, 15, 10,  0,-30],
[-30,  5, 15, 20, 20, 15,  5,-30],
[-30,  0, 15, 20, 20, 15,  0,-30],
[-30,  5, 10, 15, 15, 10,  5,-30],
[-40,-20,  0,  5,  5,  0,-20,-40],
[-50,-40,-30,-30,-30,-30,-40,-50],
],
"bishop": [
[-20,-10,-10,-10,-10,-10,-10,-20],
[-10,  0,  0,  0,  0,  0,  0,-10],
[-10,  0,  5, 10, 10,  5,  0,-10],
[-10,  5,  5, 10, 10,  5,  5,-10],
[-10,  0, 10, 10, 10, 10,  0,-10],
[-10, 10, 10, 10, 10, 10, 10,-10],
[-10,  5,  0,  0,  0,  0,  5,-10],
[-20,-10,-10,-10,-10,-10,-10,-20],
],
"rook": [
 [ 0,  0,  0,  0,  0,  0,  0,  0],
 [ 5, 10, 10, 10, 10, 10, 10,  5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
 [ 0,  0,  0,  5,  5,  0,  0,  0]
 ],
 "queen": [
[-20,-10,-10, -5, -5,-10,-10,-20],
[-10,  0,  0,  0,  0,  0,  0,-10],
[-10,  0,  5,  5,  5,  5,  0,-10],
[ -5,  0,  5,  5,  5,  5,  0, -5],
[  0,  0,  5,  5,  5,  5,  0, -5],
[-10,  5,  5,  5,  5,  5,  0,-10],
[-10,  0,  5,  0,  0,  0,  0,-10],
[-20,-10,-10, -5, -5,-10,-10,-20]
 ],
 "king": [
[-30,-40,-40,-50,-50,-40,-40,-30],
[-30,-40,-40,-50,-50,-40,-40,-30],
[-30,-40,-40,-50,-50,-40,-40,-30],
[-30,-40,-40,-50,-50,-40,-40,-30],
[-20,-30,-30,-40,-40,-30,-30,-20],
[-10,-20,-20,-20,-20,-20,-20,-10],
[ 20, 20,  0,  0,  0,  0, 20, 20],
[ 20, 30, 10,  0,  0, 10, 30, 20]
 ],

}







