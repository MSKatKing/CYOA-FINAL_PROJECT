import pygame
import settings
import resources
import inputs

pygame.init()


class Player:
    def __init__(self):
        self.images = resources.SpriteSheet("resources/player.png").load_strip((0, 0, 13, 23), 4,
                                                                               (242, 111, 155))  # dim: 121, 55, 77
        for image in self.images:
            self.images[self.images.index(image)] = pygame.transform.scale(image, (39, 69))
        self.rect = self.images[0].get_rect(topleft=(10, 10))
        self.currentImage = self.images[0]
        self.vel = (0, 0)
        self.animationCycle = 0
        self.speed = 3
        self.a, self.d = False, False
        self.facing = False
        self.lockMovement = False

    def update(self):
        if not self.lockMovement:
            self.move()

        settings.window.blit(self.currentImage, self.rect)

    def move(self):
        if inputs.inputs["a"]:
            self.vel = -self.speed
            if not self.facing:
                self.facing = True
                index = self.images.index(self.currentImage)
                for image in self.images:
                    self.images[self.images.index(image)] = pygame.transform.flip(image, True, False)
                self.currentImage = self.images[index]
        elif inputs.inputs["d"]:
            self.vel = self.speed
            if self.facing:
                self.facing = False
                index = self.images.index(self.currentImage)
                for image in self.images:
                    self.images[self.images.index(image)] = pygame.transform.flip(image, True, False)
                self.currentImage = self.images[index]
        else:
            self.vel = 0

        self.rect.x += self.vel

        if self.rect.x <= -1 or self.rect.x > settings.dimensions[0] - 15:
            self.rect.x -= self.vel
            self.vel = 0

        if not self.vel == 0:
            self.progressAnimation()
        else:
            self.cancelAnimation()

    def progressAnimation(self):
        if self.animationCycle > 100:
            self.animationCycle = 0
        elif self.animationCycle > 75:
            self.currentImage = self.images[3]
        elif self.animationCycle > 50:
            self.currentImage = self.images[2]
        elif self.animationCycle > 25:
            self.currentImage = self.images[1]
        elif self.animationCycle > 0:
            self.currentImage = self.images[0]

        self.animationCycle += 2

    def cancelAnimation(self):
        self.animationCycle = 0
        self.currentImage = self.images[0]
