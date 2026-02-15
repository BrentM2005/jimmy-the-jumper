import json
import pygame
from src.level import Level
from src.config import *

class LevelManager:
    def __init__(self):
        with open('data/levels.json', 'r') as f:
            self.level_data = json.load(f)['levels']
        self.current_level = 0
        self.level = None
        self.high_score = 0
        self.load_current_level()

    def load_current_level(self):
        data = self.level_data[self.current_level]
        data['level_index'] = self.current_level
        self.level = Level.from_data(data)
        return self.level

    def next_level(self):
        if self.current_level < len(self.level_data) - 1:
            self.current_level += 1
            return self.load_current_level()
        return None  
    
    def restart_level(self):
        return self.load_current_level()

    def reset_to_first_level(self):
        self.current_level = 0
        return self.load_current_level()

    def get_current_level_id(self):
        return self.current_level + 1
