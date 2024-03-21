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

        self.no_button_rect = pygame.Rect(((self.game.SCREEN_WIDTH)//2) - 200, ((self.game.SCREEN_HEIGHT)//2) + 150, 215, 100)
        self.no_button_rect.center = ((self.game.SCREEN_WIDTH)//2) - 200, ((self.game.SCREEN_HEIGHT)//2) + 150
        self.yes_button_rect = pygame.Rect(((self.game.SCREEN_WIDTH)//2) + 200, ((self.game.SCREEN_HEIGHT)//2) + 150, 215, 100)
        self.yes_button_rect.center = ((self.game.SCREEN_WIDTH)//2) + 200, ((self.game.SCREEN_HEIGHT)//2) + 150

        self.main_menu_button_rect = pygame.Rect((125), (self.game.SCREEN_HEIGHT)-75, 215, 100) #rectangle of menu button for collision
        self.main_menu_button_rect.center = (125, (self.game.SCREEN_HEIGHT)-75)
        

        self.exit_to_menu = False
        
    def update(self, delta_time, actions):
        if actions["click"]:
            if self.play_button_rect.collidepoint(actions["mouse_pos"]):
                self.exit_state()
            
            if self.main_menu_button_rect.collidepoint(actions["mouse_pos"]):
                self.exit_to_menu = True
            
            if self.exit_to_menu == True:
                if self.yes_button_rect.collidepoint(actions["mouse_pos"]):
                    while len(self.game.states_stack) > 1:
                        self.game.states_stack.pop()
                elif self.no_button_rect.collidepoint(actions["mouse_pos"]):
                    self.exit_to_menu = False 

    def exit(self, display):
        self.previous_state.render(display)
        self.game.text(display, (self.game.SCREEN_WIDTH)//2, 60, 215, 100, "Paused", "white", "black")
        self.game.text(display, (self.game.SCREEN_WIDTH)//2, (self.game.SCREEN_HEIGHT)//2, 800, 100, "Are you sure you want to return to the main menu?", "white", "black")
        self.game.text(display, ((self.game.SCREEN_WIDTH)//2) - 200, ((self.game.SCREEN_HEIGHT)//2) + 150, 215, 100, "No", "white", "black")
        self.game.text(display, ((self.game.SCREEN_WIDTH)//2) + 200, ((self.game.SCREEN_HEIGHT)//2) + 150, 215, 100, "Yes", "white", "black")
        

          
    
    def pause(self, display):
        self.previous_state.render(display)
        self.game.text(display, (self.game.SCREEN_WIDTH)//2, 60, 215, 100, "Paused", "white", "black")
        self.game.text(display, (self.game.SCREEN_WIDTH)-125, (self.game.SCREEN_HEIGHT)-75, 215, 100, "Play game", "white", "black")
        self.main_menu_button = self.game.text(self.game.screen, self.main_menu_button_rect.centerx, self.main_menu_button_rect.centery, 215, 100, "Main Menu", "white", "black") #render "Main Menu" text 





    def render(self, display):
        if self.exit_to_menu == True:
            self.exit(display)
        else:
            self.pause(display)
        
                                                  

    
