import pygame
import os
from states.state import State
import csv
from datetime import date

class Game_Complete(State):
    def __init__(self, game, time_secs, time_mins):
        super().__init__(game)
        self.game = game

        self.background_image = pygame.image.load(os.path.join(self.game.assets_dir, "map/menus", "leaderboard_background.png"))
        self.background_image = pygame.transform.scale_by(self.background_image, 0.48)
        self.background_image_rect = self.background_image .get_rect(center = (self.game.SCREEN_WIDTH//2, (self.game.SCREEN_HEIGHT//2)+300))

        self.main_menu_button_rect = pygame.Rect((125), (self.game.SCREEN_HEIGHT)-75, 215, 100) #rectangle of menu button for collision
        self.main_menu_button_rect.center = 125, (self.game.SCREEN_HEIGHT)-75
        self.click_sound = pygame.mixer.Sound(os.path.join(self.game.assets_dir, "audio", "mouse_click_sound.wav")) #sound for mouse click

        self.menu_options = {0:"none", 1:"main_menu"} #dictionary of menu options
        self.index = 0 #index for menu_options dictionary 

        self.time_secs = time_secs
        self.time_mins = time_mins

        self.game.number_of_levels_completed = 0

        self.final_score = str(self.calculate_final_score())

        self.update_csv("BG", self.final_score)


    def check_clicks(self, actions):
        if actions["click"]: #if mouse has been clicked 
            if self.main_menu_button_rect.collidepoint(actions["mouse_pos"]): #if the mouse is colliding with text box
                self.index = 1 #sets the index to point to "main_menu"
                self.click_sound.play() #plays click sound

    def transition_state(self):
         if self.menu_options[self.index] == "main_menu": #if the index points to "main_menu"
            while len(self.game.states_stack) > 1:
                self.game.states_stack.pop()

    def calculate_final_score(self):
        if self.time_mins < 1:
            time_factor = 100
        elif self.time_mins < 2:
            time_factor = 90
        elif self.time_mins < 3:
            time_factor = 80
        elif self.time_mins < 4:
            time_factor = 70
        elif self.time_mins < 5:
            time_factor = 60
        else:
            time_factor = 50

        score = (self.game.number_of_artifacts * self.game.number_of_total_levels * time_factor) - (self.time_secs + self.time_mins * 60)
        return(score)

    def update_csv(self, name, score):  
        scores = []
        current_date = ""
        with open(self.game.leaderboard) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                scores.append(row)
        
        if len(scores) < 5:
            current_date = str(date.today())
            scores.append([name, current_date, score])
        else:
            lowest_score_index = -1
            lowest_score = float("inf")
            for count in range (0, len(scores)):
                if int(score) >= int(scores[count][2]) and int(scores[count][2]) <= lowest_score:
                    lowest_score_index = count
                    lowest_score = int(scores[count][2])
            if lowest_score_index > -1:
                current_date = str(date.today())
                scores[lowest_score_index] = (name, current_date, score)
        
        with open(self.game.leaderboard, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(scores)
    


        
    def update(self, delta_time, actions):
        self.check_clicks(actions)
        self.transition_state()

    def render(self, display):
        display.blit(self.background_image, self.background_image_rect)
        self.main_menu_button = self.game.text(self.game.screen, self.main_menu_button_rect.centerx, self.main_menu_button_rect.centery, 215, 100, "Main Menu", "white", "black") #render "Main Menu" text 
        self.game.text(display, (self.game.SCREEN_WIDTH)/2, 200, 300, 100, "Congratulations", "white", "black") #render "Game Over" text 
        self.game.text(display, (self.game.SCREEN_WIDTH)/2, (self.game.SCREEN_HEIGHT)/2, 300, 100, "Score: " + self.final_score, "white", "black") #render score text 


        