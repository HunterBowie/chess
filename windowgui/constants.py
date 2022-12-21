import pygame


TEXTBOX_SHIFT_CHARS = {"1":"!","2":"@","3":"#",
    "4":"$","5":"%","6":"^","7":"&","8":"*",
    "9":"(","0":")","-":"_","=":"+","`":"~",
    "/": "?", ";": ":", "\\": "\|"}
TEXTBOX_MARGIN = 5
TEXTBOX_CURSOR_BLINK_TIME = .45
TEXTBOX_BACKSPACE_START_DELAY = .4
TEXTBOX_BACKSPACE_DELAY = .05
TEXTBOX_BORDER_WIDTH = 4

SLIDER_HELD_DIST_Y = 20
SLIDER_HELD_DIST_X = 100

FLASH_FADE_TIME = .5
FLASH_FADE_SPEED = 10

M_FLASH_KEY = "flash"
M_UI_KEY = "ui"
M_SOUND_KEY = "sound"

class AssetType:
    IMAGES = 1
    SOUND = 2
    FONT = 3



class UIColorStyle:
    WHITE = "white"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"


class UIEvent:
    NAMES = [
    "BUTTON_CLICKED", "BUTTON_RELEASED", "CHECKBOX_CLICKED",
    "TEXTBOX_POSTED", "TEXTBOX_SELECTED", "SLIDER_MOVED"
    ]

    BUTTON_CLICKED = pygame.USEREVENT + NAMES.index("BUTTON_CLICKED")
    BUTTON_RELEASED = pygame.USEREVENT + NAMES.index("BUTTON_RELEASED")
    CHECKBOX_CLICKED = pygame.USEREVENT + NAMES.index("CHECKBOX_CLICKED")
    TEXTBOX_POSTED = pygame.USEREVENT + NAMES.index("TEXTBOX_POSTED")
    TEXTBOX_SELECTED = pygame.USEREVENT + NAMES.index("TEXTBOX_SELECTED")
    SLIDER_MOVED = pygame.USEREVENT + NAMES.index("SLIDER_MOVED")
    
    ALL = [
    BUTTON_CLICKED, BUTTON_RELEASED, CHECKBOX_CLICKED,
    TEXTBOX_POSTED, TEXTBOX_SELECTED, SLIDER_MOVED
    ]
    

    @classmethod
    def get_name(cls, event_type):
        return cls.NAMES[cls.ALL.index(event_type)]

class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 100, 0)
    PURPLE = (150, 50, 250)
    GOLD = (200, 200, 30)
    GREY = (128, 128, 128)
    
    LIGHT_BLUE = (204, 229, 255)



    

    
