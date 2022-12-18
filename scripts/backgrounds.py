import pygame
import settings
import images
import random
import resources
import animations
from enum import Enum
import inputs

x = settings.dimensions[0]
y = settings.dimensions[1]


class Time(Enum):
    NOON = 0
    SUNSET = 1
    SUNRISE = 2
    NIGHT = 3


times = {Time.NOON: "noon",
         Time.SUNSET: "sunset",
         Time.SUNRISE: "sunrise",
         Time.NIGHT: "night"}

time = Time.SUNRISE

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
    match time:
        case Time.NOON:
            pygame.draw.rect(settings.window, (0, 150, 240), (0, 0, x, y))
            images.Sun((20, 20)).update()
        case Time.SUNRISE:
            pygame.draw.rect(settings.window, (247, 205, 93), (0, 0, x, y))
            images.Sun((20, 150)).update()
        case Time.SUNSET:
            pygame.draw.rect(settings.window, (251, 144, 98), (0, 0, x, y))
            images.Sun((850, 150)).update()
        case Time.NIGHT:
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


class InStates(Enum):
    BEGIN = 0.0
    TEXT = 0.1
    TEXT2 = 0.2
    TEXT3 = 0.3
    TEXT4 = 0.4
    STAYPUT = 1.0
    TEXTC11 = 1.1
    TEXTC12 = 1.2
    LEFT = 2.0
    RIGHT = 3.0
    TEXTLR1 = 4.1
    TEXTLR2 = 4.2
    FOREST = 5.0


timerCount = 0


def timer(ticks):
    global timerCount
    if timerCount > ticks:
        return True
    else:
        timerCount += 1
        return False


def toNextState(newState):
    global state, wait, timerCount
    state = newState
    wait = False
    timerCount = 0


state = InStates.BEGIN
wait = False


def updateMainGame():
    global state, timerCount, wait, time, times
    if settings.state == resources.States.FOREST:
        backgroundMM(True)
    else:
        backgroundMM()
    settings.player.rect.y = 400
    settings.player.update()

    match state:

        case InStates.BEGIN:
            settings.player.lockMovement = True
            if timer(50):
                toNextState(InStates.TEXT)

        case InStates.TEXT:
            resources.TextBox("Controls:",
                              "Press enter to continue text boxes...",
                              "A and D to move the player, W to enter dark spots.").update()
            if inputs.inputs["enter"]:
                toNextState(InStates.TEXT2)

        case InStates.TEXT2:
            if timer(75):
                resources.TextBox("... You wake up in a mysterious land ...",
                                  "... You have memories of you driving a truck ...",
                                  "... Now you sit on this dirt road, with no truck in sight ...").update()
            if inputs.inputs["enter"]:
                toNextState(InStates.TEXT3)

        case InStates.TEXT3:
            if timer(75):
                resources.TextBox("... There is a thick forest on either side of the road ...",
                                  "... You realize you have a choice ...",
                                  "... You can either go left, right, or stay put ...").update()
            if inputs.inputs["enter"]:
                toNextState(InStates.TEXT4)

        case InStates.TEXT4:
            if timer(75) and not wait:
                resources.TextBox("... To go left, use A to move ...",
                                  "... To go right, use D to move ...",
                                  "... To stay put, press S ...").update()
            if inputs.inputs["enter"]:
                wait = True
                settings.player.lockMovement = False
            if inputs.inputs["s"]:
                toNextState(InStates.STAYPUT)
            if settings.player.rect.x < 1:
                animations.slideAnimation(resources.States.MAINGAME)
                toNextState(InStates.LEFT)
                time = Time.SUNSET
            if settings.player.rect.x > settings.dimensions[0] - 39:
                animations.slideAnimation(resources.States.MAINGAME)
                toNextState(InStates.RIGHT)
                time = Time.SUNSET

        case InStates.LEFT:
            if not wait:
                resources.TextBox("... You decided to go left. ...",
                                  f"... You travel ten miles over the course of 5 hours. It is now {times[time]}. ...",
                                  "... Where you stop seems to be exactly where you started. ...").update()
            else:
                resources.TextBox("... You can either sleep on the road, ...",
                                  "... go into the forest, ...",
                                  "... or keep walking. ...").update()
            if inputs.inputs["enter"]:
                if wait:
                    toNextState(InStates.TEXTLR1)
                wait = True

        case InStates.RIGHT:
            settings.player.lockMovement = True
            settings.player.rect.x = settings.dimensions[0] / 2
            if not wait:
                resources.TextBox("... You decided to go right. ...",
                                  f"... You travel ten miles over the course of 5 hours. It is now {times[time]}. ...",
                                  "... Where you stop seems to be exactly where you started. ...").update()
            else:
                resources.TextBox("... You can either sleep on the road, ...",
                                  "... go into the forest, ...",
                                  "... or keep walking. ...").update()
            if inputs.inputs["enter"]:
                if wait:
                    toNextState(InStates.TEXTLR1)
                else:
                    wait = True

        case InStates.TEXTLR1:
            if not wait:
                settings.player.lockMovement = True
                resources.TextBox("... To sleep on the road, press S ...",
                                  "... To go into the forest, press W ...",
                                  "... To keep walking, use A and D").update()
            if inputs.inputs["enter"]:
                wait = True
                settings.player.lockMovement = False
            if inputs.inputs["s"]:
                toNextState(InStates.TEXTC12)
                wait = True
            if inputs.inputs["w"]:
                animations.slideAnimation(resources.States.FOREST)
                toNextState(InStates.FOREST)
            if settings.player.rect.x < 1:
                animations.slideAnimation(resources.States.MAINGAME)
                toNextState(InStates.TEXTLR2)
                time = Time.NIGHT
            if settings.player.rect.x > settings.dimensions[0] - 39:
                animations.slideAnimation(resources.States.MAINGAME)
                toNextState(InStates.TEXTLR2)
                time = Time.NIGHT

        case InStates.FOREST:
            if not wait: resources.TextBox("... You entered the forest ...",
                              "... You walk around for a while until you find an abandoned camp ...",
                              "... You can either sleep in the tent, rekindle the fire, or look for sticks ...")

        case InStates.TEXTLR2:
            resources.TextBox("... You decide to keep walking ...",
                              "...  ...",
                              "... You eventually pass out from exhaustion ...").update()
            if inputs.inputs["enter"]:
                animations.slideAnimation(resources.States.ENDGAMELOSE)

        case InStates.STAYPUT:
            resources.TextBox("",
                              "... You decide to stay put ...",
                              "").update()
            if inputs.inputs["enter"]:
                toNextState(InStates.TEXTC11)

        case InStates.TEXTC11:
            time = Time.SUNSET
            if timer(75) and not wait:
                resources.TextBox(f"... It is now {times[time]} ...",
                                  "... You can either go left with A or right with D ...",
                                  "... or, you can stay put with S ...").update()
            if inputs.inputs["enter"]:
                wait = True
                settings.player.lockMovement = False
            if inputs.inputs["s"]:
                toNextState(InStates.TEXTC12)
            if settings.player.rect.x < 0:
                animations.slideAnimation(resources.States.MAINGAME)
                toNextState(InStates.LEFT)
                time = Time.NIGHT
            if settings.player.rect.x > settings.dimensions[0] - 39:
                animations.slideAnimation(resources.States.MAINGAME)
                toNextState(InStates.RIGHT)
                time = Time.NIGHT

        case InStates.TEXTC12:
            time = Time.NIGHT
            if timer(75) and not wait:
                resources.TextBox(f"... It is now {times[time]} ...",
                                  "... You are super tired, and decide to fall asleep ...",
                                  "").update()
            if wait:
                resources.TextBox(f"... While you are sleeping, you are eaten by wolves ...",
                                  "",
                                  "... YOU LOST ...").update()
            if inputs.inputs["enter"]:
                if wait:
                    animations.slideAnimation(resources.States.ENDGAMELOSE)
                wait = True

    if animations.slideAnim:
        animations.slideAnimProgress()

    if backButton.update():
        animations.slideAnimation(resources.States.MAINMENU)

# END SCREEN ------------------------------------------------------------------------------------------
