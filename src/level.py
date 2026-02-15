import pygame
from src.config import *
from src.platform_obj import Platform
from src.enemy import Enemy
from src.items import Coin, Goal

class Level:
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.spawn_x = 0
        self.spawn_y = 0
        self.world_width = WORLD_WIDTH
        self.bg_offset = 0
        self.time_limit = 90
        self.time_remaining = float(self.time_limit)

    @classmethod
    def from_data(cls, data, level_index=0):  
        level = cls()
        level.spawn_x, level.spawn_y = data['spawn']
        level.world_width = data['goal'][0] + 100
        
        for plat in data['platforms']:
            level.platforms.add(Platform(*plat))
        
        for e in data['enemies']:
            enemy = Enemy(e[0], e[1], e[2])
            enemy.speed = ENEMY_SPEED + (level_index * 0.5)
            level.enemies.add(enemy)
            
        for c in data['coins']:
            level.coins.add(Coin(*c))

        level.goals.add(Goal(data['goal'][0], data['goal'][1]))
        level.bg_speed = data['bg_speed']
        level.time_limit = data.get('time_limit', 90)
        level.time_remaining = float(level.time_limit)
        return level

    def update(self, player, dt):
        self.enemies.update()
        self.bg_offset += self.bg_speed
        self.time_remaining = max(0, self.time_remaining - dt)

    def draw(self, screen, camera):
        for i in range(SCREEN_HEIGHT // 2):
            color = (135, 206 - i // 3, 235)
            pygame.draw.line(screen, color, (0, i), (SCREEN_WIDTH, i))

        ground_y = SCREEN_HEIGHT - 40
        pygame.draw.rect(screen, GREEN, (self.bg_offset % SCREEN_WIDTH - SCREEN_WIDTH, ground_y, SCREEN_WIDTH * 2, 40))

        for sprite in self.platforms:
            screen.blit(sprite.image, camera.apply(sprite))
        for sprite in self.enemies:
            screen.blit(sprite.image, camera.apply(sprite))
        for sprite in self.coins:
            screen.blit(sprite.image, camera.apply(sprite))
        for sprite in self.goals:
            screen.blit(sprite.image, camera.apply(sprite))