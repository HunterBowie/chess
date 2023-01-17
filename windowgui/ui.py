"""
A collection of UI elements to use with the UI manager.
"""

import pygame, pyperclip, math
from numpy import interp
from .assets import get_button_img, get_checkbox_img, get_slider_image
from .util import render_border, Text, get_text_size, Timer, root_rect
from .constants import Colors, TEXTBOX_BACKSPACE_DELAY, TEXTBOX_BORDER_WIDTH, TEXTBOX_CURSOR_BLINK_TIME,\
TEXTBOX_MARGIN, TEXTBOX_SHIFT_CHARS, Event, ColorStyle, SLIDER_HELD_DIST_X, SLIDER_HELD_DIST_Y, \
TEXTBOX_BACKSPACE_START_DELAY, CheckBoxType

class UIElement:
    def __init__(self, id: str, x: int, y: int, 
    width: int, height: int, root_center = True):
        self.rect = pygame.Rect(x, y, width, height)
        self.id = id
        if root_center:
            root_rect(self.rect, center_x=True, center_y=True)

    def post_event(self, event_type: int):
        event_data = {
            "ui_element": self,
            "ui_id": self.id,
        }
        pygame.event.post(pygame.event.Event(event_type, event_data))
                

class Button(UIElement):
    """
    A UI element for togglable or non-togglable buttons.
    """
    def __init__(self, id: str, x: int, y: int, width: int,
    height: int, color_style=ColorStyle.WHITE, text: Text = None,
    top_img: pygame.Surface = None, hide_button = False, root_center = True):
        super().__init__(id, x, y, width, height, root_center)
        self.clicked = False
        self.top_img = top_img
        self.hide_button = hide_button
        if text and top_img:
            raise Exception("No text and top_img")
        
        self.top_img_x = self.top_img_y = 0

        if text:
            self.top_img = text.surface
            self.top_img_x, self.top_img_y = text.x, text.y
            
        if self.top_img:
            self.top_img_x = int(self.rect.width/2-self.top_img.get_width()/2) + self.top_img_x
            self.top_img_y = int(self.rect.height/2-self.top_img.get_height()/2) + self.top_img_y
            
        self._img_up = get_button_img(False, (width, height), color_style)
        self._img_down = get_button_img(True, (width, height-4), color_style)

        self._force_down = False
    
    def eventloop(self, event: pygame.event.Event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pos):
                self.clicked = True
                self.post_event(Event.BUTTON_CLICKED) 

    
    def update(self):
        if not pygame.mouse.get_pressed() == (1, 0, 0) and self.clicked:
            self.clicked = False
            self.post_event(Event.BUTTON_RELEASED)


    def render(self, surface: pygame.Surface):
        if not self.hide_button:
            if self.clicked or self._force_down:
                surface.blit(self._img_down, self.rect.topleft)
            else:   
                surface.blit(self._img_up, (self.rect.left, self.rect.top-4))
        
        if self.top_img:
            if self.clicked or self._force_down:
                surface.blit(self.top_img, 
                (self.top_img_x+self.rect.x, self.top_img_y+self.rect.y))
            else:
                surface.blit(self.top_img,
                 (self.top_img_x+self.rect.x, self.top_img_y+self.rect.y-4))
        

class Slider(UIElement):
    """
    A UI element that allows that user to slide an arrow 
    to ajust a value from 0-100.
    """
    def __init__(self, id: str, x: int, y: int, width: int, 
    height: int, color_style: ColorStyle = ColorStyle.WHITE, root_center = True):
        super().__init__(id, x, y, width, height, root_center)
        self.value = 0
        self._slider_img = get_slider_image("up", color_style)
        self._mouse_held = False
    
    def calc_slider_pos(self):
        return self.rect.x+self.get_mapped_value()-int(self._slider_img.get_width()/2), \
            self.rect.centery-int(self._slider_img.get_height()/2)
    
    def get_slider_rect(self):
        x, y = self.calc_slider_pos()
        return pygame.Rect(x, y, self._slider_img.get_width(), self._slider_img.get_height())

    def get_mapped_value(self):
        return int(interp(self.value, [0, 100], [0, self.rect.width]))
    
    def set_range_value(self, mapped_value):
        self.value = int(interp(mapped_value, [0, self.rect.width], [0, 100]))
        self.post_event(Event.SLIDER_MOVED)
    
    def eventloop(self, event: pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.get_slider_rect().collidepoint(mouse_pos):
                self._mouse_held = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self._mouse_held = False
        
    def get_slider_distance_x(self, pos: tuple):
        return math.dist((self.get_slider_rect().center[0], 0), (pos[0], 0))
    
    def get_slider_distance_y(self, pos: tuple):
        return math.dist((0, self.get_slider_rect().center[1]), (0, pos[1]))   
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
   
        if self._mouse_held:
            if self.get_slider_distance_x(mouse_pos) > SLIDER_HELD_DIST_X:
                self._mouse_held = False
            elif self.get_slider_distance_y(mouse_pos) > SLIDER_HELD_DIST_Y:
                self._mouse_held = False
            mouse_value = mouse_pos[0]-self.rect.x
            if mouse_value > -1 and mouse_value <= self.rect.width:
                self.set_range_value(mouse_value)

    def render(self, surface: pygame.Surface):
        pygame.draw.line(surface, Colors.BLACK, (self.rect.left, self.rect.centery), (self.rect.right, self.rect.centery), 4)
        surface.blit(self._slider_img, self.calc_slider_pos())

class TextBox(UIElement):
    """
    A UI element for getting text from the user.
    """
    def __init__(self, id: str, x: int, y: int, width: int, 
    height: int, text_style: dict = None, border_size = 3, root_center = True):
        super().__init__(id, x, y, width, height, root_center)
        if text_style is None:
            self.text = Text(0, 0, "", {"size": 20})
        
        else:
            self.text = Text(0, 0, "", text_style)
        
        
        self.selected = False
        self._border_size = border_size
        self._cursor_blink = True
        self._cursor_timer = Timer()
        self._cursor_timer.start()
        self._backspace_timer = Timer()
        self._held_backspace_timer = Timer()


    def is_appendable(self, string: str):
        text_size = get_text_size(self.text.string + string, self.text.style)
        if text_size[0] >= (self.rect.width-TEXTBOX_MARGIN*2):
            return False
        return True
    

    def eventloop(self, event: pygame.event.Event):
        keys = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pos):
                if not self.selected:
                    self.selected = True
                    self.post_event(Event.TEXTBOX_SELECTED)
            else:
                self.selected = False

        if self.selected:
            if event.type == pygame.KEYDOWN:
                hit_key = True
                key_name = pygame.key.name(event.key)
                if key_name == "space":
                    if self.is_appendable(" "):
                        self.text.add(" ")
                elif key_name == "backspace":
                    self._backspace_timer.start()
                    self._held_backspace_timer.start()
                    if self.text.string:
                        self.text.pop()
                elif key_name == "return":
                    self.post_event(Event.TEXTBOX_POSTED)

                elif len(key_name) == 1:
                    string_data = key_name
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        string_data = key_name.upper()
                        if key_name in TEXTBOX_SHIFT_CHARS.keys():
                            string_data = TEXTBOX_SHIFT_CHARS[key_name]
                        elif key_name == "v" and event.mod and pygame.KMOD_CTRL:
                            if self.is_appendable(pyperclip.paste()):
                                string_data = pyperclip.paste()
                    if self.is_appendable(string_data):
                        self.text.add(string_data)
                else:
                    hit_key = False
                
                if hit_key:
                    self._cursor_timer.start()
                    self._cursor_blink = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self._backspace_timer.reset()
    
    def update(self):
        self.text.center_y(pygame.Rect(0, 0, self.rect.width, self.rect.height))
        keys = pygame.key.get_pressed()
        if self.selected:
            if keys[pygame.K_BACKSPACE]:
                if self._backspace_timer.passed(TEXTBOX_BACKSPACE_START_DELAY):
                    if self._held_backspace_timer.passed(TEXTBOX_BACKSPACE_DELAY):
                        self._held_backspace_timer.start()
                        if self.text.string:
                            self.text.pop()
                
        
    def render(self, surface: pygame.Surface):
        render_border(surface, self.rect, self._border_size)
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.text.render(surf)
        surface.blit(surf, (self.rect.x + TEXTBOX_MARGIN, self.rect.y))
        
        # render cursor
        if self.selected:
            x = self.rect.x+TEXTBOX_MARGIN+self.text.get_width()
            string = ""
            if self._cursor_blink:
                string = "|"
            
            if self._cursor_timer.passed(TEXTBOX_CURSOR_BLINK_TIME):
                self._cursor_timer.start()
                self._cursor_blink = not self._cursor_blink
            

            text = Text(x, 0, string)
            text.center_y(self.rect)
            text.render(surface)


class CheckBox(UIElement):
    """
    A UI element implements a basic togglable button.
    """
    
    def __init__(self, id: str, x: int, y: int, width: int,
    height: int, symbol = CheckBoxType.CHECK_SYMBOL, color_style = ColorStyle.WHITE,
     checked = False, root_center = True):
        super().__init__(id, x, y, width, height, root_center)
        self._filled_image = get_checkbox_img(True, color_style, symbol, self.rect.size)
        self._empty_image = get_checkbox_img(False, color_style, symbol, self.rect.size)
        self.checked = checked
        self.update_image()

    def update_image(self):
        if self.checked:
            self._image = self._filled_image
        else:
            self._image = self._empty_image
        
    
    def eventloop(self, event: pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mouse_pos):
                self.checked = not self.checked
                self.update_image()
                self.post_event(Event.CHECKBOX_CLICKED)
    
    def update(self):
        pass

    def render(self, surface: pygame.Surface):
        surface.blit(self._image, self.rect.topleft)

class TogglableButtonGroup:
    """
    A class for grouping and configuring buttons to be togglable with each other.
    """
    def __init__(self, buttons: list):
        self.buttons = buttons
        self.ids = [button.id for button in buttons]
        self.selected = None
    
    def eventloop(self, event: pygame.event.Event):
        for button in self.buttons:
            button.eventloop(event)
        if event.type == Event.BUTTON_CLICKED:
            if event.ui_id in self.ids:
                clicked_button = event.ui_element
                clicked_button._force_down = True
                for button in self.buttons:
                    if button != clicked_button:
                        button._force_down = False
                self.selected = clicked_button
        
    def update(self):
        for button in self.buttons:
            button.update()

    def render(self, surface: pygame.Surface):
        for button in self.buttons:
            button.render(surface)

        


class UIManager:
    """
    A built in Manager class that handles updating and provides an interface for UI.
    """
    def __init__(self, window):
        self.window = window
        self.ui = []
    
    def add(self, value):
        if type(value) is list:
            self.ui = self.ui + value
        else:
            self.ui.append(value)
    
    def clear(self):
        self.ui = []
    
    def get_element(self, id: str):
        for element in self.ui:
            if element.id == id:
                return element
        raise ValueError(f"No element with id: {id}")

    def eventloop(self, event: pygame.event.Event):
        for element in self.ui:
            element.eventloop(event)
    
    def update(self):
        for element in self.ui:
            element.update()
            element.render(self.window.screen)


