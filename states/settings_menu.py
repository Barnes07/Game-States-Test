import os
import pygame
from states.state import State


class SettingsMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.settings_image = pygame.image.load(os.path.join(self.game.assets_dir, "map/menus", "settings_background.png"))
        self.settings_image = pygame.transform.scale_by(self.settings_image, 0.48)
        self.settings_image_rect = self.settings_image .get_rect(center = (self.game.SCREEN_WIDTH//2, (self.game.SCREEN_HEIGHT//2)+300))

        self.back_button = self.game.text(self.game.screen, (125), (self.game.SCREEN_HEIGHT)-75, 215, 100, "Back", "white", "black")
        self.back_button_rect = pygame.Rect((125), (self.game.SCREEN_HEIGHT)-75, 215, 100)
        self.back_button_rect.center = ((125), (self.game.SCREEN_HEIGHT)-75)

        self.click_sound = pygame.mixer.Sound(os.path.join(self.game.assets_dir, "audio", "mouse_click_sound.wav"))

        self.menu_options = {0: "none",1: "main"}
        self.index = 0

       #artifact number settings
        self.artifacts_10_rect = pygame.Rect((self.game.SCREEN_WIDTH//2) - 150, (self.game.SCREEN_HEIGHT)-500, 100, 100)
        self.artifacts_10_rect.center = ((self.game.SCREEN_WIDTH//2) - 150, (self.game.SCREEN_HEIGHT)-500)
        self.artifacts_15_rect = pygame.Rect((self.game.SCREEN_WIDTH//2) - 50, (self.game.SCREEN_HEIGHT)-500, 100, 100)
        self.artifacts_15_rect.center = ((self.game.SCREEN_WIDTH//2) - 50, (self.game.SCREEN_HEIGHT)-500)
        self.artifacts_20_rect = pygame.Rect((self.game.SCREEN_WIDTH//2) + 50, (self.game.SCREEN_HEIGHT)-500, 100, 100)
        self.artifacts_20_rect.center = ((self.game.SCREEN_WIDTH//2) + 50, (self.game.SCREEN_HEIGHT)-500)
        self.artifacts_25_rect = pygame.Rect((self.game.SCREEN_WIDTH//2) + 150, (self.game.SCREEN_HEIGHT)-500, 100, 100)
        self.artifacts_25_rect.center = ((self.game.SCREEN_WIDTH//2) + 150, (self.game.SCREEN_HEIGHT)-500)

        #AI difficulty settings
        self.difficulty_easy_rect = pygame.Rect((self.game.SCREEN_WIDTH//2) - 150, (self.game.SCREEN_HEIGHT)-350, 100, 100)
        self.difficulty_easy_rect.center = ((self.game.SCREEN_WIDTH//2) - 150, (self.game.SCREEN_HEIGHT)-350)
        self.difficulty_medium_rect = pygame.Rect((self.game.SCREEN_WIDTH//2) - 50, (self.game.SCREEN_HEIGHT)-350, 100, 100)
        self.difficulty_medium_rect.center = ((self.game.SCREEN_WIDTH//2) - 50, (self.game.SCREEN_HEIGHT)-350)
        self.difficulty_hard_rect = pygame.Rect((self.game.SCREEN_WIDTH//2) + 50, (self.game.SCREEN_HEIGHT)-350, 100, 100)
        self.difficulty_hard_rect.center = ((self.game.SCREEN_WIDTH//2) + 50, (self.game.SCREEN_HEIGHT)-350)

        #Map size settings
        self.map_small_rect = pygame.Rect((self.game.SCREEN_WIDTH//2) - 150, (self.game.SCREEN_HEIGHT)-200, 100, 100)
        self.map_small_rect.center = ((self.game.SCREEN_WIDTH//2) - 150, (self.game.SCREEN_HEIGHT)-200)
        self.map_medium_rect = pygame.Rect((self.game.SCREEN_WIDTH//2) - 50, (self.game.SCREEN_HEIGHT)-200, 100, 100)
        self.map_medium_rect.center = ((self.game.SCREEN_WIDTH//2) - 50, (self.game.SCREEN_HEIGHT)-200)
        self.map_large_rect = pygame.Rect((self.game.SCREEN_WIDTH//2) + 50, (self.game.SCREEN_HEIGHT)-200, 100, 100)
        self.map_large_rect.center = ((self.game.SCREEN_WIDTH//2) + 50, (self.game.SCREEN_HEIGHT)-200)



        
    
        

    def check_clicks(self,actions):
        if actions["click"]:
            #checking which button the mouse is colliding with when clicked
            if self.back_button_rect.collidepoint(actions["mouse_pos"]):
                self.index = 1
                self.click_sound.play()
            
            elif self.artifacts_10_rect.collidepoint(actions["mouse_pos"]):
                self.click_sound.play()
                self.game.number_of_artifacts = 10

            elif self.artifacts_15_rect.collidepoint(actions["mouse_pos"]):
                self.click_sound.play()
                self.game.number_of_artifacts = 15

            elif self.artifacts_20_rect.collidepoint(actions["mouse_pos"]):
                self.click_sound.play()
                self.game.number_of_artifacts = 20

            elif self.artifacts_25_rect.collidepoint(actions["mouse_pos"]):
                self.click_sound.play()
                self.game.number_of_artifacts = 25
                
            elif self.difficulty_easy_rect.collidepoint(actions["mouse_pos"]):
                self.click_sound.play()
                self.game.bandit_difficulty = 0
            
            elif self.difficulty_medium_rect.collidepoint(actions["mouse_pos"]):
                self.click_sound.play()
                self.game.bandit_difficulty = 1

            elif self.difficulty_hard_rect.collidepoint(actions["mouse_pos"]):
                self.click_sound.play()
                self.game.bandit_difficulty = 2
            
            elif self.map_small_rect.collidepoint(actions["mouse_pos"]):
                self.click_sound.play()
                self.game.map_size = 40
            
            elif self.map_medium_rect.collidepoint(actions["mouse_pos"]):
                self.click_sound.play()
                self.game.map_size = 50
            
            elif self.map_large_rect.collidepoint(actions["mouse_pos"]):
                self.click_sound.play()
                self.game.map_size = 60


                
            
    def transition_state(self):
        if self.menu_options[self.index] == "main":
            self.exit_state()
        

    def update(self, delta_time, actions):
        self.check_clicks(actions)
        self.transition_state()


    def render(self, display):
        display.blit(self.settings_image, self.settings_image_rect)
        self.game.text(self.game.screen, (125), (self.game.SCREEN_HEIGHT)-75, 215, 100, "Back", "white", "black")
        self.test_text = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH)//2, (self.game.SCREEN_HEIGHT)-700, 210, 100, "Settings Menu", "white", "black")

        self.number_of_artifacts_box = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH//2) - 300, (self.game.SCREEN_HEIGHT)-500, 200, 100, "Artifacts:", "white", "black")
        self.artifacts_10 = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH//2) - 150, (self.game.SCREEN_HEIGHT)-500, 100, 100, "10", "white", "black")
        self.artifacts_15 = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH)//2 - 50, (self.game.SCREEN_HEIGHT)-500, 100, 100, "15", "white", "black")
        self.artifacts_20 = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH)//2 + 50, (self.game.SCREEN_HEIGHT)-500, 100, 100, "20", "white", "black")
        self.artifacts_25 = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH)//2 + 150, (self.game.SCREEN_HEIGHT)-500, 100, 100, "25", "white", "black")

        self.number_of_artifacts_box = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH//2) - 300, (self.game.SCREEN_HEIGHT)-350, 200, 100, "Difficulty:", "white", "black")
        self.difficulty_easy = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH//2) - 150, (self.game.SCREEN_HEIGHT)-350, 100, 100, "Easy", "white", "black")
        self.difficulty_medium = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH//2) - 50, (self.game.SCREEN_HEIGHT)-350, 100, 100, "Medium", "white", "black")
        self.difficulty_hard = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH//2) + 50, (self.game.SCREEN_HEIGHT)-350, 100, 100, "Hard", "white", "black")

        self.map_size_box =self.game.text(self.game.screen, (self.game.SCREEN_WIDTH//2) - 300, (self.game.SCREEN_HEIGHT)-200, 200, 100, "Map Size:", "white", "black")
        self.map_small = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH//2) - 150, (self.game.SCREEN_HEIGHT)-200, 100, 100, "Small", "white", "black")
        self.map_medium = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH//2) - 50, (self.game.SCREEN_HEIGHT)-200, 100, 100, "Medium", "white", "black")
        self.map_large = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH//2) + 50, (self.game.SCREEN_HEIGHT)-200, 100, 100, "Large", "white", "black")

        