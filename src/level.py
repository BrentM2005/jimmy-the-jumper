import pygame
import math
from src.config import *
from src.platform_obj import Platform
from src.tilemap import TileMap
from src.enemy import Enemy
from src.items import Coin, Goal, PowerUp, Spike
from src.assets import AssetLoader

class Level:
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.tilemap = None
        self.spawn_x = 0
        self.spawn_y = 0
        self.world_width = WORLD_WIDTH
        self.bg_offset = 0
        
        self.bg_image = AssetLoader.load_image("Backgrounds/bg_sky.png", 64, 64, SKY_BLUE)
        self.bg_tree = AssetLoader.load_image("Backgrounds/bg_tree.png", 128, 128, GREEN)
        
        self.time_limit = 90
        self.time_remaining = 90.0

    @classmethod
    def from_data(cls, data, level_index=0):
        level = cls()
        level.spawn_x, level.spawn_y = data['spawn']
        level.world_width = data['goal'][0] + 100
        
        if 'tilemap' in data:
            level.tilemap = TileMap.from_data(data['tilemap'])
            level.tilemap.generate_platforms(level.platforms)
        
        for mplat_data in data.get('moving_platforms', []):
            plat = Platform(*mplat_data)
            plat.move_speed += level_index * 0.5
            level.platforms.add(plat)
        
        if 'platforms' in data:
            for plat_data in data['platforms']:
                if len(plat_data) == 4:
                    plat = Platform(*plat_data)
                else:
                    plat = Platform(*plat_data)
                plat.move_speed += level_index * 0.5
                level.platforms.add(plat)
        
        for e in data['enemies']:
            enemy = Enemy(e[0], e[1], e[2])
            enemy.speed = ENEMY_SPEED + (level_index * 0.5)
            level.enemies.add(enemy)
        
        for c in data['coins']:
            level.coins.add(Coin(*c))
        
        if 'powerups' in data:
            for p in data['powerups']:
                level.powerups.add(PowerUp(p[0], p[1], p[2]))
        
        level.goals.add(Goal(data['goal'][0], data['goal'][1]))
        
        if 'spikes' in data:
            for s in data['spikes']:
                level.spikes.add(Spike(*s))
        
        level.bg_speed = data['bg_speed']
        level.time_limit = data.get('time_limit', 90)
        level.time_remaining = float(level.time_limit)
        return level

    def update(self, player, dt):
        self.platforms.update()
        self.enemies.update()
        self.time_remaining = max(0, self.time_remaining - dt)

    def draw(self, screen, camera):
        tile_size = 64
        parallax = 0.12
        offset_x = int(camera.camera.x * parallax) % tile_size
        if offset_x > 0:
            offset_x -= tile_size
        
        cols = math.ceil(SCREEN_WIDTH / tile_size) + 4
        rows = math.ceil(SCREEN_HEIGHT / tile_size) + 2
        
        for y in range(rows):
            for x in range(cols):
                bx = x * tile_size + offset_x
                by = y * tile_size
                screen.blit(self.bg_image, (bx, by))

        tree_width = 128
        tree_parallax = 0.45
        tree_offset = int(camera.camera.x * tree_parallax) % tree_width
        if tree_offset > 0:
            tree_offset -= tree_width
        
        tree_cols = math.ceil(SCREEN_WIDTH / tree_width) + 4
        tree_y = SCREEN_HEIGHT - 140
        
        for i in range(-1, tree_cols):
            tx = i * tree_width + tree_offset
            screen.blit(self.bg_tree, (tx, tree_y))

        for sprite in self.platforms:
            screen.blit(sprite.image, camera.apply(sprite))
        for sprite in self.goals:
            screen.blit(sprite.image, camera.apply(sprite))
        for sprite in self.powerups:
            screen.blit(sprite.image, camera.apply(sprite))
        for sprite in self.spikes:
            screen.blit(sprite.image, camera.apply(sprite))
        for sprite in self.coins:
            screen.blit(sprite.image, camera.apply(sprite))
        for sprite in self.enemies:
            screen.blit(sprite.image, camera.apply(sprite))