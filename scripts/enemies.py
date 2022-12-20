import random
import resources
import pygame

class Wolf(resources.Entity):
    def __init__(self):
        super().__init__(pygame.transform.scale(pygame.image.load("resources/wolf.png"), (10, 10)), (870, 300), 10, 12, "wolf")

class ForestBoss(resources.Entity):
    def __init__(self):
        super().__init__(pygame.transform.scale(pygame.image.load("resources/forest_boss.png"), (25, 25)), (870, 300), 12, 100, "tree monster")

class RuinBoss(resources.Entity):
    def __init__(self):
        super().__init__(pygame.transform.scale(pygame.image.load("resources/rock_boss.jpg"), (25, 25)), (870, 300), 12, 100, "ruin monster")