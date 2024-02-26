import pygame
import os 
import random
from states.state import State
from states.game_over import Game_Over


class Flute_Playing(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game 
        self.flute_playing_image = pygame.image.load(os.path.join(self.game.assets_dir, "flute", "flute_playing.png"))
        self.flute_playing_image_rect = self.flute_playing_image.get_rect(center = (self.game.SCREEN_WIDTH//2, (self.game.SCREEN_HEIGHT//2)))

        self.current_key = "a"

        self.time_since_last_key = 0

        self.flag = False

        self.keys_pressed = 0


    def display_random_key(self, display):
        self.game.text(display, (self.game.SCREEN_WIDTH)/2, (self.game.SCREEN_HEIGHT)/2 - 200, 215, 100, self.current_key, "white", "black")

    def generate_random_key(self,):
        random_letter = random.randint(1,5)
        if random_letter == 1:
            self.current_key = "a"
        if random_letter == 2:
            self.current_key = "b"
        if random_letter == 3:
            self.current_key = "c"
        if random_letter == 4:
            self.current_key = "d"
        if random_letter == 5:
            self.current_key = "e"

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
            new_state = Game_World(self.game)
            new_state.enter_state()
        self.time_since_last_key += delta_time
        if self.time_since_last_key > 3:
            if self.flag == False:
                new_state = Game_Over(self.game)
                new_state.enter_state()
            self.time_since_last_key = 0
            self.generate_random_key()
            self.flag = False
        if self.check_pressed_key():
            self.flag = True
            print("true")
            self.time_since_last_key = 4
            self.keys_pressed += 1

    def update(self, delta_time, actions):
        self.main(delta_time)

    def render(self, display):
        display.fill("black")
        display.blit(self.flute_playing_image, self.flute_playing_image_rect)

        self.display_random_key(display)
