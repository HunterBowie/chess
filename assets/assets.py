from os import path
import windowgui, constants

CURRENT_DIR = path.dirname(__file__)
IMAGES_DIR = path.join(CURRENT_DIR, "images")



IMAGES = {
    "white_square": windowgui.load_image("white_square", IMAGES_DIR),
    "black_square": windowgui.load_image("black_square", IMAGES_DIR),
    "white_rook": windowgui.load_image("white_rook", IMAGES_DIR),
    "black_rook": windowgui.load_image("black_rook", IMAGES_DIR),
    "white_knight": windowgui.load_image("white_knight", IMAGES_DIR),
    "black_knight": windowgui.load_image("black_knight", IMAGES_DIR),
    "white_king": windowgui.load_image("white_king", IMAGES_DIR),
    "black_king": windowgui.load_image("black_king", IMAGES_DIR),
    "white_queen": windowgui.load_image("white_queen", IMAGES_DIR),
    "black_queen": windowgui.load_image("black_queen", IMAGES_DIR),
    "white_bishop": windowgui.load_image("white_bishop", IMAGES_DIR),
    "black_bishop": windowgui.load_image("black_bishop", IMAGES_DIR),
    "white_pawn": windowgui.load_image("white_pawn", IMAGES_DIR),
    "black_pawn": windowgui.load_image("black_pawn", IMAGES_DIR),
    "black_centaur": windowgui.load_image("black_centaur", IMAGES_DIR),
    "white_centaur": windowgui.load_image("white_centaur", IMAGES_DIR),
    "white_joker":  windowgui.load_image("white_joker", IMAGES_DIR, scale=(constants.SQUARE_WIDTH, constants.SQUARE_WIDTH)),
}

def convert_images():
    for name,item in IMAGES.items():
        if type(item) is list:
            IMAGES[name] = [image.convert_alpha() for image in item]
        else:
            IMAGES[name] = item.convert_alpha()


