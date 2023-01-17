from game.board import Board
from minimax.scoring import get_board_score
from minimax.moves import get_moves


def minimax(board: Board, depth: int, maximize: bool,
 alpha = float("-inf"), beta = float("inf")):
    if depth == 0 or board.is_game_over():
        return get_board_score(board), None, None
    
    
    start_pos = None
    end_pos = None
    
    if maximize:
        max_score = float('-inf')
        for move in get_moves(board, "white"):
            piece_pos = board.get_pos(move.piece)
            new_board = board.copy()
            new_board.move_piece(piece_pos, move.end_pos)
            score = minimax(new_board, depth - 1, False, alpha, beta)[0]
            max_score = max(max_score, score)
            if max_score == score:
                start_pos = piece_pos
                end_pos = move.end_pos
            alpha = max(alpha, score)
            if beta < alpha:
                break

        return max_score, start_pos, end_pos
    
    min_score = float('inf')
    for move in get_moves(board, "black"):
        piece_pos = board.get_pos(move.piece)
        new_board = board.copy()
        new_board.move_piece(piece_pos, move.end_pos)
        score = minimax(new_board, depth - 1, True, alpha, beta)[0]
        min_score = min(min_score, score)
        if min_score == score:
            start_pos = piece_pos
            end_pos = move.end_pos
        beta = min(beta, score)
        if beta < alpha:
            break
    
    return min_score, start_pos, end_pos
        
