import pygame, windowgui, constants, game, assets, random

pygame.init()


class StartManager:
    def __init__(self, window):
        self.window = window
        self.text = windowgui.Text(0, -200, "Chess", 
        constants.TITLE_FONT_STYLE, root_center=True)
    
    def init_ui(self):
        human_button = windowgui.Button("human", 0, -100,
        250, 50, text=windowgui.Text(0,0,"Pass and Play")
        )
        bot_button = windowgui.Button("bot", 0, 0,
        250, 50, text=windowgui.Text(0,0,"Computer")
        )
        self.window.ui.add([human_button, bot_button])
    
    def eventloop(self, event):
        if event.type == windowgui.Event.BUTTON_CLICKED:
            if event.ui_id == "human":
                new_game = game.Game(constants.PlayerType.HUMAN, constants.PlayerType.HUMAN)
                self.window.set_manager(GameManager(self.window, new_game))
            elif event.ui_id == "bot":
                self.window.set_manager(BotMenuManager(self.window))
    
    def update(self):
        self.text.render(self.window.screen)

class BotMenuManager:
    def __init__(self, window):
        self.window = window
        self.color_buttons = None
        self.textbox = None
    
    def init_ui(self):
        white_button = windowgui.Button("white", 0, -100, 250, 50,
         text=windowgui.Text(0,0,"White"))
        black_button = windowgui.Button("black", 0, 0, 250, 50,
         text=windowgui.Text(0,0,"Black"))
        start_button = windowgui.Button("start", 0, 200, 250, 50,
         text=windowgui.Text(0,0,"Start"), color_style=windowgui.ColorStyle.YELLOW)
        self.color_buttons = windowgui.TogglableButtonGroup(
            [white_button, black_button]
        )
        self.textbox = windowgui.TextBox("botlevel", 0, 100, 250, 50)
        self.textbox.text.set("2")
        self.window.ui.add([self.color_buttons, start_button, self.textbox])
    
    def eventloop(self, event):
        if event.type == windowgui.Event.BUTTON_CLICKED:
            if event.ui_id == "start":
                player_color = random.choice(["white", "black"])
                if self.color_buttons.selected:
                    if self.color_buttons.selected.id == "white":
                        player_color = "white"
                    else:
                        player_color = "black"
                white_player = constants.PlayerType.HUMAN
                black_player = constants.PlayerType.BOT
                if player_color == "black":
                    white_player = constants.PlayerType.BOT
                    black_player = constants.PlayerType.HUMAN
                
                value = int(self.textbox.text.string)
                
                self.window.set_manager(GameManager(self.window, game.Game(white_player, black_player, bot_level=value)))

class GameManager:
    def __init__(self, window, game):
        self.window = window
        self.game = game
    
    def eventloop(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.game.on_click()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.window.set_manager(PausedManager(self.window, self.game))
    
    def update(self):
        self.game.update()

        if self.game.is_over():
            self.window.set_manager(EndManager(self.window, self.game))
            return

        self.game.render(self.window.screen)

class PausedManager:
    def __init__(self, window, game):
        self.window = window
        self.game = game
    
    def init_ui(self):
        resume_button = windowgui.Button("resume", 0, -100, 250, 50, 
        text=windowgui.Text(0,0,"Resume"))
        mainmenu_button = windowgui.Button("mainmenu", 0, 0, 250, 50, 
        text=windowgui.Text(0,0,"Main Menu"))
        self.window.ui.add([resume_button, mainmenu_button])
    
    def eventloop(self, event):
        if event.type == windowgui.Event.BUTTON_CLICKED:
            if event.ui_id == "resume":
                self.window.set_manager(GameManager(self.window, self.game))
            elif event.ui_id == "mainmenu":
                self.window.set_manager(StartManager(self.window))

class EndManager:
    def __init__(self, window, game):
        self.window = window
        self.game = game
        game_status = "Tied"
        if game.board.is_checkmated(game.turn):
            winner = "white"
            if game.turn == "white":
                winner = "black"
            game_status = winner[0].upper() + winner[1:] + " Wins"
        self.text = windowgui.Text(0, -200, game_status,
         constants.TITLE_FONT_STYLE, root_center=True)
    
    def init_ui(self):
        button = windowgui.Button("restart", 0, 200, 200, 50,
         top_img=windowgui.Text(0,0,"Restart").surface)
        self.window.ui.add(button)
    
    def eventloop(self, event):
        if event.type == windowgui.Event.BUTTON_CLICKED:
            if event.ui_id == "restart":
                self.window.set_manager(StartManager(self.window))
    
    def update(self):
        game_surf = pygame.Surface(constants.SCREEN_SIZE, pygame.SRCALPHA)
        self.game.render(game_surf)
        game_surf = pygame.transform.scale(game_surf, [constants.SCREEN_SIZE[0]//3]*2)
        x, y = windowgui.root_rect(pygame.Rect(0,0,constants.SCREEN_SIZE[0]//3, constants.SCREEN_SIZE[0]//3),
        center_y=True, center_x=True)
        self.window.screen.blit(game_surf, (x, y))
        self.text.render(self.window.screen)




window = windowgui.Window(constants.SCREEN_SIZE)
window.set_manager(StartManager(window))
pygame.display.set_caption("Chess")

assets.convert_images()

window.start(auto_cycle=True)

