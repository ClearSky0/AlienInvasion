# Author    : Gary Godfrey
# Date      : 5th Oct 2021
# Desc      : Ship module
#           : Python Crash Course.
#
# Mods      : 11th Oct - added code to help display number of ships (lives)

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship"""

    def __init__(self, ai_game):
        """Initialise the ship and set its starting position"""
        super().__init()
        
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the left centre of the screen
        self.rect.midleft = self.screen_rect.midleft

        # Store a decimal value for the ship's horizontal position
        self.y = float(self.rect.y)

        # Movement flag
        self.moving_down = False
        self.moving_up = False

    def update(self):
        """Update the ship's position based on the movement flag"""
        # Update the ship's y value, not the rect

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed

        # update the rect object from self.y
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
