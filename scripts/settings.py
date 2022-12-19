from enum import Enum
import pygame

running = False
dimensions = (900, 600)
clock = 0
window = pygame.display.set_mode(dimensions)
state = None


class Time(Enum):
    NOON = 0
    SUNSET = 1
    SUNRISE = 2
    NIGHT = 3


time = Time.NOON
times = {Time.NOON: "noon",
         Time.SUNSET: "sunset",
         Time.SUNRISE: "sunrise",
         Time.NIGHT: "night"}

player = None
