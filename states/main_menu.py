import pygame
import os
from states.state import State #Imports the state superclass
from states.game_world import Game_World
from states.settings_menu import SettingsMenu
from states.leaderboard_menu import LeaderboardMenu

class Main_Menu(State):
    def __init__(self, game):
        super().__init__(game)
        #Setting the menu
        self.menu_image = pygame.image.load(os.path.join(self.game.assets_dir, "map/menus", "main_menu.png"))
        self.menu_image = pygame.transform.scale_by(self.menu_image, 0.48)
        self.menu_rect = self.menu_image.get_rect(center = (self.game.SCREEN_WIDTH//2, (self.game.SCREEN_HEIGHT//2)+50))
        self.menu_options = {0: "none",1: "Play", 2: "Settings", 3: "Leaderboard"}
        self.index = 0

        self.play_button = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-75, 215, 100, "Play game", "white", "black")
        self.play_button_rect = pygame.Rect((self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-75, 215, 100)
        #self.play_button_rect is initialised using left and top coordinates. However, to ensure that the rectangle is alligned with the text box, 
        #a self.play_button_rect.center variable is defined so that the rectangle is perfectly alligned with the text box for perfect collsions with the mouse for when the player whishes to select an option
        self.play_button_rect.center = ((self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-75)

        self.settings_button = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-185, 215, 100, "Settings", "white", "black")
        self.settings_button_rect = pygame.Rect((self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-185, 215, 100)
        self.settings_button_rect.center = ((self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-185)

        self.leaderboard_button = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-295, 215, 100, "Leaderboard", "white", "black")
        self.leaderboard_button_rect = pygame.Rect((self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-295, 215, 100)
        self.leaderboard_button_rect.center = ((self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-295)
        
        self.click_sound = pygame.mixer.Sound(os.path.join(self.game.assets_dir, "audio", "mouse_click_sound.wav"))
        self.background_music = pygame.mixer.music.load(os.path.join(self.game.assets_dir, "audio", "main_menu_background.wav"))

    def transition_state(self):
        if self.menu_options[self.index] == "Play":
            new_state = Game_World(self.game, 0, 0)
            new_state.enter_state() #Adds new state to top of the stack
            self.index = 0
        elif self.menu_options[self.index] == "Settings":
            new_state = SettingsMenu(self.game)
            new_state.enter_state()
            self.index = 0 #Encourntered a problem where self.index was still equal to the settinsg menu, which resulted in the program wanting to consistently 
            #open the settings window even after the settings window was close. (remove this line to see it in action)
        elif self.menu_options[self.index] == "Leaderboard":
            new_state = LeaderboardMenu(self.game)
            new_state.enter_state()
            self.index = 0
        else:
            pass
        
    def play_music(self):
        music_busy = pygame.mixer.music.get_busy()       #Boolean value if music(not just mixer) is being played
        if music_busy == False:                          #Therefore, when the music is stopped, it is played again
            pygame.mixer.music.play()


    def check_clicks(self,actions):
        if actions["click"]:
            #checking which button the mouse is colliding with when clicked
            if self.play_button_rect.collidepoint(actions["mouse_pos"]):
                self.index = 1
                self.click_sound.play()
            if self.settings_button_rect.collidepoint(actions["mouse_pos"]):
                self.index = 2
                self.click_sound.play()
            if self.leaderboard_button_rect.collidepoint(actions["mouse_pos"]):
                self.index = 3
                self.click_sound.play()

    def update(self, delta_time, actions):
        self.check_clicks(actions)
        self.transition_state()
        self.play_music()

    def render(self, display):
        display.blit(self.menu_image, self.menu_rect)
        self.game.text(display, (self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-75, 215, 100, "Play game", "white", "black")
        self.game.text(display, (self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-185, 215, 100, "Settings", "white", "black")
        self.game.text(display, (self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-295, 215, 100, "Leaderboard", "white", "black")
        
        
