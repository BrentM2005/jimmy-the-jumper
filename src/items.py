import pygame
from src.config import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Placeholder: Yellow circle
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW) 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Placeholder: Green Portal/Flag
        self.image = pygame.Surface((40, 60))
        self.image.fill(PURPLE) 
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)