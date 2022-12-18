import inputs
import pygame
import resources
import settings
import sys
import backgrounds
import animations
import player
import enemies

# TODO:
'''
- add player
    - add sprite
    - add movement
    - add animation(maybe)
- add main menu
    - add character customization
- add gamestates
    - main menu
    - options
    - game
    - end (win)
    - end (lose)
- add good art
    - medium priority
    - player + animation
    - title
    - animal sprites
    - main boss sprite
    - item sprites (maybe)
'''

pygame.init()

settings.clock = pygame.time.Clock()
settings.window = pygame.display.set_mode(settings.dimensions, pygame.RESIZABLE)
pygame.display.set_caption("Choose Your Own Adventure")

settings.player = player.Player()
pygame.display.set_icon(settings.player.images[0])

settings.state = resources.States.MAINGAME
settings.running = True
while settings.running:

    match settings.state:
        case resources.States.MAINMENU:
            backgrounds.updateMainMenu()
            if animations.slideAnim:
                animations.slideAnimProgress()
        case resources.States.MAINGAME:
            backgrounds.updateMainGame()
            if animations.slideAnim:
                animations.slideAnimProgress()
            if animations.battleAnim:
                animations.battleAnimProgress()
        case resources.States.ENDGAMEWIN:
            if animations.slideAnim:
                animations.slideAnimProgress()
        case resources.States.OPTIONS:
            if animations.slideAnim:
                animations.slideAnimProgress()


    # Update Inputs, Clock, and Display
    settings.clock.tick(60)
    inputs.updateInputs()
    pygame.display.update()
