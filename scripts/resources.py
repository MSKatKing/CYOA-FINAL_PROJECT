import pygame
import settings
import inputs
import images
import animations
from enum import Enum
import random

pygame.init()


class States(Enum):
    MAINMENU = 0
    MAINGAME = 1
    FOREST = 1.01
    BOSS = 1.4
    ENDGAMEWIN = 2.1
    ENDGAMELOSE = 2.2
    OPTIONS = 3
    BATTLE = 4


class Text:
    def __init__(self, txt, dest, color, centered=False, size=16):
        self.txt = txt
        self.font = pygame.font.Font("resources/pixel_text.ttf", size)
        self.color = color
        self.render = self.font.render(txt, False, color)
        if not centered: self.rect = self.render.get_rect(topleft=dest)
        else: self.rect = self.render.get_rect(center=dest)

    def changeText(self, txt):
        self.render = self.font.render(txt, False, self.color)

    def update(self):
        settings.window.blit(self.render, self.rect)


class TextBox:
    def __init__(self, line1, line2, line3):
        self.txts = [Text(line1, (75, 475), (0, 0, 0)), Text(line2, (75, 500), (0, 0, 0)),
                     Text(line3, (75, 525), (0, 0, 0))]
        self.image = images.Image("resources/textbox.png", (25, 450), (850, 125), 0)
        self.anim = 25
        self.textY = (475, 500, 525)

    def setTextL3(self, text):
        self.txts[2] = Text(text, (50, 525), (0, 0, 0))

    def setTextL1(self, text):
        self.txts[0] = Text(text, (50, 475), (0, 0, 0))

    def update(self):
        if self.anim > -1:
            self.anim -= 5
        self.image.imageRect.y = 450 + self.anim
        self.image.update()
        for txt in self.txts:
            txt.rect.y = self.textY[self.txts.index(txt)] + self.anim
            txt.update()


class Button:
    def __init__(self, prefix, loc, size):
        self.images = [images.Image("resources/" + prefix + ".png", loc, size, 0),
                       images.Image("resources/" + prefix + "_hover.png", loc, size, 0),
                       images.Image("resources/" + prefix + "_press.png", loc, size, 0)
                       ]
        self.currentImage = self.images[0]

    def update(self):
        mousePos = pygame.mouse.get_pos()

        mousePointer = pygame.draw.rect(settings.window, (0, 0, 0), (mousePos[0], mousePos[1], 1, 1))

        if mousePointer.colliderect(self.images[0].imageRect):
            if inputs.inputs["mouseHold"]:
                self.currentImage = self.images[2]
            else:
                self.currentImage = self.images[1]
            if inputs.inputs["mouseUp"]:
                settings.window.blit(self.currentImage.image, self.currentImage.imageRect)
                return True
        else:
            self.currentImage = self.images[0]

        settings.window.blit(self.currentImage.image, self.currentImage.imageRect)

        return False


# THE CODE FROM HERE TO THE DASHED LINE IS NOT MINE
class SpriteSheet:

    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if not colorkey == None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


# ------------------------------------------------------
class Battle:
    def __init__(self, opponent, nextState, inState):
        self.winner = None
        self.opponentChoice = None
        self.opponent = opponent
        self.battle = False
        self.battleOver = False
        self.playerChoice = None
        self.moveOn = False
        self.moveOn2 = False
        self.count = 0
        self.state = nextState
        self.nextInstate = inState
    def update(self):
        settings.player.rect.x = 30
        settings.player.rect.y = settings.dimensions[1] / 2
        self.opponent.update()
        if settings.state == States.BATTLE:
            if not self.battle:
                TextBox("", f"Oh no! You have encountered a {self.opponent.name}", "").update()
                if inputs.inputs["enter"]:
                    self.battle = True
            elif not self.battleOver:
                if self.playerChoice is None:
                    TextBox("What will you do?", "", "Press F to fight or press D to defend!").update()
                    if inputs.inputs["f"]:
                        self.playerChoice = 0
                        self.opponentChoice = random.randint(0, 1)
                        if self.opponentChoice == 0:
                            settings.player.health -= self.opponent.damage
                            self.opponent.health -= settings.player.damage + settings.player.damageAdder
                    if inputs.inputs["d"]:
                        self.playerChoice = 1
                        self.opponentChoice = random.randint(0, 1)
                        settings.player.health += 5
                else:
                    if not self.moveOn:
                        if self.playerChoice == 0:
                            if self.opponentChoice == 1:
                                TextBox("", f"You hit the {self.opponent.name} for 0 health since it defended itself!", "").update()
                                if inputs.inputs["enter"]:
                                    self.moveOn = True
                            else:
                                TextBox("", f"You hit the {self.opponent.name} for {settings.player.damage + settings.player.damageAdder} health!", "").update()
                                if inputs.inputs["enter"]:
                                    self.moveOn = True
                        else:
                            TextBox("", f"You defended yourself!", "").update()
                            if inputs.inputs["enter"]:
                                self.moveOn = True
                    else:
                        if not self.moveOn2:
                            if self.opponentChoice == 0:
                                if self.playerChoice == 0:
                                    TextBox("", f"The {self.opponent.name} hit you for {self.opponent.damage} health!", "").update()
                                    if inputs.inputs["enter"]:
                                        self.moveOn2 = True
                                else:
                                    TextBox("", f"The {self.opponent.name} hit you for 0 health since you defended yourself!", "").update()
                                    if inputs.inputs["enter"]:
                                        self.moveOn2 = True
                            else:
                                self.moveOn2 = True
                        else:
                            if self.opponent.health <= 0:
                                self.battleOver = True
                                self.winner = settings.player
                            elif settings.player.health <= 0:
                                self.battleOver = True
                                self.winner = self.opponent
                            else:
                                self.opponentChoice = None
                                self.playerChoice = None
                                self.moveOn = False
                                self.moveOn2 = False
            else:
                if self.winner == settings.player:
                    TextBox("", "You won the battle!", "").update()
                    if inputs.inputs["enter"]:
                        animations.battleAnimation(self.state)
                        self.nextInstate()
                else:
                    TextBox("", "You lost the battle!", "").update()
                    if inputs.inputs["enter"]:
                        animations.battleAnimation(States.ENDGAMELOSE)

        else:
            if animations.battleAnim:
                animations.battleAnimProgress()
            else:
                animations.battleAnimation(States.BATTLE)





class Entity:
    def __init__(self, image, location, damage, health, name = "unnamed_entity"):
        self.image = image
        self.rect = image.get_rect(center=location)
        self.maxHealth = health
        self.health = health
        self.damage = damage
        self.name = name

    def update(self):
        settings.window.blit(self.image, self.rect)


class GameFrame:
    def __init__(self, text1, condition1, condition2=None, condition3=None, condition4=None, condition5=None):
        if text1 is not None: self.textBox1 = TextBox(text1[0], text1[1], text1[2])
        else: self.textBox1 = None
        self.condition1 = condition1
        self.condition2 = condition2
        self.condition3 = condition3
        self.condition4 = condition4
        self.condition5 = condition5
        self.displayText = True

    def update(self):
        if self.textBox1 is not None and self.displayText: self.textBox1.update()
        if self.condition1[0]():
            self.condition1[1]()
        if self.condition2 is not None:
            if self.condition2[0](): self.condition2[1]()
        if self.condition3 is not None:
            if self.condition3[0](): self.condition3[1]()
        if self.condition4 is not None:
            if self.condition4[0](): self.condition4[1]()
        if self.condition5 is not None:
            if self.condition5[0](): self.condition5[1]()

    def disableText(self):
        self.displayText = False
