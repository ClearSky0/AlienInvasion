# Author    : Gary Godfrey
# Date      : 5th Oct 2021
# Desc      : The is the main program for the Alien Invasion project in
#           : Python Crash Course.
#
# Mods      : 8th Oct - Shooting & destroying the aliens
#           : 8th Oct - Game Statistics
#           : 11th Oct - Game starting, stopping & scoring

# Standard library imports

# Use the amazing traceback from the rich library to catch and show errors
# much more clearly and easier to read.
from pygame.constants import K_RETURN, K_p
from rich.traceback import install
install(show_locals=True)

import  sys
import  pygame.mouse
import  pygame.sprite      # Added to get intellisense to work for the sprite methods
from    time        import sleep

# Custom imports

from    settings    import Settings
from    ship        import Ship
from    bullet      import Bullet
from    alien       import Alien
from    game_stats  import GameStats
from    button      import Button
from    scoreboard  import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialise the game and create game resources."""
        pygame.init()
        self.settings = Settings()

        # Windowed
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        # Fullscreen
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics
        #   and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.sb.prep_ships()

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()

        # Make the play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()

            self._update_aliens()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks on Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()
    
    def _start_game(self):
        """Check if a game is already in play before resetting the game"""
        if not self.stats.game_active:
            # Reset the game settings
            self.settings.initialise_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.centre_ship()

            # Hide the mouse pointer
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == K_RETURN or event.key == K_p:
            # I thouhgt I was being proactive with this but it's part of exercise 14.1
            self._start_game()


    def _check_keyup_events(self,event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        # Update bullet position
        self.bullets.update()

        # Get rid of bullets that have gone off the top of the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        # Check for any bullets that have hit aliens.
        #  If so, get rid of the bullet and the alien.

        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            # print(collisions)
            for aliens in collisions.values():
                # Make sure that we count all the hit aliens
                self.stats.score += self.settings.alien_points * len (aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens: # the aliens group is empty
            # Destroy existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
            # Increase the game speed
            self.settings.increase_speed()

            # Inscrease level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Check if the fleet is at the an edge,
            then update the position of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens landing
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Create an alien and find out how many can fit on a row
        # Space between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # Subtracted 1 from screen width to avoid situation when width is exactly divisible by alien - GG
        available_space_x = (self.settings.screen_width - 1) - (2 * alien_width)
        number_aliens_x = (self.settings.screen_width - 1) // (2 * alien_width)

        # Determing the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                            (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """ Create an alien and place it in the row """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit (aliens have landed)
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        if self.stats.game_active: # If not active the aliens should bound back and forth (Demo mode)
            for alien in self.aliens.sprites():
                alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        # Helper Method
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        
        # Draw the scoreboard
        self.sb.show_score()
        
        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""

        # Pause to let the player see they've been hit/had an alien land

        if self.stats.ships_left > 0:
            # Decrement ships left & update the lives left (scoreboard)
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and centre the ship
            self._create_fleet()
            self.ship.centre_ship()

            # Pause to let the player regroup
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

        
if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()