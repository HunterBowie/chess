"""
A package that provides a simplified and organized struture for designing UIs in pygame
"""

from .util import Colors, Timer, Text, root_rect, load_image, \
get_surface, get_text_size, rotate_surface
from .constants import ColorStyle, Event, Colors, CheckBoxType
from .assets import IMAGES_DIR, SOUNDS_DIR, FOUNTS_DIR

from .window import Window

from .flash import Flash
from .ui import Button, Slider, TextBox, CheckBox, TogglableButtonGroup


