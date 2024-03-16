import pygame
import os
from sprites.artifact import Artifact

class Smoke_Bomb(Artifact):
    def __init__(self, game, game_world, group):
        super().__init__(game, game_world, group)
        self.game = game
        self.game_world = game_world
        self.x = 0
        self.y = 0
        self.current_image = pygame.image.load(os.path.join(self.game.sprite_dir, "smoke_bomb", "smoke_bomb.png"))
        self.rect = self.current_image.get_rect(center = (self.x, self.y))

    
    #use polymorphism on collect method to prevent loot bag filling up upon collection
        
    def get_picked_up(self):
        self.game_world.player.smoke_bomb_picked_up = True
        pygame.sprite.Sprite.kill(self)
    
    


    
                  