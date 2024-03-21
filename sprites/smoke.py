import pygame
import os

class Smoke(pygame.sprite.Sprite):
    def __init__ (self, game, game_world, group):
        super().__init__(group) 
        self.game = game
        self.game_world = game_world
        self.x = 0
        self.y = 0
        self.time_since_start = 0
        self.current_image = pygame.image.load(os.path.join(self.game.sprite_dir, "smoke", "smoke_background.png")).convert_alpha()
        self.current_image.set_alpha(100)

        self.rect = self.current_image.get_rect(center = (self.x, self.y))
    

    def update(self, delta_time):
        self.time_since_start += delta_time
        if self.time_since_start > 10:
            pygame.sprite.Sprite.kill(self) #remove smoke from camera group




         

    