import pygame
from src.config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False
        self.lives = 3  
        self.score = 0
        self.double_jump = False  

    def update(self, platforms):
        self.handle_input()
        self.apply_friction()
        self.rect.x += self.vel_x
        self.check_horizontal_collisions(platforms)
        self.apply_gravity()
        self.rect.y += self.vel_y
        self.check_vertical_collisions(platforms)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_POWER
            self.on_ground = False
        elif self.double_jump:
            self.vel_y = JUMP_POWER
            self.double_jump = False

    def apply_gravity(self):
        self.vel_y += GRAVITY

    def apply_friction(self):
        self.vel_x += FRICTION * self.vel_x  

    def check_horizontal_collisions(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits:
            if self.vel_x > 0:
                self.rect.right = hit.rect.left
            elif self.vel_x < 0:
                self.rect.left = hit.rect.right
        if hits:
            self.vel_x = 0

    def check_vertical_collisions(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.on_ground = False
        for hit in hits:
            if self.vel_y > 0:
                self.rect.bottom = hit.rect.top
                self.vel_y = 0
                self.on_ground = True
            elif self.vel_y < 0:
                self.rect.top = hit.rect.bottom
                self.vel_y = 0

    def respawn(self, spawn_x, spawn_y):
        self.rect.topleft = (spawn_x, spawn_y)
        self.vel_x = self.vel_y = 0
        self.on_ground = False