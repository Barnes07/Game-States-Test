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
        self.main_menu_button_rect.center = (125, (self.game.SCREEN_HEIGHT)-75)
        self.click_sound = pygame.mixer.Sound(os.path.join(self.game.assets_dir, "audio", "mouse_click_sound.wav")) #sound for mouse click

        self.username_box_rect = pygame.Rect((self.game.SCREEN_WIDTH/2 - 50), ((self.game.SCREEN_HEIGHT)/2 +200), 215, 100) #rectangle of menu button for collision
        self.username_box_rect.center = (self.game.SCREEN_WIDTH/2 - 50, (self.game.SCREEN_HEIGHT)/2 + 200)


        self.menu_options = {0:"none", 1:"main_menu"} #dictionary of menu options
        self.index = 0 #index for menu_options dictionary 

        self.time_secs = time_secs
        self.time_mins = time_mins

        self.game.number_of_levels_completed = 0

        self.final_score = str(self.calculate_final_score())

        self.username = ""
        self.final_username = ""
        self.username_saved = False
        self.score_saved = False
        self.save_button_colour = "red"
        self.time_since_last_key = 0

        self.save_button_rect = pygame.Rect((self.game.SCREEN_WIDTH/2) + 120, (self.game.SCREEN_HEIGHT)/2 + 200, 100, 100)
        self.save_button_rect.center = (self.game.SCREEN_WIDTH/2 + 120, self.game.SCREEN_HEIGHT/2 + 200)


    def check_clicks(self, actions):
        if actions["click"]: #if mouse has been clicked 
            if self.main_menu_button_rect.collidepoint(actions["mouse_pos"]): #if the mouse is colliding with text box
                self.index = 1 #sets the index to point to "main_menu"
                self.click_sound.play() #plays click sound
            if self.save_button_rect.collidepoint(actions["mouse_pos"]): #if save button is pressed
                self.save_username()


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

        score = (self.game.number_of_artifacts * self.game.number_of_total_levels * time_factor)*100 - (self.time_secs + self.time_mins * 60)
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
 
    def get_username(self, delta_time):
        self.time_since_last_key += delta_time
        if self.time_since_last_key > 0.1:
            self.time_since_last_key = 0
            keys = pygame.key.get_pressed()
            if len(self.username) < 3:
                if keys[pygame.K_a]:
                    self.username += "A"
                if keys[pygame.K_b]:
                    self.username += "B"
                if keys[pygame.K_c]:
                    self.username += "C"
                if keys[pygame.K_d]:
                    self.username += "D"
                if keys[pygame.K_e]:
                    self.username += "E"
                if keys[pygame.K_f]:
                    self.username += "F"
                if keys[pygame.K_g]:
                    self.username += "G"
                if keys[pygame.K_h]:
                    self.username += "H"
                if keys[pygame.K_i]:
                    self.username += "I"
                if keys[pygame.K_j]:
                    self.username += "J"
                if keys[pygame.K_k]:
                    self.username += "K"
                if keys[pygame.K_l]:
                    self.username += "L"
                if keys[pygame.K_m]:
                    self.username += "M"
                if keys[pygame.K_n]:
                    self.username += "N"
                if keys[pygame.K_o]:
                    self.username += "O"
                if keys[pygame.K_p]:
                    self.username += "P"
                if keys[pygame.K_q]:
                    self.username += "Q"
                if keys[pygame.K_r]:
                    self.username += "R"
                if keys[pygame.K_s]:
                    self.username += "S"
                if keys[pygame.K_t]:
                    self.username += "T"
                if keys[pygame.K_u]:
                    self.username += "U"
                if keys[pygame.K_v]:
                    self.username += "V"
                if keys[pygame.K_w]:
                    self.username += "W"
                if keys[pygame.K_x]:
                    self.username += "X"
                if keys[pygame.K_y]:
                    self.username += "Y"
                if keys[pygame.K_z]:
                    self.username += "Z"
            if keys[pygame.K_BACKSPACE]:
                self.username = self.username[0:-1]
    
    def save_username(self):
        if len(self.username) > 0:
            self.final_username = self.username
            self.username_saved = True 
            self.save_button_colour = "green"

    def update(self, delta_time, actions):
        self.check_clicks(actions)
        self.transition_state()

        self.get_username(delta_time)

        
        if self.username_saved == True:
            if self.score_saved == False:
                self.update_csv(self.final_username, self.final_score)
                self.username_saved = False
                self.score_saved = True

    def render(self, display):
        display.blit(self.background_image, self.background_image_rect)
        self.main_menu_button = self.game.text(self.game.screen, self.main_menu_button_rect.centerx, self.main_menu_button_rect.centery, 215, 100, "Main Menu", "white", "black") #render "Main Menu" text 
        self.username_box = self.game.text(self.game.screen, self.username_box_rect.centerx, self.username_box_rect.centery, 215, 100, self.username, "white", "black")
        self.save_button = self.game.text(self.game.screen, self.save_button_rect.centerx, self.save_button_rect.centery, 100, 100, "save", self.save_button_colour, "black")
        self.game.text(display, (self.game.SCREEN_WIDTH)/2, 200, 300, 100, "Congratulations", "white", "black") #render "Game Over" text 
        self.game.text(display, (self.game.SCREEN_WIDTH)/2, (self.game.SCREEN_HEIGHT)/2, 300, 100, "Score: " + self.final_score, "white", "black") #render score text 
        self.game.text(display, (self.game.SCREEN_WIDTH)/2 -200, (self.game.SCREEN_HEIGHT)/2 + 200, 215, 100, "Username:", "white", "black")

