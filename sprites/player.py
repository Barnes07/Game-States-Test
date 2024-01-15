import os
import time
import pygame 

class Player():

    def __init__(self, game):
        self.game = game 
        self.load_sprites()
        self.x = 64
        self.y = 256
        self.current_frame = 0
        self.previous_frame_update = 0
    
    def update(self, delta_time, actions):
        #Get direction
        direction_x = actions["right"] - actions["left"]
        direction_y = actions["down"] - actions["up"]
        #Update location
        self.x += 100 * delta_time *direction_x
        self.y += 100 * delta_time *direction_y
        #Animate the player
        self.animate(delta_time, direction_x, direction_y)

    def render(self, display):
        display.blit(self.current_image, (self.x, self.y)) 

    def animate(self, delta_time, x_direction, y_direction):
        #Calculate elapsed time since last frame 
        self.previous_frame_update += delta_time
        #if no direction entered, set animation to idle
        if not (x_direction or y_direction):
            self.current_image = self.current_animation_list[0]
            return
        #if direction is pressed, use the correct sequnece of frames
        if x_direction:
            if x_direction > 0:
                self.current_animation_list = self.right_sprites
            else:
                self.current_animation_list = self.left_sprites
        if y_direction:
            if y_direction > 0:
                self.current_animation_list = self.down_sprites
            else:
                self.current_animation_list = self.up_sprites
        #Advance the animation if enough time has passed
        if self.previous_frame_update > 0.15:
            self.previous_frame_update = 0
            self.current_frame = (self.current_frame + 1) % len(self.current_animation_list)
            self.current_image = self.current_animation_list[self.current_frame]

    def load_sprites(self):
        #Load directory with player sprites
        self.sprite_dir = os.path.join(self.game.sprite_dir, "player")
        self.down_sprites = []
        self.up_sprites = []
        self.left_sprites =[]
        self.right_sprites = []
        #load frames for each direction
        for count in range (1,5):
            self.down_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_down" + str(count) + ".png")))
            self.up_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_up" + str(count) + ".png")))
            self.left_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_left" + str(count) + ".png")))
            self.right_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_right" + str(count) + ".png")))
        #Set the default frames for when idle
        self.current_image = self.up_sprites[0]
        self.current_animation_list = self.up_sprites


        
