import pygame 
import random
import os 

class Artifact(pygame.sprite.Sprite):
    def __init__ (self, game, game_world, group):
        super().__init__(group)
        self.game = game
        self.game_world = game_world
        self.x = 0
        self.y = 0
        self.current_image = pygame.image.load(os.path.join(self.game.sprite_dir, "artifact", "artifact.png"))
        self.rect = self.current_image.get_rect(center = (self.x, self.y))

    def find_start_coordiantes(self, map):
        #Find a pair of random valid coordinates.
        found = False
        while found == False:
            random_x = random.randint(1, self.game_world.actual_map_width - 1)
            random_y = random.randint(1, self.game_world.actual_map_height - 1)
            if map[random_x][random_y] == 1:
                found = True
                self.set_start_coordinates(random_x, random_y)

    def set_start_coordinates(self, x, y):
        self.rect = self.current_image.get_rect(center = (x*self.game.block_size, y*self.game.block_size))

    def check_player_collision(self):
        if pygame.sprite.collide_rect(self, self.game_world.player): #in_built pygame sprite method to check collision
            self.get_picked_up()
            self.game_world.player.artifacts_collected += 1
            self.game_world.filled_height += self.game_world.fill_per_artifact #increments the height of the "filled" loot bag 
            if self.game_world.player.speed + -20 > 100:
                self.game_world.player.speed += -20


    
    def get_picked_up(self):
        pygame.sprite.Sprite.kill(self)

    def update(self):
        if self.alive():
            self.check_player_collision()




