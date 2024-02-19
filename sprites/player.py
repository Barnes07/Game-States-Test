import os
import time
import pygame 
import math
from sprites.wall import Wall

class Player(pygame.sprite.Sprite):

    def __init__(self, game, group):
        super().__init__(group)
        self.game = game 
        self.sprite_dir = os.path.join(self.game.sprite_dir, "player")
        self.x = 64
        self.y = 256
        self.image_holder = pygame.image.load(os.path.join(self.sprite_dir, "player_down1.png")) #A placeholder of the player image so that a rectangle can be created. 
        self.rect = self.image_holder.get_rect(center = (self.x, self.y))
        self.group = group
        self.speed = 500
        self.direction = pygame.math.Vector2()
        self.load_sprites()
        self.current_frame = 0
        self.time_since_last_frame = 0

        self.actual_pos = (self.rect.centerx//self.game.block_size, self.rect.centery//self.game.block_size)
    
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
            Check = isinstance(sprite, Wall)      #"isinstance" is a function that returns a boolean value depending on whether the firsts parameter is of the class type mentioned in the second parameter
            if Check == True:
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

    def set_coordinates(self, x, y):
        self.rect = self.image_holder.get_rect(center = (x, y))

       


        

    def render(self, display):
        display.blit(self.current_image, (self.x, self.y))
        pass