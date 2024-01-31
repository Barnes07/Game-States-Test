import pygame 
import os 

class Floor (pygame.sprite.Sprite):
    def __init__(self, x, y, group, game):
        super().__init__(group)
        self.x = x
        self.y = y
        self.game = game
        self.current_image = pygame.image.load(os.path.join(self.game.assets_dir, "map", "grass.png")).convert_alpha()
        self.rect = self.current_image.get_rect(center = (self.x, self.y))



