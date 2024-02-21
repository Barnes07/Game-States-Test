import pygame
import os
from states.state import State
from states.pause_menu import PauseMenu
from sprites.player import Player
from sprites.bandit import Bandit
from sprites.artifact import Artifact
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

        self.bandit = Bandit(self.game, self.camera_group, self.actual_map_width, self.actual_map_height, self)
        self.artifact = Artifact(self.game, self, self.camera_group)

        self.player = Player(self.game, self.camera_group, self)#Player must always be the last sprite to be added to the camera group. Otherwise it will be rendered underneath the other sprites and will not be seen by the user. This was encountered during testing.
        
        self.player.find_start_coordinates(self.map.final_map)
        self.bandit.find_start_coordinates(self.map.final_map)
        self.artifact.find_start_coordiantes(self.map.final_map)

        self.time_since_start = 0


    #def time(self, delta_time):
    #self.time_since_start += delta_time
    #self.time_since_start = round(self.time_since_start)

                
    def update(self, delta_time, actions):
        if actions["escape"]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()
        self.player.update(delta_time, actions)
        self.bandit.update(delta_time)

        if self.artifact.alive():
            self.artifact.update()


        
    def render(self, display):
        display.fill("black")
        self.camera_group.render(display, self.player)

        #self.score_text = self.game.text(display, (self.game.SCREEN_WIDTH - 125), (self.game.SCREEN_HEIGHT) - 600, 200, 100, self.time_since_start, "white", "black")
        
