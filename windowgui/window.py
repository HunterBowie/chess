import pygame
from .util import Colors
from .flash import FlashManager
from .ui import UIManager

class Window:
    """
    A class for handling window settings and updating managers.
    """
    PUBLIC_MANAGER = 0
    UI_MANAGER = 1
    FLASH_MANAGER = 2

    class PublicManagerPlaceholder:
        pass

    def __init__(self, screen_size):
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.running = False
        self.max_fps = 60
        self.bg_color = Colors.WHITE
        self.force_quit = False
        self._managers = [
            self.PublicManagerPlaceholder(),
            UIManager(self),
            FlashManager(self)
        ]
        self.ui = self._managers[self.UI_MANAGER]
        self.flash = self._managers[self.FLASH_MANAGER]
        self.on_manager_change = lambda window : None
    
    def set_manager(self, manager):
        if callable(self.on_manager_change):
            self.on_manager_change.__call__(self)
        self.ui.clear()
        if self._has_callable_attr(manager, "init_ui"):
            manager.init_ui()
        self._managers[self.PUBLIC_MANAGER] = manager

    def get_manager(self, manager):
        return self._managers[self.PUBLIC_MANAGER]
    
    def start(self, auto_cycle=False):
        self.running = True
        if auto_cycle:
            while self.running:
                self.update(auto_eventloop=True)
            self.end()

    def end(self):
        for manager in self._managers:
            if self._has_callable_attr(manager, "end"):
                manager.end()
        quit()

    def eventloop(self, event):
        for manager in self._managers:
            if self._has_callable_attr(manager, "eventloop"):
                manager.eventloop(event)

        if event.type == pygame.QUIT:
            self.running = False
            if self.force_quit:
                self.end()
                quit()
        
    def update(self, auto_eventloop=False):
        if auto_eventloop:
            for event in pygame.event.get():
                self.eventloop(event)

        for manager in self._managers:
            if self._has_callable_attr(manager, "update"):
                manager.update()
        
        pygame.display.flip()
        self.clock.tick(self.max_fps)
        self.screen.fill(self.bg_color)
    
    @staticmethod
    def _has_callable_attr(object, attr):
        value = getattr(object, attr, None)
        if value == None:
            return False
        if callable(value):
            return True
        return False
        


