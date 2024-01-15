import os
import pygame
from states.state import State


class LeaderboardMenu(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self,game)
        self.leaderboard_image = pygame.image.load(os.path.join(self.game.assets_dir, "map/menus", "leaderboard_background.png"))
        self.leaderboard_image = pygame.transform.scale_by(self.leaderboard_image, 0.48)
        self.leaderboard_image_rect = self.leaderboard_image .get_rect(center = (self.game.SCREEN_WIDTH//2, (self.game.SCREEN_HEIGHT//2)+300))

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
        if actions["action1"]:
            self.exit_state()
        self.check_clicks(actions)
        self.transition_state()

    def render(self, display):
        display.blit(self.leaderboard_image, self.leaderboard_image_rect)
        self.game.text(self.game.screen, (125), (self.game.SCREEN_HEIGHT)-75, 215, 100, "Back", "white", "black")