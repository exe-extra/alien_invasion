import pygame
import os
from settings import Settings


class Ship:

    def __init__(self, ai_game):

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        current_dir = os.path.dirname(__file__)
        image_path = os.path.join(current_dir, 'images', 'ship.bmp')
        self.image = pygame.image.load(image_path)

        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def update(self):

        if self.moving_right:
            self.x += self.settings.ship_speed
        if self.moving_left:
            self.x -= self.settings.ship_speed

        if self.x < 0:
            self.x = 0
        if self.x > self.screen_rect.width - self.rect.width:
            self.x = self.screen_rect.width - self.rect.width
        
        self.rect.x = self.x
    
    def center_ship(self):

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):

        self.screen.blit(self.image, self.rect)