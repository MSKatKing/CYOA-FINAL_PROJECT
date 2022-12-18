import random
import pygame
import settings


class Image:
    def __init__(self, path, loc, size, scrollSpeed):
        self.image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)
        self.imageRect = self.image.get_rect(topleft=loc)
        self.scrollSpeed = scrollSpeed

    def update(self):
        self.imageRect.x += self.scrollSpeed
        settings.window.blit(self.image, self.imageRect)


class PineTree(Image):
    def __init__(self, loc=(0, 0), scrollSpeed=0):
        super().__init__("resources/pine_tree.png", loc, (75, 135), scrollSpeed)


class Road(Image):
    def __init__(self, loc=(0, 0)):
        super().__init__("resources/road.png", loc, (640, 140), 0)


class Sun(Image):
    def __init__(self, loc=(0, 0)):
        super().__init__("resources/sun.png", loc, (88, 88), 0)


class Cloud(Image):
    def __init__(self, loc=(0, 0)):
        super().__init__("resources/cloud.png", loc, (88, 24), -1)
