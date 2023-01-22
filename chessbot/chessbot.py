import json
from game.board import Board
from chessbot.scoring import get_board_score
from chessbot.moves import get_piece_actions, get_capture_actions


class ChessBot:
    def __init__(self, depth: int):
        self.depth = depth
    
    def run(self, board: Board, color: str):
        _, start_pos, end_pos = self._search(board, self.depth, color)
        return start_pos, end_pos

    def _search(self, board: Board, depth: int, color: str,
    alpha = float("-inf"), beta = float("inf")):

        start_pos = None
        end_pos = None
        
        if board.is_game_over() or depth == 0:
            return get_board_score(board), None, None
        
     
        if color == "white":
            max_score = float('-inf')
            for action in get_piece_actions(board, color):
                piece_pos = board.get_pos(action["piece"])
                new_board = board.copy()
                new_board.move_piece(piece_pos, action["move"])
                score = self._search(new_board, depth - 1, "black", alpha, beta)[0]
                max_score = max(max_score, score)
                if max_score == score:
                    start_pos = piece_pos
                    end_pos = action["move"]
                alpha = max(alpha, score)
                if beta < alpha:
                    break

            return max_score, start_pos, end_pos
        
        min_score = float('inf')
        for action in get_piece_actions(board, color):
            piece_pos = board.get_pos(action["piece"])
            new_board = board.copy()
            new_board.move_piece(piece_pos, action["move"])
            score = self._search(new_board, depth - 1, "white", alpha, beta)[0]
            min_score = min(min_score, score)
            if min_score == score:
                start_pos = piece_pos
                end_pos = action["move"]
            beta = min(beta, score)
            if beta < alpha:
                break
        
        return min_score, start_pos, end_pos
    