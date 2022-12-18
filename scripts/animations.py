import pygame
import settings

slideAnim = False
slideAnimReverse = False
slideAnimOffset = 900
nextState = None


def slideAnimation(state):
    global slideAnim, nextState
    slideAnim = True
    nextState = state
    slideAnimProgress()


def slideAnimProgress():
    global slideAnimOffset, slideAnim, slideAnimReverse, nextState
    if slideAnim:
        if slideAnimReverse:
            slideAnimOffset -= 30
            pygame.draw.rect(settings.window, (0, 0, 0), (slideAnimOffset, 0, 900, 600))
            if slideAnimOffset <= -900:
                slideAnim = False
                slideAnimReverse = False
                slideAnimOffset = 900
                nextState = None
        else:
            slideAnimOffset -= 30
            pygame.draw.rect(settings.window, (0, 0, 0), (slideAnimOffset, 0, 900, 600))
            if slideAnimOffset <= 0:
                slideAnimReverse = True
                settings.state = nextState

battleAnim = False
battleAnimReverse = False
battleAnimOffset = (settings.dimensions[0]/2, settings.dimensions[1]/2)
battleAnimSize = 1
count = 0

def battleAnimation():
    global battleAnim
    battleAnim = True
    battleAnimProgress()

def battleAnimProgress():
    global battleAnim, battleAnimReverse, battleAnimOffset, battleAnimSize, count
    if battleAnim:
        pygame.draw.circle(settings.window, (0, 0, 0), battleAnimOffset, battleAnimSize)
        if battleAnimReverse:
            battleAnimSize -= 15
            if battleAnimSize <= 0:
                battleAnim = False
                battleAnimReverse = False
                battleAnimSize = 1
                count = 0
        else:
            battleAnimSize += 15
            if battleAnimSize >= 600:
                count += 1
                if count >= 40:
                    battleAnimReverse = True
