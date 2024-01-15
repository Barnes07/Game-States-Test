import pygame
import os
from states.state import State
from states.pause_menu import PauseMenu
from sprites.player import Player
from map_generation.cellular_automata import CellularAutomata

class Game_World(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.grass_image = pygame.image.load(os.path.join(self.game.assets_dir, "map", "grass.png"))
        self.wall_image = pygame.image.load(os.path.join(self.game.assets_dir, "map", "wall.png"))
        self.player = Player(self.game)

        #Jungle Map
        

    def update(self, delta_time, actions):
        if actions["escape"]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()
        self.player.update(delta_time, actions)
    
    def render(self, display):
        display.fill("white")
        display.blit(self.grass_image, (0,0))
        self.player.render(display)

