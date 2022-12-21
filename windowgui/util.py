import pygame, time
from os import path
from .constants import Colors


class Text:
    """
    A class for handling text rendering and style.
    """
    default_style = {
        "font_file": pygame.font.get_default_font(),
        "size": 30,
        "antialias": True,
        "color": Colors.BLACK
    }

    def __init__(self, x, y, string, style=None, newline_width=None):
        self.style = style
        if self.style is None:
            self.style = self.default_style.copy()
        for setting, value in self.default_style.items():
            if setting not in self.style:
                self.style[setting] = value
        self.x = x
        self.y = y
        self.newline_width = newline_width
        self.set(string)

    def set(self, string):
        self.raw_string = string
        self.lines = string.split("\n")
        self.string = string.replace("\n", "")
        if self.newline_width:
            new_lines = []
            for line in self.lines:
                new_line = "" 
                for char in line:
                    new_line = new_line + char
                    if get_text_size(new_line, self.style)[0] >= self.newline_width:
                        new_lines.append(new_line.strip())
                        new_line = ""
                if new_line:
                    new_lines.append(new_line.strip())
            self.lines = new_lines
        self._load_surf()
    
    def add(self, string):
        self.set(self.raw_string + string)
    
    def pop(self):
        char = self.string[len(self.string)-1]
        self.set(self.string[:len(self.string)-1])
        return char
    
    def get_width(self):
        return self.surface.get_width()
    
    def get_height(self):
        return self.surface.get_height()
    
    def get_size(self):
        return self.get_width(), self.get_height()

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.get_width(), self.get_height())
    
    def _load_surf(self):
        font = pygame.font.Font(self.style["font_file"], self.style["size"])

        if len(self.lines) > 1:
            renders = []    
            for string in self.lines:
                renders.append(font.render(string, self.style["antialias"], self.style["color"]))
            
            height = 0
            width = 0
            for line_surf in renders:
                height += line_surf.get_height()
                if line_surf.get_width() > width:
                    width = line_surf.get_width()
            
            self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
            x = y = 0
            for line_surf in renders:
                self.surface.blit(line_surf, (x, y))
                y += line_surf.get_height()
            
        else:
            self.surface = font.render(self.string, self.style["antialias"], self.style["color"])
    
    def render(self, screen):
        screen.blit(self.surface, (self.x, self.y))
    
    def center_y(self, rect):
        self.y = rect.center[1]-self.get_height()/2

    def center_x(self, rect):
        self.x = rect.center[0]-self.get_width()/2
    
    def center(self, rect):
        self.center_x(rect)
        self.center_y(rect)

def render_text_background(surface, text, color, alpha, margin):
    surf = get_surf((text.get_width()+margin, text.get_height()+margin), color, alpha)
    surface.blit(surf, (int(text.x-margin/2), int(text.y-margin/2)))

def get_text_size(string, style=Text.default_style):
    if style != Text.default_style:
        for setting, value in Text.default_style.items():
            if setting not in style:
                style[setting] = value
    font = pygame.font.Font(style["font_file"], style["size"])
    surf = font.render(string, style["antialias"], style["color"])
    return surf.get_width(), surf.get_height()


class Timer:
    """
    A class for calculating time in seconds.
    """
    def __init__(self):
        self.reset()
    
    def start(self):
        """
        Sets the timer relative to now.
        """
        self.start_time = time.monotonic()
        self.stop_time = -1
    
    def reset(self):
        """
        Sets the timer to always read zero.
        """
        self.start_time = -1
        self.stop_time = -1

    def stop(self):
        """
        Sets the timer stop value to now.
        """
        self.stop_time = time.monotonic()
    
    def get(self):
        """
        Returns the difference between now 
        and start value. If stop() is called,
        then it returns the difference between
        start and stop times.
        """
        if self.start_time == -1:
            return 0
        if self.stop_time == -1:
            return time.monotonic()-self.start_time

        return self.stop_time-self.start_time
    
    def passed(self, seconds):
        """
        Returns true if the timer has exceeded
        the given time.
        """
        return self.get() >= seconds
    
    def stopped(self):

        return self.stop_time != -1
    
    def started(self):
        return self.start_time != -1
    
    def __repr__(self):
        return f"time: {self.get()}"


def rotate_image(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        y = rect.center[1]-rot_image.get_height()/2
        x = rect.center[0]-rot_image.get_width()/2
        return rot_image, (x, y)

def get_surf(size, color, alpha):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill(color)
    surf.set_alpha(alpha)
    return surf


def render_border(surface, rect, size):
    pygame.draw.line(surface, Colors.BLACK, rect.topleft, rect.topright, size)
    pygame.draw.line(surface, Colors.BLACK, rect.topleft, rect.bottomleft, size)
    pygame.draw.line(surface, Colors.BLACK, rect.bottomleft, rect.bottomright, size)
    pygame.draw.line(surface, Colors.BLACK, rect.topright, rect.bottomright, size)


def root_rect(screen_size, rect, top=False, bottom=False,
    left=False, right=False, center_x=False, center_y=False) -> (int, int):
    """
    A function for positioning a rect relative to the screen.
    """
    center_pos = int(screen_size[0]/2), int(screen_size[1]/2)
    
    new_x, new_y = 0, 0
    if center_x:
        new_x = center_pos[0]-int(rect.width/2)
    if center_y:
        new_y = center_pos[1]-int(rect.height/2)
    if left:
        new_x = 0
    if right:
        new_x = screen_size[0]-rect.width
    if bottom:
        new_y = screen_size[1]-rect.height
    if top:
        new_y = 0
    rect.x += new_x
    rect.y += new_y
    return rect.x, rect.y

def root_rects(screen_size, rects, top=False, bottom=False,
    left=False, right=False, center_x=False, center_y=False):
    for rect in rects:
        root_rect(screen_size, rect, top, bottom,
        left, right, center_x, center_y)

def load_image(img_name, img_dir, ext=".png", colorkey=None, convert=False, scale=None):
    full_path = path.join(img_dir, img_name) + ext
    try:
        img = pygame.image.load(full_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"no image for path {full_path}")
    if scale is not None:
        img = pygame.transform.scale(img, scale)
    if convert:
        img = img.convert_alpha()
    if colorkey:
        img.set_colorkey(Colors.BLACK)
    return img

