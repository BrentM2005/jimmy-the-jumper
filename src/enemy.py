import pygame
from src.config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, distance):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.start_x = x
        self.max_dist = distance
        self.speed = ENEMY_SPEED  
        self.direction = 1 

    def update(self):
        self.rect.x += self.speed * self.direction
        
        dist_traveled = abs(self.rect.x - self.start_x)
        if dist_traveled > self.max_dist:
            self.direction *= -1
            self.start_x = self.rect.x  