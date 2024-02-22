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
        self.x = 1380
        self.y = 1380
        self.image_holder = pygame.image.load(os.path.join(self.sprite_dir, "player_down1.png")) #A placeholder of the player image so that a rectangle can be created. 
        self.rect = self.image_holder.get_rect(center = (self.x, self.y))
        self.group = group
        self.speed = 500
        self.direction = pygame.math.Vector2()
        self.load_sprites()
        self.current_frame = 0
        self.time_since_last_frame = 0

        self.actual_pos = (self.rect.centerx//self.game.block_size, self.rect.centery//self.game.block_size)

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
        for sprite in self.group.sprites():
            check = isinstance(sprite, Wall)      #"isinstance" is a function that returns a boolean value depending on whether the firsts parameter is of the class type mentioned in the second parameter
            if check == True:
                if pygame.sprite.collide_rect(self, sprite):
                    self.rect.center -= self.speed * self.direction * delta_time     # "-=" reverses the previous player's direction of movement and therefore stops the map from scrolling behind the player

    def update(self, delta_time, actions):
        #Get direction
        self.direction.x = actions["right"] - actions["left"]
        self.direction.y = actions["down"] - actions["up"]
        if self.direction.magnitude() != 0:
            self.direction.normalize()
        #Update location
        self.x += self.speed * delta_time * self.direction.x
        self.y += self.speed  * delta_time * self.direction.y
        self.rect.centerx += self.speed * delta_time * self.direction.x #these two lines are needed to also update the x and y coordinates of the rectangle so that the x and y coordinates in the centre_player method(camera_group)are updated and allow the assets to move in the opposite direction to the player. 
        self.rect.centery += self.speed * delta_time * self.direction.y
        self.actual_pos = (self.rect.centerx//self.game.block_size, self.rect.centery//self.game.block_size)
        #Animate the player
        self.animate(delta_time, self.direction.x, self.direction.y)

    def find_start_coordinates(self, map):
        for a in range (0, self.game_world.actual_map_width):
            for b in range(0, self.game_world.actual_map_height):
                wall_count = 0
                for x in range (a-1, a+2):
                    for y in range(b-1, b+2):
                        if 0 <= x < self.game_world.actual_map_width and 0 <= y < self.game_world.actual_map_height:
                            if map[x][y] == 0:
                                wall_count = wall_count + 1
                        else:
                            wall_count = wall_count + 1
                if wall_count == 0:
                    #set player starting coordinates to those stored in a and b
                    a = a * self.game.block_size
                    b = b * self.game.block_size
                    self.set_coordinates(a, b)

    def set_coordinates(self, x, y):
        self.rect = self.image_holder.get_rect(center = (x, y))
    

       


        

    def render(self, display):
        display.blit(self.current_image, (self.x, self.y))
        