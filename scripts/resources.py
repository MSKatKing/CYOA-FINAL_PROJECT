import pygame
import settings
import inputs
import images
import animations
from enum import Enum

pygame.init()

class States(Enum):
    MAINMENU = 0
    MAINGAME = 1
    PAUSE = 1.1
    INVENTORY = 1.2
    CHESTOPEN = 1.3
    BOSS = 1.4
    ENDGAMEWIN = 2.1
    ENDGAMELOSE = 2.2
    OPTIONS = 3
    CHARACTERCUSTOM = 4
    CHARACTERCUSTOMP2 = 4.1


class Text:
    def __init__(self, txt, dest, color):
        self.txt = txt
        self.font = pygame.font.Font("resources/pixel_text.ttf", 16)
        self.color = color
        self.render = self.font.render(txt, False, color)
        self.rect = self.render.get_rect(topleft=dest)

    def changeText(self, txt):
        self.render = self.font.render(txt, False, self.color)

    def update(self):
        settings.window.blit(self.render, self.rect)


class TextBox:
    def __init__(self, line1, line2, line3):
        self.txts = [Text(line1, (50, 475), (0, 0, 0)), Text(line2, (50, 500), (0, 0, 0)),
                     Text(line3, (50, 525), (0, 0, 0))]
        self.animation = 0

    def setTextL3(self, text):
        self.txts[2] = Text(text, (50, 525), (0, 0, 0))

    def setTextL1(self, text):
        self.txts[0] = Text(text, (50, 475), (0, 0, 0))

    def update(self):
        if self.animation < 50:
            self.animation += 1
        pygame.draw.rect(settings.window, (255, 255, 255), (25, 450-self.animation, 850, 100))
        for txt in self.txts:
            txt.update()


class Button:
    def __init__(self, prefix, loc, size):
        self.images = [images.Image("resources/"+prefix+".png", loc, size, 0),
                       images.Image("resources/"+prefix+"_hover.png", loc, size, 0),
                       images.Image("resources/"+prefix+"_press.png", loc, size, 0)
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


    def image_at(self, rectangle, colorkey = None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if not colorkey == None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
# ------------------------------------------------------
class Battle:
    def __init__(self, player, opponent):
        self.player = player
        self.opponent = opponent
        animations.battleAnimation()

class Entity:
    def __init__(self, image, location, damage, health):
        self.image = image
        self.rect = image.get_rect(topleft=location)
        self.maxHealth = health
        self.health = health
        print(self.maxHealth)
        self.damage = damage

    def update(self):
        settings.window.blit(self.image, self.rect)
