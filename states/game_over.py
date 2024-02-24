import pygame
import os
from states.state import State




class Game_Over(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game

        self.main_menu_button_rect = pygame.Rect((125), (self.game.SCREEN_HEIGHT)-75, 215, 100) #rectangle of menu button for collision
        self.main_menu_button_rect.center = 125, (self.game.SCREEN_HEIGHT)-75
        self.click_sound = pygame.mixer.Sound(os.path.join(self.game.assets_dir, "audio", "mouse_click_sound.wav")) #sound for mouse click

        self.menu_options = {0:"none", 1:"main_menu"} #dictionary of menu options
        self.index = 0 #index for menu_options dictionary 

    def check_clicks(self, actions):
        if actions["click"]: #if mouse has been clicked 
            if self.main_menu_button_rect.collidepoint(actions["mouse_pos"]): #if the mouse is colliding with text box
                self.index = 1 #sets the index to point to "main_menu"
                self.click_sound.play() #plays click sound
    
    def transition_state(self):
         if self.menu_options[self.index] == "main_menu": #if the index points to "main_menu"
            while len(self.game.states_stack) > 1:
                self.game.states_stack.pop()


    def update(self, delta_time, actions):
        self.check_clicks(actions)
        self.transition_state()


    def render(self, display):
        self.main_menu_button = self.game.text(self.game.screen, self.main_menu_button_rect.centerx, self.main_menu_button_rect.centery, 215, 100, "Main Menu", "white", "black") #render "Main Menu" text 
        self.game.text(display, (self.game.SCREEN_WIDTH)/2, 200, 215, 100, "Game Over", "white", "black") #render "Game Over" text 
        


