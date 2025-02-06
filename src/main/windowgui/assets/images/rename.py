from os import listdir
from os.path import isfile, join
import os
files = [f for f in listdir(os.path.dirname(__file__)) if isfile(join(os.path.dirname(__file__), f))]

IMAGES_PATH = join(join(join(os.path.abspath(os.getcwd()), "windowgui"), 'assets'), 'images')
#C:\\Users\\hunte\\Desktop\\windowgui\\assets\\images\\grey_arrowDownGrey.png
for file_name in files:
    if "grey" in file_name:
        new_name = file_name.replace("grey", "white")
        print(f"replacing {file_name} with {new_name}")
        print(file_name)
        os.rename(join(IMAGES_PATH, file_name), join(IMAGES_PATH, new_name)) 

