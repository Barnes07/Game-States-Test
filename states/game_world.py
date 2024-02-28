import pygame
import os
import random
from states.state import State
from states.pause_menu import PauseMenu
from states.game_over import Game_Over
from states.game_complete import Game_Complete
from sprites.player import Player
from sprites.bandit import Bandit
from sprites.artifact import Artifact
from sprites.exit_door import Exit_Door
from sprites.camera_group import CameraGroup
from map_generation.cellular_automata import Cellular_Automata

from sprites.floor import Floor
from sprites.wall import Wall

class Game_World(State):
    def __init__(self, game, time_secs, time_mins):
        super().__init__(game)
        self.camera_group = CameraGroup(self.game)

        #Map
        self.actual_map_width = 50
        self.actual_map_height = 50
        self.wall_density = 61
        self.wall_count_variable = 4
        self.iterations = 4
        self.map = Cellular_Automata(self.actual_map_width ,self.actual_map_height, self.wall_density , self.wall_count_variable, self.iterations, self.camera_group, self.game)
        self.map.update()

        #object instantiations 
        self.instantiate_artifacts()
        self.bandit = Bandit(self.game, self.camera_group, self.actual_map_width, self.actual_map_height, self)
        self.exit_door = Exit_Door(self.game, self, self.camera_group)
        self.player = Player(self.game, self.camera_group, self)#Player must always be the last sprite to be added to the camera group. Otherwise it will be rendered underneath the other sprites and will not be seen by the user. This was encountered during testing.
        
        #finding start coordinates
        self.player.find_start_coordinates(self.map.final_map)
        self.bandit.find_start_coordinates(self.map.final_map)
        self.exit_door.get_random_starting_coordinates(self.map.final_map)

        #loot bag
        self.filled_height = 0
        self.loot_bag_rect = pygame.Rect(self.game.SCREEN_WIDTH - 75, 25, 50, 100)
        self.fill_per_artifact = self.loot_bag_rect.height/self.game.number_of_artifacts
        self.filled_loot_bag_rect = pygame.Rect(self.game.SCREEN_WIDTH - 75, 25, 50, self.filled_height)

        #Stamina bar
        self.stam_filled_width = 100
        self.stamina_rect = pygame.Rect(self.game.SCREEN_WIDTH - 125, self.game.SCREEN_HEIGHT - 50, 100, 25)
        self.filled_stamina_rect = pygame.Rect(self.game.SCREEN_WIDTH - 125, self.game.SCREEN_HEIGHT  - 50, self.stam_filled_width, 25)
        self.time_climbed = 0
        self.time_walking = 0

        #Timer
        self.time_since_last_frame = 0
        self.time_mins = time_mins
        self.time_secs = time_secs


    def instantiate_artifacts(self):
        for artifact in range (0,self.game.number_of_artifacts):
            artifact = Artifact(self.game, self, self.camera_group)
            artifact.find_start_coordiantes(self.map.final_map)

    def draw_loot_bag(self):
        self.loot_bag = pygame.draw.rect(self.game.screen, "grey", self.loot_bag_rect) #background, grey part of loot bag
        self.filled_loot_bag_rect = pygame.Rect(self.game.SCREEN_WIDTH - 75, self.loot_bag_rect.bottom - self.filled_height, 50, self.filled_height) #updates dimensions of "filled" rectangle
        self.filled_loot_bag = pygame.draw.rect(self.game.screen, "yellow", self.filled_loot_bag_rect) #draws updated "filled" rectangle 

    def draw_stamina(self):
        self.stamina_bar = pygame.draw.rect(self.game.screen, "grey", self.stamina_rect) #background, grey part of loot bag
        self.filled_stamina_rect = pygame.Rect(self.stamina_bar.left, self.game.SCREEN_HEIGHT - 50, self.stam_filled_width, 25)
        self.filled_stamina_bar = pygame.draw.rect(self.game.screen, "green", self.filled_stamina_rect) #draws updated "filled" rectangle 

    def check_game_over(self):
        if self.bandit.check_player_collision(self.player):
            new_state = Game_Over(self.game)
            new_state.enter_state()

    def check_open_door(self, actions):
        if self.exit_door.check_door_proximity(self.player):
            if actions["flute"]:
                new_state = Flute_Playing(self.game, self.time_secs, self.time_mins)
                new_state.enter_state()
                self.game.number_of_levels_completed += 1

                    
    def calculate_time(self, delta_time):
        self.time_since_last_frame += delta_time
        if self.time_since_last_frame > 1:
            self.time_since_last_frame = 0
            self.time_secs += 1
            if self.time_secs == 60:
                self.time_mins +=1
                self.time_secs = 0
        
    def check_valid_climb(self, actions, delta_time):
        if actions["start"] and self.stam_filled_width > 0: #If "enter" is pressed and player has sufficient stamina
            pass #do not check for collisions between player and walls
        else:
            self.player.check_wall_collision(delta_time) #check for collision between player and walls

    def update_stamina(self, actions, delta_time):
        if actions["start"]: #If the enter key is being pressed
            self.time_climbed += delta_time #increment time_climbed by the time elapsed since the last frame
            self.time_walking = 0 #reset time_walking attribute
            if self.time_climbed > 1: #if one second has elapsed
                self.time_climbed = 0 #reset the time_climbed attribute
                if self.stam_filled_width - 10 >= 0: 
                    self.stam_filled_width -= 10 #only decrease the stamina if it will remain greater than 0
        else:
            self.time_walking += delta_time #increment time_walking attribute by time since last frame
            self.time_climbed = 0 #reset time_climbed attribute
            if self.time_walking > 1: #if a second has elapsed
                self.time_walking = 0 #reset time_walking attribute
                if self.stam_filled_width+ 10 <= 100: 
                    self.stam_filled_width += 10 #only increase the stamina if it will remain less than 100


   
    def update(self, delta_time, actions):
        if actions["escape"]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()
        self.player.update(delta_time, actions)
        self.bandit.update(delta_time)

        self.exit_door.check_collision(self.player, delta_time) #must be called before camera group update so that player direction is correctly set beofore it updates
        self.check_open_door(actions)
        self.camera_group.update(delta_time, actions)

        self.check_game_over()

        self.calculate_time(delta_time)

        self.update_stamina(actions, delta_time)
        self.check_valid_climb(actions, delta_time)


                

            

        








  
    def render(self, display):
        display.fill("black")
        self.camera_group.render(display, self.player)
        self.draw_loot_bag()
        self.draw_stamina()

        self.game.text(display, 100, 50, 150, 50, (str(self.time_mins).zfill(2) + ": " + str(self.time_secs).zfill(2)), "white", "black")






class Flute_Playing(State):
    def __init__(self, game, time_secs, time_mins):
        super().__init__(game)
        self.game = game 
        self.flute_playing_image = pygame.image.load(os.path.join(self.game.assets_dir, "flute", "flute_playing.png"))
        self.flute_playing_image_rect = self.flute_playing_image.get_rect(center = (self.game.SCREEN_WIDTH//2, (self.game.SCREEN_HEIGHT//2)))

        self.previous_key = 0
        self.current_key = "a"
        self.generate_random_key()
        
        self.time_since_last_key = 0
        self.game_continue_flag = False
        self.keys_pressed = 0

        self.time_secs = time_secs
        self.time_mins = time_mins
        self.time_since_last_frame = 0

    def display_random_key(self, display):
        self.game.text(display, (self.game.SCREEN_WIDTH)/2, (self.game.SCREEN_HEIGHT)/2 - 200, 215, 100, self.current_key, "white", "black")

    def generate_random_key(self):
        found = False
        while found == False:
            random_letter = random.randint(1,5)
            if random_letter != self.previous_key:
                found = True
        if random_letter == 1:
            self.current_key = "a"

        elif random_letter == 2:
            self.current_key = "b"

        elif random_letter == 3:
            self.current_key = "c"

        elif random_letter == 4:
            self.current_key = "d"

        elif random_letter == 5:
            self.current_key = "e"
        
        self.previous_key = random_letter

    def check_pressed_key(self):
        keys = pygame.key.get_pressed()
        if self.current_key == "a":
            if keys[pygame.K_a]:  
                return(True)  
         
        if self.current_key == "b":
            if keys[pygame.K_b]:
                return(True)
        if self.current_key == "c":
            if keys[pygame.K_c]:
                return(True)
        if self.current_key == "d":
            if keys[pygame.K_d]:
                return(True)
        if self.current_key == "e":
            if keys[pygame.K_e]:
                return(True)
        return(False)

    def main(self, delta_time):
        if self.keys_pressed == 5:
            if self.game.number_of_levels_completed < self.game.number_of_total_levels:
                new_state = Game_World(self.game, self.time_secs, self.time_mins)
                new_state.enter_state()
            else:
                new_state = Game_Complete(self.game, self.time_secs, self.time_mins)
                new_state.enter_state()
        self.time_since_last_key += delta_time
        if self.time_since_last_key > 3:
            if self.game_continue_flag == False:
                new_state = Game_Over(self.game)
                new_state.enter_state()
            self.time_since_last_key = 0
            self.generate_random_key()
            self.game_continue_flag = False
        if self.check_pressed_key():
            self.game_continue_flag = True
            self.time_since_last_key = 4
            self.keys_pressed += 1
 

    def calculate_time(self, delta_time):
        self.time_since_last_frame += delta_time
        if self.time_since_last_frame > 1:
            self.time_since_last_frame = 0
            self.time_secs += 1
            if self.time_secs == 60:
                self.time_mins +=1
                self.time_secs = 0

    def update(self, delta_time, actions):
        self.main(delta_time)
        self.calculate_time(delta_time)

    def render(self, display):
        display.fill("black")
        display.blit(self.flute_playing_image, self.flute_playing_image_rect)
        self.display_random_key(display)

        self.game.text(display, 100, 50, 150, 50, (str(self.time_mins).zfill(2) + ": " + str(self.time_secs).zfill(2)), "white", "black")

        


