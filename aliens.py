import pygame
import os
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self, ai_game):

        super().__init__()    
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        current_dir = os.path.dirname(__file__)
        image_path = os.path.join(current_dir, 'images', 'alien.bmp')
        self.image = pygame.image.load(image_path)

        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    
    def update(self):

        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x