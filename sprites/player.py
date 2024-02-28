import os
import time
import pygame 
import math
from sprites.wall import Wall

class Player(pygame.sprite.Sprite):

    def __init__(self, game, group, game_world):
        super().__init__(group)
        self.game = game 
        self.game_world = game_world
        self.sprite_dir = os.path.join(self.game.sprite_dir, "player")
        self.x = 500
        self.y = 500
        self.image_holder = pygame.image.load(os.path.join(self.sprite_dir, "player_down1.png")) #A placeholder of the player image so that a rectangle can be created. 
        self.rect = self.image_holder.get_rect(center = (self.x, self.y))
        self.group = group
        self.speed = 500
        self.direction = pygame.math.Vector2()
        self.load_sprites()
        self.current_frame = 0
        self.time_since_last_frame = 0

        self.actual_pos = (self.rect.centerx//self.game.block_size, self.rect.centery//self.game.block_size)

        self.previous_position = pygame.math.Vector2()

        self.artifacts_collected = 0


    
    def animate(self, delta_time, x_direction, y_direction):
        #Calculate elapsed time since last frame 
        self.time_since_last_frame += delta_time
        #if no direction entered, set animation to idle
        if x_direction == 0 and y_direction == 0:
            self.current_image = self.current_array[0]
            return
        #if direction is pressed, use the correct sequnece of frames
        if x_direction != 0:
            if x_direction > 0:
                self.current_array = self.right_sprites
            else:
                self.current_array = self.left_sprites
        if y_direction !=0:
            if y_direction > 0:
                self.current_array = self.down_sprites
            else:
                self.current_array = self.up_sprites
        #if sufficient time has passed, the next frame can be loaded 
        if self.time_since_last_frame > 0.15:
            self.time_since_last_frame = 0
            self.current_frame = self.current_frame + 1
            if self.current_frame == len(self.current_array):
                self.current_frame = 0
            self.current_image = self.current_array[self.current_frame]

    def load_sprites(self):
        #Load directory with player sprites
        self.sprite_dir = os.path.join(self.game.sprite_dir, "player")
        self.down_sprites = []
        self.up_sprites = []
        self.left_sprites =[]
        self.right_sprites = []
        #append lists
        for count in range (1,5):
            self.down_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_down" + str(count) + ".png")))
            self.up_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_up" + str(count) + ".png")))
            self.left_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_left" + str(count) + ".png")))
            self.right_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_right" + str(count) + ".png")))
        #Set frames for when idle
        self.current_image = self.up_sprites[0]
        self.current_array = self.up_sprites
    
    def check_wall_collision(self, delta_time):
        for sprite in self.group.sprites(): #iterate through all sprites 
            check = isinstance(sprite, Wall) #assign boolean value depending on if the sprite is wall or not
            if check == True:
                if pygame.sprite.collide_rect(self, sprite): #if the player and a wall is colliding
                    if sprite.rect.collidepoint(self.rect.centerx, self.rect.centery + self.game.block_size) or sprite.rect.collidepoint(self.rect.centerx, self.rect.centery - self.game.block_size):
                        #if player is colliding with wall in the y plane
                        self.rect.y -= self.speed * self.direction.y * delta_time #reverse player movement in y direction
                    if sprite.rect.collidepoint(self.rect.centerx + self.game.block_size, self.rect.centery) or sprite.rect.collidepoint(self.rect.centerx - self.game.block_size, self.rect.centery):
                        #if the player is colliding with wall in the x plane
                        self.rect.x -= self.speed * self.direction.x * delta_time #reverse player movement in x direction


    def update(self, delta_time, actions):
        velocity_x = self.rect.centerx - self.previous_position.x
        velocity_y = self.rect.centery - self.previous_position.y
        self.velocity = pygame.math.Vector2(velocity_x, velocity_y) #need to calculate velovity at start of update method

        #Get direction
        self.direction.x = actions["right"] - actions["left"]
        self.direction.y = actions["down"] - actions["up"]
        if self.direction.magnitude() != 0:
            self.direction.normalize()
        #Update location
        self.x += self.speed * delta_time * self.direction.x
        self.y += self.speed  * delta_time * self.direction.y
        self.rect.centerx += self.speed * delta_time * self.direction.x 
        self.rect.centery += self.speed * delta_time * self.direction.y
        self.actual_pos = (self.rect.centerx//self.game.block_size, self.rect.centery//self.game.block_size)
        #Animate the player
        self.animate(delta_time, self.direction.x, self.direction.y)

        self.previous_position = pygame.math.Vector2(self.rect.centerx, self.rect.centery) #need to update the previous position at the end of the update method



    def find_start_coordinates(self, map):
        found = False
        #iterate through all blocks in the map grid
        for a in range (0, self.game_world.actual_map_width):
            for b in range(0, self.game_world.actual_map_height):
                wall_count = 0
                #iterate through neighbouring 8 blocks
                for x in range (a-1, a+2):
                    for y in range(b-1, b+2):
                        #check if the block is within map bounds
                        if 0 <= x < self.game_world.actual_map_width and 0 <= y < self.game_world.actual_map_height:
                            #check if block is a wall
                            if map[x][y] == 0:
                                wall_count = wall_count + 1
                        else:
                            wall_count = wall_count + 1
                if wall_count == 0:
                    #set player starting coordinates to those stored in a and b
                    a = a * self.game.block_size
                    b = b * self.game.block_size
                    if found == False:
                        self.set_coordinates(a, b)
                        found = True




    def set_coordinates(self, x, y):
        self.rect = self.image_holder.get_rect(center = (x, y))
    

       


        

    def render(self, display):
        display.blit(self.current_image, (self.x, self.y))
        