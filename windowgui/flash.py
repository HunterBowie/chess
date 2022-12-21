import pygame
from .util import Timer
from .constants import FLASH_FADE_SPEED, FLASH_FADE_TIME

class Flash:
    """
    A class for temperarily rendering messages on the screen.
    """
    def __init__(self, x, y, size, text, color, duration=2.3):
        self.text = text
        self.alpha = 0
        self.x = x
        self.y = y
        self.size = size
        self._rect = pygame.Rect(0, 0, size[0], size[1])
        self.color = color
        self._surf_init()

        self.timer = Timer()
        self.duration = duration
    
    def start(self):
        self.timer.start()
    
    def _surf_init(self):
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.rect(self.surface, self.color, self._rect, border_radius=5)
        text_x, text_y = self.text.x, self.text.y
        self.text.center(self._rect)
        self.text.x += text_x
        self.text.y += text_y
        
        self.text.render(self.surface)
        self.surface.set_alpha(self.alpha)
    
    def _surf_fade_in(self):
        if self.alpha < 255:
            self.alpha += FLASH_FADE_SPEED
            self.surface.set_alpha(self.alpha)
    
    def _surf_fade_out(self):
        if self.alpha > 0:
            self.alpha -= FLASH_FADE_SPEED
            self.surface.set_alpha(self.alpha)
    
    def is_finished(self):
        return self.timer.passed(self.duration)
    
    def render(self, surface):
        if self.timer.get() < FLASH_FADE_TIME:
            self._surf_fade_in()
        elif self.duration-self.timer.get() < FLASH_FADE_TIME:
            self._surf_fade_out()
        surface.blit(self.surface, (self.x, self.y))

class FlashManager:
    """
    A built in Manager class that handles updating and provides an interface for flashing.
    """
    def __init__(self, window):
        self.window = window
        self.flashes = []
    
    def clear(self):
        self.flashes.clear()

    def add(self, flash):
        flash.start()
        self.flashes.append(flash)

    def update(self):
        finished_flashes = []
        for flash in self.flashes:
            if flash.is_finished():
                finished_flashes.append(flash)
                continue
            flash.render(self.window.screen)
        
        for flash in finished_flashes:
            self.flashes.remove(flash)
