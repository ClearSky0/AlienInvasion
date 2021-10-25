# Author    : Gary Godfrey
# Date      : 8th Oct 2021
# Desc      : Game Stats module for the Alien Invasion project
#           : in the Python Crash Course book.
#
# Mods      : 8th Oct - Start in inactive state
#           : 22nd Oct - Added level to high score and file
#               Moved save scores here to encapsulate file handing. This module could be reused
#           

class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialise statistics"""

        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an active state
        self.game_active = False

        self._set_high_scores()

    def _set_high_scores(self):
        """Attempt to load the high score file or reset the high score and level"""
        # High score should never be reset. This is a helper module because high
        # scores are only set once at start of program.

        try:
            with open(self.settings.filename, 'r') as file_object:
                file_high_score = file_object.readline()
                self.high_score = int(file_high_score.rstrip())
                file_high_level = file_object.readline()
                self.high_level = int(file_high_level.rstrip())
        except:
            self.high_score = 0
            self.high_level = 1

    def save_high_score(self):
        """Save the high scores (Calling program responsible for maintaining high)"""

        with open(self.settings.filename, 'w') as file_object:
            # file_object.write([str(self.stats.high_score), str(self.stats.high_level)])
            file_object.write(str(self.high_score) + "\n")
            file_object.write(str(self.high_level) + "\n")

    def reset_stats(self):
        """Initialise statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1