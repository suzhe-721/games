class GameStats():
    def __init__(self,my_settings):
        self.my_settings = my_settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        self.ship_left = self.my_settings.ship_limit
        self.score = 0
        self.level = 1
        self.high_score = 0

