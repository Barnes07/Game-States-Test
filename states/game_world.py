import pygame
import os
from states.state import State
from states.pause_menu import PauseMenu
from sprites.player import Player
from sprites.camera_group import CameraGroup
from map_generation.cellular_automata import CellularAutomata

class Game_World(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.grass_image = pygame.image.load(os.path.join(self.game.assets_dir, "map", "grass.png"))
        self.wall_image = pygame.image.load(os.path.join(self.game.assets_dir, "map", "wall.png"))
        self.camera_group = CameraGroup(self.game)
        self.player = Player(self.game, self.camera_group)
        


        #Jungle Map
        

    def update(self, delta_time, actions):
        if actions["escape"]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()
        self.player.update(delta_time, actions)
        
    
    def render(self, display):
        display.fill("black")
        display.blit(self.grass_image, (0,0))
        #self.player.render(display) old line of code which allows the player to move freely (not centred on screen)
        self.camera_group.render(display, self.player)

