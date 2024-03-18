import os
import time
import pygame 
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, group):
        super().__init__(group)
        self.game = game
        self.group = group
        self.x = 0
        self.y = 0


        