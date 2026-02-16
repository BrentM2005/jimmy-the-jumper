import pygame
from src.platform_obj import Platform

class TileMap:
    def __init__(self, tile_size, grid):
        self.tile_size = tile_size
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0

    @classmethod
    def from_data(cls, data):
        return cls(data['tile_size'], data['grid'])

    def generate_platforms(self, platforms_group):
        platforms_group.empty()
        for r in range(self.rows):
            c = 0
            while c < self.cols:
                if self.grid[r][c] == 1:
                    start_c = c
                    while c < self.cols and self.grid[r][c] == 1:
                        c += 1
                    w = (c - start_c) * self.tile_size
                    x = start_c * self.tile_size
                    y = r * self.tile_size
                    plat = Platform(x, y, w, self.tile_size)
                    platforms_group.add(plat)
                else:
                    c += 1