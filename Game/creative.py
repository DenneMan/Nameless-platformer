import pygame
import engine
import helper
from config import *

#################################################
#  Main player class, used for the player only  #
#################################################
class CreativePlayer():

    def __init__(self, _self):
        self.transform = _self.transform

        self.speed = 1000
        self.direction = pygame.math.Vector2(0, 0)

    def update(self, dt):
        self.transform.pos += self.direction * self.speed * dt