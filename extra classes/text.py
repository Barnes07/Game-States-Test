import pygame 
import os

class text():
        def __init__(self, surface, x, y, width, height, text, colour, background_colour):
            self.surface = surface 
            self.background_colour = background_colour
            self.text = self.font.render(text, False, colour)
            self.text_rect = text.get_rect(center = (x,y))
            self.text_background = pygame.Rect(x-(width//2), y-(height//2), width, height)
            
        
        def render(self):
            pygame.draw.rect(self.surface, self.background_colour, self.text_background, border_radius = 10)
            self.surface.blit(text, self.text_rect)
              