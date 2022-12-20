import random
import resources
import pygame

class Wolf(resources.Entity):
    def __init__(self):
        super().__init__(pygame.transform.scale(pygame.image.load("resources/sun.png"), (10, 10)), (10, 10), 10, 12)

class ForestBoss(resources.Entity):
    def __init__(self):
        super().__init__(pygame.transform.scale(pygame.image.load("resources/pine_tree.png"), (25, 25)), (10, 10), 10, 12)

class RuinBoss(resources.Entity):
    def __init__(self):
        super().__init__(pygame.transform.scale(pygame.image.load("resources/pine_tree.png"), (25, 25)), (10, 10), 10, 12)