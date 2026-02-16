import pygame
import os
from src.config import *

class AssetLoader:
    _images = {}
    _sounds = {}

    @staticmethod
    def load_image(name, width, height, color):
        if name in AssetLoader._images:
            return AssetLoader._images[name]

        path = os.path.join("assets", "images", name)
        try:
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, (width, height))
        except (pygame.error, FileNotFoundError):
            image = pygame.Surface((width, height))
            image.fill(color)
            pygame.draw.rect(image, BLACK, image.get_rect(), 2)
        
        AssetLoader._images[name] = image
        return image

    @staticmethod
    def load_sound(name):
        if name in AssetLoader._sounds:
            return AssetLoader._sounds[name]

        path = os.path.join("assets", "sounds", name)
        try:
            sound = pygame.mixer.Sound(path)
        except (pygame.error, FileNotFoundError):
            sound = None
        
        AssetLoader._sounds[name] = sound
        return sound