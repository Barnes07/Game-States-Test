import pygame 
import os 
import time

from states.title import Title

pygame.display.set_caption('Snake Charmer')

class Game(): #Talkthrough of class logic: https://www.youtube.com/watch?v=b_DkQrJxpck&t=331s
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 1408
        self.SCREEN_HEIGHT = 768
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT), pygame.SCALED, vsync=1)
        self.running = True
        self.playing = True
        self.actions = {"escape": False, "left": False, "right": False, "up": False, "down": False, "click":False, "mouse_pos":(0,0), "start": False, "action1": False, "flute": False}
        self.delta_time = 0
        self.previous_time = 0
        self.states_stack = [] #Check clip for why stacks are used
        self.load_assets()
        self.load_states()
        self.block_size = 64
    
    def game_loop(self):
        while self.playing == True:
            self.get_delta_time()
            self.get_events()
            self.update()
            self.render()

        
    
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                      #Checks whether window has been closed 
                self.playing = False
                self.running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                #Setting all actions to True when pressed
                if event.key == pygame.K_ESCAPE:
                    self.actions["escape"] = True
                if event.key == pygame.K_w:
                    self.actions["up"] = True 
                if event.key == pygame.K_a:
                    self.actions["left"] = True 
                if event.key == pygame.K_s:
                    self.actions["down"] = True 
                if event.key == pygame.K_d:
                    self.actions["right"] = True 
                if event.key == pygame.K_RETURN:
                    self.actions["start"] = True
                if event.key == pygame.K_o:
                    self.actions["action1"] = True
                if event.key == pygame.K_f:
                    self.actions["flute"] = True
            if event.type == pygame.KEYUP:
                #Setting all actions to False when released
                if event.key == pygame.K_ESCAPE:
                    self.actions["escape"] = False 
                if event.key == pygame.K_w:
                    self.actions["up"] = False 
                if event.key == pygame.K_a:
                    self.actions["left"] = False  
                if event.key == pygame.K_s:
                    self.actions["down"] = False  
                if event.key == pygame.K_d:
                    self.actions["right"] = False 
                if event.key == pygame.K_RETURN:
                    self.actions["start"] = False 
                if event.key == pygame.K_o:
                    self.actions["action1"] = False
                if event.key == pygame.K_f:
                    self.actions["flute"] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Setting value of mouse click
                self.actions["click"] = True
                self.actions["mouse_pos"] = pygame.mouse.get_pos()
                



    def update(self):
        self.states_stack[-1].update(self.delta_time, self.actions)

    def render(self):
        self.states_stack[-1].render(self.screen)
        pygame.display.flip()

    def get_delta_time(self):
        now = time.time()
        self.delta_time = now - self.previous_time
        self.previous_time = now

    def text(self, surface, x, y, width, height, text, colour, background_colour):
        text = self.font.render(text, False, colour)
        text_rect = text.get_rect(center = (x,y))
        text_background = pygame.Rect(x-(width//2), y-(height//2), width, height)
        pygame.draw.rect(surface, background_colour, text_background, border_radius = 10)
        surface.blit(text, text_rect)
        
          
    
    def load_assets(self):
        #Instantiate pointers to directories
        self.assets_dir = os.path.join("assets")
        self.sprite_dir = os.path.join(self.assets_dir, "sprites")
        self.font_dir = os.path.join(self.assets_dir, "fonts")
        self.font = pygame.font.Font(os.path.join(self.font_dir, "Pixeltype.ttf"), 50)

    def load_states(self):
        self.title_screen = Title(self)
        self.states_stack.append(self.title_screen)

if __name__ == "__main__":
    g = Game()
    while g.running == True:
        g.game_loop()