import pygame
import os
from states.state import State
from states.pause_menu import PauseMenu
from states.game_over import Game_Over
from sprites.player import Player
from sprites.bandit import Bandit
from sprites.artifact import Artifact
from sprites.exit_door import Exit_Door
from sprites.camera_group import CameraGroup
from map_generation.cellular_automata import Cellular_Automata

from sprites.floor import Floor
from sprites.wall import Wall

class Game_World(State):
    def __init__(self, game):
        super().__init__(game)
        self.camera_group = CameraGroup(self.game)

        #Jungle Map
        #Potential isometric implementation https://www.youtube.com/watch?v=gE2gTCwLdFM
        self.actual_map_width = 50
        self.actual_map_height = 50
        self.map = Cellular_Automata(self.actual_map_width ,self.actual_map_height ,61 , 4, 4, self.camera_group, self.game)
        self.map.update()

        #self.instantiate_artifacts()
        self.bandit = Bandit(self.game, self.camera_group, self.actual_map_width, self.actual_map_height, self)
        
        self.exit_door = Exit_Door(self.game, self, self.camera_group)

        self.player = Player(self.game, self.camera_group, self)#Player must always be the last sprite to be added to the camera group. Otherwise it will be rendered underneath the other sprites and will not be seen by the user. This was encountered during testing.
        

            
        self.player.find_start_coordinates(self.map.final_map)
        self.bandit.find_start_coordinates(self.map.final_map)
        self.exit_door.get_random_starting_coordinates(self.map.final_map)

    
        self.time_since_start = 0

        self.filled_height = 0
        self.loot_bag_rect = pygame.Rect(self.game.SCREEN_WIDTH - 75, 25, 50, 100)
        self.fill_per_artifact = self.loot_bag_rect.height/self.game.number_of_artifacts
        self.filled_loot_bag_rect = pygame.Rect(self.game.SCREEN_WIDTH - 75, 25, 50, self.filled_height)
        


 


    #def time(self, delta_time):
    #self.time_since_start += delta_time
    #self.time_since_start = round(self.time_since_start)
        
    def instantiate_artifacts(self):
        for artifact in range (0,self.game.number_of_artifacts):
            artifact = Artifact(self.game, self, self.camera_group)
            artifact.find_start_coordiantes(self.map.final_map)

    def draw_loot_bag(self):
        self.loot_bag = pygame.draw.rect(self.game.screen, "grey", self.loot_bag_rect) #background, grey part of loot bag
        self.filled_loot_bag_rect = pygame.Rect(self.game.SCREEN_WIDTH - 75, self.loot_bag_rect.bottom - self.filled_height, 50, self.filled_height) #updates dimensions of "filled" rectangle
        self.filled_loot_bag = pygame.draw.rect(self.game.screen, "yellow", self.filled_loot_bag_rect) #draws updated "filled" rectangle 

    def check_game_over(self):
        if self.bandit.check_player_collision(self.player):
            new_state = Game_Over(self.game)
            new_state.enter_state()


                
    def update(self, delta_time, actions):
        if actions["escape"]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()
        self.player.update(delta_time, actions)
        self.bandit.update(delta_time)

        
        self.exit_door.check_collision(self.player, delta_time) #must be called before camera group update so that player direction is correctly set beofore it updates
        self.exit_door.check_door_proximity(self.player)

        self.camera_group.update(delta_time, actions)



        self.check_game_over()

        

        


        
    def render(self, display):
        display.fill("black")
        self.camera_group.render(display, self.player)
        self.draw_loot_bag()



        #self.score_text = self.game.text(display, (self.game.SCREEN_WIDTH - 125), (self.game.SCREEN_HEIGHT) - 600, 200, 100, self.time_since_start, "white", "black")
        

