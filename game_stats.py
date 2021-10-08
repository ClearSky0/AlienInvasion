# Author    : Gary Godfrey
# Date      : 8th Oct 2021
# Desc      : Game Stats module for the Alien Invasion project
#           : in the Python Crash Course book.

class GameStats:
    """Track statustucs for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialise statistics"""

        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an active state
        self.game_active = True

    def reset_stats(self):
        """Initisalise statistcs that can change during the game"""
        self.ships_left = self.settings.ship_limit