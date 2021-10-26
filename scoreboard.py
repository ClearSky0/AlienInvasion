# Author    : Gary Godfrey
# Date      : 5th Oct 2021
# Desc      : The Settings module for the Alien Invasion project in
#           : Python Crash Course.
# Mods      : 22nd Oct - Didn't like the layout of score and level, used : instead
#           : 25th Oct - Display accuracy percentage and init ships here
#               Also refactor the image prep calls in init into a single image init
#               Repositioned accuracy after score over-wrote it

import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, ai_game):
        """Initialise scorekeeping attributes"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_images()

    def prep_images(self):
        # Prepare the initial score images
        self.prep_score()
        self.prep_high_score()
        self.prep_ships()
        self.prep_accuracy()

    def prep_score(self):
        """Turn the score into a rendered image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score) + " : " + str(self.stats.level)
        self.score_image = self.font.render(score_str, True,
            self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high-score & linked high-level into a rendered image"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score) + " : " + str(self.stats.high_level)
        self.high_score_image = self.font.render(high_score_str, True,
            self.text_color, self.settings.bg_color)

        # Centre high score at top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_accuracy(self):
        """Turn the accuracy into a rendered image"""
        # accuracy_str = str(self.stats.bullets_fired) + " : " + str(self.stats.bullets_on_target)
        if self.stats.bullets_fired != 0:
            accuracy_str = str(round((self.stats.bullets_on_target / self.stats.bullets_fired) * 100, 2)) + "%"
        else:
            accuracy_str = "100%"
        self.accuracy_image = self.font.render(accuracy_str, True,
            self.text_color, self.settings.bg_color)

        # Display the accuracy at the top right of the screen
        self.accuracy_rect = self.accuracy_image.get_rect()
        self.accuracy_rect.right = self.screen_rect.right - 300
        self.accuracy_rect.top = 20

    def prep_ships(self):
        """Show how many lives are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Draw the scores, level and ships to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.accuracy_image, self.accuracy_rect)
        # self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check to see if there is a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.stats.high_level = self.stats.level
            self.prep_high_score()