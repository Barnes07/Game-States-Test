import pygame 

from sprites.artifact import Artifact
from sprites.flute import Flute

class CameraGroup(pygame.sprite.Group):
    def __init__(self,game):
        super().__init__()
        self.game = game
        self.DisplaySurface = pygame.display.get_surface()
        self.CameraOffset = pygame.math.Vector2()
        self.HalfWidth = self.game.SCREEN_WIDTH//2
        self.HalfHeight = self.game.SCREEN_HEIGHT//2

    def centre_player(self, player):
        self.CameraOffset.x = player.rect.centerx - self.HalfWidth
        self.CameraOffset.y = player.rect.centery - self.HalfHeight
        
    def update(self, delta_time, actions):
        for sprite in self.sprites():
            if isinstance(sprite, Artifact): #only calls update method for artifact 
                sprite.update()
            if isinstance(sprite, Flute): #only calls update method for flute
                sprite.update()


    def render(self, display, player):
        #old AlteredDraw function
        self.centre_player(player)
        for sprite in self.sprites():
            OffsetPosition = sprite.rect.topleft - self.CameraOffset
            display.blit(sprite.current_image, OffsetPosition)
    
    




