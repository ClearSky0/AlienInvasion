# Author    : Gary Godfrey
# Date      : 8th Oct 2021
# Desc      : Game Stats module for the Alien Invasion project
#           : in the Python Crash Course book.
#
# Mods      : 8th Oct - Start in inactive state

class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialise statistics"""

        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an active state
        self.game_active = False

        # High score should never be reset
        try:
            with open(self.settings.filename, 'r') as file_object:
                file_high_score = file_object.readline()
                self.high_score = int(file_high_score.rstrip())
        except:
            self.high_score = 0

    def reset_stats(self):
        """Initialise statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 0 