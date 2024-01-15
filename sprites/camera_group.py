import pygame 

class cameraGroup(pygame.sprite.Group):
    def __init__(self,game):
        super().__init__()
        self.DisplaySurface = pygame.display.get_surface()
        self.CameraOffset = pygame.math.Vector2()
        self.HalfWidth = self.game.SCREEN_WIDTH//2
        self.HalfHeight = self.game.SCREEN_HEIGHTt//2

    def centre_player(self, Player):
        self.CameraOffset.x = Player.rect.centerx - self.HalfWidth
        self.CameraOffset.y = Player.rect.centery - self.HalfHeight
        #To keep the player central on the screen, they need to be at a position that is half the width and height of the surface
        #The above function keeps the player in the centre (watch https://www.youtube.com/watch?v=u7LPRqrzry8 from 15:30
        
    
        
    
    def update(self, delta_time, actions):
        self.centre_player()

    def render(self, display, player):
        #old AlteredDraw function
        self.CentrePlayer(player)
        for sprite in self.sprites():
            OffsetPosition = sprite.rect.topleft - self.CameraOffset
            display.blit(sprite.image, OffsetPosition)