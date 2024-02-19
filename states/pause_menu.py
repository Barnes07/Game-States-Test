import os
import pygame
from states.state import State



class PauseMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.play_button = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-75, 215, 100, "Play game", "white", "black")
        self.play_button_rect = pygame.Rect((self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-75, 215, 100)
       
        self.play_button_rect.center = ((self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-75)
        
    def update(self, delta_time, actions):
        if actions["click"]:
            if self.play_button_rect.collidepoint(actions["mouse_pos"]):
                self.exit_state()

    def render(self, display):
        self.previous_state.render(display)
        self.game.text(display, (self.game.SCREEN_WIDTH)//2, 60, 215, 100, "Paused", "white", "black")
        self.game.text(display, (self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-75, 215, 100, "Play game", "white", "black")
                                                  

    
