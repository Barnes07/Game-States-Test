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

    
    def check_player_collision(self): #polymorphism of the method in the artifact class
        if pygame.sprite.collide_rect(self, self.game_world.player): #in_built pygame sprite method to check collision
            self.get_picked_up()
        
    def get_picked_up(self):
        self.game_world.player.smoke_bomb_picked_up = True
        pygame.sprite.Sprite.kill(self)
    
    


    
                  