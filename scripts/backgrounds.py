import StoryFrames
import settings
import images
import pygame
import random
import resources
import animations

x = settings.dimensions[0]
y = settings.dimensions[1]

# MAIN MENU ------------------------------------------------------------------------------------------
MMTreesLayer1 = []
for i in range(0, x + 1, 75):
    MMTreesLayer1.append(images.PineTree((i, y - 345)))

for i in range(-38, x + 1, 75):
    MMTreesLayer1.append(images.PineTree((i, y - 310)))

for i in range(0, x + 1, 75):
    MMTreesLayer1.append(images.PineTree((i, y - 275)))

road = images.Road((0, 460))
road2 = images.Road((640, 460))

clouds = [
    images.Cloud((random.randint(0, x), random.randint(0, y - 345))),
    images.Cloud((random.randint(0, x), random.randint(0, y - 345))),
    images.Cloud((random.randint(0, x), random.randint(0, y - 345))),
    images.Cloud((random.randint(0, x), random.randint(0, y - 345))),
    images.Cloud((random.randint(0, x), random.randint(0, y - 345))),
    images.Cloud((random.randint(0, x), random.randint(0, y - 345)))
]

startButton = resources.Button("start_button", (x / 2 - 184 / 2, (y / 2 + 75) - y / 4), (184, 68))
quitButton = resources.Button("quit_button", (x / 2 - 184 / 2, (y / 2 + 3 * 75) - y / 4), (184, 68))
optionsButton = resources.Button("options_button", (x / 2 - 184 / 2, (y / 2 + 2 * 75) - y / 4), (184, 68))


def backgroundMM(forest=False):
    match settings.time:
        case settings.Time.NOON:
            pygame.draw.rect(settings.window, (0, 150, 240), (0, 0, x, y))
            images.Sun((20, 20)).update()
        case settings.Time.SUNRISE:
            pygame.draw.rect(settings.window, (247, 205, 93), (0, 0, x, y))
            images.Sun((20, 150)).update()
        case settings.Time.SUNSET:
            pygame.draw.rect(settings.window, (251, 144, 98), (0, 0, x, y))
            images.Sun((850, 150)).update()
        case settings.Time.NIGHT:
            pygame.draw.rect(settings.window, (12, 20, 69), (0, 0, x, y))
            images.Sun((1000, 1000)).update()
    if not forest:
        pygame.draw.rect(settings.window, (21, 50, 30), (0, 350, x, 150))
        for tree in MMTreesLayer1:
            tree.update()
        road.update()
        road2.update()
        for cloud in clouds:
            if cloud.imageRect.x < -90:
                cloud.imageRect.x = x
                cloud.imageRect.y = random.randint(0, 290)
            cloud.update()
    else:
        pygame.draw.rect(settings.window, (21, 50, 30), (0, 0, x, y))
        for tree in MMTreesLayer1:
            tree.update()
    pygame.draw.rect(settings.window, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                     (0, 600, 100, 100))


def updateMainMenu():
    backgroundMM()
    if startButton.update() and not animations.slideAnim:
        animations.slideAnimation(resources.States.MAINGAME)
    if quitButton.update():
        settings.running = False
    optionsButton.update()


# Test Game Screen  ------------------------------------------------------------------------------------------

backButton = resources.Button("quit_button", (10, 10), (92, 34))


def updateMainGame():
    if settings.state == resources.States.FOREST:
        backgroundMM(True)
    else:
        backgroundMM()
    settings.player.rect.y = 400
    settings.player.update()

    StoryFrames.inState()

    if animations.slideAnim:
        animations.slideAnimProgress()

    if backButton.update():
        animations.slideAnimation(resources.States.MAINMENU)


def battleBackground():
    settings.window.fill((255, 255, 255))

# END SCREEN ------------------------------------------------------------------------------------------
