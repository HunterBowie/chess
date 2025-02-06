from os import path, pardir
import windowgui, constants

CURRENT_DIR = path.dirname(__file__)
PROJECT_DIR = path.abspath(path.join(CURRENT_DIR, pardir, pardir))
IMAGES_DIR = path.join(PROJECT_DIR, "assets/images")

IMAGES = {
    "white_square": windowgui.load_image("white_square", IMAGES_DIR, 
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "black_square": windowgui.load_image("black_square", IMAGES_DIR,
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "white_rook": windowgui.load_image("white_rook", IMAGES_DIR,
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "black_rook": windowgui.load_image("black_rook", IMAGES_DIR,
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "white_knight": windowgui.load_image("white_knight", IMAGES_DIR,
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "black_knight": windowgui.load_image("black_knight", IMAGES_DIR,
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "white_king": windowgui.load_image("white_king", IMAGES_DIR,
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "black_king": windowgui.load_image("black_king", IMAGES_DIR,
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "white_queen": windowgui.load_image("white_queen", IMAGES_DIR,
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "black_queen": windowgui.load_image("black_queen", IMAGES_DIR,
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "white_bishop": windowgui.load_image("white_bishop", IMAGES_DIR,
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "black_bishop": windowgui.load_image("black_bishop", IMAGES_DIR,
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "white_pawn": windowgui.load_image("white_pawn", IMAGES_DIR,
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "black_pawn": windowgui.load_image("black_pawn", IMAGES_DIR,
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "white_cursed_pawn": windowgui.load_image("white_pawn", IMAGES_DIR,
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "black_cursed_pawn": windowgui.load_image("black_pawn", IMAGES_DIR,
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "black_centaur": windowgui.load_image("black_centaur", IMAGES_DIR,
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "white_centaur": windowgui.load_image("white_centaur", IMAGES_DIR,
                                         scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "white_jester":  windowgui.load_image("white_jester", IMAGES_DIR, scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
    "black_jester":  windowgui.load_image("black_jester", IMAGES_DIR, scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
}

def convert_images():
    for name,item in IMAGES.items():
        if type(item) is list:
            IMAGES[name] = [image.convert_alpha() for image in item]
        else:
            IMAGES[name] = item.convert_alpha()


