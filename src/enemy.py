import pygame
from src.config import *
from src.assets import AssetLoader

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, distance):
        super().__init__()
        self.image = AssetLoader.load_image("Characters/enemy.png", 32, 32, RED)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y) 
        
        self.start_x = x
        self.max_dist = distance
        self.speed = ENEMY_SPEED
        self.direction = 1 

    def update(self):
        img = AssetLoader.load_image("Characters/enemy.png", 32, 32, RED)
        if self.direction < 0:
            self.image = pygame.transform.flip(img, True, False)
        else:
            self.image = img
            
        self.rect.x += self.speed * self.direction
        
        dist_traveled = abs(self.rect.x - self.start_x)
        if dist_traveled > self.max_dist:
            self.direction *= -1