import pygame
import os
import random

class Exit_Door(pygame.sprite.Sprite):
        def __init__ (self, game, game_world, group):
            super().__init__(group)
            self.game = game
            self.game_world = game_world
            self.x = 400
            self.y = 400
            self.current_image = pygame.image.load(os.path.join(self.game.assets_dir, "map", "aztec_door.png"))
            self.rect = self.current_image.get_rect(center = (self.x, self.y))

            self.collision_rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height*0.75)
            self.collision_rect.topleft = self.rect.topleft
        
        def get_random_starting_coordinates(self, map):
            found = False
            #iterate through random cooridinates until a valid position is found
            while found == False:
                random_x = random.randint(1, self.game_world.actual_map_width - 1)
                random_y = random.randint(1, self.game_world.actual_map_height - 1)
                wall_count = 0
                #iterate through neighbouring 8 blocks
                for x in range (random_x-2, random_x+3):
                    for y in range(random_y-2, random_y+3):
                        #check if the block is within map bounds
                        if 0 <= x < self.game_world.actual_map_width and 0 <= y < self.game_world.actual_map_height:
                            #check if block is a wall
                            if map[x][y] == 0:
                                wall_count = wall_count + 1
                        else:
                            wall_count = wall_count + 1
                if wall_count == 0:
                    #set player starting coordinates to those stored in a and b
                    random_x = random_x * self.game.block_size
                    random_y = random_y * self.game.block_size
                    if found == False:
                        self.set_coordinates(random_x, random_y)
                        found = True

        def set_coordinates(self, x, y):
            self.rect = self.current_image.get_rect(center = (x,y)) #sets coordinates of rectangle for image placement 
            self.collision_rect.topleft = self.rect.topleft #sets coordinates of rectangle for collision detection
        
        def check_collision(self, player, delta_time):
            if pygame.Rect.colliderect(self.collision_rect, player.rect): #checks for collision between player and collision rectnagles 
                if self.collision_rect.collidepoint(player.rect.centerx, player.rect.centery + self.game.block_size) or self.collision_rect.collidepoint(player.rect.centerx, player.rect.centery - self.game.block_size):
                    #if the player is colliding with the door in the vertical direction, reverse the movement made in the y direction
                    player.rect.y -= player.speed * player.direction.y * delta_time
                if self.collision_rect.collidepoint(player.rect.centerx + self.game.block_size, player.rect.centery) or self.collision_rect.collidepoint(player.rect.centerx - self.game.block_size, player.rect.centery):
                    #if the player is colliding with the door in the horizontal direction, reverse the movement made in the x direction
                    player.rect.x -= player.speed * player.direction.x * delta_time

        def check_door_proximity(self, player):
            if self.collision_rect.left <= player.rect.centerx <= self.collision_rect.right:
                if self.collision_rect.collidepoint(player.rect.centerx, player.rect.centery - self.game.block_size): #negative since (0,0) is top left
                    return(True)


                    



                    




        
            