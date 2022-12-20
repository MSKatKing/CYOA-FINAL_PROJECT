import pygame
import settings
import resources

slideAnim = False
slideAnimOffset = settings.dimensions[0]
nextState = None

def slideAnimation(state):
    global slideAnim, nextState
    slideAnim = True
    nextState = state
    slideAnimProgress()


def slideAnimProgress():
    global slideAnimOffset, slideAnim, nextState
    if slideAnim:
        slideAnimOffset -= 30
        pygame.draw.rect(settings.window, (0, 0, 0), (slideAnimOffset, 0, settings.dimensions[0], settings.dimensions[1]))
        if slideAnimOffset <= 0:
            settings.state = nextState
        if slideAnimOffset <= -settings.dimensions[0]:
            slideAnim = False
            slideAnimOffset = settings.dimensions[0]
            nextState = None

battleAnim = False
battleAnimReverse = False
battleAnimOffset = (settings.dimensions[0]/2, settings.dimensions[1]/2)
battleAnimSize = 1
count = 0
battleState = None

def battleAnimation(state):
    global battleAnim, battleState
    battleAnim = True
    battleState = state
    battleAnimProgress()

def battleAnimProgress():
    global battleAnim, battleAnimReverse, battleAnimOffset, battleAnimSize, count, battleState
    if battleAnim:
        pygame.draw.circle(settings.window, (0, 0, 0), battleAnimOffset, battleAnimSize)
        if battleAnimReverse:
            battleAnimSize -= 15
            if battleAnimSize <= 0:
                battleAnim = False
                battleAnimReverse = False
                battleAnimSize = 1
                count = 0
                battleState = None
        else:
            battleAnimSize += 15
            if battleAnimSize >= 600:
                count += 1
                if count >= 40:
                    battleAnimReverse = True
                    settings.state = battleState
