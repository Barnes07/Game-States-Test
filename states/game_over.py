import pygame
import os
from states.state import State
from states.main_menu import Main_Menu


class Game_Over(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.menu_options = {0:"none", 1:"main_menu"}

 
        self.main_menu_button_rect = pygame.Rect((125), (self.game.SCREEN_HEIGHT)-75, 215, 100)

        self.click_sound = pygame.mixer.Sound(os.path.join(self.game.assets_dir, "audio", "mouse_click_sound.wav"))

        self.index = 0

    def check_clicks(self, actions):
        if actions["click"]:
            if self.main_menu_button_rect.collidepoint(actions["mouse_pos"]):
                self.menu_options = 1
                self.click_sound.play()
    
    def transition_state(self):
         if self.menu_options[self.index] == "main_menu":
            new_state = Main_Menu(self.game)
            new_state.enter_state() #Adds new state to top of the stack

        

    def update(self, delta_time, actions):
        pass


    def render(self, display):
        self.main_menu_button = self.game.text(self.game.screen, self.main_menu_button_rect.x, self.main_menu_button_rect.y, 215, 100, "Main Menu", "white", "black")
        self.game.text(display, (self.game.SCREEN_WIDTH)/2, 200, 215, 100, "Game Over", "white", "black")
        self.check_clicks()
        self.transition_state()

