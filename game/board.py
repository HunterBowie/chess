import assets, constants, pygame, windowgui, copy
from game.pieces import Rook, Bishop, King, Queen, Knight, Pawn, Centaur, Piece, Joker

class Board:
    def __init__(self, bottom_color="white"):
        self._board = [[None for i in range(8)] for i in range(8)]
        self._index = -1
        self._init_pieces()

        self.theme = constants.BoardTheme.NORMAL
        self.bottom_color = bottom_color

    def _init_pieces(self):
        self._init_back_row(0, "black")
        self._init_pawn_row(1, "black", "down")
        self._init_pawn_row(6, "white", "up")
        self._init_back_row(7, "white")
    
    def _init_pawn_row(self, row: int, color: str, direction: str):
        for col in range(8):
            self[row][col] = Pawn(color, direction)

    def _init_back_row(self, row: int, color: str):
        self[row][0] = Rook(color)
        self[row][1] = Knight(color)
        self[row][2] = Bishop(color)
        self[row][3] = Queen(color)
        self[row][4] = King(color)
        self[row][5] = Bishop(color)
        self[row][6] = Knight(color)
        self[row][7] = Rook(color)
    
    def calc_row(self, row):
        if self.bottom_color == "black":
            return 7-row
        return row
    
    def rotate(self):
        if self.bottom_color == "white":
            self.bottom_color = "black"
        else:
            self.bottom_color = "white"

    def on_start_of_turn(self, turn):
        for row in self:
            for piece in row:
                if piece is not None:
                    if piece.color == turn:
                        piece.on_start_of_turn()

    def __repr__(self):
        return str(self._board)

    def __getitem__(self, index: int):
        return self._board[index]
    
    def __iter__(self):
        return iter(self._board)

    def is_king_checkmated(self, color: str):
        for row in self:
            for piece in row:
                if piece is not None:
                    if piece.color == color:
                        if len(self.get_moves(piece)) > 0:
                            return False
        return True
            
    def is_king_in_check(self, color: str):
        for row in self:
            for piece in row:
                if type(piece) is King and piece.color == color:
                    if piece.in_check(self.get_pos(piece), self):
                        return True
        return False
    
    def copy(self):
        board_copy = Board()
        board_copy._board = copy.deepcopy(self._board)
        return board_copy
    
    def get_moves(self, piece: Piece):
        moves = []
        for move in piece.get_moves(self.get_pos(piece), self):
            board = self.copy()
            board.move_piece(self.get_pos(piece), move)
            if not board.is_king_in_check(piece.color):
                moves.append(move)
        return moves          

    def get_mouse_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        col = mouse_pos[0]//constants.SQUARE_WIDTH
        row = mouse_pos[1]//constants.SQUARE_WIDTH
        row = self.calc_row(row)
        return row, col
    
    def get_pos(self, piece: Piece):
        for row in range(8):
            for col in range(8):
                if self[row][col] == piece:
                    return row, col
                
    def move_piece(self, start_pos: int, end_pos: int):
        piece = self[start_pos[0]][start_pos[1]]
        if piece is None:
            raise Exception(f"There is no piece to move at {start_pos}")
        self[start_pos[0]][start_pos[1]] = None
        self[end_pos[0]][end_pos[1]] = piece
        piece.moved = True
    
    def _render_board_square(self, color, pos, screen):
        x, y = pos[1]*constants.SQUARE_WIDTH, pos[0]*constants.SQUARE_WIDTH
        white_square = pygame.Surface((constants.SQUARE_WIDTH, constants.SQUARE_WIDTH))
        white_square.fill(windowgui.Colors.WHITE)
        black_square = pygame.Surface((constants.SQUARE_WIDTH, constants.SQUARE_WIDTH))
        if self.theme == constants.BoardTheme.NORMAL:
            white_square = assets.IMAGES["white_square"]
            black_square = assets.IMAGES["black_square"]
        elif self.theme == constants.BoardTheme.GREEN:
            black_square.fill(constants.Colors.BOARD_GREEN)
        elif self.theme == constants.BoardTheme.RED:
            black_square.fill(constants.Colors.BOARD_RED)
        else:
            raise Exception(f"Value {self.theme} is not a board theme")
            
        if color == "white":
            screen.blit(white_square, (x, y))
        else:
            screen.blit(black_square, (x, y))

    def render_move_dots(self, piece: Piece, screen: pygame.Surface):
        moves = self.get_moves(piece)

        small_circle = pygame.Surface((constants.SQUARE_WIDTH, constants.SQUARE_WIDTH), pygame.SRCALPHA)
        big_circle = pygame.Surface((constants.SQUARE_WIDTH, constants.SQUARE_WIDTH), pygame.SRCALPHA)
        pygame.draw.circle(small_circle, windowgui.Colors.GREY, (constants.SQUARE_WIDTH//2, constants.SQUARE_WIDTH//2), 15)
        pygame.draw.circle(big_circle, windowgui.Colors.GREY, (constants.SQUARE_WIDTH//2, constants.SQUARE_WIDTH//2), 30)
        small_circle.set_alpha(100)
        big_circle.set_alpha(100)
        
        for move in moves:
            x, y = move[1]*constants.SQUARE_WIDTH, \
                self.calc_row(move[0])*constants.SQUARE_WIDTH
            if self[move[0]][move[1]]:
                screen.blit(big_circle, (x, y))
            else:
                screen.blit(small_circle, (x, y))
    
    def render(self, screen: pygame.Surface):
        for row in range(8):
            for col in range(8):
                x, y = col*constants.SQUARE_WIDTH, row*constants.SQUARE_WIDTH
                if self.bottom_color == "white":
                    if (row + col) % 2 == 0:
                        self._render_board_square("white", (row, col), screen)
                    else:
                        self._render_board_square("black", (row, col), screen)
                else:
                    if (row + col) % 2 == 0:
                        self._render_board_square("black", (row, col), screen)
                    else:
                        self._render_board_square("white", (row, col), screen)
                
                row = self.calc_row(row)
                piece = self[row][col]
                if piece:
                    screen.blit(piece.get_image(), (x, y))
            
