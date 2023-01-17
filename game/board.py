import copy, math
from game.pieces import Rook, Bishop, King, Queen, Knight, Pawn, Centaur, Piece, Jester, CursedPawn

class Board:
    def __init__(self):
        # self._board = [[None for i in range(8)] for i in range(8)]
        self._board = [
            [None, King("black"), None, None, Rook("black"), Rook("black"), None, None],
            [None, Pawn("black"), Pawn("black"), None, None, None, Pawn("black"), Pawn("black")],
            [Pawn("black"), None, None, Pawn("black"), None, None, None, None],
            [Pawn("white"), None, None, Knight("white"), Knight("black"), Knight("black"), None, Queen("black")],
            [None, None, Pawn("white"), None, None, None, None, None],
            [None, None, None, None, None, None, None, Pawn("white")],
            [None, Pawn("white"), Queen("white"), Knight("white"), None, Pawn("white"), Pawn("white"), None],
            [None, None, None, Rook("white"), Rook("white"), None, King("white"), None],
        ]
        # self._init_pieces()

    def _init_pieces(self):
        self._init_back_row(0, "black")
        self._init_pawn_row(1, "black")
        self._init_pawn_row(6, "white")
        self._init_back_row(7, "white")
    
    def _init_pawn_row(self, row: int, color: str):
        for col in range(8):
            self[row][col] = Pawn(color)

    def _init_back_row(self, row: int, color: str):
        self[row][0] = Rook(color)
        self[row][1] = Knight(color)
        self[row][2] = Bishop(color)
        self[row][3] = Queen(color)
        self[row][4] = King(color)
        self[row][5] = Bishop(color)
        self[row][6] = Knight(color)
        self[row][7] = Rook(color)

    def __repr__(self):
        return str(self._board)

    def __getitem__(self, index: int):
        return self._board[index]
    
    def __iter__(self):
        return iter(self._board)

    def castle(self, king: King, rook: Rook):
        king_start_pos = self.get_pos(king)
        king_end_pos = king_start_pos[0],king_start_pos[1]+2
        rook_end_pos = king_end_pos[0],king_end_pos[1]-1
        if self.get_pos(rook)[1] == 0:
            king_end_pos = king_start_pos[0],king_start_pos[1]-2
            rook_end_pos = king_end_pos[0],king_end_pos[1]+1
        self.translate_piece(king_start_pos, king_end_pos)
        rook_start_pos = self.get_pos(rook)
        self.translate_piece(rook_start_pos, rook_end_pos)
    
    def get_castling_moves(self, king: King) -> list:
        moves = []
        
        if king.moved or self.in_check(king.color):
            return moves
        
        enemy_color = "black"
        if king.color == "black":
            enemy_color = "white"

        row, _ = self.get_pos(king)
        queenside_rook = self[row][0]
        kingside_rook = self[row][7]
        for rook in [queenside_rook, kingside_rook]:
            if rook is None:
                continue 

            if rook.moved:
                continue
            
            if rook == queenside_rook:
                if self[row][1] or self[row][2] or self[row][3]:
                    continue
                if self.is_under_attack((row, 2), enemy_color) or self.is_under_attack((row, 3), enemy_color):
                    continue
            else:
                if self[row][6] or self[row][5]:
                    continue
                if self.is_under_attack((row, 5), enemy_color) or self.is_under_attack((row, 6), enemy_color):
                    continue
            
            

            moves.append(self.get_pos(rook))

        return moves
    
    def get_enpassant_moves(self, pawn: Pawn):
        return []
        row, col = self.get_pos(pawn)
        side_pawns = []
        if col - 1 >= 0:
            piece = self[row][col-1]
            if type(piece) is Pawn:
                side_pawns.append(piece)
        if col + 1 <= 7:
            piece = self[row][col+1]
            if type(piece) is Pawn:
                side_pawns.append(piece)
        
        if not side_pawns:
            return []
        
        for side_pawn in side_pawns:
            pass
            
        return 
    
    def enpassant(self, pawn1: Pawn, pawn2: Pawn):
        pass

    def is_under_attack(self, pos, color: str):
        for piece in self.get_pieces():
            if piece.color == color:
                if pos in piece.get_moves(self.get_pos(piece), self):
                    return True
        return False
        
    def get_king(self, color: str):
        for piece in self.get_pieces():
            if type(piece) is King and piece.color == color:
                return piece

    def has_legal_moves(self, color: str):
        for piece in self.get_pieces():
            if piece.color == color:
                if len(self.get_moves(piece)) > 0:
                    return True
        return False

    def is_checkmated(self, color: str):
        if self.in_check(color) and not self.has_legal_moves(color):
            return True
        return False
    
    def is_stalemated(self, color: str):
        if not self.in_check(color) and not self.has_legal_moves(color):
            return True
        return False
        
    def in_check(self, color: str):
        king = self.get_king(color)
        if king.in_check(self.get_pos(king), self):
            return True
        return False
    
    def get_moves(self, piece: Piece):
        moves = []
        for move in piece.get_moves(self.get_pos(piece), self):
            board = self.copy()
            board.move_piece(self.get_pos(piece), move)
            if not board.in_check(piece.color):
                moves.append(move)
        
        if type(piece) is Pawn:
            moves = moves + self.get_enpassant_moves(piece)
        elif type(piece) is King:
            moves = moves + self.get_castling_moves(piece)
        
        return moves          
    
    def get_pos(self, piece: Piece):
        for row in range(8):
            for col in range(8):
                if self[row][col] == piece:
                    return row, col
                
    def move_piece(self, start_pos: int, end_pos: int):
        start_piece = self[start_pos[0]][start_pos[1]]
        end_piece = self[end_pos[0]][end_pos[1]]
        if type(start_piece) is King and type(end_piece) is Rook:
            if start_piece.color == end_piece.color:
                self.castle(start_piece, end_piece)
                return
            
        # if type(start_piece) is Pawn:
        #     if not start_piece.moved and int(math.dist(start_pos, end_pos)) == 2:
        #         start_piece.enpussantable = True
        #     else:
        #         start_piece.enpussantable = False

        if (type(start_piece) is Pawn or type(start_piece) is CursedPawn) and end_pos[0] in (0, 7):
            if start_piece.color == "white" and end_pos[0] == 0 or \
                start_piece.color == "black" and end_pos[0] == 7:
                self.translate_piece(start_pos, end_pos)
                if type(start_piece) is Pawn:
                    self[end_pos[0]][end_pos[1]] = Queen(start_piece.color)
                else:
                    self[end_pos[0]][end_pos[1]] = Jester(start_piece.color)
                return 
        
                    
        self.translate_piece(start_pos, end_pos)
    
    def translate_piece(self, start_pos: int, end_pos: int):
        piece = self[start_pos[0]][start_pos[1]]
        if piece is None:
            raise Exception(f"There is no piece to move at {start_pos}")
        self[start_pos[0]][start_pos[1]] = None
        self[end_pos[0]][end_pos[1]] = piece
        piece.moved = True
        
    def get_pieces(self):
        pieces = []
        for row in self:
            for piece in row:
                if piece is not None:
                    pieces.append(piece)
        return pieces

    def is_game_over(self):
        if not self.has_legal_moves("white") or not self.has_legal_moves("black"):
            return True
        return False

    def copy(self):
        board_copy = Board()
        board_copy._board = copy.deepcopy(self._board)
        return board_copy