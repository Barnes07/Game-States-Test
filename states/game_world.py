import pygame
import os
from states.state import State
from states.pause_menu import PauseMenu
from sprites.player import Player
from sprites.bandit import Bandit
from sprites.camera_group import CameraGroup
from map_generation.cellular_automata import Cellular_Automata

from sprites.floor import Floor
from sprites.wall import Wall

class Game_World(State):
    def __init__(self, game):
        super().__init__(game)
        self.camera_group = CameraGroup(self.game)
        self.player = Player(self.game, self.camera_group)

        
        #Jungle Map
        #Potential isometric implementation https://www.youtube.com/watch?v=gE2gTCwLdFM
        
        #self.jungle_map_height = self.game.SCREEN_WIDTH * 3
        #self.jungle_map_width = self.game.SCREEN_WIDTH * 3
        #self.jungle_actual_map_height = self.jungle_map_height//self.game.block_size
        #self.jungle_actual_map_width = self.jungle_map_width//self.game.block_size
        #self.jungle_iterations = 10
        #self.jungle_wall_density = 48
        #self.jungle_wall_count_variable = 3
        #self.jungle_map = CellularAutomata(self.jungle_map_height, self.jungle_map_width, self.jungle_actual_map_height, self.jungle_actual_map_width, self.jungle_iterations, self.jungle_wall_density, self.jungle_wall_count_variable, self.camera_group, self.game)
        #self.jungle_map = self.jungle_map.Generate_CA_Map()
        #print(self.jungle_map)

        self.actual_map_width = 50
        self.actual_map_height = 50
        self.map = Cellular_Automata(self.actual_map_width ,self.actual_map_height ,61 , 4, 4, self.camera_group, self.game)
        self.map.update()
        self.enemy = Bandit(self.game, self.camera_group, self.actual_map_width, self.actual_map_height, self)
        self.player = Player(self.game, self.camera_group)#Player must always be the last sprite to be added to the camera group. Otherwise it will be rendered underneath the other sprites and will not be seen by the user. This was encountered during testing.
        self.start_coordinates = self.map.find_player_starting_coordinates(self.map.final_map)
        self.player.set_coordinates(self.start_coordinates[0], self.start_coordinates[1])
        

    def update(self, delta_time, actions):
        if actions["escape"]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()
        self.player.update(delta_time, actions)
        path = self.enemy.pathfind(self.player, (self.player.rect.centerx//self.game.block_size, self.player.rect.centery//self.game.block_size), self.map.final_map)
        print(path)



        
        
    
    def render(self, display):
        display.fill("black")
        self.camera_group.render(display, self.player)
        #self.player.render(display) #old line of code which allows the player to move freely (not centred on screen)

