import assets, constants, pygame, windowgui, time, random
from game.board import Board
import chessbot

class Game:    
    def __init__(self, white_player: constants.PlayerType, 
    black_player: constants.PlayerType, bot_level = 1):
        self.white_player = white_player
        self.black_player = black_player
        self.board = Board()
        self.chessbot = chessbot.ChessBot(bot_level)
        self.turn = "white"
        self.selected_piece = None
        self.theme = constants.BoardTheme.NORMAL
        self.board_flipped = False
        self.human_timer = windowgui.Timer()
        self.bot_timer = windowgui.Timer()
        self.end_timer = windowgui.Timer()
        self.bot_level = bot_level

        self.prev_move = None

        self.highlighted = []

        if self.white_player == constants.PlayerType.BOT:
            self.bot_timer.start()
        
        if self.black_player == constants.PlayerType.HUMAN and \
            self.white_player == constants.PlayerType.BOT:
            self.board_flipped = True

        self.on_start_of_turn()

    def on_start_of_turn(self):
        for row in self.board:
            for piece in row:
                if piece is not None:
                    if piece.color == self.turn:
                        piece.on_start_of_turn()
    
    def _render_board_square(self, color, pos, screen):
        x, y = pos[1]*constants.SQUARE_WIDTH, pos[0]*constants.SQUARE_WIDTH
        white_square = pygame.Surface((constants.SQUARE_WIDTH, constants.SQUARE_WIDTH))
        white_square.fill(windowgui.Colors.WHITE)
        black_square = pygame.Surface((constants.SQUARE_WIDTH, constants.SQUARE_WIDTH))
        highlighted_square = pygame.Surface((constants.SQUARE_WIDTH, constants.SQUARE_WIDTH))
        highlighted_square.fill(constants.Colors.BOARD_HIGHLIGHT)
        if self.theme == constants.BoardTheme.NORMAL:
            white_square = assets.IMAGES["white_square"]
            black_square = assets.IMAGES["black_square"]
        elif self.theme == constants.BoardTheme.GREEN:
            black_square.fill(constants.Colors.BOARD_GREEN)
        elif self.theme == constants.BoardTheme.RED:
            black_square.fill(constants.Colors.BOARD_RED)
        else:
            raise Exception(f"Value {self.theme} is not a board theme")
        
        if (self._calc_row(pos[0]), self._calc_col(pos[1])) in self.highlighted:
            screen.blit(highlighted_square, (x, y))
            return

        if color == "white":
            screen.blit(white_square, (x, y))
        else:
            screen.blit(black_square, (x, y))
        
    def _calc_row(self, row):
        if self.board_flipped:
            return 7-row
        return row
    
    def _calc_col(self, col):
        if self.board_flipped:
            return 7-col
        return col

    def _move_piece(self, start_pos, end_pos):
        self.board.move_piece(start_pos, end_pos)
        self.prev_move = start_pos, end_pos
        self.selected_piece = None
        if self.white_player == self.black_player == constants.PlayerType.HUMAN:
            self.human_timer.start()
        else:
            self._change_turn()      
  
    def _change_turn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
        
        if self.get_current_player() != constants.PlayerType.BOT:
            pass
        self.highlighted = [self.prev_move[0], self.prev_move[1]]
        
        if self.is_over():
            self.highlighted.clear()
            return
        
        if self.white_player == self.black_player == constants.PlayerType.HUMAN:
            self.board_flipped = not self.board_flipped
        
        if self.get_current_player() == constants.PlayerType.BOT:
            self.bot_timer.start()
        
        self.on_start_of_turn()      

    def get_mouse_board_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        col = mouse_pos[0]//constants.SQUARE_WIDTH
        row = mouse_pos[1]//constants.SQUARE_WIDTH
        row, col = self._calc_row(row), self._calc_col(col)
        return row, col
        
    def on_click(self):
        if self.get_current_player() == constants.PlayerType.HUMAN and self.human_timer.get() == 0:
            moves = []
            if self.selected_piece:
                moves = self.board.get_moves(self.selected_piece)
            if self.get_mouse_board_pos() in moves:
                selected_pos = self.board.get_pos(self.selected_piece)
                self._move_piece(selected_pos, self.get_mouse_board_pos())
                
            else:
                if self.get_mouse_board_pos() == self.board.get_pos(self.selected_piece):
                    self.selected_piece = None
                
                else:
                    self.selected_piece = None

                    row, col = self.get_mouse_board_pos()
                    piece = self.board[row][col]
                    if piece:
                        if piece.color == self.turn:
                            self.selected_piece = piece

    def update(self):
        if self.is_over():
            return

        if self.human_timer.passed(constants.HUMAN_DELAY):
            self.human_timer.reset()
            self._change_turn()
        
        if self.human_timer.get() == 0:
            if self.get_current_player() == constants.PlayerType.BOT and self.bot_timer.passed(constants.BOT_DELAY):
                self.bot_timer.reset()
                timer = windowgui.Timer()
                timer.start()
                start_pos, end_pos = self.chessbot.run(self.board, self.turn)
                time = timer.get()
                score = chessbot.get_board_score(self.board)
                # print(f"Bot time: {time}, Board score {score}")
                self._move_piece(start_pos, end_pos)
            
    def render(self, screen):
        for row in range(8):
            for col in range(8):
                x, y = col*constants.SQUARE_WIDTH, row*constants.SQUARE_WIDTH
                if (row + col) % 2 == 0:
                    self._render_board_square("white", (row, col), screen)
                else:
                    self._render_board_square("black", (row, col), screen)
                
                row, col = self._calc_row(row), self._calc_col(col)
                piece = self.board[row][col]
                if piece:
                    screen.blit(piece.get_image(), (x, y))


        if self.selected_piece:
            moves = self.board.get_moves(self.selected_piece)

            small_circle = pygame.Surface((constants.SQUARE_WIDTH, constants.SQUARE_WIDTH), pygame.SRCALPHA)
            big_circle = pygame.Surface((constants.SQUARE_WIDTH, constants.SQUARE_WIDTH), pygame.SRCALPHA)
            pygame.draw.circle(small_circle, windowgui.Colors.GREY, (constants.SQUARE_WIDTH//2, constants.SQUARE_WIDTH//2), 15)
            pygame.draw.circle(big_circle, windowgui.Colors.GREY, (constants.SQUARE_WIDTH//2, constants.SQUARE_WIDTH//2), 30)
            small_circle.set_alpha(100)
            big_circle.set_alpha(100)
            
            for move in moves:
                x, y = self._calc_col(move[1])*constants.SQUARE_WIDTH, \
                    self._calc_row(move[0])*constants.SQUARE_WIDTH
                if self.board[move[0]][move[1]]:
                    screen.blit(big_circle, (x, y))
                else:
                    screen.blit(small_circle, (x, y))

    def get_current_player(self):
        if self.turn == "white":
            return self.white_player
        return self.black_player
  
    def is_over(self):
        if self.board.is_game_over():
            return True
        return False
        
    
            
        

               

        
