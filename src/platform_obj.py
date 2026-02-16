import pygame
from src.config import *
from src.assets import AssetLoader

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, move_range=0, move_speed=1.0):
        super().__init__()
        
        self.start_x = x
        self.move_range = move_range
        self.move_speed = move_speed
        self.direction = 1
        self.vel_x = 0.0
        
        self.grass_img = AssetLoader.load_image("grass.png", 20, 20, GREEN)
        self.dirt_img = AssetLoader.load_image("dirt.png", 20, 20, (101, 67, 33))
        
        self.image = pygame.Surface((width, height))
        
        for i in range(0, width, 20):
            self.image.blit(self.grass_img, (i, 0))
            
        for j in range(20, height, 20):
            for i in range(0, width, 20):
                self.image.blit(self.dirt_img, (i, j))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.move_range > 0:
            self.vel_x = self.move_speed * self.direction
            self.rect.x += self.vel_x
            if abs(self.rect.x - self.start_x) > self.move_range:
                self.direction *= -1
        else:
            self.vel_x = 0.0