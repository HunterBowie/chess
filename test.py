pieces = ["rook", "knight", "king", "queen", "bishop", "pawn"]

string = '"dark_square": windowgui.load_image("dark_square", IMAGES_DIR),'

for piece in pieces:
    for color in ["white", "black"]:
        print(f'"{color}_{piece}": windowgui.load_image("{color}_{piece}", IMAGES_DIR),')