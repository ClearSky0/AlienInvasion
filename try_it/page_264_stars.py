# Seriously quick go at the execises on page 264 of Python Crash Course book
# Gary Godfrey  7th Oct 2021

import sys

import pygame
from random import randint
from pygame.sprite import Sprite


class Settings:
    """A class to store all settings for the Alien Invasion game."""

    def __init__(self):
        """Initialise the game's settings"""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed = 1.5

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3



class Alien(Sprite):
    """A class to represent a single star"""

    def __init__(self, ai_game):
        """Initialise the alient and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/star_sml.png')
        # self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()

        # Start each new alien new the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)
    


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialise the game and create game resources."""
        pygame.init()
        self.settings = Settings()

        # Windowed
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        # Fullscreen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Stars")

        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """Respond to keyboard and mouse events"""
        # Helper Method
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self,event):
        """Respond to key presses"""
        if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self,event):
        """Respond to key releases"""

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Create an alien and find out how many can fit on a row
        # Space between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        available_space_x = (self.settings.screen_width) - (2 * alien_width)
        number_aliens_x = (self.settings.screen_width) // (2 * alien_width)

        # Determing the number of rows of aliens that fit on the screen
        available_space_y = self.settings.screen_height - alien_height
        number_rows = available_space_y // alien_height

        # Create the fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """ Create an alien and place it in the row """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.y = alien.rect.height + 2 * alien.rect.height * row_number

        rand_x = randint(-alien_width // 2, +alien_width // 2)
        rand_y = randint(-alien_height // 2, +alien_height // 2)

        alien.rect.x = alien.x + rand_x
        alien.rect.y = alien.y + rand_y

        self.aliens.add(alien)
        
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        # Helper Method
        self.screen.fill(self.settings.bg_color)

        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
