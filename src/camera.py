from src.config import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """Returns a new rect shifted by the camera offset."""
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        """Follow the target (player)"""
        x = -target.rect.x + int(SCREEN_WIDTH / 2)
        y = -target.rect.y + int(SCREEN_HEIGHT / 2)

        # Scrolling limited to map size
        x = min(0, x)  
        x = max(-(self.width - SCREEN_WIDTH), x)  
        y = max(-(self.height - SCREEN_HEIGHT), y) 
        y = min(0, y)  

        self.camera = pygame.Rect(x, y, self.width, self.height)