# Author    : Gary Godfrey
# Date      : 5th Oct 2021
# Desc      : The Settings module for the Alien Invasion project in
#           : Python Crash Course.

class Settings:
    """A class to store all settings for the Alien Invasion game."""

    def __init__(self):
        """Initialise the game's static settings"""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # File settings
        self.filename = "ai_high_score.txt"

        # Ship settings
        self.ship_limit = 2

        # Bullet settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        
        # How quickly the alien score value increases
        self.score_scale = 1.5

        self.initialise_dynamic_settings()

    def initialise_dynamic_settings(self):
        """Initialise settings that change through the game"""
        # Speed settings
        self.ship_speed = 1.5
        self.bullet_speed = 2.0
        self.alien_speed = 1

        # Scoring
        self.alien_points = 50

        # Fleet direction, 1 represents right; -1 represts left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed and alien point settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        # print("Ship", self.ship_speed, "Bullet", self.bullet_speed, "Alien", self.alien_speed, "Score", self.alien_points)
