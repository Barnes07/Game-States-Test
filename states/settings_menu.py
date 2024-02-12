import os
import pygame
from states.state import State


class SettingsMenu(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self,game)
        self.settings_image = pygame.image.load(os.path.join(self.game.assets_dir, "map/menus", "settings_background.png"))
        self.settings_image = pygame.transform.scale_by(self.settings_image, 0.48)
        self.settings_image_rect = self.settings_image .get_rect(center = (self.game.SCREEN_WIDTH//2, (self.game.SCREEN_HEIGHT//2)+300))

        self.back_button = self.game.text(self.game.screen, (125), (self.game.SCREEN_HEIGHT)-75, 215, 100, "Back", "white", "black")
        self.back_button_rect = pygame.Rect((125), (self.game.SCREEN_HEIGHT)-75, 215, 100)
        self.back_button_rect.center = ((125), (self.game.SCREEN_HEIGHT)-75)

        self.click_sound = pygame.mixer.Sound(os.path.join(self.game.assets_dir, "audio", "mouse_click_sound.wav"))

        self.menu_options = {0: "none",1: "main"}
        self.index = 0

        

    def check_clicks(self,actions):
        if actions["click"]:
            #checking which button the mouse is colliding with when clicked
            if self.back_button_rect.collidepoint(actions["mouse_pos"]):
                self.index = 1
                self.click_sound.play()
                
            
    def transition_state(self):
        if self.menu_options[self.index] == "main":
            self.exit_state()
        

    def update(self, delta_time, actions):
        self.check_clicks(actions)
        self.transition_state()

    def render(self, display):
        display.blit(self.settings_image, self.settings_image_rect)
        self.game.text(self.game.screen, (125), (self.game.SCREEN_HEIGHT)-75, 215, 100, "Back", "white", "black")
        self.test_text = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH)//2, (self.game.SCREEN_HEIGHT)//2, 210, 100, "Settings Menu", "white", "black")

        