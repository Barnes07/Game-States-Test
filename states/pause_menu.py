import os
import pygame
from states.state import State



class PauseMenu(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self,game)
        self.play_button = self.game.text(self.game.screen, (self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-75, 215, 100, "Play game", "white", "black")
        self.play_button_rect = pygame.Rect((self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-75, 215, 100)
        #self.play_button_rect is initialised using left and top coordinates. However, to ensure that the rectangle is alligned with the text box, a self.play_button_rect.center variable is defined so that the rectangle is perfectly alligned with the text box for perfect collsions with the mouse for when the player whishes to select an option
        self.play_button_rect.center = ((self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-75)
        
        

    
    

    def update(self, delta_time, actions):
        if actions["action1"]:
            self.exit_state()
     
        

    def render(self, display):
        self.previous_state.render(display)
        self.game.text(display, (self.game.SCREEN_WIDTH)//2, 60, 215, 100, "Paused", "white", "black")
        self.game.text(display, (self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-75, 215, 100, "Play game", "white", "black")
                                                  

    
