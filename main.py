import pygame, windowgui, constants, game, assets

pygame.init()


window = windowgui.Window(constants.SCREEN_SIZE)
window.set_manager(game.Game(window))
pygame.display.set_caption("Chess")

assets.convert_images()

window.start(auto_cycle=True)

