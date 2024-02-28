import pygame
import os

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, group, game):
        super().__init__(group)
        self.x = x #this is the actual x coordinate (already been multiplied by blocksize when wall object is instantiated)
        self.y = y #this is the actual y coordinate (already been multiplied by blocksize when wall object is instantiated)
        self.game = game
        self.current_image = pygame.image.load(os.path.join(self.game.assets_dir, "map", "wall.png")).convert_alpha()
        self.rect = self.current_image.get_rect(center = (self.x, self.y))


        

        