import os
from sprites.wall import Wall
import pygame

class Boundary_Wall(Wall):
    def __init__(self, x, y, group, game):
        super().__init__(x, y, group, game) #inherit from Wall
        self.current_image = pygame.image.load(os.path.join(self.game.assets_dir, "map", "boundary_wall.png")).convert_alpha()

            