import pygame
from src.config import *
from src.assets import AssetLoader

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = AssetLoader.load_image("coin.png", 24, 24, YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, type_name="double_jump"):
        super().__init__()
        self.type = type_name
        color = ORANGE if type_name == "double_jump" else PURPLE if type_name == "invincibility" else YELLOW
        self.image = AssetLoader.load_image(f"powerup_{type_name}.png", 24, 24, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 80), pygame.SRCALPHA)
        
        pole = AssetLoader.load_image("goal.png", 20, 40, PURPLE)
        flag = AssetLoader.load_image("goal_top.png", 20, 20, PURPLE)
        
        self.image.blit(pygame.transform.scale(pole, (10, 80)), (15, 0))
        self.image.blit(flag, (15, 0))
        
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = AssetLoader.load_image("spikes.png", 32, 32, RED)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)